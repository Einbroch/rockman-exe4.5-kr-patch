"""Finite A0 NPC reader proposal; preserves original compressed RAM payloads."""
import struct
from extended_dialogue import assemble_verified
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def wrap(source,address,previous_entry,table):
    if any(type(v) is not int or v&3 for v in (address,table)) or not 0x08000000<=table<table+32*16<=address<0x0A000000 or not 0x08000000<=previous_entry<0x0A000000:raise ValueError('035 NPC descriptor/code placement')
    call=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(source[0x4F76E:0x4F772],0x0804F76E))
    if len(call)!=1 or call[0].mnemonic!='bl' or call[0].size!=4 or call[0].op_str!='#0x804fb4c':raise ValueError('035 NPC caller')
    if struct.unpack_from('<I',source,0x4F78C)[0]!=0x02039800 or source[0x2E42C:0x2E432]!=bytes.fromhex('0149c87d f746'.replace(' ','')):raise ValueError('035 NPC root/selector producer')
    clock=struct.unpack_from('<I',source,0x2E434)[0]
    if clock!=0x02003D40:raise ValueError('035 NPC native selector context')
    code='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
mov r2,lr
ldr r3,caller
cmp r2,r3
bne fallback
ldr r3,root
cmp r0,r3
bne fallback
lsrs r2,r1,#8
bne fallback
cmp r1,#254
bgt fallback
mov r2,r10
ldr r2,[r2,#64]
ldrb r3,[r2,#4]
cmp r3,#160
bne fallback
ldrb r2,[r2,#5]
cmp r2,#3
bgt fallback
lsls r2,r2,#3
ldr r3,clock
ldrb r3,[r3,#23]
cmp r3,#6
bgt fallback
adds r2,r2,r3
lsls r2,r2,#4
ldr r3,descriptors
adds r3,r3,r2
ldr r4,[r3,#0]
cmp r4,#0
beq fallback
ldr r5,[r3,#4]
ldr r6,[r3,#8]
cmp r6,#0
beq fallback
movs r7,r0
compare:
ldrb r2,[r7]
ldrb r3,[r5]
cmp r2,r3
bne fallback
adds r7,#1
adds r5,#1
subs r6,#1
bne compare
str r4,[sp,#0]
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''
    blob,proof=assemble_verified(code,address,dict(caller=0x0804F76F,root=0x02039800,clock=clock,descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,source_caller=0x0804F76E,caller_lr=0x0804F76F,scene_major=0xA0,native_root=0x02039800,
        descriptor_slots=32,sub_area_count=4,selector_range=[0,6],selector_address=clock+23,
        comparison='every native payload byte, not prefix/hash',persistent_ram_bytes=0,stack_bytes=32,
        original_compressed_loader_and_RAM_extent_retained=True,analysis_only=True,runtime_tested=False)
