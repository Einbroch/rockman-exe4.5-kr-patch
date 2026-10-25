"""Generic500 batch pipeline (042+): source preparation and an immutable-source ROM component.

prepare(): pick exactly500 pending canonical IDs (whole scripts) from mmbn45 dialogue scripts that
pass generic_page_gate042_v1, merge the current authored carry for each archive (recompiled carry
must equal the bytes the current product delivers), compile with TextPet, and write a manifest.

Component: one wrapper at common4FB4C over the previous batch wrapper. Descriptor
(root, match, match_length, script_count, clone); root==0 means any EWRAM r0 (0x02000000..0x0203FFFF).
Matches are every payload the predecessor product delivers at r0 for the archive: the original/relocated
LZ RAM payloads and original/relocated/owner raw ROM roots. Full bytes must match; unselected scripts are
byte-identical to the predecessor's displayed payload, so only selected scripts change on screen.
"""
import json,re,struct,importlib
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import parse_tpi,lz77_decompress
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL
from prepare_repartition500 import layout_records
from tpl_literals import resolve_units,literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from canonical_literals_031 import canonical_literals
from textpet_korean import command
from generic_page_gate042_v1 import script_text

CENSUS='analysis/pending_insertion_500_041_inventory_v1/census.json'
OWNERS040='analysis/pending_insertion_500_041_inventory_v1/authored_owners.json'
EWRAM=0x02000000


def u32(b,at):return int.from_bytes(b[at:at+4],'little')


_OWNERS={}
def owner_records(meta,arc):
    if id(meta) not in _OWNERS:
        d=defaultdict(list)
        for r in layout_records(meta):
            if 'rom_offset' in r and 'compiled_sha256' in r:d[r['archive']].append(r)
        _OWNERS.clear();_OWNERS[id(meta)]=d
    return _OWNERS[id(meta)].get(arc,[])


def owner_payload(rom,r):
    if r.get('compression'):return lz77_decompress(rom,r['rom_offset'])[0]
    return rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']]


def owner_asset(r,owners040):
    for k in ('cumulative_generic','cumulative041'):
        if k in r:return r[k]['asset']
    m=owners040.get((r['archive'],r['rom_offset']))
    return m[0] if m else None


def deliveries(source,rom,meta,row,arc):
    """(root,bytes|None) pairs the predecessor product delivers at common4FB4C for this archive."""
    out=[];native=payload_of(source,row)
    if row['compressed']:
        out.append((0,native))
        for p in row['pointers']:
            v=u32(rom,p)
            if v!=0x08000000+row['offset']:
                if not 0x08000000<=v<0x08000000+len(rom):raise ValueError('moved pointer range '+arc)
                out.append((0,lz77_decompress(rom,v-0x08000000)[0]))
    else:
        out.append((0x08000000+row['offset'],None))
        for p in row['pointers']:
            v=u32(rom,p)
            if v!=0x08000000+row['offset']:
                if not 0x08000000<=v<0x08000000+len(rom):raise ValueError('moved pointer range '+arc)
                out.append((v,None))
    for r in owner_records(meta,arc):
        out.append((0,owner_payload(rom,r)) if r.get('compression') else (0x08000000+r['rom_offset'],None))
    seen=set();res=[]
    for root,b in out:
        k=(root,sha(b) if b is not None else None)
        if k not in seen:seen.add(k);res.append((root,b))
    return res


