"""Actual source/033 EB padding and E9 fixed flags; native helpers execute."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from inspect_remaining_034 import BASE,BASE_SHA


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes()
    survey='analysis/pending_insertion_500_034_query_layout_v1/survey.json';s=read(survey)
    if s['baseline_sha256']!=BASE_SHA:raise ValueError('034 query source population')
    flags=sorted({int(f['arguments'].split('=')[1]) for g in s['candidate_groups'] for p in g['geometry'] for f in p['preserved_flags']})
    if not flags or any(not 0<=f<=65535 for f in flags):raise ValueError('034 flag finite population')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x505B4,0x505EC),(0x505F4,0x50616),(0x503C0,0x503DE),(0x50424,0x50438),(0x504C6,0x504D2),(0x28722,0x2873C),(0x28752,0x2876C)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or raw!=rom[a:b]:raise ValueError('034 control source/current native range')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('034 native ARMv4T roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in [(0x505EC,8),(0x500B0,4),(0x50118,4),(0x500A8,4),(0x50110,4),(0x503E0,12),(0x504D4,6)]:
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('034 control literal/dispatch source identity')
        regions.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    if tuple(struct.unpack_from('<I',source,a)[0] for a in (0x500B0,0x50118,0x500A8,0x50110))!=(0x080505B5,0x080505F5,0x080503C1,0x080504C7):raise ValueError('034 native VM dispatch')
    ctx,stream,stack,stop,glob,flagbuf=0x0200FA20,0x02020000,0x03007F00,0x080000C0,0x02000100,0x02002000
    cases=[];reference={}
    for label,image in [('source',source),('033',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def execute(entry,command,before,allowed,key,expected_ctx,expected_flags):
            u.mem_write(ctx-4,b'\xA6'*4+before+b'\xA6'*4);u.mem_write(stream-4,b'\xA6'*4+command+b'\xA6'*4);u.mem_write(stack-128,b'\xA7'*128)
            values=[0x1000+i*0x101 for i in range(15)];values[4]=stream;values[5]=ctx;values[10]=glob;values[13]=stack;values[14]=stop|1
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(entry|1,0,count=2000)
            regs=[u.reg_read(r) for r in REGS];actual=bytes(u.mem_read(ctx,216));actual_flags=bytes(u.mem_read(flagbuf,8192))
            if u.reg_read(UC_ARM_REG_PC)!=stop or regs[4]!=stream+len(command) or regs[13]!=stack or actual!=expected_ctx or actual_flags!=expected_flags:raise ValueError('034 native control context/flag/continuation '+str(key))
            if any(regs[i]!=values[i] for i in range(5,13)) or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xA6'*8 or bytes(u.mem_read(stack-128,64))!=b'\xA7'*64:raise ValueError('034 native control register/canary')
            if bytes(u.mem_read(stream-4,len(command)+8))!=b'\xA6'*4+command+b'\xA6'*4:raise ValueError('034 command stream changed')
            if any(not(stack-64<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('034 native control write extent')
            result=(tuple(regs),u.reg_read(UC_ARM_REG_CPSR),actual,actual_flags,tuple(writes))
            if label=='source':reference[key]=result
            elif reference[key]!=result:raise ValueError('034 source/current native effect changed')
            cases.append(dict(image=label,fixture=list(key)))
        u.mem_write(glob+0x48,struct.pack('<I',flagbuf));blank=b'\x5A'*8192
        for pad in (8,16,24):
            for row in range(3):
                for phase,entry in [('draw',0x080505B4),('width',0x080505F4)]:
                    before=bytearray(216);before[0x18:0x1A]=bytes([92,110]);struct.pack_into('<I',before,0x7C,row*10752);struct.pack_into('<I',before,0x70,17);wanted=bytearray(before)
                    at=0x7C if phase=='draw' else 0x70;value=row*10752+4*pad if phase=='draw' else 17+pad;struct.pack_into('<I',wanted,at,value);u.mem_write(flagbuf,blank)
                    execute(entry,bytes([0xEB,1,pad]),bytes(before),[(ctx,ctx+216)],('EB01',pad,row,phase),bytes(wanted),blank)
        for flag in flags:
            for subtype in (0,1):
                for fill in (0x5A,0xA5):
                    for phase,entry in [('draw',0x080503C0),('width',0x080504C6)]:
                        before=bytes((i*7+19)&255 for i in range(216));initial=bytes([fill])*8192;u.mem_write(flagbuf,initial);wanted=bytearray(initial);address=flag//8;mask=0x80>>(flag%8)
                        if phase=='draw':wanted[address]=(wanted[address]|mask) if subtype==0 else (wanted[address]&~mask)
                        execute(entry,bytes([0xE9,subtype])+struct.pack('<H',flag),before,[(flagbuf+address,flagbuf+address+1)] if phase=='draw' else [],('E9',flag,subtype,fill,phase),before,bytes(wanted))
    deps=[survey,'tools/bench_pet_query_controls_034.py','tools/pet_query_choices_034.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_query_controls_cpu_v1/cpu.json',dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,native_ranges=regions,
        padding_pixels=[8,16,24],flag_values=flags,case_count=len(cases),cases=cases,native_helpers_substituted=[],modeled_services=[],
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,release_eligible=False,
        limits='Only native EB01 padding and E900/01 fixed flags under declared context/global pointer fixtures. Exact source/current context/flags/continuation/register/canary effects; no EA/EC/clear/input/editor/caller/acquisition, rendered Korean labels, product integration or semantic approval.'))
    print('034 query controls CPU',len(cases),'fixtures;',len(flags),'source flag values;NO ROM')


if __name__=='__main__':main()
