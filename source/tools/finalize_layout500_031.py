"""031 development cohort closure, not distribution or complete-game approval."""
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref


def main():
    out=ROOT/'analysis/pending500_031_v1';rp=ROOT/'poc/output/pending500_031_v1.gba';m=read(rp.with_suffix('.json'));h=m['output_sha256'];require_hash(rp,h)
    require_hash(ROOT/'poc/output/pending500_031_v1_repro.gba',h);old=read('poc/output/pending500_030_v1.json');p=read(out/'integration.json')
    if not p['passed'] or not p['independent_rebuild_byte_identical'] or p['new_units']!=500 or p['total_units']!=old['translated_units']+500 or p['new_raw_archives'] or len(p['merged_consumer_archives'])!=77:raise ValueError('031 source/repro/cohort delta')
    reports=[]
    names=('integration.json','chip_cpu.json','array_cpu.json','profile_cpu.json','opponent_cpu.json','event_cpu.json','time_cpu.json','frequency_cpu.json','a3_cpu.json','b0_cpu.json','integrity.json','native_control_identity.json','normal_runtime.json','opponent_runtime.json','calendar_runtime.json','visual_review.json')
    for name in names:
        r=read(out/name)
        if not r['passed'] or r.get('rom_sha256',r.get('baseline_sha256'))!=h:raise ValueError('031 report identity '+name)
        if r.get('checker'):require_hash(ROOT/r['checker']['path'],r['checker']['sha256'])
        reports.append(ref(out/name))
    counts={'chip_cpu.json':3932,'array_cpu.json':34276,'profile_cpu.json':304,'opponent_cpu.json':1580,'event_cpu.json':3024,'time_cpu.json':584,'frequency_cpu.json':50}
    for name,count in counts.items():
        if read(out/name)['case_count']!=count:raise ValueError('031 CPU denominator '+name)
    selected=read('analysis/pending_insertion_500_031_selected500_v1/selection.json');sample=read(out/'opponent_runtime.json');cal=read(out/'calendar_runtime.json')
    observed={i for page in sample['pages'] for i in page['ids']}|set(cal['new_Korean_literal_ids'])
    if len(sample['pages'])!=4 or len(observed)!=9 or not observed<=set(selected['selected_ids']):raise ValueError('031 bounded new literal samples')
    visual=read(out/'visual_inputs.json')
    if visual['rom_sha256']!=h or {s['kind']:s['screens'] for s in visual['sheets']}!={'startup':22,'mail':23,'opponent':6,'calendar':7}:raise ValueError('031 visual denominator')
    for sheet in visual['sheets']:require_hash(ROOT/sheet['path'],sheet['sha256'])
    protected=dict(read('analysis/pending500_030_v1/batch_status.json')['protected_artifacts']);protected['poc/output/pending500_030_v1.gba']=old['output_sha256']
    for path,wanted in protected.items():require_hash(ROOT/path,wanted)
    inputs=['analysis/pending_insertion_500_031_selected500_v1/selection.json','analysis/pending_insertion_500_031_compile500_v2/verification.json','analysis/pending_insertion_500_031_carry_v1/preflight.json','analysis/pending_insertion_500_031_input_gate_v1/verification.json','analysis/pending_insertion_500_031_gate_tests_v1/result.json','analysis/pending_insertion_500_031_append_tests_v1/result.json','analysis/pending_insertion_500_031_calendar_models_v1/result.json','tools/specs/primary031_version.json']
    frozen_write(out/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_NATIVE_CALENDAR_AND_OPPONENT_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=h,rom_bytes=m['output_bytes'],previous_units=old['translated_units'],new_units=500,total_units=m['translated_units'],new_whole_scripts=len(selected['groups']),primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/path) for path in inputs],protected_artifacts=protected,diagnostic_new_literal_ids=sorted(observed),new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,diagnostic_note='Own031 boot/startup/mail and natural meal calendar registration, five native providers, translated deletion prompt and Yes/No/B/reentry. Separate quarantined GutsMan62/71 aliases on own Rockman host temporarily seed and restore native max8 chip9 fields. Not all500 meaning, natural opponent acquisition, all titles/writers, save/reset/fresh reload or Hangul composition/persistence.',open_conditions=read(out/'visual_review.json')['open_conditions'],next_action='Continue from actual031 selected500 and cumulative031.scope; do not reapply. All77 old RAW consumers merged before allocation including prior027/028/030 appended routes. Current translation_assets scope label retains030 wording for031 merged owner but hash/path and cumulative031 identity verified. Fix label in a future source-bound primary version, not this frozen artifact. No distribution packages until asked.'))
    print('PASS031 +500 total',m['translated_units'],'repro/static/native calendar/opponent/bounded runtime; no package')


if __name__=='__main__':main()
