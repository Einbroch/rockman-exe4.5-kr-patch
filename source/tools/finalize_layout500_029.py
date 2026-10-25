"""029 development cohort closure, not release or distribution approval."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref

def main():
    out=ROOT/'analysis/pending500_029_v1';rp=ROOT/'poc/output/pending500_029_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);h=m['output_sha256']
    require_hash(ROOT/'poc/output/pending500_029_v1_repro.gba',h)
    old=read('poc/output/pending500_028_v1.json');p=read(out/'integration.json')
    if not p['passed'] or not p['independent_rebuild_byte_identical'] or p['new_units']!=500 or p['total_units']!=old['translated_units']+500 or p['new_raw_archives'] or len(p['merged_consumer_archives'])!=16:raise ValueError('029 complete cohort/repro delta')
    reports=[]
    for name in ('integration.json','a3_cpu.json','b0_cpu.json','array_cpu.json','integrity.json','native_control_identity.json','normal_runtime.json','profile_runtime.json','visual_review.json'):
        r=read(out/name)
        if not r['passed'] or r.get('rom_sha256',r.get('baseline_sha256'))!=h:raise ValueError('029 report identity '+name)
        if r.get('checker'):require_hash(ROOT/r['checker']['path'],r['checker']['sha256'])
        reports.append(ref(out/name))
    cpu=read(out/'array_cpu.json')
    if cpu['case_count']!=34276 or cpu['native_helpers_substituted']:raise ValueError('029 actual native CPU scope')
    sample=read(out/'profile_runtime.json');selection=read('analysis/pending_insertion_500_029_selection_v1/selection.json')
    observed={i for page in sample['pages'] for i in page['ids']}
    if len(sample['pages'])!=4 or len(observed)!=4 or not observed<=set(selection['selected_ids']):raise ValueError('029 bounded literal sample')
    visuals=read(out/'visual_inputs.json')
    if visuals['rom_sha256']!=h or {s['kind']:s['screens'] for s in visuals['sheets']}!={'startup':22,'mail':23,'raw':8}:raise ValueError('029 visual population')
    for sheet in visuals['sheets']:require_hash(ROOT/sheet['path'],sheet['sha256'])
    protected=dict(read('analysis/pending500_028_v1/batch_status.json')['protected_artifacts']);protected['poc/output/pending500_028_v1.gba']=old['output_sha256']
    for path,wanted in protected.items():require_hash(ROOT/path,wanted)
    paths=['analysis/pending_insertion_500_029_selection_v1/selection.json','analysis/pending_insertion_500_029_compile500_v1/verification.json','analysis/pending_insertion_500_029_carry_v1/preflight.json','analysis/pending_insertion_500_029_input_gate_v1/verification.json','analysis/pending_insertion_500_029_models_test_v1/result.json','analysis/pending_insertion_500_029_gate_tests_v1/result.json','analysis/pending_insertion_500_029_append_tests_v1/result.json','analysis/pending_insertion_500_029_initializer_runtime_v1/verification.json','tools/specs/primary029_version.json']
    frozen_write(out/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_NATIVE_ARRAY_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=h,rom_bytes=m['output_bytes'],previous_units=old['translated_units'],new_units=500,total_units=m['translated_units'],new_whole_scripts=len(selection['groups']),primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/path) for path in paths],protected_artifacts=protected,diagnostic_new_literal_ids=sorted(observed),diagnostic_page_observations=4,new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,diagnostic_note='Actual source startup initializer prepares all eight native caches from temporarily seeded valid legacy records. Records and flags restored after initializer; caches persist to aliased GutsMan5/35 bodies in own Rockman PET host. Four Korean pages, native max6 older-bro/max8 show values, glyph/font/OBJ/pixels, clearing, waits and PET returns sampled. Not natural character/script acquisition, full writer/default/import audit, Hangul persistence or whole500 semantic approval.',open_conditions=read(out/'visual_review.json')['open_conditions'],next_action='Continue from actual029 IDs and effective cumulative029.scope; do not reapply these500. New source carry reconstruction must include024->025->026->027->028->029. Continue500-unit cohorts and unresolved Hangul composition/commit/save/redisplay; no distribution packages until requested.'))
    print('PASS029 +500 total',m['translated_units'],'repro/static/native arrays/bounded runtime, no package')

if __name__=='__main__':main()
