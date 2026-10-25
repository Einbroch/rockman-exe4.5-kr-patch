"""Caller-selected LEGACY bytes -> compact76 candidate, not save detection.

r0 legacy record,r1 output76,r2 inputAvailable(low16)|outputAvailable(high16),
r3 logicalcapacity1..10. Return1/0; bytealignment/r4..r11/SP preserved;
stack96. Scans at most min(inputAvailable,2*cap+2), marker ignored like
original import. Singles00..E3/E4payload/E5 terminator only. Trailing legacy
padding ignored. Cursor0/activeNone, keyhistory empty. Empty record initializes.
Caller MUST select legacy format; this is not marker discrimination or a new
Hangul committed-record importer. Actual extents and disjoint stack owned by
caller; no editor/UI/destination writes or game/save integration.
"""
import struct
from hangul_native_tokens import tag
from extended_dialogue import assemble_verified


def import_legacy(record, capacity):
    if type(record) != bytes or type(capacity) != int or not 1 <= capacity <= 10:
        raise ValueError('legacy import arguments')
    bound = min(len(record), 2 * capacity + 2)
    pos, words = 1, []
    while pos < bound:
        b = record[pos]; pos += 1
        if b == 0xE5:
            return bytes([capacity | len(words) << 4, 0xF0, 0]) + struct.pack('<10H', *(tuple(words) + (65535,) * (10 - len(words)))) + bytes(52) + b'\xB0'
        if len(words) >= capacity: raise ValueError('legacy capacity')
        if b == 0xE4:
            if pos >= bound: raise ValueError('truncated legacy escape')
            words.append(tag(bytes([b, record[pos]]))); pos += 1
        elif b < 0xE4:
            words.append(tag(bytes([b])))
        else: raise ValueError('legacy control')
    raise ValueError('missing bounded legacy terminator')


CODE = '''push {r4, r5, r6, r7, lr}
sub sp, #76
movs r4, r0
movs r5, r1
movs r6, r3
cmp r6, #1
blo li_reject_start
cmp r6, #10
bhi li_reject_start
lsrs r0, r2, #16
cmp r0, #76
blo li_reject_start
lsls r0, r2, #16
lsrs r0, r0, #16
cmp r0, #2
blo li_reject_start
lsls r1, r6, #1
adds r1, #2
cmp r0, r1
bls li_bound
movs r0, r1
li_bound:
adds r0, r4, r0
cmp r0, r4
blo li_reject_start
movs r2, r5
adds r2, #76
cmp r2, r5
blo li_reject_start
cmp r4, r2
bhs li_disjoint
cmp r5, r0
blo li_reject_start
li_disjoint:
movs r7, r0
adds r4, #1
mov r3, sp
movs r0, #0
movs r1, #0
li_clear:
strb r1, [r3, r0]
adds r0, #1
cmp r0, #76
blo li_clear
movs r0, #3
movs r1, #255
li_empty_words:
strb r1, [r3, r0]
adds r0, #1
cmp r0, #23
blo li_empty_words
movs r0, #75
movs r1, #176
strb r1, [r3, r0]
movs r0, #240
strb r0, [r3, #1]
movs r2, #0
b li_scan
li_reject_start:
b li_reject
li_scan:
cmp r4, r7
bhs li_reject
ldrb r0, [r4]
adds r4, #1
cmp r0, #229
beq li_finish
cmp r2, r6
bhs li_reject
cmp r0, #228
bhi li_reject
beq li_escape
movs r1, #128
b li_word
li_escape:
cmp r4, r7
bhs li_reject
ldrb r0, [r4]
adds r4, #1
movs r1, #129
li_word:
mov r12, r4
lsls r4, r2, #1
adds r4, #3
mov r3, sp
strb r0, [r3, r4]
adds r4, #1
strb r1, [r3, r4]
mov r4, r12
adds r2, #1
b li_scan
li_finish:
mov r3, sp
lsls r2, r2, #4
orrs r2, r6
strb r2, [r3]
movs r0, #0
li_copy:
ldrb r1, [r3, r0]
strb r1, [r5, r0]
adds r0, #1
cmp r0, #76
blo li_copy
movs r0, #1
b li_return
li_reject:
movs r0, #0
li_return:
add sp, #76
pop {r4, r5, r6, r7, pc}
'''


def assemble(address=0x08000000):
    return assemble_verified(CODE, address, {})
