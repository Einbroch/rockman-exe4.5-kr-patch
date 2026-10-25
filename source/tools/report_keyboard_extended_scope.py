"""Source-derived calendar capacity/import and initial stack facts; no runtime adoption."""
import json
import struct
import subprocess
import sys
from build_visibility_poc import ROOT, sha, require_hash
from extended_dialogue import Cs, CS_ARCH_ARM, CS_MODE_THUMB


def main():
    profile = json.loads((ROOT / 'project.json').read_text(encoding='utf8'))['source_profile']
    source_path = ROOT / profile['filename']
    require_hash(source_path, profile['sha256'])
    source = source_path.read_bytes()
    product = ROOT / 'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity = '5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(product, identity)
    rom = product.read_bytes()
    regions = [(0xD0, 0xF4), (0x1B0, 0x1BC), (0x30EAA, 0x30F0C),
               (0x3100A, 0x31068), (0x3558C, 0x355AE)]
    guards = []
    for a, b in regions:
        if source[a:b] != rom[a:b]:
            raise ValueError('source caller/stack profile changed')
        guards.append(dict(start=hex(a), end=hex(b), sha256=sha(source[a:b])))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    checks = [(0x31012, 'movs', 'r0, #0xa'), (0x31014, 'movs', 'r1, #0x27'),
              (0x3101C, 'bl', '#0x80355b6'), (0x31028, 'bl', '#0x803558c'),
              (0x30EC8, 'bl', '#0x80355b6'), (0x30ED4, 'bl', '#0x803558c')]
    instructions = []
    for a, mnemonic, operands in checks:
        i = next(decoder.disasm(source[a:a + 4], a + 0x08000000), None)
        if i is None or (i.mnemonic, i.op_str) != (mnemonic, operands):
            raise ValueError('caller argument/boundary mismatch')
        instructions.append(dict(address=hex(i.address), bytes=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    temporary = struct.unpack_from('<I', source, 0x31060)[0]
    if temporary != 0x02026280 or struct.unpack_from('<I', source, 0x30F04)[0] != temporary:
        raise ValueError('shared imported staging record')
    tops = dict(zip(['irq', 'supervisor', 'system'], struct.unpack_from('<III', source, 0x1B0)))
    tests = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'tools/test_hangul_keylog_state.py')],
                           check=True, timeout=30, capture_output=True, text=True, encoding='utf8')
    if 'Ran 4 tests' not in tests.stderr or not tests.stderr.rstrip().endswith('OK'):
        raise ValueError('key-log host tests')
    data = dict(id='exe45.hangul-keyboard.extended-scope.v1', passed=True,
                source_sha256=profile['sha256'], current_rom_sha256=identity, rom_integrated=False,
                claim='bounded source calendar capacity/import callers, startup stack tops and host key-log capacity10 contract',
                calendar_input=dict(caller='0x0803100a', capacity=10, heading_script=39,
                                    source_heading='きねん日の ないよう', record_staging=hex(temporary),
                                    conditional_import_call='0x08031028', import_selection='caller state r5+0x0a, NOT record marker'),
                other_import=dict(caller='0x08030eaa', init='0x08030ec8', import_call='0x08030ed4',
                                  capacity='dynamic getter; not resolved here', record_staging=hex(temporary)),
                initial_stack_tops={k: hex(v) for k, v in tops.items()},
                native_guards=guards, selected_instructions=instructions,
                keylog_candidate=dict(bytes=64, supported_limits=[1, 10], max_keys=70,
                                      cached_ranks=False, packed_key_bytes=53, reserved_bytes=7,
                                      host_tests=4, unittest_output=tests.stderr, native_replay_implemented=False),
                tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                       ['hangul_keylog_state.py', 'test_hangul_keylog_state.py', 'report_keyboard_extended_scope.py']},
                limits=['Selected source callers only, not a complete input/call/field census or runtime import proof.',
                        'Separate initial stack tops do not establish lower stack boundaries, IRQ nested use or budget.',
                        'Original marker0-as-absent baseline proof applies to the weak-subject route, not caller-flag-driven staging imports.',
                        'Existing eight-cell native wrapper/display/record helpers remain bounded candidates, not universal game support.'],
                next='Implement native 64-byte key-log replay with temporary ten-cell state, capacity10 baseline/display/record conversion and legacy caller routing; prove runtime imports and stack before coordinated ROM installation.')
    (ROOT / 'analysis/hangul_keyboard_v1/extended_scope.json').write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS native calendar capacity10/source import callers; host key-log64/70; stack lower bounds and runtime import pending')


if __name__ == '__main__':
    main()
