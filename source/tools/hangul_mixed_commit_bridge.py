"""Compact76 -> caller-selected mixed fixed record, not original commit ABI.

r0 compact,r1 record,r2 inputAvailable low16|outputAvailable high16,
r3 pinned transition table. Return record width or0, failure no external write.
Own44+nested encoder96=140 stack; replay68 is sequential. r4..r11/SP preserved.
Format selection, destination/table ownership and disjoint stack are caller duties.
"""
from hangul_mixed_replay_thumb import CODE as REPLAY
from hangul_mixed_record import ENCODE,pack_surface,surface_from_compact
from hangul_mixed_cache_bridge import scoped
from hangul_mixed_keyedit_thumb import assemble as assemble_code

def record(raw):
    return pack_surface(surface_from_compact(raw))

CODE='''push {r4, r5, lr}
sub sp, #32
movs r4, r0
movs r5, r1
lsrs r0, r2, #16
str r0, [sp, #24]
lsls r2, r2, #16
lsrs r2, r2, #16
cmp r2, #76
blo cm_fail
movs r0, r4
adds r0, #76
cmp r0, r4
blo cm_fail
ldrb r1, [r4]
movs r2, #15
ands r1, r2
cmp r1, #1
blo cm_fail
cmp r1, #10
bhi cm_fail
lsls r1, r1, #1
adds r1, #2
ldr r2, [sp, #24]
cmp r2, r1
blo cm_fail
adds r1, r5, r1
cmp r1, r5
blo cm_fail
cmp r4, r1
bhs cm_disjoint
cmp r5, r0
blo cm_fail
cm_disjoint:
movs r2, #24
lsls r2, r2, #16
adds r2, #76
movs r0, r4
mov r1, sp
bl cm_replay
cmp r0, #0
beq cm_fail
ldr r2, [sp, #24]
lsls r2, r2, #16
adds r2, #24
mov r0, sp
movs r1, r5
movs r3, #0
bl cm_encode
b cm_return
cm_fail:
movs r0, #0
cm_return:
add sp, #32
pop {r4, r5, pc}
cm_replay:
'''+scoped(REPLAY,'cm_r_')+'''cm_encode:
'''+scoped(ENCODE,'cm_e_')

def assemble(address=0x08F06000):
    return assemble_code(address,CODE)
