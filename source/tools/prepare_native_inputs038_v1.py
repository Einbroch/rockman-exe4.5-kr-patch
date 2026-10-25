"""Register038 authored new500 plus pinned inherited496 from original assets.

Complete targets are regenerated from immutable source and selected assets,
not reverse-engineered prior-ROM extracts. No ROM writer/admission claim.
"""
from collections import defaultdict
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_038_v5 import baseline,OUT as SOURCE,BASE,BASE_SHA
from prepare_repartition500 import layout_records
from field_native_rom_selector_038_v1 import contracts,source_population
from tpl_literals import literals,skeleton,resolve_units
from survey_aggregate_pet_033 import replace_exact
from survey_new_storage_035 import VALIDATORS
from normal_store_tail038_v1 import validate as stores
from normal_navi_tail038_v1 import validate as navis
from build_development_patch import validate_characters,validate_literal_numerals
from textpet_korean import prepare_plugins
from korean_codec import EXTRA_CHARACTER_INDICES

OUT='analysis/pending_insertion_500_038_native_inputs_v1'
CPU='analysis/pending_insertion_500_038_selector_cpu_v1/cpu.json'
CARRY='analysis/pending_insertion_500_038_carry_v2/verification_v1.json'

def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))
def validators():
    v=dict(VALIDATORS);v.update({'normal-store-tail-geometry':lambda a,b,c,d,e:stores(a,b,c,d,e,88),'normal-navi-tail-geometry':lambda a,b,c,d,e:navis(a,b,c,d,e,88)})
    return v
def selected_from(records):return {r['archive']:dict(source_class=r['source_class'],scene=r['scene'],target_sha256=r['compiled_sha256'],script_count=r['scope']['script_count']) for r in records}

