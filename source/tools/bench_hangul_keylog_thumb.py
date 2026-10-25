"""Isolated keylog64 -> ten-cell native replay tests, not game runtime."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_keylog_state import KeylogComposer
from hangul_keylog_thumb import assemble
from hangul_extended_composer_thumb import encode_state


def main():
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    deps = [ROOT / 'analysis/hangul_keyboard_v1' / n for n in ('cpu_composer', 'cpu_extended_composer')]
    for dep in deps:
        r = json.loads((dep / 'report.json').read_text(encoding='utf8'))
        if not r['passed']:
            raise ValueError('unverified backend')
        for n, h in r['tools'].items():
            require_hash(ROOT / 'tools' / n, h)
        for n, h in r['artifacts'].items():
            require_hash(dep / n, h)
    blob, isa = assemble()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 16384)
    for a, n in [(0x08000000, 'feed.bin'), (0x08001000, 'undo.bin')]:
        u.mem_write(a, (deps[1] / n).read_bytes())
    u.mem_write(0x08002000, blob)
    u.mem_write(0x08003000, struct.pack('<4I', 0x08000001, 0x08001001, 0x09000000, 0x09200000))
    u.mem_protect(0x08000000, 16384, UC_PROT_READ | UC_PROT_EXEC)
    for a, n in [(0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')]:
        d = (deps[0] / n).read_bytes(); size = (len(d) + 4095) & ~4095
        u.mem_map(a, size); u.mem_write(a, d); u.mem_protect(a, size, UC_PROT_READ)
    state, baseline, sp, stop = 0x02000100, 0x02002000, 0x03007F00, 0x0FF00000
    u.mem_map(0x02000000, 4096); u.mem_map(baseline, 4096, UC_PROT_READ)
    u.mem_map(0x03007000, 4096); u.mem_map(stop, 4096)
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(calls=0, rejected=0, malformed=0)

    def base(c):
        m = Composer(c.limit); m.load(c.baseline)
        return encode_state(m)[:24]

    def execute(raw, b, action, wanted, accepted, ptr=state, bp=baseline, reconstructed=None):
        u.mem_write(state - 4, b'\xA7' * 4 + raw + b'\xA7' * 4)
        u.mem_write(baseline, b); u.mem_write(sp - 476, b'\x5A' * 4)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for reg, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],
                            [ptr, bp, action, 0x08003000]):
            u.reg_write(reg, val)
        for i, reg in enumerate(regs):
            u.reg_write(reg, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(0x08002001, stop, count=100000)
        if (u.reg_read(UC_ARM_REG_PC), u.reg_read(UC_ARM_REG_SP), u.reg_read(UC_ARM_REG_R0)) != (stop, sp, int(accepted)):
            raise ValueError(f'return ABI action={action} raw={raw.hex()}')
        if any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(regs)):
            raise ValueError('preserved register')
        if bytes(u.mem_read(state - 4, 72)) != b'\xA7' * 4 + wanted + b'\xA7' * 4:
            raise ValueError(f'keylog mutation action={action} raw={raw.hex()} actual={bytes(u.mem_read(state,64)).hex()} wanted={wanted.hex()}')
        if bytes(u.mem_read(baseline, 24)) != b or bytes(u.mem_read(sp - 476, 4)) != b'\x5A' * 4:
            raise ValueError('baseline/stack boundary')
        # Read dead fixture stack only for testing. Never return this address
        # to a game caller: it is invalid after wrapper return.
        if reconstructed is not None and bytes(u.mem_read(sp - 412, 304)) != reconstructed:
            raise ValueError('reconstructed ranks/history differ from host model')
        counts['calls'] += 1; counts['rejected'] += not accepted

    def step(c, action):
        raw = c.serialize()
        ok = c.press(KEYS[action]) if action < 40 else c.backspace() if action == 40 else action == 41
        execute(raw, base(c), action, c.serialize(), ok,
                reconstructed=encode_state(c.model) if ok else None)
        return ok

    print('keylog native full syllable creation/replay/undo', flush=True)
    for li, l in enumerate(INITIALS):
        for vi, v in enumerate(MEDIALS):
            for ti, t in enumerate(FINALS):
                c = KeylogComposer(1)
                for key in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                    if not step(c, KEYS.index(key)):
                        raise ValueError('creation rejected')
                syllable = chr(0xAC00 + li * 588 + vi * 28 + ti)
                if c.candidate() != syllable:
                    raise ValueError('syllable identity')
                step(c, 41)
                while step(c, 40):
                    pass
                c = KeylogComposer(10, '가' * 9 + syllable)
                step(c, 41)
                while len(c.display) == 10:
                    step(c, 40)
        print('initial', li + 1, '/19', flush=True)
    for cap in range(1, 11):
        for key in range(40):
            step(KeylogComposer(cap, '가' * cap), key)
    c = KeylogComposer(10, chr(0xAC00 + 588 + 10 * 28 + 9) * 10)
    while step(c, 40):
        pass
    if c.deletions != 70:
        raise ValueError('baseline deletion70')
    for key in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10:
        if not step(c, KEYS.index(key)):
            raise ValueError('70 keys rejected')
    step(c, 0); step(c, 41)
    maximum = c.serialize()
    for slot in range(70):
        bits = int.from_bytes(maximum[4:57], 'little')
        bits = (bits & ~(63 << (slot * 6))) | (63 << (slot * 6))
        bad = maximum[:4] + bits.to_bytes(53, 'little') + maximum[57:]
        execute(bad, base(c), 41, bad, False); counts['malformed'] += 1
    while step(c, 40):
        pass
    c = KeylogComposer(10); raw = c.serialize(); b = base(c)
    for slot in range(70):
        bad = raw[:4] + (1 << (slot * 6)).to_bytes(53, 'little') + raw[57:]
        execute(bad, b, 41, bad, False); counts['malformed'] += 1
    for off, val in [(0, 0), (0, 160), (1, 0), (1, 11), (2, 71), (3, 71), (3, 1),
                     (56, 16)] + [(i, 1) for i in range(57, 64)]:
        bad = bytearray(raw); bad[off] = val
        for action in (0, 40, 41):
            execute(bytes(bad), b, action, bytes(bad), False); counts['malformed'] += 1
    for off, val in [(0, 11), (1, 9), (2, 1), (3, 1), (4, 0), (22, 0)]:
        bad = bytearray(b); bad[off] = val
        execute(raw, bytes(bad), 41, raw, False); counts['malformed'] += 1
    for action in (42, 255, 0xFFFFFFFF):
        execute(raw, b, action, raw, False)
    for ptr, bp in [(state + 1, baseline), (state, baseline + 1), (state, state), (state, state + 60)]:
        execute(raw, b, 41, raw, False, ptr, bp)
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_keylog'; out.mkdir(parents=True, exist_ok=True)
    (out / 'wrapper.bin').write_bytes(blob)
    result = dict(id='exe45.hangul-keyboard.native-keylog.v1', passed=True, rom_integrated=False,
                  state_bytes=64, baseline_bytes=24, temporary_backend_bytes=304,
                  stack_bytes_including_nested_calls=472, full_syllable_creation_paths=11172,
                  loaded_tenth_cell_syllables=11172, counts=counts, machine_code=isa,
                  successful_replay_ranks_and_undo_history_compared=True,
                  dependency_reports={p.name: sha((p / 'report.json').read_bytes()) for p in deps},
                  artifacts={'wrapper.bin': sha(blob)}, tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                  ['hangul_keylog_thumb.py', 'bench_hangul_keylog_thumb.py', 'hangul_keylog_state.py',
                   'hangul_compact_thumb.py', 'hangul_extended_composer_thumb.py']},
                  limits=['Isolated aligned caller-owned state and baseline; descriptor/region extents trusted.',
                          'No game stack/IRQ ownership or timing claim; no ROM hook, display, commit or save integration.',
                          'Different valid baselines cannot be detected by keylog alone; caller must bind unchanged baseline.',
                          'Invalid vectors are boundary samples, not exhaustive invalid-domain coverage.'])
    (out / 'report.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    print('PASS', counts, flush=True)


if __name__ == '__main__':
    main()
