"""Read-only ninth-screen BG/OBJ and ROM tile-source inventory."""
import json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route

def main():
    route=ROOT/'poc/runtime/pet-graphics-v1-folder-regression';out=ROOT/'analysis/folder_labels_survey_v1'
    if out.exists():raise ValueError('fresh survey output required')
    rom=ROOT/'poc/output/exe45_ko_development_pet_graphics_v1.gba';m=json.loads(rom.with_suffix('.json').read_text());verify_route(route,m['output_sha256'],set())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    v=(route/'step_016_gbaVideoRam.bin').read_bytes();p=(route/'step_016_gbaPaletteRam.bin').read_bytes();io=(route/'step_016_display_io.bin').read_bytes();o=(route/'step_016_gbaSpriteRam.bin').read_bytes()
    state=json.loads((route/'step_016_state.json').read_text())['state'];out.mkdir();layers=[]
    for layer in range(4):
        ctrl=struct.unpack_from('<H',io,8+layer*2)[0];charbase=((ctrl>>2)&3)*0x4000;mapbase=((ctrl>>8)&31)*0x800
        if ctrl&0xC080:continue
        sx=state[f'ppu.bgLayers[{layer}].scrollX'];sy=state[f'ppu.bgLayers[{layer}].scrollY'];img=Image.new('RGBA',(240,160));cells={}
        for y in range(160):
            for x in range(240):
                xx=(x+sx)%256;yy=(y+sy)%256;at=mapbase+(yy//8)*64+(xx//8)*2;entry=struct.unpack_from('<H',v,at)[0];px=xx%8;py=yy%8
                if entry&0x400:px=7-px
                if entry&0x800:py=7-py
                offset=charbase+(entry&1023)*32;byte=v[offset+py*4+px//2];role=(byte>>(4*(px%2)))&15
                raw=struct.unpack_from('<H',p,(entry>>12)*32+role*2)[0];img.putpixel((x,y),tuple(((raw>>s)&31)*255//31 for s in (0,5,10))+(255 if role else 0,))
                if (100<=x<144 and y<12) or (96<=x<160 and 24<=y<40):cells[(yy//8,xx//8)]=(entry,offset,at)
        img.save(out/f'bg{layer}.png');records=[]
        for (row,col),(entry,offset,mapat) in sorted(cells.items()):
            tile=v[offset:offset+32];sites=[];cursor=0
            if len(set(tile))>1:
                while len(sites)<8:
                    found=native.find(tile,cursor)
                    if found<0:break
                    sites.append(found);cursor=found+1
            records.append({'row':row,'col':col,'entry':entry,'vram_offset':offset,'map_offset':mapat,'raw_rom_matches':sites,'tile_sha256':sha(tile)})
        layers.append({'layer':layer,'ctrl':ctrl,'charbase':charbase,'mapbase':mapbase,'scroll':[sx,sy],'roi_cells':records})
    objects=[]
    for index in range(128):
        a,b,c=struct.unpack_from('<HHH',o,index*8)
        if not a&512 and a&255<40:objects.append({'index':index,'attributes':[a,b,c],'xy':[b&511,a&255]})
    report={'rom_sha256':m['output_sha256'],'source_sha256':m['source_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),
        'receipt_sha256':sha((route/'result.json').read_bytes()),'scope':'One ninth screenshot header ROI only, raw palette layer previews; not whole folder/source-loader inventory',
        'layers':layers,'top_objects':objects}
    (out/'survey.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
