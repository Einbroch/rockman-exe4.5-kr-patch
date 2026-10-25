"""Execute standalone B kernel on canonical fixtures; not game/runtime proof."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_mixed_undo_thumb import CODE
from hangul_mixed_editor import MixedEditor
from hangul_mixed_state import pack, SIZE, HEADER
from hangul_native_tokens import tag


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'
    report_path = root / 'cpu_composer/report.json'
    old = json.loads(report_path.read_text(encoding='utf8'))
    for n, h in old['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    for n, h in old['artifacts'].items(): require_hash(report_path.parent / n, h)
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble_verified(CODE, 0x08000000, {})
    if any(len(bytes.fromhex(x['hex'])) != 2 for x in isa['instructions']):
        raise ValueError('Thumb1 instructions only')
    out = root / 'cpu_mixed_undo'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob)
    blob = (out / 'helper.bin').read_bytes()
    deletes = (root / 'cpu_composer/deletions.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 4096); u.mem_write(0x08000000, blob)
    u.mem_protect(0x08000000, 4096, UC_PROT_READ | UC_PROT_EXEC)
    u.mem_map(0x09200000, (len(deletes) + 4095) & ~4095); u.mem_write(0x09200000, deletes)
    u.mem_protect(0x09200000, (len(deletes) + 4095) & ~4095, UC_PROT_READ)
    u.mem_map(0x02000000, 4096); u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    state, sp, stop = 0x02000100, 0x03007F00, 0x0FF00000
    preserved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                 UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(calls=0, accepted=0, rejected=0, full_word_domain=0,
                  syllable_history_undo=0, native_cursor_paths=0, malformed=0)

    def run(before, wanted, accepted, available=SIZE, address=state):
        u.mem_write(0x02000000, b'\xA7' * 4096); u.mem_write(state, before)
        original = bytes(u.mem_read(0x02000000, 4096))
        u.mem_write(sp - 56, b'\x5A' * 56)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for reg, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],
                            [address, available, 0x09200000, 0]): u.reg_write(reg, val)
        for i, reg in enumerate(preserved): u.reg_write(reg, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(0x08000001, stop, count=15000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_R0) != int(accepted):
            raise ValueError(f'CPU return before={before[:28].hex()} expected={accepted}')
        if u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(preserved)):
            raise ValueError('ABI')
        if bytes(u.mem_read(sp - 56, 4)) != b'\x5A' * 4: raise ValueError('stack52 guard')
        expected = bytearray(original)
        if accepted: expected[state - 0x02000000:state - 0x02000000 + SIZE] = wanted
        after = bytes(u.mem_read(0x02000000, 4096))
        if after != bytes(expected):
            first = next(i for i, (a, b) in enumerate(zip(after, expected)) if a != b)
            raise ValueError(f'CPU write mismatch offset={first - 256} got={after[first]} expected={expected[first]} before={before[:28].hex()}')
        counts['calls'] += 1; counts['accepted' if accepted else 'rejected'] += 1

    def back(m):
        before = pack(m); accepted = m.backspace()
        run(before, pack(m), accepted)

    # Independent boundary expectations for all uint16 occupied words. Known
    # canonical deletion bytes are the already executed/pinned native table.
    m = MixedEditor(2); m.load([0, tag(b'\x9B')]); m.move(1)
    base = pack(m)
    print('mixed B uint16 domain', flush=True)
    for word in range(65536):
        before = bytearray(base); struct.pack_into('<H', before, 8, word)
        valid = word < 11191 or 0x8000 <= word <= 0x80E3 or 0x8100 <= word <= 0x81FF
        wanted = bytearray(before)
        if valid:
            prior = struct.unpack_from('<H', deletes, 2 * word)[0] if word < 11191 else 0xFFFF
            if prior == 0xFFFF:
                wanted[2:5] = bytes([1, 0, 255]); wanted[8:12] = struct.pack('<HH', tag(b'\x9B'), 0xFFFF)
            else:
                wanted[3:5] = bytes([1, 0]); struct.pack_into('<H', wanted, 8, prior)
        run(bytes(before), bytes(wanted), valid)
        counts['full_word_domain'] += 1
    print('mixed B complete syllable history undo', flush=True)
    for l in INITIALS:
        for v in MEDIALS:
            for t in FINALS:
                m = MixedEditor(2); m.load([tag(b'\xE4\x00'), tag(b'\x9B')])
                for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))): m.press(k)
                while m.history:
                    back(m); counts['syllable_history_undo'] += 1
    # Every structural native tag/caret, independently comparing whole-cell B
    # through the host model; glyph eligibility and save compatibility not claimed.
    for token in [bytes([i]) for i in range(228)] + [bytes([0xE4, i]) for i in range(256)]:
        for cursor in range(11):
            m = MixedEditor(10); m.load([tag(token)] * 10)
            for _ in range(cursor): m.move(1)
            back(m); counts['native_cursor_paths'] += 1
    for slot in range(10):
        m = MixedEditor(10); m.load([tag(bytes([0x9B + i])) for i in range(10)])
        for _ in range(slot): m.move(1)
        for k in 'ㄱㅏㄴㅏ': m.press(k)
        while m.history: back(m)
    m = MixedEditor(10)
    for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10: m.press(k)
    while m.history: back(m)
    back(m)
    m = MixedEditor(2); m.press('ㄱ'); m.move(-1); back(m)
    for size in range(SIZE):
        run(base, base, False, available=size); counts['malformed'] += 1
    for address in (state + 1, state + 2, state + 3, 0xFFFFFFFC):
        run(base, base, False, address=address); counts['malformed'] += 1
    for offset, value in ((0, 0), (1, 0), (1, 11), (2, 11), (3, 3), (4, 2),
                          (4, 1), (5, 71), (6, 1), (7, 1), (12, 0), (HEADER, 1), (SIZE - 1, 1)):
        bad = bytearray(base); bad[offset] = value
        run(bytes(bad), bytes(bad), False); counts['malformed'] += 1
    m = MixedEditor(2); m.load([tag(b'\x9B')]); m.press('ㄱ')
    hist = pack(m)
    for offset, value in ((4, 255), (HEADER + 3, 1), (HEADER, 3), (HEADER + 1, 2),
                          (HEADER + 2, 1), (HEADER + 4, 255), (HEADER + 6, 0)):
        bad = bytearray(hist); bad[offset] = value
        run(bytes(bad), bytes(bad), False); counts['malformed'] += 1
    # Explicit negative scope: structurally valid but impossible history is
    # NOT rejected by this trusted-input kernel. Retain this counterexample.
    forged = bytearray(hist); forged[8:10] = b'\x00\x00'
    wanted = MixedEditor(2); wanted.load([tag(b'\x9B')])
    run(bytes(forged), pack(wanted), True)
    names = ['hangul_mixed_undo_thumb.py', 'bench_hangul_mixed_undo.py',
             'hangul_mixed_editor.py', 'hangul_mixed_state.py']
    report = dict(id='exe45.hangul-keyboard.mixed-undo-cpu.v1', passed=True,
                  counts=counts, helper_bytes=len(blob), state_bytes=SIZE, stack_bytes=52,
                  code_address='08000000', ISA=isa, rom_integrated=False,
                  all_11172_syllables_history_undo=True, native_token_cursor_paths=484 * 11,
                  trusted_canonical_input_required=True, complete_history_validation=False,
                  forged_forward_transition_counterexample_accepted=True,
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  dependency_reports={'cpu_composer': sha(report_path.read_bytes())},
                  artifacts={'helper.bin': sha(blob)},
                  limits=['Standalone emitted B/undo executed on synthetic caller RAM, not actual game.',
                          'Not a decoder: caller must validate complete canonical history before invoking.',
                          'Structural top-delta checks do not reject every forged history; counterexample preserved.',
                          'Trusted table/pointer extents and stack disjointness are caller preconditions.',
                          'No feed/movement/native write kernel, game RAM allocation, hook, display or save integration.'],
                  next='Emit native mixed feed and canonical-state validation; establish memory ownership/lifetime before installing any game hook.')
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS mixed B/undo trusted CPU candidate', counts, '; NOT universal decoder/ROM integrated')


if __name__ == '__main__': main()
