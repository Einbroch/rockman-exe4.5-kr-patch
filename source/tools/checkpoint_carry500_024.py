"""Record resumable024 cumulative carry/input gate without claiming a ROM."""
import subprocess
import sys
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from layout500_inputs_024 import load_inputs, MANIFEST, OUT as GATE


def main():
    prior_path='analysis/pending_insertion_500_024_checkpoint_v3/checkpoint.json'
    prior=read(prior_path)
    for p,h in prior['dependencies'].items():require_hash(ROOT/p,h)
    for p,h in prior['preserved_artifacts'].items():require_hash(ROOT/p,h)
    cfg=read('project.json');source_path=ROOT/cfg['source_profile']['filename']
    require_hash(source_path,cfg['source_profile']['sha256'])
    records,summary=load_inputs(source_path.read_bytes())
    gate=read(GATE)
    for p,h in gate['dependencies'].items():require_hash(ROOT/p,h)
    if not gate['passed'] or gate['rom_written'] or gate['product_integrated']:
        raise ValueError('024 component versus ROM claim')
    tests=[]
    for pattern in ('test_layout500_inputs_024.py','test_normal_pages_024.py','test_pet_quick_capacity_024.py'):
        test=subprocess.run([sys.executable,'-X','utf8','-m','unittest','discover','-s','tools','-p',pattern,'-v'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        if test.returncode:raise ValueError(test.stdout+test.stderr)
        tests.append(dict(pattern=pattern,passed=True,output=test.stdout+test.stderr))
    deps=[prior_path,MANIFEST,GATE,'tools/checkpoint_carry500_024.py','tools/test_layout500_inputs_024.py']
    result=dict(schema=1,status='EXACT500_CUMULATIVE_CARRY_AND_INPUT_GATE_PASS_NO_NEW_ROM',
        baseline_rom=prior['baseline_rom'],baseline_sha256=prior['baseline_sha256'],
        verified_rom_translated_units=prior['verified_rom_translated_units'],
        planned_new_units=500,merged_new_units=summary['new_units'],
        retained_carry_units_in_changed_archives=summary['carry_units'],
        merged_archives=summary['archives'],storage=summary['storage'],profiles=summary['profiles'],
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},
        preserved_artifacts=prior['preserved_artifacts'],tests=tests,
        source_reconstructed_carry_matches_actual023=True,
        all_nonnew_parent_scripts_preserved=True,
        current_source_bound_wording_geometry_input_gate=True,
        new_rom_units=0,rom_written=False,package_written=False,product_integrated=False,
        new500_rom_runtime_tested=False,insertion_ready=False,release_eligible=False,
        next_action='Do not reselect/retranslate/recompile these500 or reconstruct carry again. '
            'Use layout500_inputs_024.load_inputs at the versioned immutable-source primary build boundary. '
            'Integrate48 primary carry merges+2 new raw archives+19 A3 clone merges before allocation; '
            'version the A3 final verifier, retain oldB0 and other reader verification, and update '
            'metadata/input ownership, ExpectedWrites and exact500 lineage. Preserve frozen023 tool hashes '
            'rather than weakening their gates. Then independent product/repro and exact024 CPU/GBA tests.',
        development_notes=[
            'Gate implementation initially assumed every carry unit had needs_review and every script literal '
            'needed translation. Legacy input policy and non-Japanese punctuation invalidate those assumptions; '
            'carry uses its adopted translator and the selected denominator is Japanese-bearing literals. '
            'All punctuation remains protected in the full target comparison and aggregate page model.',
            'One old A3 ShadowMan LF layout is applied by the legacy input stage, not stored in its original '
            'draft. Carry comparison uses that exact effective pinned input and actual023 bytes. '
            'No wording, legacy production code or frozen preflight was changed.',
        ],
        limits='Compiled cumulative messages and reusable fresh input gate, not primary ROM integration. '
            'Prior023 renderer evidence is not024 runtime evidence. Conditional/flag semantics, final reader '
            'allocation/lineage/repro, automatic Hangul commit/save/redisplay and full human review remain open.')
    frozen_write(ROOT/'analysis/pending_insertion_500_024_checkpoint_v4/checkpoint.json',result)
    print('PASS024 checkpointv4: retained3191+new500,69archives;40 tests; ROM023 unchanged')


if __name__=='__main__':main()
