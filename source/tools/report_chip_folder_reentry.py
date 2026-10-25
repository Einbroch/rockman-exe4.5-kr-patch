"""Exact folder-v2 foreign-font overwrite -> init reset -> visible names."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_folder_pixels import visible_folder
from report_chip_library_runtime import read,require,bdf_cells,visible_names
from report_fixedcell_runtime import verify_route


def main():
    build='6790782b403f07f5f850cb985e6aedf012dc8334736b4f9988e4f74379a6fd41'
    m=read(ROOT/'poc/output/exe45_ko_development_chip_folder_v2.json')
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename']
    require_hash(source,m['source_sha256']);native=source.read_bytes()
    f=m['fixedcell_extension']
    cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    routes={};seen=set()
    for part in ('library-tabs','input-lifetime','foreign-reentry'):
        p=ROOT/f'poc/runtime/chip-folder-v2-{part}'
        r=verify_route(p,build,seen)
        require(r['return_code']==0 and not list(p.glob('*failed*')),'reentry route fault')
        routes[part]=sha((p/'result.json').read_bytes())
    p=ROOT/'poc/runtime/chip-folder-v2-library-tabs'
    library_pixels={step:visible_names(p,step,{0:'캐논',3:'에어슛',4:'발칸1'},cells,native,{v:bytes([k]) for k,v in table.items()}) for step in (7,13)}
    p=ROOT/'poc/runtime/chip-folder-v2-input-lifetime'
    for step in (4,5):
        v=(p/f'step_{step:03d}_gbaVideoRam.bin').read_bytes()
        require(v[0x8000:0x9000]==native[0x63ABF4:0x63BBF4],'foreign font not reclaimed')
        require(any(v[0x8E40:0x8EB0]),'foreign tag range has no positive content')
    p=ROOT/'poc/runtime/chip-folder-v2-foreign-reentry'
    e=read(p/'folder_qa_environment.json')
    require_hash(ROOT/'tools/capture_chip_folder_qa.py',e['tool_sha256']);require(e['passed'],'folder reentry probe failed')
    c=read(p/'final_folder_cache.json')
    copies=read(p/'final_chip_ko.json')['verified_word_copies']
    require(c['resets']==1 and copies==17 and c['checks']==c['hits']+copies,'foreign reset/recopy count')
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    pixels={step:visible_folder(p,step,rows,cells,native,table) for step in (6,7,10)}
    out=ROOT/'analysis/exe45_chip_folder_reentry_v2.json'
    require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded folder/library/input/reentry; full changing timing and new-ROM save QA pending',
        'routes':routes,'library_pixels':library_pixels,'foreign_overwrite_steps':[4,5],
        'folder_pixels':pixels,'cache':c,'actual_copies':copies,
        'limits':['no other exit-route/full-game or audio/hardware claim','guard is source function/count/buffer/base/root; no explicit job/menu guard in v2']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS foreign bank overwrite, folder reset+17 real copies, library and folder screenshot pixels')


if __name__=='__main__':
    main()
