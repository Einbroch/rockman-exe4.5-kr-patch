"""041 immutable-source primary component: exact500 new + carry156 over53 archives.

One composed wrapper at common4FB4C (all41D84/3EFBF/47963/4B5AF/6A507/
4F773/213AB/6AB03 readers enter here with r0=root, r1=script). Each 20byte
descriptor is (root, match, match_length, script_count, clone): r0 must equal
root and the full bytes at r0 must equal the declared payload the040 product
delivers there (native LZ RAM, relocated old LZ RAM, or old/raw ROM root).
Unselected scripts are byte-identical to that payload, so the swap changes
only the500 selected scripts. Tail-calls the unchanged040 wrapper.
"""
import json,struct
from collections import defaultdict
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from verify_tpi_index import parse_tpi,lz77_decompress
from archive_scripts import verify_untouched_scripts
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL
from prepare_repartition500 import layout_records
from tpl_literals import resolve_units
from typed_rom_product040_v2 import verify_final as verify040,predecessor_view as predecessor_view040

SOURCE='analysis/pending_insertion_500_041_source_v8'
BASE='poc/output/pending500_040_v2.gba'
BASE_SHA='bf97f861fc244861d2728c67eff4adaf84e532bc321665073908b9e621add570'
RAW_ROOT_ARCHIVES=('6FE8D4','768BD0')


def ref(p):return dict(path=str(Path(p).relative_to(ROOT)),sha256=sha(Path(p).read_bytes()))


def wrap(address,previous_entry,table,count):
    if not 1<=count<=255 or any(x&3 for x in (address,table)) or not 0x08000000<=table<table+count*20<=address<0x0A000000 or not 0x08000000<=previous_entry<address:raise ValueError('041 descriptor/code placement')
    code='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
lsrs r2,r1,#8
bne fallback
ldr r3,descriptors
movs r7,#COUNT
candidate:
ldr r4,[r3]
cmp r0,r4
bne next
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
    return blob,dict(proof=proof,descriptor_fields=['root','match','match_length','script_count','clone'],descriptor_bytes=20,descriptor_slots=count,persistent_ram_bytes=0,stack_bytes=32,predecessor_contract='Original r3 on stack -> unchanged040 wrapper entry',runtime_tested=False)


def old_owner(base,old,arc):
    """The single040 consumer record that owns arc's inherited units and the bytes it delivers at r0."""
    recs=[r for r in layout_records(old) if r['archive']==arc]
    if len(recs)!=1:raise ValueError('041 carry owner not unique '+arc)
    r=recs[0];stored=base[r['rom_offset']:r['rom_offset']+r['compiled_bytes']]
    if r.get('compression'):
        payload=lz77_decompress(base,r['rom_offset'])[0]
        if sha(payload)!=r['compiled_sha256'] or r['compression']['destination']!=0x02024000:raise ValueError('041 relocated LZ carry '+arc)
        return r,payload,[(r['compression']['destination'],payload)]
    if sha(stored)!=r['compiled_sha256']:raise ValueError('041 carry ROM bytes '+arc)
    return r,stored,[(0x08000000+r['rom_offset'],None)]


