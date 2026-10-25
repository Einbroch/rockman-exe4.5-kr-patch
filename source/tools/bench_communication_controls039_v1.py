"""Actual038/source native F000 and EDFF semantics, CPU-memory only.

Not a039 selector/ROM/runtime or external-menu interaction test. No native
function is modeled: selected flag/timer helpers execute their real code.
"""
import sys,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rp=ROOT/'poc/output/pending500_038_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    selected=read('analysis/pending_insertion_500_039_communication_words_v1/verification_v1.json')
    if not selected['passed'] or selected['units']!=500 or selected['units_with_Hangul_syllable_break_proposal'] or selected['rom_written'] or selected['baseline_sha256']!=sha(rom):raise ValueError('039 exact500 word-boundary source prerequisite')
    for p,h in selected['dependencies'].items():require_hash(ROOT/p,h)
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for lo,hi in [(0x51098,0x510B2),(0x510B8,0x510BC),(0x50754,0x507B8),(0x507F0,0x507F4),(0x4FD60,0x4FD78),(0x553E8,0x553F6)]:
        raw=source[lo:hi];ins=list(cs.disasm(raw,0x08000000+lo))
        if raw!=rom[lo:hi] or sum(i.size for i in ins)!=hi-lo:raise ValueError('Native control code identity/extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('Native control Thumb1 roundtrip')
        ranges.append(dict(offset=lo,bytes=hi-lo,sha256=sha(raw)))
    word=lambda at:struct.unpack_from('<I',source,at)[0]
    expected={0x500B8:0x08050755,0x500C4:0x08051099,0x50120:0x080507F1,0x5012C:0x080510B9,0x510B4:0x800}
    for at,value in expected.items():
        if word(at)!=value or rom[at:at+4]!=source[at:at+4]:raise ValueError('Native dispatch/literal contract')
    flags_at=word(0x55414)
    if rom[0x55414:0x55418]!=source[0x55414:0x55418] or not 0x02000000<=flags_at<0x02040000:raise ValueError('Native status-word target')
    extent=(len(rom)+0x2000+4095)&~4095;u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,extent);u.mem_write(0x08000000,rom);readonly=0x08000000+((len(rom)+3)&~3);u.mem_write(readonly,bytes.fromhex('f00000ededff0000'));u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,stack,ram,stop=0x0200FA20,0x03007F00,0x02028000,0x080000C0;writes=[];counts={};vectors=0
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    def execute(kind,mode,root,cf,sf,speed,nzcv):
        command=bytes.fromhex('f00000') if kind=='zero-speed' else bytes.fromhex('edff0000')
        address=root if root==ram else readonly+(0 if kind=='zero-speed' else 4)
        if root==ram:u.mem_write(ram,command)
        initial=bytearray((i*37+speed)&255 for i in range(216));struct.pack_into('<H',initial,0x3E,cf);initial[8]=speed;initial[9]=speed;initial[0x11]=speed
        u.mem_write(ctx-4,b'\xAC'*4+bytes(initial)+b'\xAC'*4);u.mem_write(flags_at,struct.pack('<I',sf));u.mem_write(stack-96,b'\xCC'*96)
        vals=[0x1000+i*0x101 for i in range(15)];vals[4]=address;vals[5]=ctx;vals[6]=132;vals[13]=stack;vals[14]=stop|1
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,nzcv|0x33);writes.clear()
        entry={('zero-speed','draw'):0x08051098,('hold','draw'):0x08050754,('zero-speed','width'):0x080510B8,('hold','width'):0x080507F0}[kind,mode];u.emu_start(entry|1,0,count=1000)
        if u.reg_read(UC_ARM_REG_PC)!=stop:raise ValueError('Native control return')
        actual=bytes(u.mem_read(ctx,216));status=struct.unpack('<I',bytes(u.mem_read(flags_at,4)))[0];expect=bytearray(initial);expected_status=sf
        if mode=='draw':
            if kind=='zero-speed':expect[8]=expect[9]=expect[0x11]=0;struct.pack_into('<H',expect,0x3E,cf|0x800)
            else:struct.pack_into('<H',expect,0x3E,cf|1);expected_status|=8
        delta=0 if (kind,mode)==('hold','draw') else 3 if kind=='zero-speed' else 4
        if actual!=bytes(expect) or status!=expected_status or u.reg_read(REGS[4])!=address+delta:raise ValueError('Native timer/hold/width effect')
        if mode=='draw' and u.reg_read(REGS[0])!=(1 if kind=='zero-speed' else 0):raise ValueError('Native dispatcher continue/hold result')
        if bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAC'*8 or any(not(ctx<=a and a+n<=ctx+216 or flags_at<=a and a+n<=flags_at+4 or stack-64<=a and a+n<=stack) for a,n in writes):raise ValueError('Native control bounded writes/canaries')
        regs=[u.reg_read(r) for r in REGS];regs[4]-=address
        return regs,actual,status,u.reg_read(UC_ARM_REG_CPSR)
    for kind in ('zero-speed','hold'):
        for mode in ('draw','width'):
            count=0
            for cf in (0,1,0x800,0xFFFF):
                for sf in (0,8,0x12345678,0xFFFFFFFF):
                    for speed in (0,1,255):
                        for flags in (0,0x10000000,0xA0000000,0xF0000000):
                            if execute(kind,mode,ram,cf,sf,speed,flags)!=execute(kind,mode,readonly,cf,sf,speed,flags):raise ValueError('RAM/readonly ROM native behavior differs')
                            count+=1;vectors+=1
            counts[kind+'-'+mode]=count
    deps=['tools/bench_communication_controls039_v1.py','analysis/pending_insertion_500_039_communication_words_v1/verification_v1.json','tools/profile_quick_geometry039_v1.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_039_communication_words_v1/native_controls_cpu_v1.json',dict(passed=True,baseline_sha256=sha(rom),source_sha256=sha(source),vectors=vectors,counts=counts,native_code_ranges=ranges,status_word_address=flags_at,native_functions_modeled=False,ROM_written=False,rom_written=False,runtime039_tested=False,release_eligible=False,scope=__doc__,effects=['F000 zeroes three speed/timer bytes, ORs context flag0x800, advances3, continue1.','EDFF retains stream/page and all geometry, ORs context wait bit1 and external status bit8, returns0.','Width consumers advance3/4 without changing context or external status.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['CPU command-interface cases, not039 selector ABI or GBA renderer/menu/network outcome.','No capacity inference for shared nativeRAM02024000. Full menu font/pixel/input/link after exact039 build remains.']))
    print('PASS039 native F000/EDFF draw/width',vectors,'RAM/readonly-ROM pairs; no native function models; NO ROM')

if __name__=='__main__':main()
