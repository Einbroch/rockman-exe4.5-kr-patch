"""Native ten-cell boundary tests; no runtime or key-log wrapper claim."""
import json
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_extended_composer_thumb import FEED, UNDO, STATE_BYTES, encode_state


def main():
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    dep = ROOT / 'analysis/hangul_keyboard_v1/cpu_composer'
    report = json.loads((dep / 'report.json').read_text(encoding='utf8'))
    if not report['passed']:
        raise ValueError('unverified table dependency')
    for n, h in report['tools'].items():
        require_hash(ROOT / 'tools' / n, h)
    for n, h in report['artifacts'].items():
        require_hash(dep / n, h)
    feed, fi = assemble_verified(FEED, 0x08000000, {})
    undo, ui = assemble_verified(UNDO, 0x08001000, {})
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 8192)
    u.mem_write(0x08000000, feed)
    u.mem_write(0x08001000, undo)
    u.mem_protect(0x08000000, 8192, UC_PROT_READ | UC_PROT_EXEC)
    for a, name in [(0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')]:
        data = (dep / name).read_bytes()
        size = (len(data) + 4095) & ~4095
        u.mem_map(a, size)
        u.mem_write(a, data)
        u.mem_protect(a, size, UC_PROT_READ)
    u.mem_map(0x02000000, 4096)
    u.mem_map(0x03007000, 4096)
    u.mem_map(0x0FF00000, 4096)
    state, sp, stop = 0x02000100, 0x03007F00, 0x0FF00000
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(feed=0, undo=0, rejected=0)

    def execute(raw, wanted, accepted, key=None, capacity=304):
        u.mem_write(state - 4, b'\xA7' * 4 + raw + b'\xA7' * 4)
        u.mem_write(sp - 56, b'\x5A' * 4)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        args = [state, capacity, 0x09200000, 0] if key is None else [state, key, 0x09000000, capacity]
        for reg, value in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args):
            u.reg_write(reg, value)
        for i, reg in enumerate(regs):
            u.reg_write(reg, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp)
        u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start((0x08001000 if key is None else 0x08000000) | 1, stop, count=1000)
        if (u.reg_read(UC_ARM_REG_PC), u.reg_read(UC_ARM_REG_SP), u.reg_read(UC_ARM_REG_R0)) != (stop, sp, int(accepted)):
            raise ValueError('extended return ABI')
        if any(u.reg_read(reg) != 0x13579000 + i for i, reg in enumerate(regs)):
            raise ValueError('callee register changed')
        if bytes(u.mem_read(state - 4, 312)) != b'\xA7' * 4 + wanted + b'\xA7' * 4 or bytes(u.mem_read(sp - 56, 4)) != b'\x5A' * 4:
            raise ValueError('extended state/stack boundary')
        counts['undo' if key is None else 'feed'] += 1
        counts['rejected'] += not accepted

    def press(c, key):
        raw = encode_state(c)
        accepted = c.press(key)
        execute(raw, encode_state(c), accepted, KEYS.index(key))
        return accepted

    def back(c):
        raw = encode_state(c)
        accepted = c.backspace()
        execute(raw, encode_state(c), accepted)
        return accepted

    # Every syllable reaches slot10; loaded baseline has no accepted-key undo
    # history and a sealed ninth cell before the fresh final syllable.
    for li, l in enumerate(INITIALS):
        for vi, v in enumerate(MEDIALS):
            for ti, t in enumerate(FINALS):
                c = Composer(10)
                c.state = State(tuple('가' * 9))
                for key in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                    if not press(c, key):
                        raise ValueError('tenth syllable rejected')
                if c.candidate() != '가' * 9 + chr(0xAC00 + li * 588 + vi * 28 + ti):
                    raise ValueError('tenth syllable identity')
                while c.history:
                    back(c)
                c.load('가' * 9 + chr(0xAC00 + li * 588 + vi * 28 + ti))
                while len(c.display) == 10:
                    back(c)
    c = Composer(10)
    for key in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10:
        if not press(c, key):
            raise ValueError('70-key maximum rejected')
    if len(c.history) != 70 or len(c.candidate()) != 10:
        raise ValueError('maximum extent')
    # At history70, a new action is rejected atomically by both semantic
    # capacity and the backend's declared undo-capacity boundary.
    press(c, 'ㄱ')
    while c.history:
        back(c)
    back(c)
    for cap in (1, 4, 8, 9, 10):
        c = Composer(cap)
        for key in 'ㄱㅗㅏㄹㄱㅏ':
            press(c, key)
        while back(c):
            pass
    raw = encode_state(Composer(10))
    for capacity in (0, 276, 303):
        execute(raw, raw, False, 0, capacity)
        execute(raw, raw, False, capacity=capacity)
    for off, value in [(1, 0), (1, 11), (2, 71), (3, 2), (22, 0)]:
        bad = bytearray(raw)
        bad[off] = value
        for key in (0, None):
            execute(bytes(bad), bytes(bad), False, key)
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_extended_composer'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'feed.bin').write_bytes(feed)
    (out / 'undo.bin').write_bytes(undo)
    data = dict(id='exe45.hangul-keyboard.extended-composer.v1', passed=True, rom_integrated=False,
                state_bytes=STATE_BYTES, capacity=10, max_undo=70, stack_bytes=52,
                tenth_cell_syllables=11172, counts=counts, machine_code=dict(feed=fi, undo=ui),
                dependency_report_sha256=sha((dep / 'report.json').read_bytes()),
                artifacts={'feed.bin': sha(feed), 'undo.bin': sha(undo)},
                tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                       ['hangul_extended_composer_thumb.py', 'bench_hangul_extended_composer.py']},
                limits=['304-byte state is temporary CPU fixture memory, not reserved game RAM.',
                        'Slot10 full repertoire and boundary samples; not a rerun of all row/key/capacity combinations.',
                        '64-byte key-log native replay/display/import/record bridge and real stack/IRQ timing are pending.'])
    (out / 'report.json').write_text(json.dumps(data, indent=2), encoding='utf8')
    print('PASS ten-cell native backend', counts, '; game integration pending')


if __name__ == '__main__':
    main()
