"""Trusted-canonical mixed jamo feed kernel; no game hook or RAM allocation.

r0 aligned588-byte state, r1 key0..39, r2 pinned transition table1790720 bytes,
r3 available bytes. Return1/0, r4..r11/SP preserved; stack52 bytes.
Same caller/history/table/stack preconditions as mixed undo. Structural current
surface checks do NOT validate the historical forward-transition chain.
At most2 overwritten/appended words and8-byte undo delta are committed only
after key, capacity and table result checks pass. No insertion/shift.
"""
from hangul_mixed_undo_thumb import CODE as UNDO
from hangul_extended_composer_thumb import replace_once

PREFIX = UNDO.split('validated:\n', 1)[0]
PREFIX = replace_once(PREFIX, 'str r2, [sp, #24]\n', '''str r2, [sp, #24]
str r1, [sp, #28]
cmp r1, #40
bhs reject
movs r1, r3
''')

CODE = PREFIX + '''validated:
ldr r0, [sp, #20]
cmp r0, #70
bhs reject_feed
ldrb r0, [r4, #4]
cmp r0, #255
beq fresh_cell
movs r5, r0
lsls r1, r0, #1
adds r1, #8
ldrh r0, [r4, r1]
b row_ready
fresh_cell:
ldrb r5, [r4, #3]
movs r0, #43
lsls r0, r0, #8
adds r0, #183
row_ready:
cmp r5, r6
bhs reject_feed
movs r1, #160
muls r0, r1, r0
ldr r1, [sp, #28]
lsls r1, r1, #2
adds r0, r0, r1
ldr r1, [sp, #24]
adds r0, r0, r1
ldrh r1, [r0]
ldrh r2, [r0, #2]
movs r0, #43
lsls r0, r0, #8
adds r0, #183
cmp r1, r0
bhs reject_feed
str r1, [sp]
str r2, [sp, #4]
adds r3, r5, #1
movs r1, #255
lsls r1, r1, #8
adds r1, #255
cmp r2, r1
beq width_ready
cmp r2, r0
bhs reject_feed
adds r3, #1
width_ready:
cmp r3, r6
bhi reject_feed
str r3, [sp, #8]
cmp r3, r7
bls count_ready
movs r7, r3
count_ready:
b emit
reject_feed:
b reject
emit:
ldr r0, [sp, #20]
lsls r0, r0, #3
adds r0, #28
adds r6, r4, r0
ldrb r0, [r4, #2]
strb r0, [r6]
ldrb r1, [r4, #3]
strb r1, [r6, #1]
ldrb r1, [r4, #4]
strb r1, [r6, #2]
movs r1, #0
strb r1, [r6, #3]
movs r3, #0
capture_old:
adds r1, r5, r3
cmp r1, r0
bhs old_empty
lsls r1, r1, #1
adds r1, #8
ldrh r2, [r4, r1]
b old_ready
old_empty:
movs r2, #255
lsls r2, r2, #8
adds r2, #255
old_ready:
lsls r1, r3, #1
adds r1, #4
strh r2, [r6, r1]
adds r3, #1
cmp r3, #2
blo capture_old
lsls r0, r5, #1
adds r0, #8
ldr r1, [sp]
strh r1, [r4, r0]
ldr r2, [sp, #4]
movs r1, #255
lsls r1, r1, #8
adds r1, #255
cmp r2, r1
beq written
adds r0, #2
strh r2, [r4, r0]
written:
strb r7, [r4, #2]
ldr r0, [sp, #8]
strb r0, [r4, #3]
subs r0, #1
strb r0, [r4, #4]
ldr r0, [sp, #20]
adds r0, #1
strb r0, [r4, #5]
movs r0, #1
add sp, #32
pop {r4, r5, r6, r7, pc}
'''
