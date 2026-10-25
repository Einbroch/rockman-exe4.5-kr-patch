"""A0 loaded-payload identity selector; independent of mutable time/sub slots."""
import struct
from extended_dialogue import assemble_verified
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from verify_tpi_index import lz77_decompress

def source_population(source,selected_archives):
    if struct.unpack_from('<I',source,0x53780)[0]!=0x08053898:raise ValueError('035 A0 source population')
    pool=[]
    for sub in range(4):
        table=struct.unpack_from('<I',source,0x53898+4*sub)[0]-0x08000000
        if table!=0x538A8+32*sub:raise ValueError('035 A0 subtable')
        for slot in range(7):
            off=struct.unpack_from('<I',source,table+4*slot)[0]-0x08000000;payload,_=lz77_decompress(source,off)
            if payload[:2]!=b'\xfe\x01':raise ValueError('035 A0 native255 header')
            pool.append(dict(archive=f'{off:X}',sub=sub,slot=slot,payload=payload))
    selected=[r for r in pool if r['archive'] in selected_archives]
    if len(selected)!=len(selected_archives) or len(set(selected_archives))!=9:raise ValueError('035 exact nine selected sources')
    for r in selected:
        for other in pool:
            if r['archive']==other['archive']:continue
            n=min(len(r['payload']),len(other['payload']))
            if r['payload'][:n]==other['payload'][:n]:raise ValueError('035 ambiguous full/prefix native source identity')
    return pool

def wrap(source,address,previous_entry,table):
    if any(type(v) is not int or v&3 for v in (address,table)) or not 0x08000000<=table<table+9*16<=address<0x0A000000 or not 0x08000000<=previous_entry<0x0A000000:raise ValueError('035 NPC descriptor/code placement')
    call=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(source[0x4F76E:0x4F772],0x0804F76E))
    if len(call)!=1 or call[0].mnemonic!='bl' or call[0].size!=4 or call[0].op_str!='#0x804fb4c' or struct.unpack_from('<I',source,0x4F78C)[0]!=0x02039800:raise ValueError('035 NPC source reader')
    caller_lr=(call[0].address+call[0].size)|1
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
ldr r3,descriptors
movs r7,#9
candidate:
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
ldr r4,[r3,#0]
str r4,[sp,#0]
b fallback
next:
adds r3,#16
subs r7,#1
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''
    blob,proof=assemble_verified(code,address,dict(caller=caller_lr,root=0x02039800,descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,source_caller=0x0804F76E,caller_lr=caller_lr,scene_major=0xA0,native_root=0x02039800,
        descriptor_slots=9,comparison='every native payload byte; source-population prefix ambiguity rejected',
        mutable_selector_or_sub_area_used=False,persistent_ram_bytes=0,stack_bytes=32,
        original_compressed_loader_and_RAM_extent_retained=True,analysis_only=True,runtime_tested=False)
