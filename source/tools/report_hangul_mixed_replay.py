"""Bind smaller persistent mixed state to observed native96-byte lifecycle."""
import json
import re
import struct
import subprocess
import sys
from build_visibility_poc import ROOT, sha, require_hash
from hangul_mixed_replay_state import MixedReplay, SIZE, editor_candidate


def main():
    base = ROOT / 'analysis/hangul_keyboard_v1'
    deps = {}
    for name in ('lifecycle.json', 'mixed_editor_host.json'):
        p = base / name; r = json.loads(p.read_text(encoding='utf8'))
        if not r['passed'] or r['rom_integrated']: raise ValueError('evidence scope')
        for n, h in r['tools'].items(): require_hash(ROOT / 'tools' / n, h)
        deps['analysis/hangul_keyboard_v1/' + name] = sha(p.read_bytes())
    lifecycle = json.loads((base / 'lifecycle.json').read_text(encoding='utf8'))
    if lifecycle['initializer']['clear_bytes'] != 96: raise ValueError('observed clear')
    event = next(e for e in lifecycle['events'] if e['pc'] == 0x080355F4)
    native = bytes.fromhex(event['edit_hex'])
    ui = native[:16]; destination = struct.unpack_from('<I', native, 28)[0]
    c = MixedReplay(ui[4]); candidate = editor_candidate(ui, destination, c.serialize())
    if len(candidate) != 96 or candidate[:16] != native[:16] or struct.unpack_from('<I', candidate, 16)[0] != destination:
        raise ValueError('candidate preserved metadata')
    tests = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'tools/test_hangul_mixed_replay_state.py')],
                           check=True, timeout=60, capture_output=True, text=True, encoding='utf8')
    if 'Ran 5 tests' not in tests.stderr or not tests.stderr.rstrip().endswith('OK'): raise ValueError('compact tests')
    names = ['hangul_mixed_replay_state.py', 'test_hangul_mixed_replay_state.py', 'report_hangul_mixed_replay.py']
    report = dict(id='exe45.hangul-keyboard.mixed-replay-host.v1', passed=True, tests=5,
                  implementation_class='host compact mixed state; not emitted native code',
                  state_bytes=SIZE, baseline_header_bytes=3, baseline_word_bytes=20,
                  key_bits=420, key_storage_bytes=53, max_keys=70, version_nibble=11,
                  external_baseline_required=False, moving_seals_without_partial_loss=True,
                  syllable_slot_paths=111720, occupied_word_domain=65536, randomized_actions=5000,
                  unittest_output=re.sub(r'Ran (\d+) tests in [0-9.]+s', r'Ran \1 tests', tests.stderr),
                  unittest_timing_excluded_from_identity=True,
                  layout_candidate=dict(editor_bytes=96, preserved_native_UI_bytes=16,
                                        old_destination_offset=28, new_destination_offset=16,
                                        state_offset=20, end_exclusive=96,
                                        reference_editor_base='0200FC40',
                                        native_initializer_observed=True,
                                        old_pointer_consumers_replaced=False,
                                        actual_game_memory_adopted=False,
                                        native_UI_hex=ui.hex(), destination=hex(destination),
                                        candidate_bytes_hex=candidate.hex()),
                  dependencies=deps, tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  rom_integrated=False, native_CPU_codec=False, persistent_save_format=False,
                  limits=['96-byte numerical fit is NOT proof of safe coordinated game replacement/lifetime.',
                          'Original16 UI bytes preserved, but all metadata readers/writers and destination users are not yet audited.',
                          'Old+16/+20/+24 pointers and+28 destination overlap proposed state; existing native handlers must not run unchanged.',
                          '588-byte feed/undo artifacts remain wider reference candidates; no588-byte game allocation or temporary stack claim.',
                          'Native compact replay must rebuild only current surface and validate every key; game display/save/import/IRQ remain pending.'],
                  next='Emit compact replay-to-current-surface without588-byte history scratch; audit/replace original pointer/padding/flatten/destination consumers together before any ROM hook.')
    (base / 'mixed_replay_host.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS self-contained mixed replay76 HOST; 5 tests; UI16+destination4+state76=96 placement candidate only')


if __name__ == '__main__': main()
