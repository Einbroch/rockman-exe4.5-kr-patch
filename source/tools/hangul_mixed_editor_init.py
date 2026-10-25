"""Parameters16 -> editor96 staging candidate, NOT source ABI/hook.

Parameters: four LE uint32 (capacityFlag, heading, destination, callerValue).
r0 params16,r1 output96,r2 inputAvailable(low16)|outputAvailable(high16),r3=0.
Return1/0, bytealignment/r4..r11/SP preserved, stack116. Supports cap1..10
and80|cap; preserves original initializer UI16, relocates destination to+16,
emptycompact76 at+20. Old pointer-based consumers cannot use this layout.
Destination preserved as opaque pointer, never dereferenced. Caller owns
extents and disjoint stack. No adopted RAM layout, record or save support.
"""
import struct
from extended_dialogue import assemble_verified
from hangul_mixed_replay_state import MixedReplay, editor_candidate


def initialize(params):
    if type(params)!=bytes or len(params)!=16: raise ValueError('init parameters')
    rawcap,heading,destination,value=struct.unpack('<4I',params)
    if rawcap not in tuple(range(1,11))+tuple(range(129,139)): raise ValueError('init capacity')
    cap=rawcap&127;ui=bytearray(16)
    ui[4]=cap;ui[5]=heading&255;ui[9]=int(rawcap>=128);ui[10]=value&255;ui[14]=1
    return editor_candidate(bytes(ui),destination,MixedReplay(cap).serialize())


CODE='''push {r4, r5, r6, r7, lr}
sub sp, #96
movs r4, r0
movs r5, r1
cmp r3, #0
bne init_fail
lsls r0, r2, #16
lsrs r0, r0, #16
cmp r0, #16
blo init_fail
lsrs r0, r2, #16
cmp r0, #96
blo init_fail
movs r0, r4
adds r0, #16
cmp r0, r4
blo init_fail
movs r1, r5
adds r1, #96
cmp r1, r5
blo init_fail
cmp r4, r1
bhs init_disjoint
cmp r5, r0
blo init_fail
init_disjoint:
ldrb r0, [r4, #1]
ldrb r1, [r4, #2]
orrs r0, r1
ldrb r1, [r4, #3]
orrs r0, r1
cmp r0, #0
bne init_fail
ldrb r6, [r4]
movs r0, #127
ands r0, r6
cmp r0, #1
blo init_fail
cmp r0, #10
bhi init_fail
movs r7, r0
mov r3, sp
movs r0, #0
movs r1, #0
init_zero:
strb r1, [r3, r0]
adds r0, #1
cmp r0, #96
blo init_zero
strb r7, [r3, #4]
ldrb r0, [r4, #4]
strb r0, [r3, #5]
lsrs r6, r6, #7
strb r6, [r3, #9]
ldrb r0, [r4, #12]
strb r0, [r3, #10]
movs r0, #1
strb r0, [r3, #14]
movs r0, #0
init_destination:
movs r1, r0
adds r1, #8
ldrb r1, [r4, r1]
movs r2, r0
adds r2, #16
strb r1, [r3, r2]
adds r0, #1
cmp r0, #4
blo init_destination
strb r7, [r3, #20]
movs r0, #240
strb r0, [r3, #21]
movs r0, #23
movs r1, #255
init_empty_words:
strb r1, [r3, r0]
adds r0, #1
cmp r0, #43
blo init_empty_words
movs r0, #95
movs r1, #176
strb r1, [r3, r0]
movs r0, #0
init_copy:
ldrb r1, [r3, r0]
strb r1, [r5, r0]
adds r0, #1
cmp r0, #96
blo init_copy
movs r0, #1
b init_return
init_fail:
movs r0, #0
init_return:
add sp, #96
pop {r4, r5, r6, r7, pc}
'''


def assemble(address=0x08800000):
    return assemble_verified(CODE,address,{})
