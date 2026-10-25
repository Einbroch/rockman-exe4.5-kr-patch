"""Standalone 64-byte replay wrapper. Caller-owned baseline, NOT a ROM ABI.

r0 compact64, r1 immutable baseline20, r2 selector0..39/B40/check41,
r3 descriptor(feed Thumb ptr, undo Thumb ptr, transitions ptr, deletions ptr).
Aligned valid regions and trusted descriptor required. Reject is atomic.
Persistent memory64; temporary stack384 plus call shim8 and backend52 =444.
"""

def program():
    lines=[];serial=0
    def emit(s):lines.extend(s.strip().splitlines())
    def reject(condition):
        nonlocal serial
        inverse={'eq':'ne','ne':'eq','hi':'ls','hs':'lo','lo':'hs'}[condition]
        serial+=1
        emit(f'b{inverse} guard_{serial}\nb fail\nguard_{serial}:')
    emit('''push {r4, r5, r6, r7, lr}
sub sp, #364
str r0, [sp, #340]
str r1, [sp, #344]
str r2, [sp, #348]
str r3, [sp, #352]
movs r4, r0
orrs r4, r1
orrs r4, r3
movs r5, #3
tst r4, r5''');reject('ne')
    emit('cmp r2, #41');reject('hi')
    # Checked nonoverlap of baseline and mutable compact state.
    emit('movs r4, r0\nadds r4, #64\ncmp r4, r0');reject('lo')
    emit('movs r5, r1\nadds r5, #20\ncmp r5, r1');reject('lo')
    emit('cmp r0, r5\nbhs regions_ok\ncmp r1, r4');reject('lo')
    emit('''regions_ok:
ldrb r4, [r0, #1]
cmp r4, #1''');reject('lo')
    emit('cmp r4, #8');reject('hi')
    emit('ldrb r5, [r0, #2]\ncmp r5, #56');reject('hi')
    emit('adds r0, #62\nldrb r5, [r0]\ncmp r5, #56');reject('hi')
    emit('ldrb r5, [r0, #1]\ncmp r5, #0');reject('ne')
    emit('ldrb r5, [r1, #1]\ncmp r5, r4');reject('ne')
    emit('ldrb r5, [r1]\ncmp r5, r4');reject('hi')
    emit('ldrb r6, [r1, #2]\ncmp r6, #0');reject('ne')
    emit('movs r6, #0\ncmp r5, #0\nbeq baseline_flag\nmovs r6, #1\nbaseline_flag:\nldrb r7, [r1, #3]\ncmp r7, r6');reject('ne')
    emit('''adds r1, #4
movs r6, #0
baseline_words:
ldrh r7, [r1]
cmp r6, r5
bhs baseline_empty
movs r4, #43
lsls r4, r4, #8
adds r4, #164
cmp r7, r4''');reject('hs')
    emit('b baseline_next\nbaseline_empty:\nmovs r4, #255\nlsls r4, r4, #8\nadds r4, #255\ncmp r7, r4');reject('ne')
    emit('''baseline_next:
adds r1, #2
adds r6, #1
cmp r6, #8
blo baseline_words
ldr r1, [sp, #344]
mov r0, sp
movs r2, #5
copy_baseline:
ldr r3, [r1]
str r3, [r0]
adds r0, #4
adds r1, #4
subs r2, #1
bne copy_baseline
movs r3, #0
mvns r3, r3
movs r2, #64
clear_history:
str r3, [r0]
adds r0, #4
subs r2, #1
bne clear_history
movs r4, #0
str r4, [sp, #356]
delete_loop:
ldr r0, [sp, #340]
adds r0, #62
ldrb r0, [r0]
ldr r4, [sp, #356]
cmp r4, r0
bhs keys_start
bl undo_call
cmp r0, #1''');reject('ne')
    emit('ldr r4, [sp, #356]\nadds r4, #1\nstr r4, [sp, #356]\nb delete_loop\nkeys_start:\nmovs r4, #0\nstr r4, [sp, #356]\nkeys_loop:\nldr r0, [sp, #340]\nldr r1, [sp, #356]\nbl get_key\nmovs r5, r0\nldr r0, [sp, #340]\nldrb r0, [r0, #2]\nldr r4, [sp, #356]\ncmp r4, r0\nbhs padding_key\ncmp r5, #40');reject('hs')
    emit('movs r1, r5\nbl feed_call\ncmp r0, #1');reject('ne')
    emit('b key_next\npadding_key:\ncmp r5, #0');reject('ne')
    emit('''key_next:
ldr r4, [sp, #356]
adds r4, #1
str r4, [sp, #356]
cmp r4, #56
blo keys_loop
mov r0, sp
ldr r1, [sp, #340]
movs r2, #5
compare_header:
ldr r3, [r0]
ldr r4, [r1]
cmp r3, r4''');reject('ne')
    emit('''adds r0, #4
adds r1, #4
subs r2, #1
bne compare_header
ldr r0, [sp, #348]
cmp r0, #41
beq success
ldr r0, [sp, #340]
add r1, sp, #276
movs r2, #16
copy_proposal:
ldr r3, [r0]
str r3, [r1]
adds r0, #4
adds r1, #4
subs r2, #1
bne copy_proposal
ldr r1, [sp, #348]
cmp r1, #40
beq do_back
ldr r0, [sp, #340]
ldrb r0, [r0, #2]
cmp r0, #56''');reject('hs')
    emit('bl feed_call\ncmp r0, #1');reject('ne')
    emit('add r0, sp, #276\nldrb r1, [r0, #2]\nldr r2, [sp, #348]\nbl put_key\nb finish_header\ndo_back:\nbl undo_call\ncmp r0, #1');reject('ne')
    emit('''add r0, sp, #276
ldrb r1, [r0, #2]
cmp r1, #0
beq back_baseline
subs r1, #1
movs r2, #0
bl put_key
b finish_header
back_baseline:
adds r0, #62
ldrb r1, [r0]
cmp r1, #56''');reject('hs')
    emit('''adds r1, #1
strb r1, [r0]
finish_header:
mov r0, sp
add r1, sp, #276
movs r2, #5
copy_header:
ldr r3, [r0]
str r3, [r1]
adds r0, #4
adds r1, #4
subs r2, #1
bne copy_header
add r0, sp, #276
ldr r1, [sp, #340]
movs r2, #16
commit:
ldr r3, [r0]
str r3, [r1]
adds r0, #4
adds r1, #4
subs r2, #1
bne commit
success:
movs r0, #1
b return
fail:
movs r0, #0
return:
add sp, #364
pop {r4, r5, r6, r7, pc}
feed_call:
push {r4, lr}
ldr r4, [sp, #360]
ldr r7, [r4]
ldr r2, [r4, #8]
add r0, sp, #8
movs r3, #69
lsls r3, r3, #2
bl call_reg
pop {r4, pc}
undo_call:
push {r4, lr}
ldr r4, [sp, #360]
ldr r7, [r4, #4]
ldr r2, [r4, #12]
add r0, sp, #8
movs r1, #69
lsls r1, r1, #2
bl call_reg
pop {r4, pc}
call_reg:
bx r7
get_key:
lsls r2, r1, #1
adds r1, r1, r2
lsls r1, r1, #1
movs r2, #7
ands r2, r1
lsrs r1, r1, #3
adds r0, #20
adds r0, r0, r1
ldrb r1, [r0]
ldrb r3, [r0, #1]
lsls r3, r3, #8
orrs r1, r3
lsrs r1, r1, r2
movs r0, #63
ands r0, r1
bx lr
put_key:
push {r4, r5, lr}
lsls r3, r1, #1
adds r1, r1, r3
lsls r1, r1, #1
movs r4, #7
ands r4, r1
lsrs r1, r1, #3
adds r0, #20
adds r0, r0, r1
movs r5, #63
lsls r5, r5, r4
lsls r2, r2, r4
ldrb r1, [r0]
ldrb r3, [r0, #1]
lsls r3, r3, #8
orrs r1, r3
bics r1, r5
orrs r1, r2
strb r1, [r0]
lsrs r1, r1, #8
strb r1, [r0, #1]
pop {r4, r5, pc}''')
    return '\n'.join(lines)+'\n'

