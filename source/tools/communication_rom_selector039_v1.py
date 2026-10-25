"""Precisely typed communication reader extension; assembly only, no ROM writer.

The loader and the shared 4493C destination literal remain untouched. Original
4F7B6 owns its preset copy. The saved outer LR is read only after early gates.
"""
import struct
from collections import defaultdict
from extended_dialogue import assemble_verified, Cs, CS_ARCH_ARM, CS_MODE_THUMB
from verify_tpi_index import lz77_decompress

FIELDS = ['clone', 'native_copy', 'native_length', 'script_count']
ROOT_ADDRESS = 0x02024000
INNER_LR = 0x0804F7BD
OUTER_LR = 0x080448C7


def contracts(source):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    expected = {
        0x448BC: [('push','{lr}'),('adds','r1, r0, #0'),('ldr','r0, [pc, #0x78]'),('bl','#0x804f7b6'),('pop','{pc}')],
        0x4F7B6: [('push','{r4, r5, r6, r7, lr}'),('bl','#0x804fb4c'),('ldr','r0, [pc, #0xc]'),('mov','r1, sl'),('ldr','r1, [r1, #0x2c]'),('adds','r1, #0x68'),('movs','r2, #8'),('bl','#0x8000956'),('pop','{r4, r5, r6, r7, pc}')],
    }
    for at, seq in expected.items():
        length = 12 if at == 0x448BC else 22
        ins = list(decoder.disasm(source[at:at+length], 0x08000000+at))
        if [(i.mnemonic,i.op_str) for i in ins] != seq or sum(i.size for i in ins)!=length:
            raise ValueError(('039 native nested ABI applicability',hex(at),[(i.mnemonic,i.op_str) for i in ins]))
    if struct.unpack_from('<I',source,0x4493C)[0]!=ROOT_ADDRESS or struct.unpack_from('<I',source,0x448DC)[0]!=0x080448E0:
        raise ValueError('039 shared loader destination/table literal')
    return dict(root=ROOT_ADDRESS,inner_lr=INNER_LR,outer_lr=OUTER_LR,
                saved_outer_lr_incoming_sp_offset=16,wrapper_stack_bytes=32,
                saved_outer_lr_wrapper_sp_offset=48,original_preset_bytes=8)


def source_population(source, selected):
    """All23 table entries /21 unique archives; reject native-prefix ambiguity."""
    contracts(source)
    aliases=defaultdict(list)
    for navi in range(23):
        ptr=0x448E0+navi*4; address=struct.unpack_from('<I',source,ptr)[0]
        if not 0x08000000<=address<0x08000000+len(source):raise ValueError('039 source table bounds')
        aliases[f'{address-0x08000000:X}'].append(dict(navi=navi,pointer=ptr))
    if len(aliases)!=21:raise ValueError('039 finite source denominator')
    pool={arc:dict(archive=arc,references=refs,payload=lz77_decompress(source,int(arc,16))[0]) for arc,refs in aliases.items()}
    if not selected or not set(selected)<=set(pool):raise ValueError('039 selected source owner')
    for arc in selected:
        a=pool[arc]['payload']
        if not a or len(a)>0x4000:raise ValueError('039 native comparison extent')
        for other,p in pool.items():
            if arc!=other and a[:min(len(a),len(p['payload']))]==p['payload'][:min(len(a),len(p['payload']))]:
                raise ValueError(('039 ambiguous native prefix',arc,other))
    return list(pool.values())


def wrap(source,address,previous_entry,table,count):
    abi=contracts(source)
    if type(count)is not int or not 1<=count<=255:raise ValueError('039 descriptor count')
    if any(type(x)is not int or x&3 for x in (address,table)) or not 0x08000000<=table<table+count*16<=address<0x0A000000 or not 0x08000000<=previous_entry<0x0A000000:
        raise ValueError('039 code placement')
    code='''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
mov r2,lr
ldr r3,inner
cmp r2,r3
bne fallback
ldr r3,root
cmp r0,r3
bne fallback
lsrs r2,r1,#8
bne fallback
ldr r2,[sp,#48]
ldr r3,outer
cmp r2,r3
bne fallback
ldr r3,descriptors
movs r7,#COUNT
candidate:
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
adds r3,#16
subs r7,#1
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''.replace('COUNT',str(count))
    blob,proof=assemble_verified(code,address,dict(inner=INNER_LR,root=ROOT_ADDRESS,outer=OUTER_LR,descriptors=table,previous=previous_entry|1))
    return blob,dict(proof=proof,contracts=abi,descriptor_fields=FIELDS,descriptor_bytes=16,
                     descriptor_slots=count,persistent_ram_bytes=0,scene_dereferenced=False,
                     comparison='inner LR + root + unsigned8 script + saved outer LR + per-archive script bound + every native byte',
                     predecessor_contract='Original r3 on stack; direct038 wrapper entry, not installation stub',runtime_tested=False)
