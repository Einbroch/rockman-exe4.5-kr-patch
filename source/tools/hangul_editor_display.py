"""Candidate edit-state to display-stream boundary; NOT installed in ROM.

F9FC indices0..11171 retain syllables,11172 retains existing comma.
Proposed keyboard jamo indices follow the declared extra-character repertoire.
Supply is metadata-bound; this editor helper is not installed in the ROM.
r0 readable compact64 (already canonical-replay validated by caller),
r1 writable destination, r2 destination bytes, r3 mode0 edit/1 commit.
Return r0 bytes including E5 or0 atomic reject; callee registers/SP preserved.
Valid caller-owned pointer extents required. Does not prove font consumption.
"""
import struct
from korean_codec import PREFIX,HANGUL_COUNT,EXTRA_CHARACTER_INDICES
from hangul_composer_thumb import KEYS,EMPTY

JAMO_BASE=HANGUL_COUNT+len(EXTRA_CHARACTER_INDICES)
if set(EXTRA_CHARACTER_INDICES.values())!=set(range(HANGUL_COUNT,JAMO_BASE)):raise ValueError('noncontiguous existing extras')
JAMO_INDICES={ch:JAMO_BASE+i for i,ch in enumerate(KEYS)}

def display(raw,mode=0):
    """Structural surface validation only; baseline/history validated upstream."""
    if len(raw)!=64 or mode not in (0,1):raise ValueError('input ABI')
    count,cap,depth,active=raw[:4]
    if not 1<=cap<=8 or count>cap or depth>56 or active>1 or raw[62]>56 or raw[63]:raise ValueError('header')
    if count==0 and (active or depth or mode):raise ValueError('empty state')
    words=struct.unpack_from('<8H',raw,4);indices=[]
    for i,rank in enumerate(words):
        if i>=count:
            if rank!=EMPTY:raise ValueError('unused word')
        elif rank<HANGUL_COUNT:indices.append(rank)
        elif rank<HANGUL_COUNT+19 and i==count-1 and active and not mode:
            indices.append(JAMO_INDICES[KEYS[rank-HANGUL_COUNT]])
        else:raise ValueError('partial/invalid rank')
    return b''.join(PREFIX+index.to_bytes(2,'little') for index in indices)+b'\xe5'

CODE=f'''push {{r4, r5, r6, r7, lr}}
sub sp, #8
movs r4, r0
movs r5, r1
str r3, [sp]
cmp r3, #1
bhi reject
ldrb r7, [r4]
ldrb r0, [r4, #1]
cmp r0, #1
blo reject
cmp r0, #8
bhi reject
cmp r7, r0
bhi reject
ldrb r1, [r4, #2]
cmp r1, #56
bhi reject
ldrb r6, [r4, #3]
cmp r6, #1
bhi reject
cmp r7, #0
bne count_ready
orrs r1, r6
orrs r1, r3
cmp r1, #0
bne reject
count_ready:
movs r0, r4
adds r0, #62
ldrb r1, [r0]
cmp r1, #56
bhi reject
ldrb r1, [r0, #1]
cmp r1, #0
bne reject
movs r0, r7
lsls r0, r0, #2
adds r0, #1
cmp r2, r0
blo reject
adds r2, r5, r0
bcs reject
movs r1, r4
adds r1, #64
bcs reject
cmp r5, r1
bhs disjoint
cmp r2, r4
bls disjoint
b reject
disjoint:
adds r1, r4, #4
movs r3, #0
validate:
ldrb r0, [r1, #1]
lsls r0, r0, #8
ldrb r2, [r1]
orrs r2, r0
cmp r3, r7
bhs empty
movs r0, #43
lsls r0, r0, #8
adds r0, #164
cmp r2, r0
blo next
adds r0, #19
cmp r2, r0
bhs reject
adds r0, r3, #1
cmp r0, r7
bne reject
cmp r6, #1
bne reject
ldr r0, [sp]
cmp r0, #0
bne reject
b next
empty:
movs r0, #255
lsls r0, r0, #8
adds r0, #255
cmp r2, r0
bne reject
next:
adds r1, #2
adds r3, #1
cmp r3, #8
blo validate
b validated
reject:
movs r0, #0
add sp, #8
pop {{r4, r5, r6, r7, pc}}
validated:
adds r1, r4, #4
movs r2, r5
movs r3, #0
cmp r7, #0
beq terminator
emit:
movs r0, #249
strb r0, [r2]
movs r0, #252
strb r0, [r2, #1]
ldrb r0, [r1, #1]
lsls r0, r0, #8
ldrb r6, [r1]
orrs r6, r0
movs r0, #43
lsls r0, r0, #8
adds r0, #164
cmp r6, r0
blo mapped
adds r6, #{JAMO_BASE-HANGUL_COUNT}
mapped:
strb r6, [r2, #2]
lsrs r6, r6, #8
strb r6, [r2, #3]
adds r1, #2
adds r2, #4
adds r3, #1
cmp r3, r7
blo emit
terminator:
movs r0, #229
strb r0, [r2]
movs r0, r7
lsls r0, r0, #2
adds r0, #1
add sp, #8
pop {{r4, r5, r6, r7, pc}}
'''
