"""Stage 070 (no new text units): confirm guard (hangul_keyboard_hooks_v3) over the 069 ROM.

User decision 2026-10-25: confirming while a lone jamo is left is refused with a sound. The guard is appended and
the 0x080353B0 stub (owned by stage 068) is re-pointed at it; 068's stub patch is replaced in the carried patch
list, so the generated build gives 068's view/verify the 070-restored image.
Every region is recorded like the graphics stages (preceding_hex = 067 bytes, final_hex, base_hex) so the generated
build's predecessor views and the 034..036 'nolabel' view restore them; the appended blob lies past every
predecessor length and is checked by hash.
"""
import json
from build_visibility_poc import ROOT, sha
import hangul_keyboard_hooks_v1 as K1
import hangul_keyboard_hooks_v3 as K3

KEY = 'keyboard070'
PREDECESSOR = 'poc/output/pending500_069_v1.gba'
TAG = ' graphic fix: '


def install(source, appended, key_patches, keymeta):
    path = ROOT / PREDECESSOR;meta = json.loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base = path.read_bytes()
    if sha(base) != meta['output_sha256']:raise ValueError(KEY + ' predecessor hash')
    appended = bytearray(appended);appended.extend(b'\xff' * (-(len(source) + len(appended)) % 4))
    keys1 = 0x08000000 + keymeta['keyboard068']['hooks']['entries']['keys']
    at = len(source) + len(appended);blob, _ = K3.build_guard(0x08000000 + at, keys1);appended.extend(blob);entries = dict(guard=at)
    if len(source) + len(appended) > 0x02000000:raise ValueError(KEY + ' ROM extent')
    site = K1.SITES['keys'][0];info = None
    if base[site:site + 12] != K1.stub(keys1):raise ValueError(KEY + ' 068 keys stub expected')
    regions = [(site, K1.stub(0x08000000 + at), 'A/B handler stub -> confirm guard')]
    out = [];patches = [p for p in key_patches if p[0] != K1.SITES['keys'][0]]
    if len(patches) != len(key_patches) - 1:raise ValueError(KEY + ' carried 068 stub patch')
    earlier = {(r['offset'], r['size']): r['base_hex'] for v in keymeta.values() if isinstance(v, dict) for r in v.get('graphics', [])}
    for o, final, reason in regions:
        preceding = base[o:o + len(final)]
        patches.append((o, final, KEY + TAG + reason))
        # the 034..036 view restores base_hex in keymeta order; keep the oldest base for a re-patched region
        out.append(dict(offset=o, size=len(final), reason=reason, preceding_hex=preceding.hex(), final_hex=final.hex(), base_hex=earlier.get((o, len(final)), preceding.hex())))
    keymeta = dict(keymeta)
    keymeta[KEY] = dict(predecessor=PREDECESSOR, predecessor_sha256=meta['output_sha256'], graphics=out, page=info,
                        hooks=dict(offset=at, bytes=len(blob), sha256=sha(blob), entries={k: v for k, v in entries.items()}),
                        record_format='hangul_record_v3', runtime='pending emulator check: lone jamo confirm refused')
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
