"""Stage 077 (no new text units): Numberman quiz graphics, over the 076 ROM.

User report 2026-10-26 (mGBA): the quiz start/end words are Japanese. Captured with a copy of the user's r4 save
(poc/runtime/rt075-quiz-05). Two raw OBJ sprites:
* word sprite 0x5131A4 (pointer 0x0802BA70): frames 0 スタート, 3 ごうかく, 4 クリア, 5 失敗, each with its own raw tileset
  and an OAM piece list (quiz_sprite_v1). Each frame is composed into its canvas, the word is replaced by Galmuri11
  glyphs scaled up and widened (시작/합격/클리어/실패), filled with the original's per-row colour for each checker
  parity and outlined (8-neighbour) in the original's outline colour, then split back into the same tiles.
* counter panel tiles at 0x51236C (VRAM tile 480 + k): the tab label せいかい (tiles 480..483, rows 1..7, ink 5 on 2)
  -> Galmuri7 정답, and 問 after the counter (tiles 500..507, ink 2 + shadow 6 on 1) -> Galmuri11 문 with the same
  shadow. Only those pixel boxes change.
"""
import collections, json
from build_visibility_poc import ROOT, sha
from pet_graphics_font import glyphs
import quiz_sprite_v1 as q

KEY = 'graphics077'
PREDECESSOR = 'poc/output/pending500_076_v1.gba'
TAG = ' graphic fix: '
FONT11 = 'external/fonts/Galmuri11.bdf'
WORDS = {0: ('スタート', '시작', 3, 2, 4), 3: ('ごうかく', '합격', 3, 2, 4), 4: ('クリア', '클리어', 2, 2, 4), 5: ('失敗', '실패', 2, 1, 3)}  # frame: source, text, x scale, extra width, gap
PANEL, PANEL_TILE, PANEL_TILES = 0x51236C, 480, 68


def bdf(path, chars):
    out = {}
    for b in (ROOT / path).read_text(encoding='utf8', errors='replace').split('STARTCHAR ')[1:]:
        L = b.splitlines();ch = chr(int(next(l.split()[1] for l in L if l.startswith('ENCODING '))))
        if ch not in chars:continue
        w, h, xo, yo = map(int, next(l for l in L if l.startswith('BBX ')).split()[1:]);i = L.index('BITMAP') + 1;nb = len(L[i]) * 4
        out[ch] = dict(w=w, h=h, xo=xo, yo=yo, rows=[[(int(r, 16) >> (nb - 1 - x)) & 1 for x in range(w)] for r in L[i:i + h]])
    if set(out) != set(chars):raise ValueError(KEY + ' Galmuri11 glyph missing')
    return out


