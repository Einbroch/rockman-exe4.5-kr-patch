"""Source-regenerated039 communication component in the primary build graph."""
import json,struct
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from prepare_communication_inputs039_v1 import OUT as INPUT_DIR,ref
from fixture_communication039_v1 import OUT as SOURCE
from communication_rom_selector039_v1 import source_population,wrap,contracts
from field_native_rom_product_038_v2 import verify_final as verify038
from prepare_repartition500 import layout_records
from tpl_literals import literals,skeleton,resolve_units
from survey_aggregate_pet_033 import replace_exact
from profile_quick_geometry039_v1 import validate
from profile_layout039_v1 import reconstruct
from build_development_patch import validate_characters,validate_literal_numerals
from archive_scripts import verify_untouched_scripts
from canonical_literals_031 import canonical_literals
from verify_tpi_index import parse_tpi,lz77_decompress
from keyitem_rom_selector import INSTALL
from extended_dialogue import assemble_verified

BASE='poc/output/pending500_038_v2.gba'
BASE_SHA='97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b'
MANIFEST=INPUT_DIR+'/manifest.json'
CPU=SOURCE+'/selector_cpu_v2.json'


def require_admission():
    require_hash(ROOT/BASE,BASE_SHA);status=read('analysis/pending500_038_v2/batch_status.json')
    if status['artifact_audited_ROM_sha256']!=BASE_SHA or not status['new038_three_classes_Korean_display_verified']:raise ValueError('039 prior038 runtime prerequisite')
    paths=[CPU,SOURCE+'/native_controls_cpu_v1.json',SOURCE+'/baseline_boundary_v2.json']
    for path in paths:
        r=read(path)
        if not r['passed'] or r['baseline_sha256']!=BASE_SHA or r['rom_written']:raise ValueError('039 CPU/source boundary prerequisite')
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    return dict(reports=[ref(ROOT/p) for p in paths],scope='Development build only; selector PREFIX CPU +038 boundary, actual039 runtime pending',release_eligible=False)


