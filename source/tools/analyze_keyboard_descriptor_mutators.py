"""Bound two native descriptor consumers; not all writers or save coverage."""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';ip=base/'consumer_inventory.json';inv=read(ip)
    require_hash(ROOT/'tools/analyze_keyboard_consumers.py',inv['tool_sha256'])
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=inv['current_rom_sha256'];require_hash(play,identity);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x35D66,0x35D7C),(0x3A0F4,0x3A118),(0x32AA8,0x32AD8)]:
        raw=rom[a:b]
        if current[a:b]!=raw:raise ValueError('descriptor consumer changed')
        instructions=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in instructions)!=len(raw):raise ValueError('native extent')
        for i in instructions:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native ISA roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    literals=[]
    for a,v in [(0x35D7C,0x080526D0),(0x3A160,0x080526D0),(0x3A118,0x0803A11C),(0x3A184,0x0200F550)]:
        if struct.unpack_from('<I',rom,a)[0]!=v or rom[a:a+4]!=current[a:a+4]:raise ValueError('native literal')
        literals.append(dict(offset=a,value=hex(v)))
    descriptor_literal_candidates=[hex(i) for i in range(0,len(rom)-3,4) if rom[i:i+4]==struct.pack('<I',0x080526D0)]
    if descriptor_literal_candidates!=['0x35d7c','0x38de8','0x3a160','0x5181c','0x1ef968']:raise ValueError('bounded aligned literal inventory')
    sp,stop,ctx,glob,surface=0x03007F00,0x0FF00000,0x0200F550,0x02000020,0x02000100
    high=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    rows=[];stats=dict(delete_calls=0,setup_calls=0,first_record_marker_aliases=0,nonrecord_preceding_byte_targets=0)
    for variant,image in [('source',rom),('current',current)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        u.mem_map(0x08000000,(len(image)+4095)&~4095);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,(len(image)+4095)&~4095,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(stop,4096)
        writes=[];modeled=[]
        u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
        def clear_service(cpu,pc,size,user):
            if pc==0x0803A3B0:
                # Native setup's external clear service is explicitly modeled.
                cpu.mem_write(ctx,bytes(16));modeled.append((ctx,16));cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        u.hook_add(UC_HOOK_CODE,clear_service)
        table=struct.unpack_from('<I',image,0x32AD8)[0]-0x08000000
        start=table+struct.unpack_from('<H',image,table+71*2)[0]
        end=image.index(0xE5,start)+1;default=image[start:end]
        if default!=bytes.fromhex('7e7e7ee5'):raise ValueError('default47 baseline')
        for row in inv['metadata_rows']:
            index=row['descriptor_index'];p=int(row['descriptor_pointer'],16)
            if struct.unpack_from('<II',image,0x526D0+8*index)!=(p,row['descriptor_bytes']):raise ValueError('descriptor identity')
            for operation,pc,depth in [('delete',0x08035D66,12),('setup',0x0803A0F4,8)]:
                u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(glob,struct.pack('<I',surface))
                before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before)
                if operation=='delete':
                    expected[p-1-0x02000000]=0;expected[p-0x02000000:p-0x02000000+len(default)]=default
                    permitted=[(p-1,1),(p,len(default))]
                else:
                    state=bytearray(16);struct.pack_into('<I',state,4,p-1);state[8]=image[0x3A11C+index]
                    expected[ctx-0x02000000:ctx-0x02000000+16]=state;expected[surface-0x02000000]=0x58
                    permitted=[(ctx,16),(surface,1)]
                u.mem_write(sp-depth-4,b'\x5A'*(depth+4));u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_R0,index)
                for n,r in enumerate(high):u.reg_write(r,glob if r==UC_ARM_REG_R10 else 0x13579000+n)
                u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();modeled.clear();u.emu_start(pc|1,stop,count=10000)
                if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or bytes(u.mem_read(sp-depth-4,4))!=b'\x5A'*4 or any(u.reg_read(r)!=(glob if r==UC_ARM_REG_R10 else 0x13579000+n) for n,r in enumerate(high)):raise ValueError('descriptor consumer ABI')
                if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('descriptor consumer output')
                if any(not(sp-depth<=a and a+n<=sp or any(s<=a and a+n<=s+l for s,l in permitted)) for a,n in writes+modeled):raise ValueError('descriptor consumer write boundary')
                if operation=='setup' and modeled!=[(ctx,16)] or operation=='delete' and modeled:raise ValueError('clear service scope')
                stats[operation+'_calls']+=1
            if variant=='source':
                alias=p-1==int(row['field_start'],16);stats['first_record_marker_aliases']+=alias;stats['nonrecord_preceding_byte_targets']+=not alias
                rows.append(dict(descriptor=index,pointer=hex(p),preceding_byte=hex(p-1),metadata_first_record=row['field_start'],first_record_marker_alias=alias,
                    delete_default_hex=default.hex(),setup_context='0x0200F550',setup_pointer_field='+4',setup_selector_byte=image[0x3A11C+index],native_record_capacity=row['native_logical_limit'],
                    selector_is_proven_keyboard_capacity=False))
    report=dict(id='exe45.hangul-keyboard.descriptor-mutators.v1',passed=True,rom_integrated=False,format_discriminator_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,rows=rows,native_code=regions,literals=literals,
        aligned_descriptor_literal_candidates=descriptor_literal_candidates,setup_clear_service_modeled=True,
        default_table=dict(source_pointer=hex(struct.unpack_from('<I',rom,0x32AD8)[0]),current_pointer=hex(struct.unpack_from('<I',current,0x32AD8)[0]),index=71,bytes_hex='7e7e7ee5'),
        inventory_sha256=sha(ip.read_bytes()),tools={'analyze_keyboard_descriptor_mutators.py':sha((ROOT/'tools/analyze_keyboard_descriptor_mutators.py').read_bytes())},
        limits=['Bounded native functions/26 descriptors on source and exact current ROM. Not natural runtime route or full writer/caller/save graph.',
                'Aligned exact32-bit literal scan covers8MiB source words only; not complete computed/indirect/overlay reference inventory.',
                'Deletion clears descriptor pointer-1 then raw-copies system default47;16 alias first record markers,10 preceding bytes are elsewhere. No adoption of a global record marker enum.',
                'Setup stores descriptor pointer-1 in0200F550+4 and a selector byte from3A11C at+8. Selector does not match established keyboard capacities; its UI interpretation is unresolved.',
                'Setup clear service0803A3B0 modeled; deletion/default/raw copier executes original native machine code. No BIOS/IRQ or lifecycle claim.',
                'Any future sideband discriminator/cache must include these delete/setup transitions, not just keyboard confirmation. No hook or persistent save changes.'])
    (base/'descriptor_mutators.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS bounded native descriptor mutators',stats,'clear service modeled; no format adoption',flush=True)

if __name__=='__main__':main()
