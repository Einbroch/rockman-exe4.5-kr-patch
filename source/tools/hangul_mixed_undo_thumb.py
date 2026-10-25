"""Standalone mixed B/undo kernel, not installed and not a full state validator.

r0 aligned canonical588-byte state, r1 available bytes, r2 pinned deletion
table22382 bytes. Return1 success/0 reject; r4..r11/SP preserved, stack52.
Caller MUST establish complete canonical history, table identity, readable/
writable extents and disjoint stack. Kernel checks current surface, unused
history and top-delta bounds/words, NOT historical forward-transition validity.
Do NOT use this as decoder for imported/saved/untrusted state. No RAM allocated.
"""
CODE = '''push {r4, r5, r6, r7, lr}
sub sp, #32
movs r4, r0
str r2, [sp, #24]
movs r0, #147
lsls r0, r0, #2
cmp r1, r0
blo reject
adds r0, r4, r0
cmp r0, r4
blo reject
movs r0, #3
tst r4, r0
bne reject
ldrb r0, [r4]
cmp r0, #177
bne reject
ldrh r0, [r4, #6]
cmp r0, #0
bne reject
ldrb r6, [r4, #1]
cmp r6, #1
blo reject
cmp r6, #10
bhi reject
ldrb r7, [r4, #2]
cmp r7, r6
bhi reject
ldrb r0, [r4, #3]
cmp r0, r7
bhi reject
ldrb r1, [r4, #4]
cmp r1, #255
beq active_ok
cmp r1, r7
bhs reject
adds r1, #1
cmp r1, r0
bne reject
active_ok:
ldrb r0, [r4, #5]
cmp r0, #70
bhi reject
str r0, [sp, #20]
cmp r0, #0
beq header_ok
ldrb r1, [r4, #4]
cmp r1, #255
beq reject
header_ok:
movs r5, r4
adds r5, #8
movs r3, #0
surface_loop:
ldrh r0, [r5]
cmp r3, r7
bhs empty_word
movs r1, #43
lsls r1, r1, #8
adds r1, #183
cmp r0, r1
blo word_ok
lsrs r1, r0, #8
cmp r1, #129
beq native_word
cmp r1, #128
bne reject
movs r1, #255
ands r1, r0
cmp r1, #227
bhi reject
native_word:
ldrb r1, [r4, #4]
cmp r1, r3
beq reject
b word_ok
empty_word:
adds r0, #1
lsls r0, r0, #16
cmp r0, #0
bne reject
word_ok:
adds r5, #2
adds r3, #1
cmp r3, #10
blo surface_loop
ldr r0, [sp, #20]
lsls r0, r0, #3
adds r0, #28
movs r1, #147
lsls r1, r1, #2
padding_loop:
cmp r0, r1
bhs validated
ldrb r2, [r4, r0]
cmp r2, #0
bne reject
adds r0, #1
b padding_loop
reject:
movs r0, #0
add sp, #32
pop {r4, r5, r6, r7, pc}
validated:
ldr r0, [sp, #20]
cmp r0, #0
beq canonical
subs r0, #1
str r0, [sp, #20]
lsls r0, r0, #3
adds r0, #28
adds r5, r4, r0
ldrb r0, [r5, #3]
cmp r0, #0
bne reject_late
ldrb r0, [r5]
cmp r0, r7
bhi reject_late
str r0, [sp]
ldrb r1, [r5, #1]
cmp r1, r0
bhi reject_late
str r1, [sp, #4]
ldrb r2, [r5, #2]
str r2, [sp, #8]
cmp r2, #255
beq prior_inactive
cmp r2, r0
bhs reject_late
adds r3, r2, #1
cmp r3, r1
bne reject_late
movs r1, r2
b position_ready
prior_inactive:
ldr r3, [sp, #20]
cmp r3, #0
bne reject_late
position_ready:
cmp r1, r6
bhs reject_late
str r1, [sp, #12]
movs r3, #0
delta_words:
lsls r2, r3, #1
adds r2, #4
ldrh r2, [r5, r2]
adds r1, r1, r3
cmp r1, r0
bhs delta_empty
movs r1, #43
lsls r1, r1, #8
adds r1, #183
cmp r2, r1
blo delta_ok
lsrs r1, r2, #8
cmp r1, #129
beq delta_native
cmp r1, #128
bne reject_late
movs r1, #255
ands r1, r2
cmp r1, #227
bhi reject_late
delta_native:
cmp r3, #0
bne delta_ok
ldr r1, [sp, #8]
cmp r1, #255
bne reject_late
b delta_ok
delta_empty:
adds r2, #1
lsls r2, r2, #16
cmp r2, #0
bne reject_late
delta_ok:
adds r3, #1
ldr r1, [sp, #12]
cmp r3, #2
blo delta_words
b restore
reject_late:
b reject
restore:
ldr r0, [sp]
strb r0, [r4, #2]
ldr r1, [sp, #4]
strb r1, [r4, #3]
ldr r1, [sp, #8]
strb r1, [r4, #4]
ldr r1, [sp, #20]
strb r1, [r4, #5]
ldr r1, [sp, #12]
movs r3, #0
restore_words:
cmp r1, r0
bhs clear_tail
lsls r2, r3, #1
adds r2, #4
ldrh r2, [r5, r2]
lsls r6, r1, #1
adds r6, #8
strh r2, [r4, r6]
adds r1, #1
adds r3, #1
cmp r3, #2
blo restore_words
clear_tail:
movs r2, #255
lsls r2, r2, #8
adds r2, #255
lsls r0, r0, #1
adds r0, #8
clear_tail_loop:
cmp r0, #28
bhs clear_delta
strh r2, [r4, r0]
adds r0, #2
b clear_tail_loop
clear_delta:
movs r0, #0
str r0, [r5]
str r0, [r5, #4]
b success
canonical:
cmp r7, #0
beq reject_late
ldrb r0, [r4, #4]
cmp r0, #255
bne target_ready
ldrb r0, [r4, #3]
cmp r0, #0
beq target_ready
subs r0, #1
target_ready:
str r0, [sp, #12]
lsls r1, r0, #1
adds r1, #8
ldrh r2, [r4, r1]
lsrs r3, r2, #15
cmp r3, #0
bne remove_cell
lsls r2, r2, #1
ldr r3, [sp, #24]
ldrh r2, [r3, r2]
movs r3, #255
lsls r3, r3, #8
adds r3, #255
cmp r2, r3
beq remove_cell
strh r2, [r4, r1]
strb r0, [r4, #4]
adds r0, #1
strb r0, [r4, #3]
b success
remove_cell:
adds r5, r4, r1
subs r7, #1
strb r7, [r4, #2]
shift_loop:
cmp r0, r7
bhs removed
ldrh r2, [r5, #2]
strh r2, [r5]
adds r5, #2
adds r0, #1
b shift_loop
removed:
movs r2, #255
lsls r2, r2, #8
adds r2, #255
strh r2, [r5]
strb r2, [r4, #4]
ldr r0, [sp, #12]
strb r0, [r4, #3]
success:
movs r0, #1
add sp, #32
pop {r4, r5, r6, r7, pc}
'''
