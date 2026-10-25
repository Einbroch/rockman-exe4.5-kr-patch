"""Conditional list-initialization guard; CPU-only, no installed save ABI.

R12 is a transient status channel ONLY across verified33334/helper bodies.
Native getter/default/helper paths must not touch it. No global RAM flag.
Failure returns existing cancel code2, plays error sound127, empties three
display streams and skips count/heading/selection initialization. No dialog.
"""
from extended_dialogue import assemble_verified
from hangul_calendar_prefill import CODE


def assemble_adapter(address=0x0830E000):
    marker='pf_fail:\npop {r4}'
    if CODE.count(marker)!=1: raise ValueError('prefill failure boundary')
    code=CODE.replace(marker,'pf_fail:\nmovs r0, #0\nmov ip, r0\npop {r4}')
    return assemble_verified(code,address,dict(arena_body=0x020011FA,
        arena_bytes=255*32,pool=0x02026080,extents=41<<16|22,
        reader=0x0830D201,abort=0x08033373))


GUARD='''push {r4, lr}
movs r0, #1
mov ip, r0
ldr r4, prefill
mov lr, pc
bx r4
mov r0, ip
cmp r0, #1
bne pg_fail
pop {r4, pc}
pg_fail:
ldr r4, pool
movs r1, #3
pg_slot:
movs r0, #229
strb r0, [r4]
movs r0, #0
movs r2, #1
pg_clear:
strb r0, [r4, r2]
adds r2, #1
cmp r2, #41
blo pg_clear
adds r4, #128
subs r1, #1
bne pg_slot
movs r0, #20
str r0, [r5]
movs r0, #255
strb r0, [r5, #4]
movs r0, #24
strb r0, [r5, #5]
movs r0, #1
strb r0, [r5, #6]
movs r0, #2
strb r0, [r5, #7]
strb r0, [r5, #8]
movs r0, #0
strh r0, [r5, #10]
strb r0, [r5, #12]
strb r0, [r5, #13]
movs r0, #127
ldr r4, sound
mov lr, pc
bx r4
pop {r4}
add sp, #4
ldr r3, abort_init
bx r3
'''


def assemble_guard(address=0x0830E100):
    return assemble_verified(GUARD,address,dict(prefill=0x08033335,
        pool=0x02026080,sound=0x08000535,abort_init=0x08033151))
