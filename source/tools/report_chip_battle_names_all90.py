"""90 actual compiled name scripts:720 calls,30 held BG0/pixel diagnostic pages."""
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
    ext=m['chip_battle_name_extension'];asset=ROOT/ext['wording_source'];require_hash(asset,ext['wording_sha256']);texts={int(u['id'].split(':')[1]):u['translation'] for u in resolve_units(read(asset))}
    require(set(texts)==set(range(1,91)),'90name asset denominator')
    f=m['fixedcell_extension'];wanted={ch for text in texts.values() for ch in text if '\uac00'<=ch<='\ud7a3'};cells=bdf_cells(ROOT/f['font']['path'],wanted,f['raster'])
    table={v:int(k,16) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    expected={};glyphs={};streams={}
    for script,text in texts.items():
        payload=[];seq=[]
        for ch in text.ljust(8):
            if ch in cells: payload.append(cells[ch]);seq.append((0x08000000+f['font_offset'],ord(ch)-0xAC00))
            else:
                i=table[ch];payload.append(native[0x612E38+i*64:0x612E38+(i+1)*64]);seq.append((0x08612E38,i))
        expected[script]=b''.join(payload);glyphs[script]=seq
        streams[0x08000000+ext['clone_offset']+struct.unpack_from('<H',blob,ext['clone_offset']+script*2)[0]]=script
    p=ROOT/'poc/runtime/battle-names-v1-all90';r=verify_route(p,build,set());e=read(p/'battle_name_alias_environment.json')
    require(r['return_code']==0 and r.get('normal_play_checkpoint_eligible') is False and e['passed'] and e['parser_calls']==e['observed']['reads']==720,'name diagnostic scope/denominator')
    require_hash(ROOT/'tools/capture_chip_battle_names_all90.py',e['tool_sha256']);require(set(e['observed']['original_values'])=={29,221},'underlying chip IDs changed')
    calls=read(p/'final_fixedcells.json')['calls'];require(len(calls)==720,'name parser calls')
    for c in calls:
        script=streams[c['stream']]
        require(c['complete'] and (c['font'],c['width'],c['height'],c['bytes'],c['tint'])==(0x08612E38,8,1,512,0),'diagnostic name parser/font contract')
        require([(g['font'],g['index']) for g in c['glyphs']]==glyphs[script],'diagnostic name glyph supply')
        require((p/('fixed_%04d_stage.bin'%c['id'])).read_bytes()==expected[script],'diagnostic name actual stage')
    colors={1:(236,239,241),2:(8,8,8)};records=[];covered=set()
    for step in range(1,31):
        prefix='step_%03d'%step;cs=read(p/(prefix+'_fixedcells.json'))['calls'];require(len(cs)==step*24,'held8frame parser boundary')
        video=(p/(prefix+'_gbaVideoRam.bin')).read_bytes();io=(p/(prefix+'_display_io.bin')).read_bytes();state=read(p/(prefix+'_state.json'))['state'];shot=Image.open(p/(prefix+'.png')).convert('RGB')
        require(struct.unpack_from('<H',io,8)[0]==0x1C08 and state['ppu.bgLayers[0].scrollX']==state['ppu.bgLayers[0].scrollY']==0,'diagnostic BG0 geometry')
        scripts=[]
        for target,col in ((0x0600BE00,1),(0x0600C000,11),(0x0600C200,21)):
            c=next(c for c in reversed(cs) if c['copy_target']==target);script=streams[c['stream']];payload=expected[script];tile=(target-0x06008000)//32
            require(video[target-0x06000000:target-0x06000000+512]==payload,'diagnostic name VRAM residency')
            for cell in range(8):
                entries=[struct.unpack_from('<H',video,0xE000+(18+dy)*64+(col+cell)*2)[0] for dy in (0,1)]
                require(entries==[0xD000+tile+cell*2,0xD001+tile+cell*2],'diagnostic name BG map/palette')
                pixels=unpack_pixels(payload[cell*64:(cell+1)*64])
                for role,color in colors.items():
                    mask={(x,y) for y in range(16) for x in range(8) if pixels[y][x]==role}
                    if not mask: continue
                    measured={(x,y) for y in range(16) for x in range(8) if shot.getpixel(((col+cell)*8+x,144+y))==color}
                    require(mask==measured,'diagnostic name exact ink/shadow pixel mask')
            scripts.append(script);covered.add(script)
        require(scripts==list(range(step*3-2,step*3+1)),'held page script sequence')
        records.append({'step':step,'scripts':scripts,'stage_upload_bg_pixels':True,'screenshot_sha256':sha((p/(prefix+'.png')).read_bytes())})
    require(covered==set(texts),'90/90 stable name screenshot coverage')
    out=ROOT/'analysis/exe45_battle_names_all90_runtime_v1.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'status':'PASS diagnostic90/90 battle name glyphs/stage/upload/BG0/ink-shadow pixels; not acquired play',
        'rom_sha256':build,'result_sha256':sha((p/'result.json').read_bytes()),'tool_sha256':sha((ROOT/'tools/report_chip_battle_names_all90.py').read_bytes()),
        'calls':720,'covered_scripts':sorted(covered),'pages':records,'observed_original_chip_ids':e['observed']['original_values'],
        'limits':['name-only CPU read aliases; no90-chip acquisition or normal progression claim','wording and presentation needs_review','transparent background colors excluded; foreground masks and zero glyph padding validated','muted Mesen; no audio/hardware/timing/complete-game release claim']},indent=2),encoding='utf-8')
    print('PASS all90 actual battle-name stages/uploads/BG0/ink-shadow pixels on30 held pages')


if __name__=='__main__': main()
