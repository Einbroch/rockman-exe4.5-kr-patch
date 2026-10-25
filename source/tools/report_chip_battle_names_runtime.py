"""Actual normal battle: MiniBomb Hangul and native Roll fallback,8x1 BG pixels."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require,bdf_cells
from report_fixedcell_runtime import verify_route
from fixedcell_font import unpack_pixels
from tpl_literals import resolve_units


def main():
    rom=ROOT/'poc/output/exe45_ko_development_battle_names_v1.gba';m=read(rom.with_suffix('.json'));build=m['output_sha256'];require_hash(rom,build);blob=rom.read_bytes()
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    ext=m['chip_battle_name_extension'];asset=ROOT/ext['wording_source'];require_hash(asset,ext['wording_sha256'])
    text=next(u['translation'] for u in resolve_units(read(asset)) if int(u['id'].split(':')[1])==29)
    f=m['fixedcell_extension'];cells=bdf_cells(ROOT/f['font']['path'],set(text),f['raster'])
    payload=b''.join(cells[ch] for ch in text)+native[0x612E38:0x612E78]*(8-len(text))
    expected_glyphs=[(0x08000000+f['font_offset'],ord(ch)-0xAC00) for ch in text]+[(0x08612E38,0)]*(8-len(text))
    stream=0x08000000+ext['clone_offset']+struct.unpack_from('<H',blob,ext['clone_offset']+29*2)[0]
    roll_stream=0x08765190+struct.unpack_from('<H',native,0x765190+221*2)[0]
    require(native[roll_stream-0x08000000:roll_stream-0x08000000+4]==bytes.fromhex('358233E5'),'native Roll source control bytes')
    roll_indices=[0x35,0x82,0x33]+[0]*5
    roll_payload=b''.join(native[0x612E38+i*64:0x612E38+(i+1)*64] for i in roll_indices)
    p=ROOT/'poc/runtime/battle-names-v1-normal-labels';r=verify_route(p,build,set());env=read(p/'battle_name_environment.json')
    require(r['return_code']==0 and env['passed'] and r.get('normal_play_checkpoint_eligible',True),'normal label route')
    require_hash(ROOT/'tools/capture_chip_battle_names.py',env['tool_sha256'])
    parents=read(p/'final_battle_name_parents.json')['calls'];calls=read(p/'final_fixedcells.json')['calls'];require(len(parents)==len(calls)==15,'normal label denominator')
    for c,parent in zip(calls,parents):
        require((parent['outer_lr'],parent['wrapper_lr'],parent['context'],parent['root_job'],parent['menu'],parent['phase'])==(0x080166C3,0x080554BA,0x0200F2C0,8,28,8),'normal label native caller')
        require(c['complete'] and (c['font'],c['width'],c['height'],c['bytes'],c['tint'])==(0x08612E38,8,1,512,0),'normal label font/geometry')
        selected=c['copy_target'] in (0x0600BE00,0x0600C000)
        require(c['stream']==(stream if selected else roll_stream),'selected clone/native fallback stream')
        require([(g['font'],g['index']) for g in c['glyphs']]==(expected_glyphs if selected else [(0x08612E38,i) for i in roll_indices]),'actual glyph/provider/padding sequence')
        require((p/('fixed_%04d_stage.bin'%c['id'])).read_bytes()==(payload if selected else roll_payload),'actual selected/native stage')
    video=(p/'step_001_gbaVideoRam.bin').read_bytes();io=(p/'step_001_display_io.bin').read_bytes();state=read(p/'step_001_state.json')['state'];shot=Image.open(p/'step_001.png').convert('RGB')
    require(struct.unpack_from('<H',io,8)[0]==0x1C08 and state['ppu.bgLayers[0].scrollX']==state['ppu.bgLayers[0].scrollY']==0,'normal label BG0 geometry')
    colors={1:(236,239,241),2:(8,8,8)};records=[]
    for target,col in ((0x0600BE00,1),(0x0600C000,11),(0x0600C200,21)):
        expected=roll_payload if target==0x0600C200 else payload;tile=(target-0x06008000)//32
        require(video[target-0x06000000:target-0x06000000+512]==expected,'normal label VRAM residency')
        glyph_records=[]
        for cell in range(8):
            entries=[struct.unpack_from('<H',video,0xE000+(18+dy)*64+(col+cell)*2)[0] for dy in (0,1)]
            require(entries==[0xD000+tile+cell*2,0xD001+tile+cell*2],'normal BG tile/palette contract')
            pixels=unpack_pixels(expected[cell*64:(cell+1)*64])
            for role,color in colors.items():
                mask={(x,y) for y in range(16) for x in range(8) if pixels[y][x]==role}
                if not mask: continue
                measured={(x,y) for y in range(16) for x in range(8) if shot.getpixel(((col+cell)*8+x,144+y))==color}
                require(mask==measured,'normal Hangul/native exact screenshot mask')
            glyph_records.append({'cell':cell,'glyph_sha256':sha(expected[cell*64:(cell+1)*64]),'ink_shadow_match':True})
        records.append({'script':221 if target==0x0600C200 else 29,'translation':None if target==0x0600C200 else text,'native_fallback':target==0x0600C200,'target':target,'stage_sha256':sha(expected),'glyphs':glyph_records})
    out=ROOT/'analysis/exe45_battle_names_normal_runtime_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'status':'PASS normal MiniBomb battle Hangul names and unselected native Roll fallback8x1/BG0/pixels',
        'rom_sha256':build,'result_sha256':sha((p/'result.json').read_bytes()),'tool_sha256':sha((ROOT/'tools/report_chip_battle_names_runtime.py').read_bytes()),
        'normal_input':True,'calls':15,'screens':records,'roles':ext['roles'],'role_rgb':colors,
        'limits':['normal scripts29/221 only; not90 acquired battle chips','other source name consumers remain native','wordings/presentation needs review; not complete-game release','muted Mesen; no audio/hardware color/timing claim']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS normal MiniBomb Hangul battle names + unselected native Roll:15calls/stage/BG/ink-shadow pixels')


if __name__=='__main__': main()
