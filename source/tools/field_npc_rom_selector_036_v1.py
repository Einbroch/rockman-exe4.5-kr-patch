"""036 proposed scene+full-native-identity reader; no product ROM writer.

The low byte of r7 counts descriptors; its upper bytes retain the scene read
once on entry. It is restored along with every other low register on exit.
"""
import struct
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from extended_dialogue import assemble_verified
from verify_tpi_index import lz77_decompress

SCENE_TABLES={0xA0:0x53898,0xA1:0x53938,0xA3:0x53A78}


def source_population(source,selected):
    pool=[]
    for scene,expected in SCENE_TABLES.items():
        top=0x53700+(scene-0x80)*4
        if struct.unpack_from('<I',source,top)[0]!=0x08000000+expected:raise ValueError('036 scene table applicability')
        for sub in range(4):
            table=struct.unpack_from('<I',source,expected+sub*4)[0]-0x08000000
            if table!=expected+16+sub*32:raise ValueError('036 native subtable extent')
            for slot in range(7):
                off=struct.unpack_from('<I',source,table+slot*4)[0]-0x08000000
                payload,_=lz77_decompress(source,off)
                if payload[:2]!=b'\xfe\x01':raise ValueError('036255-script source header')
                pool.append(dict(archive=f'{off:X}',scene=scene,sub=sub,slot=slot,pointer=table+slot*4,payload=payload))
    for archive,scene in selected.items():
        found=[r for r in pool if r['archive']==archive and r['scene']==scene]
        if len(found)!=1:raise ValueError('036 selected native lookup uniqueness')
        r=found[0]
        for other in pool:
            if other['scene']!=scene or other['archive']==archive:continue
            n=min(len(r['payload']),len(other['payload']))
            if r['payload'][:n]==other['payload'][:n]:raise ValueError('036 native identity ambiguous within scene')
    return pool


def wrap(source,address,previous_entry,table,count):
    if type(count) is not int or not 1<=count<=255:raise ValueError('036 descriptor counter range')
    if any(type(x) is not int or x&3 for x in (address,table)) or not 0x08000000<=table<table+count*16<=address<0x0A000000 or not 0x08000000<=previous_entry<0x0A000000:raise ValueError('036 code/descriptor placement')
    call=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(source[0x4F76E:0x4F772],0x0804F76E))
    if len(call)!=1 or call[0].size!=4 or call[0].mnemonic!='bl' or call[0].op_str!='#0x804fb4c' or struct.unpack_from('<I',source,0x4F78C)[0]!=0x02039800:raise ValueError('036 source caller/root contract')
    caller=(call[0].address+call[0].size)|1
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
lsls r7,r3,#8
adds r7,#COUNT
ldr r3,descriptors
candidate:
lsrs r2,r7,#8
ldr r4,[r3,#12]
cmp r2,r4
bne next
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
lsls r2,r7,#24
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''.replace('COUNT',str(count))
    blob,proof=assemble_verified(code,address,dict(caller=caller,root=0x02039800,descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,source_caller=call[0].address,caller_lr=caller,native_root=0x02039800,descriptor_slots=count,descriptor_bytes=16,descriptor_fields=['clone','native_copy','native_length','scene'],comparison='scene byte then every native payload byte',scene_read_once=True,mutable_time_or_sub_used=False,persistent_ram_bytes=0,stack_bytes=32,predecessor_contract='Predecessor wrapper entry expects original r3 on stack, not its installation stub',analysis_only=True,runtime_tested=False)
