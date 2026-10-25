"""Execute emitted baseline decoder; standalone caller memory, not game RAM."""
import json
import struct
import sys
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from extended_dialogue import assemble_verified
from hangul_baseline_bridge import CODE, baseline
from hangul_record_candidate import pack
sys.path.insert(0, str(ROOT / 'external/arm_bench_python'))
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_PROT_READ, UC_PROT_EXEC, UC_PROT_WRITE
from unicorn.arm_const import *


def expected(text, cap):
    return bytes([len(text), cap, 0, int(bool(text))]) + struct.pack(
        '<8H', *([ord(c) - 0xAC00 for c in text] + [0xFFFF] * (8 - len(text))))


def main():
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    address, stop = 0x08002000, 0x0FF00000
    blob, isa = assemble_verified(CODE, address, {})
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(address, 4096)
    u.mem_write(address, blob)
    u.mem_protect(address, 4096, UC_PROT_READ | UC_PROT_EXEC)
    u.mem_map(0x02000000, 4096)
    u.mem_map(0x03007000, 4096)
    u.mem_map(stop, 4096)
    src, dest, sp = 0x02000101, 0x02000201, 0x03007F00
    preserved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                 UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = {'accepted': 0, 'rejected': 0, 'legacy_routed_without_write': 0}

    def run(record, cap, status, output=None, size=20, destination=dest):
        u.mem_write(0x02000100, b'\xA7' * 512)
        u.mem_write(src, record)
        before = bytes(u.mem_read(0x02000100, 512))
        u.mem_write(sp - 24, b'\x5A' * 4)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for reg, value in [(UC_ARM_REG_R0, src), (UC_ARM_REG_R1, cap),
                           (UC_ARM_REG_R2, destination), (UC_ARM_REG_R3, size),
                           (UC_ARM_REG_SP, sp), (UC_ARM_REG_LR, stop | 1)]:
            u.reg_write(reg, value)
        for index, reg in enumerate(preserved):
            u.reg_write(reg, 0x13579000 + index)
        u.emu_start(address | 1, stop, count=1000)
        if (u.reg_read(UC_ARM_REG_PC), u.reg_read(UC_ARM_REG_SP), u.reg_read(UC_ARM_REG_R0)) != (stop, sp, status):
            raise ValueError('return ABI')
        if any(u.reg_read(reg) != 0x13579000 + i for i, reg in enumerate(preserved)):
            raise ValueError('callee register changed')
        after = bytearray(before)
        if output is not None:
            if len(output) != 20 or status != 1:
                raise ValueError('bad fixture')
            start = destination - 0x02000100
            after[start:start + 20] = output
        if bytes(u.mem_read(0x02000100, 512)) != bytes(after) or bytes(u.mem_read(sp - 24, 4)) != b'\x5A' * 4:
            raise ValueError('output/source/reject/stack boundary')
        counts[{0: 'rejected', 1: 'accepted', 2: 'legacy_routed_without_write'}[status]] += 1

    for cap in (4, 8):
        for slot in range(cap):
            for rank in range(11172):
                text = '가' * slot + chr(0xAC00 + rank) + '힣' * (cap - slot - 1)
                record, wanted = pack(text, cap), expected(text, cap)
                if baseline(record, cap) != (1, wanted):
                    raise ValueError('host baseline contract')
                run(record, cap, 1, wanted)
    for rank in range(11172, 65536):
        run(b'\x81' + struct.pack('<H', rank) + b'\xE5', 1, 0)
    for cap in range(1, 9):
        for count in range(1, cap + 1):
            text = '힣' * count
            record, wanted = pack(text, cap), expected(text, cap)
            run(record, cap, 1, wanted)
            run(record, cap, 1, wanted, destination=src + len(record))
            run(record, cap, 0, size=19)
            for offset in (-19, -1, 0, len(record) - 1):
                run(record, cap, 0, destination=src + offset)
        absent = b'\x00' + b'\x7E' * (2 * cap) + b'\x00'
        run(absent, cap, 1, expected('', cap))
        run(b'\x01' + absent[1:], cap, 2)
        good = pack('가', cap)
        for marker in range(2, 256):
            if marker != 0x81:
                run(bytes([marker]) + good[1:], cap, 0)
        for end in (0, 0x98, 0xE4, 0xFF):
            run(good[:-1] + bytes([end]), cap, 0)
        for slot in range(cap):
            bad = bytearray(good)
            bad[1 + 2 * slot:3 + 2 * slot] = b'\xA4\x2B' if slot == 0 else b'\x00\x00'
            run(bytes(bad), cap, 0)
    for cap in (0, 9, 0xFFFFFFFF):
        run(pack('가', 1), cap, 0)
    for destination in (0xFFFFFFF0, 0xFFFFFFFF):
        run(pack('가', 1), 1, 0, destination=destination)
    # Consume this helper's emitted baseline with the already verified native
    # replay wrapper; do not replace the bridge output with a host baseline.
    from hangul_compact_state import CompactComposer
    from hangul_composer_thumb import KEYS
    dependency = ROOT / 'analysis/hangul_keyboard_v1/cpu_composer'
    compact_dir = ROOT / 'analysis/hangul_keyboard_v1/cpu_compact'
    backend = json.loads((dependency / 'report.json').read_text(encoding='utf8'))
    wrapper = json.loads((compact_dir / 'report.json').read_text(encoding='utf8'))
    if not backend['passed'] or not wrapper['passed']:
        raise ValueError('unverified replay dependencies')
    for directory, data in [(dependency, backend), (compact_dir, wrapper)]:
        for n, h in data['artifacts'].items():
            require_hash(directory / n, h)
        for n, h in data['tools'].items():
            require_hash(ROOT / 'tools' / n, h)
    v = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    v.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    v.mem_map(0x08000000, 0x5000)
    for a, p in [(0x08000000, dependency / 'feed.bin'), (0x08001000, dependency / 'undo.bin'),
                 (0x08002000, compact_dir / 'wrapper.bin')]:
        v.mem_write(a, p.read_bytes())
    v.mem_write(0x08004000, blob)
    v.mem_write(0x08003000, struct.pack('<4I', 0x08000001, 0x08001001, 0x09000000, 0x09200000))
    v.mem_protect(0x08000000, 0x5000, UC_PROT_READ | UC_PROT_EXEC)
    for a, name in [(0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')]:
        data = (dependency / name).read_bytes()
        extent = (len(data) + 4095) & ~4095
        v.mem_map(a, extent)
        v.mem_write(a, data)
        v.mem_protect(a, extent, UC_PROT_READ)
    v.mem_map(0x02000000, 0x3000)
    v.mem_map(0x03007000, 4096)
    v.mem_map(stop, 4096)
    state, record_ptr, base_ptr = 0x02000080, 0x02001001, 0x02002000
    integration = 0
    for text, cap in [('', 4), ('가', 4), ('국어', 4), ('꽭', 4), ('힣' * 8, 8)]:
        record = pack(text, cap) if text else b'\x00' + b'\x7E' * (2 * cap) + b'\x00'
        v.mem_write(record_ptr, record)
        v.mem_protect(0x02002000, 4096, UC_PROT_READ | UC_PROT_WRITE)
        v.reg_write(UC_ARM_REG_CPSR, 0x30)
        for reg, value in [(UC_ARM_REG_R0, record_ptr), (UC_ARM_REG_R1, cap),
                           (UC_ARM_REG_R2, base_ptr), (UC_ARM_REG_R3, 20),
                           (UC_ARM_REG_SP, sp), (UC_ARM_REG_LR, stop | 1)]:
            v.reg_write(reg, value)
        v.emu_start(0x08004001, stop, count=1000)
        native_base = bytes(v.mem_read(base_ptr, 20))
        if v.reg_read(UC_ARM_REG_R0) != 1 or native_base != expected(text, cap):
            raise ValueError('native bridge integration output')
        v.mem_protect(0x02002000, 4096, UC_PROT_READ)
        v.mem_write(state - 4, b'\xA7' * 4 + native_base + bytes(44) + b'\xA7' * 4)
        model = CompactComposer(cap, text)
        for action in [41, 40, 41, 0, 19, 41, 40]:
            accepted = model.press(KEYS[action]) if action < 40 else model.backspace() if action == 40 else True
            v.reg_write(UC_ARM_REG_CPSR, 0x30)
            for reg, value in [(UC_ARM_REG_R0, state), (UC_ARM_REG_R1, base_ptr),
                               (UC_ARM_REG_R2, action), (UC_ARM_REG_R3, 0x08003000),
                               (UC_ARM_REG_SP, sp), (UC_ARM_REG_LR, stop | 1)]:
                v.reg_write(reg, value)
            for i, reg in enumerate(preserved):
                v.reg_write(reg, 0x13579000 + i)
            v.mem_write(sp - 448, b'\x5A' * 4)
            v.emu_start(0x08002001, stop, count=100000)
            if (v.reg_read(UC_ARM_REG_PC), v.reg_read(UC_ARM_REG_SP), v.reg_read(UC_ARM_REG_R0)) != (stop, sp, int(accepted)):
                raise ValueError('native bridge/replay return')
            if bytes(v.mem_read(state - 4, 72)) != b'\xA7' * 4 + model.serialize() + b'\xA7' * 4:
                raise ValueError('native bridge/replay state')
            if bytes(v.mem_read(base_ptr, 20)) != native_base or bytes(v.mem_read(record_ptr, len(record))) != record:
                raise ValueError('immutable baseline/source changed')
            if bytes(v.mem_read(sp - 448, 4)) != b'\x5A' * 4 or any(v.reg_read(reg) != 0x13579000 + i for i, reg in enumerate(preserved)):
                raise ValueError('native bridge/replay preserved boundary')
            integration += 1
    out = ROOT / 'analysis/hangul_keyboard_v1/cpu_baseline_bridge'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'helper.bin').write_bytes(blob)
    report = dict(id='exe45.hangul-keyboard.baseline-bridge.v1', passed=True,
                  rom_integrated=False, record_format_adopted=False,
                  counts=counts, complete_syllable_slot_vectors=11172 * 12,
                  occupied_uint16_rank_domain=65536, baseline_bytes=20, stack_bytes=20,
                  helper_sha256=sha(blob), machine_code=isa,
                  native_bridge_to_compact_paths=integration,
                  dependencies={str(p.relative_to(ROOT)).replace('\\', '/'): sha(p.read_bytes()) for p in
                                [dependency / 'report.json', compact_dir / 'report.json']},
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                         ['hangul_baseline_bridge.py', 'bench_hangul_baseline_bridge.py',
                          'hangul_record_candidate.py', 'hangul_composer_thumb.py']},
                  limits=['Native marker0 is treated as absent, payload ignored; candidate markers81..88 are not adopted save ABI.',
                          'Marker1 returns legacy routing result2 without output writes, NOT Japanese format validation or editable legacy support.',
                          'Caller-owned readable source/writable destination extents; no actual game baseline lifetime, stack/IRQ or RAM reservation proof.',
                          'Full repertoire every slot for capacities4/8 and single occupied uint16 domain; other cases are boundary samples.'])
    (out / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print('PASS emitted baseline bridge', counts, '; game hooks and legacy handling pending')


if __name__ == '__main__':
    main()
