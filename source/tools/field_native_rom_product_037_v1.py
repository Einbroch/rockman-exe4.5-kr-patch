"""037 typed NPC/board primary component; source036 prefix retained.

No standalone ROM writer. Admission is development-only, not runtime approval.
"""
import struct,sys
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from prepare_native_inputs037_v2 import OUT as INPUT_DIR,selected_from
from prepare_source500_037_v2 import OUT as SOURCE,BASE,BASE_SHA,ref
from prepare_repartition500 import layout_records
from field_native_rom_selector_037_v2 import source_population,wrap
from field_npc_rom_product_036_v1 import verify_final as verify036
from survey_new_storage_036 import VALIDATORS
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
    status=read('analysis/pending500_036_v1/batch_status.json')
    if status['rom_sha256']!=BASE_SHA or not status.get('natural_cached_NPC_selection_verified'):
        raise ValueError('036 normal cached NPC evidence required before037 development build')
    paths=['analysis/pending500_036_v1/integration.json','analysis/pending500_036_v1/natural_cached_display_v1.json','analysis/pending500_036_v1/native_boundaries_v1.json']
    proofs=[]
    for path in paths:
        report=read(path)
        if not report.get('passed') or report.get('rom_sha256')!=BASE_SHA:
            raise ValueError('036 audited exact-ROM evidence required')
        proofs.append(ref(ROOT/path))
    cpu=read('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json')
    if not cpu['passed'] or cpu['baseline_sha256']!=BASE_SHA or cpu['rom_written'] or cpu['descriptor_count']!=70:
        raise ValueError('037 typed source/actual caller CPU evidence required')
    proofs.append(ref(ROOT/'analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json'))
    return dict(reports=proofs,scope='Development integration only;036 natural A0 plus qualified A1/A3.037 A2/board native acquisition/rendering pending',release_eligible=False)


def load_inputs(source,preflight_only=False):
    if not preflight_only:require_admission()
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    if sha(source)!=cfg['source_profile']['sha256']:raise ValueError('037 immutable source identity')
    manifest=read(MANIFEST)
    for p,h in manifest['dependencies'].items():require_hash(ROOT/p,h)
    if not manifest['passed'] or manifest['new_units']!=500 or manifest['source_sha256']!=sha(source) or manifest['baseline_rom']!=BASE or manifest['baseline_sha256']!=BASE_SHA or manifest['rom_written']:raise ValueError('037 registered input contract')
    require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'));verify036(source,base,old['keyitem_rom'])
    oldids={u['id'] for r in layout_records(old) for u in r['layout']};owned={r['archive'] for r in layout_records(old)}
    s=read(SOURCE+'/selection.json');groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    selected=selected_from(manifest['archives']);pool=source_population(source,selected);validators=dict(VALIDATORS);seen=set();result=[]
    for r in manifest['archives']:
        arc=r['archive'];row=r['source_row']
        if arc in owned or row!=catalog[arc] or not row['compressed'] or row['size_header']:raise ValueError('037 new archive storage/ownership')
        for key in ['asset','compiled','source_tpl','target_tpl']:require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        asset=read(r['asset']['path']);units=asset['units'];ids={u['id'] for u in units};payload=(ROOT/r['compiled']['path']).read_bytes();native,used=lz77_decompress(source,row['offset'])
        if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False or asset['archive']!=arc or asset['source_sha256']!=sha(source) or asset['source_archive_sha256']!=sha(native):raise ValueError('037 development asset identity')
        if ids!=set(r['new_ids']) or len(ids)!=len(units) or ids&(seen|oldids) or r['translated_units']!=len(ids):raise ValueError('037 exact disjoint IDs')
        field=next(x for x in pool if x['archive']==arc)
        if field['scene']!=r['scene'] or row['pointers']!=[field['pointer']] or r['native_sha256']!=sha(native) or r['native_bytes']!=len(native):raise ValueError('037 scene/source lookup')
        if base[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used] or any(base[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('037 native source/references altered')
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig');raw={u.key:u.text for u in literals(original)}
        if any(u['state']!='needs_review' or u['source']!=raw[u['id']] for u in units) or skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals(replace_exact(original,{u['id']:u['translation'] for u in units}))]:raise ValueError('037 protected source/target/state')
        scope=r['scope']
        if scope['consumer']!='normal-dialogue' or scope['literal_language']!='mmbn45' or set(scope['literal_ids'])!=ids or scope['storage']!='typed-scene-native-identity-ROM-clone' or scope['scene']!=field['scene'] or scope['guarded_reader_return_lr']!=field['caller_lr'] or scope['native_root']!=field['root'] or r['source_class']!=field['source_class'] or scope['script_count']!=struct.unpack_from('<H',native)[0]//2:raise ValueError('037 explicit runtime scope')
        for g in groups[arc]:
            if validators[g['profile']](original,target,[g['script']],set(g['geometry_ids']),99)!=g['geometry']:raise ValueError('037 geometry/protected consumer')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        if sha(payload)!=r['compiled_sha256'] or len(payload)!=r['compiled_bytes'] or len(payload)>65535 or len(native)>=0x1000 or verify_untouched_scripts(native,payload,r['scope']['script_count'],set(r['new_scripts']))!=r['unselected_scripts']:raise ValueError('037 payload/unselected script proof')
        result.append((r,payload));seen|=ids
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(result)!=70:raise ValueError('037 complete500/20')
    return result


def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    admission=require_admission() # BEFORE creating work files or changing bytes
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or len(key_patches[0][1])!=12 or 'npc036' not in keymeta:raise ValueError('037 one preceding composed reader')
    require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes()
    if source+bytes(appended)==base or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or key_patches[0][1]!=base[INSTALL:INSTALL+12]:raise ValueError('037 source-generated036 append/stub differs')
    tail=bytearray(appended);placements=[];records=[];work.mkdir(parents=True,exist_ok=False)
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));off=len(source)+len(tail);tail.extend(data);return off
    for r,precompiled in inputs:
        arc=r['archive'];asset=read(r['asset']['path']);original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=replace_exact(original,{u['id']:u['translation'] for u in asset['units']})
        f=work/arc;f.mkdir();tp=f/'target.tpl';bp=f/(arc+'.msg');tp.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],f/'compile.log');payload=bp.read_bytes()
        if payload!=precompiled:raise ValueError('037 immutable-source primary recompile')
        layout=validate_characters(target,plugins/'exe45-utf8.tbl',r['scope'],set(r['new_ids']))
        if layout!=r['layout']:raise ValueError('037 primary metrics')
        native=lz77_decompress(source,r['source_row']['offset'])[0];np=alloc(native);cp=alloc(payload)
        placements.append(dict(source_archive=arc,source_class=r['source_class'],scene=r['scene'],root=r['scope']['native_root'],caller_lr=r['scope']['guarded_reader_return_lr'],script_count=r['scope']['script_count'],native_copy_offset=np,native_copy_bytes=len(native),native_copy_sha256=sha(native),rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),source_row=r['source_row']))
        records.append(dict(archive=arc,rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),layout=layout,translated_units=len(asset['units']),script_count=r['scope']['script_count'],source_sha256=sha(native),source_bytes=len(native),native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,protected_controls_unchanged=True,native_ram_archive_retained=True,cumulative037=dict(scope=r['scope'],new_ids=r['new_ids'],new_scripts=r['new_scripts'],manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes())),unselected_script_bytes_preserved=r['unselected_scripts']))
    desc=alloc(b''.join(struct.pack('<7I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['scene'],p['root'],p['caller_lr'],p['script_count']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4));code_at=len(source)+len(tail)
    previous=0x08000000+keymeta['npc036']['code_offset'];code,proof=wrap(source,0x08000000+code_at,previous,0x08000000+desc,len(placements));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+code_at+1))
    if len(stub)!=12:raise ValueError('037 composed reader stub size')
    keymeta['npc037']=dict(descriptor_offset=desc,code_offset=code_at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,admission=admission,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'037 scene/native NPC reader composed over036 and all prior consumers')],keymeta,records


