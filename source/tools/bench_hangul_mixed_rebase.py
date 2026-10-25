"""Execute compact cursor/native/canonical-B plus prior keyedit fixtures."""
import json
import random
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_mixed_rebase_thumb import assemble
from hangul_mixed_replay_state import MixedReplay, KEYS, apply
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag, untag
from hangul_mixed_dispatch_thumb import assemble as assemble_dispatch


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'
    deps = {}
    for name in ('cpu_mixed_replay', 'cpu_mixed_keyedit', 'cpu_composer'):
        p = root / name / 'report.json'; r = json.loads(p.read_text(encoding='utf8'))
        if not r['passed'] or r.get('rom_integrated', False): raise ValueError('dependency scope')
        for n, h in r['tools'].items(): require_hash(ROOT / 'tools' / n, h)
        for n, h in r['artifacts'].items(): require_hash(p.parent / n, h)
        deps[name] = sha(p.read_bytes())
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble(); out = root / 'cpu_mixed_rebase'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob); blob = (out / 'helper.bin').read_bytes()
    dispatch, dispatch_isa = assemble_dispatch()
    (out / 'dispatch.bin').write_bytes(dispatch); dispatch = (out / 'dispatch.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, 16384)
    u.mem_write(0x08000000, dispatch)
    u.mem_write(0x08003000, blob)
    u.mem_write(0x08001000, (root / 'cpu_mixed_keyedit/helper.bin').read_bytes())
    u.mem_protect(0x08000000, 16384, UC_PROT_READ | UC_PROT_EXEC)
    for address, name in ((0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')):
        data = (root / 'cpu_composer' / name).read_bytes()
        u.mem_map(address, (len(data) + 4095) & ~4095); u.mem_write(address, data)
        u.mem_protect(address, (len(data) + 4095) & ~4095, UC_PROT_READ)
    u.mem_map(0x09300000, 4096); u.mem_write(0x09300000, struct.pack('<IIII', 0x09000000, 0x09200000, 0x08001001, 0x08003001))
    u.mem_protect(0x09300000, 4096, UC_PROT_READ)
    u.mem_map(0x02000000, 8192); u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    src, sp, stop = 0x02000101, 0x03007F00, 0x0FF00000
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(rebase_calls=0, keyedit_calls=0, rejected=0, canonical_word_slot_paths=0,
                  action_uint16_domain=0, native_capacity_cursor_paths=0, movement_paths=0,
                  uninterrupted_mixed_actions=0, malformed=0, native_dispatch_calls=0)

    def oracle(raw, action, keyedit=False):
        try:
            c = MixedReplay.restore(raw)
            if keyedit:
                return apply(raw, 'backspace') if action == 40 and c.keys else apply(raw, 'jamo', KEYS[action]) if 0 <= action < 40 else (False, raw)
            if action in (41, 42): return apply(raw, 'move', -1 if action == 41 else 1)
            if action == 43: return (False, raw) if c.keys else apply(raw, 'backspace')
            return apply(raw, 'native', untag(action))
        except ValueError:
            return False, raw

    def execute(raw, action, keyedit=False, capacity=76, source=src, initialized=False, pointer=None, native_dispatch=False):
        oracle_action = action
        if native_dispatch:
            keyedit = action < 40 or action == 40 and bool(raw[2])
            if action == 40 and not keyedit: oracle_action = 43
        accepted, wanted = oracle(raw, oracle_action, keyedit)
        if capacity < 76 or pointer is not None: accepted, wanted = False, raw
        if not initialized:
            u.mem_write(0x02000000, b'\xA7' * 8192); u.mem_write(source, raw)
        elif bytes(u.mem_read(source, 76)) != raw: raise ValueError('uninterrupted state drift')
        before = bytearray(u.mem_read(0x02000000, 8192))
        u.mem_write(sp - 200, b'\x5A' * 200); u.reg_write(UC_ARM_REG_CPSR, 0x30)
        args = [source if pointer is None else pointer, action, capacity, 0x09000000 if keyedit and not native_dispatch else 0x09300000]
        for reg, value in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args): u.reg_write(reg, value)
        for i, reg in enumerate(regs): u.reg_write(reg, 0x13579000 + i)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(0x08000001 if native_dispatch else 0x08001001 if keyedit else 0x08003001, stop, count=30000)
        if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(UC_ARM_REG_R0) != int(accepted) or u.reg_read(UC_ARM_REG_SP) != sp or any(u.reg_read(reg) != 0x13579000 + i for i, reg in enumerate(regs)): raise ValueError(f'ABI/status action={action} raw={raw.hex()}')
        if bytes(u.mem_read(sp - 200, 4)) != b'\x5A' * 4: raise ValueError('stack196')
        before[source - 0x02000000:source - 0x02000000 + 76] = wanted
        if bytes(u.mem_read(0x02000000, 8192)) != bytes(before): raise ValueError(f'atomic compact action={action} raw={raw.hex()} wanted={wanted.hex()}')
        counts['keyedit_calls' if keyedit else 'rebase_calls'] += 1; counts['rejected'] += not accepted
        counts['native_dispatch_calls'] += native_dispatch
        return wanted

    legacy = tuple(tag(b'\xE4\xE5') for _ in range(10))
    print('canonical B all11191 complete/partial words in every slot', flush=True)
    for slot in range(10):
        for word in range(11191):
            c = MixedReplay(10); cells = list(legacy); cells[slot] = word
            c.model.state = Snapshot(tuple(cells), slot + 1, None); c._rebase()
            execute(c.serialize(), 43); counts['canonical_word_slot_paths'] += 1
        print('canonical slot', slot + 1, flush=True)
    print('all65536 uint16 actions (484native+3commands)', flush=True)
    c = MixedReplay(2); c.load(legacy[:2]); raw = c.serialize()
    for action in range(65536): execute(raw, action); counts['action_uint16_domain'] += 1
    tokens = [tag(bytes([i])) for i in range(228)] + [tag(bytes([228, i])) for i in range(256)]
    for cap in range(1, 11):
        for cursor in range(cap + 1):
            c = MixedReplay(cap); c.load(legacy[:cap]); c.model.state = Snapshot(legacy[:cap], cursor, None); c._rebase()
            raw = c.serialize()
            for action in tokens: execute(raw, action); counts['native_capacity_cursor_paths'] += 1
            execute(raw, 43)  # native delete before cursor; cursor0 first
            for action in (41, 42): execute(raw, action); counts['movement_paths'] += 1
    # Movement must preserve partials and rebase nonempty histories, not restore
    # an overwritten native cell later via an obsolete accepted-key undo.
    c = MixedReplay(10); c.load(legacy)
    for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10:
        c.press(k); raw = c.serialize()
        for action in (41, 42, 43, tokens[0], tokens[-1]): execute(raw, action)
    for cap in range(1, 11):
        c = MixedReplay(cap)
        execute(c.serialize(), 43)
        for k in 'ㄱㅏㄴ': c.press(k)
        raw = c.serialize(); moved = execute(raw, 41)
        execute(moved, 43); execute(moved, 0, keyedit=True)
    rng = random.Random(7646)
    for cap in range(1, 11):
        c = MixedReplay(cap); c.load(legacy[:cap]); raw = c.serialize()
        for step in range(500):
            kind = rng.randrange(4)
            if kind == 0: action, keyedit = rng.randrange(40), True
            elif kind == 1: action, keyedit = rng.choice((41, 42)), False
            elif kind == 2: action, keyedit = rng.choice(tokens), False
            else:
                keyedit = False; action = 40
            raw = execute(raw, action, keyedit, initialized=step > 0, native_dispatch=True)
            counts['uninterrupted_mixed_actions'] += 1
    base = MixedReplay(1).serialize()
    for alignment in range(4): execute(base, tokens[0], source=src + alignment)
    for capacity in (0, 1, 75): execute(base, 42, capacity=capacity)
    execute(base, 41, pointer=0xFFFFFFF0)
    for capacity in (0, 75): execute(base, 40, capacity=capacity, native_dispatch=True)
    execute(base, 40, pointer=0xFFFFFFF0, native_dispatch=True)
    for action in (0x10000, 0xFFFFFFFF): execute(base, action)
    for offset, value in ((0, 0), (0, 11), (1, 0x10), (2, 71), (3, 0), (23, 1), (75, 0xA0), (75, 0xB1)):
        bad = bytearray(base); bad[offset] = value
        for action in (41, 42, 43, tokens[0]): execute(bytes(bad), action); counts['malformed'] += 1
        execute(bytes(bad), 40, native_dispatch=True); counts['malformed'] += 1
    c = MixedReplay(1); c.press('ㄱ'); good = c.serialize()
    for key in range(40, 64):
        bad = bytearray(good); bad[23] = key
        for action in (41, 42, 43, tokens[-1]): execute(bytes(bad), action); counts['malformed'] += 1
        execute(bytes(bad), 40, native_dispatch=True); counts['malformed'] += 1
    names = ['hangul_mixed_rebase_thumb.py', 'bench_hangul_mixed_rebase.py', 'hangul_mixed_keyedit_thumb.py',
             'hangul_mixed_replay_thumb.py', 'hangul_mixed_replay_state.py', 'hangul_mixed_editor.py',
             'hangul_native_tokens.py', 'hangul_composer_thumb.py', 'extended_dialogue.py', 'hangul_mixed_dispatch_thumb.py']
    report = dict(id='exe45.hangul-keyboard.mixed-rebase-cpu.v1', passed=True, counts=counts,
                  helper_bytes=len(blob), state_bytes=76, own_stack_bytes=128, nested_stack_bytes=196,
                  temporary_history_bytes=0, canonical_delete_no_history_only=True,
                  sealed_partials_preserved=True, native_overwrite_not_insert=True,
                  rom_integrated=False, ISA=isa, dispatch_ISA=dispatch_isa, dispatch_bytes=len(dispatch), dependencies=deps,
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in names}, artifacts={'helper.bin': sha(blob), 'dispatch.bin': sha(dispatch)},
                  limits=['484 structural native tokens are not glyph/input membership or raw-save eligibility.',
                          'Complete editing command connection is CPU fixture only, not game UI integration.',
                          'Context/table/stack extents and residency are caller obligations; game IRQ budget unresolved.',
                          'Initializer/import, actual cursor/cache/destination consumers, commit/save/fresh-load remain pending.'])
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    print('PASS compact rebase CPU', counts, flush=True)


if __name__ == '__main__': main()
