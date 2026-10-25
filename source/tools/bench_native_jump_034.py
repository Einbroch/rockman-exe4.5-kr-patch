"""EF00 all targets -> native stream lookup prefix; no helper replacement."""
import hashlib
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_034 import BASE,BASE_SHA
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in [(0x50FD8,0x50FEE),(0x51074,0x5107A),(0x4FD18,0x4FD2A)]:
        raw=source[a:b];instructions=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in instructions)!=len(raw):raise ValueError('034 native jump range identity')
        for i in instructions:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('034 jump ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    if source[0x500C0:0x500C4]!=rom[0x500C0:0x500C4] or struct.unpack_from('<I',source,0x500C0)[0]!=0x08050FD9:raise ValueError('034 EF dispatch')
    ranges.append(dict(offset=0x500C0,bytes=4,sha256=sha(source[0x500C0:0x500C4]),kind='data'))
    ctx,stream,pool,stack,stop,lookup_stop=0x0200FA20,0x02020000,0x02021000,0x03007F00,0x080000C0,0x0804FD2A
    results=[];reference={};cases=0
    for label,image in [('source',source),('033',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);size=(len(image)+4095)&~4095
        u.mem_map(0x08000000,size);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        writes=[];reads=[];u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop() if a in (stop,lookup_stop) else None)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)));u.hook_add(UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append((a,n)))
        table=b''.join(struct.pack('<H',512+i*4) for i in range(256));u.mem_write(pool,table+b'\xE5'*1024);digest=hashlib.sha256()
        for target in range(256):
            before=bytearray((i*7+19)&255 for i in range(216));struct.pack_into('<I',before,0x30,pool)
            u.mem_write(ctx-4,b'\xA6'*4+bytes(before)+b'\xA6'*4);u.mem_write(stream,b'\xEF\x00'+bytes([target])+b'\xE6');u.mem_write(stack-128,b'\xA7'*128)
            values=[0x1000+i*0x101 for i in range(15)];values[4]=stream;values[5]=ctx;values[13]=stack;values[14]=stop|1
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();reads.clear();u.emu_start(0x08050FD9,0,count=100)
            actual=bytes(u.mem_read(ctx,216));expected=bytearray(before);dest=pool+512+target*4
            if target<255:
                expected[1]=target;struct.pack_into('<I',expected,0x2C,dest);struct.pack_into('<I',expected,0x34,dest)
                if u.reg_read(UC_ARM_REG_PC)!=lookup_stop or u.reg_read(REGS[4])!=dest or u.reg_read(REGS[13])!=stack-8:raise ValueError('034 unconditional jump stream lookup')
            elif u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[4])!=stream+3 or u.reg_read(REGS[13])!=stack or u.reg_read(REGS[0])!=1:raise ValueError('034 target255 continuation control')
            if actual!=expected or any(a<=stream+3<a+n for a,n in reads):raise ValueError('034 jump unexpected state/trailing opcode read')
            if bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xA6'*8 or bytes(u.mem_read(stack-128,64))!=b'\xA7'*64:raise ValueError('034 jump canary')
            if any(not(stack-64<=a and a+n<=stack or ctx<=a and a+n<=ctx+216) for a,n in writes):raise ValueError('034 jump write extent')
            if any(u.reg_read(REGS[i])!=values[i] for i in range(5,13)):raise ValueError('034 jump preserved register')
            digest.update(bytes([target])+actual);cases+=1
        result=dict(image=label,cases=256,effects_sha256=digest.hexdigest());results.append(result)
        if label=='source':reference['effects']=result['effects_sha256']
        elif reference['effects']!=result['effects_sha256']:raise ValueError('034 jump source/current effects drift')
    deps=['tools/bench_native_jump_034.py','tools/normal_jump_tail_034.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_jump_cpu_v1/cpu.json',dict(schema=1,passed=True,case_count=cases,results=results,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),native_ranges=ranges,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_helpers_substituted=[],modeled_services=[],rom_written=False,release_eligible=False,limits='Controlled valid table EF00 targets0..254 execute native helper prefix through stream lookup, stop0804FD2A before remaining reset/graphics helpers. Target255 continues and MUST NOT be projected as unconditional. No proof of whole destination handler, natural quest progression, Korean rendering or persistence.'))
    print('034 native jump',cases,'PASS; NO ROM')


if __name__=='__main__':main()
