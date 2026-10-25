"""038 source-regenerated full-carry component for the one primary builder."""
import struct
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from prepare_native_inputs038_v1 import OUT as INPUT_DIR,selected_from,validators,ref
from prepare_source500_038_v5 import OUT as SOURCE,BASE,BASE_SHA
from prepare_repartition500 import layout_records
from field_native_rom_selector_038_v1 import source_population,wrap
from field_native_rom_product_037_v2 import verify_final as verify037
from survey_aggregate_pet_033 import replace_exact
from tpl_literals import literals,skeleton,resolve_units
from canonical_literals_031 import canonical_literals
from archive_scripts import verify_untouched_scripts,script_spans
from build_development_patch import validate_characters,validate_literal_numerals
from verify_tpi_index import lz77_decompress,parse_tpi
from keyitem_rom_selector import INSTALL
from extended_dialogue import assemble_verified

MANIFEST=INPUT_DIR+'/manifest.json'
CPU='analysis/pending_insertion_500_038_selector_cpu_v1/cpu.json'

def require_admission():
    require_hash(ROOT/BASE,BASE_SHA);status=read('analysis/pending500_037_v2/batch_status.json')
    if status['artifact_audited_ROM_sha256']!=BASE_SHA or not status['new037_board_actual_caller_selector_and_Korean_display_verified']:raise ValueError('037 representative runtime prerequisite')
    paths=['analysis/pending500_037_v2/integration.json','analysis/pending500_037_v2/integrity_v1.json','analysis/pending500_037_v2/normal_path_v1.json','analysis/pending500_037_v2/qualified_native_v1.json','analysis/pending500_037_v2/board_qualified_v1.json']
    for path in paths:
        r=read(path)
        if not r['passed'] or r['rom_sha256']!=BASE_SHA:raise ValueError('037 exact artifact evidence')
    for path in (CPU,'analysis/pending_insertion_500_038_native_tails_v1/cpu.json'):
        r=read(path)
        if not r['passed'] or r['baseline_sha256']!=BASE_SHA or r['rom_written']:raise ValueError('038 native CPU prerequisites')
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    return dict(reports=[ref(ROOT/p) for p in paths+[CPU,'analysis/pending_insertion_500_038_native_tails_v1/cpu.json']],scope='Development integration only; representative037 normal/qualified evidence plus038 CPU, not038 GBA execution or release',release_eligible=False)

