"""Source-bound exact500 NPC clone assets/scopes, no primary ROM writer."""
from collections import defaultdict
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_035 import BASE,BASE_SHA
from prepare_repartition500 import layout_records
from tpl_literals import literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from survey_new_storage_035 import VALIDATORS
from survey_batch500_017_layout import protected_edges
from build_development_patch import validate_characters,validate_literal_numerals
from textpet_korean import prepare_plugins
from korean_codec import EXTRA_CHARACTER_INDICES
from verify_tpi_index import parse_tpi,lz77_decompress
from archive_scripts import verify_untouched_scripts
from compile_layout_candidates_024 import ref
from field_npc_rom_selector_035_v2 import source_population

SELECTION='analysis/pending_insertion_500_035_source500_selection_v1/selection.json'
COMPILE='analysis/pending_insertion_500_035_source_compile500_v1/verification.json'
CPU='analysis/pending_insertion_500_035_npc_selector_cpu_v2/cpu.json'
OUT='analysis/pending_insertion_500_035_npc_inputs_v1'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'))
    reports=[read(p) for p in (SELECTION,COMPILE,CPU)];sel,compiled,cpu=reports
    for report in reports:
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
        if report.get('passed') is False or report['rom_written']:raise ValueError('035 preparation evidence')
    if sel['baseline_sha256']!=BASE_SHA or compiled['baseline_sha256']!=BASE_SHA or cpu['baseline_rom_sha256']!=BASE_SHA or compiled['units']!=500 or cpu['source_population_count']!=28:raise ValueError('035 evidence baseline/exact500')
    selected=set(sel['selected_ids']);applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    if len(selected)!=500 or selected&applied:raise ValueError('035 distinct500')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    grouped=defaultdict(list)
    for g in sel['groups']:grouped[g['archive']].append(g)
    pool=source_population(source,set(grouped));out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False)
    plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));records=[];all_ids=set();validators=dict(VALIDATORS)
    for r in compiled['archives']:
        arc=r['archive'];gs=grouped[arc];row=gs[0]['source_row'];native,used=lz77_decompress(source,row['offset'])
        if row!=catalog[arc] or not row['compressed'] or row['size_header'] or sha(native)!=r['source_sha256']:raise ValueError('035 source native/catalog')
        if any(rom[p:p+4]!=source[p:p+4] for p in row['pointers']) or rom[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used]:raise ValueError('035 original compressed source/reference not preserved')
        for key in ('source_tpl','target_tpl','compiled'):require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig');payload=(ROOT/r['compiled']['path']).read_bytes();units=deepcopy(r['units']);ids={u['id'] for u in units}
        if len(ids)!=len(units) or all_ids&ids or ids!={k for g in gs for k in g['ids']}:raise ValueError('035 archive ID partition')
        if skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals(replace_exact(original,{u['id']:u['translation'] for u in units}))]:raise ValueError('035 target/control/source ownership')
        source_lit={u.key:u.text for u in literals(original)};canonical={}
        for g in gs:
            if g['already_applied_ids_in_script'] or g['locked_parent_units'] or set(g['geometry_ids'])!=set(g['ids']):raise ValueError('035 new untouched script only')
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=next(u for u in a['units'] if u['id']==d['id'])
                if a['source_sha256']!=sha(source) or a['source_tpl']!=r['source_tpl'] or a['source_archive_sha256']!=sha(native):raise ValueError('035 canonical source binding')
                canonical[u['id']]=u
            proof=validators[g['profile']](original,target,[g['script']],set(g['ids']),99)
            if proof!=g['geometry']:raise ValueError('035 geometry differs')
        for u in units:
            c=canonical[u['id']]
            if u['source']!=source_lit[u['id']] or u['source']!=c['source'] or u['state']!='needs_review' or u['state']!=c['state'] or u['translation'].replace('\n',' ')!=c['translation'].replace('\n',' ') or not protected_edges(u['source'],u['translation']):raise ValueError('035 canonical wording/state/protection')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        scripts=sorted({g['script'] for g in gs});kept=verify_untouched_scripts(native,payload,255,set(scripts))
        if len(payload)>65535 or kept!=r['unselected_scripts'] or r['script_count']!=255:raise ValueError('035255/unselected script bytes')
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=scripts,literal_ids=sorted(ids),script_count=255,max_literal_rows=3,max_line_advance=180,preserve_literal_numerals=True,
                   literal_profiles=[dict(scripts=[g['script']],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=180) for g in gs],
                   compressed_source_retained=True,native_root=0x02039800,guarded_reader_caller=0x0804F76F,storage='npc-A0-ROM-clone')
        layout=validate_characters(target,out/'plugins'/'exe45-utf8.tbl',scope,ids)
        asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=arc,source_sha256=sha(source),source_tpl=r['source_tpl'],source_archive_sha256=sha(native),consumer='normal-dialogue',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units,
                   selected_wording_lineage=dict(selection=ref(ROOT/SELECTION),canonical_drafts=[d for g in gs for d in g['drafts']],within_page_LF_only=True),insertion_ready=False)
        asset_path=out/(arc+'_asset.json');frozen_write(asset_path,asset)
        records.append(dict(archive=arc,storage='npc-A0-ROM-clone',source_row=row,source_tpl=r['source_tpl'],source_payload_sha256=sha(native),native_bytes=len(native),native_stored_consumed_bytes=used,source_references_unchanged=True,source_storage_unchanged=True,
                            compiled=r['compiled'],target_tpl=r['target_tpl'],compiled_sha256=sha(payload),compiled_bytes=len(payload),script_count=255,translated_units=len(ids),layout=layout,scope=scope,
                            asset=ref(asset_path),new_ids=sorted(ids),new_scripts=scripts,unselected_scripts=kept,profiles=[dict(profile=g['profile'],script=g['script'],geometry=g['geometry']) for g in gs],product_admitted=False))
        all_ids|=ids;print('035 prepared NPC',arc,len(ids),'PASS',flush=True)
    if all_ids!=selected or len(records)!=9:raise ValueError('035 exact500/9 input population')
    deps=[SELECTION,COMPILE,CPU,'tools/prepare_npc_inputs_035.py','tools/field_npc_rom_selector_035_v2.py','tools/build_development_patch.py','tools/survey_new_storage_035.py','tools/textpet_korean.py','tools/archive_scripts.py','tools/tpl_literals.py']
    deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS if fn.__module__!='__main__']
    frozen_write(out/'manifest.json',dict(schema=1,status='EXACT500_NPC_SOURCE_ASSETS_SCOPE_METRICS_PASS_NOT_ROM_BUILD',passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,new_units=500,archives=records,
        selector_spec='tools/field_npc_rom_selector_035_v2.py',source_population_count=len(pool),requires_original_compressed_sources_and_pointers_unchanged=True,plugin=plugin,
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,
        limits='Exact500 pinned new assets, source controls and independent geometry/metrics. Primary must recompile source-derived TPL, append native identity copies and raw target clones once, compose one reader stub write with prior034 chain, verify all final placements/writes/delta/repro and runtime. No compression replacement or RAM growth permitted.'))
    print('035 exact500 NPC assets/scopes prepared;NO ROM')

if __name__=='__main__':main()
