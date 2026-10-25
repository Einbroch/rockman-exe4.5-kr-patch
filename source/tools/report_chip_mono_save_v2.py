"""v2 exact-ROM normal disk-save/reboot and restored mono sentence pixels."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require
from report_chip_mono_cannon_runtime import mono_sentence
from tpl_literals import resolve_units


def main():
    stem='exe45_ko_development_chip_mono_cannon_v2';m=read(ROOT/f'poc/output/{stem}.json');build=m['output_sha256']
    require_hash(ROOT/f'poc/output/{stem}.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    own=(stem+'.sav',stem+'.rtc');envs={};previous=None;seen=set()
    for part in ('enter','commit','finish','reboot'):
        p=ROOT/f'poc/runtime/chip-mono-cannon-v2-save-{part}';r=verify_route(p,build,seen)
        require(r['return_code']==0 and not list(p.glob('*failed*')),'mono save route fault')
        e=read(p/'save_environment.json');require(e['build_sha256']==build,'save build identity')
        for name,record in e['files_after'].items(): require_hash(p/'persistent_files_after'/name,record['sha256'])
        for name,record in e['files_before'].items():
            if name not in own: require(e['files_after'][name]==record,'unrelated save changed')
        if previous: require(e['files_before']==envs[previous]['files_after'],'save disk chain interrupted')
        if part=='reboot': require(r['state_origin'] is None and not (p/'input.mss').exists(),'reboot used state')
        envs[part]=e;previous=part
    saved=envs['finish']['files_after'][own[0]]
    require(saved['bytes']==65536 and saved!=envs['enter']['files_before'][own[0]],'new save absent')
    require(saved==envs['reboot']['files_before'][own[0]]==envs['reboot']['files_after'][own[0]],'cold reboot disk identity')
    require_hash(ROOT/'poc/runtime/chip-matrix-saves'/own[0],saved['sha256'])
    require_hash(ROOT/'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav','99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-reboot-folder';r=verify_route(p,build,seen)
    require(r['return_code']==0 and read(p/'folder_qa_environment.json')['passed'],'saved folder observer failure')
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    text=resolve_units(read(ROOT/'translations/chip_descriptions_cannon_poc_ko.json'))[0]['translation']
    pixels={step:mono_sentence(p,step,m,native,table,text) for step in (15,16)}
    out=ROOT/'analysis/exe45_chip_mono_save_v2.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded native disk-save/cold-reboot/Korean mono redisplay',
        'disk_save':saved,'save_routes':{k:sha((ROOT/f'poc/runtime/chip-mono-cannon-v2-save-{k}/result.json').read_bytes()) for k in envs},
        'restored_sentence_pixels':pixels,'visual_observations':{'enter:11':'Korean save confirmation','commit:7':'Korean save completed'},
        'limits':['not all save/error branches','native New Year greeting remains Japanese','102 drafts; not complete-game release QA']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS mono native disk-save, cold reboot and restored Korean sentence:',saved['sha256'])


if __name__=='__main__': main()
