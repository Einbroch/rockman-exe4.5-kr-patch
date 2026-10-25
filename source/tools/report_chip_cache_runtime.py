"""Cache candidate normal pixels and fixed-workload timing; not release QA."""
import json
from collections import Counter
from report_chip_library_runtime import visible_names, bdf_cells
from report_chip_library_stress import read, require, stats
from report_fixedcell_runtime import verify_route
from build_visibility_poc import ROOT, require_hash, sha


def main():
    build = '038ac069ff83dc920e82a9f9663f43fc0d7a973d1f75d39b4d7e33c6f1dffae7'
    m = read(ROOT / 'poc/output/exe45_ko_development_chip_cache_v2.json')
    require_hash(ROOT / 'poc/output/exe45_ko_development_chip_cache_v2.gba', build)
    source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    f = m['fixedcell_extension']
    require_hash(ROOT / f['font']['path'], f['font']['sha256'])
    cells = bdf_cells(ROOT / f['font']['path'], set('캐논에어슛발칸'), f['raster'])
    table = {v: bytes.fromhex(k) for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
             if '=' in line for k, v in [line.split('=', 1)] if len(v) == 1}
    p = ROOT / 'poc/runtime/chip-cache-v2-tabs'
    verify_route(p, build, set())
    env = read(p / 'cache_environment.json')
    require_hash(ROOT / 'tools/capture_chip_cache_qa.py', env['tool_sha256'])
    require(env['passed'], 'normal probe failed')
    c = read(p / 'final_cache.json')
    copies = read(p / 'final_chip_ko.json')['verified_word_copies']
    require(c['checks'] == c['hits'] + copies and c['resets'] == 1 and copies > 0, 'cache hit/miss denominator')
    pixels = {step: visible_names(p, step, {0: '캐논', 3: '에어슛', 4: '발칸1'}, cells, source.read_bytes(), table) for step in (7, 13)}
    q = ROOT / 'poc/runtime/chip-cache-v2-matrix56'
    r = verify_route(q, build, set())
    require(r.get('normal_play_checkpoint_eligible') is False and not (q / 'fixture_failed.txt').exists(), 'diagnostic scope/fault')
    env = read(q / 'cache_matrix_environment.json')
    require_hash(ROOT / 'tools/capture_chip_cache_matrix.py', env['tool_sha256'])
    require(env['passed'], 'matrix probe failed')
    d, s = read(q / 'final_timing.json'), read(q / 'final_stress.json')
    n = len(d['groups'])
    require(n > 100 and len(d['rows']) == n * 7 and len(d['updates']) == n and len(d['icons']) == n * 7, 'workload count')
    require(len(d['copies']) == 56 and d['groups'][0]['copies'] == 56 and all(g['copies'] == 0 and g['rows'] == 7 for g in d['groups'][1:]), 'cache miss/hit count')
    require(s['verified_rows'] == n * 7 and s['name_byte_substitutions'] == n * 231 and s['descriptor_read_substitutions'] == n * 28, 'fixture count')
    require(all(x['before'] == x['after'] for x in s['descriptors']), 'descriptor mutation')
    gaps = Counter(b['start']['frame'] - a['start']['frame'] for a, b in zip(d['groups'], d['groups'][1:]))
    require(dict(gaps) == {1: n - 1}, 'initial gap remains in this fixed workload')
    report = {'rom_sha256': build, 'status': 'experimental; broader regression pending',
              'normal_result_sha256': sha((p / 'result.json').read_bytes()), 'normal_cache': c, 'normal_copies': copies,
              'visible_names': pixels, 'diagnostic_result_sha256': sha((q / 'result.json').read_bytes()),
              'fixed_workload': {'groups': stats(d['groups']), 'updates': stats(d['updates']), 'copies': len(d['copies']),
                                 'icons': len(d['icons']), 'cadence_frames': dict(gaps)},
              'remaining': ['scroll and changing names', 'exit/foreign overwrite/reentry invalidation', 'save/reboot regression', 'no hardware or audio timing claim']}
    (ROOT / 'analysis/exe45_chip_cache_runtime_v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS normal pixels, reset and cache hits; fixed-workload intervals:', dict(gaps), '; broader regression PENDING')


if __name__ == '__main__':
    main()
