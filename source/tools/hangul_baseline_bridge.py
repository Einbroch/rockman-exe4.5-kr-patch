"""Record -> immutable replay baseline candidate; NOT an adopted save/game ABI.

Marker0: native absent record, payload ignored. Marker1: legacy routing result2,
not a validation of Japanese text. Proposed Hangul marker81..88 uses the strict
candidate record contract. Return1 + baseline20, or2/0 with no output writes.
r0 readable record(2*r1+2), r1 capacity1..8, r2 output, r3 output bytes>=20.
No persistent allocation: a future caller may derive baseline20 on its stack.
"""
import struct
from hangul_record_candidate import check_limit, unpack
from hangul_composer_thumb import EMPTY


def baseline(record, limit):
    check_limit(limit)
    if type(record) != bytes or len(record) != 2 * limit + 2:
        raise ValueError('record extent')
    if record[0] == 1:
        return 2, None
    text = '' if record[0] == 0 else unpack(record, limit)
    count = len(text)
    words = [ord(c) - 0xAC00 for c in text] + [EMPTY] * (8 - count)
    return 1, bytes([count, limit, 0, int(count != 0)]) + struct.pack('<8H', *words)


CODE = '''push {r4, r5, r6, r7, lr}
movs r4, r0
movs r5, r2
movs r6, r1
cmp r6, #1
blo reject
cmp r6, #8
bhi reject
cmp r3, #20
blo reject
movs r0, r5
adds r0, #20
bcs reject
movs r1, r6
lsls r1, r1, #1
adds r1, #2
adds r1, r1, r4
bcs reject
cmp r5, r1
bhs disjoint
cmp r0, r4
bls disjoint
b reject
disjoint:
ldrb r7, [r4]
cmp r7, #1
beq legacy
cmp r7, #0
beq emit_header
subs r7, #128
cmp r7, #1
blo reject
cmp r7, r6
bhi reject
movs r3, #0
adds r1, r4, #1
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
bhs reject
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
cmp r3, r6
blo validate
ldrb r0, [r1]
cmp r0, #229
beq emit_header
reject:
movs r0, #0
pop {r4, r5, r6, r7, pc}
legacy:
movs r0, #2
pop {r4, r5, r6, r7, pc}
emit_header:
strb r7, [r5]
strb r6, [r5, #1]
movs r0, #0
strb r0, [r5, #2]
cmp r7, #0
beq active_ready
movs r0, #1
active_ready:
strb r0, [r5, #3]
adds r1, r4, #1
adds r2, r5, #4
movs r3, #0
emit_words:
movs r0, #255
cmp r3, r7
bhs emit_empty
ldrb r0, [r1]
strb r0, [r2]
ldrb r0, [r1, #1]
b emit_high
emit_empty:
strb r0, [r2]
emit_high:
strb r0, [r2, #1]
adds r1, #2
adds r2, #2
adds r3, #1
cmp r3, #8
blo emit_words
movs r0, #1
pop {r4, r5, r6, r7, pc}
'''
