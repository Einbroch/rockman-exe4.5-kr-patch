"""Selected NEW-format calendar stage -> bounded text-pool slot, CPU only.

Only proposed for caller0803104E, not global rawE5 copier replacement.
r0=02026281 (native source after marker), r1=02026080/26100/26180.
Validate entire22byte cap10 record at source-1 using import helper on stack,
then copy marker AND payload/terminator22bytes. Rejection is atomic return0.
Return22 on success; caller overwrites r0 after call. r4..r11/SP preserved.
Own96 + import124 =220 stack. Selected-format premise must be established
by coordinated init/confirm/default/import writers before ROM installation.
No legacy detection, persistent-record or redisplay implementation here.
"""
from extended_dialogue import assemble_verified

CODE='''push {r4, r5, r6, r7, lr}
sub sp, #76
movs r4, r0
movs r5, r1
ldr r6, source
cmp r4, r6
bne tr_fail
ldr r6, destination
cmp r5, r6
beq tr_validate
adds r6, #128
cmp r5, r6
beq tr_validate
adds r6, #128
cmp r5, r6
bne tr_fail
tr_validate:
subs r4, #1
movs r0, r4
mov r1, sp
ldr r2, extents
movs r3, #10
ldr r6, importer
mov lr, pc
bx r6
cmp r0, #0
beq tr_fail
movs r3, #0
tr_copy:
ldrb r2, [r4, r3]
strb r2, [r5, r3]
adds r3, #1
cmp r3, #22
blo tr_copy
movs r1, r5
movs r0, #22
b tr_return
tr_fail:
movs r0, #0
tr_return:
add sp, #76
pop {r4, r5, r6, r7, pc}
'''

def assemble(address=0x08306000):
    return assemble_verified(CODE,address,dict(source=0x02026281,destination=0x02026080,extents=76<<16|22,importer=0x08F05001))

# Replaces success-only caller suffix31052..3105E as one coordinated change.
# Failure follows its original cancel state3C/import flag1; never proceeds to
# confirmation state24 with stale pool data. No explanatory dialog is added.
FINALIZE='''cmp r0, #22
beq fin_success
movs r0, #60
movs r1, #1
b fin_write
fin_success:
movs r0, #36
movs r1, #0
fin_write:
strb r0, [r5, #1]
movs r0, #0
strh r0, [r5, #2]
strb r1, [r5, #10]
bx lr
'''

def assemble_finalizer(address=0x08306100):
    return assemble_verified(FINALIZE,address,{})
