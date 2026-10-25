"""Bind cursor-aware host candidate to original bounded edit evidence."""
import json
import re
import subprocess
import sys
from build_visibility_poc import ROOT, sha, require_hash


def main():
    base = ROOT / 'analysis/hangul_keyboard_v1'
    legacy = json.loads((base / 'legacy_edit.json').read_text(encoding='utf8'))
    if not legacy['passed'] or legacy['rom_integrated'] or legacy['findings']['imported_cursor'] != 'start, unchanged':
        raise ValueError('legacy evidence scope')
    for n, h in legacy['tools'].items():
        require_hash(ROOT / 'tools' / n, h)
    tests = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'tools/test_hangul_mixed_editor.py')],
                           check=True, timeout=60, capture_output=True, text=True, encoding='utf8')
    if 'Ran 6 tests' not in tests.stderr or not tests.stderr.rstrip().endswith('OK'):
        raise ValueError('mixed editor tests')
    names = ['hangul_mixed_editor.py', 'test_hangul_mixed_editor.py', 'report_hangul_mixed_editor.py',
             'hangul_keyboard_model.py', 'hangul_composer_thumb.py', 'hangul_native_tokens.py']
    report = dict(id='exe45.hangul-keyboard.mixed-editor-host.v1', passed=True, rom_integrated=False,
                  implementation_class='host reference candidate; not machine code, game RAM or save ABI',
                  capacity=10, tests=6, unittest_output=re.sub(r'Ran (\d+) tests in [0-9.]+s', r'Ran \1 tests', tests.stderr),
                  unittest_timing_excluded_from_identity=True,
                  syllable_slot_paths=11172 * 10, structural_native_token_capacity_paths=484 * 10,
                  max_host_history_snapshots=70, imported_cursor=0,
                  original_native_token_delete_overwrite_preserved=True,
                  Hangul_carry_overwrites_next_cell=True, partial_anywhere_blocks_confirmation=True,
                  dependencies={'analysis/hangul_keyboard_v1/legacy_edit.json': sha((base / 'legacy_edit.json').read_bytes())},
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  proposed_UX=['New Hangul initial replaces the caret cell; continuing jamo targets active cell before caret.',
                               'Carry writes next cell instead of inserting/shifting; unrelated cells remain unchanged.',
                               'Successful cursor movement seals active composition/history but keeps every visible cell including partials.',
                               'B first undoes accepted jamo, then canonical Hangul components; native-token B matches original whole-cell delete.',
                               'Undo of first overwrite restores the overwritten cell; new Hangul UX is a candidate pending presentation review.'],
                  limits=['No emitted mixed CPU editor, serialized persistent state, mixed display/record codec, ROM hook or runtime evidence.',
                          'Host snapshot history is bounded by70 entries but its memory size is NOT a proven64-byte game state implementation.',
                          '484 structural native tokens are not proof of font membership, input eligibility or safe old byte-scanning commit.',
                          'Cursor/composition feedback, save compatibility and fresh-load remain unresolved.'],
                  next='Define bounded mixed-state/undo ABI and emit cursor-aware editor; verify mixed display, legacy imports, game stack and coordinated hooks.')
    (base / 'mixed_editor_host.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS mixed cursor editor HOST only; 6 tests,111720 syllable-slot and4840 native-capacity paths')


if __name__ == '__main__':
    main()
