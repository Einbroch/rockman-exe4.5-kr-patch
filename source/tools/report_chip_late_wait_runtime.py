"""Exact-hash bounded late-wait regression; no release or hardware claim."""
import json
from collections import Counter
from build_visibility_poc import ROOT, require_hash, sha
from report_chip_library_runtime import read, require, visible_names, bdf_cells
from report_fixedcell_runtime import verify_route
from report_library_runtime import visible_title

BUILD = '46fba287742b24c132728fbf9d718de9924b93e195a8d49fda986a37ed740fb6'
STEM = 'exe45_ko_development_chip_late_wait_v1'


def main():
    m = read(ROOT / f'poc/output/{STEM}.json')
    for suffix in ('', '_repro'):
        require_hash(ROOT / f'poc/output/{STEM}{suffix}.gba', BUILD)
    source = ROOT / read(ROOT / 'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    native = source.read_bytes()
    f = m['fixedcell_extension']
    require_hash(ROOT / f['font']['path'], f['font']['sha256'])
    cells = bdf_cells(ROOT / f['font']['path'], set('캐논에어슛발칸스탠더드메가기클래모칩'), f['raster'])
    table = {v: bytes.fromhex(k) for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
             if '=' in line for k, v in [line.split('=', 1)] if len(v) == 1}
    seen, routes = set(), {}

    def route(part):
        p = ROOT / f'poc/runtime/chip-late-wait-v1-{part}'
        r = verify_route(p, BUILD, seen)
        require(r['return_code'] == 0 and not list(p.glob('*failed*')), 'route/probe failed')
        routes[part] = sha((p / 'result.json').read_bytes())
        return p, r

    normal, pixels, titles = {}, {}, {}
    for part, steps in [('tabs', {7:{0:'캐논',3:'에어슛',4:'발칸1'},13:{0:'캐논',3:'에어슛',4:'발칸1'}}),
                        ('scroll-reentry', {3:{0:'캐논',3:'에어슛',4:'발칸1'},12:{1:'에어슛',2:'발칸1'},18:{},32:{0:'캐논',3:'에어슛',4:'발칸1'},38:{0:'캐논',3:'에어슛',4:'발칸1'}}),
                        ('reboot-library', {12:{0:'캐논',3:'에어슛',4:'발칸1'}})]:
        p, _ = route(part)
        for filename, tool in [('copy_variant_environment.json','capture_chip_copy_variant_qa.py'),
                               ('late_wait_normal_environment.json','capture_chip_late_wait_qa.py')]:
            e = read(p / filename)
            require(e['passed'] and e['rom_sha256'] == BUILD, 'normal observer failed')
            require_hash(ROOT / 'tools' / tool, e['tool_sha256'])
        c = read(p / 'final_cache.json')
        copies = read(p / 'final_chip_ko.json')['verified_word_copies']
        w = read(p / 'final_late_wait_normal.json')
        require(c['checks'] == c['hits'] + copies and c['resets'] == 1 and copies >= 7, 'cache coverage')
        require(w['wait_next_calls'] == w['normal_waits'] + w['eligible_skips'] and w['normal_waits'] > 0, 'native wait balance')
        normal[part] = {'cache':c, 'copies':copies, 'waits':w}
        pixels[part] = {step:visible_names(p,step,rows,cells,native,table) for step,rows in steps.items()}
        if part == 'tabs':
            for step, phase, text in [(7,4,'스탠더드칩'),(8,16,'메가클래스칩'),(9,28,'기가클래스칩'),(10,40,'P.A메모')]:
                ram = (p / f'step_{step:03d}_gbaExtWorkRam.bin').read_bytes()
                require(ram[0xF971] == phase, 'tab phase identity')
                titles[text] = visible_title(p,step,text,cells,native,table)
    p, _ = route('input-lifetime')
    for step in (4,5):
        v = (p / f'step_{step:03d}_gbaVideoRam.bin').read_bytes()
        require(v[0x8000:0x9000] == native[0x63ABF4:0x63BBF4], 'foreign font overwrite')

    diagnostics = {}
    for part, environment, tool in [('changing56','changing_environment.json','capture_chip_cache_changing.py'),
                                    ('full-icons','full_icons_environment.json','capture_chip_late_wait_full_icons.py')]:
        p, r = route(part)
        require(r.get('normal_play_checkpoint_eligible') is False, 'fixture checkpoint escaped quarantine')
        e = read(p / environment)
        require(e['passed'] and e['cadence_all_one'], 'changing data/cadence failure')
        require_hash(ROOT / 'tools' / tool, e['tool_sha256'])
        d = read(p / 'final_timing.json')
        n = len(d['groups'])
        gaps = dict(Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'],d['groups'][1:])))
        require(n > 100 and gaps == {1:n-1} and len(d['copies']) == 56*n, 'full changing transfer/cadence')
        diagnostics[part] = {'groups':n,'copies':len(d['copies']),'icons':len(d['icons']),'cadence_frames':gaps,'environment':e}

    p, r = route('icon-clear')
    e = read(p / 'icon_clear_environment.json')
    require_hash(ROOT / 'tools/capture_chip_late_wait_icon_clear.py', e['tool_sha256'])
    require(e['passed'] and e['rom_sha256'] == BUILD and r.get('normal_play_checkpoint_eligible') is False, 'icon-clear observer/scope')
    d = read(p / 'final_timing.json')
    n = len(d['groups'])
    require(e['observed'] == {'set_rows':((n+1)//2)*7,'clear_rows':(n//2)*7,'post_updates':n}, 'native map set/clear denominator')
    require(read(p / 'changing_environment.json')['cadence_all_one'], 'icon-clear cadence')
    diagnostics['icon-clear'] = e

    envs, previous = {}, None
    own = (STEM+'.sav', STEM+'.rtc')
    for part in ('entry-cold','commit-cold','finish','reboot'):
        p, r = route('save-'+part)
        e = read(p / 'save_environment.json')
        require(e['build_sha256'] == BUILD, 'foreign save build')
        for name, record in e['files_after'].items():
            require_hash(p / 'persistent_files_after' / name, record['sha256'])
        for name, record in e['files_before'].items():
            if name not in own:
                require(e['files_after'][name] == record, 'unrelated save changed')
        if previous is not None:
            require(e['files_before'] == envs[previous]['files_after'], 'save disk chain interrupted')
        if part == 'reboot':
            require(r['state_origin'] is None and not (p / 'input.mss').exists(), 'reboot not cold')
        envs[part], previous = e, part
    saved = envs['finish']['files_after'][own[0]]
    require(saved['bytes'] == 65536 and saved != envs['entry-cold']['files_before'][own[0]], 'no new disk save')
    require(saved == envs['reboot']['files_before'][own[0]] == envs['reboot']['files_after'][own[0]], 'cold reboot save identity')
    p, _ = route('saved-checkpoint-return')
    e = read(p / 'save_environment.json')
    require(e['files_after'][own[0]] == saved, 'verified saved checkpoint did not restore test persistence')
    for name, record in e['files_before'].items():
        if name not in own:
            require(e['files_after'][name] == record, 'unrelated persistence changed on return')
    require_hash(p / 'persistent_files_after' / own[0], saved['sha256'])
    require_hash(ROOT / 'poc/runtime/chip-matrix-saves' / own[0], saved['sha256'])
    require_hash(ROOT / 'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav', '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    report = {'rom_sha256':BUILD,'status':'PASS bounded muted-Mesen standard-library late-wait regression; not release QA',
              'reproducible':True,'routes':routes,'normal':normal,'visible_names':pixels,'titles':titles,
              'foreign_overwrite_steps':[4,5],'diagnostics':diagnostics,'disk_save':saved,
              'guard_tab_phases':{'standard':4,'mega':16,'giga':28,'PA':40},
              'excluded_attempts':{'save-entry':'nickname screen, not save confirmation','save-commit':'nickname screen, not save commit'},
              'visual_observations':{'save-entry-cold:11':'Korean save confirmation','save-commit-cold:7':'Korean save-completed message'},
              'test_persistence_return':'Cold diagnostic checkpoint rolled back isolated scratch SRAM; returned using validated same-ROM saved checkpoint, not manual SRAM editing',
              'limits':['72 draft units only; full translation incomplete','icon RAM-map checks are not a scanout tearing proof',
                        'audio disabled; no hardware timing or listening claim','no full save/error-branch compatibility claim']}
    out = ROOT / 'analysis/exe45_chip_late_wait_runtime_v2.json'
    require(not out.exists(), 'refuse report overwrite')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS exact ROM, tabs, scroll/reentry, foreign overwrite, changing full icons, disk save/cold reboot', saved['sha256'])


if __name__ == '__main__':
    main()
