"""Native description OBJ tile/palette/scanout proof before mono font edits."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha
from fixedcell_font import unpack_pixels
from report_chip_library_runtime import read,require


def main():
    survey=read(ROOT/'analysis/exe45_chip_description_mono_native_v1.json')
    p=ROOT/'poc/runtime/chip-folder-v3-normal-r1';step=8;prefix=f'step_{step:03d}'
    v=(p/f'{prefix}_gbaVideoRam.bin').read_bytes();a=(p/f'{prefix}_gbaSpriteRam.bin').read_bytes()
    palette=(p/f'{prefix}_gbaPaletteRam.bin').read_bytes();shot=Image.open(p/f'{prefix}.png').convert('RGB')
    call=[c for c in read(p/f'{prefix}_fixedcells.json')['calls'] if c['font']==0x08619EF8][-1]
    stage=(p/f"fixed_{call['id']:04d}_stage.bin").read_bytes()
    require(v[0x12800:0x12F80]==stage,'description upload bytes')
    records=[];colors={};tiles=set()
    for i in range(128):
        attr0,attr1,attr2=struct.unpack_from('<HHH',a,i*8);tile=attr2&1023
        if not 320<=tile<380: continue
        require(attr0>>14==2 and attr1>>14==0 and not attr0&0x3F00 and not attr1&0x3E00,'native mono OBJ format')
        require(tile%2==0 and attr2>>12==2,'mono OBJ tile/palette')
        x=attr1&511;y=attr0&255;cell=(tile-320)//2
        require(cell%10<9 and (x,y)==(10+(cell%10)*8,88+(cell//10)*16),'mono OBJ position')
        glyph=v[0x10000+tile*32:0x10000+tile*32+64];pixels=unpack_pixels(glyph)
        for yy in range(16):
            for xx in range(8):
                role=pixels[yy][xx]
                require(role!=0,'unexpected transparent description source pixel')
                color=shot.getpixel((x+xx,y+yy));raw=struct.unpack_from('<H',palette,0x240+role*2)[0]
                key=str(role)
                if key in colors: require(colors[key]['rgb']==list(color),'mono role inconsistency')
                colors[key]={'rgb':list(color),'palette_bgr555':raw}
        tiles.add(tile);records.append({'oam_index':i,'cell':cell,'tile':tile,'x':x,'y':y,'glyph_sha256':sha(glyph)})
    require(tiles=={320+row*20+col*2 for row in range(3) for col in range(9)},'mono 27-visible-cell OBJ coverage')
    require(all(stage[(row*10+9)*64:(row*10+10)*64]==bytes([0x11])*64 for row in range(3)),'unshown tenth column is not native blank')
    out=ROOT/'analysis/exe45_chip_description_mono_pixels_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':survey['rom_sha256'],'status':'PASS native 10x3 staging, 9x3 visible OBJ upload/palette/pixels; translated mono pending',
        'survey_sha256':sha((ROOT/'analysis/exe45_chip_description_mono_native_v1.json').read_bytes()),
        'step':step,'source_script':1,'role_colors':colors,'sprites':records,'unshown_blank_columns':[9,19,29],
        'limits':['native Cannon description only; 10 staging cells do not prove 10 visible cells',
                  'screenshot RGB is empirically bound to palette indices; hardware BGR555-to-RGB conversion not claimed',
                  'no translated mono font/layout or full-game QA claim']},indent=2),encoding='utf-8')
    print('PASS native mono 30 staged/27 visible cells, upload, OBJ positions and exact palette pixels:',colors)


if __name__=='__main__':
    main()
