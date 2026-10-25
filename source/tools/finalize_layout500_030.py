"""030 development cohort closure; no release/distribution approval."""
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref

def main():
    out=ROOT/'analysis/pending500_030_v1';rp=ROOT/'poc/output/pending500_030_v1.gba';m=read(rp.with_suffix('.json'));h=m['output_sha256'];require_hash(rp,h)
    require_hash(ROOT/'poc/output/pending500_030_v1_repro.gba',h);old=read('poc/output/pending500_029_v1.json');p=read(out/'integration.json')
    if not p['passed'] or not p['independent_rebuild_byte_identical'] or p['new_units']!=500 or p['total_units']!=old['translated_units']+500 or p['new_raw_archives']!=['6D44D4'] or len(p['merged_consumer_archives'])!=19:raise ValueError('030 cohort/source/repro delta')
    reports=[]
    for name in ('integration.json','chip_cpu.json','array_cpu.json','profile_cpu.json','a3_cpu.json','b0_cpu.json','integrity.json','native_control_identity.json','normal_runtime.json','profile_runtime.json','visual_review.json'):
        r=read(out/name)
        if not r['passed'] or r.get('rom_sha256',r.get('baseline_sha256'))!=h:raise ValueError('030 report identity '+name)
        if r.get('checker'):require_hash(ROOT/r['checker']['path'],r['checker']['sha256'])
        reports.append(ref(out/name))
    for name,count in (('chip_cpu.json',3932),('array_cpu.json',34276),('profile_cpu.json',304)):
        r=read(out/name)
        if r['case_count']!=count or r['native_helpers_substituted']:raise ValueError('030 native CPU scope')
    sample=read(out/'profile_runtime.json');selection=read('analysis/pending_insertion_500_030_selection_v1/selection.json');observed={i for page in sample['pages'] for i in page['ids']}
    if len(sample['pages'])!=4 or len(observed)!=4 or not observed<=set(selection['selected_ids']):raise ValueError('030 bounded four-new-literal sample')
    visual=read(out/'visual_inputs.json')
    if visual['rom_sha256']!=h or {s['kind']:s['screens'] for s in visual['sheets']}!={'startup':22,'mail':23,'raw':6}:raise ValueError('030 visual denominator')
    for sheet in visual['sheets']:require_hash(ROOT/sheet['path'],sheet['sha256'])
    protected=dict(read('analysis/pending500_029_v1/batch_status.json')['protected_artifacts']);protected['poc/output/pending500_029_v1.gba']=old['output_sha256']
    for path,wanted in protected.items():require_hash(ROOT/path,wanted)
    inputs=['analysis/pending_insertion_500_030_selection_v1/selection.json','analysis/pending_insertion_500_030_compile500_v1/verification.json','analysis/pending_insertion_500_030_carry_v1/preflight.json','analysis/pending_insertion_500_030_input_gate_v1/verification.json','analysis/pending_insertion_500_030_models_test_v1/result.json','analysis/pending_insertion_500_030_gate_tests_v1/result.json','analysis/pending_insertion_500_030_append_tests_v1/result.json','analysis/pending_insertion_500_030_chip_pools_v1/census.json','analysis/pending_insertion_500_030_chip_runtime_v1/verification.json','tools/specs/primary030_version.json']
    frozen_write(out/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_NATIVE_CHIP_STATS_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=h,rom_bytes=m['output_bytes'],previous_units=old['translated_units'],new_units=500,total_units=m['translated_units'],new_whole_scripts=len(selection['groups']),primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/path) for path in inputs],protected_artifacts=protected,diagnostic_new_literal_ids=sorted(observed),diagnostic_page_observations=4,new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,diagnostic_note='Own Rockman PET host with quarantined GutsMan75/89 read aliases. Actual source native chip9(Standard)/302(Giga) max8 names temporarily seeded in valid record fields and restored after real F90C reader. Four new Korean pages, native chip RAM/font/OBJ/pixels, row widths, clearing, waits and PET returns sampled. Native lookup/stats writer CPU separately covers393 names. Shared chip-name values stay Japanese; not natural battle acquisition, all500 meanings, full Korean chip serialization or Hangul persistence.',open_conditions=read(out/'visual_review.json')['open_conditions'],next_action='Continue from actual030 IDs and effective cumulative030.scope; do not reapply these500. Source carry024->025->026->027->028->029->030, including appended027/028 and030 newRAW before allocation. Continue500 cohorts and unresolved Hangul composition/commit/save/redisplay; no distribution packages until requested.'))
    print('PASS030 +500 total',m['translated_units'],'repro/static/native chip stats/bounded runtime; no package')

if __name__=='__main__':main()
