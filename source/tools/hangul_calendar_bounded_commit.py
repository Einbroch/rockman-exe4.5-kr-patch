"""Explicit NEW cap10 canonical stage -> existing calendar name field.

CPU candidate only. Stage02026280 is assumed owned for this selected session,
NOT detected from marker nor adopted as universal canonical/save ABI.
Field must equal ctx02014DD0+2C's record+10, record in255 stride32 arena.
Validate entire22bytes through importer before copying; no partial writes.
Own96+import124=220; adapters add8, outer caller push4 adds4.
Two coordinated adapters skip success metadata on failure; no global copier.
"""
from extended_dialogue import assemble_verified

COPY='''push {r4, r5, r6, r7, lr}
sub sp, #76
movs r5, r1
ldr r6, context
ldr r6, [r6, #44]
movs r7, r6
adds r7, #10
cmp r5, r7
bne bc_fail
ldr r7, arena
cmp r6, r7
blo bc_fail
subs r6, r6, r7
ldr r7, arena_bytes
cmp r6, r7
bhs bc_fail
movs r7, #31
tst r6, r7
bne bc_fail
ldr r4, canonical
movs r0, r4
mov r1, sp
ldr r2, extents
movs r3, #10
ldr r6, importer
mov lr, pc
bx r6
cmp r0, #0
beq bc_fail
movs r3, #0
bc_copy:
ldrb r2, [r4, r3]
strb r2, [r5, r3]
adds r3, #1
cmp r3, #22
blo bc_copy
movs r0, #22
b bc_return
bc_fail:
movs r0, #0
bc_return:
add sp, #76
pop {r4, r5, r6, r7, pc}
'''

def assemble(address=0x08308000):
    return assemble_verified(COPY,address,dict(context=0x02014DD0,arena=0x020011F0,arena_bytes=255*32,
        canonical=0x02026280,extents=76<<16|22,importer=0x08F05001))

# Pool-route BL32F06 replaces only native copier; native metadata37366 follows.
# Direct-stage route replaces3354A..3355E together: validate BEFORE success sound.
# No source instructions moved. Success resumes original3355E metadata selection.
def assemble_adapter(direct=False,address=None):
    if address is None: address=0x08308200 if direct else 0x08308100
    pre='''ldr r1, context
ldr r1, [r1, #44]
adds r1, #10
''' if direct else ''
    success='''movs r0, #128
ldr r4, sound
mov lr, pc
bx r4
''' if direct else ''
    code='''push {r4, lr}
'''+pre+'''ldr r4, copier
mov lr, pc
bx r4
cmp r0, #22
bne ca_fail
'''+success+'''pop {r4, pc}
ca_fail:
movs r0, #2
strb r0, [r5, #8]
movs r0, #1
strb r0, [r5, #6]
pop {r4}
add sp, #4
ldr r3, failure
bx r3
'''
    literals=dict(context=0x02014DD0,copier=0x08308001,failure=0x0803359F if direct else 0x08032F1B)
    if direct: literals['sound']=0x08000535
    return assemble_verified(code,address,literals)
