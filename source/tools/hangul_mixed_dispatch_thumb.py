"""Native edit command dispatcher fixture, no ROM placement adopted.

r0 compact76,r1 jamo0..39/B40/left41/right42/native opaque word,
r2 available,r3 aligned context16: transition, deletion, keyedit Thumb entry,
rebase Thumb entry. Caller pins context and verified helpers. Temporary4-byte
push is released before tail call; peak with helpers remains196, not200.
Malformed original states are validated by the selected helper before writes.
"""
from extended_dialogue import assemble_verified

CODE = '''cmp r2, #76
blo dispatch_reject
push {r0}
adds r0, #76
ldr r0, [sp]
bcs dispatch_wrap
cmp r1, #40
blo dispatch_key
bhi dispatch_rebase
ldrb r1, [r0, #2]
cmp r1, #0
beq dispatch_canonical
movs r1, #40
b dispatch_key
dispatch_canonical:
movs r1, #43
dispatch_rebase:
ldr r0, [r3, #12]
mov r12, r0
pop {r0}
bx r12
dispatch_key:
ldr r0, [r3, #8]
mov r12, r0
pop {r0}
ldr r3, [r3]
bx r12
dispatch_wrap:
pop {r0}
dispatch_reject:
movs r0, #0
bx lr
'''


def assemble(address=0x08000000):
    return assemble_verified(CODE, address, {})
