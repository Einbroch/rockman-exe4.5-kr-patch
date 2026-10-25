"""Bounded A/B/cursor bridge for native353B0 ABI, CPU candidate ONLY.

r5=new editor96, r10=global with key-state pointer+4, pressed u16 at keys+2.
B precedes A. Candidate page0/6 rows/15 columns; col15 row2 right,row3 left.
Other commands/pages consumed without edits, pending full UI integration.
Return0/Z=1 when no A/B, return1/Z=0 for ALL A/B, including rejected edits:
original caller BNE must not move the grid after a consumed/rejected key.
No sound/visual rejection feedback, cancel/confirm/page/Latin support yet.
Own12+nested196=208 stack, caller owns pointers/tables/editor and stack.
Preserves r4..r11/SP. Never reads legacy word pointers. No ROM installation.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, r6, lr}
mov r3, r10
ldr r3, [r3, #4]
ldrh r3, [r3, #2]
movs r0, #3
tst r3, r0
beq action_unhandled
ldr r0, editor
cmp r5, r0
bne action_handled
ldrb r0, [r5, #4]
cmp r0, #1
blo action_handled
cmp r0, #10
bhi action_handled
movs r4, r5
adds r4, #20
ldrb r1, [r4]
movs r2, #15
ands r1, r2
cmp r0, r1
bne action_handled
movs r0, #2
tst r3, r0
beq action_select
movs r1, #40
b action_dispatch
action_select:
ldrb r0, [r5, #6]
cmp r0, #15
bhi action_handled
ldrb r1, [r5, #7]
cmp r1, #5
bhi action_handled
cmp r0, #15
beq action_command
ldrb r2, [r5, #8]
cmp r2, #0
bne action_handled
movs r2, #15
muls r1, r2, r1
adds r1, r1, r0
ldr r2, selectors
ldrb r1, [r2, r1]
cmp r1, #40
bhs action_handled
b action_dispatch
action_command:
cmp r1, #2
beq action_right
cmp r1, #3
bne action_handled
movs r1, #41
b action_dispatch
action_right:
movs r1, #42
action_dispatch:
movs r0, r4
movs r2, #76
ldr r3, context
ldr r6, helper
mov lr, pc
bx r6
action_handled:
movs r0, #1
pop {r4, r6, pc}
action_unhandled:
movs r0, #0
pop {r4, r6, pc}
'''

def assemble(address=0x08303000,selectors=0x09301000,context=0x09300000,helper=0x08F0D001):
    if context%4 or not helper&1:raise ValueError('context alignment/Thumb helper')
    return assemble_verified(CODE,address,dict(editor=0x0200FC40,selectors=selectors,context=context,helper=helper))
