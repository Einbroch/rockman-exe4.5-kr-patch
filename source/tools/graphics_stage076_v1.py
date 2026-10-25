"""Stage 076 (no new text units): clear the kana remnants under the subchip title, over the 075 ROM.

The title bar is two map rows: row 0 cols 12..17 = tiles 6..11 (redrawn by 073/075) and row 1 cols 12..17 =
tiles 17,18,18,19,20,21, whose top two pixel rows hold the bottom of サブチップ (ink 11/12 on 13). 075 left them, so
yellow pieces showed under 서브칩 (poc/runtime/rt075-sav-03). Tiles 17..21 are used only there (BG1/BG2 maps of the
subchip screen, poc/runtime/rt072-sav-03); their rows 0..1 become background 13. Tile 18 is shared by two cells, so
the glyphs stay in the row-0 tiles. Same LZ77 block as 073/075; the 075 patch is replaced and the 073/075 region
checks read this stage's predecessor view (make_graphics_stage076_v1.py).
"""
import json
from build_visibility_poc import ROOT, sha
from gba_lz77_v1 import compress, decompress
from graphics_stage073_v1 import BLOCK, BLOCK_END, BG
import graphics_stage075_v1

KEY = 'graphics076'
PREDECESSOR = 'poc/output/pending500_075_v1.gba'
TAG = ' graphic fix: '
LOWER_TILES, LOWER_ROWS, TEXT_INKS = range(17, 22), range(2), {11, 12}


def title_block(source):
    final075, _ = graphics_stage075_v1.title_block(source)
    raw = bytearray(decompress(final075, 0)[0]);seen = set()
    for t in LOWER_TILES:
        for y in range(8):
            for x in range(8):
                o = 4 + (t - 1) * 32 + y * 4 + x // 2;v = (raw[o] >> 4) if x & 1 else raw[o] & 15
                if y in LOWER_ROWS:
                    seen.add(v)
                    if v in TEXT_INKS:raw[o] = (raw[o] & 0x0F) | BG << 4 if x & 1 else (raw[o] & 0xF0) | BG
                elif y < 4 and v != BG:raise ValueError(KEY + ' lower tile layout')
    if seen != {BG} | TEXT_INKS:raise ValueError(KEY + ' lower tile colours')
    packed = compress(bytes(raw))
    if len(packed) > BLOCK_END - BLOCK:raise ValueError(KEY + ' recompressed block too large')
    return packed + bytes(BLOCK_END - BLOCK - len(packed)), sha(bytes(raw))


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    prior = keymeta['graphics075']['graphics'][0]
    if (prior['offset'], prior['size']) != (BLOCK, BLOCK_END - BLOCK) or base[BLOCK:BLOCK_END].hex() != prior['final_hex']:raise ValueError(KEY + ' 075 block state')
    final, raw_sha = title_block(source)
    reason = 'subchip title: clear the サブチップ remnants in the row-1 tiles 17..21 (replaces the 075 drawing of this block)'
    patches = [p for p in key_patches if not (p[0] == BLOCK and p[2].startswith('graphics075' + TAG))]
    if len(patches) != len(key_patches) - 1:raise ValueError(KEY + ' 075 patch not found once')
    patches.append((BLOCK, final, KEY + TAG + reason))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], raw_sha256=raw_sha, replaces='graphics075',
                        graphics=[dict(offset=BLOCK, size=len(final), reason=reason, preceding_hex=base[BLOCK:BLOCK_END].hex(),
                                       final_hex=final.hex(), base_hex=source[BLOCK:BLOCK_END].hex())],
                        runtime='pending emulator check: no yellow pieces under 서브칩')
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
