"""Stage 075 (no new text units): subchip screen title redrawn like the equipment title, over the 074 ROM.

User feedback 2026-10-25 (mGBA): 073's hand-drawn 서브칩 did not read well; draw it like 장비 (folder_labels.title):
Galmuri7 glyphs, one ink colour, no outline, 8-px advance. Same LZ77 block as 073 (0x6FB82C, BG1 tiles 6..11):
rows 1..7 of the six tiles become background 13 with the glyphs in ink 11, row 0 (bar line, colour 15) stays.
The 073 patch for this block is dropped from the patch list and replaced; 073's region record keeps its own bytes,
so its verify has to be given this stage's predecessor view (done by make_graphics_stage075_v1.py).
"""
import json
from build_visibility_poc import ROOT, sha
from gba_lz77_v1 import compress, decompress
from pet_graphics_font import glyphs
from graphics_stage073_v1 import BLOCK, BLOCK_END, POINTER, FIRST_TILE, TILES, BORDER, BG, at, pixel

KEY = 'graphics075'
PREDECESSOR = 'poc/output/pending500_074_v1.gba'
TAG = ' graphic fix: '
INK, TEXT, ADVANCE = 11, '서브칩', 8


def title_block(source):
    raw, used = decompress(source, BLOCK)
    if (len(raw), used, BLOCK + used) != (2884, 1036, BLOCK_END):raise ValueError(KEY + ' block layout')
    w = TILES * 8
    if {pixel(raw, x, 0) for x in range(w)} != {BORDER}:raise ValueError(KEY + ' title border')
    g = glyphs(json.loads((ROOT / 'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8')), extra_characters=TEXT)
    points, pen = [], 0
    for ch in TEXT:
        gl = g[ch]
        if gl['top'] < 1 or gl['top'] + gl['height'] > 8:raise ValueError(KEY + ' glyph height ' + ch)
        for y, bits in enumerate(gl['bits']):
            for x in range(gl['width']):
                if bits & (1 << (7 - x)):points.append((pen + x, gl['top'] + y))
        pen += ADVANCE
    width = max(x for x, _ in points) + 1;x0 = (w - width) // 2
    rows = [[BG] * w for _ in range(8)]
    for x, y in points:rows[y][x + x0] = INK
    out = bytearray(raw)
    for y in range(1, 8):
        for x in range(0, w, 2):out[at(x, y)] = rows[y][x] | rows[y][x + 1] << 4
    keep = 4 + (FIRST_TILE - 1) * 32
    if out[:keep] != raw[:keep] or out[keep + TILES * 32:] != raw[keep + TILES * 32:]:raise ValueError(KEY + ' protected tiles')
    packed = compress(bytes(out))
    if len(packed) > BLOCK_END - BLOCK:raise ValueError(KEY + ' recompressed block too large')
    return packed + bytes(BLOCK_END - BLOCK - len(packed)), sha(bytes(out))


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    prior = keymeta['graphics073']['graphics'][0]
    if (prior['offset'], prior['size']) != (BLOCK, BLOCK_END - BLOCK) or base[BLOCK:BLOCK_END].hex() != prior['final_hex']:raise ValueError(KEY + ' 073 block state')
    if source[POINTER:POINTER + 4] != (0x08000000 + BLOCK).to_bytes(4, 'little'):raise ValueError(KEY + ' block pointer')
    final, raw_sha = title_block(source)
    reason = 'subchip screen title 서브칩 redrawn like 장비 (Galmuri7, 8-px advance; replaces the 073 drawing)'
    patches = [p for p in key_patches if not (p[0] == BLOCK and p[2].startswith('graphics073' + TAG))]
    if len(patches) != len(key_patches) - 1:raise ValueError(KEY + ' 073 patch not found once')
    patches.append((BLOCK, final, KEY + TAG + reason))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], raw_sha256=raw_sha, replaces='graphics073',
                        graphics=[dict(offset=BLOCK, size=len(final), reason=reason, preceding_hex=base[BLOCK:BLOCK_END].hex(),
                                       final_hex=final.hex(), base_hex=source[BLOCK:BLOCK_END].hex())],
                        runtime='pending emulator check: subchip title like 장비')
    return appended, patches, keymeta


def predecessor_view(source, target, keymeta):
    target = bytearray(target)
    for r in keymeta[KEY]['graphics']:
        o, n = r['offset'], r['size']
        if target[o:o + n] != bytes.fromhex(r['final_hex']):raise ValueError(KEY + ' region final %X' % o)
        target[o:o + n] = bytes.fromhex(r['preceding_hex'])
    return bytes(target)


def verify(source, target, keymeta):
    k = keymeta[KEY]
    for r in k['graphics']:
        if target[r['offset']:r['offset'] + r['size']] != bytes.fromhex(r['final_hex']):raise ValueError(KEY + ' region bytes')
    if sha(decompress(target, BLOCK)[0]) != k['raw_sha256']:raise ValueError(KEY + ' decompressed title')
    return True
