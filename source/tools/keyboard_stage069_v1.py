"""Stage 069 (no new text units): fixed-cell buffer prints decode format A, over the 068 ROM.

* hangul_keyboard_hooks_v2.fcopy appended after the predecessor's append area;
* the IWRAM fixed-cell parser image's only memcpy literal (ROM 0x1EF96C) points at fcopy, so the keyboard input
  box (descriptor 0) and the profile confirmation screen show Hangul (068 runtime probe showed kana bytes).
Every region is recorded like the graphics stages (preceding_hex = 067 bytes, final_hex, base_hex) so the generated
build's predecessor views and the 034..036 'nolabel' view restore them; the appended blob lies past every
predecessor length and is checked by hash.
"""
import json
from build_visibility_poc import ROOT, sha
import hangul_keyboard_hooks_v2 as K2

KEY = 'keyboard069'
PREDECESSOR = 'poc/output/pending500_068_v1.gba'
TAG = ' graphic fix: '


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    appended = bytearray(appended);appended.extend(b'\xff' * (-(len(source) + len(appended)) % 4))
    at = len(source) + len(appended);blob, _ = K2.build_fcopy(0x08000000 + at);appended.extend(blob);entries = dict(fcopy=at)
    if len(source) + len(appended) > 0x02000000:raise ValueError(KEY + ' ROM extent')
    regions = K2.patches(source, at);info = None
    out = [];patches = list(key_patches)
    for o, final, reason in regions:
        preceding = base[o:o + len(final)]
        patches.append((o, final, KEY + TAG + reason))
        out.append(dict(offset=o, size=len(final), reason=reason, preceding_hex=preceding.hex(), final_hex=final.hex(), base_hex=preceding.hex()))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], graphics=out, page=info,
                        hooks=dict(offset=at, bytes=len(blob), sha256=sha(blob), entries={k: v for k, v in entries.items()}),
                        record_format='hangul_record_v3', runtime='pending emulator check of input box / confirmation screen')
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
    h = k['hooks']
    if sha(target[h['offset']:h['offset'] + h['bytes']]) != h['sha256']:raise ValueError(KEY + ' hook blob')
    return True
