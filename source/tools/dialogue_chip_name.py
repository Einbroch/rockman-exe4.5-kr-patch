"""Caller-stream-gated native printChip104 source selection, no shared roots."""
import struct
from archive_scripts import script_spans
from extended_dialogue import assemble_verified
from korean_codec import encode_character
from build_visibility_poc import sha
INSTALL=0x5162C
EXPECTED=bytes.fromhex('40182f1c64373a88d2013049')

def construct(source,appended,archive,asset,guts_command=None):
    if source[INSTALL:INSTALL+12]!=EXPECTED or source[0x516F8:0x516FC]!=struct.pack('<I',0x02010AC0):raise ValueError('native printChip source instructions changed')
    if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['review']['release_eligible'] is not False or asset['source_sha256']!=sha(source):raise ValueError('chip wording development identity')
    wording=next(w for w in asset['wordings'] if w['id']=='library.chip.batch04.104');unit=next(w for w in asset['units'] if w['id']=='765190:104:0')
    if wording['state']!='needs_review' or unit['source']!='ビッグハンマー1' or unit['wording_id']!=wording['id'] or wording['translation']!='빅해머1':raise ValueError('adopted chip104 wording/identity changed')
    srcname=script_spans(source[0x765190:0x765190+2437],256)[104]
    if srcname!=bytes.fromhex('4b593d243a298202e5'):raise ValueError('chip104 source name changed')
    command=0x08000000+archive['rom_offset']+archive['script13_offset']+17
    if guts_command is not None and (not isinstance(guts_command,int) or not 0x08800000<=guts_command<0x0a000000 or guts_command==command):raise ValueError('Guts additional exact command range/identity')
    if archive['script13_prefix_hex']!='f6000a0c01e702f6025c6e03f604e18d92f9006801':raise ValueError('Roll13 printChip stream anchor changed')
    body=b''.join(encode_character(c) if '\uac00'<=c<='\ud7a3' else b'\x02' if c=='1' else (_ for _ in ()).throw(ValueError('unmapped chip104 character')) for c in wording['translation'])+b'\xe5'
    if len(body)>128:raise ValueError('native chip buffer overflow')
    out=bytearray(appended);out.extend(b'\xff'*(-len(out)%4));name_at=len(source)+len(out);block=body+b'\xe5'*(128-len(body));out.extend(block);out.extend(b'\xff'*(-len(out)%4));hook_at=len(source)+len(out)
    # Stub saves r3; hook reconstructs all six overwritten effects. A small
    # stack return frame preserves every high register and the original LR.
    code='''pop {r3}
sub sp,#8
str r3,[sp,#0]
ldr r3,continuation
str r3,[sp,#4]
adds r0,r0,r1
ldr r3,command_stream
cmp r4,r3
bne resume
ldr r3,normal_context
cmp r5,r3
bne resume
ldr r3,native_name
cmp r0,r3
bne resume
ldr r0,korean_name
resume:
adds r7,r5,#0
adds r7,#100
ldrh r2,[r7]
lsls r2,r2,#7
ldr r1,native_buffer
pop {r3,pc}'''
    name_source=0x08765190+struct.unpack_from('<H',source,0x765190+208)[0]
    literals={'continuation':0x08051639,'command_stream':command,'normal_context':0x0200FA20,'native_name':name_source,'korean_name':0x08000000+name_at,'native_buffer':0x02010AC0}
    if guts_command is not None:
        code=code.replace('cmp r4,r3\nbne resume\nldr r3,normal_context','cmp r4,r3\nbeq selected_stream\nldr r3,guts_command_stream\ncmp r4,r3\nbne resume\nselected_stream:\nldr r3,normal_context')
        literals['guts_command_stream']=guts_command
    payload,record=assemble_verified(code,0x08000000+hook_at,literals);out.extend(payload)
    stub,install=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,{'target':0x08000001+hook_at})
    if len(stub)!=12:raise ValueError('printChip installation extent')
    metadata={'policy':'development-draft; NON-DISTRIBUTION','install_offset':INSTALL,'install_bytes':12,'source_expected_hex':EXPECTED.hex(),'hook_offset':hook_at,'hook_bytes':len(payload),'name_offset':name_at,'name_bytes':len(body),'copy_extent':128,'name_block_sha256':sha(block),'name_hex':body.hex(),'name':'빅해머1','wording_id':wording['id'],'wording_count_increment':0,'command_stream':command,'context':0x0200FA20,'native_name_stream':name_source,'normal_dialogue_archive':'664E28','native_copy_continuation':0x08051638,'machine_code':[record,install],'shared_name_roots_unchanged':True,'source_normal_name_pool_unchanged':True,'runtime':'pending native lookup/copy128/RAM/font/ABI/fallback/exit; other dialogue names native'}
    if guts_command is not None:metadata.update(gutsman_command_stream=guts_command,additional_archive='66A844',runtime='pending both exact Roll13/Guts13 lookup/copy128/RAM/font/ABI/fallback/exit')
    return bytes(out),[(INSTALL,stub,('Roll13/Guts13' if guts_command is not None else 'Roll13')+' printChip104 isolated Korean source selector')],metadata
