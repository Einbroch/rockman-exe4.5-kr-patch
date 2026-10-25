"""Record source-only272 compilation without promoting it to ROM admission."""
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records


def main():
    previous = 'analysis/pending_insertion_500_024_checkpoint_v1/checkpoint.json'
    compile_path = 'analysis/pending_insertion_500_024_compile_v2/verification.json'
    cpu_path = 'analysis/pending_insertion_500_024_native_controls_v2/cpu.json'
    old, compiled, cpu = read(previous), read(compile_path), read(cpu_path)
    for r in (compiled, cpu):
        if not r['passed'] or r['rom_written'] or r['baseline_sha256'] != old['baseline_sha256']:
            raise ValueError('Evidence identity/scope')
    if compiled['insertion_ready'] or compiled['product_integrated'] or compiled['units'] != 272 or cpu['runtime_tested']:
        raise ValueError('No promotion of component evidence')
    for p, h in old['preserved_artifacts'].items():
        require_hash(ROOT/p, h)
    for r in (compiled,cpu):
        for p,h in r['dependencies'].items():
            require_hash(ROOT/p,h)
    initial_cpu = read('analysis/pending_insertion_500_024_native_controls_v1/cpu.json')
    if cpu['cases'] != initial_cpu['cases']:
        raise ValueError('Extended source-range binding changed CPU effects')
    m = read(old['baseline_rom'].replace('.gba','.json'))
    applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    new_ids = [u['id'] for r in compiled['archives'] for u in r['units']]
    if len(new_ids) != len(set(new_ids)) or applied & set(new_ids):
        raise ValueError('Distinct not-yet-applied candidate IDs')
    for r in compiled['archives']:
        for key in ('source_tpl','compiled','target_tpl'):
            require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        if not r['native_roundtrip'] or not r['binary_roundtrip'] or not r['controls_preserved'] or r['product_admitted']:
            raise ValueError('Archive mechanical policy')
    deps = [previous,compile_path,cpu_path,'analysis/pending_insertion_500_024_native_controls_v1/cpu.json','tools/checkpoint_pending024_compile.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_024_checkpoint_v2/checkpoint.json',dict(schema=1,status='SOURCE_ONLY272_COMPILED_NATIVE_CONTROL_CPU_VERIFIED_NO_NEW_ROM',baseline_rom=old['baseline_rom'],baseline_sha256=old['baseline_sha256'],verified_translated_units=old['verified_translated_units'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},preserved_artifacts=old['preserved_artifacts'],source_only_candidate_units=len(new_ids),source_only_archives=len(compiled['archives']),source_only_glyphs=compiled['extended_glyphs_checked'],within_page_lf_edit_units=len(compiled['within_page_lf_edits']),native_control_cpu_cases=cpu['case_count'],new_ids_do_not_overlap_applied=True,requested_batch_units=500,selected500=None,new_rom_units=0,rom_written=False,package_written=False,runtime_tested=False,release_eligible=False,next_action='Collect the remaining distinct units by establishing msgOpen-before-portrait and other preserved-source command forms; do not re-survey the272 already mechanically compiled. Before primary integration, bind exact500/current source/explicit LF policy, rederive cumulative carry from actual023, then product/repro/write-plan/CPU and GBA render/clear/reentry checks.',limits='Source-only full archives contain unselected original literals and MUST NOT replace023 carry directly.72 CPU cases substitute one exact BIOS CpuFastSet contract, not actual GBA transfer/pixels. Full original source and023 hashes plus specific native literal ranges bind evidence. Automatic Hangul commit/save/redisplay and other recorded product defects remain open.'))
    print('PASS checkpoint024v2:272 distinct source-only units/58 archives/376 glyphs/72 CPU cases;ROM023 unchanged')


if __name__ == '__main__':
    main()
