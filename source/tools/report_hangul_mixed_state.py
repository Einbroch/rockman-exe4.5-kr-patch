"""Derived fixed-width HOST candidate evidence; no native/RAM ownership claim."""
import json
import re
import subprocess
import sys
from build_visibility_poc import ROOT, sha, require_hash
from hangul_mixed_state import SIZE, HEADER


def main():
    base = ROOT / 'analysis/hangul_keyboard_v1'
    dependency = base / 'mixed_editor_host.json'
    mixed = json.loads(dependency.read_text(encoding='utf8'))
    if not mixed['passed'] or mixed['rom_integrated']:
        raise ValueError('mixed host evidence scope')
    for name, digest in mixed['tools'].items(): require_hash(ROOT / 'tools' / name, digest)
    tests = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'tools/test_hangul_mixed_state.py')],
                           check=True, timeout=60, capture_output=True, text=True, encoding='utf8')
    if 'Ran 4 tests' not in tests.stderr or not tests.stderr.rstrip().endswith('OK'):
        raise ValueError('mixed state tests')
    names = ['hangul_mixed_state.py', 'test_hangul_mixed_state.py', 'report_hangul_mixed_state.py']
    report = dict(id='exe45.hangul-keyboard.mixed-state-host.v1', passed=True,
                  implementation_class='fixed-width host codec candidate', tests=4,
                  unittest_output=re.sub(r'Ran (\d+) tests in [0-9.]+s', r'Ran \1 tests', tests.stderr),
                  unittest_timing_excluded_from_identity=True, state_bytes=SIZE, header_bytes=HEADER,
                  undo_entries=70, undo_entry_bytes=8, little_endian=True,
                  completed_syllable_roundtrips=11172, occupied_word_domain=65536,
                  every_short_extent_rejected=SIZE,
                  history_semantics_checked='Every reversed delta must have an accepted forward jamo transition.',
                  rejected_action_returns_identical_bytes=True,
                  dependencies={'analysis/hangul_keyboard_v1/mixed_editor_host.json': sha(dependency.read_bytes())},
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  rom_integrated=False, game_RAM_allocated=False, native_CPU_codec=False,
                  persistent_record_format=False,
                  limits=['588 bytes are an extent, NOT proof of free RAM or stack budget.',
                          'Cannot fit previous64-byte keylog overlay; no existing game region assigned.',
                          'Host transaction reconstructs reference snapshots; not emitted native code.',
                          'Mixed display, record/save compatibility, natural nonempty import, IRQ and fresh-load remain pending.'],
                  next='Implement/execute bounded native mixed edit/undo; determine state lifetime/allocation without overwriting owned game RAM.')
    (base / 'mixed_state_host.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS fixed mixed state HOST588 bytes; 4 tests; native allocation/integration pending')


if __name__ == '__main__': main()
