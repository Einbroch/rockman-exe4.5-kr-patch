"""Selected friend recipe: cap6 person pool + exact bounded ROM suffix.

CPU clone only. r0 must be pool02026080. Return final stream length or0.
Validate person, canonicalize to private stream, append bounded suffix, validate
cap10 title, canonicalize again and require exact suffix extent consumption.
No external write before success. Person stage never touched; no global RAM.
Own88 + record-display80 =168 nested stack bytes. IRQ/space not adopted.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, r5, r6, r7, lr}
sub sp, #68
movs r4, r0
ldr r1, pool
cmp r4, r1
beq ac_start
b ac_fail
ac_start:
mov r1, sp
adds r1, #44
ldr r2, person_extents
movs r3, #6
ldr r7, converter
mov lr, pc
bx r7
cmp r0, #14
beq ac_person_valid
b ac_fail
ac_person_valid:
mov r0, sp
adds r0, #44
mov r1, sp
ldr r2, person_display_extents
movs r3, #6
ldr r7, decoder
mov lr, pc
bx r7
cmp r0, #0
beq ac_fail
subs r6, r0, #1
ldr r7, suffix_length
cmp r7, #1
blo ac_fail
cmp r7, #41
bhi ac_fail
adds r5, r6, r7
cmp r5, #41
bhi ac_fail
ldr r0, suffix
mov r1, sp
adds r1, r1, r6
movs r2, #0
ac_append:
ldrb r3, [r0, r2]
strb r3, [r1, r2]
adds r2, #1
cmp r2, r7
blo ac_append
mov r0, sp
mov r1, sp
adds r1, #44
ldr r2, title_output_extent
orrs r2, r5
movs r3, #10
ldr r7, converter
mov lr, pc
bx r7
cmp r0, #22
bne ac_fail
mov r0, sp
adds r0, #44
mov r1, sp
ldr r2, title_display_extents
movs r3, #10
ldr r7, decoder
mov lr, pc
bx r7
cmp r0, r5
bne ac_fail
mov r1, sp
movs r2, #0
ac_copy:
ldrb r3, [r1, r2]
strb r3, [r4, r2]
adds r2, #1
cmp r2, r5
blo ac_copy
movs r0, r5
b ac_return
ac_fail:
movs r0, #0
ac_return:
add sp, #68
pop {r4, r5, r6, r7, pc}
'''


def assemble(suffix_address,suffix_length,address=0x0830A000):
    if not 1<=suffix_length<=41 or not 0x08000000<=suffix_address<0x0A000000 or suffix_address+suffix_length>0x0A000000:
        raise ValueError('ROM suffix extent')
    return assemble_verified(CODE,address,dict(pool=0x02026080,
        suffix=suffix_address,suffix_length=suffix_length,
        converter=0x08309001,decoder=0x08F09001,
        person_extents=14<<16|25,person_display_extents=41<<16|14,
        title_output_extent=22<<16,title_display_extents=41<<16|22))


# Replaces3302A..3303C scan+append, not a global raw copier. Native sprite
# preceding and heading following remain in place. Native33050 has a coordinated
# explicit success result; failure restores33014's saved frame in a separate tail.
ADAPTER='''push {r4, lr}
ldr r0, pool
ldr r4, helper
mov lr, pc
bx r4
cmp r0, #0
beq aa_fail
pop {r4, pc}
aa_fail:
movs r0, #2
strb r0, [r5, #8]
movs r0, #1
strb r0, [r5, #6]
pop {r4}
add sp, #4
ldr r3, failure
bx r3
'''


def assemble_adapter(address=0x0830A200):
    return assemble_verified(ADAPTER,address,dict(pool=0x02026080,helper=0x0830A001,failure=0x0830A241))


def assemble_failure(address=0x0830A240):
    return assemble_verified('movs r0, #0\npop {r4, r5, r6, r7, pc}\n',address,{})


# Caller32E22 must not continue confirmation init32E26..34 after failed append.
# Accepted route unchanged; rejection goes to native caller pop32E36 with exit16.
CALLER='''push {r4, lr}
ldr r4, title
mov lr, pc
bx r4
cmp r0, #1
bne aw_fail
pop {r4, pc}
aw_fail:
movs r0, #16
str r0, [r5]
pop {r4}
add sp, #4
ldr r3, failure
bx r3
'''


def assemble_caller(address=0x0830A280):
    return assemble_verified(CALLER,address,dict(title=0x08033015,failure=0x08032E37))
