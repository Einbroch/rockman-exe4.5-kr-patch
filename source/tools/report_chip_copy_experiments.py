"""Retain rejected copy-engine experiments and their bounded evidence."""
import json
from collections import Counter
from build_visibility_poc import ROOT, require_hash, sha
from report_fixedcell_runtime import verify_route
from report_chip_library_stress import read, require, stats
from report_chip_library_runtime import visible_names, bdf_cells


def main():
    rows = []
    cases = [('burst', '22e337da4c5e137c1f6cf9e5782fd2db2134bfaf7fc054363289b7cff2603c08', 'capture_chip_burst_changing.py'),
             ('fast', '6b8438dd9aa9465ca75798daed677c7603234579573b0731799f9f25b297764b', 'capture_chip_fast_changing.py'),
             ('stack', '7274da9b778215a80e2b57253ab96b8bce47722f26dafbe42c21b3a34c510d6b', 'capture_chip_stack_changing.py')]
    for kind, build, tool in cases:
        stem = f'exe45_ko_development_chip_{kind}_cache_v1'
        require_hash(ROOT / f'poc/output/{stem}.gba', build)
        m = read(ROOT / f'poc/output/{stem}.json')
        source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
        require_hash(source, m['source_sha256'])
        p = ROOT / f'poc/runtime/chip-{kind}-cache-v1-changing56'
        r = verify_route(p, build, set())
        require(r.get('normal_play_checkpoint_eligible') is False and not (p / 'fixture_failed.txt').exists(), 'diagnostic failure')
        e = read(p / f'{kind}_environment.json')
        require_hash(ROOT / f'tools/{tool}', e['tool_sha256'])
        d, s = read(p / 'final_timing.json'), read(p / 'final_stress.json')
        n = len(d['groups'])
        require(n > 100 and len(d['copies']) == 56*n and all(g['copies'] == 56 and g['rows'] == 7 for g in d['groups']), 'copy denominator')
        require(s['verified_rows'] == 7*n and len(d['updates']) == n and len(d['icons']) == ((n+1)//2)*7, 'row/update/icon denominator')
        require(read(p / 'final_changing.json') == {'epochs':n, 'post_icon_checks':n}, 'post-icon lifetime')
        require(all(x['before'] == x['after'] for x in s['descriptors']), 'underlying descriptor mutation')
        pe = read(p / 'probe_environment.json')
        for filename, old in pe['files_before'].items():
            if filename.endswith('.sav'):
                require(pe['files_after'][filename] == old, 'isolated save changed')
        gaps = Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
        entry = {'kind':kind, 'rom_sha256':build, 'result_sha256':sha((p / 'result.json').read_bytes()),
                 'data_correctness':'PASS bounded changing fixture', 'cadence_frames':dict(gaps),
                 'groups':stats(d['groups']), 'updates':stats(d['updates']),
                 'decision':'not a timing fix; retain as experiment'}
        if kind == 'stack':
            st = read(p / 'final_stack.json')
            require(e['passed'] and st['invocations'] == st['rows_returned'] == 7*n, 'stack invocation denominator')
            entry['stack'] = st
        rows.append(entry)
    p = ROOT / 'poc/runtime/chip-burst-cache-v1-tabs'
    verify_route(p, cases[0][1], set())
    m = read(ROOT / 'poc/output/exe45_ko_development_chip_burst_cache_v1.json')
    f = m['fixedcell_extension']
    cells = bdf_cells(ROOT / f['font']['path'], set('캐논에어슛발칸'), f['raster'])
    table = {v:bytes.fromhex(k) for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
             if '=' in line for k,v in [line.split('=',1)] if len(v) == 1}
    pixels = {step:visible_names(p,step,{0:'캐논',3:'에어슛',4:'발칸1'},cells,source.read_bytes(),table) for step in (7,13)}
    require_hash(ROOT / 'poc/output/exe45_ko_development_chip_burst_cache_v1_repro.gba', cases[0][1])
    report = {'scope':'copy-engine comparison on separate same-revision cold routes; no identical full-state timing claim',
              'cases':rows, 'burst_normal_cache':read(p / 'final_cache.json'), 'burst_visible_names':pixels,
              'conclusion':'burst reduces copy cost; fast BIOS and per-row stack execution do not fix the wait boundary',
              'baseline_selection':'unchanged ce839 chip-library development ROM',
              'limits':['changing fixture substitutes reads', 'no audio/hardware proof', 'fast/stack not promoted']}
    (ROOT / 'analysis/exe45_chip_copy_experiments_v1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS bounded evidence for burst/fast/stack; all retain initial cadence gap')


if __name__ == '__main__':
    main()
