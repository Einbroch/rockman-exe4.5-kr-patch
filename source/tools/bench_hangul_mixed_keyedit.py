"""CPU fixtures for atomic compact key append/pop, not full editor support."""
import json
import random
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_mixed_keyedit_thumb import assemble
from hangul_mixed_replay_state import MixedReplay, KEYS, apply
from hangul_native_tokens import tag
from hangul_mixed_display import display


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'
    rp = root / 'cpu_mixed_replay/report.json'
    replay = json.loads(rp.read_text(encoding='utf8'))
    if not replay['passed'] or replay['rom_integrated']: raise ValueError('replay scope')
    for n, h in replay['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    for n, h in replay['artifacts'].items(): require_hash(rp.parent / n, h)
    for p, h in replay['host_dependency'].items(): require_hash(ROOT / p, h)
    dp = root / 'cpu_mixed_display/report.json'
    displayed = json.loads(dp.read_text(encoding='utf8'))
    if not displayed['passed'] or displayed['rom_integrated']: raise ValueError('display scope')
    for n, h in displayed['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    for n, h in displayed['artifacts'].items(): require_hash(dp.parent / n, h)
    if displayed['dependencies']['cpu_mixed_replay'] != sha(rp.read_bytes()): raise ValueError('display replay binding')
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble()
    out = root / 'cpu_mixed_keyedit'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob); blob = (out / 'helper.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 12288); u.mem_write(0x08001000, blob)
    u.mem_write(0x08000000, (rp.parent / 'helper.bin').read_bytes())
    u.mem_write(0x08002000, (dp.parent / 'helper.bin').read_bytes())
    u.mem_protect(0x08000000, 12288, UC_PROT_READ | UC_PROT_EXEC)
    pairs = (root / 'cpu_composer/transitions.bin').read_bytes()
    u.mem_map(0x09000000, (len(pairs) + 4095) & ~4095); u.mem_write(0x09000000, pairs)
    u.mem_protect(0x09000000, (len(pairs) + 4095) & ~4095, UC_PROT_READ)
    u.mem_map(0x02000000, 8192); u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    src, sp, stop = 0x02000101, 0x03007F00, 0x0FF00000
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(calls=0, rejected=0, syllable_final_key_paths=0, packed_position_key_paths=0,
                  history_pop_paths=0, uninterrupted_actions=0, malformed=0, native_edit_replay_display_paths=0)

    def pipeline(raw):
        # No host writes to compact/current surface between the three helpers.
        current, dest = 0x02001100, 0x02001503
        c = MixedReplay.restore(raw)
        s = c.model.state
        expected_surface = bytes([len(s.cells), c.model.capacity, s.cursor, 255 if s.active is None else s.active]) + struct.pack('<10H', *(s.cells + (65535,) * (10 - len(s.cells))))
        wanted = display(expected_surface, 1)
        for pc, args, expected_result, output, payload, stack in (
            (0x08000000, [src, current, 76 | 24 << 16, 0x09000000], 1, current, expected_surface, 68),
            (0x08002000, [current, dest, 41, 1], len(wanted), dest, wanted, 36)):
            before = bytearray(u.mem_read(0x02000000, 8192))
            u.mem_write(sp - stack - 4, b'\x5A' * (stack + 4))
            u.reg_write(UC_ARM_REG_CPSR, 0x30)
            for r, v in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args): u.reg_write(r, v)
            for i, r in enumerate(regs): u.reg_write(r, 0x13579000 + i)
            u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
            u.emu_start(pc | 1, stop, count=30000)
            if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_R0) != expected_result or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(regs)): raise ValueError('pipeline ABI')
            if bytes(u.mem_read(sp - stack - 4, 4)) != b'\x5A' * 4: raise ValueError('pipeline stack')
            before[output - 0x02000000:output - 0x02000000 + len(payload)] = payload
            if bytes(u.mem_read(0x02000000, 8192)) != bytes(before): raise ValueError('actual CPU edit/replay/display output')
        counts['native_edit_replay_display_paths'] += 1

    def oracle(raw, action):
        try:
            c = MixedReplay.restore(raw)
            if action == 40:
                # Explicitly no canonical-B implementation in this helper.
                return apply(raw, 'backspace') if c.keys else (False, raw)
            if not 0 <= action < 40: return False, raw
            return apply(raw, 'jamo', KEYS[action])
        except ValueError:
            return False, raw

    def execute(raw, action, capacity=76, source=src, initialized=False, pointer=None):
        accepted, wanted = oracle(raw, action)
        if capacity < 76 or pointer is not None: accepted, wanted = False, raw
        if not initialized:
            u.mem_write(0x02000000, b'\xA7' * 8192); u.mem_write(source, raw)
        elif bytes(u.mem_read(source, 76)) != raw:
            raise ValueError('uninterrupted input drift')
        before = bytes(u.mem_read(0x02000000, 8192))
        u.mem_write(sp - 200, b'\x5A' * 200)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for r, v in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],
                        [source if pointer is None else pointer, action, capacity, 0x09000000]): u.reg_write(r, v)
        for i, r in enumerate(regs): u.reg_write(r, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(0x08001001, stop, count=30000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_R0) != int(accepted) or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(regs)): raise ValueError('ABI/return')
        if bytes(u.mem_read(sp - 200, 4)) != b'\x5A' * 4: raise ValueError('stack196')
        expected = bytearray(before)
        expected[source - 0x02000000:source - 0x02000000 + 76] = wanted
        if bytes(u.mem_read(0x02000000, 8192)) != bytes(expected): raise ValueError(f'atomic state/bounds action={action} raw={raw.hex()}')
        counts['calls'] += 1; counts['rejected'] += not accepted
        return wanted

    legacy = [tag(b'\xE4\xE5')] * 10
    print('compact keyedit all syllable final keys at last slot', flush=True)
    for l in INITIALS:
        for v in MEDIALS:
            for t in FINALS:
                c = MixedReplay(10); c.load(legacy)
                for _ in range(9): c.move(1)
                path = [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,))))
                for k in path[:-1]: c.press(k)
                raw = c.serialize(); result = execute(raw, KEYS.index(path[-1]))
                if MixedReplay.restore(result).candidate()[9] != INITIALS.index(l)*588 + MEDIALS.index(v)*28 + FINALS.index(t): raise ValueError('final syllable')
                pipeline(result)
                execute(result, 40); counts['syllable_final_key_paths'] += 1; counts['history_pop_paths'] += 1
        print('initial', l, flush=True)
    c = MixedReplay(10); maximum_path = 'ㄱㄱㅗㅏㅣㄹㄱ' * 10
    print('all70 packed positions and40keys; exact pop restoration', flush=True)
    for k in maximum_path:
        raw = c.serialize()
        for action in range(40): execute(raw, action); counts['packed_position_key_paths'] += 1
        c.press(k)
        result = execute(raw, KEYS.index(k)); restored = execute(result, 40)
        if restored != raw: raise ValueError('exact overwritten baseline restoration')
        counts['history_pop_paths'] += 1
    raw = c.serialize()
    for action in range(40): execute(raw, action)
    # CPU outputs feed following edits without host rewriting the state.
    raw = MixedReplay(10).serialize(); rng = random.Random(7645)
    for step in range(1000):
        raw = execute(raw, rng.randrange(41), initialized=step > 0)
        counts['uninterrupted_actions'] += 1
    base = MixedReplay(1).serialize()
    execute(base, 40)
    for cap in range(1, 11):
        c = MixedReplay(cap); c.load(legacy[:cap]); execute(c.serialize(), 40)
        for k in 'ㄱㅏㄴ': c.press(k)
        execute(c.serialize(), KEYS.index('ㅏ'))
    for source in [src + i for i in range(4)]: execute(base, 0, source=source)
    for capacity in (0, 1, 75): execute(base, 0, capacity=capacity)
    for action in (41, 255, 0xFFFFFFFF): execute(base, action)
    execute(base, 0, pointer=0xFFFFFFF0)
    for offset, value in ((0, 0), (0, 11), (1, 0x10), (2, 71), (3, 0), (23, 1), (75, 0xA0), (75, 0xB1)):
        bad = bytearray(base); bad[offset] = value
        for action in (0, 40): execute(bytes(bad), action); counts['malformed'] += 1
    c = MixedReplay(1); c.press('ㄱ'); valid = c.serialize()
    for key in range(40, 64):
        bad = bytearray(valid); bad[23] = key
        for action in (0, 40): execute(bytes(bad), action); counts['malformed'] += 1
    # A pop must not sanitize an invalid last key into a valid state.
    bad = bytearray(valid); bad[23] = KEYS.index('ㅏ')
    execute(bytes(bad), 40); counts['malformed'] += 1
    names = ['hangul_mixed_keyedit_thumb.py', 'bench_hangul_mixed_keyedit.py', 'hangul_mixed_replay_thumb.py',
             'hangul_mixed_replay_state.py', 'hangul_mixed_editor.py', 'hangul_native_tokens.py', 'hangul_mixed_display.py', 'extended_dialogue.py']
    report = dict(id='exe45.hangul-keyboard.mixed-keyedit-cpu.v1', passed=True, counts=counts,
                  helper_bytes=len(blob), state_bytes=76, own_stack_bytes=128, nested_stack_bytes=196,
                  temporary_history_bytes=0, ISA=isa, rom_integrated=False,
                  original_and_proposal_replay_validated=True, history_pop_only=True,
                  dependencies={'cpu_mixed_replay': sha(rp.read_bytes()), 'cpu_mixed_display': sha(dp.read_bytes())},
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names}, artifacts={'helper.bin': sha(blob)},
                  limits=['No-history canonical B, cursor movement, native writes and rebase are not implemented here.',
                          'CPU fixture stack196 is not proof of game/IRQ budget or RAM ownership.',
                          'No game hook, keyboard screen, commit, save or fresh-load claim.'])
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS compact keyedit CPU', counts, 'stack196; no-history B deferred', flush=True)


if __name__ == '__main__': main()