def load_inputs(source):
    cfg=read('project.json');require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'))
    if sha(source)!=cfg['source_profile']['sha256'] or old['output_sha256']!=BASE_SHA:raise ValueError('041 immutable source/baseline')
    s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v3.json');cv=read(SOURCE+'/carry_verification_v2.json');rt=read(SOURCE+'/carry_roundtrip_v2.json');nc=read(SOURCE+'/native_contracts_v2.json')
    for rep in (s,v,cv,nc):
        if rep['source_sha256']!=sha(source) or rep['baseline_sha256']!=BASE_SHA:raise ValueError('041 report lineage')
    if not (v['passed'] and cv['passed'] and rt['passed'] and nc['passed']) or len(s['selected_ids'])!=500 or cv['new_units']!=500 or cv['inherited_units']!=156:raise ValueError('041 source/carry prerequisites')
    catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    roots={a['archive']:sorted({x['load_root'] for x in a['references']}) for a in nc['archives']}
    oldids={u['id'] for r in layout_records(old) for u in r['layout']};seen=set();carry=set();result=[]
    for r in cv['archives']:
        arc=r['archive'];row=catalog[arc];new=set(r['new_ids']);inh=set(r['inherited_ids'])
        for k in ('asset','target_tpl','compiled'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        payload=(ROOT/r['compiled']['path']).read_bytes();units=resolve_units(read(r['asset']['path']))
        if {u['id'] for u in units}!=new|inh or new&(seen|oldids) or not inh<=oldids or new!={i for g in groups[arc] for i in g['ids']}:raise ValueError('041 population/ownership '+arc)
        scripts=sorted({g['script'] for g in groups[arc]});count=int.from_bytes(payload[:2],'little')//2
        if row['compressed']:
            native=lz77_decompress(source,row['offset'])[0]
            if any(base[p:p+4]!=source[p:p+4] for p in row['pointers']) and not inh:raise ValueError('041 unowned archive moved '+arc)
            if base[row['offset']:row['offset']+row['size']]!=source[row['offset']:row['offset']+row['size']]:raise ValueError('041 source LZ retained '+arc)
            matches=[(root,native) for root in roots[arc]]
        else:
            native=source[row['offset']:row['offset']+row['size']]
            if arc not in RAW_ROOT_ARCHIVES:raise ValueError('041 unexpected raw archive '+arc)
            matches=[(0x08000000+row['offset'],None)]
        if int.from_bytes(native[:2],'little')!=count*2 or not matches:raise ValueError('041 native script count/root '+arc)
        prior=native;owner=None
        if inh:
            owner,prior,extra=old_owner(base,old,arc)
            if {u['id'] for u in owner['layout']}!=inh:raise ValueError('041 carry exact inherited IDs '+arc)
            matches+=extra
        kept=verify_untouched_scripts(prior,payload,count,set(scripts))
        if kept!=r['current_unselected_scripts']:raise ValueError('041 unselected current scripts '+arc)
        seen|=new;carry|=inh
        result.append((dict(archive=arc,source_row=row,new_ids=sorted(new),inherited_ids=sorted(inh),new_scripts=scripts,script_count=count,asset=r['asset'],target_tpl=r['target_tpl'],compiled=r['compiled'],native_sha256=sha(native),prior_sha256=sha(prior),old_owner=(dict(rom_offset=owner['rom_offset'],compiled_sha256=owner['compiled_sha256']) if owner else None),unselected_scripts=kept),payload,matches,native))
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(carry)!=156 or len(result)!=53:raise ValueError('041 exact500/carry156/53')
    return result


def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    base=(ROOT/BASE).read_bytes()
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or 'typed040' not in keymeta:raise ValueError('041 regenerated040 complete predecessor')
    tail=bytearray(appended);work.mkdir(parents=True,exist_ok=False);records=[];descs={};clone_at={}
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);tail.extend(data);return at
    for r,expected,matches,native in inputs:
        arc=r['archive'];f=work/arc;f.mkdir();bp=f/(arc+'.msg')
        run_textpet(common+['Read-Text-Archives',str(ROOT/r['target_tpl']['path']),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],f/'compile.log')
        if bp.read_bytes()!=expected:raise ValueError('041 primary authored recompile '+arc)
        key=sha(expected)
        if key not in clone_at:clone_at[key]=0x08000000+alloc(expected)
        cp=clone_at[key]
        for root,match in matches:
            if match is None:mp,ml=root,1
            else:mp,ml=0x08000000+alloc(match),len(match)
            k=(root,sha(match) if match is not None else 'rom')
            if k in descs:
                if descs[k]['clone']!=cp:raise ValueError('041 identical root/bytes map to different payloads '+arc)
                descs[k]['archives'].append(arc);continue
            descs[k]=dict(root=root,match=mp,match_length=ml,match_sha256=(sha(match) if match is not None else None),script_count=r['script_count'],clone=cp,archives=[arc])
        units=resolve_units(read(r['asset']['path']))
        records.append(dict(archive=arc,rom_offset=cp-0x08000000,compiled_bytes=len(expected),compiled_sha256=key,layout=[dict(id=u['id']) for u in units],translated_units=len(units),script_count=r['script_count'],native_sha256=r['native_sha256'],prior_sha256=r['prior_sha256'],cumulative041=dict(new_ids=r['new_ids'],new_scripts=r['new_scripts'],inherited_ids=r['inherited_ids'],old_owner=r['old_owner'],asset=r['asset']),unselected_script_bytes_preserved=r['unselected_scripts']))
    placements=list(descs.values())
    def body(p):
        at=p['match']-0x08000000-len(source);return bytes(tail[at:at+p['match_length']])
    byroot=defaultdict(list)
    for p in placements:byroot[p['root']].append(p)
    for root,ps in byroot.items():
        if any(p['match_sha256'] is None for p in ps) and len(ps)!=1:raise ValueError('041 ROM root shared %X'%root)
        for a in ps:
            for b in ps:
                if a is not b and a['match_length']<=b['match_length'] and body(b).startswith(body(a)):raise ValueError('041 prefix-ambiguous descriptors at root %X'%root)
    desc=alloc(b''.join(struct.pack('<5I',p['root'],p['match'],p['match_length'],p['script_count'],p['clone']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4))
    at=len(source)+len(tail);previous=0x08000000+keymeta['typed040']['code_offset'];code,proof=wrap(0x08000000+at,previous,0x08000000+desc,len(placements));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+at+1))
    if len(stub)!=12 or len(source)+len(tail)>0x02000000:raise ValueError('041 stub/extent')
    keymeta['typed041']=dict(descriptor_offset=desc,code_offset=at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'041 composed root+full-bytes selector over040; original LZ/tables retained')],keymeta,records


