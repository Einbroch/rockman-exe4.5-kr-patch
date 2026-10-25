"""Separate changing-workload data correctness from cadence acceptance."""
import json
from collections import Counter
from build_visibility_poc import ROOT, require_hash, sha
from report_fixedcell_runtime import verify_route
from report_chip_library_stress import read, require, stats


def main():
    build = '038ac069ff83dc920e82a9f9663f43fc0d7a973d1f75d39b4d7e33c6f1dffae7'
    p = ROOT / 'poc/runtime/chip-cache-v2-changing56'
    r = verify_route(p, build, set())
    require(r['normal_play_checkpoint_eligible'] is False and not (p / 'checkpoint.mss').exists(), 'diagnostic quarantine')
    require(not (p / 'fixture_failed.txt').exists(), 'fixture failure')
    env = read(p / 'changing_environment.json')
    require_hash(ROOT / 'tools/capture_chip_cache_changing.py', env['tool_sha256'])
    require(env['passed'], 'changing observer failed')
    m = read(ROOT / 'poc/output/exe45_ko_development_chip_cache_v2.json')
    require_hash(ROOT / 'poc/output/exe45_ko_development_chip_cache_v2.gba', build)
    require_hash(ROOT / read(ROOT / 'project.json')['source_profile']['filename'], m['source_sha256'])
    d, s = read(p / 'final_timing.json'), read(p / 'final_stress.json')
    n = len(d['groups'])
    require(n > 100 and len(d['rows']) == 7*n and len(d['updates']) == n, 'group denominator')
    require(all(g['copies'] == 56 and g['rows'] == 7 for g in d['groups']) and len(d['copies']) == 56*n, 'changing misses')
    require(len(d['icons']) == ((n+1)//2)*7, 'icon denominator')
    require(read(p / 'final_changing.json') == {'epochs': n, 'post_icon_checks': n}, 'post-icon residency checks')
    require(s['verified_rows'] == 7*n and s['name_byte_substitutions'] == 231*n, 'row/name denominator')
    require(s['descriptor_read_substitutions'] == 28*((n+1)//2)+21*(n//2), 'descriptor denominator')
    require(all(x['before'] == x['after'] for x in s['descriptors']), 'descriptor memory modified')
    saves = read(p / 'probe_environment.json')
    for name, record in saves['files_before'].items():
        if name.endswith('.sav'):
            require(saves['files_after'][name] == record, 'disk save changed')
    require_hash(ROOT / 'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav', '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    gaps = Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
    report = {'rom_sha256': build, 'result_sha256': sha((p / 'result.json').read_bytes()),
              'data_correctness': 'PASS synthetic changing 56 cells; actual copies, tags and post-icon residency',
              'cadence_all_one': dict(gaps) == {1:n-1}, 'cadence_frames': dict(gaps),
              'name_groups': stats(d['groups']), 'updates': stats(d['updates']),
              'copies': len(d['copies']), 'icons': len(d['icons']), 'rows': s['verified_rows'],
              'limits': ['diagnostic read substitutions, not acquired inventory', 'standard tab only',
                         'icon copy/residency checked, not complete visible icon/clearing QA',
                         'muted Mesen, no hardware/audio or scanout tearing claim']}
    (ROOT / 'analysis/exe45_chip_cache_changing_v2.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
