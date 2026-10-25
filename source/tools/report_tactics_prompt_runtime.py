"""Source-bound5x2 stage/upload/BG3/pixel audit; exact native input only."""
import argparse
import json
import struct
from PIL import Image
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import verify_route
from report_chip_library_runtime import read, require, bdf_cells
from fixedcell_font import unpack_pixels
from tpl_literals import resolve_units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--route', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--steps', required=True)
    ap.add_argument('--script', type=int, choices=(0,1), required=True)
    args = ap.parse_args()
    rom = ROOT/'poc/output/exe45_ko_development_tactics_prompts_v1.gba'
    m = read(rom.with_suffix('.json')); build = m['output_sha256']
    require_hash(rom, build); blob = rom.read_bytes()
    source = ROOT/read(ROOT/'project.json')['source_profile']['filename']
    require_hash(source, m['source_sha256']); native = source.read_bytes()
    asset = ROOT/'translations/megaman_tactics_prompts_ko.json'
    record = next(a for a in m['translation_assets'] if a['archive']=='76C944')
    require_hash(asset, record['sha256']); units = resolve_units(read(asset))
    font = m['fixedcell_extension']['mono_provider']
    cells = bdf_cells(ROOT/font['font']['path'], {ch for u in units for ch in u['translation'] if '\uac00'<=ch<='\ud7a3'}, font['raster'])
    table = {v:int(k,16) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    ar = next(r for r in m['archives'] if r['archive']=='76C944')
    expected = {}
    for u in units:
        script = int(u['id'].split(':')[1]); data = []; glyphs = []; chars = []
        for line in u['translation'].split('\n'):
            for ch in line.ljust(5):
                if ch in cells:
                    cell = cells[ch]; bank = 0x08000000+font['font_offset']; index = ord(ch)-0xAC00
                else:
                    index = table[ch]; bank = 0x08619EF8; cell = native[0x619EF8+index*64:0x619EF8+(index+1)*64]
                data.append(cell); glyphs.append((bank,index)); chars.append(ch)
        stream = 0x08000000+ar['rom_offset']+struct.unpack_from('<H',blob,ar['rom_offset']+script*2)[0]
        expected[stream] = (script, data, glyphs, chars)
    p = ROOT/args.route; route = verify_route(p, build, set())
    require(route['complete'] and route['return_code']==0, 'incomplete route')
    parents = read(p/'final_tactics_prompt_parents.json')['calls']
    require(parents and all(c['outer_lr']==0x08020B5F and c['width']==5 and c['height']==2 and c['stream'] in expected for c in parents), 'TACTICS parent/source binding')
    records = []; seen = set()
    for step in map(int,args.steps.split(',')):
        require(step in route['capture_steps'], 'unrecorded screenshot step')
        prefix = f'step_{step:03d}'
        calls = read(p/f'{prefix}_fixedcells.json')['calls']
        if not calls: continue
        c = calls[-1]
        if c['stream'] not in expected: continue
        script, data, glyphs, chars = expected[c['stream']]
        require(c['complete'] and (c['width'],c['height'],c['bytes'])==(5,2,640), 'prompt geometry')
        require([(g['font'],g['index']) for g in c['glyphs']]==glyphs, 'prompt provider cursor')
        payload = b''.join(data); stage = (p/f"fixed_{c['id']:04d}_stage.bin").read_bytes()
        require(stage==payload, 'prompt stage mismatch')
        target = c['copy_target']; video = (p/f'{prefix}_gbaVideoRam.bin').read_bytes()
        require(video[target-0x06000000:target-0x06000000+640]==payload, 'held prompt upload mismatch')
        require(target==0x06008A20, 'native prompt BG3 upload target')
        io = (p/f'{prefix}_display_io.bin').read_bytes()
        state = read(p/f'{prefix}_state.json')['state']
        require(struct.unpack_from('<H',io,14)[0]==0x1F09 and state['ppu.bgLayers[3].scrollX']==state['ppu.bgLayers[3].scrollY']==0, 'prompt BG3 geometry')
        tile0 = (target-0x06008000)//32
        objects = {}; x0,y0,palette = 56,32,10
        for cell in range(10):
            row,col = divmod(cell,5)
            entries = [struct.unpack_from('<H',video,0xF800+(4+row*2+dy)*64+(7+col)*2)[0] for dy in (0,1)]
            require(entries==[0xA000+tile0+cell*2,0xA001+tile0+cell*2], 'prompt BG3 map/roles')
            objects[cell] = (x0+col*8,y0+row*16,palette)
        shot = Image.open(p/f'{prefix}.png').convert('RGB'); colors = {}
        for cell, ch in enumerate(chars):
            if ch in cells or ch==' ': continue
            x,y,_ = objects[cell]
            for yy,row in enumerate(unpack_pixels(data[cell])):
                for xx,role in enumerate(row):
                    color = shot.getpixel((x+xx,y+yy))
                    require(role not in colors or colors[role]==color, 'native punctuation role inconsistency')
                    colors[role] = color
        require(set(colors)=={1,3,4}, 'native punctuation role calibration')
        for cell,(x,y,_) in objects.items():
            for yy,row in enumerate(unpack_pixels(data[cell])):
                for xx,role in enumerate(row):
                    require(shot.getpixel((x+xx,y+yy))==colors[role], 'prompt screenshot mask mismatch')
        seen.add(script)
        records.append({'step':step,'script':script,'stage_sha256':sha(stage),'copy_target':target,'origin':[x0,y0],'palette':palette,'role_rgb':colors,'visible_cells':10,'pixels_verified':True})
    require(seen=={args.script}, 'requested prompt held pixel denominator')
    out = ROOT/args.out; require(not out.exists(), 'refuse overwrite')
    out.write_text(json.dumps({'rom_sha256':build,'status':'PASS bounded normal Rockman TACTICS prompts5x2','result_sha256':sha((p/'result.json').read_bytes()),'parents':parents,'screens':records,'limits':['two Rockman prompts only, other142 scripts unchanged','wording needs_review; no release or full-game QA']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS TACTICS prompt',args.script,'stage/upload/BG3/10cells/pixels')


if __name__=='__main__':
    main()
