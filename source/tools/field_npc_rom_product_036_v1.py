"""036 single-writer installation component;035 natural-route gate stays shut.

No command here builds a ROM. --preflight checks500 inputs and confirms that
the unresolved035 admission condition refuses installation before any writes.
"""
import struct,sys
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from prepare_npc_inputs_036_v1 import OUT as INPUT_DIR
from prepare_source500_036_v1 import OUT as SOURCE,BASE,BASE_SHA,ref
from prepare_repartition500 import layout_records
from field_npc_rom_selector_036_v1 import source_population,wrap
from field_npc_rom_product_035_v2 import verify_final as verify035
from survey_new_storage_035 import VALIDATORS
from survey_aggregate_pet_033 import replace_exact
from tpl_literals import literals,skeleton
from canonical_literals_031 import canonical_literals
from archive_scripts import verify_untouched_scripts
from build_development_patch import validate_characters,validate_literal_numerals
from verify_tpi_index import lz77_decompress,parse_tpi
from keyitem_rom_selector import INSTALL
from extended_dialogue import assemble_verified

MANIFEST=INPUT_DIR+'/manifest.json'


def require_admission():
    status=read('analysis/pending500_035_v2/batch_status.json')
    if status['rom_sha256']!=BASE_SHA or not status.get('natural_cached_NPC_selection_verified'):
        raise ValueError('035 natural cached NPC selection/display remains pending;036 ROM installation refused before writes')
    proof=status.get('reports',{}).get('natural_cached_display')
    if not proof:raise ValueError('035 natural runtime evidence missing')
    require_hash(ROOT/proof['path'],proof['sha256']);r=read(proof['path'])
    if not r.get('passed') or r.get('rom_sha256')!=BASE_SHA or r.get('natural_actor_selection_verified') is not True or r.get('release_eligible') is True:
        raise ValueError('035 development natural runtime evidence contract')
    return proof


