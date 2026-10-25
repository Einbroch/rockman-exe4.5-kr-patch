"""Close152 source-only date candidates without misreporting500 ROM insertion."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from compile_layout_candidates_024 import ref


def main():
    base='poc/output/pending500_031_v1.gba';m=read(base.replace('.gba','.json'));require_hash(ROOT/base,m['output_sha256']);require_hash(ROOT/'poc/output/pending500_031_v1_repro.gba',m['output_sha256']);cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    out=ROOT/'analysis/pending_insertion_500_032_preflight_v1';selection=read('analysis/pending_insertion_500_032_date_selection_v1/selection.json');compiled=read('analysis/pending_insertion_500_032_date_compile_v1/verification.json');native=read('analysis/pending_insertion_500_032_anniversary_runtime_v1/verification.json');cpu=read('analysis/pending_insertion_500_032_date_cpu_v1/cpu.json');tests=read('analysis/pending_insertion_500_032_date_models_v1/result.json');census=read('analysis/pending_insertion_500_032_calendar_inventory_v1/census.json')
    for report in (selection,compiled,native,cpu,census):
        if report['baseline_sha256']!=m['output_sha256'] or report['rom_written']:raise ValueError('032 exact source-only baseline')
        for p,h in report.get('dependencies',{}).items():require_hash(ROOT/p,h)
    if not all(r['passed'] for r in (compiled,native,cpu,tests)) or cpu['case_count']!=1500 or tests['positive_cases']!=2 or tests['negative_cases']!=17:raise ValueError('032 CPU/model denominator')
    if compiled['units']!=selection['planned_new_units'] or not compiled['source_and_target_roundtrip'] or not compiled['unselected_script_bytes_preserved'] or compiled['product_integrated']:raise ValueError('032 source-only compile binding')
    ids=set(selection['selected_ids']);applied={u['id'] for r in layout_records(m) for u in r['layout']}
    if ids&applied or len(ids)!=sum(len(r['units']) for r in compiled['archives']) or {u['id'] for r in compiled['archives'] for u in r['units']}!=ids:raise ValueError('032 new disjoint source candidate identity')
    for r in compiled['archives']:
        for field in ('compiled','target_tpl'):require_hash(ROOT/r[field]['path'],r[field]['sha256'])
        if not all(r[k] for k in ('native_roundtrip','semantic_roundtrip','binary_roundtrip')):raise ValueError('032 compiled archive roundtrip')
    for receipt in native['receipts']:
        require_hash(ROOT/receipt['path'],receipt['sha256']);r=read(receipt['path']);folder=(ROOT/receipt['path']).parent
        for filename,h in r['artifacts'].items():require_hash(folder/filename,h)
    for p,h in native['screenshots'].items():require_hash(ROOT/p,h)
    visual=dict(schema=1,passed=True,baseline_sha256=m['output_sha256'],screenshots_directly_viewed=True,screenshots=native['screenshots'],screen_count=len(native['screenshots']),observations=['Directly viewed native anniversary editor10th accepted/11th rejected, normal registration and sourceJapanese51 preview/confirmation/No/Yes screens.','10nativeE406 glyphs fit the quoted title row; date/year/month/day/weekday and title all resident. Prior title line clears on confirmation; No preserves and Yes removes record.','Japanese source prompts and kana keyboard remain. These are not new Korean032screens or Hangul automatic input/save evidence.'],release_eligible=False)
    frozen_write(out/'visual_review.json',visual)
    previous=read('analysis/pending500_031_v1/batch_status.json')
    for p,h in previous['protected_artifacts'].items():require_hash(ROOT/p,h)
    for name,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/name,h)
    if (ROOT/'poc/output/pending500_032_v1.gba').exists():raise ValueError('032 preflight cannot replace actual ROM authority')
    paths=['analysis/pending_insertion_500_032_calendar_inventory_v1/census.json','analysis/pending_insertion_500_032_date_cpu_v1/cpu.json','analysis/pending_insertion_500_032_anniversary_runtime_v1/verification.json','analysis/pending_insertion_500_032_date_models_v1/result.json','analysis/pending_insertion_500_032_date_selection_v1/selection.json','analysis/pending_insertion_500_032_date_compile_v1/verification.json',str((out/'visual_review.json').relative_to(ROOT))]
    frozen_write(out/'status.json',dict(schema=1,status='SOURCE_ONLY152_DATE_CANDIDATES_NATIVE_ANNIVERSARY10_VERIFIED_NOT500_OR_ROM_APPLIED',baseline_rom=base,baseline_sha256=m['output_sha256'],actual_applied_total=m['translated_units'],new_units_applied=0,source_compiled_candidates=len(ids),source_compiled_archives=compiled['archive_count'],source_compiled_whole_scripts=len(selection['groups']),requested_next_cohort=500,additional_safe_units_needed=500-len(ids),selected_ids=sorted(ids),reports=[ref(ROOT/p) for p in paths],source_and_previous_artifacts_preserved=True,new_distribution_packages_created=False,rom_written=False,release_eligible=False,complete_integrated_request=False,limits=['513inventory is calendar21root originalJapanese literal remainder only, not safe candidates or full-game count.','152source-compiled candidates retain other Japanese source and do not carry031translations. Never inject these whole binaries directly as cumulative ROM replacements.','Native actual031calendar51 maximal native anniversary title and Yes/No only;52 conditionaldate geometry, allotherwriters/imports/save/reset/reload and fullHangul remain open.'],next_action='Collect another348safe units under explicit calendar menu/choice/current-date consumers or independent supported profiles; selectexact500. Preserve canonical words/controls; then cumulative031.scope merge and immutable-source032primary/repro/finalKorean runtime. No packages until asked.'))
    print('032 preflight PASS',len(ids),'source candidates;',m['translated_units'],'actually applied, +0; no032ROM/package')


if __name__=='__main__':main()
