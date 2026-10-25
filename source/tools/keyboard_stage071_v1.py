"""Stage 071 (no new text units): make the jamo page cells for ㅕ and ㅗ reachable, over the 070 ROM.

User report 2026-10-25: ㅗ could not be selected. The cursor refresh 0x08035086 redirects cells listed in a skip
table (12-byte records: col,row + target per direction, 0xFF end). Pages 0 and 1 share 0x080350D8, whose first two
records skip (6,2) and (8,2), the blanks of the kana layout (や ゆ よ) where the jamo page has ㅕ and ㅗ; page 2
uses 0x0803514C. The table choice at 0x0803508C..0x08035095 (ldr/ldrb/cmp/bne/ldr) becomes
`ldrb r0,[r3,#8] / lsls r0,#2 / ldr r2,[literal 0x350D4] / ldr r2,[r2,r0] / nop` with the literal pointing at a
3-word table appended after the predecessor: page 0 -> 0x080350F0 (the shared table minus its first two records),
page 1 -> 0x080350D8, page 2 -> 0x0803514C. The loop head 0x08035096 and both other users are untouched.
"""
import json,sys
from pathlib import Path
from build_visibility_poc import ROOT, sha
sys.path.insert(0, str(ROOT / 'external/arm_debug_python'))
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB

KEY = 'keyboard071'
PREDECESSOR = 'poc/output/pending500_070_v1.gba'
TAG = ' graphic fix: '
CODE_AT, CODE_SOURCE_HEX = 0x3508C, '114a187a022800d12c4a'
LIT_AT, LIT_SOURCE_HEX = 0x350D4, 'd8500308'
SHARED, PAGE2 = 0x080350D8, 0x0803514C


def code_bytes():
    src = '.syntax unified\n.cpu arm7tdmi\n.thumb\nldrb r0,[r3,#8]\nlsls r0,r0,#2\nldr r2,[pc,#0x40]\nldr r2,[r2,r0]\nmov r8,r8\n'
    b = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(src, 0x08000000 + CODE_AT)[0])
    if len(b) != 10:raise ValueError('table select size')
    return b


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    if base[CODE_AT:CODE_AT + 10].hex() != CODE_SOURCE_HEX or base[LIT_AT:LIT_AT + 4].hex() != LIT_SOURCE_HEX:raise ValueError(KEY + ' site drift')
    if base[0x350D8:0x350DA] != b'\x06\x02' or base[0x350E4:0x350E6] != b'\x08\x02' or base[0x350F0:0x350F2] != b'\x06\x04':raise ValueError(KEY + ' skip table layout')
    appended = bytearray(appended);appended.extend(b'\xff' * (-(len(source) + len(appended)) % 4))
    at = len(source) + len(appended)
    table = b''.join(x.to_bytes(4, 'little') for x in (SHARED + 24, SHARED, PAGE2));appended.extend(table)
    regions = [(CODE_AT, code_bytes(), 'skip-table select by page (page 0 drops the (6,2)/(8,2) records)'),
               (LIT_AT, (0x08000000 + at).to_bytes(4, 'little'), 'literal -> per-page skip table pointers')]
    out = [];patches = list(key_patches)
    for o, final, reason in regions:
        preceding = base[o:o + len(final)]
        patches.append((o, final, KEY + TAG + reason))
        out.append(dict(offset=o, size=len(final), reason=reason, preceding_hex=preceding.hex(), final_hex=final.hex(), base_hex=source[o:o + len(final)].hex()))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], graphics=out,
                        pointer_table=dict(offset=at, hex=table.hex()), runtime='pending emulator check: cursor reaches ㅕ/ㅗ on page 0, page 1 still skips')
    return bytes(appended), patches, keymeta


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
    p = k['pointer_table']
    if target[p['offset']:p['offset'] + 12].hex() != p['hex']:raise ValueError(KEY + ' pointer table')
    return True