CODE=program()

def assemble(address=0x08002000):
    # Existing dialogue verifier deliberately accepts only two-byte opcodes.
    # This wrapper additionally uses ARMv4T's two-halfword BL, never BLX/Thumb-2.
    from extended_dialogue import Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB,KS_VERSION,CS_VERSION
    if (KS_VERSION,CS_VERSION)!=('0.9.2','5.0.7'):raise ValueError('toolchain drift')
    header='.syntax unified\n.cpu arm7tdmi\n.thumb\n'
    source=[s for s in CODE.splitlines() if s and not s.endswith(':')]
    size=sum(4 if s.startswith('bl ') else 2 for s in source)
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    blob=bytes(ks.asm(header+CODE,address)[0])
    instructions=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(blob,address))
    if len(blob)!=size or len(instructions)!=len(source):raise ValueError('instruction extent')
    for i,s in zip(instructions,source):
        if i.size!=(4 if s.startswith('bl ') else 2):raise ValueError('unexpected wide opcode')
        if i.size==4:
            lo=int.from_bytes(i.bytes[:2],'little');hi=int.from_bytes(i.bytes[2:],'little')
            if i.mnemonic!='bl' or lo&0xf800!=0xf000 or hi&0xf800!=0xf800:raise ValueError('not ARMv4T BL')
        if bytes(ks.asm(header+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('placement roundtrip')
        if s.split()[0] in {'b','bl','beq','bne','bhs','blo','bhi','bls'}:
            target=int(i.op_str.lstrip('#'),0)
            if not address<=target<address+size or target%2:raise ValueError('branch target')
    return blob,dict(isa='ARMv4T Thumb-1 including BL; no BLX/Thumb-2',assembler=KS_VERSION,disassembler=CS_VERSION,address=address,code_bytes=size,final_placement_roundtrip=True,instructions=[dict(address=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in instructions])
