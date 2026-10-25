"""039 outer/helper and common initializer PREFIX CPU ABI, NOT a product ROM.

Execute native0090C/00956 wrappers; only CpuSet BIOS boundary080EC144 is
modeled for the exact216-byte zero-fill and8-byte preset-copy operations.
Initializer continuation4FB90..4FC20 (graphics/audio/status work) is explicitly
skipped to its original pop epilogue. This is NOT complete native initialization.
Invalid inputs stop at038 entry, not passed into an unsafe native consumer.
"""
import sys,struct
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import frozen_write
from fixture_communication039_v1 import construct,OUT
from keyitem_rom_selector import INSTALL
from communication_rom_selector039_v1 import ROOT_ADDRESS,INNER_LR,OUTER_LR


def main():
    source,base,meta,image,guards,pool,f=construct();previous=f['previous_wrapper_address'];stop=0x080000C0
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,stack=0x0200FA20,0x02000100,0x03007F00;writes=[];reads=[];bios=[];calls=[];counts=Counter();boundary=False
    def cpuset(uc,a,n,d):
        src,dest,mode=[uc.reg_read(REGS[i]) for i in range(3)];bios.append((src,dest,mode))
        if dest==ctx and mode==0x05000036 and stack-160<=src<stack and bytes(uc.mem_read(src,4))==bytes(4):uc.mem_write(dest,bytes(216))
        elif (src,dest,mode)==(0x0804F7D0,ctx+0x68,4):uc.mem_write(dest,bytes(uc.mem_read(src,8)))
        else:raise ValueError(('039 bounded CpuSet model',src,dest,mode))
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,cpuset,begin=0x080EC144,end=0x080EC144)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.reg_write(UC_ARM_REG_PC,0x0804FC21),begin=0x0804FB90,end=0x0804FB90)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop() if boundary else None,begin=previous,end=previous)
    def common(uc,a,n,d):
        sp=uc.reg_read(REGS[13]);calls.append((uc.reg_read(REGS[0]),uc.reg_read(REGS[1]),uc.reg_read(REGS[14]),struct.unpack('<I',bytes(uc.mem_read(sp+16,4)))[0]))
    u.hook_add(UC_HOOK_CODE,common,begin=0x08000000+INSTALL,end=0x08000000+INSTALL)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    u.hook_add(UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append((a,n)) if f['code_address']<=uc.reg_read(UC_ARM_REG_PC)<f['code_address']+f['wrapper']['proof']['code_bytes'] else None)
    def execute(native,script,patched=True,direct=False,root=ROOT_ADDRESS,inner=INNER_LR,outer=OUTER_LR,flags=0):
        u.mem_write(0x08000000+INSTALL,f['new_stub'] if patched else f['old_stub']);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(ROOT_ADDRESS-4,b'\xAD'*0x4008);u.mem_write(ROOT_ADDRESS,native);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,bytes(4))
        u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-192,b'\xCC'*224)
        if direct:u.mem_write(stack+16,struct.pack('<I',outer))
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=root if direct else script;vals[1]=script if direct else vals[1];vals[10]=glob;vals[13]=stack;vals[14]=inner if direct else stop|1
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,flags|0x33);writes.clear();reads.clear();bios.clear();calls.clear()
        try:u.emu_start((0x08000000+INSTALL if direct else 0x080448BC)|1,0,count=600000)
        except unicorn.UcError as exc:raise ValueError(('039 CPU execution',hex(u.reg_read(UC_ARM_REG_PC)),hex(u.reg_read(UC_ARM_REG_CPSR)),bios)) from exc
        if u.reg_read(UC_ARM_REG_PC)!=(previous if boundary else stop):raise ValueError('039 native return/instruction budget')
        expected_call=(root,script,inner,outer) if direct else (ROOT_ADDRESS,script,INNER_LR,OUTER_LR)
        if calls!=[expected_call]:raise ValueError(('039 actual nested callers',calls,expected_call))
        if len(bios)!=(0 if boundary else 2):raise ValueError('039 original clear/preset operations')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-160<=a and a+n<=stack) for a,n in writes):raise ValueError('039 persistent write escaped context/stack')
        if bytes(u.mem_read(ROOT_ADDRESS,len(native)))!=native or bytes(u.mem_read(ROOT_ADDRESS-4,4))!=b'\xAD'*4 or bytes(u.mem_read(ROOT_ADDRESS+len(native),4))!=b'\xAD'*4 or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('039 native/context canaries')
        if any(glob+64<=a<glob+68 or a==0 for a,n in reads):raise ValueError('039 unrelated scene dereference')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR),vals,list(reads)
    chosen={g['archive']:g for g in guards}
    for p in pool:
        g=chosen.get(p['archive']);scripts=struct.unpack_from('<H',p['payload'])[0]//2
        for script in range(scripts):
            for flags in (0,0xF0000000):
                nr,nc,nf,_,_=execute(p['payload'],script,patched=False,flags=flags);pr,pc,pf,_,_=execute(p['payload'],script,flags=flags);ec=bytearray(nc)
                if g:
                    off=struct.unpack_from('<H',g['target'],script*2)[0]
                    for at,value in [(0x30,g['clone']),(0x2C,g['clone']+off),(0x34,g['clone']+off)]:struct.pack_into('<I',ec,at,value)
                if pr!=nr or pc!=bytes(ec) or pf!=nf:raise ValueError(('039 full helper registers/context/flags',p['archive'],script,pr,nr))
                if pc[0x68:0x70]!=source[0x4F7D0:0x4F7D8] or pr[13]!=stack or pr[14]!=0x08000963:raise ValueError('039 actual8-byte copy and nested return ABI')
                counts['selected-all-valid-scripts' if g else 'unselected-communication-all-valid-scripts']+=1
        print('PASS039 CPU',p['archive'],scripts,'selected' if g else 'original',flush=True)
    boundary=True
    for g in guards:
        cases=[]
        for root in (0x02039800,0x0203C800,0x0203D800,0x02038000):cases.append(('wrong-root',0,dict(root=root)))
        for inner in (0x0804F773,0x0806A507,0x0804F807,0x0804F785):cases.append(('wrong-inner',0,dict(inner=inner)))
        for outer in (0,0x08012345,OUTER_LR-2,OUTER_LR+2):cases.append(('wrong-outer',0,dict(outer=outer)))
        for script in (g['scripts'],255,256,0xFFFFFFFF):cases.append(('script-bound',script,{}))
        for pos in sorted({0,1,len(g['native'])//2,len(g['native'])-1}):
            native=bytearray(g['native']);native[pos]^=1;cases.append(('native-corruption',0,dict(native=bytes(native))))
        for kind,script,kw in cases:
            kw=dict(kw);native=kw.pop('native',g['native']);regs,context,flags,vals,rd=execute(native,script,direct=True,**kw);expected=vals[:];expected[3]=previous|1;expected[13]=stack-4
            if regs!=expected or struct.unpack('<I',bytes(u.mem_read(stack-4,4)))[0]!=vals[3]:raise ValueError(('039 parent register/stack ABI',kind))
            if kind in ('wrong-root','wrong-inner') or script>=256:
                if any(a==stack+16 or ROOT_ADDRESS<=a<ROOT_ADDRESS+len(native) for a,n in rd):raise ValueError('039 early gate read stack/native before eligibility')
            counts[kind]+=1
    u.mem_write(0x08000000+INSTALL,f['new_stub'])
    if bytes(u.mem_read(0x08000000,len(image)))!=image:raise ValueError('039 readonly fixture changed')
    deps=['tools/bench_communication_selector039_v2.py','tools/fixture_communication039_v1.py','tools/communication_rom_selector039_v1.py',OUT+'/selection.json',OUT+'/verification_v1.json',OUT+'/native_controls_cpu_v1.json',OUT+'/baseline_boundary_v2.json']
    public={k:v for k,v in f.items() if k not in ('new_stub','old_stub')}
    frozen_write(ROOT/OUT/'selector_cpu_v2.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),vectors=sum(counts.values()),case_counts=dict(counts),descriptor_count=len(guards),source_archives=len(pool),source_table_entries=23,fixture_only=public,actual_original_outer_helper_common_prefix_executed=True,native_initializer_continuation_skipped=[0x0804FB90,0x0804FC20],native_preset_copy_verified=True,scene_pointer_dereferenced=False,persistent_ram_bytes=0,CpuSet_BIOS_model='Only exact216-byte zero fill /8-byte preset copy; actual0090C and00956 wrappers execute',rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['CPU-memory fixture only; NOT039 product build or GBA loader, rendering, interaction, multiplayer, hardware, timing or audio proof.','Common initializer tail4FB90..4FC20 skipped; no complete initializer/helper-native-state equivalence claim.','Malformed inputs stop at038 predecessor before original code; all23 communication table entries covered statically /21 unique archives all valid scripts executed.','Prior field domains early-fallback stack/register boundary covered; full old field execution remains required in actual product regression.']))
    print('PASS039 selector CPU',sum(counts.values()),'vectors; NO ROM')


if __name__=='__main__':main()
