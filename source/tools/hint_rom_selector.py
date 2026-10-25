"""Full-native-identity hint wrapper; development runtime verification required."""
from extended_dialogue import assemble_verified
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def wrap(source,address,previous_entry,table,*,scene=0xA3):
    if type(scene) is not int or scene not in (0xA3,0xB0):raise ValueError('Unestablished hint scene')
    if any(x&3 for x in (address,table)) or not 0x08000000<=table<table+23*16<=address<0x0A000000 or not 0x08000000<=previous_entry<0x0A000000:raise ValueError('PoC descriptor/code placement')
    call=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(source[0x4F802:0x4F806],0x0804F802))
    if len(call)!=1 or call[0].mnemonic!='bl' or call[0].size!=4 or call[0].op_str!='#0x804fb4c':raise ValueError('Native hint caller')
    if source[0xCEC:0xCF4]!=bytes.fromhex('5046006c4078f746'):raise ValueError('Native Navi provider')
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
cmp r3,#163
bne fallback
ldrb r2,[r2,#1]
cmp r2,#22
bgt fallback
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
    code=code.replace('cmp r3,#163\n',f'cmp r3,#{scene}\n')
    blob,proof=assemble_verified(code,address,dict(caller=0x0804F807,root=0x0203D800,descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,source_caller=0x0804F802,caller_lr=0x0804F807,scene_major=scene,native_root=0x0203D800,descriptor_slots=23,comparison='every native payload byte, not a prefix/hash',persistent_ram_bytes=0,stack_bytes=32,analysis_only=True,runtime_tested=False)