def main():
    cfg,source,base,m=baseline();s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json');c=read(CARRY);cpu=read(CPU);tail=read('analysis/pending_insertion_500_038_native_tails_v1/cpu.json')
    for r in (c,cpu,tail):
        if not r['passed'] or r['rom_written'] or r.get('baseline_sha256')!=BASE_SHA:raise ValueError('038 native/source prerequisite')
        for p,h in r['dependencies'].items():require_hash(ROOT/p,h)
    abi=contracts(source);raw_records={r['archive']:r for r in v['archives']};groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));records=[];seen=set();inherit=set();check=validators()
    for r in c['archives']:
        arc=r['archive'];raw=raw_records[arc];gs=groups[arc];new=deepcopy(raw['units']);newids={u['id'] for u in new};parent=r['parent_record'];links=[];old=[]
        for key in ('source_tpl','target_tpl','compiled'):require_hash(ROOT/raw[key]['path'],raw[key]['sha256'])
        if parent:
            links=[x for x in m['translation_assets'] if x.get('archive')==arc and not x.get('scope','').startswith('read-only inherited')]
            if len(links)!=1:raise ValueError('038 inherited asset owner ambiguity')
            link=links[0];require_hash(ROOT/link['path'],link['sha256']);a=read(link['path']);old=deepcopy(resolve_units(a));expected={u['id'] for u in parent['layout']};derived={u['id']:u['translation'] for u in r['inherited_translation_derivative']}
            if {u['id'] for u in old}!=expected or any(derived.get(u['id'])!=u['translation'] for u in old):raise ValueError('038 parent authored asset differs from current037 carry bytes')
        units=old+new;ids={u['id'] for u in units};oldids={u['id'] for u in old}
        if len(ids)!=len(units) or newids&seen or oldids&newids or newids!={k for g in gs for k in g['ids']}:raise ValueError('038 new/inherited ID ownership')
        original=(ROOT/raw['source_tpl']['path']).read_text(encoding='utf-8-sig');source_literals={u.key:u.text for u in literals(original)}
        if any(u['state']!='needs_review' or u['source']!=source_literals[u['id']] for u in units):raise ValueError('038 source/inherited protected unit')
        target=replace_exact(original,{u['id']:u['translation'] for u in units});newtarget=replace_exact(original,{u['id']:u['translation'] for u in new})
        if skeleton(original)!=skeleton(target):raise ValueError('038 protected source/complete target controls')
        for g in gs:
            if check[g['profile']](original,newtarget,[g['script']],set(g['geometry_ids']),99)!=g['geometry']:raise ValueError('038 new-script geometry replay')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));lookup=r['source_lookup_candidates']
        if len(lookup)!=1:raise ValueError('038 exact source context')
        p=lookup[0];count=r['script_count'];scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_ids=sorted(ids),literal_scripts=sorted({int(k.split(':')[1]) for k in ids}),script_count=count,max_literal_rows=3,max_line_advance=180,preserve_literal_numerals=True,storage='typed-scene-native-identity-ROM-clone',scene=p['scene'],native_root=abi[p['source_class']]['root'],guarded_reader_return_lr=abi[p['source_class']]['caller_lr'],original_compressed_source_retained=True)
        layout=validate_characters(target,out/'plugins/exe45-utf8.tbl',scope,ids)
        ap=out/(arc+'_asset.json');asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=arc,source_sha256=sha(source),source_tpl=raw['source_tpl'],source_archive_sha256=raw['source_payload_sha256'],consumer='normal-dialogue',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units,new_ids=sorted(newids),inherited_ids=sorted(oldids),parent_asset_lineage=links,selected_wording_lineage=dict(selection=ref(ROOT/SOURCE/'selection.json'),canonical_drafts=[d for g in gs for d in g['drafts']],within_page_LF_only=True),insertion_ready=False)
        frozen_write(ap,asset);tp=out/(arc+'_target.tpl');tp.write_text(target,encoding='utf8',newline='\n')
        records.append(dict(archive=arc,source_class=p['source_class'],scene=p['scene'],source_row=gs[0]['source_row'],source_lookup_candidates=lookup,source_tpl=raw['source_tpl'],target_tpl=ref(tp),asset=ref(ap),compiled=r['compiled'],compiled_bytes=r['compiled_bytes'],compiled_sha256=r['compiled']['sha256'],native_bytes=raw['native_bytes'],native_sha256=raw['source_payload_sha256'],scope=scope,layout=layout,new_ids=sorted(newids),new_scripts=r['new_scripts'],inherited_ids=sorted(oldids),parent_record=parent,parent_asset_lineage=links,translated_units=len(ids),parent_unselected_scripts=r['parent_unselected_script_bytes_preserved'],profiles=[dict(script=g['script'],profile=g['profile'],geometry=g['geometry']) for g in gs],product_admitted=False));seen|=newids;inherit|=oldids
    if seen!=set(s['selected_ids']) or len(seen)!=500 or len(inherit)!=496 or len(records)!=66:raise ValueError('038 full input population')
    population=source_population(source,selected_from(records));deps=[SOURCE+'/selection.json',SOURCE+'/verification_v1.json',SOURCE+'/preflight_v1.json',CARRY,CPU,'analysis/pending_insertion_500_038_native_tails_v1/cpu.json','tools/prepare_native_inputs038_v1.py','tools/field_native_rom_selector_038_v1.py','tools/normal_store_tail038_v1.py','tools/normal_navi_tail038_v1.py','tools/build_development_patch.py','tools/textpet_korean.py','tools/archive_scripts.py']+['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS]
    frozen_write(out/'manifest.json',dict(passed=True,schema=1,status='EXACT500_PLUS496_PINNED_INHERITED_TYPED_SOURCE_INPUTS_NOT_ROM',source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,new_units=500,inherited_units=496,archives=records,plugin=plugin,source_population_count=len(population),selector_CPU_vectors=cpu['vectors'],native_tail_CPU_vectors=tail['vectors'],dependencies={p:sha((ROOT/p).read_bytes()) for p in set(deps)},product_admitted=False,rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['Registered source/authored-asset targets, not product integration or exact038 GBA execution.','Inherited496 retain their original selected asset identities; new996-unit payload population adds only500 unique IDs.','Primary builder must recompile full targets and verify carry bytes against regenerated037 parent, full write ownership and CPU fixture whole-image hash.']))
    print('PASS038 source registry500 new +496 inherited /66 complete authored targets; NO ROM')

if __name__=='__main__':main()