def load_inputs(source,preflight_only=False):
    if not preflight_only:require_admission()
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    if sha(source)!=cfg['source_profile']['sha256']:raise ValueError('036 immutable source identity')
    manifest=read(MANIFEST)
    for p,h in manifest['dependencies'].items():require_hash(ROOT/p,h)
    if not manifest['passed'] or manifest['new_units']!=500 or manifest['source_sha256']!=sha(source) or manifest['baseline_rom']!=BASE or manifest['baseline_sha256']!=BASE_SHA or manifest['rom_written']:raise ValueError('036 registered input contract')
    require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'));verify035(source,base,old['keyitem_rom'])
    oldids={u['id'] for r in layout_records(old) for u in r['layout']};owned={r['archive'] for r in layout_records(old)}
    s=read(SOURCE+'/selection.json');groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    selected={r['archive']:r['scene'] for r in manifest['archives']};pool=source_population(source,selected);validators=dict(VALIDATORS);seen=set();result=[]
    for r in manifest['archives']:
        arc=r['archive'];row=r['source_row']
        if arc in owned or row!=catalog[arc] or not row['compressed'] or row['size_header']:raise ValueError('036 new archive storage/ownership')
        for key in ['asset','compiled','source_tpl','target_tpl']:require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        asset=read(r['asset']['path']);units=asset['units'];ids={u['id'] for u in units};payload=(ROOT/r['compiled']['path']).read_bytes();native,used=lz77_decompress(source,row['offset'])
        if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False or asset['archive']!=arc or asset['source_sha256']!=sha(source) or asset['source_archive_sha256']!=sha(native):raise ValueError('036 development asset identity')
        if ids!=set(r['new_ids']) or len(ids)!=len(units) or ids&(seen|oldids) or r['translated_units']!=len(ids):raise ValueError('036 exact disjoint IDs')
        field=next(x for x in pool if x['archive']==arc)
        if field['scene']!=r['scene'] or row['pointers']!=[field['pointer']] or r['native_sha256']!=sha(native) or r['native_bytes']!=len(native):raise ValueError('036 scene/source lookup')
        if base[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used] or any(base[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('036 native source/references altered')
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig');raw={u.key:u.text for u in literals(original)}
        if any(u['state']!='needs_review' or u['source']!=raw[u['id']] for u in units) or skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals(replace_exact(original,{u['id']:u['translation'] for u in units}))]:raise ValueError('036 protected source/target/state')
        scope=r['scope']
        if scope['consumer']!='normal-dialogue' or scope['literal_language']!='mmbn45' or set(scope['literal_ids'])!=ids or scope['storage']!='scene-native-identity-ROM-clone' or scope['scene']!=field['scene'] or scope['guarded_reader_return_lr']!=0x0804F773 or scope['native_root']!=0x02039800:raise ValueError('036 explicit runtime scope')
        for g in groups[arc]:
            if validators[g['profile']](original,target,[g['script']],set(g['geometry_ids']),99)!=g['geometry']:raise ValueError('036 geometry/protected consumer')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        if sha(payload)!=r['compiled_sha256'] or len(payload)!=r['compiled_bytes'] or len(payload)>65535 or verify_untouched_scripts(native,payload,255,set(r['new_scripts']))!=r['unselected_scripts']:raise ValueError('036 payload/unselected script proof')
        result.append((r,payload));seen|=ids
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(result)!=20:raise ValueError('036 complete500/20')
    return result


def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    admission=require_admission() # BEFORE creating work files or changing bytes
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or len(key_patches[0][1])!=12 or 'npc035' not in keymeta:raise ValueError('036 one preceding composed reader')
    require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes()
    if source+bytes(appended)==base or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or key_patches[0][1]!=base[INSTALL:INSTALL+12]:raise ValueError('036 source-generated035 append/stub differs')
    tail=bytearray(appended);placements=[];records=[];work.mkdir(parents=True,exist_ok=False)
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));off=len(source)+len(tail);tail.extend(data);return off
    for r,precompiled in inputs:
        arc=r['archive'];asset=read(r['asset']['path']);original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=replace_exact(original,{u['id']:u['translation'] for u in asset['units']})
        f=work/arc;f.mkdir();tp=f/'target.tpl';bp=f/(arc+'.msg');tp.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],f/'compile.log');payload=bp.read_bytes()
        if payload!=precompiled:raise ValueError('036 immutable-source primary recompile')
        layout=validate_characters(target,plugins/'exe45-utf8.tbl',r['scope'],set(r['new_ids']))
        if layout!=r['layout']:raise ValueError('036 primary metrics')
        native=lz77_decompress(source,r['source_row']['offset'])[0];np=alloc(native);cp=alloc(payload)
        placements.append(dict(source_archive=arc,scene=r['scene'],native_copy_offset=np,native_copy_bytes=len(native),native_copy_sha256=sha(native),rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),source_row=r['source_row']))
        records.append(dict(archive=arc,rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),layout=layout,translated_units=len(asset['units']),script_count=255,source_sha256=sha(native),source_bytes=len(native),native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,protected_controls_unchanged=True,native_ram_archive_retained=True,cumulative036=dict(scope=r['scope'],new_ids=r['new_ids'],new_scripts=r['new_scripts'],manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes())),unselected_script_bytes_preserved=r['unselected_scripts']))
    desc=alloc(b''.join(struct.pack('<4I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['scene']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4));code_at=len(source)+len(tail)
    previous=0x08000000+keymeta['npc035']['code_offset'];code,proof=wrap(source,0x08000000+code_at,previous,0x08000000+desc,len(placements));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+code_at+1))
    if len(stub)!=12:raise ValueError('036 composed reader stub size')
    keymeta['npc036']=dict(descriptor_offset=desc,code_offset=code_at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,admission=admission,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'036 scene/native NPC reader composed over035 and all prior consumers')],keymeta,records


