"""Caller-gated name helper clone; native8x1 parser/font/upload remain intact."""
from extended_dialogue import assemble_verified,sha


def construct(source,spec,appended,clone_offset,selected_scripts):
    if sha(source)!=spec['source_sha256']: raise ValueError('battle-name source mismatch')
    install=spec['install'];at=install['offset']
    if source[at:at+8].hex()!=install['expected_hex']: raise ValueError('battle-name entry drift')
    for item in spec['protected']:
        if source[item['offset']:item['offset']+len(bytes.fromhex(item['hex']))].hex()!=item['hex']:
            raise ValueError('battle-name native continuation/root/font drift')
    ids=sorted(selected_scripts)
    if not ids or any(type(i) is not int or not 1<=i<=255 for i in ids) or len(ids)!=len(set(ids)):
        raise ValueError('battle-name selector needs explicit unique primary IDs1..255')
    gate=f'cmp r1, #1\nblt primary\ncmp r1, #{ids[-1]}\nbgt primary\n'
    if ids!=list(range(1,ids[-1]+1)):
        runs=[]
        for i in ids:
            if runs and i==runs[-1][1]+1: runs[-1][1]=i
            else: runs.append([i,i])
        gate=''
        for lo,hi in runs:
            gate+=f'cmp r1, #{lo}\nblt primary\ncmp r1, #{hi}\nble use_clone\n'
        gate+='b primary\nuse_clone:\n'
    append=bytearray(appended);append.extend(b'\xff'*(-len(append)%4));hook_at=len(source)+len(append)
    code=f'''push {{r2, r3}}
adds r1, r0, #0
lsls r1, r1, #23
lsrs r1, r1, #23
mov r2, lr
ldr r3, caller
cmp r2, r3
bne primary
{gate}
ldr r2, clone
b selected
primary:
ldr r2, native_primary
selected:
cmp r1, #255
ble lower
ldr r0, native_secondary
lsls r1, r1, #24
lsrs r1, r1, #24
b done
lower:
adds r0, r2, #0
cmp r1, #255
done:
pop {{r2, r3}}
mov pc, lr
'''
    body,body_isa=assemble_verified(code,0x08000000+hook_at,{
        'caller':spec['caller_lr'],'clone':0x08000000+clone_offset,
        'native_primary':spec['native_primary'],'native_secondary':spec['native_secondary']})
    append.extend(body)
    thunk,thunk_isa=assemble_verified('ldr r1, target\nbx r1\n',0x08000000+at,{'target':0x08000001+hook_at})
    if len(thunk)!=8: raise ValueError('battle-name thunk extent changed')
    metadata={'policy':'development-draft; NON-DISTRIBUTION','hook_offset':hook_at,
        'install_offset':at,'clone_offset':clone_offset,'selected_scripts':ids,
        'caller_lr':spec['caller_lr'],'native_font':spec['native_font'],'roles':spec['roles'],
        'width':8,'height':1,'cell_bytes':64,'extra_stack_bytes':8,
        'native_fallback':'all other caller LRs, script0, unselected primary IDs and all secondary IDs',
        'abi':'r0=pool/r1=normalized9-bit sourceID; r2..r14 and SP preserved; original final CMP/shift flags; native MOV PC,LR return',
        'layout':[{'name':'caller-gated battle name helper','offset':hook_at,'bytes':len(body),'sha256':sha(body)}],
        'machine_code':[body_isa,thunk_isa],
        'scope':'native name draw caller166A8 only; original helper primary/secondary pools and all shared pointer words retained',
        'runtime':'pending exact-ROM source/stack/font/tilemap/pixel/fallback verification'}
    return bytes(append),[(at,thunk,'caller-gated battle chip-name helper')],metadata
