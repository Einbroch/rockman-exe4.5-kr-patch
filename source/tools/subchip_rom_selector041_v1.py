"""041 subchip-only full-native ROM selector component, no ROM writer.

Entry is common4FB4C's existing 12-byte push-r3 trampoline ABI. Return is
the exact040 wrapper entry with originalr3 pushed. Only selected r0 root
may change. r1..r14/stack/native RAM preserved; NZCV is native-init scratch.
"""
from extended_dialogue import assemble_verified

FIELDS=['clone','native_copy','native_length','script_count','selected_script_mask']


def wrap(address,previous_entry,table,count):
    if type(count)is not int or not 1<=count<=255 or any(type(x)is not int or x&3 for x in (address,table)) or not 0x08000000<=table<table+count*20<=address<0x0A000000 or not 0x08000000<=previous_entry<address:raise ValueError('041 subchip descriptor/code placement')
    code='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
ldr r3,native_root
cmp r0,r3
bne fallback
mov r2,lr
ldr r3,native_caller
cmp r2,r3
bne fallback
ldr r2,[sp,#48]
ldr r3,native_outer
cmp r2,r3
bne fallback
lsrs r2,r1,#5
bne fallback
ldr r3,descriptors
movs r7,#COUNT
candidate:
ldr r1,[sp,#4]
ldr r4,[r3,#12]
cmp r1,r4
bhs next
movs r2,#1
lsls r2,r1
ldr r4,[r3,#16]
tst r2,r4
beq next
movs r1,r0
ldr r5,[r3,#4]
ldr r6,[r3,#8]
compare:
ldrb r2,[r1]
ldrb r4,[r5]
cmp r2,r4
bne next
adds r1,#1
adds r5,#1
subs r6,#1
bne compare
ldr r4,[r3]
str r4,[sp]
b fallback
next:
adds r3,#20
subs r7,#1
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''.replace('COUNT',str(count))
    blob,proof=assemble_verified(code,address,dict(native_root=0x02026C00,native_caller=0x0804F7BD,native_outer=0x08041D8F,descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,descriptor_fields=FIELDS,descriptor_bytes=20,descriptor_slots=count,persistent_ram_bytes=0,stack_bytes=32,script_gate='uint5 input then per-descriptor selected mask AND script_count',native_identity='all native decoded bytes, not table header only',predecessor_contract='Original r3 on stack -> unchanged040 wrapper entry, never its installation stub',runtime_tested=False,product_integrated=False)
