"""Protected30 descriptions, real normal selections and quarantined all30 pixels."""
import json
import struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells
from report_chip_folder_pixels import visible_folder
from report_chip_mono_cannon_runtime import mono_sentence
from archive_scripts import verify_untouched_scripts
from tpl_literals import resolve_units


def main():
    stem='exe45_ko_development_chip_mono_batch01_v1';rom_path=ROOT/f'poc/output/{stem}.gba'
    m=read(rom_path.with_suffix('.json'));build=m['output_sha256']
    for suffix in ('','_repro'): require_hash(ROOT/f'poc/output/{stem}{suffix}.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    asset=ROOT/'translations/chip_descriptions_batch01_ko.json';a=next(a for a in m['translation_assets'] if a['archive']=='76937C');require_hash(asset,a['sha256'])
    units=resolve_units(read(asset));texts={int(u['id'].split(':')[1]):u['translation'] for u in units}
    require(set(texts)==set(range(1,31)) and m['translated_units']==129,'description draft denominator')
    r=next(a for a in m['archives'] if a['archive']=='76937C');rom=rom_path.read_bytes();payload=rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']]
    preserved=verify_untouched_scripts(native[0x76937C:0x76937C+10467],payload,256,set(texts));require(len(preserved)==226,'unselected script preservation')
    require(r['protected_controls_unchanged'] and r['native_roundtrip'] and r['semantic_roundtrip'] and r['binary_roundtrip'],'archive round-trip')
    for pointer in r['pointers']: require(struct.unpack_from('<I',rom,pointer)[0]==0x08000000+r['rom_offset'],'description root relocation')
    f=m['fixedcell_extension'];mono=f['mono_provider'];require_hash(ROOT/mono['font']['path'],mono['font']['sha256'])
    cells=bdf_cells(ROOT/mono['font']['path'],{ch for text in texts.values() for ch in text if '\uac00'<=ch<='\ud7a3'},mono['raster'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    seen=set();normal={};p=ROOT/'poc/runtime/chip-mono-batch01-v1-normal-scroll';route=verify_route(p,build,seen)
    require(route['return_code']==0 and read(p/'folder_qa_environment.json')['passed'] and not list(p.glob('*failed*')),'normal scroll observer/fault')
    for step,script in ((9,1),(12,4),(15,15),(16,15)):
        normal[step]=mono_sentence(p,step,m,native,table,texts[script],script,rom_path)
    name_cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    name_pixels={step:visible_folder(p,step,rows,name_cells,native,table) for step in (9,12,15,16)}
    p=ROOT/'poc/runtime/chip-mono-batch01-v1-all30';route=verify_route(p,build,seen);e=read(p/'mono_batch_environment.json')
    require_hash(ROOT/'tools/capture_chip_mono_batch.py',e['tool_sha256'])
    require(route['return_code']==0 and route.get('normal_play_checkpoint_eligible') is False and e['passed'] and e['covered_scripts']==list(range(1,31)),'all30 diagnostic scope/fault')
    pixels={};covered=set()
    for step in route['capture_steps']:
        calls=[c for c in read(p/f'step_{step:03d}_fixedcells.json')['calls'] if c['font']==0x08619EF8]
        require(calls,'diagnostic mono capture missing')
        off=calls[-1]['stream']-0x08000000-r['rom_offset']
        script=next(i for i in texts if struct.unpack_from('<H',payload,i*2)[0]==off)
        pixels[step]=mono_sentence(p,step,m,native,table,texts[script],script,rom_path);covered.add(script)
    require(covered==set(texts),'all30 lacks independent stable pixel coverage')
    out=ROOT/'analysis/exe45_chip_mono_batch01_runtime_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded30 description development clone; NON-DISTRIBUTION',
        'draft_units':129,'description_units':30,'new_description_units':27,'unselected_description_scripts':226,
        'required_hangul_glyphs':len(cells),'reproducible':True,'normal_selections':normal,'normal_chip_names':name_pixels,
        'diagnostic_environment':e,'all30_stable_pixels':pixels,
        'limits':['diagnostic source-table aliases do not prove30 acquired normal-play chips','new-ROM library/input/save/timing regressions pending',
                  'shared pointer consumers2165C/D2B58 and full game still pending','wording and terminology needs review; no audio/hardware/release claim']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS protected30 descriptions, normal Cannon/Airshot/Vulcan and all30 stable stage/OBJ/pixels')


if __name__=='__main__': main()
