"""Compare retained cold-derived diagnostic workloads; preserve open defect."""
import json
from report_chip_library_matrix import validate
from report_chip_library_stress import stats, read, require
from report_fixedcell_runtime import verify_route
from build_visibility_poc import ROOT, require_hash, sha


def main():
    cases = []
    for name, h, build in [
        ('chip-legacy-matrix-cold56', 56, 'ce839b60c8125da7ca8ce0240bcdfc82a8e8f5604202449af1acffa80158cbff'),
        ('chip-wordcopy-matrix-cold56', 56, '403fc8670b32646ebe9a854ae3f3c194095311bd4966af70effd1e161fd9436a'),
        ('chip-wordcopy-matrix-cold0', 0, '403fc8670b32646ebe9a854ae3f3c194095311bd4966af70effd1e161fd9436a')]:
        p = ROOT / 'poc/runtime' / name
        r = verify_route(p, build, set())
        require(r.get('normal_play_checkpoint_eligible') is False and not (p / 'fixture_failed.txt').exists(), 'diagnostic isolation/fault')
        d, s = read(p / 'final_timing.json'), read(p / 'final_stress.json')
        e = read(p / 'matrix_environment.json')
        require((e['hangul'], e['icons']) == (h, 7), 'factor labels')
        require_hash(ROOT / 'tools/capture_chip_library_matrix.py', e['tool_sha256'])
        if 'wordcopy' in name:
            w = read(p / 'wordcopy_matrix_environment.json')
            require_hash(ROOT / 'tools/capture_chip_wordcopy_matrix.py', w['tool_sha256'])
        result = validate(d, s, h, 7)
        cases.append(dict(name=name, rom_sha256=build, result_sha256=sha((p / 'result.json').read_bytes()),
            state_sha256=r['state_sha256'], actions=r['actions'], emulator=r['emulator_components'],
            copy_cycles=stats(d['copies']) if h else None, initial_groups=d['groups'][:4], **result))
    require(all(c['actions'] == cases[0]['actions'] and c['emulator'] == cases[0]['emulator'] for c in cases), 'route/environment mismatch')
    require(cases[1]['state_sha256'] == cases[2]['state_sha256'], 'candidate control state mismatch')
    require_hash(ROOT / 'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav',
                 '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    report = {'scope': 'muted Mesen diagnostic read substitutions, not normal acquisition or hardware FPS',
        'comparison_limit': 'Each ROM uses its own cold-derived state; frame count and route agree, CPU/PPU cycle and EWRAM are not byte-identical. Candidate 56 versus 0 uses exactly the same state.',
        'issue': 'CHIP-CACHE-TIMING-001', 'status': 'OPEN', 'cases': cases,
        'name_group_median_reduction_percent': 100 * (1 - cases[1]['groups']['median'] / cases[0]['groups']['median']),
        'full_update_median_reduction_percent': 100 * (1 - cases[1]['updates']['median'] / cases[0]['updates']['median'])}
    (ROOT / 'analysis/exe45_chip_wordcopy_timing_v1.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
