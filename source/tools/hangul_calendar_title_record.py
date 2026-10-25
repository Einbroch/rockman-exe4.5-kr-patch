"""Bounded final display title -> caller-selected NEW mixed record.

CPU candidate only, no format detection, save discriminator or ROM adoption.
r0 stream, r1 record, r2 inputAvailable low16 | outputAvailable high16,
r3 cap1..10. Input extent1..41; output2*cap+2, disjoint declared extents.
Return record width or0; validate in private stack before any external write.
Accept native00..E3, E4+any payload, F9FC+LE complete Hangul rank, E5 end.
No partial jamo, empty title, silent truncation, or control commands accepted.
Own stack44bytes. Preserve r4..r11/SP. Stage/person baseline never accessed.
"""
import struct
from extended_dialogue import assemble_verified


def convert(stream, cap=10):
    if not 1 <= cap <= 10 or not 1 <= len(stream) <= 41:
        raise ValueError('extent/cap')
    words=[]; i=0
    while i < len(stream):
        b=stream[i]; i+=1
        if b == 0xE5:
            if not words: raise ValueError('empty')
            return bytes([0x80+len(words)])+b''.join(struct.pack('<H',w) for w in words)+b'\xFF\xFF'*(cap-len(words))+b'\xE5'
        if len(words) == cap: raise ValueError('capacity')
        if b <= 0xE3: w=0x8000+b
        elif b == 0xE4:
            if i == len(stream): raise ValueError('truncated escape')
            w=0x8100+stream[i]; i+=1
        elif b == 0xF9:
            if i+3 > len(stream) or stream[i] != 0xFC: raise ValueError('truncated glyph')
            w=int.from_bytes(stream[i+1:i+3],'little'); i+=3
            if w >= 11172: raise ValueError('not complete Hangul')
        else: raise ValueError('command')
        words.append(w)
    raise ValueError('unterminated')


CODE='''push {r4, r5, r6, r7, lr}
sub sp, #24
movs r4, r0
movs r5, r1
movs r7, r3
cmp r7, #1
blo tr_early
cmp r7, #10
bhi tr_early
lsls r0, r2, #16
lsrs r0, r0, #16
cmp r0, #1
blo tr_early
cmp r0, #41
bhi tr_early
adds r6, r4, r0
cmp r6, r4
blo tr_early
lsrs r2, r2, #16
lsls r0, r7, #1
adds r0, #2
cmp r2, r0
blo tr_early
adds r1, r5, r2
cmp r1, r5
blo tr_early
cmp r4, r1
bhs tr_disjoint
cmp r5, r6
blo tr_early
tr_disjoint:
mov r2, sp
movs r0, #255
movs r1, #0
tr_pad:
strb r0, [r2, r1]
adds r1, #1
cmp r1, #24
blo tr_pad
movs r3, #0
b tr_next
tr_early:
b tr_fail
tr_next:
cmp r4, r6
bhs tr_fail
ldrb r0, [r4]
adds r4, #1
cmp r0, #229
beq tr_end
cmp r3, r7
bhs tr_fail
cmp r0, #227
bls tr_single
cmp r0, #228
beq tr_escape
cmp r0, #249
bne tr_fail
movs r1, r4
adds r1, #3
cmp r1, r6
bhi tr_fail
ldrb r0, [r4]
cmp r0, #252
bne tr_fail
ldrb r1, [r4, #1]
ldrb r0, [r4, #2]
lsls r0, r0, #8
orrs r1, r0
ldr r0, rank_limit
cmp r1, r0
bhs tr_fail
adds r4, #3
b tr_word
tr_escape:
cmp r4, r6
bhs tr_fail
ldrb r1, [r4]
adds r4, #1
movs r0, #129
b tr_tag
tr_single:
movs r1, r0
movs r0, #128
tr_tag:
lsls r0, r0, #8
orrs r1, r0
tr_word:
lsls r0, r3, #1
adds r0, #1
strb r1, [r2, r0]
adds r0, #1
lsrs r1, r1, #8
strb r1, [r2, r0]
adds r3, #1
b tr_next
tr_end:
cmp r3, #0
beq tr_fail
adds r3, #128
strb r3, [r2]
lsls r0, r7, #1
adds r0, #1
movs r1, #229
strb r1, [r2, r0]
adds r7, r0, #1
movs r3, #0
tr_copy:
ldrb r1, [r2, r3]
strb r1, [r5, r3]
adds r3, #1
cmp r3, r7
blo tr_copy
movs r0, r7
b tr_return
tr_fail:
movs r0, #0
tr_return:
add sp, #24
pop {r4, r5, r6, r7, pc}
'''


def assemble(address=0x08309000):
    return assemble_verified(CODE,address,dict(rank_limit=11172))


# Pool route32F06 receives final title, not person stage. Record arena check
# precedes converter; register37366 runs only after success via shared adapter.
COMMIT='''push {r4, r5, r6, lr}
movs r4, r0
movs r5, r1
ldr r6, context
ldr r6, [r6, #44]
movs r2, r6
adds r2, #10
cmp r5, r2
bne tc_fail
ldr r2, arena
cmp r6, r2
blo tc_fail
subs r6, r6, r2
ldr r2, arena_bytes
cmp r6, r2
bhs tc_fail
movs r2, #31
tst r6, r2
bne tc_fail
ldr r2, pool
cmp r4, r2
bne tc_fail
movs r0, r4
movs r1, r5
ldr r2, extents
movs r3, #10
ldr r6, converter
mov lr, pc
bx r6
b tc_return
tc_fail:
movs r0, #0
tc_return:
pop {r4, r5, r6, pc}
'''


def assemble_commit(address=0x08309200):
    return assemble_verified(COMMIT,address,dict(context=0x02014DD0,
        arena=0x020011F0,arena_bytes=255*32,pool=0x02026080,
        extents=22<<16|41,converter=0x08309001))
