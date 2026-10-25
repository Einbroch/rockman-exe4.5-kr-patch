"""Mixed display conversion and native compact replay -> display CPU fixtures."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_mixed_display import CODE, display
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag


def surface(words, cursor=0, active=255, cap=10):
    return bytes([len(words), cap, cursor, active]) + struct.pack('<10H', *(tuple(words) + (65535,) * (10 - len(words))))


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'
    rp = root / 'cpu_mixed_replay/report.json'; replay = json.loads(rp.read_text(encoding='utf8'))
    if not replay['passed'] or replay['rom_integrated']: raise ValueError('replay scope')
    for n, h in replay['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    for n, h in replay['artifacts'].items(): require_hash(rp.parent / n, h)
    for p, h in replay['host_dependency'].items(): require_hash(ROOT / p, h)
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble_verified(CODE, 0x08001000, {})
    out = root / 'cpu_mixed_display'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob); blob = (out / 'helper.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 8192); u.mem_write(0x08001000, blob)
    u.mem_write(0x08000000, (rp.parent / 'helper.bin').read_bytes())
    u.mem_protect(0x08000000, 8192, UC_PROT_READ | UC_PROT_EXEC)
    pairs = (root / 'cpu_composer/transitions.bin').read_bytes()
    u.mem_map(0x09000000, (len(pairs) + 4095) & ~4095); u.mem_write(0x09000000, pairs)
    u.mem_protect(0x09000000, (len(pairs) + 4095) & ~4095, UC_PROT_READ)
    u.mem_map(0x02000000, 8192); u.mem_protect(0x02000000, 4096, UC_PROT_READ)
    u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    src, dest, decoded, sp, stop = 0x02000101, 0x02001503, 0x02001100, 0x03007F00, 0x0FF00000
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(display_calls=0, rejected=0, occupied_word_domain=0,
                  complete_syllable_slot_paths=0, partial_slot_mode_paths=0,
                  native_token_slot_paths=0, native_replay_display_paths=0)

    def call(pc, args, stack):
        u.mem_write(sp - stack - 4, b'\x5A' * (stack + 4))
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for r, v in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args): u.reg_write(r, v)
        for i, r in enumerate(regs): u.reg_write(r, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(pc | 1, stop, count=25000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(r) != 0x13579000 + i for i, r in enumerate(regs)): raise ValueError('ABI')
        if bytes(u.mem_read(sp - stack - 4, 4)) != b'\x5A' * 4: raise ValueError('stack boundary')
        return u.reg_read(UC_ARM_REG_R0)

    def convert(raw, mode=0, wanted=None, capacity=41, source=src, output=dest, initialized=False, pointer=None):
        if not initialized:
            u.mem_write(0x02000000, b'\xA7' * 8192); u.mem_write(source, raw)
        before = bytes(u.mem_read(0x02000000, 8192))
        expected_len = len(wanted) if wanted is not None and capacity >= len(wanted) else 0
        if call(0x08001000, [source if pointer is None else pointer, output, capacity, mode], 36) != expected_len: raise ValueError(f'display status mode={mode} raw={raw.hex()} wanted={wanted}')
        expected = bytearray(before)
        if expected_len: expected[output - 0x02000000:output - 0x02000000 + expected_len] = wanted
        if bytes(u.mem_read(0x02000000, 8192)) != bytes(expected): raise ValueError('display atomic/bounds/source')
        counts['display_calls'] += 1; counts['rejected'] += expected_len == 0

    print('mixed display occupied uint16 domain, both modes', flush=True)
    for word in range(65536):
        raw = surface([word], cap=1)
        for mode in (0, 1):
            if word < 11172: wanted = b'\xF9\xFC' + word.to_bytes(2, 'little') + b'\xE5'
            elif word < 11191: wanted = b'\xF9\xFC' + (word + 1).to_bytes(2, 'little') + b'\xE5' if mode == 0 else None
            elif 0x8000 <= word <= 0x80E3: wanted = bytes([word & 255, 229])
            elif 0x8100 <= word <= 0x81FF: wanted = bytes([228, word & 255, 229])
            else: wanted = None
            try: host = display(raw, mode)
            except ValueError: host = None
            if host != wanted: raise ValueError('host domain conversion')
            convert(raw, mode, wanted)
            counts['occupied_word_domain'] += 1
    legacy = [tag(b'\x9B')] * 10
    for slot in range(10):
        for rank in range(11172):
            words = legacy.copy(); words[slot] = rank
            raw = surface(words)
            wanted = b'\x9B' * slot + b'\xF9\xFC' + rank.to_bytes(2, 'little') + b'\x9B' * (9 - slot) + b'\xE5'
            convert(raw, 1, wanted); counts['complete_syllable_slot_paths'] += 1
        for rank in range(11172, 11191):
            words = legacy.copy(); words[slot] = rank
            raw = surface(words)  # sealed initial anywhere, not only active/tail
            wanted = b'\x9B' * slot + b'\xF9\xFC' + (rank + 1).to_bytes(2, 'little') + b'\x9B' * (9 - slot) + b'\xE5'
            convert(raw, 0, wanted); convert(raw, 1, None)
            counts['partial_slot_mode_paths'] += 2
        print('mixed display slot', slot + 1, '/10', flush=True)
    for token in [bytes([i]) for i in range(228)] + [bytes([228, i]) for i in range(256)]:
        for slot in range(10):
            words = legacy.copy(); words[slot] = tag(token)
            convert(surface(words), 0, b'\x9B' * slot + token + b'\x9B' * (9 - slot) + b'\xE5')
            counts['native_token_slot_paths'] += 1
    print('native compact replay -> mixed display final-slot repertoire', flush=True)
    for l in INITIALS:
        for v in MEDIALS:
            for t in FINALS:
                c = MixedReplay(10); c.load(legacy)
                for _ in range(9): c.move(1)
                for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))): c.press(k)
                u.mem_write(0x02000000, b'\xA7' * 8192); u.mem_write(src, c.serialize())
                before = bytearray(u.mem_read(0x02000000, 8192))
                if call(0x08000000, [src, decoded, 76 | 24 << 16, 0x09000000], 68) != 1: raise ValueError('native replay integration')
                expected_surface = surface(c.model.state.cells, c.model.state.cursor, c.model.state.active, 10)
                before[decoded - 0x02000000:decoded - 0x02000000 + 24] = expected_surface
                if bytes(u.mem_read(0x02000000, 8192)) != bytes(before): raise ValueError('actual replay output')
                # Feed actual CPU output into second CPU helper, no host writes.
                convert(expected_surface, 1, display(expected_surface, 1), source=decoded, initialized=True)
                counts['native_replay_display_paths'] += 1
    empty = surface([], cap=1); convert(empty, 0, b'\xE5'); convert(empty, 1, None)
    maximum = surface([11171] * 10, cursor=10, active=9)
    for capacity in range(42): convert(maximum, 1, display(maximum, 1), capacity=capacity)
    for slot in range(10):
        words = legacy.copy(); words[slot] = 0
        raw = surface(words)
        for mode in (2, 255, 0xFFFFFFFF): convert(raw, mode, None)
    for offset, value in ((0, 11), (1, 0), (1, 11), (2, 11), (3, 10), (3, 0)):
        raw = bytearray(surface(legacy)); raw[offset] = value
        convert(bytes(raw), 0, None)
    raw = bytearray(surface([0], cap=1)); raw[6] = 0
    convert(bytes(raw), 0, None)
    for a in range(4):
        for b in range(4): convert(maximum, 0, display(maximum), source=src + a, output=dest + b)
    convert(maximum, 0, None, output=0xFFFFFFF0)
    convert(maximum, 0, None, pointer=0xFFFFFFFC)
    for delta in range(-40, 24): convert(maximum, 0, None, output=src + delta)
    names = ['hangul_mixed_display.py', 'bench_hangul_mixed_display.py', 'hangul_mixed_replay_state.py',
             'hangul_mixed_editor.py', 'hangul_native_tokens.py', 'hangul_editor_display.py', 'hangul_composer_thumb.py']
    report = dict(id='exe45.hangul-keyboard.mixed-display-cpu.v1', passed=True, counts=counts,
                  helper_bytes=len(blob), surface_bytes=24, max_output_bytes=41, stack_bytes=36,
                  ISA=isa, rom_integrated=False, partial_anywhere_edit_preserved=True,
                  partial_anywhere_commit_rejected=True, native_token_bytes_preserved=True,
                  native_replay_display_paths=11172,
                  dependencies={'cpu_mixed_replay': sha(rp.read_bytes())},
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names},
                  artifacts={'helper.bin': sha(blob)},
                  limits=['CPU fixtures only; no game cache/descriptor/cursor wiring, hooks or actual jamo screen evidence.',
                          '484 structural native tokens are not proof of glyph membership or safe raw save commit.',
                          'Payload98/E5 bytes are preserved in display; original byte-scanning writer is still unsafe for committed mixed records.',
                          'No game memory ownership/IRQ budget or persistence/save compatibility claim.'],
                  next='Implement compact edit handlers and coordinated native editor/cache/destination replacements; separate committed record serialization and verify game runtime/save/fresh-load.')
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS mixed display CPU', counts, '; native replay connected, ROM uninstalled')


if __name__ == '__main__': main()
