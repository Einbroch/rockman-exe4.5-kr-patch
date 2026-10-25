"""Verify retained cache-v2 normal scrolling and foreign-VRAM reuse evidence."""
import json
from build_visibility_poc import ROOT, require_hash, sha
from report_chip_library_runtime import visible_names, bdf_cells
from report_chip_library_stress import read, require
from report_fixedcell_runtime import verify_route


def main():
    build = '038ac069ff83dc920e82a9f9663f43fc0d7a973d1f75d39b4d7e33c6f1dffae7'
    m = read(ROOT / 'poc/output/exe45_ko_development_chip_cache_v2.json')
    require_hash(ROOT / 'poc/output/exe45_ko_development_chip_cache_v2.gba', build)
    source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    native = source.read_bytes()
    p = ROOT / 'poc/runtime/chip-cache-v2-input-lifetime'
    q = ROOT / 'poc/runtime/chip-cache-v2-scroll-reentry'
    for path in (p, q):
        verify_route(path, build, set())
        require(not list(path.glob('*failed*')), 'runtime fault artifact')
    overwritten = []
    for step in (4, 5):
        v = (p / f'step_{step:03d}_gbaVideoRam.bin').read_bytes()
        require(v[0x8000:0x9000] == native[0x63ABF4:0x63BBF4], 'foreign font reclamation missing')
        require(any(v[0x8E40:0x8EB0]), 'foreign tags unexpectedly zero')
        overwritten.append(step)
    env = read(q / 'cache_environment.json')
    require_hash(ROOT / 'tools/capture_chip_cache_qa.py', env['tool_sha256'])
    require(env['passed'] and env['rom_sha256'] == build, 'cache observer failed')
    c = read(q / 'final_cache.json')
    copies = read(q / 'final_chip_ko.json')['verified_word_copies']
    require(c['checks'] == c['hits'] + copies and c['resets'] == 1 and copies > 7, 'scroll miss/reset coverage')
    f = m['fixedcell_extension']
    require_hash(ROOT / f['font']['path'], f['font']['sha256'])
    cells = bdf_cells(ROOT / f['font']['path'], set('캐논에어슛발칸'), f['raster'])
    table = {v: bytes.fromhex(k) for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
             if '=' in line for k, v in [line.split('=', 1)] if len(v) == 1}
    expected = {3: {0: '캐논', 3: '에어슛', 4: '발칸1'}, 12: {1: '에어슛', 2: '발칸1'},
                18: {}, 32: {0: '캐논', 3: '에어슛', 4: '발칸1'}, 38: {0: '캐논', 3: '에어슛', 4: '발칸1'}}
    pixels = {s: visible_names(q, s, rows, cells, native, table) for s, rows in expected.items()}
    save = ROOT / 'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav'
    require_hash(save, '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    report = {'rom_sha256': build, 'status': 'PASS bounded normal-input reentry and scroll; not release QA',
              'routes': {str(x.relative_to(ROOT)): sha((x / 'result.json').read_bytes()) for x in (p, q)},
              'foreign_font_overwrite_steps': overwritten, 'cache': c, 'actual_copies': copies,
              'visible_names': pixels, 'baseline_save_sha256': sha(save.read_bytes()),
              'remaining': ['save/reboot regression', 'changing full 56-cell workload timing', 'conditional icon lifetimes', 'hardware/audio unverified']}
    (ROOT / 'analysis/exe45_chip_cache_reentry_v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS foreign overwrite, reset, scrolling pixels:', c, 'copies:', copies)


if __name__ == '__main__':
    main()
