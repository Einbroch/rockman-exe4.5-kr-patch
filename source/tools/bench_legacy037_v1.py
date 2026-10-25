"""Actual037 versus036 legacy clone context-initializer CPU ABI regression.

Direct reader ABI at a deliberately unrelated LR, not acquisition/rendering
or a claim that all legacy consumers call this normal-dialogue initializer.
"""
import sys,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_037_v2 import BASE,BASE_SHA
from verify_pending500_002_rom import clones
from keyitem_rom_selector import INSTALL


def main():
    rp=ROOT/'poc/output/pending500_037_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();old=read(BASE.replace('.gba','.json'))
    fixture=read('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json')
    if sha(rom)!=fixture['fixture_only']['sha256']:raise ValueError('037 actual artifact CPU fixture identity')
    if unicorn.__version__!='2.1.4':raise ValueError('Pinned CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,stack,stop=0x0200FA20,0x02000100,0x03007F00,0x0804FB90;writes=[];clears=[];records=[];vectors=0
    def clear(uc,a,n,d):
        dest=uc.reg_read(REGS[0]);size=uc.reg_read(REGS[1]);clears.append((dest,size))
        if (dest,size)!=(ctx,216):raise ValueError('Exact216 context clear model')
        uc.mem_write(dest,bytes(size));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,clear,begin=0x0800090C,end=0x0800090C);u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    def execute(root,flags,patched):
        u.mem_write(0x08000000+INSTALL,(rom if patched else base)[INSTALL:INSTALL+12]);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,bytes(4)) # Deliberately no scene context for unrelated caller.
        u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-160,b'\xCC'*160)
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=root;vals[1]=0;vals[10]=glob;vals[13]=stack;vals[14]=0x08012345
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,flags|0x33);writes.clear();clears.clear();u.emu_start(0x08000000+INSTALL+1,0,count=200000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('037 legacy initializer continuation')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-128<=a and a+n<=stack) for a,n in writes):raise ValueError('037 legacy persistent write')
        if bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('037 context bounds')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    for path,r in clones(old):
        if r.get('compression'):continue # Raw archive roots only; no synthetic parsing of LZ data.
        root=0x08000000+r['rom_offset']
        for flags in (0,0x10000000,0xA0000000,0xF0000000):
            if execute(root,flags,False)!=execute(root,flags,True):raise ValueError(('037 legacy ABI drift',path,flags))
            vectors+=1
        records.append(dict(path=list(path),archive=r['archive'],root=root))
    u.mem_write(0x08000000+INSTALL,rom[INSTALL:INSTALL+12])
    if bytes(u.mem_read(0x08000000,len(rom)))!=rom:raise ValueError('037 CPU fixture ROM mutation')
    frozen_write(ROOT/'analysis/pending500_037_v2/legacy_cpu_v1.json',dict(passed=True,rom_sha256=sha(rom),baseline_sha256=sha(base),scope=__doc__,vectors=vectors,raw_clone_records=records,modeled_native_clear216=True,deliberately_uninitialized_scene_pointer=True,rom_written=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/bench_legacy037_v1.py','analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json']}))
    print('PASS037 actual-image legacy initializer ABI',vectors,'vectors;',len(records),'raw clone roots; NOT full legacy runtime')


if __name__=='__main__':main()