def verify_final(source,target,keymeta):
    n=keymeta['npc036'];stub=bytes.fromhex(n['final_stub_hex']);oldstub=bytes.fromhex(n['preceding_stub_hex'])
    if target[INSTALL:INSTALL+12]!=stub:raise ValueError('036 installed composed reader')
    previous=bytearray(target);previous[INSTALL:INSTALL+12]=oldstub;verify035(source,previous,keymeta)
    code,proof=wrap(source,0x08000000+n['code_offset'],0x08000000+keymeta['npc035']['code_offset'],0x08000000+n['descriptor_offset'],len(n['placements']))
    if proof!=n['wrapper'] or len(code)!=n['code_bytes'] or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError('036 final code/literals')
    selected={p['source_archive']:p['scene'] for p in n['placements']};source_population(source,selected)
    if len(selected)!=20:raise ValueError('036 final descriptor population')
    for i,p in enumerate(n['placements']):
        a=p['rom_offset'];b=p['native_copy_offset'];native,used=lz77_decompress(source,p['source_row']['offset']);off=p['source_row']['offset']
        if target[b:b+len(native)]!=native or sha(target[a:a+p['compiled_bytes']])!=p['compiled_sha256'] or struct.unpack_from('<4I',target,n['descriptor_offset']+i*16)!=(0x08000000+a,0x08000000+b,len(native),p['scene']):raise ValueError('036 native/clone/scene descriptor bytes')
        if target[off:off+used]!=source[off:off+used] or any(target[x:x+4]!=source[x:x+4] for x in p['source_row']['pointers']):raise ValueError('036 original loader assets changed')
    return True


def finalize(source,target,result,inputs,records):
    require_admission();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'))
    if len(target)<=len(base) or target[:INSTALL]!=base[:INSTALL] or target[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('036 preceding035 bytes changed')
    before=list(layout_records(old));prior=list(layout_records(result))
    if [(r['archive'],r['compiled_sha256'],r['layout']) for r in before]!=[(r['archive'],r['compiled_sha256'],r['layout']) for r in prior]:raise ValueError('036 old record/owner/metrics changed')
    result['keyitem_rom']['npc036']['archives']=records;oldids={u['id'] for r in before for u in r['layout']};allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for r,_ in inputs for k in r['new_ids']}
    if len(new)!=500 or oldids-allids or allids-oldids!=new or result['translated_units']!=old['translated_units']:raise ValueError('036 actual cumulative500 delta')
    result['translated_units']+=500
    for r,_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='036 scene/native NPC clone translation owner'))
    result['pending_batch500_036']=dict(new_units=500,archives=20,manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes()),rom_integrated=True,runtime='pending',release_eligible=False)
    result['primary_entry']='tools/build_development_patch_036_v1.py'
    result['limits'].append('036 exact500 source-bound NPC clones; native RAM/compression retained. Exact-ROM GBA runtime/scene acquisition/timing/human review pending; NON-DISTRIBUTION')


def preflight():
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();inputs=load_inputs(source,preflight_only=True)
    try:require_admission()
    except ValueError as e:refusal=str(e)
    else:raise ValueError('Admission now changed; rerun through real primary integration, not this pending-gate preflight')
    from cumulative_batch500 import frozen_write
    p=ROOT/'analysis/pending_insertion_500_036_npc_inputs_v1/product_preflight_v1.json'
    frozen_write(p,dict(passed=True,scope='Source input validation and pending035 gate refusal; installer/finalizer NOT executed',inputs=len(inputs),units=sum(r['translated_units'] for r,_ in inputs),baseline_sha256=BASE_SHA,manifest=ref(ROOT/MANIFEST),gate_refusal=refusal,tool=ref(ROOT/'tools/field_npc_rom_product_036_v1.py'),rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False))
    print('PASS036 product input preflight500; pending035 natural route correctly REFUSED; no install/ROM')


if __name__=='__main__':
    if sys.argv[1:]==['--preflight']:preflight()
    else:raise SystemExit('Use --preflight; this module never builds a ROM independently')
