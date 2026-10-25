"""Version read-only hint tracing; do not transfer037 runtime evidence to038."""
from build_visibility_poc import ROOT, sha
from cumulative_batch500 import read, frozen_write

base = ROOT/'tools/capture_hint_observe037_v1.py'
dst = ROOT/'tools/capture_hint_observe038_v1.py'
if dst.exists():
    raise ValueError('Preserve existing038 observer')
text = base.read_text(encoding='utf8')
text = text.replace('037', '038')
dst.write_text(text, encoding='utf8')
frozen_write(ROOT/'tools/specs/hint_observer038_v1_version.json', dict(
    base=str(base.relative_to(ROOT)), base_sha256=sha(base.read_bytes()),
    replacement=['037','038'], output=str(dst.relative_to(ROOT)),
    output_sha256=sha(dst.read_bytes()),
    scope='Read-only hint provider/caller trace; actual038 ROM and own038 state required. No aliases, memory writes or transferred037 proof.'))

folder = ROOT/'poc/runtime/pending500-037-hint-controls-observe-v2'
r = read(folder/'result.json')
e = read(folder/'hint_entries.json')['entries']
if not r['complete'] or r['rom_sha256'] != 'b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd':
    raise ValueError('037 observation identity')
if [x['pc'] for x in e] != [0x0806A818,0x0804F7FC] or any(x['script_provider'] != 0 or x['Navi'] != 0 for x in e):
    raise ValueError('Original L hint route differs')
if e[1]['registers']['0'] != 0 or e[1]['registers']['14'] != 0x0806A825:
    raise ValueError('Original hint provider ABI')
frozen_write(ROOT/'analysis/pending500_038_v2/hint_route_prerequisite037_v1.json', dict(
    passed=True, scope='037 original L controller route only; NOT038 runtime evidence',
    rom_sha256=r['rom_sha256'], actions=r['actions'],
    caller=0x0806A818, entry=0x0804F7FC, provider=0, Navi=0,
    scene=e[0]['scene'], source_alias_or_RAM_write=False,
    observation='L after field reload settled opens hint; early L during RTC reload was busy, not unsupported.',
    runtime038_tested=False, release_eligible=False,
    evidence={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in [folder/'result.json',folder/'hint_entries.json',folder/'step_001.png']}))
print('Prepared038 read-only observer; verified037 L route, not038 runtime')
