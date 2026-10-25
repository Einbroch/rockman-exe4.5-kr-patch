"""Logical page/Start/empty-cancel controls, explicit new editor CPU candidate.

r0 command0 previous/1 next/2 toggle01/3 toggle12/4 Start/5 emptyB cancel;
r5 fixed new editor96. Returns1/Z0 handled,0/Z1 unsupported/invalid.
Page upload, sound, dialog are native service addresses, modeled in bench.
Start selects end cell first; complete second Start requests native dialog10.
Empty requests native dialog11/substate4. Partial emits7F and stays;
malformed query returns0 atomically, feedback policy remains unresolved.
Dry-run commit targets OWN stack24; never persistent record before Yes.
Own40+nestedcommit140=180 stack (query100 sequential); no game budget claim.
No raw-key integration, page glyph replacement, format/save/runtime adoption.
"""
from extended_dialogue import assemble_verified

# Native0850 has96 entries and silently skips a full queue. The new page
# index must not change before a transfer can be admitted. No IRQ reservation
# or runtime concurrency guarantee is inferred from this CPU-only guard.
QUEUE_GUARD='''ldr r0, queue_count
ldr r0, [r0]
cmp r0, #96
bhs control_fail_early
'''

CODE='''push {r4, r6, r7, lr}
sub sp, #24
movs r6, r0
ldr r0, editor
cmp r5, r0
bne control_fail_early
cmp r6, #5
bhi control_fail_early
cmp r6, #4
bhs control_query
'''+QUEUE_GUARD+'''
ldrb r1, [r5, #8]
cmp r1, #2
bhi control_fail_early
cmp r6, #0
beq control_previous
cmp r6, #1
beq control_next
cmp r6, #2
beq control_toggle01
cmp r1, #2
beq control_page1
movs r1, #2
b control_page
control_toggle01:
cmp r1, #0
beq control_page1
movs r1, #0
b control_page
control_previous:
cmp r1, #0
bne control_dec
movs r1, #3
control_dec:
subs r1, #1
b control_page
control_next:
adds r1, #1
cmp r1, #3
blo control_page
movs r1, #0
b control_page
control_page1:
movs r1, #1
control_page:
strb r1, [r5, #8]
ldr r4, page
mov lr, pc
bx r4
movs r0, #211
adds r0, #255
b control_sound_success
control_fail_early:
b control_fail
control_query:
ldrb r0, [r5, #4]
cmp r0, #1
blo control_fail
cmp r0, #10
bhi control_fail
movs r7, r5
adds r7, #20
ldrb r1, [r7]
movs r2, #15
ands r1, r2
cmp r0, r1
bne control_fail
movs r0, r7
movs r1, #24
movs r2, #76
ldr r3, table
ldr r4, query
mov lr, pc
bx r4
cmp r1, #1
bne control_fail
cmp r6, #5
bne control_start
cmp r0, #0
bne control_fail
ldrb r0, [r5, #14]
cmp r0, #2
beq control_success
movs r0, #2
strb r0, [r5, #14]
movs r0, #0
strb r0, [r5, #10]
movs r0, #20
strb r0, [r5]
movs r0, #127
b control_sound_success
control_start:
ldrb r1, [r5, #6]
cmp r1, #15
bne control_select_end
ldrb r1, [r5, #7]
cmp r1, #5
bne control_select_end
cmp r0, #0
beq control_empty
movs r0, r7
mov r1, sp
movs r2, #24
lsls r2, r2, #16
adds r2, #76
ldr r3, table
ldr r4, commit
mov lr, pc
bx r4
cmp r0, #0
beq control_partial
movs r6, #0
movs r7, #10
movs r0, #212
adds r0, #255
b control_dialog_sound
control_empty:
movs r6, #4
movs r7, #11
movs r0, #105
control_dialog_sound:
ldr r4, sound
mov lr, pc
bx r4
movs r0, #16
strb r0, [r5]
strb r6, [r5, #1]
movs r0, r7
movs r1, r6
ldr r4, dialog
mov lr, pc
bx r4
b control_success
control_partial:
movs r0, #127
b control_sound_success
control_select_end:
movs r0, #15
strb r0, [r5, #6]
movs r0, #5
strb r0, [r5, #7]
movs r0, #211
adds r0, #255
control_sound_success:
ldr r4, sound
mov lr, pc
bx r4
control_success:
movs r0, #1
b control_return
control_fail:
movs r0, #0
control_return:
add sp, #24
pop {r4, r6, r7, pc}
'''

def assemble(address=0x08F10000):
    return assemble_verified(CODE,address,dict(editor=0x0200FC40,page=0x080356D1,
        sound=0x08000535,dialog=0x080322CD,table=0x09000000,
        query=0x08F11001,commit=0x08F06001,queue_count=0x02010724))