def current_carry(source,rom,meta,arc,original,owners040):
    """Authored units the predecessor displays for arc and that payload; None if not reconstructible."""
    recs=owner_records(meta,arc)
    if not recs:return [],payload_of(source,meta['_catalog'][arc]),None
    sets=[]
    for r in recs:
        a=owner_asset(r,owners040)
        if a is None:return None
        require_hash(ROOT/a['path'],a['sha256']);units={u['id']:u for u in resolve_units(read(a['path'])) if u['id'].split(':')[0]==arc}
        if set(units)!={u['id'] for u in r['layout']}:return None
        sets.append((r,units))
    top=max(sets,key=lambda x:len(x[1]))
    for r,units in sets:
        if any(k not in top[1] or top[1][k]['translation']!=v['translation'] for k,v in units.items()):return None
    raw={u.key:u.text for u in literals(original)}
    if any(raw.get(k)!=u['source'] for k,u in top[1].items()):return None
    ordered=[top[1][u.key] for u in literals(original) if u.key in top[1]]
    return ordered,owner_payload(rom,top[0]),top[0]


def compile_tpl(common,text,folder,name):
    folder.mkdir(parents=True,exist_ok=True);tp=folder/(name+'.tpl');bp=folder/(name+'.msg')
    tp.write_text(canonical_literals(text),encoding='utf8',newline='\n')
    run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],folder/(name+'.log'))
    return tp,bp.read_bytes()


def charset_ok(text,codes,extras):
    from build_development_patch import encode_character,EXTRA_CHARACTER_INDICES
    for ch in text:
        if ch=='\n':continue
        if 0xAC00<=ord(ch)<=0xD7A3:
            if codes.get(ch)!=encode_character(ch):return False
        elif ch in EXTRA_CHARACTER_INDICES:
            if ch not in extras:return False
        elif ch not in codes:return False
    return True


