"""Standalone native composition backend candidate, NOT a ROM hook.

State: byte0 cell count; byte1 capacity1..8; byte2 undo depth0..64;
byte3 active-tail flag0/1; eight little-endian words at+4 (ranks0..11171,
unfinished initial11172..11190, emptyFFFF); 64 undo pairs at+20
(old count | old active flag<<8, old tail). Exactly276 bytes. Caller owns aligned readable/writable
state and pinned immutable tables. This does NOT reserve game RAM.
Feed: r0 state, r1 key0..39, r2 transition table, r3 state byte capacity.
Undo: r0 state, r1 state byte capacity, r2 canonical deletion table.
Return r0=1 success/0 reject, r4..r11/SP preserved, flags unspecified.
"""
import struct
from hangul_keyboard_model import INITIALS,MEDIALS,State,Composer,transition

EMPTY=0xffff
EMPTY_ROW=11191
STATE_BYTES=276
KEYS=INITIALS+MEDIALS

def tail_rank(state):
    if state.l is None:return EMPTY
    return 11172+state.l if state.v is None else state.l*588+state.v*28+state.t

def state_from_rank(rank):
    if rank==EMPTY_ROW:return State()
    if rank>=11172:return State(l=rank-11172)
    return State(l=rank//588,v=(rank%588)//28,t=rank%28)

def table_pair(rank,key):
    try:n=transition(state_from_rank(rank),key,2)
    except ValueError:return EMPTY,EMPTY
    if n.committed:return ord(n.committed[0])-0xac00,tail_rank(n)
    return tail_rank(n),EMPTY

def build_tables():
    pairs=bytearray();deletions=bytearray()
    for rank in range(EMPTY_ROW+1):
        for key in KEYS:pairs.extend(struct.pack('<HH',*table_pair(rank,key)))
        if rank<EMPTY_ROW:
            c=Composer(1);c.state=state_from_rank(rank)
            if not c.backspace():raise ValueError('canonical deletion')
            deletions.extend(struct.pack('<H',tail_rank(c.state)))
    return bytes(pairs),bytes(deletions)

# Validation is shared source, not a game-specific live ABI. The first reject
# block stays close to validation branches to avoid Thumb-2 long branches.
VALIDATE='''ldrb r0, [r4]
str r0, [sp]
ldrb r1, [r4, #1]
cmp r1, #1
blo reject
cmp r1, #8
bhi reject
cmp r0, r1
bhi reject
ldrb r2, [r4, #2]
cmp r2, #64
bhi reject
str r2, [sp, #16]
ldrb r2, [r4, #3]
cmp r2, #1
bhi reject
str r2, [sp, #24]
cmp r0, #0
bne flag_ready
cmp r2, #0
bne reject
ldr r2, [sp, #16]
cmp r2, #0
bne reject
flag_ready:
movs r2, #255
lsls r2, r2, #8
adds r2, #255
str r2, [sp, #4]
adds r5, r4, #4
movs r7, #0
validate_words:
ldrh r2, [r5]
cmp r7, r0
bhs validate_empty
movs r3, #43
lsls r3, r3, #8
adds r3, #164
adds r1, r7, #1
cmp r1, r0
bne validate_rank
str r2, [sp, #4]
ldr r1, [sp, #24]
cmp r1, #0
beq validate_rank
adds r3, #19
validate_rank:
cmp r2, r3
bhs reject
b validate_next
validate_empty:
movs r3, #255
lsls r3, r3, #8
adds r3, #255
cmp r2, r3
bne reject
validate_next:
adds r5, #2
adds r7, #1
cmp r7, #8
blo validate_words
b validated
reject:
movs r0, #0
add sp, #32
pop {r4, r5, r6, r7, pc}
validated:
'''

FEED='''push {r4, r5, r6, r7, lr}
sub sp, #32
movs r4, r0
movs r6, r2
str r1, [sp, #20]
cmp r1, #40
bhs reject
movs r0, #69
lsls r0, r0, #2
cmp r3, r0
blo reject
'''+VALIDATE+'''ldr r0, [sp, #16]
cmp r0, #64
bhs reject_tail
ldr r0, [sp, #24]
cmp r0, #0
bne select_tail
movs r0, #43
lsls r0, r0, #8
adds r0, #183
b select_row
select_tail:
ldr r0, [sp, #4]
select_row:
movs r1, #160
muls r0, r1, r0
ldr r1, [sp, #20]
lsls r1, r1, #2
adds r0, r0, r1
adds r0, r0, r6
ldrh r1, [r0]
ldrh r2, [r0, #2]
movs r3, #43
lsls r3, r3, #8
adds r3, #183
cmp r1, r3
bhs reject_tail
str r1, [sp, #8]
str r2, [sp, #12]
ldr r0, [sp]
ldr r1, [sp, #24]
cmp r1, #0
bne count_started
adds r0, #1
count_started:
movs r5, #255
lsls r5, r5, #8
adds r5, #255
cmp r2, r5
beq count_ready
cmp r2, r3
bhs reject_tail
subs r3, #19
cmp r1, r3
bhs reject_tail
adds r0, #1
count_ready:
ldrb r1, [r4, #1]
cmp r0, r1
bhi reject_tail
str r0, [sp, #28]
ldr r0, [sp, #16]
lsls r1, r0, #2
adds r1, r1, r4
adds r1, #20
ldr r2, [sp]
ldr r3, [sp, #24]
lsls r3, r3, #8
orrs r3, r2
strh r3, [r1]
ldr r3, [sp, #4]
strh r3, [r1, #2]
adds r0, #1
strb r0, [r4, #2]
ldr r0, [sp, #24]
cmp r0, #0
beq output_slot
subs r2, #1
output_slot:
lsls r2, r2, #1
adds r2, r2, r4
adds r2, #4
ldr r0, [sp, #8]
strh r0, [r2]
ldr r0, [sp, #12]
cmp r0, r5
beq output_done
strh r0, [r2, #2]
output_done:
ldr r0, [sp, #28]
strb r0, [r4]
movs r0, #1
strb r0, [r4, #3]
add sp, #32
pop {r4, r5, r6, r7, pc}
reject_tail:
movs r0, #0
add sp, #32
pop {r4, r5, r6, r7, pc}
'''

UNDO='''push {r4, r5, r6, r7, lr}
sub sp, #32
movs r4, r0
movs r6, r2
movs r0, #69
lsls r0, r0, #2
cmp r1, r0
blo reject
'''+VALIDATE+'''ldr r0, [sp]
cmp r0, #0
beq reject_tail
ldr r3, [sp, #16]
cmp r3, #0
beq canonical
subs r3, #1
lsls r5, r3, #2
adds r5, r5, r4
adds r5, #20
ldrh r1, [r5]
lsrs r7, r1, #8
cmp r7, #1
bhi reject_tail
str r7, [sp, #24]
lsls r1, r1, #24
lsrs r1, r1, #24
ldrh r2, [r5, #2]
cmp r1, r0
bhi reject_tail
subs r0, r0, r1
cmp r0, #1
bhi reject_tail
movs r7, #255
lsls r7, r7, #8
adds r7, #255
cmp r1, #0
bne prior_rank
ldr r0, [sp, #24]
cmp r0, #0
bne reject_tail
cmp r2, r7
bne reject_tail
ldr r0, [sp]
cmp r0, #1
bne reject_tail
b restore
prior_rank:
movs r0, #43
lsls r0, r0, #8
adds r0, #164
ldr r7, [sp, #24]
cmp r7, #0
beq prior_limit_ready
adds r0, #19
prior_limit_ready:
cmp r2, r0
bhs reject_tail
restore:
movs r7, #255
lsls r7, r7, #8
adds r7, #255
strb r3, [r4, #2]
strh r7, [r5]
strh r7, [r5, #2]
ldr r0, [sp]
subs r0, #1
lsls r0, r0, #1
adds r0, r0, r4
adds r0, #4
strh r7, [r0]
cmp r1, #0
beq restore_done
subs r0, r1, #1
lsls r0, r0, #1
adds r0, r0, r4
adds r0, #4
strh r2, [r0]
restore_done:
strb r1, [r4]
ldr r0, [sp, #24]
strb r0, [r4, #3]
b success
canonical:
ldr r0, [sp, #4]
lsls r0, r0, #1
adds r0, r0, r6
ldrh r2, [r0]
movs r3, #255
lsls r3, r3, #8
adds r3, #255
cmp r2, r3
beq canonical_write
movs r0, #43
lsls r0, r0, #8
adds r0, #183
cmp r2, r0
bhs reject_tail
canonical_write:
ldr r1, [sp]
subs r0, r1, #1
lsls r0, r0, #1
adds r0, r0, r4
adds r0, #4
strh r2, [r0]
cmp r2, r3
bne canonical_active
subs r1, #1
strb r1, [r4]
movs r0, #0
strb r0, [r4, #3]
b success
canonical_active:
movs r0, #1
strb r0, [r4, #3]
success:
movs r0, #1
add sp, #32
pop {r4, r5, r6, r7, pc}
reject_tail:
movs r0, #0
add sp, #32
pop {r4, r5, r6, r7, pc}
'''
