"""Keylog64 replay candidate, not a ROM hook or allocated game memory.

r0 keylog64, r1 immutable baseline24, r2 key0..39/B40/check41,
r3 trusted descriptor16 (feed, undo, transitions, deletions).
Aligned valid nonoverlapping state/baseline regions required. Atomic reject.
Temporary backend304 + proposal64 + locals24 + saved20 =412 stack;
backend calls add shim8+52 =472 maximum. No reconstructed ranks returned.
"""
from hangul_compact_thumb import program as old_program
from hangul_extended_composer_thumb import replace_once


def program():
    s = old_program()
    # Retain control flow while changing the explicitly checked ABI/layout.
    for old, new in [('sub sp, #364', 'sub sp, #392'), ('add sp, #364', 'add sp, #392'),
                     ('#340', '#368'), ('#344', '#372'), ('#348', '#376'),
                     ('#352', '#380'), ('#356', '#384'), ('#360', '#388'),
                     ('#276', '#304'), ('#56', '#70')]:
        if old not in s:
            raise ValueError('keylog layout applicability')
        s = s.replace(old, new)
    s = replace_once(s, 'adds r5, #20', 'adds r5, #24')
    s = replace_once(s, 'cmp r4, #8', 'cmp r4, #10')
    s = replace_once(s, 'cmp r6, #8', 'cmp r6, #10')
    s = replace_once(s, 'movs r2, #5\ncopy_baseline:', 'movs r2, #6\ncopy_baseline:')
    s = replace_once(s, 'movs r2, #64\nclear_history:', 'movs r2, #70\nclear_history:')
    s = s.replace('adds r0, #20', 'adds r0, #4')  # get_key/put_key packed stream
    s = s.replace('movs r3, #69', 'movs r3, #76').replace('movs r1, #69', 'movs r1, #76')
    # Every initial guard before the common failure branch uses far-safe guards.
    def guards(checks):
        out = []
        for i, (code, condition) in enumerate(checks):
            inverse = {'ne': 'eq', 'hi': 'ls'}[condition]
            out.append(f'{code}\nb{inverse} keylog_guard_{i}\nb fail\nkeylog_guard_{i}:')
        return '\n'.join(out) + '\n'
    start = s.index('adds r0, #62\nldrb r5, [r0]')
    end = s.index('ldrb r5, [r1, #1]', start)
    s = s[:start] + guards([
        ('ldrb r5, [r0, #3]\ncmp r5, #70', 'hi'),
        ('ldrb r5, [r0]\ncmp r5, #161', 'ne'),
        ('movs r6, r0\nadds r6, #56\nldrb r5, [r6]\nmovs r7, #240\ntst r5, r7', 'ne'),
        ('movs r7, #7\nreserved_loop:\nadds r6, #1\nldrb r5, [r6]\ncmp r5, #0', 'ne'),
    ]) + 'subs r7, #1\nbne reserved_loop\n' + s[end:]
    s = replace_once(s, 'adds r0, #62\nldrb r0, [r0]', 'ldrb r0, [r0, #3]')
    # No cached ranks in keylog: replay itself is validation.
    start = s.index('mov r0, sp\nldr r1, [sp, #368]\nmovs r2, #5\ncompare_header:')
    end = s.index('ldr r0, [sp, #376]', start)
    s = s[:start] + s[end:]
    s = replace_once(s, 'ldr r2, [sp, #376]\nbl put_key\nb finish_header',
                     'ldr r2, [sp, #376]\nbl put_key\nadd r0, sp, #304\nldrb r1, [r0, #2]\nadds r1, #1\nstrb r1, [r0, #2]\nb finish_header')
    s = replace_once(s, 'bl put_key\nb finish_header\nback_baseline:',
                     'bl put_key\nadd r0, sp, #304\nldrb r1, [r0, #2]\nsubs r1, #1\nstrb r1, [r0, #2]\nb finish_header\nback_baseline:')
    s = replace_once(s, 'adds r0, #62\nldrb r1, [r0]', 'adds r0, #3\nldrb r1, [r0]')
    start = s.index('finish_header:\nmov r0, sp')
    end = s.index('add r0, sp, #304\nldr r1, [sp, #368]', start)
    s = s[:start] + 'finish_header:\n' + s[end:]
    return s


CODE = program()


def assemble(address=0x08002000):
    from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB, KS_VERSION, CS_VERSION
    if (KS_VERSION, CS_VERSION) != ('0.9.2', '5.0.7'):
        raise ValueError('toolchain drift')
    header = '.syntax unified\n.cpu arm7tdmi\n.thumb\n'
    source = [s for s in CODE.splitlines() if s and not s.endswith(':')]
    size = sum(4 if s.startswith('bl ') else 2 for s in source)
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    blob = bytes(ks.asm(header + CODE, address)[0])
    ins = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(blob, address))
    if len(blob) != size or len(ins) != len(source):
        raise ValueError('instruction extent')
    for i, s in zip(ins, source):
        if i.size != (4 if s.startswith('bl ') else 2):
            raise ValueError('unexpected wide opcode')
        if i.size == 4:
            lo = int.from_bytes(i.bytes[:2], 'little'); hi = int.from_bytes(i.bytes[2:], 'little')
            if i.mnemonic != 'bl' or lo & 0xf800 != 0xf000 or hi & 0xf800 != 0xf800:
                raise ValueError('not ARMv4T BL')
        if bytes(ks.asm(header + i.mnemonic + ' ' + i.op_str, i.address)[0]) != i.bytes:
            raise ValueError('placement roundtrip')
        if s.split()[0] in {'b', 'bl', 'beq', 'bne', 'bhs', 'blo', 'bhi', 'bls'}:
            target = int(i.op_str.lstrip('#'), 0)
            if not address <= target < address + size or target % 2:
                raise ValueError('branch target')
    return blob, dict(isa='ARMv4T Thumb-1 including BL; no BLX/Thumb-2',
                      assembler=KS_VERSION, disassembler=CS_VERSION, address=address,
                      code_bytes=size, final_placement_roundtrip=True,
                      instructions=[dict(address=i.address, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str) for i in ins])