def load_inputs(source):
    require_admission();cfg=read('project.json');manifest=read(MANIFEST)
    if sha(source)!=cfg['source_profile']['sha256'] or manifest['source_sha256']!=sha(source) or manifest['baseline_sha256']!=BASE_SHA or manifest['new_units']!=500 or manifest['inherited_units']!=496 or manifest['rom_written']:raise ValueError('038 source/input baseline')
    for p,h in manifest['dependencies'].items():require_hash(ROOT/p,h)
    base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'));verify037(source,base,old['keyitem_rom']);oldids={u['id'] for r in layout_records(old) for u in r['layout']};current={r['archive']:r for r in layout_records(old)}
    s=read(SOURCE+'/selection.json');groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    pool=source_population(source,selected_from(manifest['archives']));check=validators();catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};result=[];seen=set();inherit=set()
    for r in manifest['archives']:
        arc=r['archive'];row=r['source_row'];ids=set(r['new_ids']);oldkeys=set(r['inherited_ids']);allids=ids|oldkeys
        for k in ('source_tpl','target_tpl','compiled','asset'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        if row!=catalog[arc] or not row['compressed'] or row['size_header'] or ids&(seen|oldids) or not oldkeys<=oldids or ids&oldkeys:raise ValueError('038 source/new/inherited storage ownership')
        asset=read(r['asset']['path']);units=resolve_units(asset);native,used=lz77_decompress(source,row['offset']);payload=(ROOT/r['compiled']['path']).read_bytes();field=next(p for p in pool if p['archive']==arc)
        if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False or {u['id'] for u in units}!=allids or len(units)!=len(allids) or asset['source_sha256']!=sha(source) or asset['source_archive_sha256']!=sha(native):raise ValueError('038 complete authored asset policy')
        if r['scope']['native_root']!=field['root'] or r['scope']['guarded_reader_return_lr']!=field['caller_lr'] or r['scene']!=field['scene'] or row['pointers']!=[field['pointer']] or r['scope']['script_count']!=struct.unpack_from('<H',native)[0]//2 or len(native)> {0x02039800:0x3000,0x0203C800:0x1000,0x0203D800:0x2800}[field['root']]:raise ValueError('038 typed consumer/source capacity')
        if base[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used] or any(base[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('038 original compression/lookup changed')
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=replace_exact(original,{u['id']:u['translation'] for u in units});raw={u.key:u.text for u in literals(original)}
        if any(u['state']!='needs_review' or u['source']!=raw[u['id']] for u in units) or skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals((ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig'))]:raise ValueError('038 source/selected wording/control structure')
        newtarget=replace_exact(original,{u['id']:u['translation'] for u in units if u['id'] in ids})
        for g in groups[arc]:
            if check[g['profile']](original,newtarget,[g['script']],set(g['geometry_ids']),99)!=g['geometry']:raise ValueError('038 geometry/source tail profile')
        if r['parent_record']:
            parent=current.get(arc)
            if parent!=r['parent_record'] or {u['id'] for u in parent['layout']}!=oldkeys:raise ValueError('038 parent clone identity')
            links=r['parent_asset_lineage']
            if len(links)!=1:raise ValueError('038 parent authored owner')
            link=links[0];require_hash(ROOT/link['path'],link['sha256']);prior=resolve_units(read(link['path']));indexed={u['id']:u for u in units}
            if any(indexed.get(u['id'])!=u for u in prior):raise ValueError('038 prior authored wording/state altered')
            before=base[parent['rom_offset']:parent['rom_offset']+parent['compiled_bytes']]
        else:
            if oldkeys or arc in current:raise ValueError('038 untracked parent')
            before=native
        if sha(payload)!=r['compiled_sha256'] or len(payload)!=r['compiled_bytes'] or len(payload)>65535 or verify_untouched_scripts(before,payload,r['scope']['script_count'],set(r['new_scripts']))!=r['parent_unselected_scripts']:raise ValueError('038 target/carry/unselected scripts')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));seen|=ids;inherit|=oldkeys;result.append((r,payload))
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(inherit)!=496 or len(result)!=66:raise ValueError('038 full500/496/66 input denominator')
    return result

def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    admission=require_admission();base=(ROOT/BASE).read_bytes()
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or key_patches[0][1]!=base[INSTALL:INSTALL+12] or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or 'npc037' not in keymeta:raise ValueError('038 source-regenerated037 append/stub prerequisite')
    tail=bytearray(appended);placements=[];records=[];work.mkdir(parents=True,exist_ok=False)
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));off=len(source)+len(tail);tail.extend(data);return off
    for r,expected in inputs:
        arc=r['archive'];asset=read(r['asset']['path']);units=resolve_units(asset);original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=replace_exact(original,{u['id']:u['translation'] for u in units});f=work/arc;f.mkdir();tp=f/'target.tpl';bp=f/(arc+'.msg');tp.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],f/'compile.log');payload=bp.read_bytes()
        if payload!=expected:raise ValueError('038 immutable-source/authored-assets recompile differs')
        layout=validate_characters(target,plugins/'exe45-utf8.tbl',r['scope'],set(r['new_ids'])|set(r['inherited_ids']))
        if layout!=r['layout']:raise ValueError('038 current primary metrics')
        native=lz77_decompress(source,r['source_row']['offset'])[0];parent=r['parent_record']
        if parent:
            before=bytes(tail[parent['rom_offset']-len(source):parent['rom_offset']-len(source)+parent['compiled_bytes']])
            if sha(before)!=parent['compiled_sha256']:raise ValueError('038 actual regenerated037 parent payload')
        else:before=native
        kept=verify_untouched_scripts(before,payload,r['scope']['script_count'],set(r['new_scripts']))
        if kept!=r['parent_unselected_scripts']:raise ValueError('038 regenerated parent carry bytes')
        np=alloc(native);cp=alloc(payload);placements.append(dict(source_archive=arc,source_class=r['source_class'],scene=r['scene'],root=r['scope']['native_root'],caller_lr=r['scope']['guarded_reader_return_lr'],script_count=r['scope']['script_count'],native_copy_offset=np,native_copy_bytes=len(native),native_copy_sha256=sha(native),rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),source_row=r['source_row']))
        records.append(dict(archive=arc,rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),layout=layout,translated_units=len(units),script_count=r['scope']['script_count'],source_sha256=sha(native),source_bytes=len(native),native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,protected_controls_unchanged=True,native_ram_archive_retained=True,cumulative038=dict(scope=r['scope'],new_ids=r['new_ids'],new_scripts=r['new_scripts'],inherited_ids=r['inherited_ids'],supersedes_parent_record=(dict(archive=r['parent_record']['archive'],rom_offset=r['parent_record']['rom_offset'],compiled_sha256=r['parent_record']['compiled_sha256']) if r['parent_record'] else None),manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes())),unselected_script_bytes_preserved=kept))
    desc=alloc(b''.join(struct.pack('<7I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['scene'],p['root'],p['caller_lr'],p['script_count']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4));code_at=len(source)+len(tail);previous=0x08000000+keymeta['npc037']['code_offset'];code,proof=wrap(source,0x08000000+code_at,previous,0x08000000+desc,len(placements));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+code_at+1))
    if len(stub)!=12:raise ValueError('038 single composed stub')
    keymeta['npc038']=dict(descriptor_offset=desc,code_offset=code_at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,admission=admission,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'038 typed NPC/board/hint reader composed over037; full authored carry')],keymeta,records

def verify_final(source,target,keymeta):
    n=keymeta['npc038'];stub=bytes.fromhex(n['final_stub_hex'])
    if target[INSTALL:INSTALL+12]!=stub:raise ValueError('038 installed composed reader')
    previous=bytearray(target);previous[INSTALL:INSTALL+12]=bytes.fromhex(n['preceding_stub_hex']);verify037(source,previous,keymeta)
    code,proof=wrap(source,0x08000000+n['code_offset'],0x08000000+keymeta['npc037']['code_offset'],0x08000000+n['descriptor_offset'],len(n['placements']))
    if proof!=n['wrapper'] or len(code)!=n['code_bytes'] or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError('038 complete code/final literals')
    selected={p['source_archive']:dict(scene=p['scene'],source_class=p['source_class'],target_sha256=p['compiled_sha256'],script_count=p['script_count']) for p in n['placements']};source_population(source,selected)
    if len(selected)!=66:raise ValueError('038 descriptor owner population')
    for i,p in enumerate(n['placements']):
        a,b=p['rom_offset'],p['native_copy_offset'];native,used=lz77_decompress(source,p['source_row']['offset']);off=p['source_row']['offset']
        if target[b:b+len(native)]!=native or sha(target[a:a+p['compiled_bytes']])!=p['compiled_sha256'] or struct.unpack_from('<7I',target,n['descriptor_offset']+28*i)!=(0x08000000+a,0x08000000+b,len(native),p['scene'],p['root'],p['caller_lr'],p['script_count']):raise ValueError('038 compiled/native/descriptor identity')
        if target[off:off+used]!=source[off:off+used] or any(target[x:x+4]!=source[x:x+4] for x in p['source_row']['pointers']):raise ValueError('038 original source/lookup altered')
    return True

def predecessor_view(source,target,keymeta):
    """Verified regenerated037 projection for its unchanged whole-image gate."""
    n=keymeta['npc038'];base=(ROOT/BASE).read_bytes()
    if target[INSTALL:INSTALL+12]!=bytes.fromhex(n['final_stub_hex']):raise ValueError('038 parent projection final stub')
    parent=bytearray(target[:len(base)]);parent[INSTALL:INSTALL+12]=bytes.fromhex(n['preceding_stub_hex'])
    if sha(parent)!=BASE_SHA:raise ValueError('038 regenerated complete037 parent projection')
    verify037(source,parent,keymeta)
    return bytes(parent)

def finalize(source,target,result,inputs,records):
    require_admission();base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'))
    if len(target)<=len(base) or target[:INSTALL]!=base[:INSTALL] or target[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('038 preceding037 image changed')
    before=list(layout_records(old));prior=list(layout_records(result))
    if [(r['archive'],r['compiled_sha256'],r['layout']) for r in before]!=[(r['archive'],r['compiled_sha256'],r['layout']) for r in prior]:raise ValueError('038 old578 records/owner metrics changed')
    result['keyitem_rom']['npc038']['archives']=records;oldids={u['id'] for r in before for u in r['layout']};allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for r,_ in inputs for k in r['new_ids']}
    if len(new)!=500 or oldids-allids or allids-oldids!=new or result['translated_units']!=old['translated_units']:raise ValueError('038 exact cumulative500 delta')
    cpu=read(CPU);fixture=cpu['fixture_only']
    if sha(target)!=fixture['fixture_sha256'] or len(target)!=fixture['fixture_bytes']:raise ValueError('038 entire primary image differs from original-caller CPU fixture')
    result['translated_units']+=500
    for r,_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='038 active full-carry typed owner; explicitly supersedes parent if declared'))
    result['pending_batch500_038']=dict(new_units=500,inherited_units_unchanged=496,archives=66,manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes()),rom_integrated=True,runtime='pending',release_eligible=False)
    result['active_fullcarry_owners038']={r['archive']:dict(asset=r['asset'],supersedes=r['parent_asset_lineage']) for r,_ in inputs};result['primary_entry']='tools/build_development_patch_038_v2.py';result['limits'].append('038 exact500 with full496 carry; actual038 GBA execution/lookup/timing/human review pending; NON-DISTRIBUTION')
