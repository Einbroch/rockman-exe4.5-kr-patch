"""Conditional version-aware adapters for native calendar prefill copies.

CPU candidate only: not adopted ROM placement or full save ABI. The native
33334 caller/getter/default copies remain executed. Source must be a record
body in the 255-record arena, destination one of its three 128-byte pool slots.
Reader validates before writing; failure skips remaining native prefill calls
through its existing POP. Earlier valid/default slots are not rolled back.
No error feedback, editor initialization, or whole-consumer coverage claim.
"""
from extended_dialogue import assemble_verified

CODE = '''push {r4, lr}
ldr r4, arena_body
cmp r0, r4
blo pf_fail
subs r4, r0, r4
movs r2, #31
tst r4, r2
bne pf_fail
ldr r2, arena_bytes
cmp r4, r2
bhs pf_fail
ldr r4, pool
cmp r1, r4
beq pf_read
adds r4, #128
cmp r1, r4
beq pf_read
adds r4, #128
cmp r1, r4
bne pf_fail
pf_read:
ldr r2, extents
movs r3, #10
ldr r4, reader
mov lr, pc
bx r4
cmp r0, #0
beq pf_fail
pop {r4, pc}
pf_fail:
pop {r4}
add sp, #4
ldr r3, abort
bx r3
'''


def assemble(address=0x0830E000):
    return assemble_verified(CODE, address, dict(
        arena_body=0x020011FA, arena_bytes=255*32,
        pool=0x02026080, extents=41<<16|22,
        reader=0x0830D201, abort=0x08033373))
