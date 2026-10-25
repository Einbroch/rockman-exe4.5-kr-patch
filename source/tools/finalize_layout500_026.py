"""Bind026 actual500/repro/static and bounded runtime; no packaging.

Visual observations below were authored after viewing the three exact-ROM
contact sheets, not inferred from the existence of screenshots or a checker.
"""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref

def main():
    folder=ROOT/'analysis/pending500_026_v1';rp=ROOT/'poc/output/pending500_026_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/'poc/output/pending500_026_v1_repro.gba',sha(rom));visual=read(folder/'visual_inputs.json')
    if visual['rom_sha256']!=sha(rom) or {s['kind']:s['screens'] for s in visual['sheets']}!={'startup':22,'mail':23,'raw':30}:raise ValueError('026 visual population')
    for sheet in visual['sheets']:require_hash(ROOT/sheet['path'],sheet['sha256'])
    frozen_write(folder/'visual_review.json',dict(schema=1,passed=True,scope='AGENT_OBSERVED_BOUNDED_NEW_CHOICES_AND_REGRESSION_NOT_GLOBAL_APPROVAL',rom_sha256=sha(rom),sheets=visual['sheets'],agent_observations=[
        'Viewed all22 startup,23 first-mail and30 raw diagnostic panels at native240x160 per panel.',
        'SearchMan mission prompt and two centered Korean rows 시작한다/그만둔다 are readable. Cursor moves between both rows, B leaves the disabled-cancel menu open, and return panels show original PET dialogue without the old choice labels.',
        'PET sibling question shows Korean prompt and 있어/없어 labels. Both cursor positions are readable; cancel shows retained 그렇습니까... page and subsequent original PET dialogue. No translated choice ink was visibly covered by the cursor.',
        'First-mail23 panels have readable Korean text and expected page progression; this is not a full-game language/style approval.',
        'Known inherited startup purchase/welcome bitmap has tight/overlapping lines. Native Japanese kana keyboard, nickname/suffix and field-date weekday remain visible; these are unresolved, not approved or newly fixed.'
    ],human_presentation_approved=False,semantic_human_approved=False,release_eligible=False,open_conditions=['Inherited welcome bitmap leading/overlap.','Kana keyboard and native Japanese nickname/suffix; automatic Hangul compose/commit/save/redisplay unfinished.','Field-date weekday and title logo remain Japanese.','Whole500 meaning/voice/natural caller/event/battle effects and maximum dynamic provider review remain incomplete.']))
    names=['integration.json','a3_cpu.json','b0_cpu.json','integrity.json','native_control_identity.json','normal_runtime.json','raw_samples.json','visual_review.json'];reports=[]
    for name in names:
        report=read(folder/name)
        if not report['passed'] or report['rom_sha256']!=sha(rom):raise ValueError('026 report identity '+name)
        reports.append(ref(folder/name))
    proof=read(folder/'integration.json');baseline=read('poc/output/pending500_025_v2.json')
    if not proof['independent_rebuild_byte_identical'] or proof['new_units']!=500 or proof['total_units']!=baseline['translated_units']+500 or len(proof['merged_consumer_archives'])!=28:raise ValueError('026 exact product scope')
    selection=read('analysis/pending_insertion_500_026_selection_v1/selection.json');samples=read(folder/'raw_samples.json');new_seen={k for page in samples['pages'] for k in page['ids']}&set(selection['selected_ids'])
    if len(new_seen)!=8 or len(samples['pages'])!=26 or len(samples['outcomes'])!=2:raise ValueError('026 bounded runtime scope')
    protected=read('analysis/pending500_025_v2/batch_status.json')['protected_artifacts'];protected['poc/output/pending500_025_v2.gba']=baseline['output_sha256']
    for path,h in protected.items():require_hash(ROOT/path,h)
    inputs=['analysis/pending_insertion_500_026_selection_v1/selection.json','analysis/pending_insertion_500_026_compile500_v1/verification.json','analysis/pending_insertion_500_026_carry_v1/preflight.json','analysis/pending_insertion_500_026_input_gate_v1/verification.json','analysis/pending_insertion_500_026_models_test_v1/result.json','analysis/pending_insertion_500_026_gate_tests_v1/result.json','analysis/pending_insertion_500_026_native_controls_v1/cpu.json','analysis/pending_insertion_500_026_layout_v5/survey.json','tools/specs/primary026_version.json']
    frozen_write(folder/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_VERTICAL_PET_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=sha(rom),rom_bytes=len(rom),previous_units=baseline['translated_units'],new_units=500,total_units=m['translated_units'],primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/p) for p in inputs],protected_artifacts=protected,diagnostic_new_literal_ids=sorted(new_seen),diagnostic_page_observations=26,new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,
        diagnostic_note='New8 literal samples use quarantined PET root/table read aliases, native initializer/width pass/glyph/choice handlers. Both two-node direction graphs, vertical B-disable/A-confirm, PET B-cancel->retained script2 and normal PET return execute. No diagnostic alias enters product ROM; not natural mission/battle/caller/flag effect coverage. Nickname start offset is observed/bounded, not independently recomputed or worst-case provider proof.',
        open_conditions=read(folder/'visual_review.json')['open_conditions']+['No full playthrough, save integration, hardware or audio completion claim.'],
        next_action='Continue against actual026 IDs and effective owner/cumulative026.scope. These500 are already applied; do not reselect/reapply. Reconstruct old carry024->025->026 before next merge. Continue500-unit cohorts and keyboard persistence/known UI defects. Preserve prior ROMs/evidence/saves; no BPS/xdelta/ZIP until requested.'))
    print('PASS026 checkpoint: +500 total',m['translated_units'],'ROM/repro/static/normal/choice samples bound; no package')

if __name__=='__main__':main()
