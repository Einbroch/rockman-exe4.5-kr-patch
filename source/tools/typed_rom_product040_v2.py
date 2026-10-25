"""040 immutable-source primary component: three typed consumers, exact500+8."""
import json,struct
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from prepare_typed_inputs040_v1 import OUT as INPUT_DIR,ref
from fixture_typed040_v1 import SOURCE,BASE,BASE_SHA
from consumer_links040_v1 import contracts,source_population,CLASSES
from typed_rom_selector040_v1 import wrap
from communication_rom_product039_v1 import verify_final as verify039
from prepare_repartition500 import layout_records
from verify_pending500_002_rom import clones
from tpl_literals import literals,skeleton,resolve_units
from survey_aggregate_pet_033 import replace_exact
from profile_quick_geometry039_v1 import validate as comm_geometry
from battle_bbs_geometry040_v1 import validate as bbs_geometry
from normal_timing_capacity_025 import validate as normal_geometry
from build_development_patch import validate_characters,validate_literal_numerals
from archive_scripts import verify_untouched_scripts
from canonical_literals_031 import canonical_literals
from verify_tpi_index import parse_tpi,lz77_decompress
from keyitem_rom_selector import INSTALL
from extended_dialogue import assemble_verified

MANIFEST=INPUT_DIR+'/manifest.json'
CPU=SOURCE+'/selector_cpu_v1.json'


def require_admission():
    require_hash(ROOT/BASE,BASE_SHA);status=read('analysis/pending500_039_v1/batch_status.json')
    if status['current_ROM_sha256']!=BASE_SHA or not status['new039_communication_display_verified'] or not status['independent_rebuild_byte_identical']:raise ValueError('040 prior039 exact runtime baseline')
    require_hash(ROOT/MANIFEST,'111e2fa91e80a4df395d77eb345f043a9d39e63c5f467834c2eecc0af43527e4')
    require_hash(ROOT/SOURCE/'selection.json','d386fed7afbd483b43b1bc5d0c7073b360fed7fd20890fa70038b029a7670bb8')
    require_hash(ROOT/SOURCE/'verification_v1.json','eaf2793403d87840e55474bcddb18af2c78623dfcba02af57c3bd15475e60b66')
    require_hash(ROOT/SOURCE/'tournament_boundary_v1.json','fdd8efd11efe489d44414a7ac847030b4c532857e3fbf0ac5f49d4481cb49e44')
    paths=[CPU,SOURCE+'/bbs_boundary_v2.json',SOURCE+'/tournament_boundary_v1.json']
    for path in paths:
        r=read(path)
        if not r['passed'] or r['baseline_sha256']!=BASE_SHA:raise ValueError('040 source/CPU/qualified original runtime prerequisite')
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
        if 'receipt' in r:
            q=r['receipt'];require_hash(ROOT/q['path'],q['sha256']);receipt=read(q['path'])
            if not receipt['complete'] or receipt['rom_sha256']!=BASE_SHA:raise ValueError('040 exact baseline receipt')
            for name,h in receipt['artifacts'].items():require_hash((ROOT/q['path']).parent/name,h)
    return dict(reports=[ref(ROOT/p) for p in paths],scope='Development-only admission from source500/carry8 +prefix CPU +qualified original039 three-domain boundaries; exact040 runtime pending. Frozen registry earlier pending-admission state is not runtime certification.',release_eligible=False)


def authored(r):
    units=resolve_units(read(r['asset']['path']));original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig')
    return units,original,replace_exact(original,{u['id']:u['translation'] for u in units})