def prepare(batch,base,plugins,limit=500,gate='generic_page_gate042_v1',kind='dialogue',redirect_ok=(),fits=None):
    fitmap={f['id']:f for f in read(fits)['fixes']} if fits else {}
    G=importlib.import_module(gate);check,reflow,fit,simulate,CAPS=G.check,G.reflow,G.fit,G.simulate,G.CAPS
    def full(original,units):
        vals={u['id']:u['translation'] for u in units};pages={u['id']:u['pages'] for u in units if u.get('pages')}
        if pages and not hasattr(G,'render'):raise ValueError('page split needs gate render')
        return G.render(original,vals,pages) if pages else replace_exact(original,vals)
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();meta=read(base.replace('.gba','.json'));require_hash(ROOT/base,meta['output_sha256']);rom=(ROOT/base).read_bytes()
    out=ROOT/f'analysis/pending_insertion_500_{batch}_v1'
    if out.exists():raise ValueError('Preserve existing batch '+batch)
    catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};meta['_catalog']=catalog
    census=read(CENSUS);owners040=defaultdict(list)
    for r in read(OWNERS040)['records']:
        if r['authored_set_matches']:owners040[(r['archive'],r['rom_offset'])]=r['authored_set_matches']
    applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    codes={}
    for line in (ROOT/plugins/'exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            k,v=line.split('=',1)
            if len(v)==1:codes[v]=bytes.fromhex(k)
    extras=set(meta.get('extra_glyph_metrics',{}))
    # global uniqueness pool of RAM payloads (catalog natives) for twin/prefix rejection
    natives={arc:payload_of(source,r) for arc,r in catalog.items() if r['compressed']}
    by_hash=defaultdict(set)
    for arc,b in natives.items():by_hash[sha(b)].add(arc)
    templates={};drafts={};cands=[];rejected=defaultdict(int);carry_cache={};common=command(ROOT/plugins)
    cells_by_root=None
    def label_budget(arc,script):
        """Cells per row the renderer callers give this archive: per-script immediate r1 if any, else the
        narrowest caller for the root. Raw archives use their ROM root; LZ archives only when their native
        load root is known from the 041 contracts (subchip 02026C00 family). None when unknown."""
        nonlocal cells_by_root
        if cells_by_root is None:
            from label_cells_v1 import scan
            cells_by_root=scan(source)[0]
        row=catalog[arc];roots=[]
        if not row['compressed']:roots=[0x08000000+row['offset']]
        else:
            nc=read('analysis/pending_insertion_500_041_source_v8/native_contracts_v2.json')
            roots=sorted({x['load_root'] for a in nc['archives'] if a['archive']==arc for x in a['references']})
        calls=[c for r in roots for c in cells_by_root.get(r,[])]
        if not calls:return None
        exact=[c[1] for c in calls if c[3]==script]
        return min(exact) if exact else min(c[1] for c in calls)
    def label_renderer(row):
        import capstone
        md=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB)
        for p in row['pointers']:
            for a in range(max(0,p-1024),p,2):
                ins=source[a:a+2]
                if (ins[1]&0xF8)==0x48 and ((a+4)&~3)+ins[0]*4==p:
                    bl=[i.op_str for i in md.disasm(source[a:a+48],0x08000000+a) if i.mnemonic=='bl'][:1]
                    if bl and bl[0] in ('#0x80554a4','#0x80554c8','#0x80554d0'):return True
                    break
        return False
    def archive_ok(arc):
        c=current_carry(source,rom,meta,arc,templates[arc],owners040)
        if c is None:return 'carry owner not reconstructible'
        old,prior,top=c
        if old:
            _,before=compile_tpl(common,full(templates[arc],old),out/'_carry_check'/arc,'prior')
            if before!=prior:return 'carry recompile differs'
        dl=deliveries(source,rom,meta,catalog[arc],arc)
        for root,bts in dl:
            if bts is None:continue
            for other,ob in natives.items():
                if other!=arc and (ob.startswith(bts) or bts.startswith(ob)):return 'prefix-ambiguous RAM payload'
        return (old,prior,top,dl)
    for g in census['groups']:
        arc=g['archive'];ids=set(g['ids'])
        if ids&applied:continue
        why=None
        if kind=='dialogue' and g['literal_language']!='mmbn45':why='label dialect mmbn45s (renderer not admitted)'
        elif kind=='label' and g['literal_language']!='mmbn45s':why='dialogue (not a label batch)'
        elif kind=='label' and not catalog[arc]['compressed'] and not label_renderer(catalog[arc]) and arc not in redirect_ok:why='raw label read only by non-0x080554A4 renderers'
        elif g['storage'] not in ('raw-existing','compressed','raw-new'):why='storage '+g['storage']
        elif not g['all_japanese_literals_unapplied']:why='partially applied script'
        elif arc in natives and len(by_hash[sha(natives[arc])])>1:why='twin native archive'
        if why:rejected[why]+=g['units'];continue
        if arc not in templates:require_hash(ROOT/g['source_tpl']['path'],g['source_tpl']['sha256']);templates[arc]=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        if arc not in carry_cache:carry_cache[arc]=archive_ok(arc)
        if isinstance(carry_cache[arc],str):rejected[carry_cache[arc]]+=g['units'];continue
        one,_=script_text(templates[arc],g['script']);raw={u.key:u.text for u in literals(one)};values={};units=[]
        for d in g['drafts']:
            if d['path'] not in drafts:require_hash(ROOT/d['path'],d['sha256']);drafts[d['path']]=read(d['path'])
            a=drafts[d['path']];u=deepcopy(next(x for x in a['units'] if x['id']==d['id']))
            if a['source_sha256']!=sha(source) or u['source']!=raw.get(u['id']):why='draft provenance';break
            f=fitmap.get(u['id'])
            if f and f['before']==u['translation'] and f['source']==u['source']:
                u['canonical_wording']=u['translation'];u['translation']=f['after'];u['wording_fit']=dict(file=fits,reason=f['reason'])
            values[u['id']]=u['translation'];units.append(u)
        if why:rejected[why]+=g['units'];continue
        if kind=='label':
            # Fixed-cell fonts have the native middle dot U+30FB but not the VWF extra U+00B7: same glyph role,
            # no wording change. Bracket tokens are allowed only when the same token is in the source literal.
            for k in list(values):
                if '·' in values[k]:values[k]=values[k].replace('·','・')
                for u in units:
                    if u['id']==k:u.setdefault('canonical_wording',u['translation']);u['translation']=values[k];u['label_glyph_normalized']=(u['canonical_wording']!=values[k])
            plain={k:re.sub(r'\[[^\]]+\]',lambda m:'' if m.group(0) in raw[k] else m.group(0),v) for k,v in values.items()}
        else:plain=values
        if not all(charset_ok(v,codes,extras if kind=='dialogue' else set()) for v in plain.values()):rejected['glyph not in current font']+=g['units'];continue
        if kind=='label':
            budget=label_budget(arc,g['script'])
            bad=[k for k,v in values.items() if len(v.split('\n'))!=len(raw[k].split('\n')) or any(len(a)>max(len(b),budget or 0) for a,b in zip(v.split('\n'),raw[k].split('\n')))]
            if bad:rejected['label wider than source cells']+=g['units'];continue
            for u in units:u.setdefault('canonical_wording',u['translation'])
            cands.append(dict(archive=arc,script=g['script'],ids=sorted(ids),units=units,geometry=dict(label_cells='<= source per line'),storage=g['storage'],source_tpl=g['source_tpl'],source_row=g['source_row']));continue
        geo=None;split={}
        try:geo=check(one,replace_exact(one,values))
        except ValueError:
            values=fit(one,values)
            try:geo=check(one,replace_exact(one,values))
            except ValueError:
                r=G.split_fit(one,values) if hasattr(G,'split_fit') else None
                if r is not None:
                    try:geo=G.check_split(one,*r);values,split=r
                    except ValueError:geo=None
        if geo is None:rejected['page extent exceeds window']+=g['units'];continue
        for u in units:
            u.setdefault('canonical_wording',u['translation']);u['translation']=values[u['id']]
            if u['id'] in split:u['pages']=split[u['id']]
        cands.append(dict(archive=arc,script=g['script'],ids=sorted(ids),units=units,geometry=geo,storage=g['storage'],source_tpl=g['source_tpl'],source_row=g['source_row']))
    order={'raw-existing':0,'compressed':1,'raw-new':2}
    cands.sort(key=lambda c:(order[c['storage']],c['archive'],c['script']))
    chosen=[];total=0
    for c in cands:
        n=len(c['ids'])
        if total+n<=limit:chosen.append(c);total+=n
        if total==limit:break
    if total!=limit and len(chosen)<len(cands):raise ValueError(f'could not fill exact batch: {total}')
    if not chosen:raise ValueError('no remaining gate candidates')
    # compile per archive
    gs=defaultdict(list)
    for c in chosen:gs[c['archive']].append(c)
    archives=[]
    for arc,cs in sorted(gs.items()):
        original=templates[arc];old,prior,top,dl=carry_cache[arc];new=[u for c in cs for u in c['units']];newids={u['id'] for u in new}
        units=list(old)+new;ordered=[next(u for u in units if u['id']==l.key) for l in literals(original) if l.key in {u['id'] for u in units}]
        f=out/arc
        if skeleton(replace_exact(original,{u['id']:u['translation'] for u in ordered}))!=skeleton(original):raise ValueError('controls '+arc)
        target=full(original,ordered)
        tp,payload=compile_tpl(common,target,f,'target')
        count=int.from_bytes(payload[:2],'little')//2;scripts=sorted({c['script'] for c in cs})
        if len(payload)>65535:raise ValueError('u16 archive size '+arc)
        kept=verify_untouched_scripts(prior,payload,count,set(scripts))
        asset=dict(schema=1,archive=arc,policy='development-draft; NON-DISTRIBUTION',source_sha256=sha(source),source_tpl=cs[0]['source_tpl'],units=ordered,new_ids=sorted(newids),inherited_ids=[u['id'] for u in old],carry_owner=(dict(rom_offset=top['rom_offset'],compiled_sha256=top['compiled_sha256']) if top else None),insertion_ready=False,review=dict(wording='needs_review',layout='generic-page-gate',release_eligible=False))
        ap=f/'authored_combined_asset.json';frozen_write(ap,asset);(f/(arc+'.msg')).write_bytes(payload)
        archives.append(dict(archive=arc,asset=dict(path=str(ap.relative_to(ROOT)),sha256=sha(ap.read_bytes())),target_tpl=dict(path=str(tp.relative_to(ROOT)),sha256=sha(tp.read_bytes())),compiled=dict(path=str((f/(arc+'.msg')).relative_to(ROOT)),sha256=sha(payload)),new_ids=sorted(newids),inherited_ids=[u['id'] for u in old],new_scripts=scripts,script_count=count,prior_sha256=sha(prior),deliveries=[dict(root=r,match_sha256=(sha(b) if b is not None else None),match_bytes=(len(b) if b is not None else None)) for r,b in dl],unselected_scripts=kept,geometry={c['script']:c['geometry'] for c in cs}))
        print('PASS',batch,arc,'new',len(newids),'carry',len(old),flush=True)
    newall=sorted(k for a in archives for k in a['new_ids'])
    manifest=dict(schema=1,batch=batch,kind=kind,status=f'{batch}_SOURCE_PREPARED',baseline_rom=base,baseline_sha256=meta['output_sha256'],source_sha256=sha(source),plugins=plugins,new_units=len(newall),selected_ids=newall,archives=archives,rejected_pool_units=dict(rejected),remaining_gate_candidates=sum(len(c['ids']) for c in cands)-len(newall),tool='tools/batch_generic_v1.py',tool_sha256=sha((ROOT/'tools/batch_generic_v1.py').read_bytes()),gate=f'tools/{gate}.py',gate_sha256=sha((ROOT/f'tools/{gate}.py').read_bytes()),rom_written=False,release_eligible=False)
    frozen_write(out/'manifest.json',manifest)
    print('PREPARED',batch,'units',len(newall),'archives',len(archives),'remaining gate candidates',manifest['remaining_gate_candidates'],'rejected',dict(rejected))
    return manifest


