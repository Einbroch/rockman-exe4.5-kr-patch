"""Normal battle MiniBomb source-bound 9x3 staging and independent glyph pixels."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require,bdf_cells
from fixedcell_font import unpack_pixels
from tpl_literals import resolve_units


def main():
    rom_path=ROOT/'poc/output/exe45_ko_development_chip_mono_batch01_v1.gba'
    m=read(rom_path.with_suffix('.json'));build=m['output_sha256'];require_hash(rom_path,build)
    native_path=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(native_path,m['source_sha256']);native=native_path.read_bytes()
    asset=ROOT/'translations/chip_descriptions_batch01_ko.json';a=next(a for a in m['translation_assets'] if a['archive']=='76937C');require_hash(asset,a['sha256'])
    text=next(u['translation'] for u in resolve_units(read(asset)) if int(u['id'].split(':')[1])==29)
    f=m['fixedcell_extension']['mono_provider'];cells=bdf_cells(ROOT/f['font']['path'],{ch for ch in text if '\uac00'<=ch<='\ud7a3'},f['raster'])
    table={v:int(k,16) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    expected=[];glyphs=[]
    lines=text.split('\n')
    for line in lines+['']*(3-len(lines)):
        for ch in line.ljust(9):
            if ch in cells: cell=cells[ch];font=0x08000000+f['font_offset'];index=ord(ch)-0xAC00
            else:
                index=table[ch];font=0x08619EF8;cell=native[0x619EF8+index*64:0x619EF8+(index+1)*64]
            expected.append(cell);glyphs.append((font,index))
    payload=b''.join(expected);r=next(a for a in m['archives'] if a['archive']=='76937C');blob=rom_path.read_bytes()
    stream=0x08000000+r['rom_offset']+struct.unpack_from('<H',blob,r['rom_offset']+29*2)[0]
    p=ROOT/'poc/runtime/chip-mono-batch01-v1-battle-tactics-info';route=verify_route(p,build,set());require(route['return_code']==0,'battle route failure')
    parents=read(p/'final_mono_parents.json')['calls'];require(len(parents)==3,'battle parent denominator')
    require(all(c['outer_lr']==0x0802164B and c['wrapper_lr']==0x080554BA and c['width']==9 and c['height']==3 and c['stream']==stream and c['context']==0x0200F2C0 and c['root_job']==8 for c in parents),'battle native21628 caller')
    records=[]
    for step in (2,3,4):
        prefix=f'step_{step:03d}';calls=read(p/f'{prefix}_fixedcells.json')['calls'];c=calls[-1]
        require(c['complete'] and (c['width'],c['height'],c['bytes'])==(9,3,1728) and c['stream']==stream,'battle script geometry')
        require([(g['font'],g['index']) for g in c['glyphs']]==glyphs,'battle provider selection')
        stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();require(stage==payload,'battle native/Korean/padding bytes')
        target=c['copy_target'];require(target==0x06016560,'battle native upload target')
        video=(p/f'{prefix}_gbaVideoRam.bin').read_bytes();require(video[target-0x06000000:target-0x06000000+1728]==stage,'battle upload bytes')
        oam=(p/f'{prefix}_gbaSpriteRam.bin').read_bytes();pal=(p/f'{prefix}_gbaPaletteRam.bin').read_bytes();shot=Image.open(p/f'{prefix}.png').convert('RGB');objects={}
        for i in range(128):
            a0,a1,a2=struct.unpack_from('<HHH',oam,i*8);tile=a2&1023
            if not 811<=tile<865: continue
            require((tile-811)%2==0 and a0>>14==2 and a1>>14==0 and not a0&0x3F00 and not a1&0x3E00 and a2>>12==12,'battle OBJ contract')
            cell=(tile-811)//2;row,col=divmod(cell,9);objects[cell]=(a1&511,a0&255)
            require((a0&255)==80+row*16,'battle OBJ row')
        require(set(objects)==set(range(27)),'battle27 visible cells')
        origin=objects[0][0];require(origin in (4,84,164) and all(pos==(origin+(cell%9)*8,80+(cell//9)*16) for cell,pos in objects.items()),'battle moving-panel coordinates')
        # Native source ASCII3 is unpatched and carries all three roles. Use it
        # to calibrate this battle palette's scanout, not previous menu colors.
        colors={};x,y=objects[0]
        for yy,row in enumerate(unpack_pixels(expected[0])):
            for xx,role in enumerate(row):
                color=shot.getpixel((x+xx,y+yy));require(role not in colors or colors[role]==color,'native ASCII calibration inconsistency');colors[role]=color
        require(set(colors)=={1,3,4},'native ASCII role coverage')
        for cell,(x,y) in objects.items():
            for yy,row in enumerate(unpack_pixels(expected[cell])):
                for xx,role in enumerate(row): require(shot.getpixel((x+xx,y+yy))==colors[role],'battle Hangul screenshot pixel')
        records.append({'step':step,'script':29,'call_id':c['id'],'stage_sha256':sha(stage),'visible_cells':27,'panel_x':origin,'role_rgb':colors,'palette_bgr555':{role:struct.unpack_from('<H',pal,0x380+role*2)[0] for role in colors},'pixel_match':True})
    out=ROOT/'analysis/exe45_chip_mono_battle_runtime_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded normal tutorial battle MiniBomb Korean description at9x3',
        'result_sha256':sha((p/'result.json').read_bytes()),'normal_input':True,'native_consumer_entry':0x08021628,'source_pool_literal':0x0802165C,'parents':parents,'screens':records,
        'limits':['normal tutorial MiniBomb only; not all30 battle scripts','native ASCII3 calibrates battle role colors; no hardware color claim','battle chip names remain native Japanese outside current name scope','D2B58 consumer remains unresolved','129 drafts; not complete-game release']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS normal battle MiniBomb9x3 stage/upload/27OBJ/pixels on3 held screens')


if __name__=='__main__': main()
