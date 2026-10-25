"""New-layout confirmation handler candidate, NOT installed game hook.

Caller selects new editor96 layout: r5 UI16+destination4+compact76.
Busy/choice/sound are original service addresses. Success emits record then
sound80/state14; failure emits sound7F/state0C. No/Cancel retains old state0C.
Own8+commit140=148 stack. No old temporary normalize/display write.
Caller owns editor/destination/stack and pinned transition table.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, lr}
movs r0, #128
ldr r4, busy
mov lr, pc
bx r4
bne cf_return
ldr r4, choice
mov lr, pc
bx r4
cmp r0, #2
beq cf_cancel
cmp r0, #1
beq cf_cancel
ldrb r0, [r5, #4]
cmp r0, #1
blo cf_cancel
cmp r0, #10
bhi cf_cancel
movs r1, r5
adds r1, #20
ldrb r2, [r1]
movs r3, #15
ands r2, r3
cmp r0, r2
bne cf_cancel
lsls r2, r0, #1
adds r2, #2
lsls r2, r2, #16
adds r2, #76
movs r0, r1
ldr r1, [r5, #16]
movs r4, r2
lsrs r4, r4, #16
adds r4, r1, r4
cmp r4, r1
blo cf_cancel
movs r0, r5
adds r0, #96
cmp r0, r5
blo cf_cancel
cmp r5, r4
bhs cf_disjoint
cmp r1, r0
blo cf_cancel
cf_disjoint:
movs r0, r5
adds r0, #20
ldr r3, table
ldr r4, commit
mov lr, pc
bx r4
cmp r0, #0
beq cf_cancel
movs r0, #128
ldr r4, sound
mov lr, pc
bx r4
movs r0, #20
b cf_state
cf_cancel:
movs r0, #127
ldr r4, sound
mov lr, pc
bx r4
movs r0, #12
cf_state:
strh r0, [r5]
cf_return:
pop {r4, pc}
'''

def assemble(address=0x08F08000,commit=0x08F06001,table=0x09000000):
    if not commit&1 or not 0x08000000<=commit<0x0A000000 or table%4:raise ValueError('confirm dependencies')
    return assemble_verified(CODE,address,dict(busy=0x08055409,choice=0x08055419,
        sound=0x08000535,commit=commit,table=table))
