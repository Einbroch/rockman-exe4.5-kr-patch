"""Atomic compact76 accepted-key edit candidate, NOT a complete B handler.

r0 in-place compact76, r1 key0..39 or history-pop40, r2 available,
r3 pinned replay transition table. Return1/0; byte alignment, r4..r11/SP
preserved. Own stack128 plus nested decoder68 =196 bytes, no588 history.
Validate original before mutation, then proposed replay before copying back.
B with no accepted-key history returns0; caller must implement canonical B
separately. This is not a game hook, RAM/IRQ budget or save integration.
"""
from hangul_mixed_replay_thumb import CODE as REPLAY

CODE = '''push {r4, r5, r6, r7, lr}
sub sp, #108
movs r4, r0
movs r5, r3
movs r6, r1
cmp r2, #76
blo edit_reject
cmp r6, #40
bhi edit_reject
adds r0, #76
cmp r0, r4
blo edit_reject
mov r7, sp
movs r0, #0
edit_copy_in:
ldrb r1, [r4, r0]
strb r1, [r7, r0]
adds r0, #1
cmp r0, #76
blo edit_copy_in
movs r0, r7
movs r1, r7
adds r1, #76
movs r2, #24
lsls r2, r2, #16
adds r2, #76
movs r3, r5
bl edit_decode
cmp r0, #1
bne edit_reject
ldrb r0, [r7, #2]
cmp r6, #40
beq edit_pop
cmp r0, #70
bhs edit_reject
adds r1, r0, #1
strb r1, [r7, #2]
b edit_pack
edit_pop:
cmp r0, #0
beq edit_reject
subs r0, #1
strb r0, [r7, #2]
edit_pack:
movs r1, #6
muls r0, r1, r0
movs r3, #7
ands r3, r0
lsrs r0, r0, #3
adds r0, #23
ldrb r1, [r7, r0]
adds r2, r0, #1
ldrb r2, [r7, r2]
lsls r2, r2, #8
orrs r1, r2
movs r2, #63
lsls r2, r3
bics r1, r2
cmp r6, #40
beq edit_store
lsls r6, r3
orrs r1, r6
edit_store:
strb r1, [r7, r0]
adds r0, #1
lsrs r1, r1, #8
strb r1, [r7, r0]
movs r0, r7
movs r1, r7
adds r1, #76
movs r2, #24
lsls r2, r2, #16
adds r2, #76
movs r3, r5
bl edit_decode
cmp r0, #1
bne edit_reject
movs r0, #0
edit_copy_out:
ldrb r1, [r7, r0]
strb r1, [r4, r0]
adds r0, #1
cmp r0, #76
blo edit_copy_out
movs r0, #1
b edit_return
edit_reject:
movs r0, #0
edit_return:
add sp, #108
pop {r4, r5, r6, r7, pc}
edit_decode:
''' + REPLAY


def assemble(address=0x08001000, code=CODE):
    # Match existing BL-capable compact wrappers, not the dialogue verifier
    # whose contract intentionally permits only two-byte instructions.
    from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB, KS_VERSION, CS_VERSION
    if (KS_VERSION, CS_VERSION) != ('0.9.2', '5.0.7'):
        raise ValueError('toolchain drift')
    header = '.syntax unified\n.cpu arm7tdmi\n.thumb\n'
    source = [s for s in code.splitlines() if s and not s.endswith(':')]
    size = sum(4 if s.startswith('bl ') else 2 for s in source)
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    blob = bytes(ks.asm(header + code, address)[0])
    ins = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(blob, address))
    if len(blob) != size or len(ins) != len(source):
        raise ValueError('instruction extent')
    boundaries = {i.address for i in ins}
    for i, s in zip(ins, source):
        if i.size != (4 if s.startswith('bl ') else 2):
            raise ValueError('unexpected wide opcode')
        if i.size == 4:
            lo = int.from_bytes(i.bytes[:2], 'little'); hi = int.from_bytes(i.bytes[2:], 'little')
            if i.mnemonic != 'bl' or lo & 0xF800 != 0xF000 or hi & 0xF800 != 0xF800:
                raise ValueError('not ARMv4T BL')
        if bytes(ks.asm(header + i.mnemonic + ' ' + i.op_str, i.address)[0]) != i.bytes:
            raise ValueError('placement roundtrip')
        if s.split()[0] in {'b', 'bl', 'beq', 'bne', 'bhs', 'blo', 'bhi', 'bls'}:
            if int(i.op_str.lstrip('#'), 0) not in boundaries:
                raise ValueError('branch target boundary')
    return blob, dict(isa='ARMv4T Thumb-1 including BL; no BLX/Thumb-2',
                      assembler=KS_VERSION, disassembler=CS_VERSION, address=address,
                      code_bytes=size, final_placement_roundtrip=True,
                      instructions=[dict(address=i.address, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str) for i in ins])
