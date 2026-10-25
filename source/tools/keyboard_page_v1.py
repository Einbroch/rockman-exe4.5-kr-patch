"""Keyboard page 0 (hiragana) -> jamo page, merged per 8x8 cell over the predecessor ROM's page.

Page 0 is a raw bank 0x63ABF4 (9600 bytes, uploaded to 0x06008000 by descriptor 0x356E8) and a raw 30x20 map
0x6412D4. Codex's candidate (analysis/hangul_keyboard_v1/kana_replacement page0_tiles/map, built from the original
ROM) changes only cells in columns 2..23 (the editable grid); the earlier native-keyboard-label stage changed only
columns 24..27 (command labels). Cells that the candidate changes are taken from it, every other cell keeps the
predecessor's tile/flip/palette. Candidate tiles are matched to existing tiles or written into slots that no longer
have any reference. Bank size and both addresses are unchanged.
"""
import json
from build_visibility_poc import ROOT, sha

BANK, BANK_SIZE, MAP, W, H = 0x63ABF4, 9600, 0x6412D4, 30, 20
CAND = ROOT / 'analysis/hangul_keyboard_v1/kana_replacement'


def _tile(bank, e):
    return bank[(e & 1023) * 32:(e & 1023) * 32 + 32]


def build(source, prev):
    rep = json.loads((CAND / 'report.json').read_text(encoding='utf-8'))
    ctiles, cmap = (CAND / 'page0_tiles.bin').read_bytes(), (CAND / 'page0_map.bin').read_bytes()
    for name, data in (('page0_tiles.bin', ctiles), ('page0_map.bin', cmap)):
        if sha(data) != rep['artifacts'][name]:raise ValueError('candidate artifact drift ' + name)
    sbank, smap = source[BANK:BANK + BANK_SIZE], source[MAP:MAP + W * H * 2]
    pbank, pmap = bytearray(prev[BANK:BANK + BANK_SIZE]), bytearray(prev[MAP:MAP + W * H * 2])
    ent = lambda m, i: int.from_bytes(m[2 * i:2 * i + 2], 'little')
    def cell(bank, m, i):e = ent(m, i);return (e & 0xFC00, _tile(bank, e))
    take = [i for i in range(W * H) if cell(ctiles, cmap, i) != cell(sbank, smap, i)]
    keep = [i for i in range(W * H) if cell(pbank, pmap, i) != cell(sbank, smap, i)]
    if set(take) & set(keep) or any(not 2 <= i % W <= 23 for i in take):raise ValueError('candidate/predecessor cells overlap')
    used = {ent(pmap, i) & 1023 for i in range(W * H) if i not in take}
    free = [t for t in range(BANK_SIZE // 32) if t not in used]
    index = {bytes(pbank[t * 32:t * 32 + 32]): t for t in sorted(used)}
    for i in take:
        e = ent(cmap, i);data = _tile(ctiles, e)
        if data not in index:
            if not free:raise ValueError('page 0 tile slots exhausted')
            t = free.pop(0);pbank[t * 32:t * 32 + 32] = data;index[data] = t
        pmap[2 * i:2 * i + 2] = ((e & 0xFC00) | index[data]).to_bytes(2, 'little')
    return bytes(pbank), bytes(pmap), dict(cells_from_candidate=len(take), cells_kept=len(keep), free_slots_left=len(free))


def patches(source, prev):
    bank, mp, info = build(source, prev)
    return [(BANK, bank, 'keyboard page 0 jamo grid (tiles)'), (MAP, mp, 'keyboard page 0 jamo grid (map)')], info
