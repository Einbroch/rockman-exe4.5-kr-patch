"""Revalidate retained factorial diagnostics; never declares a product fix."""
import json
from collections import Counter
from pathlib import Path
from report_chip_library_stress import BUILD, read, require, stats
from report_fixedcell_runtime import verify_route
from build_visibility_poc import ROOT, require_hash, sha

PINS = {
    (0, 0): 'b69fb54f416a7cf808b6e29490a9d57d030464b46ff3878c31a1ea8226fadcef',
    (0, 7): '86a77d2b9128ce35662ac3ff3dac9d0bbdc2cc7cd7707daaaffc36fb97606c17',
    (56, 0): 'a0799efcd2a6b49fcb3c30783348d8e416fa80a83c0fec31c2348cd215aad5d0',
    (56, 7): '8b40607a9921d47549dca7abf4b9bca7bafe9ba96635060304b329a25cecf51c',
}


def validate(d, s, hangul, icons):
    n = len(d['groups'])
    require(n > 100, 'insufficient groups')
    require(len(d['rows']) == n * 7 and len(d['copies']) == n * hangul
            and len(d['icons']) == n * icons and len(d['updates']) == n, 'workload count')
    require(all(g['rows'] == 7 and g['copies'] == hangul for g in d['groups']), 'group workload')
    require(s['verified_rows'] == n * 7 and s['name_byte_substitutions'] == n * 7 * (33 if hangul else 9)
            and s['descriptor_read_substitutions'] == n * (28 if icons else 21), 'substitution count')
    require(bool(s['descriptors']) and all(x['before'] == x['after'] for x in s['descriptors']), 'descriptor mutation')
    for group in d['groups']:
        require(group['end']['clock'] - group['start']['clock'] == group['cycles'], 'clock mismatch')
    gaps = [b['start']['frame'] - a['start']['frame'] for a, b in zip(d['groups'], d['groups'][1:])]
    require(all(x > 0 for x in gaps), 'nonmonotonic cadence')
    return {'groups': stats(d['groups']), 'updates': stats(d['updates']),
            'glyph_copies': len(d['copies']), 'icon_copies': len(d['icons']),
            'cadence_frames': dict(sorted(Counter(gaps).items())),
            'gap_after_group_1based': [i + 1 for i, gap in enumerate(gaps) if gap != 1]}


def main():
    results, seen, baseline = [], set(), None
    for (h, i), pin in PINS.items():
        path = ROOT / f'poc/runtime/chip-matrix-h{h}-i{i}'
        require_hash(path / 'result.json', pin)
        r = verify_route(path, BUILD, seen)
        require(r.get('normal_play_checkpoint_eligible') is False and not (path / 'checkpoint.mss').exists(), 'diagnostic isolation')
        require(not (path / 'fixture_failed.txt').exists(), 'fixture failed')
        identity = [r[k] for k in ('state_sha256', 'actions', 'emulator_components')]
        if baseline is None:
            baseline = identity
        require(identity == baseline, 'comparison baseline differs')
        env = read(path / 'matrix_environment.json')
        require((env['hangul'], env['icons']) == (h, i), 'factor labels')
        require_hash(ROOT / 'tools/capture_chip_library_matrix.py', env['tool_sha256'])
        result = validate(read(path / 'final_timing.json'), read(path / 'final_stress.json'), h, i)
        results.append(dict(hangul=h, icons=i, path=str(path.relative_to(ROOT)), result_sha256=pin, **result))
    save = ROOT / 'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav'
    require_hash(save, '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    out = ROOT / 'analysis/exe45_chip_library_matrix_v1.json'
    report = {'scope': 'synthetic consumer-input factorial experiment; NOT normal-play reachability or fix verification',
              'rom_sha256': BUILD, 'issue': 'CHIP-CACHE-TIMING-001', 'status': 'OPEN',
              'prior_verified_save_unchanged': True, 'cases': results}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
