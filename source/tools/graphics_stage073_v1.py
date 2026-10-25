"""Stage 073 (no new text units): subchip screen header 「サブチップ」 -> 「서브칩」, over the 072 ROM.

User report 2026-10-25 (mGBA): the subchip screen title bar still shows kana. It is BG1 (char base 0) map row 0
cols 12..17 = tiles 6..11, loaded from the LZ77 block 0x6FB82C (pointer 0x08041E98, 2,884 bytes raw: a 4-byte size
header then tiles from VRAM tile 1, so tile n is raw +4+(n-1)*32). Row 0 of the six tiles is the bar's top line
(colour 15) and stays; rows 1..7 are redrawn as background 13 with hand-drawn 서/브/칩 in ink 11, 2-px verticals
like the kana (Galmuri7 at this size came out about half the kana's weight). The block is recompressed in place: the original stream is 1,036 bytes and the
next block starts right after it (0x6FBC38), the tail of the region is zero padding.
Found from a runtime capture with a copy of the user's save (poc/runtime/rt072-sav-03).
"""
import json
from build_visibility_poc import ROOT, sha
from gba_lz77_v1 import compress, decompress

KEY = 'graphics073'
PREDECESSOR = 'poc/output/pending500_072_v1.gba'
TAG = ' graphic fix: '
BLOCK, BLOCK_END, POINTER = 0x6FB82C, 0x6FBC38, 0x41E98
FIRST_TILE, TILES, BORDER, BG, INK = 6, 6, 15, 13, 11
GLYPHS = [['..##.....##',      # 서
           '..##.....##',
           '.####....##',
           '.#..#..####',
           '##..##...##',
           '#....#...##',
           '.........##'],
          ['.##.....##.',      # 브
           '.#########.',
           '.##.....##.',
           '.#########.',
           '...........',
           '###########',
           '...........'],
          ['...##....##',      # 칩
           '#######..##',
           '.##..##..##',
           '##....##.##',
           '.#....#....',
           '.######....',
           '.######....']]
GAP = 2


def at(x, y):
    return 4 + (FIRST_TILE - 1 + x // 8) * 32 + y * 4 + (x % 8) // 2


def pixel(raw, x, y):
    b = raw[at(x, y)];return (b >> 4) if x & 1 else b & 15


def title_block(source):
    raw, used = decompress(source, BLOCK)
    if (len(raw), used, BLOCK + used) != (2884, 1036, BLOCK_END) or source[BLOCK_END] != 0x10:raise ValueError(KEY + ' block layout')
    w = TILES * 8
    if {pixel(raw, x, 0) for x in range(w)} != {BORDER} or {pixel(raw, x, y) for x in range(w) for y in range(1, 8)} != {BG, 11, 12}:raise ValueError(KEY + ' title colours')
    points, pen = [], 0
    for gl in GLYPHS:
        if len(gl) != 7 or len({len(r) for r in gl}) != 1:raise ValueError(KEY + ' glyph shape')
        points += [(pen + x, 1 + y) for y, r in enumerate(gl) for x, c in enumerate(r) if c == '#']
        pen += len(gl[0]) + GAP
    width = pen - GAP;x0 = (w - width) // 2
    rows = [[BG] * w for _ in range(8)]
    for x, y in points:rows[y][x + x0] = INK
    out = bytearray(raw)
    for y in range(1, 8):
        for x in range(0, w, 2):out[at(x, y)] = rows[y][x] | rows[y][x + 1] << 4
    lo, hi = at(0, 0), at(w - 1, 7) + 1
    if out[:4 + (FIRST_TILE - 1) * 32] != raw[:4 + (FIRST_TILE - 1) * 32] or out[4 + (FIRST_TILE - 1 + TILES) * 32:] != raw[4 + (FIRST_TILE - 1 + TILES) * 32:]:raise ValueError(KEY + ' protected tiles')
    packed = compress(bytes(out))
    if len(packed) > BLOCK_END - BLOCK:raise ValueError(KEY + ' recompressed block too large')
    return packed + bytes(BLOCK_END - BLOCK - len(packed)), sha(bytes(out))


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    if base[BLOCK:BLOCK_END] != source[BLOCK:BLOCK_END]:raise ValueError(KEY + ' block already modified')
    if source[POINTER:POINTER + 4] != (0x08000000 + BLOCK).to_bytes(4, 'little'):raise ValueError(KEY + ' block pointer')
    final, raw_sha = title_block(source)
    reason = 'subchip screen title サブチップ -> 서브칩 (LZ77 BG tile block, recompressed in place)'
    patches = list(key_patches);patches.append((BLOCK, final, KEY + TAG + reason))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], raw_sha256=raw_sha,
                        graphics=[dict(offset=BLOCK, size=len(final), reason=reason, preceding_hex=base[BLOCK:BLOCK_END].hex(),
                                       final_hex=final.hex(), base_hex=source[BLOCK:BLOCK_END].hex())],
                        runtime='pending emulator check: subchip screen title shows 서브칩')
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
