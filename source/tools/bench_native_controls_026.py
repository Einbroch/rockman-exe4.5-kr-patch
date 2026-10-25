"""Bounded ARMv4T source/actual025 F608, EB00/01 and F801/02 CPU evidence.

Real native helpers and dispatchers execute; no service substitution, ROM
mutation, battle caller/effect or GBA presentation claim is made.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T

OUT='analysis/pending_insertion_500_026_native_controls_v1/cpu.json'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/'poc/output/pending500_025_v2.gba';require_hash(rp,'ad775421ab5353c1326ab3861cbc22e323ce6885c411273de5e2bdcaebde040e');rom=rp.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x520A4,0x520F6),(0x52134,0x5213E),(0x3B3B8,0x3B3C2),(0x4FD78,0x4FD82),
          (0x524A8,0x524B8),(0x524E0,0x524F2),(0x524F4,0x5250C),(0x52534,0x52540),
          (0x505B4,0x505EC),(0x505F4,0x50616)]
    data=[(0x500DC,4),(0x50144,4),(0x51F64,4),(0x3B468,4),(0x52140,14),
          (0x500E4,4),(0x5014C,4),(0x524B8,20),(0x52530,4),(0x52654,44),(0x52540,8),
          (0x500B0,4),(0x50118,4),(0x505EC,8)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in code:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('026 native instruction identity/extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('026 ARMv4T native roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in data:
        if rom[a:a+n]!=source[a:a+n]:raise ValueError('026 native literal/table identity')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    def ptr(at):return struct.unpack_from('<I',source,at)[0]
    if [ptr(a) for a in (0x500DC,0x50144,0x51F64,0x500E4,0x5014C,0x500B0,0x50118)]!=[0x8051F31,0x8052135,0x80520A5,0x80524A9,0x8052535,0x80505B5,0x80505F5]:raise ValueError('026 native dispatch')
    ctx,stream,stack,stop=0x0200FA20,0x02020000,0x03007F00,0x080000C0
    query=ptr(0x3B468);cases=[];reference={}
    for label,image in [('source',source),('025',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append((a,n)))
        def execute(entry,command,before,mode,extra=None):
            u.mem_write(ctx,before);u.mem_write(stream,command);u.mem_write(query+8,struct.pack('<I',mode));u.mem_write(stack-64,b'\xA7'*64)
            if extra is not None:u.mem_write(extra,b'\xA6'*8)
            values=[0x1000+i*0x101 for i in range(15)];values[4]=stream;values[5]=ctx;values[13]=stack;values[14]=stop|1
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(entry|1,0,count=1000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack or u.reg_read(REGS[4])!=stream+len(command):raise ValueError('026 continuation/stack')
            if any(not(ctx<=a and a+n<=ctx+216 or stack-32<=a and a+n<=stack or extra is not None and extra<=a and a+n<=extra+8) for a,n in writes):raise ValueError('026 unexpected write extent')
            if any(u.reg_read(REGS[i])!=values[i] for i in (5,6,7,8,9,10,11,12)):raise ValueError('026 preserved register drift')
            return bytes(u.mem_read(ctx,216)),bytes(u.mem_read(extra,8)) if extra is not None else None
        def check(key,actual,wanted):
            if actual!=wanted:raise ValueError('026 native effects '+str(key))
            if label=='source':reference[key]=actual
            elif reference[key]!=actual:raise ValueError('026 source/product mismatch')
            cases.append(dict(image=label,fixture=list(key)))
        for w in range(1,11):
            for flags in (0,2):
                for mode in (0,1):
                    for origin in (8,52):
                        for row in range(3):
                            before=bytearray(216);before[0x18]=origin;struct.pack_into('<H',before,0x3E,flags);struct.pack_into('<I',before,0x7C,row*10752)
                            allocation=11*w+8;area=(166 if mode else 176) if flags else (230 if mode else 240);rel=(area-allocation)//2-(0 if flags else origin)
                            if rel<0 or not 8<=origin+rel<origin+rel+allocation<=234:raise ValueError('026 unsafe declared vertical bounds')
                            wanted=bytearray(before);wanted[0x94]=(origin+rel)&255;struct.pack_into('<I',wanted,0x7C,row*10752+4*rel)
                            cmd=bytes([0xF6,8,w]);check(('F608',w,flags,mode,origin,row),execute(0x80520A4,cmd,bytes(before),mode),(bytes(wanted),None))
                            check(('F608-width',w,flags,mode,origin,row),execute(0x8052134,cmd,bytes(before),mode),(bytes(before),None))
        for subtype,counts in ((0,(1,)),(1,(16,))):
            for row in range(3):
                before=bytearray(216);struct.pack_into('<I',before,0x7C,row*10752);struct.pack_into('<I',before,0x70,17)
                for count in counts:
                    cmd=bytes([0xEB,subtype,count]);delta=count*(1 if subtype else 8)
                    wanted=bytearray(before);struct.pack_into('<I',wanted,0x7C,row*10752+4*delta)
                    check(('EB-draw',subtype,count,row),execute(0x80505B4,cmd,bytes(before),0),(bytes(wanted),None))
                    wanted=bytearray(before);struct.pack_into('<I',wanted,0x70,17+delta)
                    check(('EB-width',subtype,count,row),execute(0x80505F4,cmd,bytes(before),0),(bytes(wanted),None))
        for subtype,index,values in ((1,8,range(256)),(1,9,range(256)),(2,10,(0,1,255,256,6082,32767,65535))):
            dest=ptr(0x52654+4*index)
            for value in values:
                before=bytes([0x53])*216;encoded=value.to_bytes(subtype,'little');cmd=bytes([0xF8,subtype,index])+encoded;wanted=encoded+b'\xA6'*(8-len(encoded))
                check(('F8-draw',subtype,index,value),execute(0x80524A8,cmd,before,0,dest),(before,wanted))
                check(('F8-width',subtype,index,value),execute(0x8052534,cmd,before,0,dest),(before,b'\xA6'*8))
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),tool_sha256=sha((ROOT/'tools/bench_native_controls_026.py').read_bytes()),native_ranges=ranges,case_count=len(cases),cases=cases,substituted_helpers=[],rom_written=False,release_eligible=False,limits='Bounded native CPU source/025 identity and effects only. No026 product integration, actual extended-choice GBA cursor graph/outcomes, event acquisition/battle effects, presentation approval or save support.'))
    print('PASS026 native controls',len(cases),'source/025 fixtures; NO ROM written')

if __name__=='__main__':main()
