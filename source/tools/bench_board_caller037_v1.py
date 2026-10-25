"""Actual036 versus source, original board6A4FC caller; no assigned fake LR.

Unmodified source caller executes its own BL. Context216 zero-fill090C is
modeled explicitly; parsing/gameplay/rendering is outside this CPU boundary.
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
from verify_tpi_index import lz77_decompress

def main():
    pre=read('analysis/pending_insertion_500_037_source_only_v2/preflight_v2.json');rp=ROOT/pre['baseline_rom'];require_hash(rp,pre['baseline_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    if unicorn.__version__!='2.1.4':raise ValueError('Pinned CPU runtime version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    contract=pre['corrected_board_reader']
    if (contract['entry'],contract['source_bl'],contract['derived_return_lr'])!=(0x0806A4FC,0x0806A502,0x0806A507):raise ValueError('Decoded actual source board caller')
    ctx,glob,actor,stack,stop=0x0200FA20,0x02000100,0x02001000,0x03007F00,0x0804FB90
    def engine(image):
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,image);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[];clears=[];callers=[]
        def clear(uc,a,n,d):
            dest=uc.reg_read(REGS[0]);size=uc.reg_read(REGS[1]);clears.append((dest,size))
            if (dest,size)!=(ctx,216):raise ValueError('Exact native clear helper domain')
            uc.mem_write(dest,bytes(size));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
        u.hook_add(UC_HOOK_CODE,clear,begin=0x0800090C,end=0x0800090C);u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:callers.append((uc.reg_read(REGS[0]),uc.reg_read(REGS[1]),uc.reg_read(REGS[14]))),begin=0x0804FB4C,end=0x0804FB4C)
        return u,writes,clears,callers
    engines=[engine(source),engine(rom)];records=[];vectors=0
    for r in pre['archives_detail']:
        if r['source_class']!='field-board':continue
        native=lz77_decompress(source,int(r['archive'],16))[0];root=0x0203C800;count=r['script_count']
        if not 1<=count<=256 or len(native)>=0x1000:raise ValueError('Board root/source declared domain')
        for script in range(count):
            results=[]
            for u,writes,clears,callers in engines:
                u.mem_write(root-4,b'\xA5'*4+native+b'\xA5'*4);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,struct.pack('<I',0x02000200));u.mem_write(0x02000204,bytes([r['source_reference']['scene'],r['source_reference']['sub']]))
                u.mem_write(actor,b'\x00'*0x20);u.mem_write(actor+4,bytes([script]));u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-160,b'\xCC'*160)
                vals=[0x1000+i*0x101 for i in range(15)];vals[5]=actor;vals[10]=glob;vals[13]=stack;vals[14]=0x08001001
                for reg,value in zip(REGS,vals):u.reg_write(reg,value)
                u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();callers.clear();u.emu_start(0x0806A4FD,0,count=100000)
                if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)] or callers!=[(root,script,0x0806A507)]:raise ValueError('Actual source caller/BL/full initializer continuation')
                off=struct.unpack_from('<H',native,script*2)[0];actual=bytes(u.mem_read(ctx,216))
                if struct.unpack_from('<I',actual,0x30)[0]!=root or [struct.unpack_from('<I',actual,k)[0] for k in [0x2C,0x34]]!=[root+off]*2:raise ValueError('Actual native root/script-offset consumption')
                if any(not(ctx<=a and a+n<=ctx+216 or stack-128<=a and a+n<=stack) for a,n in writes):raise ValueError('Unexpected persistent RAM writes')
                if bytes(u.mem_read(root-4,len(native)+8))!=b'\xA5'*4+native+b'\xA5'*4 or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('Board native/context boundaries')
                results.append(([u.reg_read(x) for x in REGS],actual,u.reg_read(UC_ARM_REG_CPSR)))
            if results[0]!=results[1]:raise ValueError('036 changes source board caller ABI/flags/context')
            vectors+=1
        records.append(dict(archive=r['archive'],scripts=count,root=root,source_BL=0x0806A502,actual_return_lr=0x0806A507,all_valid_script_offsets_verified=True))
    frozen_write(ROOT/'analysis/pending_insertion_500_037_source_only_v2/board_caller_cpu_v1.json',dict(passed=True,scope='Original source board6A4FC caller through actual036 composed reader and context init, compared to immutable source CPU; not037 translation or GBA runtime',source_sha256=sha(source),baseline_rom_sha256=sha(rom),vectors=vectors,archives=records,source_clear216_modeled=True,actual_BL_executed=True,registers_context_flags_and_native_source_preserved=True,ROM_written=False,new_units_applied=0,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/bench_board_caller037_v1.py','analysis/pending_insertion_500_037_source_only_v2/preflight_v2.json']}))
    print('PASS actual board caller',vectors,'valid-script CPU cases; realBL6A502->LR6A507;036 matches source; NO037 ROM')

if __name__=='__main__':main()
