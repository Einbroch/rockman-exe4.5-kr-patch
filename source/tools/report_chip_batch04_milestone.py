"""Bind311-unit development evidence without inheriting old-ROM QA."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from tpl_literals import resolve_units
from archive_scripts import verify_untouched_scripts


def main():
    stem='exe45_ko_development_chip_batch04_v1';rom=ROOT/f'poc/output/{stem}.gba'
    m=read(rom.with_suffix('.json'));build=m['output_sha256'];require_hash(rom,build)
    repro=ROOT/f'poc/output/{stem}_repro.gba';require_hash(repro,build)
    require(rom.read_bytes()==repro.read_bytes(),'repro bytes')
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes();blob=rom.read_bytes()
    require(m['translated_units']==311,'draft denominator')
    for base in ('library_chip_names','chip_descriptions'):
        current=resolve_units(read(ROOT/f'translations/{base}_batch04_ko.json'))
        prior=resolve_units(read(ROOT/f'translations/{base}_batch03_ko.json'))
        require(len(current)==120 and current[:90]==prior,'prior90 altered')
        require(all(u['state']=='needs_review' for u in current),'review state drift')
    desc=next(r for r in m['archives'] if r['archive']=='76937C')
    preserved=verify_untouched_scripts(native[0x76937C:0x76937C+10467],blob[desc['rom_offset']:desc['rom_offset']+desc['compiled_bytes']],256,set(range(1,121)))
    require(len(preserved)==136,'unselected description denominator')
    prompt=next(r for r in m['archives'] if r['archive']=='76C944')
    require(len(prompt['unselected_script_bytes_preserved'])==142,'unselected prompt denominator')
    names=['exe45_chip_batch04_mono_provider_cpu_v1.json','exe45_chip_batch04_folder_cpu_v1.json','exe45_chip_batch04_library_cpu_v1.json','exe45_chip_batch04_description_parser_cpu_v1.json','exe45_chip_batch04_name_parser_cpu_v1.json','exe45_chip_batch04_battle_helper_cpu_v1_r2.json','exe45_chip_batch04_runtime_v1.json','exe45_chip_folder_names_batch04_v1.json']
    evidence=[]
    for name in names:
        p=ROOT/'analysis'/name;r=read(p)
        identity=r.get('rom_sha256',r.get('build_sha256'))
        require(identity==build,'evidence ROM binding:'+name)
        require(r.get('status','').startswith('PASS') or r.get('register_memory_tile_checks') is True,'failed evidence:'+name)
        evidence.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'status':r.get('status'),'vectors':r.get('vectors')})
    survey=ROOT/'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav'
    require_hash(survey,'99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    out=ROOT/'analysis/exe45_chip_batch04_milestone_v1.json';require(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'status':'PASS bounded311-draft technical milestone; NON-DISTRIBUTION','rom_sha256':build,'source_sha256':m['source_sha256'],'repro_byte_identical':True,'draft_units':311,'new_chip_name_units':30,'new_description_units':30,'prior90_names_and_descriptions_verbatim':True,'unselected_description_scripts':136,'unselected_prompt_scripts':142,'evidence':evidence,'limits':['All draft wording, terminology and presentation need human review.','Diagnostic120 source-table/descriptor aliases do not prove normal acquisition or battle coverage.','New-ROM exhaustive battle labels, TACTICS prompts, input lifetime, save and maximum-workload timing regressions still pending.','Other name consumers, most dialog and graphics are still native; not whole-game/audio/hardware/release QA.']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS exact311-draft bounded milestone; no old-ROM QA inherited')


if __name__=='__main__':main()
