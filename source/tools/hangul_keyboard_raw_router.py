"""Native input ABI glue to verified edit/control candidates, CPU ONLY.

r5=new editor96, r10 global+4 -> key-state+2 pressed u16.
Priority B > A > Start > L > R; only these consume input. Rejections consumed
withr0=1/Z0; other keys return0/Z1 to native grid navigation. Empty B invokes
validated cancellation; nonempty B invokes existing edit dispatcher.
col15 rows0/1 page toggles,2/3 caret,4 pending,5 confirmation request.
Page0 jamo only; other-page glyph/Latin/space mapping still unresolved.
Own12+existing AB208=220 stack; logical controls192/query112 sequential.
Caller must select layout/format and own key/table/stack lifetimes.
No actual ROM installation or sound/page/dialog runtime execution.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, r6, lr}
mov r3, r10
ldr r3, [r3, #4]
ldrh r6, [r3, #2]
movs r0, #3
lsls r0, r0, #8
adds r0, #11
tst r6, r0
beq raw_unhandled
ldr r0, editor
cmp r5, r0
bne raw_handled
ldrb r0, [r5, #4]
cmp r0, #1
blo raw_handled
cmp r0, #10
bhi raw_handled
movs r1, r5
adds r1, #20
ldrb r1, [r1]
movs r2, #15
ands r1, r2
cmp r0, r1
bne raw_handled
movs r0, #2
tst r6, r0
beq raw_A
movs r0, r5
adds r0, #20
movs r1, #24
movs r2, #76
ldr r3, table
ldr r4, query
mov lr, pc
bx r4
cmp r1, #1
bne raw_handled
cmp r0, #0
bne raw_edit
movs r0, #5
b raw_control
raw_A:
movs r0, #1
tst r6, r0
beq raw_Start
ldrb r0, [r5, #6]
cmp r0, #15
bne raw_edit
ldrb r0, [r5, #7]
cmp r0, #0
beq raw_toggle01
cmp r0, #1
beq raw_toggle12
cmp r0, #5
bne raw_edit
movs r0, #4
b raw_control
raw_toggle01:
movs r0, #2
b raw_control
raw_toggle12:
movs r0, #3
b raw_control
raw_Start:
movs r0, #8
tst r6, r0
beq raw_L
movs r0, #4
b raw_control
raw_L:
movs r0, #2
lsls r0, r0, #8
tst r6, r0
beq raw_R
movs r0, #0
b raw_control
raw_R:
movs r0, #1
b raw_control
raw_edit:
ldr r4, edit
mov lr, pc
bx r4
b raw_handled
raw_control:
ldr r4, control
mov lr, pc
bx r4
raw_handled:
movs r0, #1
pop {r4, r6, pc}
raw_unhandled:
movs r0, #0
pop {r4, r6, pc}
'''

def assemble(address=0x08304000):
    return assemble_verified(CODE,address,dict(editor=0x0200FC40,table=0x09000000,
        query=0x08F11001,edit=0x08303001,control=0x08F10001))