def load_inputs(source):
    require_admission();cfg=read('project.json');manifest=read(MANIFEST);s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json');base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'));verify039(source,base,old['keyitem_rom'])
    if sha(source)!=cfg['source_profile']['sha256'] or manifest['source_sha256']!=sha(source) or manifest['baseline_sha256']!=BASE_SHA or manifest['new_units']!=500 or manifest['inherited_units']!=8 or manifest['rom_written'] or not v['passed']:raise ValueError('040 immutable source/registry')
    for report in (manifest,s,v):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    before=list(layout_records(old));oldids={u['id'] for r in before for u in r['layout']};catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    chosen={r['archive']:r['source_class'] for r in manifest['archives']};pool={p['archive']:p for p in source_population(source,chosen)};seen=set();carry=set();result=[]
    if manifest['selector_contract']!=json.loads(json.dumps(contracts(source))):raise ValueError('040 exact original typed ABI')
    for r,vr in zip(manifest['archives'],v['archives'],strict=True):
        arc=r['archive'];row=r['source_row'];ids=set(r['new_ids']);inherited=set(r['inherited_ids']);kind=r['source_class'];abi=CLASSES[kind]
        for k in ('source_tpl','target_tpl','compiled','asset'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        if r['archive']!=vr['archive'] or row!=catalog[arc] or not row['compressed'] or row['size_header'] or ids&(seen|oldids) or not inherited<=oldids:raise ValueError('040 source/population/ownership')
        native,used=lz77_decompress(source,row['offset']);payload=(ROOT/r['compiled']['path']).read_bytes();asset=read(r['asset']['path']);units,original,target=authored(r);raw={u.key:u.text for u in literals(original)}
        if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False or asset['source_sha256']!=sha(source) or asset['source_archive_sha256']!=sha(native) or units!=vr['units'] or {u['id'] for u in units}!=ids|inherited or len(units)!=len(ids|inherited) or any(u['state']!='needs_review' or u['source']!=raw[u['id']] for u in units):raise ValueError('040 authored source/policy/complete population')
        lineage=asset['selected_wording_lineage']
        if len(lineage['canonical_drafts'])!=len(ids) or {d['id'] for d in lineage['canonical_drafts']}!=ids:raise ValueError('040 canonical wording denominator')
        for d in lineage['canonical_drafts']:
            require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);canonical=next(u for u in a['units'] if u['id']==d['id']);u=next(u for u in units if u['id']==d['id'])
            if a['source_sha256']!=sha(source) or a['source_tpl']!=r['source_tpl'] or canonical['translation']!=u['canonical_wording'] or canonical['source']!=u['source'] or canonical['state']!=u['state'] or u['translation'].replace('\n',' ')!=canonical['translation'].replace('\n',' '):raise ValueError('040 selected exact canonical words')
        if skeleton(target)!=skeleton(original) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals((ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig'))]:raise ValueError('040 protected controls/current target')
        for g in groups[arc]:
            subset={u['id']:u['translation'] for u in units if u['id'] in g['ids']};one=replace_exact(original,subset)
            if subset!=g['explicit_layouts']:raise ValueError('040 selected explicit LF/word layout')
            geo=comm_geometry(original,one,[g['script']],set(g['ids'])) if kind=='communication-help' else bbs_geometry(original,one,[g['script']],set(g['ids'])) if kind=='battle-BBS-trial' else normal_geometry(original,one,[g['script']],set(g['ids']),99,88)
            if json.loads(json.dumps(geo))!=g['geometry']:raise ValueError('040 consumer-specific geometry')
        if (r['scope']['native_root'],r['scope']['guarded_reader_return_lr'],r['scope']['saved_outer_reader_return_lr'])!=(abi['root'],abi['caller_lr'],abi['outer_lr']) or r['scope']['script_count']!=struct.unpack_from('<H',native)[0]//2 or set(row['pointers'])!={p['pointer'] for p in pool[arc]['references']} or sha(native)!=r['native_sha256']:raise ValueError('040 typed native source/table ABI')
        prior=native
        if inherited:
            parent=r['parent_asset'];require_hash(ROOT/parent['path'],parent['sha256'])
            if old['active_communication_owners039'].get(arc)!=parent:raise ValueError('040 authored active parent owner')
            oldunits=resolve_units(read(parent['path']))
            if oldunits!=[u for u in units if u['id'] in inherited]:raise ValueError('040 exact inherited authored units')
            p=next(x for x in old['keyitem_rom']['communication039']['archives'] if x['archive']==arc)
            if {k:p[k] for k in r['parent_record_identity']}!=r['parent_record_identity'] or {u['id'] for u in p['layout']}!=inherited:raise ValueError('040 exact inherited record')
            prior=base[p['rom_offset']:p['rom_offset']+p['compiled_bytes']]
            if sha(prior)!=p['compiled_sha256'] or {u['id']:u for u in p['layout']}!={u['id']:u for u in r['layout'] if u['id'] in inherited}:raise ValueError('040 inherited bytes/metrics')
        elif r['parent_asset'] is not None or r['parent_record_identity'] is not None or any(x['archive']==arc for x in before):raise ValueError('040 unexpected owned archive')
        if base[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used] or any(base[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('040 source LZ/lookup retained')
        if len(payload)>65535 or len(payload)!=r['compiled_bytes'] or sha(payload)!=r['compiled_sha256'] or verify_untouched_scripts(prior,payload,r['scope']['script_count'],set(r['new_scripts']))!=r['unselected_current039_scripts']:raise ValueError('040 compiled/unselected current scripts')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));seen|=ids;carry|=inherited;result.append((r,payload))
    if len(result)!=10 or len(list(clones(old)))!=661 or seen!=set(s['selected_ids']) or len(seen)!=500 or len(carry)!=8:raise ValueError('040 exact500/carry8/10/old661')
    return result


def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    admission=require_admission();base=(ROOT/BASE).read_bytes()
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or key_patches[0][1]!=base[INSTALL:INSTALL+12] or len(source)+len(appended)!=len(base) or appended!=base[len(source):] or 'communication039' not in keymeta:raise ValueError('040 regenerated039 complete predecessor')
    tail=bytearray(appended);placements=[];records=[];work.mkdir(parents=True,exist_ok=False)
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);tail.extend(data);return at
    for r,expected in inputs:
        arc=r['archive'];units,original,target=authored(r);f=work/arc;f.mkdir();tp=f/'target.tpl';bp=f/(arc+'.msg');tp.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],f/'compile.log');payload=bp.read_bytes();layout=validate_characters(target,plugins/'exe45-utf8.tbl',r['scope'],{u['id'] for u in units})
        if payload!=expected or layout!=r['layout']:raise ValueError('040 primary authored compile/metrics')
        native=lz77_decompress(source,r['source_row']['offset'])[0];prior=native
        if r['inherited_ids']:
            owner=r['parent_record_identity'];prior=base[owner['rom_offset']:owner['rom_offset']+owner['compiled_bytes']]
        kept=verify_untouched_scripts(prior,payload,r['scope']['script_count'],set(r['new_scripts']))
        if kept!=r['unselected_current039_scripts']:raise ValueError('040 primary current unselected scripts')
        np=alloc(native);cp=alloc(payload);abi=CLASSES[r['source_class']]
        placements.append(dict(source_archive=arc,source_class=r['source_class'],script_count=r['scope']['script_count'],native_copy_offset=np,native_copy_bytes=len(native),native_copy_sha256=sha(native),rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),source_row=r['source_row'],**abi))
        records.append(dict(archive=arc,rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),layout=layout,translated_units=len(units),script_count=r['scope']['script_count'],source_sha256=sha(native),source_bytes=len(native),native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,protected_controls_unchanged=True,native_ram_archive_retained=True,cumulative040=dict(scope=r['scope'],new_ids=r['new_ids'],new_scripts=r['new_scripts'],inherited_ids=r['inherited_ids'],parent_record_identity=r['parent_record_identity'],manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes())),unselected_script_bytes_preserved=kept))
    desc=alloc(b''.join(struct.pack('<7I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['script_count'],p['root'],p['caller_lr'],p['outer_lr']) for p in placements));tail.extend(b'\xff'*(-len(tail)%4));at=len(source)+len(tail);previous=0x08000000+keymeta['communication039']['code_offset'];code,proof=wrap(source,0x08000000+at,previous,0x08000000+desc,len(placements));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+at+1))
    if len(stub)!=12:raise ValueError('040 one composed stub')
    keymeta['typed040']=dict(descriptor_offset=desc,code_offset=at,code_bytes=len(code),code_sha256=sha(code),previous_wrapper_address=previous,wrapper=proof,stub=stubproof,preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,admission=admission,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'040 typed three-consumer full-native selector over039; original LZ/shared RAM retained')],keymeta,records


def predecessor_view(source,target,keymeta):
    n=keymeta['typed040'];base=(ROOT/BASE).read_bytes()
    if target[INSTALL:INSTALL+12]!=bytes.fromhex(n['final_stub_hex']):raise ValueError('040 projection final stub')
    parent=bytearray(target[:len(base)]);parent[INSTALL:INSTALL+12]=bytes.fromhex(n['preceding_stub_hex'])
    if sha(parent)!=BASE_SHA:raise ValueError('040 complete regenerated039 projection')
    verify039(source,parent,keymeta);return bytes(parent)


def verify_final(source,target,keymeta):
    predecessor_view(source,target,keymeta);n=keymeta['typed040'];code,proof=wrap(source,0x08000000+n['code_offset'],0x08000000+keymeta['communication039']['code_offset'],0x08000000+n['descriptor_offset'],len(n['placements']))
    if json.loads(json.dumps(proof))!=json.loads(json.dumps(n['wrapper'])) or len(code)!=n['code_bytes'] or sha(code)!=n['code_sha256'] or target[n['code_offset']:n['code_offset']+len(code)]!=code:raise ValueError('040 complete code/literals')
    source_population(source,{p['source_archive']:p['source_class'] for p in n['placements']})
    if len(n['placements'])!=10:raise ValueError('040 descriptor denominator')
    for i,p in enumerate(n['placements']):
        a,b=p['rom_offset'],p['native_copy_offset'];native,used=lz77_decompress(source,p['source_row']['offset']);off=p['source_row']['offset'];abi=CLASSES[p['source_class']]
        if any(p[k]!=abi[k] for k in abi) or target[b:b+len(native)]!=native or sha(target[a:a+p['compiled_bytes']])!=p['compiled_sha256'] or struct.unpack_from('<7I',target,n['descriptor_offset']+28*i)!=(0x08000000+a,0x08000000+b,len(native),p['script_count'],abi['root'],abi['caller_lr'],abi['outer_lr']):raise ValueError('040 typed native/compiled/descriptor')
        if target[off:off+used]!=source[off:off+used] or any(target[x:x+4]!=source[x:x+4] for x in p['source_row']['pointers']):raise ValueError('040 original LZ/source references')
    return True


def finalize(source,target,result,inputs,records):
    require_admission();verify_final(source,target,result['keyitem_rom']);old=read(BASE.replace('.gba','.json'));before=list(layout_records(old));prior=list(layout_records(result))
    if [(r['archive'],r['compiled_sha256'],r['layout']) for r in before]!=[(r['archive'],r['compiled_sha256'],r['layout']) for r in prior]:raise ValueError('040 old661 consumer records')
    result['keyitem_rom']['typed040']['archives']=records;oldids={u['id'] for r in before for u in r['layout']};allids={u['id'] for r in layout_records(result) for u in r['layout']};new={k for r,_ in inputs for k in r['new_ids']};carry={k for r,_ in inputs for k in r['inherited_ids']}
    if len(new)!=500 or len(carry)!=8 or oldids-allids or allids-oldids!=new or result['translated_units']!=old['translated_units']:raise ValueError('040 exact cumulative500/carry8')
    fixture=read(CPU)['fixture_only']
    if sha(target)!=fixture['fixture_sha256'] or len(target)!=fixture['fixture_bytes']:raise ValueError('040 complete primary differs from PREFIX CPU fixture')
    result['translated_units']+=500
    for r,_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='040 active typed authored owner'))
    result['active_typed_owners040']={r['archive']:r['asset'] for r,_ in inputs};result['active_communication_owners040']=dict(old['active_communication_owners039'])
    for r,_ in inputs:
        if r['source_class']=='communication-help':result['active_communication_owners040'][r['archive']]=r['asset']
    result['pending_batch500_040']=dict(new_units=500,inherited_units_unchanged=8,archives=10,manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes()),rom_integrated=True,runtime='pending',release_eligible=False,superseded039_owner_archives=[r['archive'] for r,_ in inputs if r['parent_asset']])
    result['primary_entry']='tools/build_development_patch_040_v2.py';result['limits'].append('040 exact500+carry8 three-domain integration: Korean040 BBS geometry/caches/terminal/exit and tournament/communication runtime pending; Japanese fixed-cell labels unchanged; NON-DISTRIBUTION')
