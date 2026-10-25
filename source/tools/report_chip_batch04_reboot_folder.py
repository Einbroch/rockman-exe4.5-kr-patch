"""Same-ROM native save reboot to Korean folder, bounded normal play."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require,bdf_cells
from report_fixedcell_runtime import verify_route
from report_chip_mono_cannon_runtime import mono_sentence
from report_chip_folder_pixels import visible_folder
from tpl_literals import resolve_units


def main():
    rom=ROOT/'poc/output/exe45_ko_development_chip_batch04_v1.gba';m=read(rom.with_suffix('.json'));build=m['output_sha256'];require_hash(rom,build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    asset=ROOT/'translations/chip_descriptions_batch04_ko.json';require_hash(asset,next(a['sha256'] for a in m['translation_assets'] if a['archive']=='76937C'))
    texts={int(u['id'].split(':')[1]):u['translation'] for u in resolve_units(read(asset))}
    p=ROOT/'poc/runtime/chip-batch04-v1-reboot-folder';r=verify_route(p,build,set());env=read(p/'folder_qa_environment.json')
    require(r['return_code']==0 and env['passed'],'reboot folder faults')
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    records={step:mono_sentence(p,step,m,native,table,texts[1],1,rom) for step in (15,16)}
    font=m['fixedcell_extension'];cells=bdf_cells(ROOT/font['font']['path'],set('캐논에어슛발칸'),font['raster'])
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    names={step:visible_folder(p,step,rows,cells,native,table) for step in (15,16)}
    e=read(p/'probe_environment.json');key='exe45_ko_development_chip_batch04_v1.sav'
    require(e['files_before'][key]==e['files_after'][key] and e['files_after'][key]['sha256']=='0619f62e766994fb66b231336417961a6453391393f0ba94776dbd74fb5ac59f','own reboot save preservation')
    require(all(e['files_after'].get(k)==v for k,v in e['files_before'].items() if k.endswith('.sav')),'other save mutation')
    out=ROOT/'analysis/exe45_chip_batch04_reboot_folder_v1.json';require(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'status':'PASS native saved-game Korean folder reentry','rom_sha256':build,'result_sha256':sha((p/'result.json').read_bytes()),'descriptions':records,'names':names,'saved_data_unchanged':True,'limits':['Normal saved-game Cannon only; not120normally acquired chips.','Step14 was not a description frame and is not credited; first reporter geometry assumption failed closed.','Foreign-font/input lifetime, maximum-workload timing and full-game review remain pending.']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS saved-game folder Korean names/descriptions and SAV preservation')


if __name__=='__main__':main()
