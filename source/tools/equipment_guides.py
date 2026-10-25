"""Isolated guide helper: normal call ABI, source-pool identity based routing."""
from build_visibility_poc import sha
from extended_dialogue import assemble_verified
from folder_labels import validate_header_path

INSTALL=0x3C478
SCOPE={'source_bytes':625,'pointers':[0x3C5BC,0x3C5F0,0x3C5F4],'compressed':True,
 'consumer':'normal-dialogue','max_literal_rows':2,'max_line_advance':132,
 'complete_literal_scope':False,'literal_scripts':[60,61,62],'script_count':76}

def validate(source):
    validate_header_path(source)
    if source[INSTALL:INSTALL+16]!=bytes.fromhex('00b5011c3c31024813f099f900bd0000') or source[0xCEC:0xCF4]!=bytes.fromhex('5046006c4078f746'):raise ValueError('native guide/query instructions')
    targets=[]
    for i in range(23):
        if int.from_bytes(source[0x3C5BC+i*4:0x3C5C0+i*4],'little')==0x086E1068:targets.append(i)
    if targets!=[0,13,14]:raise ValueError('source guide pool selection')
    return targets

def construct(source,appended,clone_offset,roll_clone_offset=None):
    targets=validate(source);out=bytearray(appended);out.extend(b'\xff'*(-len(out)%4));hook=len(source)+len(out);address=0x08000000+hook
    # Installation saves r3 before using it for the long branch. The hook
    # restores it, recreates original push{lr}/r1=selection+60, preserves r2/r3,
    # then sets the original BL return address and tail-jumps to normal entry.
    # r12 is normal-call scratch; r4..r11/SP/caller LR and source RAM retained.
    code='''pop {r3}
push {lr}
movs r1,r0
adds r1,#60
push {r2,r3}
mov r0,r10
ldr r0,[r0,#64]
ldrb r0,[r0,#1]
cmp r0,#0
beq translated
cmp r0,#13
beq translated
cmp r0,#14
beq translated
ldr r0,native_root
b resume
translated:
ldr r0,korean_root
resume:
ldr r2,native_call
mov r12,r2
ldr r2,native_return
mov lr,r2
pop {r2,r3}
mov pc,r12'''
    literals={'native_root':0x0202BA7C,'korean_root':0x08000000+clone_offset,'native_call':0x0804F7B6,'native_return':0x0803C485}
    if roll_clone_offset is not None:
        if int.from_bytes(source[0x3C5C0:0x3C5C4],'little')!=0x086E12DC or roll_clone_offset%4 or roll_clone_offset<len(source):raise ValueError('Roll source pool/clone boundary')
        code=code.replace('ldr r0,native_root','cmp r0,#1\nbeq roll_translated\nldr r0,native_root').replace('resume:\n','b resume\nroll_translated:\nldr r0,roll_root\nresume:\n')
        literals['roll_root']=0x08000000+roll_clone_offset
    payload,record=assemble_verified(code,address,literals)
    out.extend(payload)
    stub,install=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,{'target':address|1})
    if len(stub)!=12 or source[0x3C484:0x3C488]!=bytes.fromhex('00bd0000'):raise ValueError('guide source return/install extent')
    metadata={'hook_offset':hook,'hook_bytes':len(payload),'install_offset':INSTALL,'install_bytes':12,'clone_offset':clone_offset,'selected_navi_indices':targets,'source_dialogue_root_unchanged':True,'original_return':0x0803C485,'machine_code':[record,install],'policy':'Only helper0803C478 for guide60..62; Navi0/13/14 use identical original source pool translated clone; all other Navi retain originalRAM; no expansion of RAM, no shared loader changes','runtime':'pending exact-ROM root/font/ABI/screens'}
    if roll_clone_offset is not None:
        metadata.update(roll_clone_offset=roll_clone_offset,selected_navi_indices=[0,1,13,14],policy='Only helper0803C478 guide60..62; Navi0/13/14 Rockman clone, Navi1 separate Roll clone; all others originalRAM; no RAM or shared loader changes')
    return bytes(out),[(INSTALL,stub,'isolated equipment guide ROM selector')],metadata
