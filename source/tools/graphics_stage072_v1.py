"""Stage 072 (no new text units): Data Library P.A memo card label 「パターン」 -> 「패턴」, over the 071 ROM.

User report 2026-10-25 (mGBA): the P.A memo card shows 「●パターン ?/?」. The label is OBJ (32x8, 4 tiles) from the
LZ77 sprite block 0x6D8188 (pointer 0x0804280C, 6,108 bytes raw), tiles at raw +5508..+5636 (ink 14 on 7). The
lettering is hand drawn with 2-px strokes like the kana; the block is recompressed in place (original 1,173 of the 1,176 bytes
before the next block 0x6D8620) and the tail is zero padding; 패 at x1, 턴 at x18 is the spacing that fits (1,176 bytes). The ?/? digits are separate OBJ and stay.

Second user report the same day (mGBA): the chip-get line prints 「メットガード1」. The dialogue name command reads the
pool table 0x08051660 (+0 items 778B08, +4 chips 765190, +8 chips 765B18) and copies 0x80 bytes, so the chip roots
0x51664/0x51668 now point at the existing Korean library clones (same script counts). The 065 item redirect
(batch_label_v4) never took effect: it looked the 058 clone up in keymeta archives that are filled only when the build
finalizes, so all six 778B08 literals still held the source address; they point at the 058 clone here.
"""
import json
from build_visibility_poc import ROOT, sha
from gba_lz77_v1 import compress, decompress

KEY = 'graphics072'
PREDECESSOR = 'poc/output/pending500_071_v1.gba'
TAG = ' graphic fix: '
BLOCK, BLOCK_END = 0x6D8188, 0x6D8620
ITEM_LITERALS = (0x349C4, 0x419B8, 0x4CA10, 0x4CB0C, 0x51660, 0xD2A98)
CHIP_LITERALS = ((0x51664, 0x765190, 'clone_offset', 'clone'), (0x51668, 0x765B18, 'secondary_clone_offset', 'secondary_clone'))
LABEL_AT, BG, INK = 5508, 7, 14
PAE = ['.########.##.##',
       '..##..##..##.##',
       '..##..##..##.##',
       '..##..##..#####',
       '..##..##..##.##',
       '#########.##.##',
       '..........##.##',
       '..........##.##']
TEON = ['#######..##',
        '##.......##',
        '###########',
        '##.......##',
        '#######..##',
        '.##........',
        '.##........',
        '.##########']


def pixel(raw, x, y):
    b = raw[LABEL_AT + (x // 8) * 32 + y * 4 + (x % 8) // 2];return (b >> 4) if x & 1 else b & 15


def label_block(source):
    raw, used = decompress(source, BLOCK)
    if (len(raw), used) != (6108, 1173) or any(source[BLOCK + used:BLOCK_END]):raise ValueError(KEY + ' block layout')
    if {pixel(raw, x, y) for x in range(32) for y in range(8)} != {BG, 12, INK}:raise ValueError(KEY + ' label colours')   # 12 = the handakuten of パ
    rows = [['.'] * 32 for _ in range(8)]
    for y in range(8):
        for x, c in enumerate(PAE[y]):rows[y][1 + x] = c
        for x, c in enumerate(TEON[y]):rows[y][18 + x] = c
    out = bytearray(raw)
    for y in range(8):
        for x in range(0, 32, 2):
            lo, hi = (INK if rows[y][x + k] == '#' else BG for k in (0, 1))
            out[LABEL_AT + (x // 8) * 32 + y * 4 + (x % 8) // 2] = lo | hi << 4
    if out[:LABEL_AT] != raw[:LABEL_AT] or out[LABEL_AT + 128:] != raw[LABEL_AT + 128:]:raise ValueError(KEY + ' protected tiles')
    packed = compress(bytes(out))
    if len(packed) > BLOCK_END - BLOCK:raise ValueError(KEY + ' recompressed block too large')
    return packed + bytes(BLOCK_END - BLOCK - len(packed)), sha(bytes(out))


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    if base[BLOCK:BLOCK_END] != source[BLOCK:BLOCK_END]:raise ValueError(KEY + ' block already modified')
    if source[0x4280C:0x42810] != (0x08000000 + BLOCK).to_bytes(4, 'little'):raise ValueError(KEY + ' block pointer')
    final, raw_sha = label_block(source)
    reason = 'Data Library P.A memo label パターン -> 패턴 (LZ77 sprite block, recompressed in place)'
    regions = [(BLOCK, final, reason)];clones = []
    item = [r for r in meta['keyitem_rom']['typed058']['archives'] if r['archive'] == '778B08']
    if len(item) != 1 or any(r['archive'] == '778B08' for k, v in meta['keyitem_rom'].items()
                             if k != 'typed058' and isinstance(v, dict) for r in v.get('archives', []) or []):raise ValueError(KEY + ' item clone not unique')
    item = item[0];clones.append(dict(root=0x778B08, offset=item['rom_offset'], size=item['compiled_bytes'], sha256=item['compiled_sha256']))
    for at in ITEM_LITERALS:regions.append((at, (0x08000000 + item['rom_offset']).to_bytes(4, 'little'), 'item names 778B08 -> 058 Korean clone (065 redirect never applied)'))
    e = meta['chip_library_extension']
    for at, root, field, body in CHIP_LITERALS:
        clones.append(dict(root=root, offset=e[field], size=e[body]['clone_bytes'], sha256=e[body]['clone_sha256']))
        regions.append((at, (0x08000000 + e[field]).to_bytes(4, 'little'), 'dialogue chip names %X -> Korean library clone' % root))
    for c in clones:
        if sha(base[c['offset']:c['offset'] + c['size']]) != c['sha256']:raise ValueError(KEY + ' clone bytes %X' % c['root'])
        if base[c['offset']:c['offset'] + 2] != source[c['root']:c['root'] + 2]:raise ValueError(KEY + ' clone script count %X' % c['root'])
    for at, _, _ in regions[1:]:
        if base[at:at + 4] != source[at:at + 4] or source[at:at + 4] not in {(0x08000000 + c['root']).to_bytes(4, 'little') for c in clones}:raise ValueError(KEY + ' literal %X' % at)
    import batch_label_v3   # the final catalog audit accepts a changed root pointer only from this set
    batch_label_v3.REDIRECT_POINTERS = batch_label_v3.REDIRECT_POINTERS | {at for at, _, _ in regions[1:]}
    patches = list(key_patches);out = []
    for o, b, why in regions:
        patches.append((o, b, KEY + TAG + why))
        out.append(dict(offset=o, size=len(b), reason=why, preceding_hex=base[o:o + len(b)].hex(), final_hex=b.hex(), base_hex=source[o:o + len(b)].hex()))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], raw_sha256=raw_sha, graphics=out, clones=clones,
                        runtime='pending emulator check: P.A memo card shows 패턴; chip-get line shows the Korean chip name')
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
    if sha(decompress(target, BLOCK)[0]) != k['raw_sha256']:raise ValueError(KEY + ' decompressed label')
    for c in k['clones']:
        if sha(target[c['offset']:c['offset'] + c['size']]) != c['sha256']:raise ValueError(KEY + ' clone bytes %X' % c['root'])
    return True
