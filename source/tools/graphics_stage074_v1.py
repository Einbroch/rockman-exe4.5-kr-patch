"""Stage 074 (no new text units): battle popup words 「アタック」 -> 「어택」 and 「ナビ」 -> 「내비」, over the 073 ROM.

User report 2026-10-25 (mGBA): using アタック+10 in battle shows 「アタック / +10」 above the player. Captured in
battle with a copy of the user's save (poc/runtime/rt072-bat-03): OBJ 20 (32x8, tiles 724..727) is the word and
OBJ 19 (tiles 728..731) the amount. The word tiles are raw 4bpp in ROM at 0x770080 (sheet tile 4; the +10..+90
amounts follow from 0x770140). Sheet row: アタック at x0..23 (tiles 4..6), ナビ (Navi+N chips) at x29..43.
Lettering is ink 7 with an 8-neighbour outline 8 on transparent 0, like the kana; ink rows 1..6. Only pixels
inside each word's box are rewritten; the amounts are untouched.
"""
import json
from build_visibility_poc import ROOT, sha

KEY = 'graphics074'
PREDECESSOR = 'poc/output/pending500_073_v1.gba'
TAG = ' graphic fix: '
SHEET, FIRST, TILES = 0x770080, 4, 6          # tiles 4..9 hold both words
INK, EDGE, CLEAR = 7, 8, 0
WORDS = [(0, 24, 2, [['.##...#', '#..#..#', '#..#.##', '#..#..#', '.##...#', '......#'],          # 어
                     ['####.#.#', '###..###', '####.#.#', '........', '#######.', '......#.']]),        # 택
         (28, 44, 29, [['...#.#', '#..#.#', '#..###', '#..#.#', '##.#.#', '...#.#'],              # 내
                       ['#..#.#', '####.#', '#..#.#', '####.#', '.....#', '.....#']])]            # 비
GAP = {0: 2, 28: 1}   # per word box


def at(x, y):
    return SHEET + (x // 8) * 32 + y * 4 + (x % 8) // 2


def pixel(rom, x, y):
    b = rom[at(x, y)];return (b >> 4) if x & 1 else b & 15


def sheet(source):
    w = TILES * 8
    px = [[pixel(source, x, y) for x in range(w)] for y in range(8)]
    for lo, hi, ink_x, glyphs in WORDS:
        box = {px[y][x] for y in range(8) for x in range(lo, hi)}
        if box != {INK, EDGE, CLEAR}:raise ValueError(KEY + ' word box colours')
        if any(px[y][x] != CLEAR for y in range(8) for x in (lo - 1, hi) if 0 <= x < w and not any(l <= x < h for l, h, _, _ in WORDS)):raise ValueError(KEY + ' word box edge')
        ink, pen = set(), ink_x
        for g in glyphs:
            if len(g) != 6 or len({len(r) for r in g}) != 1:raise ValueError(KEY + ' glyph shape')
            ink |= {(pen + x, 1 + y) for y, r in enumerate(g) for x, c in enumerate(r) if c == '#'}
            pen += len(g[0]) + GAP[lo]
        for y in range(8):
            for x in range(lo, hi):
                near = any((x + dx, y + dy) in ink for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                px[y][x] = INK if (x, y) in ink else EDGE if near else CLEAR
        if min(x for x, _ in ink) - 1 < lo or max(x for x, _ in ink) + 1 >= hi:raise ValueError(KEY + ' word overflow')
    out = bytearray(TILES * 32)
    for y in range(8):
        for x in range(0, w, 2):out[at(x, y) - SHEET] = px[y][x] | px[y][x + 1] << 4
    return bytes(out)


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    n = TILES * 32
    if base[SHEET:SHEET + n] != source[SHEET:SHEET + n]:raise ValueError(KEY + ' sheet already modified')
    final = sheet(source)
    reason = 'battle popup words アタック -> 어택, ナビ -> 내비 (raw OBJ sheet 0x770080, tiles 4..9)'
    patches = list(key_patches);patches.append((SHEET, final, KEY + TAG + reason))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'],
                        graphics=[dict(offset=SHEET, size=n, reason=reason, preceding_hex=base[SHEET:SHEET + n].hex(),
                                       final_hex=final.hex(), base_hex=source[SHEET:SHEET + n].hex())],
                        runtime='pending emulator check: battle popup shows 어택 / +10')
    return appended, patches, keymeta


def predecessor_view(source, target, keymeta):
    target = bytearray(target)
    for r in keymeta[KEY]['graphics']:
        o, n = r['offset'], r['size']
        if target[o:o + n] != bytes.fromhex(r['final_hex']):raise ValueError(KEY + ' region final %X' % o)
        target[o:o + n] = bytes.fromhex(r['preceding_hex'])
    return bytes(target)


def verify(source, target, keymeta):
    for r in keymeta[KEY]['graphics']:
        if target[r['offset']:r['offset'] + r['size']] != bytes.fromhex(r['final_hex']):raise ValueError(KEY + ' region bytes')
    return True
