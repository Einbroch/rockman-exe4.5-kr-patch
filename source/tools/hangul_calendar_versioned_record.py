"""Conditional calendar storage candidate, NOT adopted save ABI.

Fixed22: F8 version marker +10 LE identity words +E5. Count is derived from
contiguous occupied words followed byFFFF padding; existing strict decoder
validates values/padding/terminator. F8 is outside the DECLARED legacy title
grammar00..E3/E4payload/F9FCrank/E5, not a proof of all real game writers.
Inventory of every default/import/writer and real save compatibility pending.
Keep internal count-marker records unchanged; convert only at storage boundary.
Both helpers r0source,r1dest,r2 inputAvailable low16|outputAvailable high16,
r3=10. Reject overlapping declared output/source extents, no partial writes.
Writer consumes stream1..41, emits22. Reader consumes exactly22, emits<=41.
Writer stack44+converter44=88. Reader44+decoder80=124.
"""
import struct
from extended_dialogue import assemble_verified
from hangul_calendar_title_record import convert
from hangul_mixed_record_display import stream

VERSION=0xF8


def pack(title):
    record=convert(title,10)
    return bytes([VERSION])+record[1:]


def read(record):
    if type(record)!=bytes or len(record)!=22:raise ValueError('calendar field width')
    if record[0]==VERSION:
        words=struct.unpack_from('<10H',record,1)
        count=next((i for i,w in enumerate(words) if w==65535),10)
        if not count:raise ValueError('empty tagged record')
        internal=bytes([128+count])+record[1:]
    else:internal=convert(record,10)
    return stream(internal,10)


WRITER='''push {r4, r5, r6, r7, lr}
sub sp, #24
movs r4, r0
movs r5, r1
cmp r3, #10
bne vw_fail
lsls r6, r2, #16
lsrs r6, r6, #16
cmp r6, #1
blo vw_fail
cmp r6, #41
bhi vw_fail
adds r0, r4, r6
cmp r0, r4
blo vw_fail
lsrs r2, r2, #16
cmp r2, #22
blo vw_fail
adds r1, r5, r2
cmp r1, r5
blo vw_fail
cmp r4, r1
bhs vw_disjoint
cmp r5, r0
blo vw_fail
vw_disjoint:
movs r0, r4
mov r1, sp
ldr r2, output_extent
orrs r2, r6
movs r3, #10
ldr r7, converter
mov lr, pc
bx r7
cmp r0, #22
bne vw_fail
mov r1, sp
movs r0, #248
strb r0, [r1]
movs r2, #0
vw_copy:
ldrb r3, [r1, r2]
strb r3, [r5, r2]
adds r2, #1
cmp r2, #22
blo vw_copy
movs r0, #22
b vw_return
vw_fail:
movs r0, #0
vw_return:
add sp, #24
pop {r4, r5, r6, r7, pc}
'''


READER='''push {r4, r5, r6, r7, lr}
sub sp, #24
movs r4, r0
movs r5, r1
cmp r3, #10
bne vr_early
lsls r0, r2, #16
lsrs r0, r0, #16
cmp r0, #22
blo vr_early
movs r0, r4
adds r0, #22
cmp r0, r4
blo vr_early
lsrs r7, r2, #16
adds r1, r5, r7
cmp r1, r5
blo vr_early
cmp r4, r1
bhs vr_disjoint
cmp r5, r0
blo vr_early
vr_disjoint:
ldrb r0, [r4]
cmp r0, #248
beq vr_tagged
movs r0, r4
mov r1, sp
ldr r2, legacy_extents
movs r3, #10
ldr r6, converter
mov lr, pc
bx r6
cmp r0, #22
bne vr_early
b vr_decode
vr_early:
b vr_fail
vr_tagged:
mov r2, sp
movs r3, #0
vr_copy:
ldrb r0, [r4, r3]
strb r0, [r2, r3]
adds r3, #1
cmp r3, #22
blo vr_copy
movs r6, #0
movs r3, #1
vr_count:
ldrb r0, [r2, r3]
adds r3, #1
ldrb r1, [r2, r3]
adds r3, #1
cmp r0, #255
bne vr_occupied
cmp r1, #255
beq vr_count_done
vr_occupied:
adds r6, #1
cmp r6, #10
blo vr_count
vr_count_done:
cmp r6, #0
beq vr_fail
adds r6, #128
strb r6, [r2]
vr_decode:
mov r0, sp
movs r1, r5
lsls r2, r7, #16
adds r2, #22
movs r3, #10
ldr r6, decoder
mov lr, pc
bx r6
b vr_return
vr_fail:
movs r0, #0
vr_return:
add sp, #24
pop {r4, r5, r6, r7, pc}
'''


def assemble_writer(address=0x0830D000):
    return assemble_verified(WRITER,address,dict(output_extent=22<<16,converter=0x08309001))


def assemble_reader(address=0x0830D200):
    return assemble_verified(READER,address,dict(legacy_extents=22<<16|22,converter=0x08309001,decoder=0x08F09001))