def wrap(address,previous_entry,table,count):
    if not 1<=count<=255 or any(x&3 for x in (address,table)) or not 0x08000000<=table<table+count*20<=address<0x0A000000 or not 0x08000000<=previous_entry<address:raise ValueError('generic descriptor/code placement')
    code='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
lsrs r2,r1,#8
bne fallback
ldr r3,descriptors
movs r7,#COUNT
candidate:
ldr r4,[r3]
cmp r4,#0
bne exact
lsrs r4,r0,#18
cmp r4,#0x80
bne next
b rooted
exact:
cmp r0,r4
bne next
rooted:
ldr r1,[sp,#4]
ldr r4,[r3,#12]
cmp r1,r4
bhs next
movs r1,r0
ldr r5,[r3,#4]
ldr r6,[r3,#8]
compare:
ldrb r2,[r1]
ldrb r4,[r5]
cmp r2,r4
bne next
adds r1,#1
adds r5,#1
subs r6,#1
bne compare
ldr r4,[r3,#16]
str r4,[sp]
b fallback
next:
adds r3,#20
subs r7,#1
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''.replace('COUNT',str(count))
    blob,proof=assemble_verified(code,address,dict(descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,descriptor_fields=['root(0=any EWRAM)','match','match_length','script_count','clone'],descriptor_bytes=20,descriptor_slots=count,persistent_ram_bytes=0,stack_bytes=32,runtime_tested=False)


class Component:
    def __init__(self,batch,base,base_sha,manifest,prev_module,prev_key):
        self.batch=batch;self.key='typed'+batch;self.base=base;self.base_sha=base_sha;self.manifest=manifest;self.prev=importlib.import_module(prev_module);self.prev_key=prev_key

    def load_inputs(self,source):
        cfg=read('project.json');require_hash(ROOT/self.base,self.base_sha);rom=(ROOT/self.base).read_bytes();meta=read(self.base.replace('.gba','.json'));m=read(self.manifest)
        if sha(source)!=cfg['source_profile']['sha256'] or m['baseline_sha256']!=self.base_sha or m['source_sha256']!=sha(source) or not 0<m['new_units']<=500:raise ValueError(self.batch+' manifest lineage')
        catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};applied={u['id'] for r in layout_records(meta) for u in r['layout']};res=[];seen=set()
        for a in m['archives']:
            arc=a['archive'];row=catalog[arc]
            for k in ('asset','target_tpl','compiled'):require_hash(ROOT/a[k]['path'],a[k]['sha256'])
            payload=(ROOT/a['compiled']['path']).read_bytes();units=resolve_units(read(a['asset']['path']))
            new=set(a['new_ids']);inh=set(a['inherited_ids'])
            if {u['id'] for u in units}!=new|inh or new&(applied|seen) or not inh<=applied:raise ValueError(self.batch+' population '+arc)
            dl=deliveries(source,rom,meta,row,arc)
            if [dict(root=r,match_sha256=(sha(b) if b is not None else None),match_bytes=(len(b) if b is not None else None)) for r,b in dl]!=a['deliveries']:raise ValueError(self.batch+' predecessor deliveries changed '+arc)
            seen|=new;res.append((a,payload,dl))
        if seen!=set(m['selected_ids']) or len(seen)!=m['new_units']:raise ValueError(self.batch+' exact batch population')
        return res

    def install(self,source,appended,key_patches,keymeta,inputs,common,plugins,work):
        base=(ROOT/self.base).read_bytes()
        if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or self.prev_key not in keymeta:raise ValueError(self.batch+' regenerated predecessor')
        tail=bytearray(appended);work.mkdir(parents=True,exist_ok=False);records=[];descs={};clone_at={}
        def alloc(data):
            tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);tail.extend(data);return at
        for a,expected,dl in inputs:
            arc=a['archive'];f=work/arc;f.mkdir();bp=f/(arc+'.msg')
            run_textpet(common+['Read-Text-Archives',str(ROOT/a['target_tpl']['path']),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],f/'compile.log')
            if bp.read_bytes()!=expected:raise ValueError(self.batch+' primary authored recompile '+arc)
            key=sha(expected)
            if key not in clone_at:clone_at[key]=0x08000000+alloc(expected)
            cp=clone_at[key]
            for root,match in dl:
                mp,ml=(root,1) if match is None else (0x08000000+alloc(match),len(match))
                k=(root,sha(match) if match is not None else 'rom')
                if k in descs:
                    if descs[k]['clone']!=cp:raise ValueError(self.batch+' identical delivery maps to two payloads '+arc)
                    descs[k]['archives'].append(arc);continue
                descs[k]=dict(root=root,match=mp,match_length=ml,match_sha256=(sha(match) if match is not None else None),script_count=a['script_count'],clone=cp,archives=[arc])
            units=resolve_units(read(a['asset']['path']))
            records.append(dict(archive=arc,rom_offset=cp-0x08000000,compiled_bytes=len(expected),compiled_sha256=key,layout=[dict(id=u['id']) for u in units],translated_units=len(units),script_count=a['script_count'],prior_sha256=a['prior_sha256'],cumulative_generic=dict(batch=self.batch,new_ids=a['new_ids'],new_scripts=a['new_scripts'],inherited_ids=a['inherited_ids'],asset=a['asset']),unselected_script_bytes_preserved=a['unselected_scripts']))
        placements=list(descs.values())
        def body(p):
            at=p['match']-0x08000000-len(source);return bytes(tail[at:at+p['match_length']])
        groups=defaultdict(list)
        for p in placements:groups[p['root']].append(p)
        for root,ps in groups.items():
            if root and len(ps)!=1:raise ValueError(self.batch+' ROM root shared %X'%root)
            for x in ps:
                for y in ps:
                    if x is not y and x['match_sha256'] and y['match_sha256'] and body(y).startswith(body(x)):raise ValueError(self.batch+' prefix-ambiguous descriptors')
        if len(placements)>255:raise ValueError(self.batch+' descriptor count')
        desc=alloc(b''.join(struct.pack('<5I',p['root'],p['match'],p['match_length'],p['script_count'],p['clone']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4))
        at=len(source)+len(tail);previous=0x08000000+keymeta[self.prev_key]['code_offset'];code,proof=wrap(0x08000000+at,previous,0x08000000+desc,len(placements));tail.extend(code)
        stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+at+1))
        if len(stub)!=12 or len(source)+len(tail)>0x02000000:raise ValueError(self.batch+' stub/extent')
        keymeta[self.key]=dict(descriptor_offset=desc,code_offset=at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,persistent_ram_bytes=0,runtime='pending')
        return bytes(tail),[(INSTALL,stub,self.batch+' generic root/full-bytes selector over predecessor')],keymeta,records

    def predecessor_view(self,source,target,keymeta):
        n=keymeta[self.key];base=(ROOT/self.base).read_bytes()
        if target[INSTALL:INSTALL+12]!=bytes.fromhex(n['final_stub_hex']):raise ValueError(self.batch+' projection final stub')
        parent=bytearray(target[:len(base)]);parent[INSTALL:INSTALL+12]=bytes.fromhex(n['preceding_stub_hex'])
        if sha(parent)!=self.base_sha:raise ValueError(self.batch+' complete predecessor projection')
        return bytes(parent)

    def verify_final(self,source,target,keymeta):
        parent=self.predecessor_view(source,target,keymeta);self.prev.verify_final(source,parent,keymeta);n=keymeta[self.key]
        code,proof=wrap(0x08000000+n['code_offset'],n['previous_wrapper_address'],0x08000000+n['descriptor_offset'],len(n['placements']))
        if json.loads(json.dumps(proof))!=json.loads(json.dumps(n['wrapper'])) or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError(self.batch+' code/literals')
        for i,p in enumerate(n['placements']):
            if struct.unpack_from('<5I',target,n['descriptor_offset']+20*i)!=(p['root'],p['match'],p['match_length'],p['script_count'],p['clone']):raise ValueError(self.batch+' descriptor')
            if p['match_sha256'] and sha(target[p['match']-0x08000000:p['match']-0x08000000+p['match_length']])!=p['match_sha256']:raise ValueError(self.batch+' match copy')
        return True

    def finalize(self,source,target,result,inputs,records):
        self.verify_final(source,target,result['keyitem_rom']);old=read(self.base.replace('.gba','.json'))
        oldids={u['id'] for r in layout_records(old) for u in r['layout']}
        for rec in records:
            if sha(target[rec['rom_offset']:rec['rom_offset']+rec['compiled_bytes']])!=rec['compiled_sha256']:raise ValueError(self.batch+' final clone bytes')
        result['keyitem_rom'][self.key]['archives']=records
        allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for a,*_ in inputs for k in a['new_ids']}
        n=read(self.manifest)['new_units']
        if oldids-allids or allids-oldids!=new or len(new)!=n:raise ValueError(self.batch+' exact cumulative batch')
        result['translated_units']+=n
        for a,*_ in inputs:result['translation_assets'].append(dict(a['asset'],archive=a['archive'],scope=self.batch+' active authored owner (new+carry)'))
        result['pending_batch500_'+self.batch]=dict(new_units=n,archives=len(inputs),manifest=self.manifest,rom_integrated=True,runtime='pending',release_eligible=False)
        result['primary_entry']=f'tools/build_development_patch_{self.batch}_v1.py';result['limits'].append(self.batch+' generic500 batch (generic page gate): Korean runtime per scene pending; NON-DISTRIBUTION')
