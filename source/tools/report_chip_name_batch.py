"""Bind 30-name draft to protected source, CPU and scoped runtime evidence."""
import json
from build_visibility_poc import ROOT, sha, require_hash
from chip_library_extension import compile_clone
from report_chip_library_runtime import read, require, visible_names, bdf_cells
from report_fixedcell_runtime import verify_route


def main():
    build = '16afa15fb530f1aded001691767f39fecb44394fab0e20760eeedd9408833241'
    stem = 'exe45_ko_development_chip_names_batch01_v1'
    m = read(ROOT / f'poc/output/{stem}.json')
    for suffix in ('','_repro'):
        require_hash(ROOT / f'poc/output/{stem}{suffix}.gba',build)
    source_path = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source_path,m['source_sha256'])
    native = source_path.read_bytes()
    asset_path = ROOT / 'translations/library_chip_names_batch01_ko.json'
    asset = read(asset_path)
    selected_asset = next(a for a in m['translation_assets'] if a['path'] == str(asset_path.relative_to(ROOT)))
    require_hash(asset_path,selected_asset['sha256'])
    table = {int(k,16):v for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
             if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    clone, record = compile_clone(native,read(ROOT / 'tools/specs/exe45_chip_library_v1.json'),asset,table)
    e = m['chip_library_extension']
    rom = (ROOT / f'poc/output/{stem}.gba').read_bytes()
    require(rom[e['clone_offset']:e['clone_offset']+len(clone)] == clone, 'final clone mismatch')
    require(m['translated_units'] == 99 and len(record['units']) == 30 and len(record['unselected_scripts']) == 226, 'draft denominator')
    cpu = read(ROOT / 'analysis/exe45_chip_names_batch01_cpu_v1.json')
    wait = read(ROOT / 'analysis/exe45_chip_names_batch01_wait_cpu_v1.json')
    require(cpu['rom_sha256'] == wait['rom_sha256'] == build and cpu['vectors'] == 34054 and wait['vectors'] == 288, 'CPU identity/count')
    f = m['fixedcell_extension']
    require_hash(ROOT / f['font']['path'],f['font']['sha256'])
    names = {u['script']:u['text'] for u in record['units']}
    cells = bdf_cells(ROOT / f['font']['path'],{c for text in names.values() for c in text if '\uac00'<=c<='\ud7a3'},f['raster'])
    byte_table = {v:bytes([k]) for k,v in table.items()}
    seen, routes, pixels = set(), {}, {}
    p = ROOT / 'poc/runtime/chip-names-batch01-v1-tabs'
    r = verify_route(p,build,seen)
    require(r['return_code'] == 0,'normal route failed')
    for filename in ('cache_environment.json','copy_variant_environment.json','late_wait_normal_environment.json'):
        require(read(p / filename)['passed'],'normal observer failed')
    for step in (7,13):
        pixels[f'normal:{step}'] = visible_names(p,step,{0:'캐논',3:'에어슛',4:'발칸1'},cells,native,byte_table)
    routes['normal'] = sha((p / 'result.json').read_bytes())
    for part in ('all30','all30-stable'):
        p = ROOT / f'poc/runtime/chip-names-batch01-v1-{part}'
        r = verify_route(p,build,seen)
        b = read(p / 'batch_environment.json')
        require_hash(ROOT / 'tools/capture_chip_names_batch.py',b['tool_sha256'])
        require(r['return_code'] == 0 and r.get('normal_play_checkpoint_eligible') is False and b['passed'], 'batch scope/failure')
        require(b['covered_scripts'] == list(range(1,31)), 'missing compiled name')
        if part == 'all30-stable':
            s = read(p / 'stable_batch_environment.json')
            require_hash(ROOT / 'tools/capture_chip_names_batch_stable.py',s['adapter_sha256'])
            require(s['hold_updates'] == 30,'page hold identity')
            for step in (7,8):
                epoch = read(p / f'step_{step:03d}_batch.json')['epochs']
                start = ((epoch-1)//30)*7
                expected = {row:names[(start+row)%30+1] for row in range(7)}
                pixels[f'held:{step}'] = visible_names(p,step,expected,cells,native,byte_table)
        routes[part] = {'result_sha256':sha((p / 'result.json').read_bytes()),'environment':b}
    out = ROOT / 'analysis/exe45_chip_names_batch01_runtime_v1.json'
    require(not out.exists(),'refuse report overwrite')
    report = {'rom_sha256':build,'status':'PASS bounded 30-name development clone; NON-DISTRIBUTION',
              'draft_units':99,'chip_name_units':30,'new_chip_name_units':27,'unselected_name_scripts':226,
              'source_rechecked':True,'reproducible':True,'routes':routes,'visible_pixel_masks':pixels,
              'cpu_vectors':cpu['vectors'],'wait_vectors':wait['vectors'],
              'limits':['all new wording needs independent/human review','diagnostic acquisition is bypassed; not 30 acquired normal-play claims',
                        'rapid fixture screenshot is not current-VRAM scanout proof; held-page samples are independently checked',
                        'other chip-name consumers and mono descriptions remain native','no full-game, audio or hardware QA claim']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS 30 protected names, 226 native scripts, actual clone runtime, held-page glyph/screenshot masks')


if __name__ == '__main__':
    main()
