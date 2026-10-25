"""Caller-selected descriptor16 record -> native dialogue cache candidate.

Only source020010A7/bound9/LR08051805 selects new cap4 record at source-1.
Caller MUST already establish mixed format and own disjoint128byte output.
Other calls tail-enter original memcpy. Invalid selected record emits emptyE5
for memory safety, not adopted UX. No format detection or ROM installation.
Own12+record display80=92 stack; original handler12 adds up to104.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4}
ldr r3, selected_source
cmp r0, r3
bne legacy
cmp r2, #9
bne legacy
ldr r3, selected_return
cmp lr, r3
bne legacy
push {r5, lr}
movs r5, r1
subs r0, #1
movs r2, #128
lsls r2, r2, #16
adds r2, #10
movs r3, #4
ldr r4, record_display
mov lr, pc
bx r4
cmp r0, #0
bne finish
movs r1, #229
strb r1, [r5]
finish:
pop {r5}
pop {r3}
mov lr, r3
pop {r4}
mov pc, lr
legacy:
ldr r3, original_copy
pop {r4}
bx r3'''

def assemble(address=0x08300000):
    return assemble_verified(CODE,address,dict(selected_source=0x020010A7,
        selected_return=0x08051805,record_display=0x08F09001,original_copy=0x0800094D))