def verify_final(source,target,keymeta):
    n=keymeta['npc037'];stub=bytes.fromhex(n['final_stub_hex']);oldstub=bytes.fromhex(n['preceding_stub_hex'])
    if target[INSTALL:INSTALL+12]!=stub:raise ValueError('037 installed composed reader')
    previous=bytearray(target);previous[INSTALL:INSTALL+12]=oldstub;verify036(source,previous,keymeta)
    code,proof=wrap(source,0x08000000+n['code_offset'],0x08000000+keymeta['npc036']['code_offset'],0x08000000+n['descriptor_offset'],len(n['placements']))
    if proof!=n['wrapper'] or len(code)!=n['code_bytes'] or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError('037 final code/literals')
    selected={p['source_archive']:dict(scene=p['scene'],source_class=p['source_class'],target_sha256=p['compiled_sha256'],script_count=p['script_count']) for p in n['placements']};source_population(source,selected)
    if len(selected)!=70:raise ValueError('037 final descriptor population')
    for i,p in enumerate(n['placements']):
        a=p['rom_offset'];b=p['native_copy_offset'];native,used=lz77_decompress(source,p['source_row']['offset']);off=p['source_row']['offset']
        if target[b:b+len(native)]!=native or sha(target[a:a+p['compiled_bytes']])!=p['compiled_sha256'] or struct.unpack_from('<7I',target,n['descriptor_offset']+i*28)!=(0x08000000+a,0x08000000+b,len(native),p['scene'],p['root'],p['caller_lr'],p['script_count']):raise ValueError('037 native/clone/scene descriptor bytes')
        if target[off:off+used]!=source[off:off+used] or any(target[x:x+4]!=source[x:x+4] for x in p['source_row']['pointers']):raise ValueError('037 original loader assets changed')
    return True


def finalize(source,target,result,inputs,records):
    require_admission();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'))
    if len(target)<=len(base) or target[:INSTALL]!=base[:INSTALL] or target[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('037 preceding036 bytes changed')
    before=list(layout_records(old));prior=list(layout_records(result))
    if [(r['archive'],r['compiled_sha256'],r['layout']) for r in before]!=[(r['archive'],r['compiled_sha256'],r['layout']) for r in prior]:raise ValueError('037 old record/owner/metrics changed')
    result['keyitem_rom']['npc037']['archives']=records;oldids={u['id'] for r in before for u in r['layout']};allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for r,_ in inputs for k in r['new_ids']}
    if len(new)!=500 or oldids-allids or allids-oldids!=new or result['translated_units']!=old['translated_units']:raise ValueError('037 actual cumulative500 delta')
    cpu=read('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json')
    if sha(target)!=cpu['fixture_only']['sha256'] or len(target)!=cpu['fixture_only']['bytes']:raise ValueError('037 final complete artifact differs from actual-caller CPU fixture')
    result['translated_units']+=500
    for r,_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='037 scene/native NPC clone translation owner'))
    result['pending_batch500_037']=dict(new_units=500,archives=70,manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes()),rom_integrated=True,runtime='pending',release_eligible=False)
    result['primary_entry']='tools/build_development_patch_037_v1.py'
    result['limits'].append('037 exact500 source-bound NPC clones; native RAM/compression retained. Exact-ROM GBA runtime/scene acquisition/timing/human review pending; NON-DISTRIBUTION')


if __name__=='__main__':raise SystemExit('Component only; use the037 primary build entry')
