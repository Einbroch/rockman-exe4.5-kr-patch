"""Native F903 numeric clock formatter in source/030; all valid time values.

No helper/BIOS replacements. CPU, not calendar acquisition or GBA timing.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
BASE='poc/output/pending500_031_v1.gba'

OUT='analysis/pending500_031_v1/event_time_format_cpu.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    meta=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,meta['output_sha256']);rom=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in [(0x516AC,0x516F8),(0x52150,0x521D0),(0xA0C,0xA3A),(0xA68,0xA7E)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('031 numeric source scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('031 numeric ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    for a,n in [(0xA3C,44),(0x51584,4),(0x51594,4),(0x516F8,4)]:
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('031 numeric literal/table drift')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n])))
    if struct.unpack_from('<I',source,0x51594)[0]!=0x080516AD or struct.unpack_from('<I',source,0x516F8)[0]!=0x02010AC0:raise ValueError('031 F903 binding')
    stop,stack,ctx,stream=0x080000C0,0x03007F00,0x0200FA20,0x02020000;cases=[];reference={}
    for label,image in [('source',source),('030',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        for kind,flag,maximum in [('hour',0x82,12),('minute',0xC2,59)]:
            for value in range(maximum+1):
                for slot in range(4):
                    scratch=0x02010AC0+slot*128;u.mem_write(ctx,bytes(216));u.mem_write(ctx+0x4C,struct.pack('<I',value));u.mem_write(ctx+0x64,struct.pack('<H',slot));u.mem_write(stream,bytes([0xF9,3,flag,1]));u.mem_write(scratch-4,b'\xA6'*13);u.mem_write(stack-256,b'\xA7'*256)
                    before=[0x1000+i*0x101 for i in range(15)];before[4]=stream;before[5]=ctx;before[13]=stack;before[14]=stop|1
                    u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
                    for r,v in zip(REGS,before):u.reg_write(r,v)
                    writes.clear();u.emu_start(0x080516AD,0,count=5000)
                    if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack:raise ValueError('031 numeric native return/stack')
                    text=f'{value:02}' if kind=='minute' else f'{value:2}';expected=bytes(0 if ch==' ' else int(ch)+1 for ch in text)+b'\xE5\0\0'
                    if bytes(u.mem_read(scratch,5))!=expected or bytes(u.mem_read(scratch-4,4))+bytes(u.mem_read(scratch+5,4))!=b'\xA6'*8:raise ValueError('031 exact numeric bytes/canaries')
                    if bytes(u.mem_read(stack-256,128))!=b'\xA7'*128 or any(not(stack-128<=a and a+n<=stack or ctx<=a and a+n<=ctx+216 or scratch<=a and a+n<=scratch+5) for a,n in writes):raise ValueError('031 numeric allowed writes/stack canary')
                    state=bytes(u.mem_read(ctx,216));after=[u.reg_read(r) for r in REGS];flags=u.reg_read(UC_ARM_REG_CPSR)
                    if after[4]!=scratch or struct.unpack_from('<I',state,0x44)[0]!=stream+4 or struct.unpack_from('<I',state,0x2C)[0]!=scratch or struct.unpack_from('<H',state,0x64)[0]!=slot+1 or state[5]!=1:raise ValueError('031 numeric continuation')
                    key=(kind,value,slot);effect=(after,flags,state,bytes(u.mem_read(scratch-4,13)))
                    if label=='source':reference[key]=effect
                    elif effect!=reference[key]:raise ValueError('031 source/030 full native effects')
                    width=sum(struct.unpack_from('<I',source,0x5290C+ch*4)[0] for ch in expected[:2])
                    if width>22:raise ValueError('031 clock width')
                    cases.append(dict(image=label,kind=kind,value=value,slot=slot,raw_hex=expected.hex(),width=width))
    paths=['tools/bench_event_time_format_product_031.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),cases=len(cases),case_details=cases,native_ranges=ranges,maximum_clock_component_width=22,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},rom_written=False,release_eligible=False,limits=['CPU source/030 exact native output/registers/CPSR/context/canaries; no helper or BIOS replaced.','Valid hour0..12/minute0..59 only, four native slots; not arbitrary integer/date formatting.','No new ROM or translated units; no native UI/RTC/save/max-title GBA proof.']))
    print('031 numeric formatter PASS',len(cases),'source/030 cases; maximum22px; no ROM',flush=True)


if __name__=='__main__':main()
