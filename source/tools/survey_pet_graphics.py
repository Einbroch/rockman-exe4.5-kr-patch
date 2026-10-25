"""Read-only PET BG extraction/source lookup; no image or ROM edits."""
import json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route

def main():
    p=ROOT/'poc/runtime/roll-tactics-v1-cold-part2';out=ROOT/'analysis/pet_graphics_survey_v1'
    if out.exists():raise ValueError('fresh survey output required')
    m=json.loads((ROOT/'poc/output/exe45_ko_development_roll_tactics_v1.json').read_text());verify_route(p,m['output_sha256'],set())
    project=json.loads((ROOT/'project.json').read_text());source=ROOT/project['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    v=(p/'step_040_gbaVideoRam.bin').read_bytes();pal=(p/'step_040_gbaPaletteRam.bin').read_bytes();io=(p/'step_040_display_io.bin').read_bytes()
    state=json.loads((p/'step_040_state.json').read_text())['state'];out.mkdir();layers=[]
    for layer in range(4):
        ctrl=struct.unpack_from('<H',io,8+layer*2)[0];charbase=((ctrl>>2)&3)*0x4000;mapbase=((ctrl>>8)&31)*0x800
        if ctrl&0xC080:continue
        sx=state[f'ppu.bgLayers[{layer}].scrollX'];sy=state[f'ppu.bgLayers[{layer}].scrollY'];img=Image.new('RGBA',(240,160));cells=[]
        for y in range(160):
            for x in range(240):
                xx=(x+sx)%256;yy=(y+sy)%256;entry=struct.unpack_from('<H',v,mapbase+(yy//8)*64+(xx//8)*2)[0]
                px=xx%8;py=yy%8
                if entry&0x400:px=7-px
                if entry&0x800:py=7-py
                at=charbase+(entry&1023)*32;bt=v[at+py*4+px//2];role=(bt>>(4*(px%2)))&15
                rgb=struct.unpack_from('<H',pal,(entry>>12)*32+role*2)[0]
                color=tuple(((rgb>>shift)&31)*255//31 for shift in (0,5,10))
                img.putpixel((x,y),color+(255 if role else 0,))
        img.save(out/f'bg{layer}.png')
        for row in range(2,13):
            for col in range(15,26):
                entry=struct.unpack_from('<H',v,mapbase+row*64+col*2)[0];at=charbase+(entry&1023)*32;tile=v[at:at+32]
                if len(set(tile))==1:continue
                sites=[];cursor=0
                while len(sites)<12:
                    found=native.find(tile,cursor)
                    if found<0:break
                    sites.append(found);cursor=found+1
                cells.append({'row':row,'col':col,'entry':entry,'vram_offset':at,'tile_sha256':sha(tile),'raw_rom_matches':sites})
        layers.append({'layer':layer,'control':ctrl,'character_base':charbase,'map_base':mapbase,'scroll':[sx,sy],'cells_in_menu_roi':cells})
    report={'rom_sha256':m['output_sha256'],'source_sha256':m['source_sha256'],'runtime_receipt_sha256':sha((p/'result.json').read_bytes()),
        'tool_sha256':sha(Path(__file__).read_bytes()),'scope':'One PET screen, four BG layers and visible menu ROI only; NOT full-game graphic inventory or translation/loader proof',
        'palette_limit':'Layer previews use raw BGR555 converted RGB, not emulator LCD color correction, blending, priority or OBJ composition','layers':layers}
    (out/'survey.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
