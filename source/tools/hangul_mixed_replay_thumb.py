"""Read-only compact76 -> mixed current surface24 native candidate.

r0 source, r1 output, r2 sourceAvailable | outputAvailable<<16, r3 pinned
transition table1790720 bytes. Return1/0; byte alignment allowed; r4..r11/SP
preserved;68-byte stack (scratch24/locals24/saved20), no588-byte history.
Output: count/cap/cursor/active(FF=none),10 LE words/unusedFFFF. This differs
from older pure-Hangul24-byte surface; do NOT pass it to those consumers.
Rejects malformed baseline/packed keys/failed replay atomically. Extents,
table identity/address alignment and disjoint function stack are caller-owned.
Not game/save integration or glyph/commit validation.
"""
CODE = '''push {r4, r5, r6, r7, lr}
sub sp, #48
movs r4, r0
str r1, [sp, #24]
str r3, [sp, #28]
lsls r0, r2, #16
lsrs r0, r0, #16
cmp r0, #76
blo reject_start
lsrs r0, r2, #16
cmp r0, #24
blo reject_start
movs r0, r4
adds r0, #76
cmp r0, r4
blo reject_start
movs r2, r1
adds r2, #24
cmp r2, r1
blo reject_start
cmp r4, r2
bhs disjoint
cmp r1, r0
blo reject_start
disjoint:
movs r0, #75
ldrb r0, [r4, r0]
lsrs r0, r0, #4
cmp r0, #11
bne reject_start
ldrb r0, [r4, #2]
cmp r0, #70
bhi reject_start
str r0, [sp, #32]
ldrb r6, [r4]
lsrs r0, r6, #4
movs r7, #15
ands r7, r6
movs r6, r0
cmp r7, #1
blo reject_start
cmp r7, #10
bhi reject_start
cmp r6, r7
bhi reject_start
mov r5, sp
strb r6, [r5]
strb r7, [r5, #1]
ldrb r2, [r4, #1]
lsrs r1, r2, #4
movs r0, #15
ands r2, r0
cmp r2, r6
bhi reject_start
cmp r1, #15
bne has_active
movs r1, #255
b active_ready
has_active:
cmp r1, r6
bhs reject_start
adds r0, r1, #1
cmp r0, r2
bne reject_start
active_ready:
strb r2, [r5, #2]
strb r1, [r5, #3]
b baseline_begin
reject_start:
movs r0, #0
add sp, #48
pop {r4, r5, r6, r7, pc}
baseline_begin:
movs r3, #0
baseline_loop:
lsls r1, r3, #1
adds r1, #3
ldrb r0, [r4, r1]
adds r1, #1
ldrb r2, [r4, r1]
lsls r2, r2, #8
orrs r0, r2
cmp r3, r6
bhs empty_word
movs r1, #43
lsls r1, r1, #8
adds r1, #183
cmp r0, r1
blo baseline_valid
lsrs r1, r0, #8
cmp r1, #129
beq native_word
cmp r1, #128
bne reject_baseline
movs r1, #255
ands r1, r0
cmp r1, #227
bhi reject_baseline
native_word:
ldrb r1, [r5, #3]
cmp r1, r3
beq reject_baseline
b baseline_valid
empty_word:
adds r2, r0, #1
lsls r2, r2, #16
cmp r2, #0
bne reject_baseline
baseline_valid:
lsls r1, r3, #1
adds r1, #4
strh r0, [r5, r1]
adds r3, #1
cmp r3, #10
blo baseline_loop
movs r0, #0
str r0, [sp, #36]
b keys_begin
reject_baseline:
b reject_start
keys_begin:
ldr r0, [sp, #36]
cmp r0, #70
bhs emit
movs r1, #6
muls r0, r1, r0
movs r3, #7
ands r3, r0
lsrs r0, r0, #3
adds r0, #23
ldrb r2, [r4, r0]
adds r0, #1
ldrb r1, [r4, r0]
lsls r1, r1, #8
orrs r2, r1
lsrs r2, r3
movs r1, #63
ands r2, r1
ldr r0, [sp, #36]
ldr r1, [sp, #32]
cmp r0, r1
blo replay
cmp r2, #0
bne reject_key
b key_next
replay:
cmp r2, #40
bhs reject_key
str r2, [sp, #40]
ldrb r0, [r5, #3]
cmp r0, #255
beq fresh
str r0, [sp, #44]
lsls r0, r0, #1
adds r0, #4
ldrh r0, [r5, r0]
b row_ready
fresh:
ldrb r0, [r5, #2]
str r0, [sp, #44]
movs r0, #43
lsls r0, r0, #8
adds r0, #183
row_ready:
ldr r1, [sp, #44]
cmp r1, r7
bhs reject_key
movs r1, #160
muls r0, r1, r0
ldr r1, [sp, #40]
lsls r1, r1, #2
adds r0, r0, r1
ldr r1, [sp, #28]
adds r0, r0, r1
ldrh r1, [r0]
ldrh r2, [r0, #2]
movs r0, #43
lsls r0, r0, #8
adds r0, #183
cmp r1, r0
bhs reject_key
ldr r3, [sp, #44]
adds r3, #1
str r1, [sp, #40]
movs r1, #255
lsls r1, r1, #8
adds r1, #255
cmp r2, r1
beq single
cmp r2, r0
bhs reject_key
adds r3, #1
single:
cmp r3, r7
bhi reject_key
ldr r0, [sp, #44]
lsls r0, r0, #1
adds r0, #4
ldr r1, [sp, #40]
strh r1, [r5, r0]
movs r1, #255
lsls r1, r1, #8
adds r1, #255
cmp r2, r1
beq words_ready
adds r0, #2
strh r2, [r5, r0]
words_ready:
cmp r3, r6
bls count_ready
movs r6, r3
strb r6, [r5]
count_ready:
strb r3, [r5, #2]
subs r3, #1
strb r3, [r5, #3]
key_next:
ldr r0, [sp, #36]
adds r0, #1
str r0, [sp, #36]
b keys_begin
reject_key:
b reject_start
emit:
ldr r1, [sp, #24]
movs r0, #0
copy_output:
ldrb r2, [r5, r0]
strb r2, [r1, r0]
adds r0, #1
cmp r0, #24
blo copy_output
movs r0, #1
add sp, #48
pop {r4, r5, r6, r7, pc}
'''
