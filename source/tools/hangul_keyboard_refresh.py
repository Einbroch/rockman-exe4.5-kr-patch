"""Fixed-fixture editor96 -> cache41 -> native20-cell render refresh.

r5=new editor, r10 preserved; return1/Z0 queued,0/Z1 deferred/rejected.
No game RAM/ROM/IRQ adoption. Queue guard protects pending staging readers.
Own32+cache112=144 stack; native parser/queue56 sequential below this bound.
"""
from extended_dialogue import assemble_verified

GUARD='''push {r4, r5, lr}
ldr r0, counter
ldr r4, [r0]
cmp r4, #96
bhs guard_fail
ldr r1, queue
ldr r2, stage
ldr r5, stage_end
guard_loop:
cmp r4, #0
beq guard_success
ldr r0, [r1]
ldr r3, [r1, #8]
cmp r3, #0
beq guard_next
adds r3, r0, r3
bcs guard_fail
cmp r0, r5
bhs guard_next
cmp r3, r2
bhi guard_fail
guard_next:
adds r1, #20
subs r4, #1
b guard_loop
guard_success:
movs r0, #1
pop {r4, r5, pc}
guard_fail:
movs r0, #0
pop {r4, r5, pc}
'''

CODE='''push {r4, r5, r6, r7, lr}
mov r4, r8
mov r6, r9
mov r7, r10
push {r4, r6, r7}
ldr r0, editor
cmp r5, r0
bne refresh_fail
ldrb r0, [r5, #4]
cmp r0, #1
blo refresh_fail
cmp r0, #10
bhi refresh_fail
movs r1, r5
adds r1, #20
ldrb r1, [r1]
movs r2, #15
ands r1, r2
cmp r0, r1
bne refresh_fail
ldr r4, guard
mov lr, pc
bx r4
cmp r0, #1
bne refresh_fail
movs r0, r5
adds r0, #20
ldr r1, cache
movs r2, #41
lsls r2, r2, #16
adds r2, #76
ldr r3, table
ldr r4, cache_helper
mov lr, pc
bx r4
cmp r0, #0
beq refresh_fail
ldr r0, context
mov r10, r0
movs r1, #0
str r1, [r0, #48]
ldr r1, parser
mov r12, r1
ldr r0, cache
movs r1, #165
ldr r2, stage
ldr r3, target
movs r4, #20
movs r5, #1
ldr r6, font
movs r7, #0
mov lr, pc
bx r12
movs r0, #1
b refresh_return
refresh_fail:
movs r0, #0
refresh_return:
pop {r4, r6, r7}
mov r8, r4
mov r9, r6
mov r10, r7
pop {r4, r5, r6, r7, pc}
'''


def assemble():
    guard,guard_isa=assemble_verified(GUARD,0x08F13000,dict(counter=0x02010724,queue=0x02012730,stage=0x0201E800,stage_end=0x0201ED00))
    refresh,isa=assemble_verified(CODE,0x08F12000,dict(editor=0x0200FC40,guard=0x08F13001,cache=0x020155F0,table=0x09000000,cache_helper=0x08F01001,context=0x0200FBE0,parser=0x03006825,stage=0x0201E800,target=0x0600B000,font=0x08619EF8))
    return refresh,guard,isa,guard_isa
