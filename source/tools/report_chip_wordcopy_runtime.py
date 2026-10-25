"""Retained normal-route evidence for the word-copy candidate, not timing closure."""
import json
from report_chip_library_runtime import ROOT, read, require, visible_names, bdf_cells
from report_fixedcell_runtime import verify_route
from build_visibility_poc import require_hash, sha


def main():
    build = '403fc8670b32646ebe9a854ae3f3c194095311bd4966af70effd1e161fd9436a'
    path = ROOT / 'poc/runtime/chip-wordcopy-v1-tabs-verified'
    r = verify_route(path, build, set())
    env = read(path / 'wordcopy_environment.json')
    require(env['passed'] and env['rom_sha256'] == build, 'probe failed')
    require_hash(ROOT / 'tools/capture_chip_wordcopy_qa.py', env['tool_sha256'])
    m = read(ROOT / 'poc/output/exe45_ko_development_chip_wordcopy_v1.json')
    require_hash(ROOT / 'poc/output/exe45_ko_development_chip_wordcopy_v1.gba', build)
    source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    f = m['fixedcell_extension']
    require_hash(ROOT / f['font']['path'], f['font']['sha256'])
    cells = bdf_cells(ROOT / f['font']['path'], set('캐논에어슛발칸'), f['raster'])
    table = {}
    for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            if len(value) == 1:
                table[value] = bytes.fromhex(key)
    samples = {step: visible_names(path, step, {0: '캐논', 3: '에어슛', 4: '발칸1'}, cells, source.read_bytes(), table)
               for step in (7, 9, 15)}
    lib = read(path / 'final_library.json')
    require(lib['loads'] and all(x['outside_changed_bytes'] == 0 for x in lib['loads']), 'loader collateral change')
    require(lib['hook_calls'] and all(x['abi_pass'] for x in lib['hook_calls']), 'header ABI')
    c = read(path / 'final_chip_ko.json')
    require(c['abi_calls'] > 0 and c['verified_word_copies'] > 0, 'no word-copy evidence')
    report = {'rom_sha256': build, 'result_sha256': sha((path / 'result.json').read_bytes()),
              'scope': 'normal cold-derived library entry, tabs and return; NOT worst-case timing or save regression',
              'abi_calls': c['abi_calls'], 'verified_word_copies': c['verified_word_copies'],
              'visible_name_samples': samples, 'loader_checks': lib['loads'], 'timing_issue': 'OPEN'}
    (ROOT / 'analysis/exe45_chip_wordcopy_runtime_v1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS', c['abi_calls'], 'ABI returns;', c['verified_word_copies'], 'actual word copies;', len(samples), 'pixel/map samples')


if __name__ == '__main__':
    main()
