"""Ten-cell conversion and native read-only keylog replay integration."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_extended_composer_thumb import encode_state
from hangul_keylog_state import KeylogComposer
from hangul_ten_cell_display import CODE, display, JAMO_INDICES
from hangul_keylog_display_thumb import assemble


def main():
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    root = ROOT / 'analysis/hangul_keyboard_v1'
    dependencies = {}
    for name in ('cpu_composer', 'cpu_extended_composer', 'cpu_keylog', 'cpu_editor_display'):
        p = root / name / 'report.json'; r = json.loads(p.read_text(encoding='utf8'))
        if not r['passed'] or r['rom_integrated']:
            raise ValueError('unverified candidate dependency')
        for n, h in r['tools'].items():
            require_hash(ROOT / 'tools' / n, h)
        for n, h in r['artifacts'].items():
            require_hash(p.parent / n, h)
        dependencies[name] = sha(p.read_bytes())
    helper, hi = assemble_verified(CODE, 0x08004000, {})
    bridge, bi = assemble()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 32768)
    for a, p in [(0x08000000, root / 'cpu_extended_composer/feed.bin'),
                 (0x08001000, root / 'cpu_extended_composer/undo.bin')]:
        u.mem_write(a, p.read_bytes())
    u.mem_write(0x08004000, helper); u.mem_write(0x08006000, bridge)
    for a, n in [(0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')]:
        data = (root / 'cpu_composer' / n).read_bytes(); size = (len(data) + 4095) & ~4095
        u.mem_map(a, size); u.mem_write(a, data); u.mem_protect(a, size, UC_PROT_READ)
    u.mem_protect(0x08000000, 32768, UC_PROT_READ | UC_PROT_EXEC)
    src, dest, baseline, desc, sp, stop = 0x02000100, 0x02000201, 0x02002000, 0x02003000, 0x03007F00, 0x0FF00000
    u.mem_map(0x02000000, 4096); u.mem_map(baseline, 4096, UC_PROT_READ)
    u.mem_map(desc, 4096, UC_PROT_READ)
    u.mem_map(0x03007000, 4096); u.mem_map(stop, 4096)
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(surface=0, replay_display=0, rejected=0)

    def call(pc, args):
        u.mem_write(sp - 412, b'\x5A' * 4)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for r, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args):
            u.reg_write(r, val)
        for i, r in enumerate(regs):
            u.reg_write(r, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(pc | 1, stop, count=100000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(regs)):
            raise ValueError('return ABI')
        if bytes(u.mem_read(sp - 412, 4)) != b'\x5A' * 4:
            raise ValueError('stack boundary')
        return u.reg_read(UC_ARM_REG_R0)

    def surface(words, cap=10, active=1, depth=0):
        return bytes([len(words), cap, depth, active if words else 0]) + struct.pack('<10H', *(words + [EMPTY] * (10 - len(words))))

    def run(raw, mode=0, capacity=41, output=dest):
        try:
            expected = display(raw, mode)
        except ValueError:
            expected = None
        if expected and (capacity < len(expected) or src < output + len(expected) and output < src + 24):
            expected = None
        u.mem_write(0x02000000, b'\xA7' * 4096); u.mem_write(src, raw)
        before = bytes(u.mem_read(0x02000000, 4096))
        ret = call(0x08004000, [src, output, capacity, mode])
        if ret != (len(expected) if expected else 0):
            raise ValueError(f'surface status {raw.hex()} mode={mode} ret={ret}')
        wanted = bytearray(before)
        if expected:
            wanted[output - 0x02000000:output - 0x02000000 + len(expected)] = expected
        if bytes(u.mem_read(0x02000000, 4096)) != bytes(wanted):
            raise ValueError('surface atomic write extent')
        counts['surface'] += 1; counts['rejected'] += expected is None

    print('ten-cell full uint16 domain and ten complete-syllable slots', flush=True)
    for rank in range(65536):
        run(surface([rank]))
    for slot in range(10):
        for rank in range(11172):
            words = [0] * 10; words[slot] = rank
            run(surface(words), 1)
        print('slot', slot + 1, '/10', flush=True)
    for cap in range(1, 11):
        for count in range(1, cap + 1):
            for l in range(19):
                raw = surface([11171] * (count - 1) + [11172 + l], cap)
                run(raw); run(raw, 1); run(raw, capacity=count * 4)
            raw = surface([11171] * count, cap)
            run(raw, capacity=count * 4 + 1); run(raw, capacity=count * 4)
            for off in (-1, 0, 1, 23):
                run(raw, output=src + off)
            run(raw, output=src + 24)
    empty = surface([])
    run(empty); run(empty, 1); run(empty, capacity=0)
    for off, value in [(0, 11), (1, 0), (1, 11), (2, 1), (2, 71), (3, 1), (3, 2), (4, 0), (22, 0)]:
        bad = bytearray(empty); bad[off] = value; run(bytes(bad))
    for mode in (2, 255, 0xFFFFFFFF):
        run(empty, mode)
    run(surface([11172, 0])); run(surface([11172], active=0)); run(surface([11191]))

    def replay(c, mode=0, capacity=41, output=dest, raw=None, bp=baseline):
        raw = c.serialize() if raw is None else raw
        m = Composer(c.limit); m.load(c.baseline); b = encode_state(m)[:24]
        request = struct.pack('<7I', 0x08000001, 0x08001001, 0x09000000, 0x09200000, 0x08004001, capacity, mode)
        u.mem_write(0x02000000, b'\xA7' * 4096); u.mem_write(src, raw)
        u.mem_write(baseline, b); u.mem_write(desc, request)
        before = bytes(u.mem_read(0x02000000, 4096))
        try:
            restored = KeylogComposer.restore(raw, c.baseline)
            expected = display(encode_state(restored.model)[:24], mode)
        except ValueError:
            expected = None
        if expected and (capacity < len(expected) or output + 41 > 0xFFFFFFFF or
                         any(a < output + 41 and output < a + n for a, n in [(src, 64), (baseline, 24), (desc, 28)]) or bp != baseline):
            expected = None
        ret = call(0x08006000, [src, bp, output, desc])
        if ret != (len(expected) if expected else 0):
            raise ValueError(f'replay display status raw={raw.hex()} mode={mode} ret={ret}')
        wanted = bytearray(before)
        if expected:
            wanted[output - 0x02000000:output - 0x02000000 + len(expected)] = expected
        if bytes(u.mem_read(0x02000000, 4096)) != bytes(wanted) or bytes(u.mem_read(baseline, 24)) != b or bytes(u.mem_read(desc, 28)) != request:
            raise ValueError('replay output/state/baseline/descriptor write extent')
        counts['replay_display'] += 1; counts['rejected'] += expected is None

    print('native replay -> display, full syllables at tenth loaded cell', flush=True)
    for rank in range(11172):
        c = KeylogComposer(10, '가' * 9 + chr(0xAC00 + rank))
        replay(c, 1)
    # Every supported syllable also gets a fresh key-log replay path.
    for l in INITIALS:
        for v in MEDIALS:
            for t in FINALS:
                c = KeylogComposer(1)
                for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                    c.press(k); replay(c)
                replay(c, 1)
        print('fresh replay initial', INITIALS.index(l) + 1, '/19', flush=True)
    c = KeylogComposer(10, chr(0xAC00 + 588 + 10 * 28 + 9) * 10)
    replay(c)
    while c.backspace():
        replay(c)
    for key in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10:
        c.press(key); replay(c); replay(c, 1)
    replay(c, capacity=40); replay(c, capacity=32)
    while c.backspace():
        replay(c)
    for off, value in [(0, 0), (1, 11), (2, 71), (3, 71), (56, 16)] + [(i, 1) for i in range(57, 64)]:
        bad = bytearray(c.serialize()); bad[off] = value; replay(c, raw=bytes(bad))
    # Invalid but structurally bounded logs must fail canonical replay too.
    raw = c.serialize()
    for slot in range(70):
        bad = raw[:4] + (1 << (slot * 6)).to_bytes(53, 'little') + raw[57:]
        replay(c, raw=bad)
    bad = bytearray(raw); bad[3] = 1; replay(c, raw=bytes(bad))
    bad = bytearray(raw); bad[2] = 1; bad[4] = 63; replay(c, raw=bytes(bad))
    for mode in (2, 255, 0xFFFFFFFF):
        replay(c, mode=mode)
    replay(c, capacity=0)
    for output in (src - 41, src + 64):
        replay(c, output=output)
    for off in (-40, -1, 0, 63):
        replay(c, output=src + off)
    for output in (baseline, desc, 0xFFFFFFF0):
        replay(c, output=output)
    replay(c, bp=baseline + 1)
    out = root / 'cpu_ten_cell_display'; out.mkdir(parents=True, exist_ok=True)
    (out / 'helper.bin').write_bytes(helper); (out / 'bridge.bin').write_bytes(bridge)
    result = dict(id='exe45.hangul-keyboard.ten-cell-display.v1', passed=True, rom_integrated=False,
                  counts=counts, full_uint16_rank_domain=65536, complete_syllable_slot_vectors=111720,
                  full_syllable_keylog_paths=11172, loaded_tenth_cell_syllables=11172,
                  source_surface_bytes=24, output_max_bytes=41, stack_bytes_including_nested_calls=408,
                  native_readonly_keylog_to_display=True, machine_code=dict(helper=hi, bridge=bi),
                  jamo_mapping=JAMO_INDICES, preserved_comma_index=11172, dependency_reports=dependencies,
                  artifacts={n: sha((out / n).read_bytes()) for n in ('helper.bin', 'bridge.bin')},
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in
                         ['hangul_ten_cell_display.py', 'hangul_keylog_display_thumb.py', 'bench_hangul_ten_cell_display.py']},
                  limits=['Isolated CPU fixtures only; no ROM hooks, glyph consumption, cursor/padding or cache lifetime claim.',
                          'Valid caller pointer extents and trusted descriptor; output must be outside stack workspace.',
                          'Canonical full replay validates keylog; surface helper alone does not validate undo history.',
                          'Original 32-byte descriptor0 cannot hold ten-cell 41-byte output.',
                          'Game stack/IRQ/timing, legacy import, record, save and fresh-load remain unresolved.'])
    (out / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS ten-cell display', counts, flush=True)


if __name__ == '__main__':
    main()
