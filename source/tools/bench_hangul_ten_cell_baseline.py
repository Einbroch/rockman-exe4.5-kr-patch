"""Caller-selected baseline24 conversion and native replay/display fixtures."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_ten_cell_baseline import CODE, baseline, pack, unpack
from hangul_keylog_state import KeylogComposer
from hangul_extended_composer_thumb import encode_state
from hangul_ten_cell_display import display


def expected(text, cap):
    return bytes([len(text), cap, 0, int(bool(text))]) + struct.pack('<10H', *([ord(c) - 0xAC00 for c in text] + [0xFFFF] * (10 - len(text))))


def main():
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble_verified(CODE, 0x08005000, {})
    root = ROOT / 'analysis/hangul_keyboard_v1'
    dependencies = {}
    for name in ('cpu_composer', 'cpu_extended_composer', 'cpu_keylog', 'cpu_ten_cell_display'):
        p = root / name / 'report.json'; r = json.loads(p.read_text(encoding='utf8'))
        if not r['passed'] or r['rom_integrated']:
            raise ValueError('unverified dependency')
        for n, h in r['tools'].items():
            require_hash(ROOT / 'tools' / n, h)
        for n, h in r['artifacts'].items():
            require_hash(p.parent / n, h)
        dependencies[name] = sha(p.read_bytes())
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 32768)
    for a, p in [(0x08000000, root / 'cpu_extended_composer/feed.bin'),
                 (0x08001000, root / 'cpu_extended_composer/undo.bin'),
                 (0x08002000, root / 'cpu_keylog/wrapper.bin'),
                 (0x08004000, root / 'cpu_ten_cell_display/helper.bin'),
                 (0x08006000, root / 'cpu_ten_cell_display/bridge.bin')]:
        u.mem_write(a, p.read_bytes())
    u.mem_write(0x08005000, blob)
    u.mem_protect(0x08000000, 32768, UC_PROT_READ | UC_PROT_EXEC)
    for a, n in [(0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')]:
        data = (root / 'cpu_composer' / n).read_bytes(); size = (len(data) + 4095) & ~4095
        u.mem_map(a, size); u.mem_write(a, data); u.mem_protect(a, size, UC_PROT_READ)
    src, dest, state, sp, stop = 0x02000101, 0x02000200, 0x02000080, 0x03007F00, 0x0FF00000
    u.mem_map(0x02000000, 4096); u.mem_map(0x02002000, 4096, UC_PROT_READ)
    u.mem_map(0x03007000, 4096); u.mem_map(stop, 4096)
    descriptor = struct.pack('<7I', 0x08000001, 0x08001001, 0x09000000, 0x09200000, 0x08004001, 41, 0)
    u.mem_write(0x02002000, descriptor)
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(convert=0, rejected=0, legacy_without_write=0, native_initialize=0, native_edit=0, native_display=0)

    def call(pc, args, stack_bytes=20):
        u.mem_write(sp - stack_bytes - 4, b'\x5A' * 4)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for r, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args):
            u.reg_write(r, val)
        for i, r in enumerate(regs):
            u.reg_write(r, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(pc | 1, stop, count=100000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(regs)):
            raise ValueError('return ABI')
        if bytes(u.mem_read(sp - stack_bytes - 4, 4)) != b'\x5A' * 4:
            raise ValueError('stack boundary')
        return u.reg_read(UC_ARM_REG_R0)

    def run(record, cap, imported, status, wanted=None, size=24, output=dest, request=None):
        u.mem_write(0x02000000, b'\xA7' * 4096); u.mem_write(src, record)
        before = bytes(u.mem_read(0x02000000, 4096))
        config = cap | (int(imported) << 8) if request is None else request
        ret = call(0x08005000, [src, config, output, size])
        if ret != status:
            raise ValueError(f'conversion status cap={cap} request={config} record={record.hex()} ret={ret} wanted={status}')
        after = bytearray(before)
        if wanted is not None:
            after[output - 0x02000000:output - 0x02000000 + 24] = wanted
        if bytes(u.mem_read(0x02000000, 4096)) != bytes(after):
            raise ValueError('conversion atomic write extent')
        counts['convert'] += 1; counts['rejected'] += status == 0; counts['legacy_without_write'] += status == 2

    print('baseline24 full rank domain and ten-cell repertoire', flush=True)
    for rank in range(65536):
        rec = b'\x81' + struct.pack('<H', rank) + b'\xE5'
        run(rec, 1, True, int(rank < 11172), expected(chr(0xAC00 + rank), 1) if rank < 11172 else None)
    for slot in range(10):
        for rank in range(11172):
            text = '가' * slot + chr(0xAC00 + rank) + '힣' * (9 - slot)
            rec = pack(text, 10); wanted = expected(text, 10)
            if unpack(rec, 10) != text or baseline(rec, 10, True) != (1, wanted):
                raise ValueError('host round-trip')
            run(rec, 10, True, 1, wanted)
        print('baseline slot', slot + 1, '/10', flush=True)
    from hangul_record_candidate import pack as old_pack
    for cap in range(1, 11):
        for count in range(1, cap + 1):
            rec = pack('힣' * count, cap); wanted = expected('힣' * count, cap)
            if cap <= 8 and rec != old_pack('힣' * count, cap):
                raise ValueError('old candidate byte compatibility')
            run(rec, cap, True, 1, wanted)
            run(rec, cap, False, 1, expected('', cap))
            run(rec, cap, True, 1, wanted, output=src + len(rec))
            run(rec, cap, True, 0, size=23)
            for offset in (-23, -1, 0, len(rec) - 1):
                run(rec, cap, True, 0, output=src + offset)
        good = pack('가', cap)
        for marker in range(256):
            rec = bytes([marker]) + good[1:]
            try:
                status, wanted = baseline(rec, cap, True)
            except ValueError:
                status, wanted = 0, None
            run(rec, cap, True, status, wanted)
            # Caller has deliberately requested a fresh entry: marker is not
            # a substitute for that decision, including stale Hangul payload.
            run(rec, cap, False, 1, expected('', cap))
        for marker in (0, 1):
            for payload in (b'\x9B\xE5', b'\xE4\x20', b'\x98\xFF'):
                rec = bytes([marker]) + (payload * (cap + 1))[:2 * cap + 1]
                run(rec, cap, True, 2)
        for value in (0, 0x98, 0xE4, 0xFF):
            run(good[:-1] + bytes([value]), cap, True, 0)
        for slot in range(cap):
            bad = bytearray(good); bad[1 + 2 * slot:3 + 2 * slot] = b'\xA4\x2B' if slot == 0 else b'\x00\x00'
            run(bytes(bad), cap, True, 0)
    for request in (0, 11, 0x100, 0x10B, 0x201, 0x301, 0xFFFFFFFF):
        run(pack('가', 1), 1, True, 0, request=request)
    for output in (0xFFFFFFF0, 0xFFFFFFFF):
        run(pack('가', 1), 1, True, 0, output=output)

    def initialize(text, cap):
        rec = pack(text, cap) if text else b'\x00' + b'\x7E' * (2 * cap + 1)
        u.mem_write(src, rec); u.mem_write(dest, b'\xA7' * 24)
        before = bytearray(u.mem_read(0x02000000, 4096))
        if call(0x08005000, [src, cap | (0x100 if text else 0), dest, 24]) != 1 or bytes(u.mem_read(dest, 24)) != expected(text, cap):
            raise ValueError('native initializer')
        before[dest - 0x02000000:dest - 0x02000000 + 24] = expected(text, cap)
        if bytes(u.mem_read(0x02000000, 4096)) != bytes(before):
            raise ValueError('initializer atomic write extent')
        counts['native_initialize'] += 1
        u.mem_write(state, KeylogComposer(cap, text).serialize())
        return rec, bytes(u.mem_read(dest, 24))

    def redisplay(model, rec, native_base):
        before = bytes(u.mem_read(0x02000000, 4096))
        result = display(encode_state(model.model)[:24])
        output = 0x02000401
        if call(0x08006000, [state, dest, output, 0x02002000], 408) != len(result):
            raise ValueError('native imported display return')
        after = bytearray(before); after[output - 0x02000000:output - 0x02000000 + len(result)] = result
        if bytes(u.mem_read(0x02000000, 4096)) != bytes(after) or bytes(u.mem_read(dest, 24)) != native_base or bytes(u.mem_read(src, len(rec))) != rec:
            raise ValueError('native import/display atomic write extent')
        counts['native_display'] += 1

    print('native baseline -> keylog -> display, tenth-cell full repertoire', flush=True)
    for rank in range(11172):
        text = '가' * 9 + chr(0xAC00 + rank)
        rec, native_base = initialize(text, 10)
        redisplay(KeylogComposer(10, text), rec, native_base)
    for text, cap in [('', 1), ('가', 4), ('국어', 4), ('꽭', 10), ('힣' * 10, 10), (chr(0xAC00 + 588 + 10 * 28 + 9) * 10, 10)]:
        rec, native_base = initialize(text, cap); model = KeylogComposer(cap, text)
        for action in [41] + [40] * 71 + [KEYS.index(k) for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * cap] + [41] + [40] * 71:
            before = bytearray(u.mem_read(0x02000000, 4096))
            ok = model.press(KEYS[action]) if action < 40 else model.backspace() if action == 40 else True
            if call(0x08002000, [state, dest, action, 0x02002000], 472) != int(ok) or bytes(u.mem_read(state, 64)) != model.serialize():
                raise ValueError('native imported edit state')
            if bytes(u.mem_read(dest, 24)) != native_base or bytes(u.mem_read(src, len(rec))) != rec:
                raise ValueError('import baseline/source changed')
            before[state - 0x02000000:state - 0x02000000 + 64] = model.serialize()
            if bytes(u.mem_read(0x02000000, 4096)) != bytes(before):
                raise ValueError('import/edit atomic write extent')
            counts['native_edit'] += 1
            redisplay(model, rec, native_base)
    out = root / 'cpu_ten_cell_baseline'; out.mkdir(parents=True, exist_ok=True)
    (out / 'helper.bin').write_bytes(blob)
    report = dict(id='exe45.hangul-keyboard.ten-cell-baseline.v1', passed=True, rom_integrated=False,
                  record_format_adopted=False, counts=counts, baseline_bytes=24, stack_bytes=20,
                  candidate_capacity=10, complete_syllable_slot_vectors=111720, occupied_uint16_rank_domain=65536,
                  native_tenth_cell_baseline_to_display_paths=11172, caller_selected_import=True,
                  legacy_marker0_import_preserved=True, machine_code=isa, dependency_reports=dependencies,
                  artifacts={'helper.bin': sha(blob)}, tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                         ['hangul_ten_cell_baseline.py', 'bench_hangul_ten_cell_baseline.py', 'hangul_baseline_bridge.py', 'hangul_record_candidate.py']},
                  limits=['Experimental marker81..8A/width2*cap+2 is NOT adopted native save ABI.',
                          'Caller decides import explicitly; marker0/1 import returns2 without validating or editing Japanese text.',
                          'Caller-owned source/output extents; no game baseline lifetime, stack/IRQ or ROM hook proof.',
                          'Legacy/unknown format support and commit/save/fresh-load remain unresolved; CPU integration is not game runtime.'])
    (out / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf8')
    print('PASS caller-selected ten-cell baseline', counts, flush=True)


if __name__ == '__main__':
    main()
