"""Explicit NEW cap10 detail-record -> calendar string pool, CPU only.

For native33C9A call r0=record body22/r1=pool0. No format detection.
Success resumes33C9E; rejected record skips heading via original33CB6 POP.
Own8+record decoder80=88; native detail caller adds20=108 fixture bytes.
Pool41 extent, source field22 and selected-format dispatch must be owned.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, lr}
ldr r2, extents
movs r3, #10
ldr r4, decoder
mov lr, pc
bx r4
cmp r0, #0
beq cd_abort
pop {r4, pc}
cd_abort:
pop {r4}
add sp, #4
ldr r3, continuation
bx r3
'''

def assemble(address=0x08307000):
    return assemble_verified(CODE,address,dict(extents=41<<16|22,decoder=0x08F09001,continuation=0x08033CB7))
