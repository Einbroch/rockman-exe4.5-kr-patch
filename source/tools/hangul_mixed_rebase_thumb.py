"""Compact76 cursor/native/canonical-delete rebase CPU candidate, not hook.

r0 in-place76,r1 left41/right42/canonicalB43 or opaque native word,
r2 available,r3 aligned context8 (LE transition pointer, deletion pointer).
Return1/0; preserves r4..r11/SP; own128+nested68=196 stack. Pinned tables,
actual context/state extents and stack disjointness are caller obligations.
Canonical B only when keycount0; dispatch accepted-key B to keyedit40.
Movement/native overwrite clear history, preserving every sealed partial.
No actual memory allocation, save serialization or native keyboard hooks.
"""
from hangul_mixed_replay_thumb import CODE as REPLAY
from hangul_mixed_keyedit_thumb import assemble as assemble_verified

CODE = '''push {r4, r5, r6, r7, lr}
sub sp, #108
movs r4, r0
movs r5, r3
movs r6, r1
cmp r2, #76
blo rb_fail_start
adds r0, #76
cmp r0, r4
blo rb_fail_start
mov r7, sp
movs r0, #0
rb_copy_in:
ldrb r1, [r4, r0]
strb r1, [r7, r0]
adds r0, #1
cmp r0, #76
blo rb_copy_in
movs r0, r7
movs r1, r7
adds r1, #76
movs r2, #24
lsls r2, r2, #16
adds r2, #76
ldr r3, [r5]
bl rb_decode
cmp r0, #1
bne rb_fail_start
adds r7, #76
cmp r6, #41
beq rb_left
cmp r6, #42
beq rb_right
cmp r6, #43
beq rb_delete
b rb_native
rb_fail_start:
b rb_fail
rb_left:
ldrb r0, [r7, #2]
cmp r0, #0
beq rb_fail_start
subs r0, #1
b rb_move
rb_right:
ldrb r0, [r7, #2]
ldrb r1, [r7]
cmp r0, r1
bhs rb_fail_start
adds r0, #1
rb_move:
strb r0, [r7, #2]
movs r0, #255
strb r0, [r7, #3]
b rb_serialize
rb_native:
lsrs r0, r6, #8
cmp r0, #129
beq rb_native_valid
cmp r0, #128
bne rb_fail_start
movs r0, #255
ands r0, r6
cmp r0, #227
bhi rb_fail_start
rb_native_valid:
ldrb r0, [r7, #2]
ldrb r1, [r7, #1]
cmp r0, r1
bhs rb_fail_start
lsls r1, r0, #1
adds r1, #4
strh r6, [r7, r1]
adds r0, #1
strb r0, [r7, #2]
ldrb r1, [r7]
cmp r0, r1
bls rb_native_count
strb r0, [r7]
rb_native_count:
movs r0, #255
strb r0, [r7, #3]
b rb_serialize
rb_delete:
mov r0, sp
ldrb r0, [r0, #2]
cmp r0, #0
bne rb_fail_start
ldrb r0, [r7]
cmp r0, #0
beq rb_fail_start
ldrb r3, [r7, #3]
cmp r3, #255
bne rb_target
ldrb r3, [r7, #2]
cmp r3, #0
beq rb_target
subs r3, #1
rb_target:
lsls r0, r3, #1
adds r0, #4
ldrh r1, [r7, r0]
lsrs r2, r1, #15
movs r6, r2
cmp r2, #0
bne rb_remove
lsls r1, r1, #1
ldr r2, [r5, #4]
ldrh r1, [r2, r1]
movs r2, #255
lsls r2, r2, #8
adds r2, #255
cmp r1, r2
beq rb_remove
strh r1, [r7, r0]
strb r3, [r7, #3]
adds r3, #1
strb r3, [r7, #2]
b rb_serialize
rb_remove:
movs r1, r0
rb_shift:
adds r2, r1, #2
cmp r2, #24
bhs rb_shift_done
ldrh r2, [r7, r2]
strh r2, [r7, r1]
adds r1, #2
b rb_shift
rb_shift_done:
movs r1, #255
lsls r1, r1, #8
adds r1, #255
strh r1, [r7, #22]
ldrb r1, [r7]
subs r1, #1
strb r1, [r7]
cmp r6, #0
beq rb_remove_cursor
ldrb r3, [r7, #2]
cmp r3, #0
beq rb_remove_cursor
subs r3, #1
rb_remove_cursor:
strb r3, [r7, #2]
movs r0, #255
strb r0, [r7, #3]
rb_serialize:
mov r2, sp
ldrb r0, [r7]
lsls r0, r0, #4
ldrb r1, [r7, #1]
orrs r0, r1
strb r0, [r2]
ldrb r0, [r7, #3]
movs r1, #15
ands r0, r1
lsls r0, r0, #4
ldrb r1, [r7, #2]
orrs r0, r1
strb r0, [r2, #1]
movs r0, #0
strb r0, [r2, #2]
movs r0, #0
rb_baseline_words:
adds r1, r0, #4
ldrb r1, [r7, r1]
adds r3, r0, #3
strb r1, [r2, r3]
adds r0, #1
cmp r0, #20
blo rb_baseline_words
movs r0, #23
movs r1, #0
rb_clear_keys:
strb r1, [r2, r0]
adds r0, #1
cmp r0, #76
blo rb_clear_keys
movs r0, #75
movs r1, #176
strb r1, [r2, r0]
movs r0, r2
movs r1, r7
movs r2, #24
lsls r2, r2, #16
adds r2, #76
ldr r3, [r5]
bl rb_decode
cmp r0, #1
bne rb_fail
mov r7, sp
movs r0, #0
rb_copy_out:
ldrb r1, [r7, r0]
strb r1, [r4, r0]
adds r0, #1
cmp r0, #76
blo rb_copy_out
movs r0, #1
b rb_return
rb_fail:
movs r0, #0
rb_return:
add sp, #108
pop {r4, r5, r6, r7, pc}
rb_decode:
''' + REPLAY


def assemble(address=0x08003000):
    return assemble_verified(address, CODE)
