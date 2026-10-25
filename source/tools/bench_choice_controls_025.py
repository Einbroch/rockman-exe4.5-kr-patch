"""Source/actual024 F607 centering, width-pass skip and F000 timing CPU.

No BIOS/service substitution; real native query/flag helpers execute. Fixed
CPU fixtures, not new025 GBA cursor/input/outcome or product admission.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/'poc/output/pending500_024_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x51F30,0x51F40),(0x52044,0x520A2),(0x52134,0x5213E),
          (0x3B3B8,0x3B3C2),(0x4FD60,0x4FD82),(0x51098,0x510B2),(0x510B8,0x510BC)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);isa=[]
    for a,b in code:
        raw=source[a:b];decoded=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in decoded)!=len(raw) or rom[a:b]!=raw:raise ValueError('025 bounded native instruction extent/applicability')
        for i in decoded:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:
                raise ValueError('025 ARMv4T native instruction roundtrip')
        isa.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    data=[(0x500C4,4),(0x5012C,4),(0x500DC,4),(0x50144,4),(0x51F40,4),(0x51F60,4),(0x3B468,4),(0x510B4,4),(0x52140,14)]
    for a,n in data:
        if rom[a:a+n]!=source[a:a+n]:raise ValueError('025 native dispatch/literal applicability')
    if (struct.unpack_from('<I',source,0x500DC)[0],struct.unpack_from('<I',source,0x50144)[0],struct.unpack_from('<I',source,0x51F60)[0])!=(0x08051F31,0x08052135,0x08052045):raise ValueError('025 F6 dispatch slots')
    query=struct.unpack_from('<I',source,0x3B468)[0];speed_flag=struct.unpack_from('<I',source,0x510B4)[0]
    ctx,stream,stack,stop=0x0200FA20,0x02020000,0x03007F00,0x080000C0
    reference={};cases=[]
    for label,image in [('source',source),('024',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,data:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,data:writes.append((a,n)))
        def execute(entry,command,before,global_value):
            u.mem_write(ctx,before);u.mem_write(stream,command);u.mem_write(query+8,struct.pack('<I',global_value));u.mem_write(stack-64,b'\xA7'*64)
            values=[0x1000+i*0x101 for i in range(15)];values[4]=stream;values[5]=ctx;values[13]=stack;values[14]=stop|1
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(entry|1,0,count=1000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack or u.reg_read(REGS[4])!=stream+3:
                raise ValueError('025 command continuation/stack')
            if any(not(ctx<=a and a+n<=ctx+216 or stack-32<=a and a+n<=stack) for a,n in writes):raise ValueError('025 command write extent')
            if any(u.reg_read(REGS[i])!=values[i] for i in (5,6,7,8,9,10,11,12)):
                raise ValueError('025 command preserved register drift')
            return bytes(u.mem_read(ctx,216))
        for width in range(1,12):
            for flags in (0,2):
                for mode in (0,1):
                    for origin in (8,52):
                        for row in range(3):
                            before=bytearray(216);before[0x18]=origin;struct.pack_into('<H',before,0x3E,flags);struct.pack_into('<I',before,0x7C,row*10752)
                            actual=execute(0x08052044,bytes([0xF6,7,width]),bytes(before),mode)
                            allocation=11*(width-1)+16;area=(166 if mode else 176) if flags&2 else 240
                            relative=(area-allocation)//2-(0 if flags&2 else origin)
                            wanted=bytearray(before);wanted[0x94]=(relative+origin)&255
                            struct.pack_into('<I',wanted,0x7C,(row*10752+4*(relative&~1))&0xFFFFFFFF)
                            if actual!=wanted:raise ValueError('025 actual F607 placement formula')
                            left=origin+(relative&~1);right=left+allocation
                            if not 8<=left<right<=234:raise ValueError('025 declared choice screen extent')
                            key=('F607',width,flags,mode,origin,row)
                            if label=='source':reference[key]=actual
                            elif actual!=reference[key]:raise ValueError('025 source/product placement mismatch')
                            skipped=execute(0x08052134,bytes([0xF6,7,width]),bytes(before),mode)
                            if skipped!=before:raise ValueError('025 width-pass F607 must not draw/reposition')
                            cases.append(dict(image=label,kind='F607',width=width,flags=flags,global_mode=mode,origin=origin,row=row,allocation=allocation,glyph_left=left,right_bound=right,cursor_x=wanted[0x94]))
        for delay in range(256):
            before=bytearray(216);struct.pack_into('<I',before,0x7C,10752);struct.pack_into('<H',before,0x3E,2)
            actual=execute(0x08051098,bytes([0xF0,0,delay]),bytes(before),0)
            wanted=bytearray(before)
            for at in (8,9,0x11):wanted[at]=delay
            struct.pack_into('<H',wanted,0x3E,2|speed_flag)
            if actual!=wanted:raise ValueError('025 native textSpeed exact effect')
            if execute(0x080510B8,bytes([0xF0,0,delay]),bytes(before),0)!=before:raise ValueError('025 width-pass textSpeed changes geometry')
            cases.append(dict(image=label,kind='F000',delay=delay,row_offset_unchanged=True))
    refs=isa+[dict(offset=a,bytes=n,sha256=sha(source[a:a+n])) for a,n in data]
    out='analysis/pending_insertion_500_025_native_controls_v1/cpu.json'
    frozen_write(ROOT/out,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),
        tool_sha256=sha((ROOT/'tools/bench_choice_controls_025.py').read_bytes()),native_ranges=refs,cases=cases,
        case_count=len(cases),real_native_query_and_flag_helpers_executed=True,substituted_helpers=[],
        horizontal_allocation_formula='11*(nativeWidth-1)+16',mode_query_address=query,zero_delay_geometry_neutral=True,
        rom_written=False,release_eligible=False,limits='Bounded source/actual024 handler CPU and native-code/dispatch identity. '
            'No025 product, extended-glyph width-pass/cursor graph execution, actual choices/outcomes, natural events or presentation approval.'))
    print('PASS025 native F607/F000',len(cases),'source/024 fixtures; no substituted helpers')


if __name__=='__main__':main()
