"""032 exact500 development closure; no distribution/full-game approval."""
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref


def main():
    out=ROOT/'analysis/pending500_032_v1';rp=ROOT/'poc/output/pending500_032_v1.gba';m=read(rp.with_suffix('.json'));h=m['output_sha256'];require_hash(rp,h);require_hash(ROOT/'poc/output/pending500_032_v1_repro.gba',h);old=read('poc/output/pending500_031_v1.json');p=read(out/'integration.json')
    if not p['passed'] or not p['independent_rebuild_byte_identical'] or p['new_units']!=500 or p['total_units']!=old['translated_units']+500 or p['new_raw_archives'] or len(p['merged_consumer_archives'])!=20:raise ValueError('032 source/repro/cohort delta')
    reports=[];names=('integration.json','chip_cpu.json','array_cpu.json','profile_cpu.json','opponent_chip_cpu.json','event_cpu.json','event_time_format_cpu.json','frequency_cpu.json','date_cpu.json','current_date_cpu.json','a3_cpu.json','b0_cpu.json','integrity.json','native_control_identity.json','normal_runtime.json','anniversary_runtime.json','calendar_menu_runtime.json','visual_review.json')
    for name in names:
        r=read(out/name)
        if not r['passed'] or r.get('rom_sha256',r.get('baseline_sha256'))!=h:raise ValueError('032 report identity '+name)
        if r.get('checker'):require_hash(ROOT/r['checker']['path'],r['checker']['sha256'])
        reports.append(ref(out/name))
    counts={'chip_cpu.json':3932,'array_cpu.json':34276,'profile_cpu.json':304,'opponent_chip_cpu.json':1580,'event_cpu.json':3024,'event_time_format_cpu.json':584,'frequency_cpu.json':50,'date_cpu.json':1500,'current_date_cpu.json':430}
    for name,count in counts.items():
        r=read(out/name)
        if r.get('case_count',r.get('cases'))!=count:raise ValueError('032 CPU denominator '+name)
    selection=read('analysis/pending_insertion_500_032_calendar_selection_v3/selection.json');sample=read(out/'calendar_menu_runtime.json');observed=set(sample['new_Korean_literal_ids'])
    if len(observed)!=16 or not observed<=set(selection['selected_ids']):raise ValueError('032 bounded16 new literal sample')
    visual=read(out/'visual_inputs.json')
    if visual['rom_sha256']!=h or {s['kind']:s['screens'] for s in visual['sheets']}!={'startup':22,'mail':23,'menus':12,'anniversary':7}:raise ValueError('032 visual denominator')
    for sheet in visual['sheets']:require_hash(ROOT/sheet['path'],sheet['sha256'])
    protected=dict(read('analysis/pending500_031_v1/batch_status.json')['protected_artifacts']);protected['poc/output/pending500_031_v1.gba']=old['output_sha256']
    for path,wanted in protected.items():require_hash(ROOT/path,wanted)
    inputs=['analysis/pending_insertion_500_032_calendar_selection_v3/selection.json','analysis/pending_insertion_500_032_compile500_v2/verification.json','analysis/pending_insertion_500_032_carry_v2/preflight.json','analysis/pending_insertion_500_032_input_gate_v1/verification.json','analysis/pending_insertion_500_032_gate_tests_v1/result.json','analysis/pending_insertion_500_032_append_guard_v1/result.json','analysis/pending_insertion_500_032_menu_models_v1/result.json','analysis/pending_insertion_500_032_date_models_v1/result.json','tools/specs/primary032_version.json']
    frozen_write(out/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_CALENDAR_APPLIED_REBUILT_NATIVE_MENU_ANNIVERSARY_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=h,rom_bytes=m['output_bytes'],previous_units=old['translated_units'],new_units=500,total_units=m['translated_units'],new_whole_scripts=len(selection['groups']),primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/path) for path in inputs],protected_artifacts=protected,normal_new_literal_ids=sorted(observed),new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,open_conditions=read(out/'visual_review.json')['open_conditions'],next_action='Continue from actual032 IDs and cumulative032.scope, do not reapply these500. Source carry024..032 with frozen031 append routes guarded disjoint from032changes. Remaining Japanese UI/images, all writers/imported/default states and Hangulcompose->commit->save->freshredisplay unresolved. No packages until asked.'))
    print('032 +500 total',m['translated_units'],'repro/static/native menus/anniversary/bounded visual PASS; no package')


if __name__=='__main__':main()
