"""Register exact500 source-bound037 inputs; no ROM/admission claim."""
from collections import defaultdict
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_037_v2 import baseline,OUT as SOURCE,ref
from prepare_repartition500 import layout_records
from field_native_rom_selector_037_v2 import source_population,contracts
from survey_new_storage_035 import VALIDATORS
from survey_aggregate_pet_033 import replace_exact
from tpl_literals import literals,skeleton
from archive_scripts import verify_untouched_scripts
from build_development_patch import validate_characters,validate_literal_numerals
from textpet_korean import prepare_plugins
from korean_codec import EXTRA_CHARACTER_INDICES

OUT='analysis/pending_insertion_500_037_native_inputs_v2'
CPU='analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json'


def selected_from(records):
    return {r['archive']:dict(source_class=r['source_class'],scene=r['scene'],target_sha256=r['compiled_sha256'],script_count=r['scope']['script_count']) for r in records}


def main():
    cfg,source,rom,m=baseline(); s=read(SOURCE+'/selection.json'); v=read(SOURCE+'/verification_v1.json'); pre=read(SOURCE+'/preflight_v2.json'); cpu=read(CPU)
    for report in (v,pre,cpu):
        if not report['passed'] or report['rom_written'] or report['baseline_sha256']!=sha(rom): raise ValueError('037 prerequisite scope')
    for p,h in s['dependencies'].items(): require_hash(ROOT/p,h)
    for p,h in pre['dependencies'].items(): require_hash(ROOT/p,h)
    for r in [v['selection'],cpu['source_compile'],cpu['preflight'],cpu['board_caller']]+cpu['tools']: require_hash(ROOT/r['path'],r['sha256'])
    fields={r['archive']:r for r in pre['archives_detail']}; compiled={r['archive']:r for r in v['archives']}
    population=source_population(source,{a:dict(source_class=r['source_class'],scene=r['source_reference']['scene'],target_sha256=compiled[a]['compiled']['sha256'],script_count=r['script_count']) for a,r in fields.items()})
    abi=contracts(source); oldids={u['id'] for r in layout_records(m) for u in r['layout']}; oldarcs={r['archive'] for r in layout_records(m)}; selected=set(s['selected_ids'])
    if len(selected)!=500 or selected&oldids: raise ValueError('037 distinct500 prerequisite')
    grouped=defaultdict(list)
    for g in s['groups']: grouped[g['archive']].append(g)
    out=ROOT/OUT; out.mkdir(parents=True,exist_ok=False); plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES)); records=[]; seen=set(); validators=dict(VALIDATORS)
    for ar in v['archives']:
        arc=ar['archive']; gs=grouped[arc]; field=fields[arc]; kind=field['source_class']; count=ar['script_count']; native=next(r['payload'] for r in population if r['archive']==arc)
        for key in ('source_tpl','target_tpl','compiled'): require_hash(ROOT/ar[key]['path'],ar[key]['sha256'])
        original=(ROOT/ar['source_tpl']['path']).read_text(encoding='utf-8-sig'); target=(ROOT/ar['target_tpl']['path']).read_text(encoding='utf-8-sig'); units=deepcopy(ar['units']); ids={u['id'] for u in units}; payload=(ROOT/ar['compiled']['path']).read_bytes()
        if arc in oldarcs or ids&seen or len(ids)!=len(units) or ids!={k for g in gs for k in g['ids']}: raise ValueError('037 archive/new ID ownership')
        if skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals(replace_exact(original,{u['id']:u['translation'] for u in units}))]: raise ValueError('037 target/protected controls')
        raw={u.key:u.text for u in literals(original)}
        if any(u['state']!='needs_review' or raw[u['id']]!=u['source'] for u in units): raise ValueError('037 source literal/state')
        for g in gs:
            if validators[g['profile']](original,target,[g['script']],set(g['geometry_ids']),99)!=g['geometry']: raise ValueError('037 geometry scope')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True)); scripts=sorted({g['script'] for g in gs}); kept=verify_untouched_scripts(native,payload,count,set(scripts))
        if kept!=ar['unselected_scripts'] or len(payload)>65535 or len(native)>=0x1000: raise ValueError('037 script/storage capacity')
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_ids=sorted(ids),literal_scripts=scripts,script_count=count,max_literal_rows=3,max_line_advance=180,preserve_literal_numerals=True,literal_profiles=[dict(scripts=[g['script']],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=180) for g in gs],storage='typed-scene-native-identity-ROM-clone',scene=field['source_reference']['scene'],native_root=abi[kind]['root'],guarded_reader_return_lr=abi[kind]['caller_lr'],original_compressed_source_retained=True)
        layout=validate_characters(target,out/'plugins/exe45-utf8.tbl',scope,ids)
        asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=arc,source_sha256=sha(source),source_tpl=ar['source_tpl'],source_archive_sha256=sha(native),consumer='normal-dialogue',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units,selected_wording_lineage=dict(selection=ref(ROOT/SOURCE/'selection.json'),canonical_drafts=[d for g in gs for d in g['drafts']],within_page_LF_only=True),insertion_ready=False)
        ap=out/(arc+'_asset.json'); frozen_write(ap,asset)
        records.append(dict(archive=arc,source_class=kind,scene=scope['scene'],source_row=gs[0]['source_row'],source_tpl=ar['source_tpl'],target_tpl=ar['target_tpl'],compiled=ar['compiled'],compiled_bytes=len(payload),compiled_sha256=sha(payload),native_bytes=len(native),native_sha256=sha(native),asset=ref(ap),scope=scope,layout=layout,new_ids=sorted(ids),new_scripts=scripts,translated_units=len(ids),unselected_scripts=kept,profiles=[dict(script=g['script'],profile=g['profile'],geometry=g['geometry']) for g in gs],product_admitted=False)); seen|=ids
    if seen!=selected or len(records)!=70: raise ValueError('037 final input population')
    source_population(source,selected_from(records))
    deps=[SOURCE+'/selection.json',SOURCE+'/verification_v1.json',SOURCE+'/preflight_v2.json',SOURCE+'/board_caller_cpu_v1.json',CPU,'tools/prepare_native_inputs037_v2.py','tools/field_native_rom_selector_037_v2.py','tools/build_development_patch.py','tools/textpet_korean.py','tools/archive_scripts.py']
    deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS]
    frozen_write(out/'manifest.json',dict(schema=1,status='EXACT500_REGISTERED_TYPED_SOURCE_INPUTS_CPU_PASS_NOT_ROM',passed=True,source_sha256=sha(source),baseline_rom=s['baseline_rom'],baseline_sha256=sha(rom),new_units=500,archives=records,plugin=plugin,source_population_count=len(population),cpu_vectors=cpu['vectors'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},product_admitted=False,rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['Input registry is not product integration or natural runtime evidence.','NPC363 and board137 retain original source LZ/RAM. Exact equal source aliases require all owners selected and complete target bytes equal.','037 primary build, final write ownership, independent rebuild and exact-ROM consumption/rendering remain required.']))
    print('PASS037 registered500 inputs/70 assets; NOT ROM')


if __name__=='__main__': main()