def load_inputs(source):
    require_admission();cfg=read('project.json');manifest=read(MANIFEST);s=read(SOURCE+'/selection.json');base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'));verify038(source,base,old['keyitem_rom'])
    if sha(source)!=cfg['source_profile']['sha256'] or manifest['source_sha256']!=sha(source) or manifest['baseline_sha256']!=BASE_SHA or manifest['new_units']!=500 or manifest['inherited_units'] or manifest['rom_written']:raise ValueError('039 immutable source/registry')
    for p,h in manifest['dependencies'].items():require_hash(ROOT/p,h)
    oldids={u['id'] for r in layout_records(old) for u in r['layout']};owners={r['archive'] for r in layout_records(old)};catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    pool={p['archive']:p for p in source_population(source,{r['archive'] for r in manifest['archives']})};abi=contracts(source);seen=set();result=[]
    for r in manifest['archives']:
        arc=r['archive'];row=r['source_row'];ids=set(r['new_ids'])
        for k in ('source_tpl','target_tpl','compiled','asset'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        if row!=catalog[arc] or not row['compressed'] or row['size_header'] or ids&(seen|oldids) or arc in owners or r['inherited_ids'] or r['parent_record'] is not None:raise ValueError('039 source/no-carry owner')
        native,used=lz77_decompress(source,row['offset']);payload=(ROOT/r['compiled']['path']).read_bytes();asset=read(r['asset']['path']);units=resolve_units(asset);original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');raw={u.key:u.text for u in literals(original)}
        if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False or asset['source_sha256']!=sha(source) or asset['source_archive_sha256']!=sha(native) or {u['id'] for u in units}!=ids or len(units)!=len(ids):raise ValueError('039 authored asset policy/identity')
        for d in asset['selected_wording_lineage']['canonical_drafts']:
            require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);canonical=next(u for u in a['units'] if u['id']==d['id']);u=next(u for u in units if u['id']==d['id']);p=u['explicit_layout_proposal']
            if a['source_sha256']!=sha(source) or a['source_tpl']!=r['source_tpl'] or canonical['translation']!=u['canonical_wording'] or canonical['source']!=u['source'] or canonical['state']!=u['state'] or p['canonical']!=canonical['translation'] or p['soft_breaks'] or p['target']!=u['translation'] or reconstruct(p['lines'],p['break_kinds'])!=p['flat_wording'] or u['translation'].replace('\n',' ')!=canonical['translation'].replace('\n',' '):raise ValueError('039 canonical wording/layout source binding')
        if len(asset['selected_wording_lineage']['canonical_drafts'])!=len(ids) or any(u['state']!='needs_review' or u['source']!=raw[u['id']] for u in units):raise ValueError('039 literal source/state')
        target=replace_exact(original,{u['id']:u['translation'] for u in units})
        if skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals((ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig'))]:raise ValueError('039 protected target topology')
        for g in groups[arc]:
            subset={u['id']:u['translation'] for u in units if u['id'] in g['ids']}
            if json.loads(json.dumps(validate(original,replace_exact(original,subset),[g['script']],set(g['ids'])),ensure_ascii=False))!=g['geometry']:raise ValueError('039 communication geometry')
        if r['scope']['native_root']!=abi['root'] or r['scope']['guarded_reader_return_lr']!=abi['inner_lr'] or r['scope']['saved_outer_reader_return_lr']!=abi['outer_lr'] or r['scope']['script_count']!=struct.unpack_from('<H',native)[0]//2 or set(row['pointers'])!={p['pointer'] for p in pool[arc]['references']}:raise ValueError('039 scoped reader/table ABI')
        if base[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used] or any(base[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('039 original LZ/lookup retained')
        if len(payload)>65535 or len(payload)!=r['compiled_bytes'] or sha(payload)!=r['compiled_sha256'] or verify_untouched_scripts(native,payload,r['scope']['script_count'],set(r['new_scripts']))!=r['unselected_source_scripts']:raise ValueError('039 target/unselected scripts')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));seen|=ids;result.append((r,payload))
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(result)!=17:raise ValueError('039 exact500/17')
    return result


def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    admission=require_admission();base=(ROOT/BASE).read_bytes()
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or key_patches[0][1]!=base[INSTALL:INSTALL+12] or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or 'npc038' not in keymeta:raise ValueError('039 regenerated complete038 prerequisite')
    tail=bytearray(appended);placements=[];records=[];work.mkdir(parents=True,exist_ok=False)
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);tail.extend(data);return at
    for r,expected in inputs:
        arc=r['archive'];units=resolve_units(read(r['asset']['path']));original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=replace_exact(original,{u['id']:u['translation'] for u in units});folder=work/arc;folder.mkdir();tp=folder/'target.tpl';bp=folder/(arc+'.msg');tp.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],folder/'compile.log');payload=bp.read_bytes()
        if payload!=expected:raise ValueError('039 authored current compile mismatch')
        layout=validate_characters(target,plugins/'exe45-utf8.tbl',r['scope'],set(r['new_ids']))
        if layout!=r['layout']:raise ValueError('039 primary metrics')
        native=lz77_decompress(source,r['source_row']['offset'])[0];kept=verify_untouched_scripts(native,payload,r['scope']['script_count'],set(r['new_scripts']))
        if kept!=r['unselected_source_scripts']:raise ValueError('039 source unselected scripts')
        np=alloc(native);cp=alloc(payload);placements.append(dict(source_archive=arc,source_class='communication-help',script_count=r['scope']['script_count'],native_copy_offset=np,native_copy_bytes=len(native),native_copy_sha256=sha(native),rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),source_row=r['source_row']))
        records.append(dict(archive=arc,rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),layout=layout,translated_units=len(units),script_count=r['scope']['script_count'],source_sha256=sha(native),source_bytes=len(native),native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,protected_controls_unchanged=True,native_ram_archive_retained=True,cumulative039=dict(scope=r['scope'],new_ids=r['new_ids'],new_scripts=r['new_scripts'],inherited_ids=[],manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes())),unselected_script_bytes_preserved=kept))
    desc=alloc(b''.join(struct.pack('<4I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['script_count']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);previous=0x08000000+keymeta['npc038']['code_offset'];code,proof=wrap(source,0x08000000+at,previous,0x08000000+desc,len(placements));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+at+1))
    if len(stub)!=12:raise ValueError('039 single composed stub')
    keymeta['communication039']=dict(descriptor_offset=desc,code_offset=at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,admission=admission,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'039 typed nested communication reader over038; original LZ and shared RAM retained')],keymeta,records


def predecessor_view(source,target,keymeta):
    n=keymeta['communication039'];base=(ROOT/BASE).read_bytes()
    if target[INSTALL:INSTALL+12]!=bytes.fromhex(n['final_stub_hex']):raise ValueError('039 projection final stub')
    parent=bytearray(target[:len(base)]);parent[INSTALL:INSTALL+12]=bytes.fromhex(n['preceding_stub_hex'])
    if sha(parent)!=BASE_SHA:raise ValueError('039 complete regenerated038 projection')
    verify038(source,parent,keymeta);return bytes(parent)


def verify_final(source,target,keymeta):
    predecessor_view(source,target,keymeta);n=keymeta['communication039'];code,proof=wrap(source,0x08000000+n['code_offset'],0x08000000+keymeta['npc038']['code_offset'],0x08000000+n['descriptor_offset'],len(n['placements']))
    if proof!=n['wrapper'] or len(code)!=n['code_bytes'] or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError('039 complete code/literals')
    source_population(source,{p['source_archive'] for p in n['placements']})
    if len(n['placements'])!=17:raise ValueError('039 descriptor denominator')
    for i,p in enumerate(n['placements']):
        a,b=p['rom_offset'],p['native_copy_offset'];native,used=lz77_decompress(source,p['source_row']['offset']);off=p['source_row']['offset']
        if target[b:b+len(native)]!=native or sha(target[a:a+p['compiled_bytes']])!=p['compiled_sha256'] or struct.unpack_from('<4I',target,n['descriptor_offset']+16*i)!=(0x08000000+a,0x08000000+b,len(native),p['script_count']):raise ValueError('039 native/compiled/descriptor')
        if target[off:off+used]!=source[off:off+used] or any(target[x:x+4]!=source[x:x+4] for x in p['source_row']['pointers']):raise ValueError('039 source LZ/table retained')
    return True


def finalize(source,target,result,inputs,records):
    require_admission();predecessor_view(source,target,result['keyitem_rom']);old=read(BASE.replace('.gba','.json'));before=list(layout_records(old));prior=list(layout_records(result))
    if [(r['archive'],r['compiled_sha256'],r['layout']) for r in before]!=[(r['archive'],r['compiled_sha256'],r['layout']) for r in prior]:raise ValueError('039 old644 consumer records')
    result['keyitem_rom']['communication039']['archives']=records;oldids={u['id'] for r in before for u in r['layout']};allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for r,_ in inputs for k in r['new_ids']}
    if len(new)!=500 or oldids-allids or allids-oldids!=new or result['translated_units']!=old['translated_units']:raise ValueError('039 exact cumulative500')
    fixture=read(CPU)['fixture_only']
    if sha(target)!=fixture['fixture_sha256'] or len(target)!=fixture['fixture_bytes']:raise ValueError('039 whole primary image differs from PREFIX CPU fixture')
    result['translated_units']+=500
    for r,_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='039 active communication authored owner'))
    result['pending_batch500_039']=dict(new_units=500,inherited_units_unchanged=0,archives=17,manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes()),rom_integrated=True,runtime='pending',release_eligible=False)
    result['active_communication_owners039']={r['archive']:r['asset'] for r,_ in inputs};result['primary_entry']='tools/build_development_patch_039_v1.py';result['limits'].append('039 exact500 communication help: native full initialization/local menu/render/runtime pending; fixed-cell options unchanged; NON-DISTRIBUTION')
