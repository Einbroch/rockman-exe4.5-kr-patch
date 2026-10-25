"""Reconcile exact251-unit build evidence; development only, no release gate."""
import json
from build_visibility_poc import ROOT, sha, require_hash
from report_chip_library_runtime import read, require


def main():
    stem = 'exe45_ko_development_tactics_prompts_v1'
    rom = ROOT/f'poc/output/{stem}.gba'; m = read(rom.with_suffix('.json'))
    build = m['output_sha256']; require_hash(rom, build)
    repro = ROOT/f'poc/output/{stem}_repro.gba'; require_hash(repro, build)
    require(rom.read_bytes()==repro.read_bytes(), 'rebuild byte comparison')
    source = ROOT/read(ROOT/'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256'])
    survey = ROOT/'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav'
    require_hash(survey, '99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    report_names = ['exe45_tactics_prompt_parser_cpu_v1.json','exe45_tactics_target_runtime_v1.json','exe45_tactics_distance_runtime_v1.json','exe45_tactics_description_regression_v1.json','exe45_tactics_battle_names_regression_v1.json']
    records = []
    for name in report_names:
        p = ROOT/'analysis'/name; r = read(p)
        require(r['rom_sha256']==build and r['status'].startswith('PASS'), 'unbound or failed evidence:'+name)
        records.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'status':r['status']})
    row = next(r for r in m['archives'] if r['archive']=='76C944')
    require(row['translated_units']==2 and len(row['unselected_script_bytes_preserved'])==142, 'prompt scope preservation')
    require(all(row[k] for k in ['native_roundtrip','semantic_roundtrip','binary_roundtrip','protected_controls_unchanged']), 'prompt roundtrip')
    route = ROOT/'poc/runtime/tactics-prompts-v1-native-reboot'
    env = read(route/'save_environment.json'); result = read(route/'result.json')
    require(env['build_sha256']==build and result['complete'] and result['return_code']==0, 'native reboot result')
    require(result.get('state_origin') is None, 'reboot loaded a state')
    before, after = env['files_before'],env['files_after']; key = stem+'.sav'
    require(before[key]==after[key] and before[key]['sha256']=='0619f62e766994fb66b231336417961a6453391393f0ba94776dbd74fb5ac59f', 'own native save reboot drift')
    require(all(after.get(k)==v for k,v in before.items() if k.endswith('.sav')), 'existing save mutation')
    out = ROOT/'analysis/exe45_tactics_prompts_milestone_v1.json'; require(not out.exists(), 'refuse overwrite')
    out.write_text(json.dumps({'status':'PASS bounded251-draft development milestone; NON-DISTRIBUTION','rom_sha256':build,'source_sha256':m['source_sha256'],'bytes':rom.stat().st_size,'repro_byte_identical':True,'prompt_scripts':[0,1],'unselected_prompt_scripts_preserved':142,'evidence':records,'native_reboot':{'state_loaded':False,'own_save':before[key],'all_existing_sav_preserved':True,'result_sha256':sha((route/'result.json').read_bytes())},'limits':['All251 drafts need wording/presentation review.','This build has not repeated prior90-script exhaustive diagnostics; do not inherit old-ROM evidence.','New candidate full folder/library timing and save-commit cycles remain pending.','Other Navi prompts, escape messages, most game scripts and text graphics remain native.','No muted-emulator evidence constitutes audio, hardware, full-game or release approval.']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS exact251-unit bounded milestone; original and native SAV preserved')


if __name__=='__main__':
    main()