def predecessor_view(source,target,keymeta):
    n=keymeta['typed041'];base=(ROOT/BASE).read_bytes()
    if target[INSTALL:INSTALL+12]!=bytes.fromhex(n['final_stub_hex']):raise ValueError('041 projection final stub')
    parent=bytearray(target[:len(base)]);parent[INSTALL:INSTALL+12]=bytes.fromhex(n['preceding_stub_hex'])
    if sha(parent)!=BASE_SHA:raise ValueError('041 complete regenerated040 projection')
    return bytes(parent)


def verify_final(source,target,keymeta):
    parent=predecessor_view(source,target,keymeta);verify040(source,parent,keymeta);n=keymeta['typed041']
    code,proof=wrap(0x08000000+n['code_offset'],n['previous_wrapper_address'],0x08000000+n['descriptor_offset'],len(n['placements']))
    if json.loads(json.dumps(proof))!=json.loads(json.dumps(n['wrapper'])) or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError('041 complete code/literals')
    for i,p in enumerate(n['placements']):
        if struct.unpack_from('<5I',target,n['descriptor_offset']+20*i)!=(p['root'],p['match'],p['match_length'],p['script_count'],p['clone']):raise ValueError('041 descriptor')
        if p['match_sha256'] and sha(target[p['match']-0x08000000:p['match']-0x08000000+p['match_length']])!=p['match_sha256']:raise ValueError('041 match copy')
    return True


def finalize(source,target,result,inputs,records):
    verify_final(source,target,result['keyitem_rom']);old=read(BASE.replace('.gba','.json'))
    oldids={u['id'] for r in layout_records(old) for u in r['layout']}
    for rec in records:
        if sha(target[rec['rom_offset']:rec['rom_offset']+rec['compiled_bytes']])!=rec['compiled_sha256']:raise ValueError('041 final clone bytes')
    result['keyitem_rom']['typed041']['archives']=records
    allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for r,*_ in inputs for k in r['new_ids']}
    if oldids-allids or allids-oldids!=new or len(new)!=500:raise ValueError('041 exact cumulative500')
    result['translated_units']+=500
    for r,*_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='041 active authored owner (new+carry)'))
    result['active_typed_owners041']={r['archive']:r['asset'] for r,*_ in inputs}
    result['pending_batch500_041']=dict(new_units=500,inherited_units_reauthored=156,archives=53,source=SOURCE,rom_integrated=True,runtime='pending',release_eligible=False)
    result['primary_entry']='tools/build_development_patch_041_v1.py';result['limits'].append('041 exact500+carry156 composed root/full-bytes selector: Korean runtime of equipment warnings, mail alerts, tournament, subchip, BBS, B2, trader/tutorial pending; NON-DISTRIBUTION')
