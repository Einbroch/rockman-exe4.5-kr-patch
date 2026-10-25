"""Exact744-unit ROM: secondary name working-set and descriptions pixels."""
import json
import struct
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require,bdf_cells
from tpl_literals import resolve_units
from archive_scripts import verify_untouched_scripts
from report_fixedcell_runtime import verify_route
from report_chip_folder_pixels import visible_folder
from report_secondary_chip_descriptions import secondary_sentence

def prepare():
    stem='exe45_ko_development_chip_secondary_names_v1';rom_path=ROOT/f'poc/output/{stem}.gba';m=read(rom_path.with_suffix('.json'));build=m['output_sha256']
    require(m['translated_units']==744 and m['final_diff_audited'] and m['header_unchanged'],'cumulative744')
    for suffix in ('','_repro'):require_hash(ROOT/f'poc/output/{stem}{suffix}.gba',build)
    rom=rom_path.read_bytes();source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    name_asset=read(ROOT/'translations/chip_secondary_names_ko.json');names={int(u['id'].split(':')[1]):u['translation'] for u in resolve_units(name_asset)}
    require(len(names)==98 and rom[0x765B18:0x765B18+1103]==native[0x765B18:0x765B18+1103],'source name pool preserved')
    for key in ('chip_library_extension','chip_folder_extension'):
        e=m[key];record=e['secondary_clone'];at=e['secondary_clone_offset']
        require(len(record['units'])==98 and len(record['unselected_scripts'])==39,'98 translated39 native slots')
        require(len(verify_untouched_scripts(native[0x765B18:0x765B18+1103],rom[at:at+record['clone_bytes']],137,set(names)))==39,'unselected payload preservation')
    require(m['chip_battle_name_extension']['selected_scripts']==list(range(1,195))+list(range(201,256)),'battle primary scope unchanged')
    p=ROOT/'poc/runtime/chip-secondary-names-v1-folder-samples';seen=set();route=verify_route(p,build,seen)
    e=read(p/'secondary_environment.json');require(e['passed'] and read(p/'folder_qa_environment.json')['passed'] and route['normal_play_checkpoint_eligible'] is False,'diagnostic folder environment')
    require_hash(ROOT/'tools/capture_secondary_names_folder.py',e['tool_sha256'])
    ids=[0,1,7,16,22,29,88];rows={row:names[i] for row,i in enumerate(ids)}
    f=m['fixedcell_extension'];cells=bdf_cells(ROOT/f['font']['path'],{ch for s in rows.values() for ch in s if '\uac00'<=ch<='\ud7a3'},f['raster'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    name_pixels={str(step):visible_folder(p,step,rows,cells,native,table) for step in route['capture_steps']}
    texts={int(u['id'].split(':')[1]):u['translation'] for u in resolve_units(read(ROOT/'translations/chip_secondary_descriptions_ko.json'))}
    ar=next(a for a in m['archives'] if a['archive']=='76BC60');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    offsets={struct.unpack_from('<H',payload,i*2)[0]:i for i in ids};sentences={};covered=set()
    for step in route['capture_steps']:
        calls=[c for c in read(p/f'step_{step:03d}_fixedcells.json')['calls'] if c['font']==0x08619EF8]
        i=offsets[calls[-1]['stream']-0x08000000-ar['rom_offset']]
        sentences[str(step)]=secondary_sentence(p,step,m,native,table,texts[i],i,rom_path);covered.add(i)
    require(covered==set(ids),'secondary name/description sample coverage')
    normal=ROOT/'poc/runtime/chip-secondary-names-v1-normal-scroll';nr=verify_route(normal,build,seen);require(read(normal/'folder_qa_environment.json')['passed'],'primary regression')
    normal_rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    normal_cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    primary_pixels={str(step):visible_folder(normal,step,normal_rows,normal_cells,native,table) for step in nr['capture_steps']}
    cpu={}
    for consumer in ('library','folder'):
        r=read(ROOT/f'analysis/exe45_secondary_names_{consumer}_cpu_v1.json');require(r['rom_sha256']==build and r['register_memory_tile_checks'],'selector CPU binding');cpu[consumer]=r['vectors']
    saves={}
    for directory in seen:
        env=read(directory/'probe_environment.json')
        for filename,before in env['files_before'].items():
            if filename not in (stem+'.sav',stem+'.rtc'):require(env['files_after'].get(filename)==before,'foreign save changed')
        saves[str(directory.relative_to(ROOT))]={'own_save':env['files_after'].get(stem+'.sav'),'own_rtc':env['files_after'].get(stem+'.rtc'),'other_saves_preserved':True}
    return {'rom_sha256':build,'policy':'development-draft; NON-DISTRIBUTION','status':'PASS bounded secondary folder name/description development build','translated_units':744,'secondary_name_units':98,'native_slots_preserved':39,'sample_scripts':ids,'name_pixels':name_pixels,'secondary_description_pixels':sentences,'primary_name_regression':primary_pixels,'cpu_vectors':cpu,'reproducible':True,'saves':saves,
            'limits':['diagnostic source IDs not normal-play acquired chips','7-of98 secondary name screenshot samples; full selector CPU coverage not full runtime population coverage','library selector CPU checked, new-ROM library screen/reentry pending','secondary battle names and other name consumers still native','remaining dialogue/UI/graphics, human meaning/presentation approval, timing/lifetime, save-commit/reboot, full-game/audio/hardware/release pending']}

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
