"""Read-only keylog replay -> ten-cell display bridge, not ROM hook.

r0 keylog64, r1 immutable baseline24, r2 caller-owned output,
r3 trusted aligned descriptor28: feed/undo/transition/delete/display pointers,
output capacity, mode0 edit/1 commit. All fields LE uint32.
Output must be disjoint from state64/baseline24/descriptor28 over maximum41
bytes, and caller must keep it outside this function's stack workspace.
Return output byte count1..41 or0 with no output/state writes on reject.
Replay workspace348 + shim8/backend52 =408 maximum stack; the edit-only
wrapper's proposal64 is unnecessary on this read-only path.
"""
from hangul_keylog_thumb import CODE as REPLAY
from hangul_extended_composer_thumb import replace_once


def program():
    s = replace_once(REPLAY, 'sub sp, #392\nstr r0',
                     'sub sp, #392\nstr r2, [sp, #388]\nmovs r2, #41\nstr r0')
    start = s.index('ldr r0, [sp, #376]\ncmp r0, #41')
    end = s.index('fail:\n', start)
    checks = '''ldr r4, [sp, #388]
movs r5, r4
adds r5, #41
bcs fail
ldr r6, [sp, #368]
movs r7, r6
adds r7, #64
cmp r4, r7
bhs output_base
cmp r5, r6
bls output_base
b fail
output_base:
ldr r6, [sp, #372]
movs r7, r6
adds r7, #24
cmp r4, r7
bhs output_descriptor
cmp r5, r6
bls output_descriptor
b fail
output_descriptor:
ldr r6, [sp, #380]
movs r7, r6
adds r7, #28
bcs fail
cmp r4, r7
bhs output_ready
cmp r5, r6
bls output_ready
b fail
output_ready:
ldr r7, [r6, #16]
ldr r2, [r6, #20]
ldr r3, [r6, #24]
mov r0, sp
movs r1, r4
bl call_reg
b return
'''
    s = s[:start] + checks + s[end:]
    s = s[:s.index('put_key:')]
    # No proposal is committed here, so reclaim its64 bytes instead of carrying
    # the edit wrapper's temporary allocation into every display invocation.
    for old, new in [('#392', '#328'), ('#368', '#304'), ('#372', '#308'),
                     ('#376', '#312'), ('#380', '#316'), ('#384', '#320'), ('#388', '#324')]:
        if old not in s:
            raise ValueError('read-only workspace applicability')
        s = s.replace(old, new)
    return s


CODE = program()


def assemble(address=0x08006000):
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
        if s.split()[0] in {'b', 'bl', 'beq', 'bne', 'bhs', 'blo', 'bhi', 'bls', 'bcs'}:
            target = int(i.op_str.lstrip('#'), 0)
            if not address <= target < address + size or target % 2:
                raise ValueError('branch target')
    return blob, dict(isa='ARMv4T Thumb-1 including BL; no BLX/Thumb-2',
                      assembler=KS_VERSION, disassembler=CS_VERSION, address=address,
                      code_bytes=size, final_placement_roundtrip=True,
                      instructions=[dict(address=i.address, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str) for i in ins])