def word(rom, k, text, sx, extra, gap, g11):
    f = q.frame(rom, k);px, origin = q.canvas(rom, f);H, W = len(px), len(px[0])
    ink = {(x, y) for y in range(H) for x in range(W) if px[y][x]}
    edge = {(x, y) for x, y in ink if any((x + dx, y + dy) not in ink for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    oc = collections.Counter(px[y][x] for x, y in edge).most_common(1)[0][0]
    top, bot = min(y for _, y in ink), max(y for _, y in ink);fill = {}
    for y in range(top, bot + 1):
        for par in (0, 1):
            c = collections.Counter(px[y][x] for x in range(W) if (x, y) in ink and (x, y) not in edge and (x + y) % 2 == par and px[y][x] != oc)
            fill[(y, par)] = c.most_common(1)[0][0] if c else None
    mask, pen = set(), 0
    for ch in text:
        gl = g11[ch]
        for yy, r in enumerate(gl['rows']):
            for xx, v in enumerate(r):
                if v:mask |= {(pen + (gl['xo'] + xx) * sx + a, (11 - gl['h'] - gl['yo'] + yy) * 2 + b) for a in range(sx) for b in range(2)}
        pen += (gl['w'] + gl['xo']) * sx + gap
    for _ in range(extra):mask |= {(x + 1, y) for x, y in mask}
    mx0, mx1 = min(x for x, _ in mask), max(x for x, _ in mask);my0, my1 = min(y for _, y in mask), max(y for _, y in mask)
    dx, dy = (W - (mx1 - mx0 + 1)) // 2 - mx0, top + 1 + ((bot - top - 1) - (my1 - my0 + 1)) // 2 - my0
    mask = {(x + dx, y + dy) for x, y in mask}
    if min(x for x, _ in mask) < 1 or max(x for x, _ in mask) > W - 2 or min(y for _, y in mask) < 1 or max(y for _, y in mask) > H - 2:raise ValueError(KEY + ' word overflow ' + text)
    t2, b2 = dy + my0, dy + my1;out = [[0] * W for _ in range(H)]
    for x, y in mask:
        ry = top + 1 + round((y - t2) * (bot - top - 2) / max(1, b2 - t2))
        out[y][x] = fill.get((ry, (x + y) % 2)) or fill.get((ry, 1 - (x + y) % 2)) or oc
    for y in range(H):
        for x in range(W):
            if (x, y) not in mask and any((x + a, y + b) in mask for a in (-1, 0, 1) for b in (-1, 0, 1)):out[y][x] = oc
    data = rom[f['tiles']:f['tiles'] + f['ntiles'] * 32]
    if q.split(f, px, origin, data) != data:raise ValueError(KEY + ' canvas roundtrip ' + text)
    return f['tiles'], q.split(f, out, origin, data)


def ppx(buf, k, x, y):
    b = buf[(k - PANEL_TILE) * 32 + y * 4 + x // 2];return (b >> 4) if x & 1 else b & 15


def pset(buf, k, x, y, v):
    o = (k - PANEL_TILE) * 32 + y * 4 + x // 2;buf[o] = (buf[o] & 0x0F) | v << 4 if x & 1 else (buf[o] & 0xF0) | v


def panel(rom, g11):
    buf = bytearray(rom[PANEL:PANEL + PANEL_TILES * 32])
    # 정답 on the tab: tiles 480..483 (32x8), rows 1..7, ink 5 on 2 (row 0 is the border)
    g7 = glyphs(json.loads((ROOT / 'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8')), extra_characters='정답')
    tab = lambda x, y: (480 + x // 8, x % 8, y)
    if {ppx(buf, *tab(x, y)) for x in range(32) for y in range(1, 8)} != {2, 3, 4, 5}:raise ValueError(KEY + ' tab colours')
    pts, pen = [], 0
    for ch in '정답':
        gl = g7[ch]
        for y, bits in enumerate(gl['bits']):
            pts += [(pen + x, gl['top'] + y) for x in range(gl['width']) if bits & (1 << (7 - x))]
        pen += 8
    x0 = 3 + (28 - (max(x for x, _ in pts) + 1)) // 2
    for x in range(32):
        for y in range(1, 8):pset(buf, *tab(x, y), 2)
    for x, y in pts:pset(buf, *tab(x + x0, y), 5)
    # 문 after the counter: OBJ 32x16 = tiles 500..507 (two rows of four), box x16..29, rows 3..14, ink 2 shadow 6 on 1
    cell = lambda x, y: (500 + (y // 8) * 4 + x // 8, x % 8, y % 8)
    box = [(x, y) for x in range(16, 30) for y in range(3, 15)]
    if {ppx(buf, *cell(x, y)) for x, y in box} != {1, 2, 6}:raise ValueError(KEY + ' counter suffix colours')
    gl = g11['문'];ink = {(x, y) for y, r in enumerate(gl['rows']) for x, v in enumerate(r) if v}
    ox, oy = 17 + (11 - gl['w']) // 2, 4 + (10 - gl['h']) // 2
    ink = {(x + ox, y + oy) for x, y in ink}
    if not all(16 <= x <= 28 and 3 <= y <= 13 for x, y in ink):raise ValueError(KEY + ' 문 box')
    for x, y in box:pset(buf, *cell(x, y), 1)
    for x, y in ink:
        if (x + 1, y + 1) not in ink:pset(buf, *cell(x + 1, y + 1), 6)
    for x, y in ink:pset(buf, *cell(x, y), 2)
    return PANEL, bytes(buf)


def regions(rom):
    g11 = bdf(FONT11, '시작합격클리어실패문')
    out = [word(rom, k, text, sx, extra, gap, g11) + ('quiz word %s -> %s' % (src, text),) for k, (src, text, sx, extra, gap) in WORDS.items()]
    return out + [panel(rom, g11) + ('quiz counter panel せいかい -> 정답, 問 -> 문',)]


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    if source[0x2BA70:0x2BA74] != (0x08000000 + q.ARCHIVE).to_bytes(4, 'little'):raise ValueError(KEY + ' word sprite pointer')
    patches = list(key_patches);out = []
    for o, final, reason in regions(source):
        if base[o:o + len(final)] != source[o:o + len(final)]:raise ValueError(KEY + ' region already modified %X' % o)
        patches.append((o, final, KEY + TAG + reason))
        out.append(dict(offset=o, size=len(final), reason=reason, preceding_hex=base[o:o + len(final)].hex(), final_hex=final.hex(), base_hex=source[o:o + len(final)].hex()))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], graphics=out,
                        font=dict(path=FONT11, sha256=sha((ROOT / FONT11).read_bytes())),
                        runtime='pending emulator check: quiz start/result words and counter panel')
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
