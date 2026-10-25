"""New-ROM mono sentence plus big names/titles and foreign-font reentry."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells,visible_names
from report_library_runtime import visible_title
from report_chip_folder_pixels import visible_folder
from report_chip_mono_cannon_runtime import mono_sentence
from tpl_literals import resolve_units


def main():
    m=read(ROOT/'poc/output/exe45_ko_development_chip_mono_cannon_v2.json');build=m['output_sha256']
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    require_hash(ROOT/'poc/output/exe45_ko_development_chip_mono_cannon_v2.gba',build)
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    f=m['fixedcell_extension'];wanted=set('캐논에어슛발칸스탠더드칩메가클래스기가메모')
    cells=bdf_cells(ROOT/f['font']['path'],wanted,f['raster']);byte_table={v:bytes([k]) for k,v in table.items()}
    routes={};seen=set()
    for part in ('library-tabs','input-lifetime','foreign-reentry'):
        p=ROOT/f'poc/runtime/chip-mono-cannon-v2-{part}';r=verify_route(p,build,seen)
        require(r['return_code']==0 and not list(p.glob('*failed*')),'mono regression route fault')
        routes[part]=sha((p/'result.json').read_bytes())
    text=resolve_units(read(ROOT/'translations/chip_descriptions_cannon_poc_ko.json'))[0]['translation']
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-library-tabs';library={};titles={};sentences={}
    for filename in ('cache_environment.json','copy_variant_environment.json','late_wait_normal_environment.json'):
        require(read(p/filename)['passed'],'library cache/copy/wait observer failure')
    for step in (7,13):
        library[step]=visible_names(p,step,{0:'캐논',3:'에어슛',4:'발칸1'},cells,native,byte_table)
        sentences[f'library:{step}']=mono_sentence(p,step,m,native,table,text)
    for step,phase,title in ((7,4,'스탠더드칩'),(8,16,'메가클래스칩'),(9,28,'기가클래스칩'),(10,40,'P.A메모')):
        ram=(p/f'step_{step:03d}_gbaExtWorkRam.bin').read_bytes();require(ram[0xF971]==phase,'tab identity')
        titles[title]=visible_title(p,step,title,cells,native,byte_table)
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-input-lifetime'
    for step in (4,5):
        v=(p/f'step_{step:03d}_gbaVideoRam.bin').read_bytes()
        require(v[0x8000:0x9000]==native[0x63ABF4:0x63BBF4] and any(v[0x8E40:0x8EB0]),'foreign font/tag overwrite absent')
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-foreign-reentry';c=read(p/'final_folder_cache.json')
    copies=read(p/'final_chip_ko.json')['verified_word_copies']
    require(read(p/'folder_qa_environment.json')['passed'] and c['resets']==1 and copies==17 and c['checks']==c['hits']+copies,'folder recopy/reset denominator')
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'};folder={}
    for step in (6,7,10):
        folder[step]=visible_folder(p,step,rows,cells,native,table)
        sentences[f'folder:{step}']=mono_sentence(p,step,m,native,table,text)
    out=ROOT/'analysis/exe45_chip_mono_regressions_v2.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded mono/big titles/names/foreign overwrite/reentry',
        'routes':routes,'library_names':library,'titles':titles,'folder_names':folder,'mono_sentences':sentences,
        'cache':c,'actual_copies':copies,'limits':['Cannon normal sentence only; other shared consumers and script2/3 pending',
        'new-ROM maximum timing/save closure requires separate reports','102 draft units, not complete translation or release QA']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS new-ROM mono sentence, 4 big titles, chip names, foreign-font reentry pixels')


if __name__=='__main__': main()
