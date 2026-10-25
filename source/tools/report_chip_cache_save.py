"""Bounded cache-v2 save/cold-reboot evidence, not full save compatibility."""
import json
from build_visibility_poc import ROOT, require_hash, sha
from report_chip_library_runtime import read, require, visible_names, bdf_cells
from report_fixedcell_runtime import verify_route


def main():
    build = '038ac069ff83dc920e82a9f9663f43fc0d7a973d1f75d39b4d7e33c6f1dffae7'
    stem = 'exe45_ko_development_chip_cache_v2'
    m = read(ROOT / f'poc/output/{stem}.json')
    require_hash(ROOT / f'poc/output/{stem}.gba', build)
    source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    name = stem + '.sav'
    routes, envs, seen = {}, {}, set()
    for part in ('entry', 'commit', 'finish', 'reboot'):
        p = ROOT / f'poc/runtime/chip-cache-v2-save-{part}'
        r = verify_route(p, build, seen)
        require(r['return_code'] == 0, 'runner failure')
        e = read(p / 'save_environment.json')
        require(e['build_sha256'] == build, 'foreign environment')
        for filename, record in e['files_after'].items():
            require_hash(p / 'persistent_files_after' / filename, record['sha256'])
        for filename, record in e['files_before'].items():
            if filename not in (name, stem + '.rtc'):
                require(e['files_after'][filename] == record, 'unrelated persistent file changed')
        if envs:
            require(e['files_before'] == envs[previous]['files_after'], 'disk state chain interrupted')
        envs[part] = e
        previous = part
        routes[part] = {'result_sha256': sha((p / 'result.json').read_bytes()),
                        'environment_sha256': sha((p / 'save_environment.json').read_bytes())}
        if part == 'reboot':
            require(r['state_origin'] is None and not (p / 'input.mss').exists(), 'reboot loaded checkpoint')
    saved = envs['finish']['files_after'][name]
    require(saved['bytes'] == 65536 and saved == envs['reboot']['files_before'][name] == envs['reboot']['files_after'][name], 'save/reboot identity mismatch')
    require(saved != envs['entry']['files_before'][name], 'no new save recorded')
    require_hash(ROOT / f'poc/runtime/chip-matrix-saves/{name}', saved['sha256'])
    p = ROOT / 'poc/runtime/chip-cache-v2-reboot-library-retry'
    verify_route(p, build, seen)
    c = read(p / 'final_cache.json')
    e = read(p / 'cache_environment.json')
    require_hash(ROOT / 'tools/capture_chip_cache_qa.py', e['tool_sha256'])
    copies = read(p / 'final_chip_ko.json')['verified_word_copies']
    require(e['passed'] and c['resets'] == 1 and copies == 7 and c['checks'] == copies + c['hits'], 'reboot library cache mismatch')
    f = m['fixedcell_extension']
    require_hash(ROOT / f['font']['path'], f['font']['sha256'])
    cells = bdf_cells(ROOT / f['font']['path'], set('캐논에어슛발칸'), f['raster'])
    table = {v: bytes.fromhex(k) for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
             if '=' in line for k, v in [line.split('=', 1)] if len(v) == 1}
    pixels = visible_names(p, 12, {0: '캐논', 3: '에어슛', 4: '발칸1'}, cells, source.read_bytes(), table)
    require_hash(ROOT / 'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav', '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    report = {'rom_sha256': build, 'status': 'bounded save/cold-reboot/library regression PASS',
              'routes': routes, 'disk_save': saved, 'reboot_used_checkpoint': False,
              'library_result_sha256': sha((p / 'result.json').read_bytes()), 'cache': c,
              'actual_copies': copies, 'visible_names': pixels,
              'visual_observations': {'entry:10': 'Korean save-screen prompt', 'commit:8': 'Korean saving warning',
                                      'finish:1': 'Korean save completed', 'reboot:8': 'saved Navi selection',
                                      'reboot:11': 'PET return; native New Year greeting'},
              'limits': ['no full save compatibility or error-branch claim', 'native greeting remains Japanese',
                         'changing 56-cell timing and conditional icons pending', 'audio disabled; hardware unverified']}
    (ROOT / 'analysis/exe45_chip_cache_save_v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PASS saved disk -> fresh reboot -> library pixels', saved['sha256'], c)


if __name__ == '__main__':
    main()
