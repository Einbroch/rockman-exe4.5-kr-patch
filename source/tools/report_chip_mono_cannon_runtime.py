"""Exact new-ROM real Cannon sentence staging, OBJ and screenshot pixels."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells
from report_chip_folder_pixels import visible_folder
from fixedcell_font import unpack_pixels
from archive_scripts import script_spans,verify_untouched_scripts
from tpl_literals import resolve_units


def mono_sentence(p,step,m,native,table,text,script=1,rom_path=None):
    prefix=f'step_{step:03d}';f=m['fixedcell_extension'];mono=f['mono_provider']
    calls=[c for c in read(p/f'{prefix}_fixedcells.json')['calls'] if c['font']==0x08619EF8]
    require(bool(calls),'mono sentence missing')
    c=calls[-1];require(c['complete'] and (c['width'],c['height'],c['bytes'])==(10,3,1920),'mono geometry')
    record=next(a for a in m['archives'] if a['archive']=='76937C')
    rom=(rom_path or ROOT/'poc/output/exe45_ko_development_chip_mono_cannon_v2.gba').read_bytes()
    payload=rom[record['rom_offset']:record['rom_offset']+record['compiled_bytes']]
    require(c['stream']==0x08000000+record['rom_offset']+struct.unpack_from('<H',payload,script*2)[0],'Cannon script identity')
    wanted={ch for ch in text if '\uac00'<=ch<='\ud7a3'}
    cells=bdf_cells(ROOT/mono['font']['path'],wanted,mono['raster'])
    stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();expected=[];expected_glyphs=[]
    lines=text.split('\n');require(len(lines)<=3,'mono sentence row overflow')
    for row,line in enumerate(lines+['']*(3-len(lines))):
        require(len(line)<=9,'sentence beyond visible mono width')
        for ch in line.ljust(10):
            if ch in cells:
                glyph=cells[ch];font=0x08000000+mono['font_offset'];index=ord(ch)-0xAC00
            else:
                code=next(k for k,v in table.items() if v==ch)
                glyph=native[0x619EF8+code*64:0x619EF8+(code+1)*64];font=0x08619EF8;index=code
            expected.append(glyph);expected_glyphs.append((font,index))
    require(stage==b''.join(expected),'compiled Korean/native/padding stage mismatch')
    require([(g['font'],g['index']) for g in c['glyphs']]==expected_glyphs,'mono glyph-provider selection')
    video=(p/f'{prefix}_gbaVideoRam.bin').read_bytes();require(video[0x12800:0x12F80]==stage,'mono upload mismatch')
    oam=(p/f'{prefix}_gbaSpriteRam.bin').read_bytes();palette=(p/f'{prefix}_gbaPaletteRam.bin').read_bytes()
    shot=Image.open(p/f'{prefix}.png').convert('RGB')
    colors=read(ROOT/'analysis/exe45_chip_description_mono_pixels_v1.json')['role_colors'];seen=set()
    for i in range(128):
        a0,a1,a2=struct.unpack_from('<HHH',oam,i*8);tile=a2&1023
        if not 320<=tile<380: continue
        cell=(tile-320)//2;row,col=divmod(cell,10)
        require(tile%2==0 and col<9 and a0>>14==2 and a1>>14==0 and not a0&0x3F00 and not a1&0x3E00 and a2>>12==2,'mono OBJ contract')
        x,y=a1&511,a0&255;require((x,y)==(10+col*8,88+row*16),'mono OBJ position')
        for yy,pixels in enumerate(unpack_pixels(expected[cell])):
            for xx,role in enumerate(pixels):
                color=colors[str(role)]
                require(struct.unpack_from('<H',palette,0x240+role*2)[0]==color['palette_bgr555'],'mono native palette changed')
                require(shot.getpixel((x+xx,y+yy))==tuple(color['rgb']),'translated mono screenshot pixel mismatch')
        seen.add(cell)
    require(seen=={row*10+col for row in range(3) for col in range(9)},'mono visible cell coverage')
    return {'call_id':c['id'],'script':script,'text':text,'stage_sha256':sha(stage),'glyphs':30,'visible_cells':27,'pixel_masks_match':True}


def main():
    stem='exe45_ko_development_chip_mono_cannon_v2';m=read(ROOT/f'poc/output/{stem}.json');build=m['output_sha256']
    require_hash(ROOT/f'poc/output/{stem}.gba',build);require_hash(ROOT/'poc/output/exe45_ko_development_chip_mono_cannon_v1.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    asset=read(ROOT/'translations/chip_descriptions_cannon_poc_ko.json');units=resolve_units(asset)
    a=next(a for a in m['translation_assets'] if a['archive']=='76937C');require_hash(ROOT/a['path'],a['sha256'])
    r=next(a for a in m['archives'] if a['archive']=='76937C');rom=(ROOT/f'poc/output/{stem}.gba').read_bytes()
    payload=rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']]
    preserved=verify_untouched_scripts(native[0x76937C:0x76937C+10467],payload,256,{1,2,3})
    require(len(preserved)==253 and m['translated_units']==102,'mono draft denominator')
    for pointer in r['pointers']: require(struct.unpack_from('<I',rom,pointer)[0]==0x08000000+r['rom_offset'],'description pointer relocation')
    p=ROOT/'poc/runtime/chip-mono-cannon-v2-folder';route=verify_route(p,build,set())
    require(route['return_code']==0 and read(p/'folder_qa_environment.json')['passed'],'folder route/probe fault')
    require(not list(p.glob('*failed*')),'runtime fault')
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
           if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    text=units[0]['translation'];sentences={step:mono_sentence(p,step,m,native,table,text) for step in (8,9,12)}
    f=m['fixedcell_extension'];cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster'])
    rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    names={step:visible_folder(p,step,rows,cells,native,table) for step in (8,9,12)}
    out=ROOT/'analysis/exe45_chip_mono_cannon_runtime_v2.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded normal folder Cannon Korean sentence and chip-name regression; NON-DISTRIBUTION',
        'translated_units':102,'description_units':3,'unselected_description_scripts':253,'result_sha256':sha((p/'result.json').read_bytes()),
        'sentences':sentences,'chip_names':names,'limits':['Cannon normal folder only; scripts2/3 and other shared consumers pending',
        'library/input/reentry/save/new-ROM timing regressions pending','all wording needs review; no complete-game/audio/hardware release claim']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS actual compiled Korean Cannon sentence stage/OBJ/pixels and folder names')


if __name__=='__main__': main()
