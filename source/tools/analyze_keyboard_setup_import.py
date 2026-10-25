"""Resolve setup selector through actual native initializer/import caller window."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';dep=base/'descriptor_mutators.json';d=read(dep)
    require_hash(ROOT/'tools/analyze_keyboard_descriptor_mutators.py',d['tools']['analyze_keyboard_descriptor_mutators.py'])
    inv=read(base/'consumer_inventory.json');require_hash(base/'consumer_inventory.json',d['inventory_sha256'])
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,d['current_rom_sha256']);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x3A1C2,0x3A1E8),(0x3558C,0x355AE),(0x355B6,0x355F6)]:
        raw=rom[a:b]
        if current[a:b]!=raw:raise ValueError('setup/import code identity')
        ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('setup/import ISA')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    for a,v in [(0x3A1FC,0x0803B0D0),(0x3574C,0x0200FC40)]:
        if struct.unpack_from('<I',rom,a)[0]!=v or current[a:a+4]!=rom[a:a+4]:raise ValueError('setup/import literal')
    rows=[];stats=dict(calls=0,legacy_imports=0,mixed_rank229_imported_empty=0,dynamic_heading_modeled_calls=0)
    ctx,editor,sp,end=0x0200F550,0x0200FC40,0x03007F00,0x0803A1E8
    for variant,image in [('source',rom),('current',current)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        u.mem_map(0x08000000,(len(image)+4095)&~4095);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,(len(image)+4095)&~4095,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096)
        writes=[];calls=[];modeled=[]
        u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
        def services(cpu,pc,size,user):
            if pc==0x0800090C:
                if cpu.reg_read(UC_ARM_REG_R0)!=editor or cpu.reg_read(UC_ARM_REG_R1)!=96:raise ValueError('clear96 ABI')
                cpu.mem_write(editor,bytes(96));modeled.append('clear96');cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
            elif pc==0x08038DB8:
                cpu.reg_write(UC_ARM_REG_R0,33);modeled.append('dynamic_heading');cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
            elif pc in (0x080355B6,0x0803558C):
                calls.append((pc,tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3))))
        u.hook_add(UC_HOOK_CODE,services)
        # Only the coherent descriptor2..17 -> metadata0..15 mapping is used.
        # This is a structural denominator, not all valid setup arguments.
        for index in range(2,18):
            selector=image[0x3A11C+index];row=inv['metadata_rows'][selector];cap=row['native_logical_limit']
            if selector!=index-2 or row['descriptor_index']!=index:raise ValueError('selector/metadata relationship')
            meta=image[row['metadata_offset']:row['metadata_offset']+16];heading=33 if selector==0 else meta[3]
            pointer=int(row['descriptor_pointer'],16)-1;body=editor+32
            for kind in ('legacy','mixed_rank229'):
                raw=(b'\x01\x9B\xE5'+bytes(2*cap-1)) if kind=='legacy' else b'\x81\xE5\0'+b'\xFF\xFF'*(cap-1)+b'\xE5'
                u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(pointer,raw)
                state=bytearray(16);struct.pack_into('<I',state,4,pointer);state[8]=selector;u.mem_write(ctx,bytes(state))
                before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before);ed=bytearray(96)
                ed[4]=cap;ed[5]=heading;ed[14]=1
                struct.pack_into('<I',ed,28,pointer)
                for offset in (16,20):struct.pack_into('<I',ed,offset,body)
                cursor=body+2 if kind=='legacy' else body;struct.pack_into('<I',ed,24,cursor)
                ed[32:36]=b'\x9B\0\xE5\0' if kind=='legacy' else b'\xE5\0\0\0'
                expected[editor-0x02000000:editor-0x02000000+96]=ed
                u.mem_write(sp-28,b'\x5A'*28);u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_R5,ctx);u.reg_write(UC_ARM_REG_SP,sp)
                writes.clear();calls.clear();modeled.clear();u.emu_start(0x0803A1C3,end,count=10000)
                if u.reg_read(UC_ARM_REG_PC)!=end or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_R5)!=ctx or bytes(u.mem_read(sp-28,4))!=b'\x5A'*4:raise ValueError('caller window return/stack')
                if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('setup/import whole EWRAM')
                if any(not(sp-24<=a and a+n<=sp or editor<=a and a+n<=editor+96) for a,n in writes):raise ValueError('setup/import writes')
                if calls[0]!=(0x080355B6,(cap,heading,pointer,0)) or calls[1][0]!=0x0803558C or calls[1][1][0]!=pointer or modeled.count('clear96')!=1 or modeled.count('dynamic_heading')!=(selector==0):raise ValueError('initializer/import live-ins')
                stats['calls']+=1;stats['legacy_imports' if kind=='legacy' else 'mixed_rank229_imported_empty']+=1;stats['dynamic_heading_modeled_calls']+=selector==0
            if variant=='source':rows.append(dict(descriptor=index,setup_selector=selector,metadata_offset=row['metadata_offset'],capacity=cap,heading=heading,destination=hex(pointer),caller_initializer='0x0803A1DE',caller_import='0x0803A1E4',mixed_rank229_import_result='empty'))
    report=dict(id='exe45.hangul-keyboard.setup-import-caller.v1',passed=True,rom_integrated=False,format_discriminator_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=d['current_rom_sha256'],counts=stats,rows=rows,native_code=regions,
        caller_window=dict(start='0x0803A1C2',end_exclusive='0x0803A1E8',original_initializer_executed=True,original_import_executed=True,clear96_modeled=True,selector0_heading_modeled=True),
        dependencies={'descriptor_mutators.json':sha(dep.read_bytes())},tools={'analyze_keyboard_setup_import.py':sha((ROOT/'tools/analyze_keyboard_setup_import.py').read_bytes())},
        limits=['Bounded source/current caller window with coherent descriptor2..17/metadata0..15 only. Not natural game entry, every setup argument or complete caller graph.',
                'Selector is metadata row index, not keyboard capacity; original caller resolves capacity/heading then passes descriptor pointer-1.',
                'Initializer and import execute original machine code; external clear96 and metadata0 dynamic heading are explicitly modeled.',
                'Complete mixed rank229 record begins payloadE5 and is imported as empty by the native caller/import. New-format import must replace this boundary, not merely the later display copy.',
                'No auto discriminator, legacy-save policy, keyboard hook, RAM/IRQ budget, actual glyph pixels or native persistence evidence.'])
    (base/'setup_import_caller.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,d['current_rom_sha256'])
    print('PASS native setup selector->metadata->initializer/import',stats,'mixed rank229 imported empty; not ROM integrated',flush=True)

if __name__=='__main__':main()
