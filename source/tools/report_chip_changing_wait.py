"""Verify same-state controls for the changed-glyph wait-boundary regression."""
import json
from collections import Counter
from build_visibility_poc import ROOT, require_hash, sha
from report_fixedcell_runtime import verify_route
from report_chip_library_stress import read, require, stats
from report_chip_wait_trace import summarize


def main():
    build = '038ac069ff83dc920e82a9f9663f43fc0d7a973d1f75d39b4d7e33c6f1dffae7'
    rows = []
    for mode, tool in (('changing-wait', 'capture_chip_changing_wait.py'), ('stable-control', 'capture_chip_cache_stable_control.py')):
        p = ROOT / ('poc/runtime/chip-cache-v2-' + mode)
        r = verify_route(p, build, set())
        require(r['normal_play_checkpoint_eligible'] is False and not (p / 'fixture_failed.txt').exists(), 'diagnostic scope')
        e = read(p / ('changing_wait_environment.json' if mode == 'changing-wait' else 'stable_control_environment.json'))
        require_hash(ROOT / ('tools/' + tool), e['tool_sha256'])
        d, s = read(p / 'final_timing.json'), read(p / 'final_stress.json')
        n = len(d['groups'])
        require(n > 100 and s['verified_rows'] == n*7 and len(d['updates']) == n, 'workload denominator')
        require(len(d['icons']) == 7*((n+1)//2), 'alternating icon denominator')
        expected = [56]*n if mode == 'changing-wait' else [56]+[0]*(n-1)
        require([g['copies'] for g in d['groups']] == expected, 'copy schedule')
        gaps = Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'], d['groups'][1:]))
        rows.append({'mode': mode, 'state_sha256': r['state_sha256'], 'actions': r['actions'],
                     'result_sha256': sha((p / 'result.json').read_bytes()), 'groups': stats(d['groups']),
                     'cadence': dict(gaps), 'wait_group_2': summarize(read(p / 'final_wait_trace.json')['events'])})
    require(rows[0]['state_sha256'] == rows[1]['state_sha256'] and rows[0]['actions'] == rows[1]['actions'], 'control state/input mismatch')
    require(rows[0]['cadence'].get(2) == 1 and list(rows[1]['cadence']) == [1], 'discriminating outcome absent')
    require(rows[0]['wait_group_2']['entry_scanline'] >= 160 and rows[1]['wait_group_2']['entry_scanline'] < 160, 'wait boundary not isolated')
    report = {'issue': 'CHIP-CACHE-TIMING-001', 'status': 'OPEN', 'rom_sha256': build,
              'boundary': 'same state and alternating icons: changed 56 glyphs cross native VBlank wait boundary; stable glyph hits arrive before it',
              'cases': rows, 'limits': ['diagnostic reads; whole clock streams not claimed identical', 'muted Mesen only', 'native wait code unchanged']}
    (ROOT / 'analysis/exe45_chip_changing_wait_v2.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
