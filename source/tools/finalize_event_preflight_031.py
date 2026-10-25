"""Reconcile independent031 source-only preparations; actual030 unchanged."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

OUT='analysis/pending_insertion_500_031_event_preflight_v1/status.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);m=read('poc/output/pending500_030_v1.json');require_hash(ROOT/'poc/output/pending500_030_v1.gba',m['output_sha256'])
    prior=read('analysis/pending500_030_v1/batch_status.json')
    for n,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/n,h)
    for p,h in prior['protected_artifacts'].items():require_hash(ROOT/p,h)
    paths=['analysis/pending_insertion_500_031_event_title_bounds_v1/cpu.json','analysis/pending_insertion_500_031_event_layout_v1/survey.json','analysis/pending_insertion_500_031_event_models_v1/result.json','analysis/pending_insertion_500_031_event_selection_v1/selection.json','analysis/pending_insertion_500_031_event_compile205_v1/verification.json','analysis/pending_insertion_500_031_event_time_format_v1/cpu.json','analysis/pending_insertion_500_031_event_native_boundary_v1/verification.json']
    reports={p:read(p) for p in paths}
    for p,r in reports.items():
        if r.get('passed') is False or r.get('rom_written') is True or r.get('release_eligible') is True or r.get('baseline_sha256',m['output_sha256'])!=m['output_sha256']:raise ValueError('031 event scope '+p)
        for q,h in r['dependencies'].items():require_hash(ROOT/q,h)
    compiled=reports[paths[4]];selection=reports[paths[3]];ids={u['id'] for a in compiled['archives'] for u in a['units']}
    if len(ids)!=205 or ids!=set(selection['selected_ids']) or compiled['archive_count']!=40 or compiled['extended_glyphs_checked']!=185 or not compiled['source_and_target_roundtrip'] or not compiled['unselected_script_bytes_preserved']:raise ValueError('031 source compile205 identity')
    for a in compiled['archives']:
        for key in ('compiled','target_tpl'):require_hash(ROOT/a[key]['path'],a[key]['sha256'])
    old_path='analysis/pending_insertion_500_031_preflight_v1/status.json';old=read(old_path)
    if old['new_units_applied'] or old['actual_applied_total']!=16122 or set(old['selected_ids'])&ids:raise ValueError('031 disjoint original130 preparation')
    if reports[paths[5]]['cases']!=584 or not reports[paths[6]]['eighth_accepted'] or not reports[paths[6]]['ninth_rejected']:raise ValueError('031 event new evidence denominator')
    for ref in reports[paths[6]]['receipts']:
        require_hash(ROOT/ref['path'],ref['sha256']);r=read(ref['path']);folder=(ROOT/ref['path']).parent
        for p,h in r['artifacts'].items():require_hash(folder/p,h)
    if (ROOT/'poc/output/pending500_031_v1.gba').exists():raise ValueError('031 unexpected product contradicts source-only report')
    frozen_write(ROOT/OUT,dict(schema=1,status='EVENT205_SOURCE_ONLY_PREPARATION_AND_NATIVE8_BOUNDARY_VERIFIED_NOT_500_OR_ROM',baseline_rom='poc/output/pending500_030_v1.gba',baseline_sha256=m['output_sha256'],source_sha256=cfg['source_profile']['sha256'],actual_applied_total=16122,new_units_applied=0,new_event_source_compile_units=205,event_whole_scripts=107,event_archives=40,event_font_glyphs=185,previous_chip_source_compile_units=130,disjoint_source_compile_units=335,analysis_requested_subset_pool=reports[paths[1]]['max_reachable_requested_subset'],exact500_available=reports[paths[1]]['selected500'] is not None,source_and_target_roundtrip=True,normal_native8_boundary_passed=True,source_and_current_ROMS_preserved=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths+[old_path,'tools/finalize_event_preflight_031.py']},rom_written=False,distribution_package_written=False,release_eligible=False,limits=['335 source-only units are not335new applied translations; actual total16122 unchanged.','428 is a conditional geometry subset pool, not a whole-game remainder or admitted batch.','Event source-only binaries preserve unselected Japanese and omit cumulative carry; do not inject or present as playable ROMs.','Still requires complete selected-name/provider applicability, preserved guard/loop behavior, final500 selection/carry/build/repro/current Korean GBA QA.','Native8 other-title boundary is not native10 anniversary, friend+suffix acquisition, Hangul input or save/reload.']))
    print('031 event205/40archives source-only closed; combined335 source-compiled; actual16122 +0; conditional pool428; no ROM/package',flush=True)


if __name__=='__main__':main()
