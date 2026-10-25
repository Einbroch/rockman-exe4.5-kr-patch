"""040 three-domain full-native selector; assembly only, no ROM writer."""
from extended_dialogue import assemble_verified
from consumer_links040_v1 import contracts,CLASSES

FIELDS=['clone','native_copy','native_length','script_count','root','caller_lr','outer_lr']


def wrap(source,address,previous_entry,table,count):
    abi=contracts(source)
    if type(count)is not int or not 1<=count<=255 or any(type(x)is not int or x&3 for x in (address,table)) or not 0x08000000<=table<table+count*28<=address<0x0A000000 or not 0x08000000<=previous_entry<0x0A000000:raise ValueError('040 descriptor/code placement')
    code='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
mov r2,lr
ldr r3,comm_caller
cmp r2,r3
beq shared_root
ldr r3,normal_caller
cmp r2,r3
beq shared_root
ldr r3,bbs_caller
cmp r2,r3
bne fallback
ldr r3,bbs_root
cmp r0,r3
bne fallback
b script_gate
shared_root:
ldr r3,shared
cmp r0,r3
bne fallback
script_gate:
lsrs r2,r1,#8
bne fallback
mov r2,lr
ldr r3,comm_caller
cmp r2,r3
bne table_gate
ldr r2,[sp,#48]
ldr r3,comm_outer
cmp r2,r3
bne fallback
table_gate:
ldr r3,descriptors
movs r7,#COUNT
candidate:
mov r2,lr
ldr r4,[r3,#20]
cmp r2,r4
bne next
ldr r4,[r3,#16]
cmp r0,r4
bne next
ldr r2,[sp,#4]
ldr r4,[r3,#12]
cmp r2,r4
bhs next
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
adds r3,#28
subs r7,#1
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''.replace('COUNT',str(count))
    blob,proof=assemble_verified(code,address,dict(comm_caller=CLASSES['communication-help']['caller_lr'],normal_caller=CLASSES['compressed-normal']['caller_lr'],bbs_caller=CLASSES['battle-BBS-trial']['caller_lr'],bbs_root=CLASSES['battle-BBS-trial']['root'],shared=CLASSES['communication-help']['root'],comm_outer=CLASSES['communication-help']['outer_lr'],descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,contracts=abi,descriptor_fields=FIELDS,descriptor_bytes=28,descriptor_slots=count,persistent_ram_bytes=0,scene_dereferenced=False,stack_bytes=32,predecessor_contract='Originalr3 on stack -> direct039 wrapper entry; not installation stub',runtime_tested=False)
