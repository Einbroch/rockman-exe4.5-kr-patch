"""Candidate grid tile assets, separate from the editing-field glyph provider.

Decode the fixed revision's 30x20 BG maps and uncompressed 4-bpp pages.
No product ROM changes. Previews are offline pixel decoding, not emulator QA.
"""
import json, struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT, sha, require_hash
from fixedcell_font import unpack_pixels
from report_fixedcell_runtime import verify_route


def decode(bank, raw_map):
    if len(bank) % 32 or len(raw_map) != 1200:
        raise ValueError('page extent')
    pixels = [[0]*240 for _ in range(160)]
    for n, v in enumerate(struct.unpack('<600H', raw_map)):
        tile = v & 1023
        if v >> 12 != 9 or (tile+1)*32 > len(bank):
            raise ValueError('palette9 / tile bounds')
        data = bank[tile*32:(tile+1)*32]
        for y in range(8):
            for x in range(8):
                sx, sy = (7-x if v & 1024 else x), (7-y if v & 2048 else y)
                pixels[n//30*8+y][n%30*8+x] = data[sy*4+sx//2] >> (4*(sx%2)) & 15
    return pixels


def encode(pixels):
    bank, mapping, ids = bytearray(), [], {}
    for y in range(0,160,8):
        for x in range(0,240,8):
            data = bytes(pixels[y+j][x+i] | pixels[y+j][x+i+1] << 4
                         for j in range(8) for i in range(0,8,2))
            if data not in ids:
                ids[data] = len(ids); bank.extend(data)
            mapping.append(0x9000 | ids[data])
    if len(bank) > 0x3000:
        raise ValueError('candidate crosses editing-field VRAM B000')
    return bytes(bank), struct.pack('<600H', *mapping)


def preview(pixels, path, colors):
    im = Image.new('RGB',(240,160)); im.putdata([colors[p] for row in pixels for p in row])
    im.resize((720,480),Image.Resampling.NEAREST).save(path)


def main():
    base = ROOT/'analysis/hangul_keyboard_v1'; out = base/'page_graphics'; out.mkdir(exist_ok=True)
    profile = json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source = ROOT/profile['filename']; require_hash(source,profile['sha256']); rom = source.read_bytes()
    play = ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity = '5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(play,identity); current = play.read_bytes()
    route=ROOT/'poc/runtime/hangul-keyboard-v1-native-edit'; verify_route(route,identity,set())
    palette_path=route/'step_001_gbaPaletteRam.bin'; palette=palette_path.read_bytes()
    if len(palette)!=1024: raise ValueError('observed palette extent')
    colors=[]
    for color in struct.unpack('<16H',palette[288:320]):
        colors.append(tuple(((color>>shift)&31)*255//31 for shift in (0,5,10)))
    # Index0 is transparent in BG graphics. Offline background is diagnostic.
    colors[0]=(170,220,220)
    # Fixed-revision literals, not heuristic discovery or whole-ROM references.
    if struct.unpack_from('<I',rom,0x356BC)[0] != 0x080356C0 or struct.unpack_from('<I',rom,0x356E4)[0] != 0x080356E8:
        raise ValueError('page lookup literals')
    pages = []
    for page in range(3):
        at = 0x356E8+16*page
        src,dst,length,end = struct.unpack_from('<4I',rom,at)
        mp = struct.unpack_from('<I',rom,0x356C0+page*4)[0]-0x08000000
        a = src-0x08000000
        if dst != 0x06008000 or end != 0 or length not in (9600,9440,7232):
            raise ValueError('native transfer descriptor')
        bank, mapping = rom[a:a+length],rom[mp:mp+1200]
        if current[a:a+length] != bank or current[mp:mp+1200] != mapping:
            raise ValueError('native current asset drift')
        pixels = decode(bank,mapping); preview(pixels,out/f'native_page{page}.png',colors)
        pages.append(dict(page=page,bank_offset=a,bank_bytes=length,bank_sha256=sha(bank),map_offset=mp,map_sha256=sha(mapping),descriptor_offset=at,descriptor_hex=rom[at:at+16].hex()))
    plan_path = base/'candidates/plan.json'; plan = json.loads(plan_path.read_text(encoding='utf8'))
    require_hash(base/'candidates/jamo_big_cells.bin',plan['bank_sha256'])
    jamo = (base/'candidates/jamo_big_cells.bin').read_bytes()
    pixels = decode(rom[pages[0]['bank_offset']:pages[0]['bank_offset']+pages[0]['bank_bytes']],rom[pages[0]['map_offset']:pages[0]['map_offset']+1200])
    preview(pixels,out/'native_page0.png',colors)
    original = [row[:] for row in pixels]
    # Source blank strip and entire background samples establish this pattern.
    # Only glyph colors7/8 are removed; no new letterform strokes are invented.
    def background(x,y): return 5 if (x+y)%4 == 3 else 9
    for y in range(56,152):
        for x in range(14,16):
            if pixels[y][x] != background(x,y): raise ValueError('blank strip pattern')
        for x in range(16,191):
            value = pixels[y][x]
            if value not in (5,7,8,9) or value in (5,9) and value != background(x,y):
                raise ValueError('grid background/stroke classification')
            pixels[y][x] = background(x,y)
    placements = []
    for s in plan['selectors'][:90]:
        if not s['active']: continue
        col,row = s['column'],s['row']
        x,y = 16+col*11+6*(col>=5)+6*(col>=10),56+16*row
        glyph = unpack_pixels(jamo[s['glyph_index']*64:(s['glyph_index']+1)*64])
        for j,line in enumerate(glyph):
            for i,v in enumerate(line):
                if v not in (0,1,2): raise ValueError('jamo palette transform')
                if v: pixels[y+j][x+i] = {1:7,2:8}[v]
        placements.append(dict(column=col,row=row,x=x,y=y,character=s['character']))
    for y in range(160):
        for x in range(240):
            if not (16<=x<191 and 56<=y<152) and pixels[y][x] != original[y][x]:
                raise ValueError('protected pixels')
    bank,mapping = encode(pixels)
    # Native transfer uses CpuFastSet: length must be a multiple of32bytes.
    if len(bank)%32 or decode(bank,mapping) != pixels: raise ValueError('candidate pixel roundtrip')
    (out/'jamo_page0_tiles.bin').write_bytes(bank); (out/'jamo_page0_map.bin').write_bytes(mapping)
    preview(pixels,out/'jamo_page0_preview.png',colors)
    report = dict(passed=True,rom_integrated=False,source_sha256=profile['sha256'],current_rom_sha256=identity,pages=pages,plan_sha256=sha(plan_path.read_bytes()),jamo_bank_sha256=sha(jamo),candidate=dict(page=0,active_cells=40,grid_cells=90,placements=placements,bank_bytes=len(bank),map_bytes=len(mapping),VRAM_start='0x06008000',VRAM_end=hex(0x06008000+len(bank)),preserved_outside_grid=True),tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in [Path(__file__).name,'fixedcell_font.py']},artifacts={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.name != 'report.json'},limits=['Native page storage/lookup extent decoded; page upload/draw CPU execution pending in separate bench.','Previews use a diagnostic palette, not actual game rendering, presentation approval or release evidence.','40jamo/50inactive cells match page0 selector plan; command labels and pages1/2 remain Japanese and unsupported for input.','Reindexed tiles preserve all pixels outside left grid; VRAM fit is an extent check, not lifetime/IRQ/scanout proof.','No ROM/hooks/RAM/save changes.'])
    report['observed_palette']=dict(path=str(palette_path.relative_to(ROOT)).replace('\\','/'),sha256=sha(palette),route_result_sha256=sha((route/'result.json').read_bytes()),bank=9,transparent_preview_background='diagnostic cyan')
    report['limits'][1]='Offline tile decode uses previously observed native palette9 and diagnostic transparent background; not actual candidate game rendering or presentation approval.'
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS native 3-page decode + candidate40jamo tiles',len(bank),'bytes',flush=True)


if __name__ == '__main__': main()
