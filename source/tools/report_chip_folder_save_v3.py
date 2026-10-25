"""Bind v3 native save/cold reboot and subsequent folder pixels."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells
from report_chip_folder_pixels import visible_folder


def main():
    stem='exe45_ko_development_chip_folder_v3'
    m=read(ROOT/f'poc/output/{stem}.json');build=m['output_sha256']
    require_hash(ROOT/f'poc/output/{stem}.gba',build)
    require_hash(ROOT/f'poc/output/{stem}_repro.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename']
    require_hash(source,m['source_sha256']);native=source.read_bytes()
    own=(stem+'.sav',stem+'.rtc');environments={};previous=None;seen=set()
    for part in ('enter','commit','finish','reboot'):
        p=ROOT/f'poc/runtime/chip-folder-v3-save-{part}'
        r=verify_route(p,build,seen)
        require(r['return_code']==0 and not list(p.glob('*failed*')),'save route fault')
        e=read(p/'save_environment.json')
        require(e['build_sha256']==build,'save build identity')
        for name,record in e['files_after'].items():
            require_hash(p/'persistent_files_after'/name,record['sha256'])
        for name,record in e['files_before'].items():
            if name not in own:
                require(e['files_after'][name]==record,'unrelated save changed')
        if previous:
            require(e['files_before']==environments[previous]['files_after'],'disk chain interrupted')
        if part=='reboot':
            require(r['state_origin'] is None and not (p/'input.mss').exists(),'reboot used state')
        environments[part]=e;previous=part
    saved=environments['finish']['files_after'][own[0]]
    require(saved['bytes']==65536 and saved!=environments['enter']['files_before'][own[0]],'new save absent')
    require(saved==environments['reboot']['files_before'][own[0]]==environments['reboot']['files_after'][own[0]],'reboot disk identity')
    require_hash(ROOT/'poc/runtime/chip-matrix-saves'/own[0],saved['sha256'])
    require_hash(ROOT/'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav','99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    p=ROOT/'poc/runtime/chip-folder-v3-reboot-folder-r2'
    r=verify_route(p,build,seen);require(r['return_code']==0,'reboot folder fault')
    require(read(p/'folder_qa_environment.json')['passed'],'folder ABI observer')
    f=m['fixedcell_extension'];cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    pixels={step:visible_folder(p,step,rows,cells,native,table) for step in (15,16)}
    out=ROOT/'analysis/exe45_chip_folder_save_v3.json';require(not out.exists(),'refuse report overwrite')
    report={'rom_sha256':build,'status':'PASS bounded save/cold reboot/folder reentry',
        'disk_save':saved,'save_routes':{k:sha((ROOT/f'poc/runtime/chip-folder-v3-save-{k}/result.json').read_bytes()) for k in environments},
        'folder_pixels':pixels,'visual_observations':{'enter:11':'Korean save confirmation','commit:7':'Korean save completed'},
        'excluded_attempts':{'reboot-folder':'New Year greeting intercepted input; equipment cursor, no folder positive evidence',
                             'reboot-folder-r1':'incomplete predecessor rejected before execution'},
        'limits':['normal New Year dialogue remains Japanese','not all save/error branches or complete game QA','99 draft units; NON-DISTRIBUTION']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS native disk save/cold reboot/folder pixels:',saved['sha256'])


if __name__=='__main__':
    main()
