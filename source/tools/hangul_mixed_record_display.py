"""Caller-selected mixed fixed record -> display stream, NOT save detection.

r0 record,r1 stream,r2 inputAvailable low16|outputAvailable high16,r3 cap1..10.
Return byte length inclE5 or0; failure no external write. Byte alignment,
r4..r11/SP preserved; own44+display36=80 stack. Entire declared output extent
must be disjoint from consumed record. No table/history/import76 needed.
Caller selects format and owns buffers/stack; original normalize is bypassed.
"""
import struct
from hangul_mixed_display import CODE as DISPLAY,display
from hangul_mixed_cache_bridge import scoped
from hangul_mixed_record import unpack_selected_record,surface_from_compact
from hangul_mixed_keyedit_thumb import assemble as assemble_code

def stream(record,cap):
    return display(surface_from_compact(unpack_selected_record(record,cap)),1)

CODE='''push {r4, r5, r6, r7, lr}
sub sp, #24
movs r4, r0
movs r5, r1
movs r6, r3
lsrs r7, r2, #16
cmp r6, #1
blo rd_early_fail
cmp r6, #10
bhi rd_early_fail
lsls r0, r2, #16
lsrs r0, r0, #16
lsls r1, r6, #1
adds r1, #2
cmp r0, r1
blo rd_early_fail
adds r0, r4, r1
cmp r0, r4
blo rd_early_fail
adds r2, r5, r7
cmp r2, r5
blo rd_early_fail
cmp r4, r2
bhs rd_disjoint
cmp r5, r0
blo rd_early_fail
rd_disjoint:
ldrb r0, [r4]
subs r0, #128
cmp r0, #1
blo rd_early_fail
cmp r0, r6
bhi rd_early_fail
mov r3, sp
strb r0, [r3]
strb r6, [r3, #1]
movs r0, #0
strb r0, [r3, #2]
movs r0, #255
strb r0, [r3, #3]
subs r1, #1
ldrb r2, [r4, r1]
cmp r2, #229
bne rd_early_fail
movs r1, #4
rd_pad:
strb r0, [r3, r1]
adds r1, #1
cmp r1, #24
blo rd_pad
lsls r2, r6, #1
movs r1, #0
rd_words:
adds r0, r1, #1
ldrb r0, [r4, r0]
adds r1, #4
strb r0, [r3, r1]
subs r1, #3
cmp r1, r2
blo rd_words
b rd_render
rd_early_fail:
b rd_fail
rd_render:
mov r0, sp
movs r1, r5
movs r2, r7
movs r3, #1
bl rd_display
b rd_return
rd_fail:
movs r0, #0
rd_return:
add sp, #24
pop {r4, r5, r6, r7, pc}
rd_display:
'''+scoped(DISPLAY,'rd_d_')

def assemble(address=0x08F09000):
    return assemble_code(address,CODE)
