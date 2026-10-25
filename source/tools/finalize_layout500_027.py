"""Bind027 exact500/source builds and bounded QA, never a release package."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref


def main():
    out=ROOT/'analysis/pending500_027_v1';rp=ROOT/'poc/output/pending500_027_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/'poc/output/pending500_027_v1_repro.gba',sha(rom));baseline=read('poc/output/pending500_026_v1.json');proof=read(out/'integration.json')
    if not proof['passed'] or not proof['independent_rebuild_byte_identical'] or proof['new_units']!=500 or proof['total_units']!=baseline['translated_units']+500 or len(proof['new_raw_archives'])!=11 or proof['merged_consumer_archives']:
        raise ValueError('027 cumulative exact500/repro scope')
    reports=[]
    for name in ('integration.json','a3_cpu.json','b0_cpu.json','profile_cpu.json','integrity.json','native_control_identity.json','normal_runtime.json','profile_runtime.json','visual_review.json'):
        r=read(out/name)
        if not r['passed'] or r.get('rom_sha256',r.get('baseline_sha256'))!=sha(rom):raise ValueError('027 report identity '+name)
        reports.append(ref(out/name))
    cpu=read(out/'profile_cpu.json')
    if cpu['case_count']!=304 or cpu['native_helpers_substituted']:raise ValueError('027 bounded CPU scope')
    samples=read(out/'profile_runtime.json');selection=read('analysis/pending_insertion_500_027_selection_v1/selection.json');sampled={k for page in samples['pages'] for k in page['ids']}
    if len(samples['pages'])!=2 or len(sampled)!=3 or not sampled<=set(selection['selected_ids']):raise ValueError('027 bounded new literal sample scope')
    visual=read(out/'visual_inputs.json')
    if visual['rom_sha256']!=sha(rom) or {s['kind']:s['screens'] for s in visual['sheets']}!={'startup':22,'mail':23,'raw':5}:raise ValueError('027 visual scope')
    for s in visual['sheets']:require_hash(ROOT/s['path'],s['sha256'])
    protected=dict(read('analysis/pending500_026_v1/batch_status.json')['protected_artifacts']);protected['poc/output/pending500_026_v1.gba']=baseline['output_sha256']
    for p,h in protected.items():require_hash(ROOT/p,h)
    inputs=['analysis/pending_insertion_500_027_selection_v1/selection.json','analysis/pending_insertion_500_027_compile500_v1/verification.json','analysis/pending_insertion_500_027_carry_v2/preflight.json','analysis/pending_insertion_500_027_input_gate_v1/verification.json','analysis/pending_insertion_500_027_models_test_v1/result.json','analysis/pending_insertion_500_027_gate_tests_v2/result.json','analysis/pending_insertion_500_027_profile_cpu_v2/cpu.json','analysis/pending_insertion_500_027_checkpoint_failures.json','tools/specs/primary027_version.json']
    frozen_write(out/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_MAX_NATIVE_PROFILE_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=sha(rom),rom_bytes=len(rom),previous_units=baseline['translated_units'],new_units=500,total_units=m['translated_units'],new_whole_scripts=len(selection['groups']),primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],independent_rebuild_byte_identical=True,reports=reports,inputs=[ref(ROOT/p) for p in inputs],protected_artifacts=protected,diagnostic_new_literal_ids=sorted(sampled),diagnostic_page_observations=2,new_distribution_packages_created=False,semantic_human_approved=False,release_eligible=False,complete_integrated_request=False,diagnostic_note='Two max8/max4 valid native profile records are temporarily seeded at real F90C reader and restored after native copy. Root/table read aliases select two scripts; native PET initializer, RAM provider consumption, ROM literals, fonts, OBJ/pixels, aggregate offsets, waits and return sampled. Not natural acquisition/default/import, every provider, saves or Hangul support.',open_conditions=read(out/'visual_review.json')['open_conditions'],next_action='Continue against actual027 IDs/effective cumulative027.scope and source. These500 are applied; do not reapply. New carry reconstruction must include024->025->026->027. Continue500-unit cohorts, full-context review and unresolved Hangul commit/save/redisplay. Preserve original/prior ROMs/saves/evidence/ZIP; no new packages until asked.'))
    print('PASS027 +500 total',m['translated_units'],'source builds/repro/static/max-profile sample QA; no package')


if __name__=='__main__':main()
