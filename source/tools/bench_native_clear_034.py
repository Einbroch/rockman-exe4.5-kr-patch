"""Native F1 clear effects at default origin; fixed BIOS FastSet32 model."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_034 import BASE,BASE_SHA
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in [(0x510BC,0x5111C),(0x4FD60,0x4FD78),(0x553E8,0x553F6),(0x5543C,0x55456),(0x92C,0x946),(0xEC140,0xEC144)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('034 clear native range')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('034 clear ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in [(0x500C8,4),(0x5111C,8),(0x55414,4),(0x55458,16),(0x948,4)]:
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('034 clear literal drift')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    if struct.unpack_from('<I',source,0x500C8)[0]!=0x080510BD:raise ValueError('034 F1 dispatch')
    ctx,stream,stack,stop,signal=0x0200FA20,0x02020000,0x03007F00,0x080000C0,0x0200FB24
    buffers=[0x02012F50,0x02013E50];cases=[];refs={};bios_calls=0
    for label,image in [('source',source),('033',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);size=(len(image)+4095)&~4095;u.mem_map(0x08000000,size);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,size,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def bios(uc,number,d):
            nonlocal bios_calls
            a,b,c=[uc.reg_read(REGS[i]) for i in range(3)]
            if number!=2 or uc.reg_read(UC_ARM_REG_PC)!=0x080EC142 or b not in buffers or c!=0x010003C0 or a%4 or not stack-128<=a<stack or bytes(uc.mem_read(a,4))!=bytes(4):raise ValueError('034 fixed FastSet32 zero domain')
            uc.mem_write(b,bytes(3840));writes.append((b,3840));bios_calls+=1
        u.hook_add(UC_HOOK_INTR,bios)
        for mode in (0,1,2):
            for fill in (0x5A,0xA5):
                before=bytearray([fill]*216);before[8]=mode;before[5]=0;before[0x18]=52;before[0x19]=110;expected=bytearray(before)
                mask=struct.unpack_from('<H',before,0x3E)[0];mask=(mask|1) if mode else mask;mask&=~0xC00;struct.pack_into('<H',expected,0x3E,mask)
                struct.pack_into('<I',expected,0x34,stream+1)
                for at,n in [(4,1),(0x64,4),(0x12,1),(2,1),(0x17,1),(0x3D,1),(0x80,4),(0x0F,1),(0x70,4),(0x7C,4)]:expected[at:at+n]=bytes(n)
                struct.pack_into('<I',expected,0x78,4);struct.pack_into('<I',expected,0x74,1);expected[0x11]=mode;expected[0x94]=52
                u.mem_write(ctx-4,b'\xA6'*4+bytes(before)+b'\xA6'*4);u.mem_write(stream,b'\xF1\xE7\x00');u.mem_write(stack-160,b'\xA7'*160);u.mem_write(signal,struct.pack('<I',0x12340000))
                for at in buffers:u.mem_write(at-4,b'\xA6'*3848)
                values=[0x1000+i*0x101 for i in range(15)];values[4]=stream;values[5]=ctx;values[13]=stack;values[14]=stop|1
                for r,v in zip(REGS,values):u.reg_write(r,v)
                u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(0x080510BD,0,count=500)
                actual=bytes(u.mem_read(ctx,216))
                if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[4])!=stream+1 or u.reg_read(REGS[13])!=stack or actual!=expected:raise ValueError('034 clear exact context/stream')
                if any(u.reg_read(REGS[i])!=values[i] for i in range(5,13)):raise ValueError('034 clear preserved registers')
                if struct.unpack('<I',u.mem_read(signal,4))[0]!=0x12340200:raise ValueError('034 clear signal')
                for at in buffers:
                    if bytes(u.mem_read(at,3840))!=bytes(3840):raise ValueError('034 clear text buffer')
                # The two source-native ranges are adjacent, not isolated:
                # an interior canary would occupy the other valid buffer.
                if bytes(u.mem_read(buffers[0]-4,4))+bytes(u.mem_read(buffers[-1]+3840,4))!=b'\xA6'*8:raise ValueError('034 clear combined buffer outer canaries')
                if bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xA6'*8 or bytes(u.mem_read(stack-160,32))!=b'\xA7'*32:raise ValueError('034 clear outer canary')
                if any(not(stack-128<=a and a+n<=stack or ctx<=a and a+n<=ctx+216 or signal<=a and a+n<=signal+4 or any(lo<=a and a+n<=lo+3840 for lo in buffers)) for a,n in writes):raise ValueError('034 clear write extent')
                key=(mode,fill)
                if label=='source':refs[key]=actual
                elif refs[key]!=actual:raise ValueError('034 source/current clear drift')
                cases.append(dict(image=label,mode=mode,fill=fill,origin_preserved=[52,110]))
    deps=['tools/bench_native_clear_034.py','tools/normal_leading_clear_034.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_leading_clear_cpu_v1/cpu.json',dict(schema=1,passed=True,case_count=len(cases),cases=cases,baseline_rom=BASE,baseline_sha256=BASE_SHA,native_ranges=ranges,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_helpers_substituted=[],modeled_services=dict(BIOS_FastSet32_zero3840=bios_calls),rom_written=False,release_eligible=False,limits='Native F1 full handler and native helpers executed for modes0/1/2, two context fills, default52/110 origin, non-nested stream only. Exact two fixed BIOS FastSet32 fills modeled, no native helper replaced. Not arbitrary caller origin, chip-trader branch acquisition, next E700 execution, GBA pixels or persistence.'))
    print('034 native clear',len(cases),'PASS;NO ROM')


if __name__=='__main__':main()
