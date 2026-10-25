"""Execute emitted compact decoder over serialized bytes, not game runtime."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_READ
from hangul_mixed_replay_thumb import CODE
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag


def raw_state(cap, baseline, keys=()):
    words = baseline.cells + (65535,) * (10 - len(baseline.cells))
    active = 15 if baseline.active is None else baseline.active
    bits = sum(k << (6 * i) for i, k in enumerate(keys)) | (11 << 420)
    return bytes([cap | len(baseline.cells) << 4, baseline.cursor | active << 4, len(keys)]) + struct.pack('<10H', *words) + bits.to_bytes(53, 'little')


def surface(model):
    s = model.state
    return bytes([len(s.cells), model.capacity, s.cursor, 255 if s.active is None else s.active]) + struct.pack('<10H', *(s.cells + (65535,) * (10 - len(s.cells))))


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'
    old_path = root / 'cpu_composer/report.json'; old = json.loads(old_path.read_text(encoding='utf8'))
    for n, h in old['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    for n, h in old['artifacts'].items(): require_hash(old_path.parent / n, h)
    host_path = root / 'mixed_replay_host.json'; host = json.loads(host_path.read_text(encoding='utf8'))
    if not host['passed'] or host['rom_integrated'] or host['state_bytes'] != 76: raise ValueError('compact host scope')
    for n, h in host['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble_verified(CODE, 0x08000000, {})
    out = root / 'cpu_mixed_replay'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob); blob = (out / 'helper.bin').read_bytes()
    pairs = (root / 'cpu_composer/transitions.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 4096); u.mem_write(0x08000000, blob)
    u.mem_protect(0x08000000, 4096, UC_PROT_READ | UC_PROT_EXEC)
    u.mem_map(0x09000000, (len(pairs) + 4095) & ~4095); u.mem_write(0x09000000, pairs)
    u.mem_protect(0x09000000, (len(pairs) + 4095) & ~4095, UC_PROT_READ)
    u.mem_map(0x02000000, 8192); u.mem_protect(0x02000000, 4096, UC_PROT_READ)
    u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    src, dest, sp, stop = 0x02000101, 0x02001103, 0x03007F00, 0x0FF00000
    preserved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                 UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(calls=0, accepted=0, rejected=0, row_key_vectors=0,
                  syllable_slot_paths=0, occupied_word_domain=0, malformed=0,
                  profiled_reads=0)
    profile = None

    def reads(uc, access, address, size, value, userdata):
        if profile is not None and not any(a <= address and address + size <= b for a, b in profile):
            raise ValueError(f'out-of-contract read {address:08X}+{size}')

    def run(raw, wanted, accepted=True, source=src, output=dest, source_bytes=76, output_bytes=24, audit=False, source_argument=None):
        nonlocal profile
        u.mem_write(0x02000000, b'\xA7' * 8192); u.mem_write(source, raw)
        before = bytes(u.mem_read(0x02000000, 8192))
        # Native source page is read-only in normal fixtures; for intentional
        # adjacency/overlap fixtures permit output writes but audit all bytes.
        u.mem_protect(0x02000000, 4096, UC_PROT_READ if output >= 0x02001000 else UC_PROT_READ | 2)
        u.mem_write(sp - 72, b'\x5A' * 72)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for reg, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],
                            [source if source_argument is None else source_argument, output, source_bytes | output_bytes << 16, 0x09000000]): u.reg_write(reg, val)
        for i, reg in enumerate(preserved): u.reg_write(reg, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        profile = [(source, source + 76), (sp - 68, sp), (0x09000000, 0x09000000 + len(pairs))] if audit else None
        hook = u.hook_add(UC_HOOK_MEM_READ, reads) if audit else None
        u.emu_start(0x08000001, stop, count=25000)
        if hook is not None: u.hook_del(hook)
        profile = None
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_R0) != int(accepted):
            raise ValueError(f'CPU status expected={accepted} raw={raw.hex()}')
        if u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(preserved)):
            raise ValueError('ABI')
        if bytes(u.mem_read(sp - 72, 4)) != b'\x5A' * 4: raise ValueError('stack68 lower boundary')
        expected = bytearray(before)
        if accepted: expected[output - 0x02000000:output - 0x02000000 + 24] = wanted
        if bytes(u.mem_read(0x02000000, 8192)) != bytes(expected): raise ValueError('atomic output/source/bounds')
        counts['calls'] += 1; counts['accepted' if accepted else 'rejected'] += 1
        counts['profiled_reads'] += audit

    print('compact replay all11192 rows x40 keys', flush=True)
    for rank in range(11192):
        for key, k in enumerate(KEYS):
            c = MixedReplay(3)
            c.baseline = Snapshot((rank, tag(b'\x9B'), tag(b'\xE4\x00')), 1, 0) if rank < 11191 else Snapshot((), 0, None)
            c.model.state = c.baseline
            accepted = c.press(k)
            run(raw_state(3, c.baseline, [key]), surface(c.model) if accepted else None, accepted)
            counts['row_key_vectors'] += 1
        if rank % 2800 == 0: print('row', rank, '/11192', flush=True)
    legacy = tuple(tag(bytes([0x9B + i])) for i in range(10))
    for slot in range(10):
        for li, l in enumerate(INITIALS):
            for vi, v in enumerate(MEDIALS):
                for ti, t in enumerate(FINALS):
                    c = MixedReplay(10); c.baseline = Snapshot(legacy, slot, None); c.model.state = c.baseline
                    for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))): c.press(k)
                    wanted = list(legacy); wanted[slot] = li * 588 + vi * 28 + ti
                    if c.model.state.cells != tuple(wanted): raise ValueError('host target')
                    run(raw_state(10, c.baseline, c.keys), surface(c.model))
                    counts['syllable_slot_paths'] += 1
        print('compact replay slot', slot + 1, '/10', flush=True)
    base = raw_state(1, Snapshot((0,), 0, None))
    for word in range(65536):
        raw = bytearray(base); struct.pack_into('<H', raw, 3, word)
        valid = word < 11191 or 0x8000 <= word <= 0x80E3 or 0x8100 <= word <= 0x81FF
        wanted = bytes([1, 1, 0, 255]) + struct.pack('<10H', word, *([65535] * 9)) if valid else None
        run(bytes(raw), wanted, valid); counts['occupied_word_domain'] += 1
    c = MixedReplay(10)
    for i, k in enumerate('ㄱㄱㅗㅏㅣㄹㄱ' * 10):
        c.press(k); run(c.serialize(), surface(c.model), audit=i in (0, 5, 69))
    for _ in range(70):
        c.backspace(); run(c.serialize(), surface(c.model))
    for cap in range(1, 11):
        for slot in range(cap):
            c = MixedReplay(cap); c.load(legacy[:cap])
            for _ in range(slot): c.move(1)
            for k in 'ㄱㅏㄴㅏ':
                c.press(k); run(c.serialize(), surface(c.model))
            c.move(-1); run(c.serialize(), surface(c.model))
            c.write_native(b'\xE4\xE5'); run(c.serialize(), surface(c.model))
            for _ in range(3): c.backspace(); run(c.serialize(), surface(c.model))
    c = MixedReplay(2); c.press('ㄱ'); c.move(-1)
    run(c.serialize(), surface(c.model), audit=True)
    empty = MixedReplay(1); raw = empty.serialize()
    for source_bytes in range(76):
        run(raw, None, False, source_bytes=source_bytes); counts['malformed'] += 1
    for output_bytes in range(24):
        run(raw, None, False, output_bytes=output_bytes); counts['malformed'] += 1
    for a in range(4):
        for b in range(4): run(raw, surface(empty.model), source=src + a, output=dest + b, audit=True)
    for delta in range(-23, 76):
        run(raw, None, False, output=src + delta); counts['malformed'] += 1
    run(raw, surface(empty.model), output=src - 24, audit=True)
    run(raw, surface(empty.model), output=src + 76, audit=True)
    # End-of-page input and output are consumed exactly, byte-aligned.
    run(raw, surface(empty.model), source=0x02000FB4, output=0x02001FE8, audit=True)
    run(raw, None, False, output=0xFFFFFFF0); counts['malformed'] += 1
    # Source overflow rejects before dereferencing the unmapped source argument.
    for source_argument in (0xFFFFFFFC, 0xFFFFFFB4):
        run(raw, None, False, source_argument=source_argument); counts['malformed'] += 1
    for offset, val in ((0, 0x10), (0, 0x1B), (0, 0x21), (1, 0xF2), (1, 0x10),
                        (2, 71), (5, 0), (23, 1), (75, 0xA0), (75, 0xB1)):
        bad = bytearray(base); bad[offset] = val
        run(bytes(bad), None, False); counts['malformed'] += 1
    for active in range(16):
        bad = bytearray(base); bad[1] = (active << 4) | 1
        valid = active in (0, 15)
        wanted = bytes([1, 1, 1, 0 if active == 0 else 255]) + struct.pack('<10H', 0, *([65535] * 9)) if valid else None
        run(bytes(bad), wanted, valid)
    for version in range(16):
        bad = bytearray(raw); bad[75] = version << 4
        run(bytes(bad), surface(empty.model) if version == 11 else None, version == 11)
    # All key positions / out-of-domain selectors and unused-bit positions.
    legal_prefix = [KEYS.index(k) for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10]
    for position in range(70):
        for key in range(40, 64):
            bad = raw_state(10, Snapshot((), 0, None), legal_prefix[:position] + [key])
            run(bad, None, False); counts['malformed'] += 1
        bad = bytearray(raw); bits = (11 << 420) | (1 << (position * 6)); bad[23:76] = bits.to_bytes(53, 'little')
        run(bytes(bad), None, False); counts['malformed'] += 1
    for cap in range(1, 11):
        # legal prefix followed by a capacity-overflow carry at the final slot.
        baseline = Snapshot(legacy[:cap], cap - 1, None)
        bad = raw_state(cap, baseline, [KEYS.index(k) for k in 'ㄱㅏㄴㅏ'])
        run(bad, None, False, audit=True); counts['malformed'] += 1
    names = ['hangul_mixed_replay_thumb.py', 'bench_hangul_mixed_replay_thumb.py',
             'hangul_mixed_replay_state.py', 'hangul_mixed_editor.py', 'hangul_keyboard_model.py',
             'hangul_composer_thumb.py', 'hangul_native_tokens.py']
    report = dict(id='exe45.hangul-keyboard.mixed-replay-cpu.v1', passed=True, counts=counts,
                  helper_bytes=len(blob), state_bytes=76, output_bytes=24, stack_bytes=68,
                  temporary_history_bytes=0, ISA=isa, rom_integrated=False,
                  full_compact_key_stream_validated=True, byte_alignment_supported=True,
                  output_format='count/cap/cursor/activeFF +10 LE words; NOT old pure-Hangul surface ABI',
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  dependency_reports={'cpu_composer': sha(old_path.read_bytes())},
                  host_dependency={'analysis/hangul_keyboard_v1/mixed_replay_host.json': sha(host_path.read_bytes())},
                  artifacts={'helper.bin': sha(blob)},
                  limits=['Synthetic standalone CPU execution, not ROM hooks or actual game memory/IRQ budget.',
                          'Caller supplies actual readable/writable extents, pinned table and stack disjointness.',
                          'Decoder returns editing partials, not committed record/glyph eligibility validation.',
                          'Mixed surface24 differs from pure display ABI; movement/write handlers and display/save consumers pending.'],
                  next='Connect compact edits and mixed display to decoded surface; replace native editor pointer/writer consumers together and verify stack/IRQ before ROM install.')
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS compact76 -> mixed surface24 CPU', counts, '; stack68, no588 history; ROM uninstalled')


if __name__ == '__main__': main()
