"""Bind025 applied500/static/repro and bounded runtime evidence; no packaging."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref

def main():
    folder=ROOT/'analysis/pending500_025_v2';rp=ROOT/'poc/output/pending500_025_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/'poc/output/pending500_025_v2_repro.gba',sha(rom))
    names=['integration.json','a3_cpu.json','b0_cpu.json','integrity.json','normal_runtime.json','raw_samples_v3.json','visual_review.json'];reports=[]
    for name in names:
        report=read(folder/name)
        if not report['passed'] or report['rom_sha256']!=sha(rom):raise ValueError('025 current report binding '+name)
        reports.append(ref(folder/name))
    proof=read(folder/'integration.json')
    if not proof['independent_rebuild_byte_identical'] or proof['new_units']!=500 or proof['total_units']!=13622 or len(proof['merged_consumer_archives'])!=33:raise ValueError('025 applied500 final scope')
    protected=read('analysis/pending500_024_v1/batch_status.json')['protected_artifacts']
    protected['poc/output/pending500_024_v1.gba']='206f130070538fe1ca4fb7a7534045afeb210dc4959f290fd631f60429dc048e'
    for path,h in protected.items():require_hash(ROOT/path,h)
    inputs=['analysis/pending_insertion_500_025_selection_v1/selection.json','analysis/pending_insertion_500_025_compile500_v1/verification.json','analysis/pending_insertion_500_025_carry_v1/preflight.json','analysis/pending_insertion_500_025_input_gate_v1/verification.json','analysis/pending_insertion_500_025_models_test_v1/result.json','analysis/pending_insertion_500_025_gate_tests_v1/result.json','analysis/pending_insertion_500_025_native_controls_v1/cpu.json','tools/specs/primary025_version.json','analysis/pending_insertion_500_025_consumer_identity_v1/result.json','analysis/pending500_025_v1/build_failure.json','analysis/pending500_025_v2/sample_checker_correction.json']
    frozen_write(folder/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_AND_CHOICE_NICKNAME_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=sha(rom),rom_bytes=len(rom),previous_units=13122,new_units=500,total_units=m['translated_units'],primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/p) for p in inputs],protected_artifacts=protected,new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,
        diagnostic_note='New choice/nickname samples use quarantined PET root/table read aliases. Native initializer, text/choice handlers, navigation, confirm/cancel continuation and return execute; no alias enters the product ROM. Not battle caller/outcome or natural Navi/speaker acquisition coverage.',
        open_conditions=['Automatic Hangul composition/commit/save/redisplay remains unfinished; native kana keyboard and Japanese name suffix remain.','Inherited welcome bitmap tight/overlapping leading and untranslated field date HUD remain.','All500 semantic/human review, natural event/caller/branch/flag effects and worst-case dynamic providers remain incomplete.','No full playthrough, save integration, hardware or audio completion claim.'],
        next_action='Continue against actual025 applied-ID set. These500 are already applied; do not reselect/reapply. Preserve024/earlier evidence/saves. Continue500-unit cohorts and keyboard persistence/known UI defects; no BPS/xdelta/ZIP until requested.'))
    print('PASS025 checkpoint: +500, total13622; ROM/repro/runtime bound; no package')

if __name__=='__main__':main()

