"""Execute cursor-aware mixed feed with native undo; synthetic RAM only."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_mixed_feed_thumb import CODE
from hangul_mixed_editor import MixedEditor, Snapshot
from hangul_mixed_state import pack, unpack, SIZE, HEADER
from hangul_native_tokens import tag


def encode(m):
    # Controlled fixture serializer, not a substitute validator for CPU results.
    # Histories below are produced by real accepted host transitions or depth0.
    s = m.state
    out = bytearray(SIZE)
    out[:8] = bytes([177, m.capacity, len(s.cells), s.cursor,
                     255 if s.active is None else s.active, len(m.history), 0, 0])
    struct.pack_into('<10H', out, 8, *(s.cells + (65535,) * (10 - len(s.cells))))
    for i, prior in enumerate(m.history):
        p = prior.cursor if prior.active is None else prior.active
        words = [prior.cells[j] if j < len(prior.cells) else 65535 for j in (p, p + 1)]
        struct.pack_into('<BBBBHH', out, HEADER + i * 8, len(prior.cells), prior.cursor,
                         255 if prior.active is None else prior.active, 0, *words)
    return bytes(out)


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'
    deps = {}
    for name in ('cpu_composer', 'cpu_mixed_undo'):
        p = root / name / 'report.json'; r = json.loads(p.read_text(encoding='utf8'))
        if not r['passed'] or r['rom_integrated']: raise ValueError('dependency scope')
        for n, h in r['tools'].items(): require_hash(ROOT / 'tools' / n, h)
        for n, h in r['artifacts'].items(): require_hash(p.parent / n, h)
        deps[name] = sha(p.read_bytes())
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble_verified(CODE, 0x08000000, {})
    out = root / 'cpu_mixed_feed'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob); blob = (out / 'helper.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 8192); u.mem_write(0x08000000, blob)
    u.mem_write(0x08001000, (root / 'cpu_mixed_undo/helper.bin').read_bytes())
    u.mem_protect(0x08000000, 8192, UC_PROT_READ | UC_PROT_EXEC)
    for a, n in ((0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')):
        data = (root / 'cpu_composer' / n).read_bytes(); size = (len(data) + 4095) & ~4095
        u.mem_map(a, size); u.mem_write(a, data); u.mem_protect(a, size, UC_PROT_READ)
    u.mem_map(0x02000000, 4096); u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    state, sp, stop = 0x02000100, 0x03007F00, 0x0FF00000
    preserved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                 UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(feed=0, undo=0, rejected=0, row_key_vectors=0,
                  syllable_slot_paths=0, full_word_domain=0, malformed=0,
                  uninterrupted_native_sequences=0)

    def call(key, available=SIZE, address=state):
        u.mem_write(sp - 56, b'\x5A' * 56)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        args = ([address, available, 0x09200000, 0] if key is None else
                [address, key, 0x09000000, available])
        for reg, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args): u.reg_write(reg, val)
        for i, reg in enumerate(preserved): u.reg_write(reg, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start((0x08001000 if key is None else 0x08000000) | 1, stop, count=15000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(preserved)):
            raise ValueError('ABI/return')
        if bytes(u.mem_read(sp - 56, 4)) != b'\x5A' * 4: raise ValueError('stack52 guard')
        ret = u.reg_read(UC_ARM_REG_R0)
        if ret not in (0, 1): raise ValueError('status domain')
        counts['feed' if key is not None else 'undo'] += 1
        counts['rejected'] += ret == 0
        return bool(ret)

    def run(before, wanted, accepted, key=0, available=SIZE, address=state):
        u.mem_write(0x02000000, b'\xA7' * 4096); u.mem_write(state, before)
        original = bytes(u.mem_read(0x02000000, 4096))
        if call(key, available, address) != accepted:
            raise ValueError(f'return key={key} accepted={accepted} before={before[:28].hex()}')
        expected = bytearray(original)
        if accepted: expected[state - 0x02000000:state - 0x02000000 + SIZE] = wanted
        after = bytes(u.mem_read(0x02000000, 4096))
        if after != bytes(expected):
            i = next(i for i, (a, b) in enumerate(zip(after, expected)) if a != b)
            raise ValueError(f'write key={key} offset={i-256} got={after[i]} want={expected[i]} before={before[:28].hex()}')

    def press(m, key):
        before = encode(m); accepted = m.press(key)
        run(before, encode(m), accepted, KEYS.index(key)); return accepted

    def back(m):
        before = encode(m); accepted = m.backspace()
        run(before, encode(m), accepted, key=None)

    print('mixed feed all11192 rows x40 keys', flush=True)
    for rank in range(11192):
        for key in KEYS:
            m = MixedEditor(3)
            m.state = Snapshot((rank, tag(b'\x9B'), tag(b'\xE4\x00')), 1, 0) if rank < 11191 else Snapshot((), 0, None)
            press(m, key); counts['row_key_vectors'] += 1
        if rank % 2800 == 0: print('row', rank, '/11192', flush=True)
    legacy = tuple(tag(bytes([0x9B + i])) for i in range(10))
    # Every syllable in every slot, intermediate CPU states and reverse undo.
    for slot in range(10):
        for li, l in enumerate(INITIALS):
            for vi, v in enumerate(MEDIALS):
                for ti, t in enumerate(FINALS):
                    m = MixedEditor(10); m.state = Snapshot(legacy, slot, None)
                    for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                        if not press(m, k): raise ValueError('syllable path rejected')
                    expected = list(legacy); expected[slot] = li * 588 + vi * 28 + ti
                    if m.state.cells != tuple(expected): raise ValueError('syllable target')
                    while m.history: back(m)
                    if m.state != Snapshot(legacy, slot, None): raise ValueError('legacy undo restoration')
                    counts['syllable_slot_paths'] += 1
        print('mixed slot', slot + 1, '/10', flush=True)
    print('mixed inactive occupied uint16 domain', flush=True)
    m = MixedEditor(1); m.load([0]); base = encode(m)
    for word in range(65536):
        before = bytearray(base); struct.pack_into('<H', before, 8, word)
        valid = word < 11191 or 0x8000 <= word <= 0x80E3 or 0x8100 <= word <= 0x81FF
        wanted = bytearray(before)
        if valid:
            wanted[3:6] = bytes([1, 0, 1]); struct.pack_into('<H', wanted, 8, 11172)
            struct.pack_into('<BBBBHH', wanted, HEADER, 1, 0, 255, 0, word, 65535)
        run(bytes(before), bytes(wanted), valid)
        counts['full_word_domain'] += 1

    # Uninterrupted emitted feed -> emitted undo; no host rewrites between calls.
    # Independently decode actual serialized CPU state at each boundary.
    for cap in range(1, 11):
        for slot in range(cap):
            for sequence in ('ㄱㅏㄴㅏ', 'ㄱㄱㅗㅏㅣㄹㄱ', 'ㅏㄱㅏㅏㄴ', 'ㄴㅏㄹㄱㅏ'):
                m = MixedEditor(cap); m.load(list(legacy[:cap]))
                for _ in range(slot): m.move(1)
                u.mem_write(0x02000000, b'\xA7' * 4096); u.mem_write(state, pack(m))
                for k in sequence:
                    accepted = m.press(k)
                    if call(KEYS.index(k)) != accepted or bytes(u.mem_read(state, SIZE)) != pack(m): raise ValueError('uninterrupted feed')
                    actual = unpack(bytes(u.mem_read(state, SIZE)))
                    if (actual.state, actual.history) != (m.state, m.history): raise ValueError('actual CPU serialization')
                while m.history:
                    accepted = m.backspace()
                    if call(None) != accepted or bytes(u.mem_read(state, SIZE)) != pack(m): raise ValueError('uninterrupted undo')
                if bytes(u.mem_read(state - 4, 4)) != b'\xA7' * 4 or bytes(u.mem_read(state + SIZE, 4)) != b'\xA7' * 4: raise ValueError('sequence bounds')
                counts['uninterrupted_native_sequences'] += 1
    m = MixedEditor(10)
    for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10: press(m, k)
    press(m, 'ㄱ')
    while m.history: back(m)
    m = MixedEditor(2); m.press('ㄱ'); m.move(-1)
    press(m, 'ㅏ'); press(m, 'ㄴ')
    for available in range(SIZE):
        run(base, base, False, available=available); counts['malformed'] += 1
    for key in (40, 41, 255, 65535, 0xFFFFFFFF):
        run(base, base, False, key=key); counts['malformed'] += 1
    for address in (state + 1, state + 2, state + 3, 0xFFFFFFFC):
        run(base, base, False, address=address); counts['malformed'] += 1
    for offset, value in ((0, 0), (1, 0), (1, 11), (2, 2), (3, 2), (4, 1), (5, 71),
                          (5, 1), (6, 1), (7, 1), (10, 0), (HEADER, 1), (SIZE - 1, 1)):
        bad = bytearray(base); bad[offset] = value
        run(bytes(bad), bytes(bad), False); counts['malformed'] += 1
    # Keep the non-decoder boundary visible: feed assumes historical validity.
    m = MixedEditor(2); m.load([tag(b'\x9B')]); m.press('ㄱ')
    forged = bytearray(pack(m)); forged[8:10] = b'\x00\x00'
    # A final after forged complete 가 is a legal new step, but earlier history
    # remains impossible. The kernel accepts it under its violated precondition.
    u.mem_write(state, bytes(forged))
    if not call(KEYS.index('ㄴ')): raise ValueError('non-decoder counterexample changed')
    with_invalid_history = bytes(u.mem_read(state, SIZE))
    try: unpack(with_invalid_history)
    except ValueError: pass
    else: raise ValueError('forged history should fail full host decoding')
    names = ['hangul_mixed_feed_thumb.py', 'bench_hangul_mixed_feed.py',
             'hangul_mixed_undo_thumb.py', 'hangul_mixed_editor.py', 'hangul_mixed_state.py',
             'hangul_keyboard_model.py', 'hangul_composer_thumb.py', 'hangul_native_tokens.py',
             'hangul_extended_composer_thumb.py']
    report = dict(id='exe45.hangul-keyboard.mixed-feed-cpu.v1', passed=True, counts=counts,
                  helper_bytes=len(blob), state_bytes=SIZE, stack_bytes=52, ISA=isa,
                  rom_integrated=False, game_RAM_allocated=False, trusted_canonical_input_required=True,
                  complete_history_validation=False, forged_history_counterexample_accepted=True,
                  all_11172_syllables_in_each10_slots=True, carry_overwrites_next_cell=True,
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  dependency_reports=deps, artifacts={'helper.bin': sha(blob)},
                  limits=['Emitted feed and undo run only in isolated CPU fixtures; no game hook/runtime evidence.',
                          'Caller must establish canonical history and pinned tables, extents and stack disjointness.',
                          'No full native decoder; structurally plausible forged history can remain accepted.',
                          'Movement/native writes/import initialization, mixed display/save and game RAM lifetime remain pending.'],
                  next='Implement native mixed cursor/native-write/import and full canonical history validation; establish state RAM lifetime and integrate display/save.')
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS mixed feed/undo CPU only', counts, '; no full decoder/game integration')


if __name__ == '__main__': main()
