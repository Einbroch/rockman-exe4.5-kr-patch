"""Current024 development evidence index, never a distribution package."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rp=ROOT/'poc/output/pending500_024_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    repro=rp.with_name(rp.stem+'_repro.gba');require_hash(repro,sha(rom))
    out=ROOT/'analysis/pending500_024_v1'
    names=['integration.json','a3_cpu.json','b0_cpu.json','integrity.json','normal_runtime.json',
           'raw_displays.json','a3_runtime.json','natural_b0_runtime.json','exit_runtime.json',
           'visual_review_initial.json','visual_review_hints.json']
    reports={n:read(out/n) for n in names}
    for name,r in reports.items():
        if r['rom_sha256']!=sha(rom) or not r['passed']:raise ValueError('024 report applicability/pass '+name)
    integration=reports['integration.json'];normal=reports['normal_runtime.json']
    if not integration['independent_rebuild_byte_identical'] or integration['new_units']!=500 or normal['first_mail_ordered_page_count']!=23 or not normal['first_mail_normal_reentry_verified']:
        raise ValueError('024 exact500/repro/normal regression')
    checkpoint=read('analysis/pending_insertion_500_024_checkpoint_v4/checkpoint.json')
    for p,h in checkpoint['preserved_artifacts'].items():require_hash(ROOT/p,h)
    previous=read('poc/output/pending500_023_v1.json')
    if m['translated_units']!=previous['translated_units']+500:raise ValueError('024 cumulative total')
    inputs=['analysis/pending_insertion_500_024_checkpoint_v4/checkpoint.json',
            'analysis/pending_insertion_500_024_carry_v1/preflight.json',
            'analysis/pending_insertion_500_024_input_gate_v1/verification.json',
            'tools/specs/primary024_version.json']
    frozen_write(out/'batch_status.json',dict(schema=1,
        status='DEVELOPMENT_500_APPLIED_REBUILT_AND_RAW_A3_B0_SAMPLED_NOT_RELEASE',
        rom=str(rp.relative_to(ROOT)),rom_sha256=sha(rom),rom_bytes=len(rom),
        previous_units=previous['translated_units'],new_units=500,total_units=m['translated_units'],
        primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],
        independent_rebuild_byte_identical=True,
        reports=[dict(path=str((out/n).relative_to(ROOT)),sha256=sha((out/n).read_bytes())) for n in names],
        inputs=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in inputs],
        protected_artifacts=checkpoint['preserved_artifacts'],new_distribution_packages_created=False,
        new_raw_pages_sampled=4,new_A3_scripts_sampled=2,new_A3_executions_sampled=4,
        old_B0_normal_executions_sampled=2,native_keyboard_pages_sampled=3,first_mail_pages_sampled=23,
        source_bound_normal_and_PET_page_models=True,semantic_human_approved=False,release_eligible=False,
        complete_integrated_request=False,
        diagnostic_note='Raw samples use quarantined PET root/table read aliases. A3 uses native compressed '
            'loader/scene/table read aliases, but source-preserved native flags/weekdays execute without edits. '
            'B0 is ordinary Monday L input without those aliases. No diagnostic survives in the product ROM.',
        implementation_notes=[
            'Current primary tools/build_layout500_024.py -> explicit versioned build_development_patch_024.py. '
            'Legacy023 production modules and their frozen tool-hash gates remain unchanged. All final writes '
            'are composed before allocation/application from the immutable original, not a patched-ROM overlay.',
            'First A3 capture attempt refused a historical prefix-only assumption before launching the emulator. '
            'Native scripts10/26 actually have conditionals before the portrait opener. Failed tool is retained; '
            'v2 requires the entire original guard prefix plus opener unchanged and executes the native guards. '
            'No ROM or flags were changed to make the observation pass.'
        ],
        open_conditions=[
            'Automatic Hangul composition/commit/save/redisplay remains unfinished; native kana input and Japanese name suffix remain.',
            'Inherited welcome bitmap tight/overlapping leading and untranslated field date HUD remain.',
            'All500 wording/human review, natural A3 event/provider/branch coverage, fixed-flag event effects and variable-insertion displays remain incomplete.',
            'No full playthrough, save integration, real-hardware or audio completion claim.'
        ],
        next_action='Resume against actual024 applied-ID set, not023. Continue remaining untranslated population '
            'in500-unit cohorts where eligible, keeping source/consumer coverage and carry preservation. '
            'Do not retranslate or reapply these500. Keep keyboard persistence and known UI defects visible. '
            'No BPS/xdelta/ZIP until the user requests packaging again.'))
    print('PASS024 development500 applied/rebuilt/sampled; total',m['translated_units'],'NOT RELEASE; no packages')


if __name__=='__main__':main()
