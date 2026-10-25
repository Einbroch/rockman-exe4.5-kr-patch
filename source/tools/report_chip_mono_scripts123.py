"""Diagnostic actual compiled script1/2/3 consumption, never acquisition proof."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require
from report_chip_mono_cannon_runtime import mono_sentence
from tpl_literals import resolve_units


def main():
    m=read(ROOT/'poc/output/exe45_ko_development_chip_mono_cannon_v2.json');build=m['output_sha256']
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-scripts123';r=verify_route(p,build,set());e=read(p/'mono_script_environment.json')
    require_hash(ROOT/'tools/capture_chip_mono_cannon_scripts.py',e['tool_sha256'])
    require(r['return_code']==0 and r.get('normal_play_checkpoint_eligible') is False and e['passed'] and e['covered_scripts']==[1,2,3] and e['lookup_reads']==3,'mono diagnostic scope/count')
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    units=resolve_units(read(ROOT/'translations/chip_descriptions_cannon_poc_ko.json'))
    texts={int(u['id'].split(':')[1]):u['translation'] for u in units}
    pixels={step:mono_sentence(p,step,m,native,table,texts[script],script) for step,script in ((15,1),(17,2),(19,3),(20,3))}
    out=ROOT/'analysis/exe45_chip_mono_scripts123_v2.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS diagnostic actual script1/2/3 Korean stage/OBJ/pixels; NON-DISTRIBUTION',
        'result_sha256':sha((p/'result.json').read_bytes()),'environment':e,'pixels':pixels,
        'limits':['script-table CPU read substitution; no HiCannon/MegaCannon acquired normal-play claim',
                  'not other shared pointer consumers or full-game/audio/hardware release QA']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS actual compiled mono scripts1/2/3 and independent screenshot pixels')


if __name__=='__main__': main()
