"""Source-bound native font/card label consumption before any battle-name hook."""
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from report_fixedcell_runtime import verify_route
from fixedcell_font import unpack_pixels


def main():
    rom=ROOT/'poc/output/exe45_ko_development_chip_mono_batch03_v1.gba'
    m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256'])
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    p=ROOT/'poc/runtime/chip-mono-batch03-v1-battle-native-names';r=verify_route(p,m['output_sha256'],set())
    e=read(p/'battle_name_environment.json');require(e['passed'] and r['return_code']==0,'native battle name observation')
    require_hash(ROOT/'tools/capture_chip_battle_names.py',e['tool_sha256'])
    parents=read(p/'final_battle_name_parents.json')['calls'];calls=read(p/'final_fixedcells.json')['calls']
    lookup={0x08765190+struct.unpack_from('<H',native,0x765190+i*2)[0]:i for i in range(256)}
    require(len(parents)==len(calls)==15,'native name denominator')
    for c,parent in zip(calls,parents):
        require((parent['outer_lr'],parent['wrapper_lr'],parent['context'],parent['root_job'],parent['menu'],parent['phase'])==(0x080166C3,0x080554BA,0x0200F2C0,8,28,8),'native name caller/context')
        require(c['complete'] and (c['font'],c['width'],c['height'],c['bytes'],c['tint'])==(0x08612E38,8,1,512,0),'native name font/geometry')
        require(c['stream'] in lookup and len(c['glyphs'])==8,'source primary pool binding')
        expected=b''.join(native[0x612E38+g['index']*64:0x612E38+(g['index']+1)*64] for g in c['glyphs'])
        require((p/('fixed_%04d_stage.bin'%c['id'])).read_bytes()==expected,'native copier payload')
    video=(p/'step_001_gbaVideoRam.bin').read_bytes();io=(p/'step_001_display_io.bin').read_bytes()
    state=read(p/'step_001_state.json')['state'];shot=Image.open(p/'step_001.png').convert('RGB')
    require(struct.unpack_from('<H',io,8)[0]==0x1C08 and state['ppu.bgLayers[0].scrollX']==state['ppu.bgLayers[0].scrollY']==0,'native name BG0 geometry')
    records=[];colors=None
    for target,col in ((0x0600BE00,1),(0x0600C000,11),(0x0600C200,21)):
        c=next(c for c in reversed(calls) if c['copy_target']==target)
        expected=(p/('fixed_%04d_stage.bin'%c['id'])).read_bytes()
        require(video[target-0x06000000:target-0x06000000+512]==expected,'native name upload')
        tile=(target-0x06008000)//32
        glyph_records=[]
        for cell in range(8):
            entries=[struct.unpack_from('<H',video,0xE000+(18+dy)*64+(col+cell)*2)[0] for dy in (0,1)]
            require(entries==[0xD000+tile+cell*2,0xD001+tile+cell*2],'native card BG map/palette')
            pixels=unpack_pixels(expected[cell*64:(cell+1)*64])
            local={role:{shot.getpixel(((col+cell)*8+x,144+y)) for y in range(16) for x in range(8) if pixels[y][x]==role} for role in (1,2)}
            if not any(local.values()): continue
            require(all(len(v)==1 for v in local.values()),'native name role pixel color')
            measured={role:next(iter(v)) for role,v in local.items()}
            if colors is None: colors=measured
            require(measured==colors and colors[1]!=colors[2],'native name palette role consistency')
            glyph_records.append({'cell':cell,'glyph_index':c['glyphs'][cell]['index'],'role_positions_match':True})
        records.append({'script':lookup[c['stream']],'target':target,'xy':[col*8,144],'stage_sha256':sha(expected),'glyphs':glyph_records})
    require([x['script'] for x in records]==[29,29,221],'actual slots differ from observed baseline')
    require(colors=={1:(236,239,241),2:(8,8,8)},'native white ink/dark shadow calibration')
    out=ROOT/'analysis/exe45_chip_battle_native_names_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'status':'PASS bounded native 8x1 card name source/stage/BG role positions; Korean implementation pending',
        'rom_sha256':m['output_sha256'],'result_sha256':sha((p/'result.json').read_bytes()),'tool_sha256':sha((ROOT/'tools/report_chip_battle_native_names.py').read_bytes()),
        'parent':parents[0],'font':{'native_base':0x08612E38,'cell_bytes':64,'roles':{'background':0,'ink':1,'shadow':2}},'screens':records,
        'role_rgb':colors,'limits':['scripts29/221 in this normal route only','transparent background pixels excluded from role-position comparisons','native font observation is not Hangul implementation or all9 root-pair reachability','muted Mesen; no hardware color or audio claim']},indent=2),encoding='utf-8')
    print('PASS native battle name8x1:15calls, scripts29/29/221, BG0 upload and ink/shadow pixels')


if __name__=='__main__': main()
