"""Label batches v2: one cumulative, fast lookup at the fixed-cell label renderer (supersedes v1 chaining).

v1 chained one linear full-bytes wrapper per batch at 0x554A4/0x554DC; measured 057 cost up to ~20,000
instructions per label call (near-identical subchip/comm archives share long prefixes), which dropped menu
input frames on the own coldboot. v2 installs, per batch, a single wrapper per site that holds ALL label
mappings so far and falls back straight to the original trampoline:
  * ROM r0: binary search over sorted (root, clone, script_count).
  * EWRAM r0: linear over entries with 8 sampled bytes (offset,value). Offsets are chosen at build time so
    every other payload that can sit at a label root (all catalog LZ natives and every LZ payload the
    predecessor delivers for any catalog archive) differs from the entry at one sampled offset inside its
    own length; entries that cannot be discriminated that way are left on the native path.
The 4FB4C dialogue chain is unchanged (generic Component).
"""
import struct
from collections import defaultdict
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL
from verify_tpi_index import parse_tpi,lz77_decompress
from compare_archive_payloads import payload_of
from batch_generic_v1 import Component
from batch_label_v1 import SITES,ALLOWED,previous_label

SAMPLES=8
RAM_ENTRY=8+4*SAMPLES
CODE='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
lsrs r2,r1,#8
bne fallback
lsrs r2,r0,#24
cmp r2,#8
beq romsearch
lsrs r2,r0,#18
cmp r2,#0x80
bne fallback
ldr r3,ramtab
ldr r7,ramcount
cmp r7,#0
beq fallback
ramloop:
ldrh r4,[r3,#4]
cmp r1,r4
bhs ramnext
movs r6,#8
movs r5,#8
adds r5,r5,r3
samp:
ldrh r4,[r5]
ldrb r4,[r0,r4]
ldrb r2,[r5,#2]
cmp r4,r2
bne ramnext
adds r5,#4
subs r6,#1
bne samp
ldr r4,[r3]
str r4,[sp]
b fallback
ramnext:
adds r3,#40
subs r7,#1
bne ramloop
b fallback
romsearch:
movs r2,#0
ldr r3,romcount
bsloop:
cmp r2,r3
bhs fallback
adds r4,r2,r3
lsrs r4,r4,#1
movs r5,#12
muls r5,r4,r5
ldr r6,romtab
adds r6,r6,r5
ldr r5,[r6]
cmp r0,r5
beq found
bhi higher
movs r3,r4
b bsloop
higher:
adds r2,r4,#1
b bsloop
found:
ldr r5,[r6,#8]
cmp r1,r5
bhs fallback
ldr r5,[r6,#4]
str r5,[sp]
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''


def label_wrap(address,romtab,romcount,ramtab,ramcount,previous):
    blob,proof=assemble_verified(CODE,address,dict(ramtab=ramtab,ramcount=ramcount,romtab=romtab,romcount=romcount,previous=previous|1))
    return blob,dict(proof=proof,rom_entry_bytes=12,ram_entry_bytes=RAM_ENTRY,samples=SAMPLES,persistent_ram_bytes=0,stack_bytes=32)


def choose_samples(p,others):
    """Greedy offsets in p so each q in others differs at a chosen offset < len(q); None if impossible."""
    rem=[q for q in others if q!=p];chosen=[]
    while rem:
        best=None;bestn=0
        for off in range(len(p)):
            n=sum(1 for q in rem if off<len(q) and q[off]!=p[off])
            if n>bestn:best,bestn=off,n
        if best is None or len(chosen)==SAMPLES:return None
        chosen.append(best);rem=[q for q in rem if not (best<len(q) and q[best]!=p[best])]
    while len(chosen)<SAMPLES:chosen.append(chosen[0] if chosen else 0)
    if any(o>0xFFFF for o in chosen):return None
    return chosen


class FastLabelComponent(Component):
    def extra_rom_roots(self,image,keymeta):return {}

    def install(self,source,appended,key_patches,keymeta,inputs,common,plugins,work):
        offsets=[p[0] for p in key_patches]
        if offsets.count(INSTALL)!=1 or set(offsets)-ALLOWED or len(set(offsets))!=len(offsets):raise ValueError(self.batch+' predecessor patch set')
        carried={p[0]:p for p in key_patches if p[0]!=INSTALL};main=[p for p in key_patches if p[0]==INSTALL]
        tail,patches,keymeta,records=super().install(source,appended,main,keymeta,inputs,common,plugins,work)
        tail=bytearray(tail);image=bytes(source)+bytes(tail);base=(ROOT/self.base).read_bytes()
        def rd(addr,n):at=addr-0x08000000;return image[at:at+n]
        def place(blob):
            tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);tail.extend(blob);return at
        # label archives = catalog archives whose source TPL has any mmbn45s script
        cfg=read('project.json');catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
        def is_label(arc):
            p=ROOT/'analysis/full_scope_v1/source_tpl'/(arc+'.tpl')
            return p.exists() and ' mmbn45s {' in p.read_text(encoding='utf-8-sig')
        # newest clone per archive across every typed/generic batch (higher batch wins)
        latest={}
        for k,v in keymeta.items():
            if k.startswith('typed') and k[5:].isdigit() and isinstance(v,dict) and 'placements' in v and int(k[5:])>=41:
                for p in v['placements']:
                    for arc in p.get('archives',[]):
                        if arc not in latest or latest[arc][0]<int(k[5:]):latest[arc]=(int(k[5:]),p['clone'],p['script_count'])
        rom_map={};ram_map={}
        for k,v in keymeta.items():
            if k.startswith('typed') and k[5:].isdigit() and isinstance(v,dict) and 'placements' in v and int(k[5:])>=41:
                for p in v['placements']:
                    arcs=[a for a in p.get('archives',[]) if is_label(a)]
                    if not arcs:continue
                    _,clone,count=latest[arcs[0]]
                    if any(latest[a][1]!=clone for a in arcs):continue
                    if p['root']>=0x08000000 and not p.get('match_sha256'):rom_map[p['root']]=(clone,count)
                    else:
                        body=rd(p['match'],p['match_length'])
                        if sha(body)!=p['match_sha256']:raise ValueError(self.batch+' match copy')
                        ram_map[sha(body)]=(body,clone,count,arcs[0])
        # every LZ payload that can sit at a RAM label root: all catalog natives + predecessor-delivered LZ payloads
        others={}
        for arc,row in catalog.items():
            if not row['compressed']:continue
            n=payload_of(source,row);others[sha(n)]=n
            for ptr in row['pointers']:
                v=int.from_bytes(base[ptr:ptr+4],'little')
                if v!=0x08000000+row['offset'] and 0x08000000<=v<0x08000000+len(base):
                    try:d=lz77_decompress(base,v-0x08000000)[0];others[sha(d)]=d
                    except Exception:pass
        for body,*_ in ram_map.values():others[sha(body)]=body
        ram_entries=[];skipped=[]
        for h,(body,clone,count,arc) in sorted(ram_map.items(),key=lambda x:x[1][3]):
            offs=choose_samples(body,list(others.values()))
            if offs is None:skipped.append(arc);continue
            ram_entries.append(struct.pack('<IHH',clone,count,0)+b''.join(struct.pack('<HBB',o,body[o],0) for o in offs))
        rom_map.update(self.extra_rom_roots(image,keymeta))   # v4+: static pool roots; empty for 057..064
        rom_entries=[struct.pack('<III',r,c,n) for r,(c,n) in sorted(rom_map.items())]
        romtab=0x08000000+place(b''.join(rom_entries) or b'\0'*12);ramtab=0x08000000+place(b''.join(ram_entries) or b'\0'*RAM_ENTRY)
        n=keymeta[self.key];hooks={}
        for site,spec in SITES.items():
            if source[site:site+spec['size']].hex()!=spec['source_hex']:raise ValueError(self.batch+' label site source bytes %X'%site)
            prev=previous_label(keymeta,site)
            first=None
            for k,v in keymeta.items():
                hk=v.get('label_hooks',{}).get(str(site)) if isinstance(v,dict) else None
                if hk and hk.get('trampoline'):first=hk['trampoline']
            if prev is None or first is None:raise ValueError(self.batch+' v2 needs the v1 trampoline already installed')
            preceding=bytes.fromhex(prev['final_stub_hex'])
            if carried.get(site,(None,None))[1]!=preceding:raise ValueError(self.batch+' carried label stub %X'%site)
            tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail)
            code,proof=label_wrap(0x08000000+at,romtab,len(rom_entries),ramtab,len(ram_entries),0x08000000+first['offset'])
            tail.extend(code);entry=at;pre=None
            if spec['pre']:
                tail.extend(b'\xff'*(-len(tail)%4));entry=len(source)+len(tail)
                pcode,pproof=assemble_verified(spec['pre'],0x08000000+entry,dict(wrapper=0x08000000+at+1));tail.extend(pcode);pre=dict(offset=entry,bytes=len(pcode),sha256=sha(pcode),proof=pproof)
            stub,sproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+site,dict(target=0x08000000+entry+1))
            if len(stub)!=spec['size']:raise ValueError(self.batch+' label stub size')
            hooks[str(site)]=dict(version=2,pre=pre,code_offset=at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=0x08000000+first['offset'],wrapper=proof,stub=sproof,preceding_stub_hex=preceding.hex(),final_stub_hex=stub.hex(),trampoline=None)
            patches.append((site,stub,self.batch+' v2 cumulative label lookup %X'%site))
        if len(source)+len(tail)>0x02000000:raise ValueError(self.batch+' extent')
        n['label_hooks']=hooks;n['label_lookup']=dict(romtab=romtab,rom_entries=len(rom_entries),ramtab=ramtab,ram_entries=len(ram_entries),rom_sha256=sha(b''.join(rom_entries)),ram_sha256=sha(b''.join(ram_entries)),skipped_not_discriminable=skipped,others_compared=len(others),rule='ROM exact root binary search; EWRAM 8 sampled bytes that separate the entry from every catalog LZ payload variant')
        return bytes(tail),patches,keymeta,records

    def predecessor_view(self,source,target,keymeta):
        n=keymeta[self.key];target=bytearray(target)
        for site,h in n.get('label_hooks',{}).items():
            site=int(site);size=SITES[site]['size']
            if target[site:site+size]!=bytes.fromhex(h['final_stub_hex']):raise ValueError(self.batch+' label final stub')
            target[site:site+size]=bytes.fromhex(h['preceding_stub_hex'])
        return super().predecessor_view(source,bytes(target),keymeta)

    def verify_final(self,source,target,keymeta):
        super().verify_final(source,target,keymeta);n=keymeta[self.key];L=n['label_lookup']
        if sha(target[L['romtab']-0x08000000:L['romtab']-0x08000000+12*L['rom_entries']])!=L['rom_sha256'] or sha(target[L['ramtab']-0x08000000:L['ramtab']-0x08000000+RAM_ENTRY*L['ram_entries']])!=L['ram_sha256']:raise ValueError(self.batch+' label tables')
        for site,h in n['label_hooks'].items():
            code,_=label_wrap(0x08000000+h['code_offset'],L['romtab'],L['rom_entries'],L['ramtab'],L['ram_entries'],h['previous_wrapper_address'])
            if sha(code)!=h['code_sha256'] or target[h['code_offset']:h['code_offset']+len(code)]!=code:raise ValueError(self.batch+' label wrapper code')
            pr=h.get('pre')
            if pr and sha(target[pr['offset']:pr['offset']+pr['bytes']])!=pr['sha256']:raise ValueError(self.batch+' label pre-code')
        return True
