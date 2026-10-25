"""Caller-selected mixed fixed record -> compact76. No automatic detection.

r0 record,r1 output76,r2 inputAvailable low16|outputAvailable high16,
r3 capacity1..10. Returns1/0, rejects partial/empty/malformed without external
writes. Byte alignment, r4..r11/SP preserved; own88+nested36=124 stack.
Caller owns disjoint record/output/stack. Not game/save integration.
"""
from hangul_mixed_display import CODE as DISPLAY
from hangul_mixed_cache_bridge import scoped
from hangul_mixed_keyedit_thumb import assemble as assemble_code

CODE='''push {r4, r5, r6, r7, lr}
sub sp, #68
movs r4, r0
movs r5, r1
movs r6, r3
cmp r6, #1
blo ri_early_fail
cmp r6, #10
bhi ri_early_fail
lsrs r0, r2, #16
cmp r0, #76
blo ri_early_fail
lsls r0, r2, #16
lsrs r0, r0, #16
lsls r1, r6, #1
adds r1, #2
cmp r0, r1
blo ri_early_fail
adds r0, r4, r1
cmp r0, r4
blo ri_early_fail
movs r2, r5
adds r2, #76
cmp r2, r5
blo ri_early_fail
cmp r4, r2
bhs ri_disjoint
cmp r5, r0
blo ri_early_fail
ri_disjoint:
ldrb r7, [r4]
subs r7, #128
cmp r7, #1
blo ri_early_fail
cmp r7, r6
bhi ri_early_fail
subs r1, #1
ldrb r0, [r4, r1]
cmp r0, #229
bne ri_early_fail
mov r3, sp
strb r7, [r3]
strb r6, [r3, #1]
movs r0, #0
strb r0, [r3, #2]
movs r0, #255
strb r0, [r3, #3]
movs r1, #4
ri_pad:
strb r0, [r3, r1]
adds r1, #1
cmp r1, #24
blo ri_pad
lsls r2, r6, #1
movs r1, #0
ri_words:
adds r0, r1, #1
ldrb r0, [r4, r0]
adds r1, #4
strb r0, [r3, r1]
subs r1, #3
cmp r1, r2
blo ri_words
b ri_validate
ri_early_fail:
b ri_fail
ri_validate:
mov r0, sp
add r1, sp, #24
movs r2, #41
movs r3, #1
bl ri_display
cmp r0, #0
beq ri_fail
movs r0, #0
movs r1, #0
ri_clear:
strb r1, [r5, r0]
adds r0, #1
cmp r0, #76
blo ri_clear
lsls r0, r7, #4
orrs r0, r6
strb r0, [r5]
movs r0, #240
strb r0, [r5, #1]
movs r0, #75
movs r1, #176
strb r1, [r5, r0]
mov r3, sp
movs r2, #0
ri_copy:
adds r0, r2, #4
ldrb r1, [r3, r0]
subs r0, #1
strb r1, [r5, r0]
adds r2, #1
cmp r2, #20
blo ri_copy
movs r0, #1
b ri_return
ri_fail:
movs r0, #0
ri_return:
add sp, #68
pop {r4, r5, r6, r7, pc}
ri_display:
'''+scoped(DISPLAY,'ri_d_')

def assemble(address=0x08F05000):
    return assemble_code(address,CODE)
