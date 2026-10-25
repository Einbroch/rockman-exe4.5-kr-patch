"""Label (mmbn45s) batches: the generic component plus root/full-bytes wrappers on the fixed-cell label renderer.

The label renderer entries 0x080554A4 (98 callers) and the shared 0x080554C8/0x080554D0 path take r0=archive
root, r1=script, then index the offset table and call the IWRAM fixed-cell parser whose F9 command already
carries the F9FC Hangul extension. A 12-byte push{r3}/ldr/bx stub at each 4-aligned site enters a wrapper that
uses THIS batch's descriptor table (same rule as at common4FB4C). Site 0x554DC overwrites the caller-argument
pop, so a per-batch pre-code restores r0..r2 first. The wrapper fallback reaches the previous batch's label
wrapper or a trampoline that replays the overwritten instructions and resumes the renderer.
"""
from build_visibility_poc import sha
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL
from batch_generic_v1 import Component,wrap

SITES={
 0x554A4:dict(size=12,replay='push {lr}\nlsls r1,r1,#1\nldrh r1,[r0,r1]\nadds r0,r0,r1\nmov r1,r8\npush {r1}',ret=0x080554B1,
              source_hex='00b54900415a4018414602b4',pre=None),
 0x554DC:dict(size=12,replay='lsls r1,r1,#1\nldrh r1,[r0,r1]\nadds r0,r0,r1\nmov r1,ip\npush {r1}',ret=0x080554E9,
              source_hex='07bc4900415a4018614602b4',pre='pop {r3}\npop {r0,r1,r2}\npush {r3}\nldr r3,wrapper\nbx r3'),
}
ALLOWED=set(SITES)|{INSTALL}


def previous_label(keymeta,site):
    """Latest label wrapper already installed for site (highest batch number), else None."""
    best=None
    for k,v in keymeta.items():
        if k.startswith('typed') and isinstance(v,dict) and str(site) in v.get('label_hooks',{}):
            n=int(k[5:])
            if best is None or n>best[0]:best=(n,v['label_hooks'][str(site)])
    return best[1] if best else None


class LabelComponent(Component):
    def install(self,source,appended,key_patches,keymeta,inputs,common,plugins,work):
        offsets=[p[0] for p in key_patches]
        if offsets.count(INSTALL)!=1 or set(offsets)-ALLOWED or len(set(offsets))!=len(offsets):raise ValueError(self.batch+' predecessor patch set')
        carried={p[0]:p for p in key_patches if p[0]!=INSTALL};main=[p for p in key_patches if p[0]==INSTALL]
        tail,patches,keymeta,records=super().install(source,appended,main,keymeta,inputs,common,plugins,work)
        tail=bytearray(tail);n=keymeta[self.key];hooks={}
        def place(code,literals):
            tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);blob,proof=assemble_verified(code,0x08000000+at,literals);tail.extend(blob);return at,blob,proof
        for site,spec in SITES.items():
            if source[site:site+spec['size']].hex()!=spec['source_hex']:raise ValueError(self.batch+' label site source bytes %X'%site)
            prev=previous_label(keymeta,site)
            if prev is None:
                tat,tramp,tproof=place('pop {r3}\n'+spec['replay']+'\nldr r1,ret\nbx r1',dict(ret=spec['ret']))
                previous=0x08000000+tat;preceding=source[site:site+spec['size']];trampoline=dict(offset=tat,bytes=len(tramp),sha256=sha(tramp),proof=tproof)
            else:
                previous=0x08000000+prev['code_offset'];preceding=bytes.fromhex(prev['final_stub_hex']);trampoline=None
                if carried.get(site,(None,None))[1]!=preceding:raise ValueError(self.batch+' carried label stub %X'%site)
            tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail)
            code,proof=wrap(0x08000000+at,previous,0x08000000+n['descriptor_offset'],len(n['placements']));tail.extend(code)
            entry=at;pre=None
            if spec['pre']:
                entry,pcode,pproof=place(spec['pre'],dict(wrapper=0x08000000+at+1));pre=dict(offset=entry,bytes=len(pcode),sha256=sha(pcode),proof=pproof)
            stub,sproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+site,dict(target=0x08000000+entry+1))
            if len(stub)!=spec['size']:raise ValueError(self.batch+' label stub size %X %d'%(site,len(stub)))
            hooks[str(site)]=dict(pre=pre,code_offset=at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=sproof,preceding_stub_hex=preceding.hex(),final_stub_hex=stub.hex(),trampoline=trampoline)
            patches.append((site,stub,self.batch+' label renderer root/full-bytes selector %X'%site))
        if len(source)+len(tail)>0x02000000:raise ValueError(self.batch+' extent')
        n['label_hooks']=hooks
        return bytes(tail),patches,keymeta,records

    def predecessor_view(self,source,target,keymeta):
        n=keymeta[self.key];target=bytearray(target)
        for site,h in n.get('label_hooks',{}).items():
            site=int(site);size=SITES[site]['size']
            if target[site:site+size]!=bytes.fromhex(h['final_stub_hex']):raise ValueError(self.batch+' label final stub')
            target[site:site+size]=bytes.fromhex(h['preceding_stub_hex'])
        return super().predecessor_view(source,bytes(target),keymeta)

    def verify_final(self,source,target,keymeta):
        super().verify_final(source,target,keymeta);n=keymeta[self.key]
        for site,h in n['label_hooks'].items():
            code,proof=wrap(0x08000000+h['code_offset'],h['previous_wrapper_address'],0x08000000+n['descriptor_offset'],len(n['placements']))
            if sha(code)!=h['code_sha256'] or target[h['code_offset']:h['code_offset']+len(code)]!=code:raise ValueError(self.batch+' label wrapper code')
            for part in (h.get('pre'),h.get('trampoline')):
                if part and sha(target[part['offset']:part['offset']+part['bytes']])!=part['sha256']:raise ValueError(self.batch+' label pre/trampoline')
        return True
