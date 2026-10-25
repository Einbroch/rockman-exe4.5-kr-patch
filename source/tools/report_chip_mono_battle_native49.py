"""Unselected native WideSword49 fallback between two Korean Vulcan1 displays."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read,require
from fixedcell_font import unpack_pixels
from archive_scripts import script_spans
from tpl_literals import literals


def main():
    rom_path=ROOT/'poc/output/exe45_ko_development_chip_mono_batch01_v1.gba';m=read(rom_path.with_suffix('.json'));build=m['output_sha256'];require_hash(rom_path,build);blob=rom_path.read_bytes()
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    ar=next(a for a in m['archives'] if a['archive']=='76937C');pool=blob[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    require(script_spans(pool,256)[49]==script_spans(native[0x76937C:0x76937C+10467],256)[49],'unselected script49 changed')
    text=next(l.text for l in literals((ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig')) if l.key=='76937C:49:0')
    table={v:(int(k,16) if len(k)==2 else 0xE4+int(k[2:],16)) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 or len(k)==4 and k.startswith('E4')}
    indices=[table[ch] for line in text.split('\n') for ch in line.ljust(9)];require(len(indices)==27,'native49 geometry')
    cells=[native[0x619EF8+i*64:0x619EF8+(i+1)*64] for i in indices];payload=b''.join(cells)
    p=ROOT/'poc/runtime/chip-mono-batch01-v1-battle-airshot-info';route=verify_route(p,build,set());require(route['return_code']==0,'native fallback route failure');prefix='step_004'
    c=read(p/f'{prefix}_fixedcells.json')['calls'][-1]
    require(c['complete'] and (c['width'],c['height'],c['bytes'])==(9,3,1728),'native49 call geometry')
    stream=0x08000000+ar['rom_offset']+struct.unpack_from('<H',pool,98)[0];require(c['stream']==stream,'native49 script identity')
    require([(g['font'],g['index']) for g in c['glyphs']]==[(0x08619EF8,i) for i in indices],'native49 glyphs/font fallback')
    stage=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes();require(stage==payload,'native49 stage bytes')
    require(c['copy_target']==0x06016560,'native49 target');video=(p/f'{prefix}_gbaVideoRam.bin').read_bytes();require(video[0x16560:0x16C20]==payload,'native49 upload')
    # Reuse the same route's source-native ASCII3 calibrated palette roles,
    # after requiring this native fallback screen's exact palette identity.
    calibrated=read(ROOT/'analysis/exe45_chip_mono_battle_vulcan_runtime_v1.json');require(calibrated['rom_sha256']==build,'calibration ROM');colors=calibrated['screens'][0]['role_rgb'];expected_palette=calibrated['screens'][0]['palette_bgr555']
    pal=(p/f'{prefix}_gbaPaletteRam.bin').read_bytes();require(all(struct.unpack_from('<H',pal,0x380+int(role)*2)[0]==value for role,value in expected_palette.items()),'native49 palette differs from calibrated screen')
    shot=Image.open(p/f'{prefix}.png').convert('RGB');oam=(p/f'{prefix}_gbaSpriteRam.bin').read_bytes();objects={}
    for i in range(128):
        a0,a1,a2=struct.unpack_from('<HHH',oam,i*8);tile=a2&1023
        if not 811<=tile<865: continue
        require((tile-811)%2==0 and a0>>14==2 and a1>>14==0 and not a0&0x3F00 and not a1&0x3E00 and a2>>12==12,'native49 OBJ')
        cell=(tile-811)//2;row,col=divmod(cell,9);x,y=a1&511,a0&255;require((x,y)==(84+col*8,80+row*16),'native49 panel location');objects[cell]=(x,y)
        for yy,pixels in enumerate(unpack_pixels(cells[cell])):
            for xx,role in enumerate(pixels): require(shot.getpixel((x+xx,y+yy))==tuple(colors[str(role)]),'native49 fallback pixel')
    require(set(objects)==set(range(27)),'native49 visible coverage')
    out=ROOT/'analysis/exe45_chip_mono_battle_native49_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded normal Korean15→native49→Korean15 fallback','native_script':49,'source_text':text,'untouched_script':True,'glyphs':27,'visible_cells':27,'stage_sha256':sha(stage),'result_sha256':sha((p/'result.json').read_bytes()),'calibration_report_sha256':sha((ROOT/'analysis/exe45_chip_mono_battle_vulcan_runtime_v1.json').read_bytes()),'limits':['native49 fallback only; not every unselected script','muted isolated Mesen; not hardware/full-game QA']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS normal native49 fallback bytes/provider/upload/27OBJ/pixels')


if __name__=='__main__': main()
