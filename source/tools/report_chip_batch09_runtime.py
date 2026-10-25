"""Exact571-unit build: normal folder pixels + diagnostic17 description pixels."""
import json
import struct
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require,bdf_cells
from report_fixedcell_runtime import verify_route
from report_chip_mono_cannon_runtime import mono_sentence
from report_chip_folder_pixels import visible_folder
from tpl_literals import resolve_units
from archive_scripts import verify_untouched_scripts
from capture_chip_batch09_samples import SCRIPTS

def prepare():
    stem='exe45_ko_development_chip_batch09_v1';rom_path=ROOT/f'poc/output/{stem}.gba'
    m=read(rom_path.with_suffix('.json'));build=m['output_sha256'];require(m['translated_units']==571,'selected571')
    require_hash(rom_path,build);require_hash(ROOT/f'poc/output/{stem}_repro.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes();rom=rom_path.read_bytes()
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    require(m['final_diff_audited'] and m['header_unchanged'],'final changes/header')
    a=read(ROOT/'translations/chip_descriptions_batch09_ko.json');units=resolve_units(a)
    texts={int(x['id'].split(':')[1]):x['translation'] for x in units}
    require(len(texts)==251,'description denominator')
    ar=next(x for x in m['archives'] if x['archive']=='76937C')
    payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    require(len(verify_untouched_scripts(native[0x76937C:0x76937C+10467],payload,256,set(texts)))==5,'native descriptions')
    for ptr in ar['pointers']:require(struct.unpack_from('<I',rom,ptr)[0]==0x08000000+ar['rom_offset'],'description relocation')
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    seen=set();normal=ROOT/'poc/runtime/chip-batch09-v1-normal-scroll'
    route=verify_route(normal,build,seen);require(route['return_code']==0 and read(normal/'folder_qa_environment.json')['passed'],'normal consumer fault')
    sentences={str(step):mono_sentence(normal,step,m,native,table,texts[script],script,rom_path) for step,script in ((9,1),(12,4),(15,15),(16,15))}
    f=m['fixedcell_extension'];cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    names={str(step):visible_folder(normal,step,rows,cells,native,table) for step in (9,12,15,16)}
    sample=ROOT/'poc/runtime/chip-batch09-v1-description-samples';route=verify_route(sample,build,seen)
    e=read(sample/'mono_batch_environment.json');require(e['passed'] and e['covered_scripts']==SCRIPTS and route['normal_play_checkpoint_eligible'] is False,'diagnostic scope')
    require_hash(ROOT/'tools/capture_chip_batch09_samples.py',e['tool_sha256'])
    offsets={struct.unpack_from('<H',payload,i*2)[0]:i for i in SCRIPTS};covered=set();pixels={}
    for step in route['capture_steps']:
        calls=[c for c in read(sample/f'step_{step:03d}_fixedcells.json')['calls'] if c['font']==0x08619EF8]
        require(calls,'sample mono missing');off=calls[-1]['stream']-0x08000000-ar['rom_offset'];i=offsets[off]
        pixels[str(step)]=mono_sentence(sample,step,m,native,table,texts[i],i,rom_path);covered.add(i)
    require(covered==set(SCRIPTS),'representative screenshot coverage incomplete')
    name_sample=ROOT/'poc/runtime/chip-batch09-v1-name-samples'
    name_route=verify_route(name_sample,build,seen);name_environment=read(name_sample/'folder_batch_environment.json')
    name_ids=[187,201,202,219,236,251,255]
    require(name_environment['passed'] and name_environment['covered_scripts']==name_ids and name_route['normal_play_checkpoint_eligible'] is False,'name diagnostic scope')
    require_hash(ROOT/'tools/capture_chip_batch09_name_samples.py',name_environment['tool_sha256'])
    name_units=resolve_units(read(ROOT/'translations/library_chip_names_batch08_ko.json'))
    name_texts={int(x['id'].split(':')[1]):x['translation'] for x in name_units}
    sample_rows={row:name_texts[i] for row,i in enumerate(name_ids)}
    sample_cells=bdf_cells(ROOT/f['font']['path'],{ch for name in sample_rows.values() for ch in name if '\uac00'<=ch<='\ud7a3'},f['raster'])
    name_pixels={str(step):visible_folder(name_sample,step,sample_rows,sample_cells,native,table) for step in name_route['capture_steps']}
    saves={}
    for directory in seen:
        environment=read(directory/'probe_environment.json');before=environment['files_before'];after=environment['files_after']
        for filename,identity in before.items():
            if filename not in (stem+'.sav',stem+'.rtc'):require(after.get(filename)==identity,'other save changed')
        saves[str(directory.relative_to(ROOT))]={'own_save':after.get(stem+'.sav'),'own_rtc_before':before.get(stem+'.rtc'),'own_rtc_after':after.get(stem+'.rtc'),'other_saves_preserved':True}
    for name,count in (('mono',502),('battle_name',249)):
        cpu=read(ROOT/f'analysis/exe45_chip_batch09_{name}_cpu_v1.json');require(cpu['rom_sha256']==build and cpu['vectors']==count,'CPU vector identity/count')
    return {'rom_sha256':build,'policy':'development-draft; NON-DISTRIBUTION','status':'PASS bounded normal folder and representative17 diagnostic descriptions; not full game validation',
            'selected_translation_units':571,'primary_name_units':249,'description_units':251,'additional_dark_description_units':2,'secondary98_names_not_integrated':True,
            'reproducible':True,'normal_description_pixels':sentences,'normal_folder_name_pixels':names,'diagnostic_description_pixels':pixels,'diagnostic_scripts':sorted(covered),'diagnostic_name_pixels':name_pixels,'diagnostic_name_scripts':name_ids,'save_chain':saves,
            'limits':['17-of251 screenshot samples only; all251 have CPU parser coverage, not full runtime coverage','diagnostic aliases do not prove normal-play chip acquisition','new sparse battle helper has CPU differential coverage but actual battle screen regression remains pending','secondary98 names, secondary descriptions, other dialogue and graphics incomplete','wording/presentation needs human review; audio/hardware/full game/release unverified']}

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
