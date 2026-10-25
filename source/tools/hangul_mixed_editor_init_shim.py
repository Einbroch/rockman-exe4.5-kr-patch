"""Original initializer argument/live-out ABI bridge, CPU candidate only.

r0 capacityFlag, r1 heading, r2 opaque destination, r3 callerValue.
Accepts only 1..10 and 129..138. Success preserves original r0..r3/NZCV
for this domain; r2=editor+32 is an ABI compatibility value, NOT a valid
legacy word-buffer pointer in the new layout. Unsupported capacity returns
r0=0 without changing editor96. No caller currently handles that failure.
Must replace every old pointer consumer atomically before a real hook.
Own stack24 + nested staging116 =140, not a measured game/IRQ budget.
Caller must own editor96, code entry, and disjoint stack throughout call.
"""
from extended_dialogue import assemble_verified


CODE='''push {r4, lr}
push {r0, r1, r2, r3}
mov r0, sp
ldr r1, editor
ldr r2, extents
movs r3, #0
ldr r4, helper
mov lr, pc
bx r4
cmp r0, #0
beq shim_fail
pop {r0, r1, r2, r3}
movs r1, #0
cmp r0, #128
blt shim_liveout
movs r1, #1
shim_liveout:
movs r0, #1
ldr r2, editor
adds r2, #32
pop {r4, pc}
shim_fail:
add sp, #16
movs r0, #0
pop {r4, pc}
'''


def assemble(address=0x08801000, editor=0x0200FC40, helper=0x08800001):
    if editor % 4 or not 0x02000000 <= editor <= 0x0203FFA0:
        raise ValueError('caller-owned aligned editor96 EWRAM candidate')
    if not helper & 1 or not 0x08000000 <= helper < 0x0A000000:
        raise ValueError('Thumb ROM helper entry')
    return assemble_verified(CODE,address,dict(editor=editor,extents=96<<16|16,helper=helper))
