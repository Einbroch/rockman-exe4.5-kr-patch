"""Caller-selected mixed-record reentry adapter; CPU candidate, no ROM hook.

Entry r0=record, new editor96 already initialized. Source must match editor+16,
be bounded EWRAM and disjoint from the ENTIRE editor96 (not just compact76).
Return1/0; failure preserves editor. r4..r11/SP preserved. Own8+nested124=132
stack. Original caller ignores failure: rejection UX is NOT established.
Never detects format by marker. All callers must explicitly select this format.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, lr}
ldr r1, editor
ldr r2, [r1, #16]
cmp r0, r2
bne import_fail
ldrb r3, [r1, #4]
cmp r3, #1
blo import_fail
cmp r3, #10
bhi import_fail
lsls r2, r3, #1
adds r2, #2
ldr r4, ewram_start
cmp r0, r4
blo import_fail
adds r4, r0, r2
cmp r4, r0
blo import_fail
ldr r2, ewram_end
cmp r4, r2
bhi import_fail
cmp r4, r1
bls import_disjoint
movs r2, r1
adds r2, #96
cmp r0, r2
blo import_fail
import_disjoint:
lsls r2, r3, #1
adds r2, #2
ldr r4, output_extent
orrs r2, r4
adds r1, #20
ldr r4, helper
mov lr, pc
bx r4
pop {r4, pc}
import_fail:
movs r0, #0
pop {r4, pc}
'''

def assemble(address=0x08302000, editor=0x0200FC40, helper=0x08F05001):
    if editor%4 or not 0x02000000<=editor<=0x0203FFA0:
        raise ValueError('aligned caller-owned EWRAM editor96')
    if not helper&1 or not 0x08000000<=helper<0x0A000000:
        raise ValueError('Thumb ROM helper')
    return assemble_verified(CODE,address,dict(editor=editor,helper=helper,
        ewram_start=0x02000000,ewram_end=0x02040000,output_extent=76<<16))
