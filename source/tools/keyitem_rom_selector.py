"""Adopted deterministic Thumb-1 emitter for the guarded key-item ROM reader.

Evidence: analysis/KEYITEM_ROM_SELECTOR_HANDOFF.md. The caller owns final writes.
"""
import struct
from extended_dialogue import assemble_verified
from build_visibility_poc import sha
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

INSTALL=0x4FB4C
EXPECTED=bytes.fromhex('70b55546ed6aea6c2b6d6c6d')
CALLERS={0x02020800:(0x0803497F,),0x02031000:(0x0804CC31,0x0804CC3F,0x0804CC5D)}
CALL_SITES={0x3497A:'1bf0e7f8',0x4CC30:'02f08cff',0x4CC3E:'02f085ff',0x4CC5C:'02f076ff'}

def construct(source,header,clone_address,hook_address,payload_bytes=2477,mail=None,missions=None,equipment=None,hints=None,b0_hints=None):
    if source[INSTALL:INSTALL+12]!=EXPECTED or len(header)!=16 or struct.unpack_from('<H',header)[0]!=98:
        raise ValueError('reader source / 49-entry header identity')
    call_proof=[]
    for at,expected in CALL_SITES.items():
        blob=source[at:at+4];decoded=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(blob,0x08000000+at))
        if blob.hex()!=expected or len(decoded)!=1 or decoded[0].size!=4 or decoded[0].mnemonic!='bl' or int(decoded[0].op_str.lstrip('#'),0)!=0x0804FB4C:
            raise ValueError('declared native call source changed')
        call_proof.append(dict(address=0x08000000+at,hex=expected,reader=0x0804FB4C,caller_lr=0x08000000+at+5))
    if not 98<=payload_bytes<=0xffff or clone_address&3 or hook_address&3 or not 0x08000000<=clone_address<0x0A000000 or not clone_address+payload_bytes<=hook_address<0x0A000000:
        raise ValueError('analysis ROM-map/alignment/overlap')
    # Installation temporarily saves r3; selector has no persistent state.
    # Header identity distinguishes loaded709408 from alternate709704.
    # No new decompression, buffers, or text-RAM writes are introduced.
    code='''pop {r3}
push {r2,r3,r4}
mov r2,lr
'''
    if mail is not None:
        if (set(mail)!={'clone_address','payload_bytes','guard_header_hex'} or
            source[0x4F7B8:0x4F7BC]!=bytes.fromhex('00f0c8f9') or
            len(bytes.fromhex(mail['guard_header_hex']))!=16 or
            int.from_bytes(bytes.fromhex(mail['guard_header_hex'])[:2],'little')!=64 or
            not 64<=mail['payload_bytes']<=0xffff or mail['clone_address']&3 or
            not clone_address+payload_bytes<=mail['clone_address'] or
            not mail['clone_address']+mail['payload_bytes']<=hook_address<0x0A000000):
            raise ValueError('mail clone identity/caller/placement')
        code+='''ldr r3,mail_root
cmp r0,r3
bne item
ldr r3,mail_call
cmp r2,r3
bne native
movs r3,#255
ands r3,r1
cmp r3,r1
bne native
cmp r1,#31
bgt native
'''
        for i in range(4):
            code+=f'ldr r3,[r0,#{i*4}]\nldr r4,mail_header{i}\ncmp r3,r4\nbne native\n'
        code+='ldr r0,mail_clone\nb native\nitem:\n'
    code+='''
ldr r3,ui_root
cmp r0,r3
beq ui
ldr r3,other_root
cmp r0,r3
bne native
ldr r3,other_call0
cmp r2,r3
beq identity
ldr r3,other_call1
cmp r2,r3
beq identity
ldr r3,other_call2
cmp r2,r3
bne native
b identity
ui:
ldr r3,ui_call
cmp r2,r3
bne native
identity:
movs r3,#255
ands r3,r1
cmp r3,r1
bne native
cmp r1,#48
bgt native
'''
    for i in range(4):
        code+=f'ldr r3,[r0,#{i*4}]\nldr r4,header{i}\ncmp r3,r4\nbne native\n'
    code+='''ldr r0,clone
native:
pop {r2,r3,r4}
push {r4,r5,r6,lr}
mov r5,r10
ldr r5,[r5,#44]
ldr r2,[r5,#76]
ldr r3,[r5,#80]
ldr r4,[r5,#84]
ldr r6,resume
bx r6'''
    values=dict(ui_root=0x02020800,other_root=0x02031000,other_call0=0x0804CC31,other_call1=0x0804CC3F,other_call2=0x0804CC5D,ui_call=0x0803497F,
        **{f'header{i}':struct.unpack_from('<I',header,i*4)[0] for i in range(4)},clone=clone_address,resume=0x0804FB59)
    if mail is not None:
        values.update(mail_root=0x0202B2F4,mail_call=0x0804F7BD,mail_clone=mail['clone_address'],
            **{f'mail_header{i}':struct.unpack_from('<I',bytes.fromhex(mail['guard_header_hex']),i*4)[0] for i in range(4)})
    hook,isa=assemble_verified(code,hook_address,values)
    entry=hook_address;wrapper_isa=None
    if missions:
        guards=set();previous=mail['clone_address']+mail['payload_bytes'] if mail else clone_address+payload_bytes
        for m in missions:
            if set(m)!={'clone_address','payload_bytes','guard_header_hex','script_count'} or m['script_count'] not in (66,52,47,34) or len(bytes.fromhex(m['guard_header_hex']))!=16 or int.from_bytes(bytes.fromhex(m['guard_header_hex'])[:2],'little')!=2*m['script_count'] or m['guard_header_hex'] in guards or not previous<=m['clone_address'] or m['clone_address']&3 or not 2*m['script_count']<=m['payload_bytes']<=65535 or m['clone_address']+m['payload_bytes']>hook_address:raise ValueError('mission clone identity/placement')
            guards.add(m['guard_header_hex']);previous=m['clone_address']+m['payload_bytes']
        entry=hook_address+len(hook)
        wrapper='pop {r3}\npush {r2,r3,r4}\nmov r2,lr\nldr r3,root\ncmp r0,r3\nbne fallback\nldr r3,caller\ncmp r2,r3\nbne fallback\nmovs r3,#255\nands r3,r1\ncmp r3,r1\nbne fallback\ncmp r1,#65\nbgt fallback\n'
        vals=dict(root=0x0202B2F4,caller=0x0804F7BD,original=hook_address|1)
        for j,m in enumerate(missions):
            for i in range(4):
                wrapper+=f'ldr r3,[r0,#{i*4}]\nldr r4,g{j}_{i}\ncmp r3,r4\nbne next{j}\n'
                vals[f'g{j}_{i}']=struct.unpack_from('<I',bytes.fromhex(m['guard_header_hex']),i*4)[0]
            wrapper+=f"cmp r1,#{m['script_count']-1}\nbgt fallback\nldr r0,clone{j}\nb fallback\nnext{j}:\n";vals[f'clone{j}']=m['clone_address']
        wrapper+='fallback:\npop {r2,r3,r4}\npush {r3}\nldr r3,original\nbx r3'
        extra,wrapper_isa=assemble_verified(wrapper,entry,vals);hook+=extra
    equipment_proof=None
    if equipment:
        from equipment_rom_selector import wrap
        new_entry=hook_address+len(hook)
        extra,equipment_proof=wrap(source,new_entry,entry,equipment)
        hook+=extra;entry=new_entry
    hint_proof=None
    if hints is not None:
        if set(hints)!={'descriptor_address'}:raise ValueError('Hint descriptor contract')
        from hint_rom_selector import wrap
        new_entry=hook_address+len(hook)
        extra,hint_proof=wrap(source,new_entry,entry,hints['descriptor_address'])
        hook+=extra;entry=new_entry
    b0_proof=None
    if b0_hints is not None:
        if hints is None or set(b0_hints)!={'descriptor_address'}:raise ValueError('B0 requires preceding A3 reader/descriptor')
        from hint_rom_selector import wrap
        new_entry=hook_address+len(hook)
        extra,b0_proof=wrap(source,new_entry,entry,b0_hints['descriptor_address'],scene=0xB0)
        hook+=extra;entry=new_entry
    stub,stub_isa=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=entry|1))
    if len(stub)!=12:raise ValueError('probe veneer must cover six original instructions')
    return stub,hook,dict(install_offset=INSTALL,source_hex=EXPECTED.hex(),stub_hex=stub.hex(),hook_sha256=sha(hook),
        clone_address=clone_address,hook_address=hook_address,guard_header_hex=header.hex(),guarded_callers={hex(k):[hex(v) for v in vs] for k,vs in CALLERS.items()},
        machine_code=[stub_isa,isa]+([wrapper_isa] if wrapper_isa else [])+([equipment_proof['proof']] if equipment_proof else [])+([hint_proof['proof']] if hint_proof else [])+([b0_proof['proof']] if b0_proof else []),replayed_source_bytes=12,resume=0x0804FB58,
        native_call_sites=call_proof,unrecognized_callers_preserved_not_claimed_complete=True,
        scratch_r6_dead_until_native_reload=True,flags_not_preserved_at_selector_but_native_flags_recomputed=True,
        persistent_ram_bytes=0,mail_guard=mail,mission_guards=missions,entry_address=entry,
        equipment_guards=equipment,equipment_wrapper=equipment_proof,**(dict(hint_guard=hints,hint_wrapper=hint_proof) if hints is not None else {}),**(dict(b0_hint_guard=b0_hints,b0_hint_wrapper=b0_proof) if b0_hints is not None else {}))
