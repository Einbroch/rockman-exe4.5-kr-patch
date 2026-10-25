"""040 three original argument-provider PREFIX CPU ABI; NOT product/GBA.

Execute original common initializer through4FB8E, stop at4FB90. Original0090C
wrapper executes; only exact CpuSet216zero at080EC144 is modeled. The native
common tail, communication8-byte preset and BBS UI continuation are NOT run.
BBS starts at proven4B59C argument tail with fixture UI/post map, not full UI.
"""
import sys,struct
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import frozen_write
from fixture_typed040_v1 import construct,SOURCE
from keyitem_rom_selector import INSTALL


def main():
    source,base,meta,image,guards,pool,f=construct();previous=f['previous_wrapper_address'];stop=0x0804FB90
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,ui,desc,stack=0x0200FA20,0x02000100,0x02001000,0x02001100,0x03007F00;writes=[];reads=[];calls=[];bios=[];counts=Counter();boundary=False
    def cpuset(uc,a,n,d):
        src,dest,mode=[uc.reg_read(REGS[i]) for i in range(3)];bios.append((src,dest,mode))
        if dest!=ctx or mode!=0x05000036 or not stack-160<=src<stack or bytes(uc.mem_read(src,4))!=bytes(4):raise ValueError('040 exact216-byte zero CpuSet model')
        uc.mem_write(ctx,bytes(216));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,cpuset,begin=0x080EC144,end=0x080EC144)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop() if boundary else None,begin=previous,end=previous)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:calls.append(tuple(uc.reg_read(REGS[i]) for i in (0,1,14))),begin=0x08000000+INSTALL,end=0x08000000+INSTALL)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    u.hook_add(UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append((a,n)) if f['code_address']<=uc.reg_read(UC_ARM_REG_PC)<f['code_address']+f['wrapper']['proof']['code_bytes'] else None)
    def execute(p,script,patched=True,direct=False,root=None,caller=None,outer=None,native=None,flags=0):
        root=p['root'] if root is None else root;caller=p['caller_lr'] if caller is None else caller;outer=p['outer_lr'] if outer is None else outer;native=p['payload'] if native is None else native
        u.mem_write(0x08000000+INSTALL,f['new_stub'] if patched else f['old_stub']);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        for a in (0x02024000,0x02032000):u.mem_write(a-4,b'\xAD'*0x7808)
        u.mem_write(p['root'],native);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,bytes(4));u.mem_write(ui,bytes(32));u.mem_write(ui+28,struct.pack('<I',desc));u.mem_write(desc,struct.pack('<II',0x0202E000,0x02032000));u.mem_write(0x02022000,bytes([script&255]));u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-192,b'\xCC'*224)
        if direct:u.mem_write(stack+16,struct.pack('<I',outer))
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=root if direct else script;vals[1]=script if direct else vals[1];vals[5]=ui;vals[10]=glob;vals[13]=stack;vals[14]=caller if direct else 0x080000C1
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,flags|0x33);writes.clear();reads.clear();calls.clear();bios.clear()
        entry=0x08000000+INSTALL if direct else {'communication-help':0x080448BC,'compressed-normal':0x08047958,'battle-BBS-trial':0x0804B59C}[p['source_class']];u.emu_start(entry|1,0,count=1500000)
        if u.reg_read(UC_ARM_REG_PC)!=(previous if boundary else stop) or calls!=[(root,script,caller)] or len(bios)!=(0 if boundary else 1):raise ValueError(('040 provider/common prefix boundary',p['archive'],script,calls,bios))
        if any(not(ctx<=a and a+n<=ctx+216 or stack-160<=a and a+n<=stack) for a,n in writes):raise ValueError('040 unexpected persistent write')
        if bytes(u.mem_read(p['root']-4,len(native)+8))!=b'\xAD'*4+native+b'\xAD'*4 or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('040 native/context canaries')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR),vals,list(reads)
    chosen={g['archive']:g for g in guards}
    for p in pool:
        g=chosen.get(p['archive']);scripts=struct.unpack_from('<H',p['payload'])[0]//2
        for script in range(scripts):
            nr,nc,nf,_,_=execute(p,script,patched=False);pr,pc,pf,_,_=execute(p,script);er=nr[:];ec=bytearray(nc)
            if g:
                off=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=off
                for at,value in [(0x30,g['clone']),(0x2C,g['clone']+off),(0x34,g['clone']+off)]:struct.pack_into('<I',ec,at,value)
            if pr!=er or pc!=bytes(ec) or pf!=nf:raise ValueError(('040 prefix registers/context/flags',p['archive'],script))
            counts['selected-'+p['source_class'] if g else 'unselected-'+p['source_class']]+=1
        print('PASS040 CPU',p['archive'],p['source_class'],scripts,flush=True)
    boundary=True
    for g in guards:
        p=next(p for p in pool if p['archive']==g['archive']);cases=[]
        for root in ({0x02024000,0x02032000,0x02039800,0x0203C800}-{p['root']}):cases.append(('wrong-root',0,dict(root=root)))
        for caller in ({0x0804F7BD,0x08047963,0x0804B5AF,0x0804F773,0x08012345}-{p['caller_lr']}):cases.append(('wrong-caller',0,dict(caller=caller,outer=0)))
        if p['outer_lr']:
            for outer in (0,p['outer_lr']-2,p['outer_lr']+2):cases.append(('wrong-outer',0,dict(outer=outer)))
        for script in (g['scripts'],256,0xFFFFFFFF):cases.append(('script-bound',script,{}))
        for at in sorted({0,1,len(p['payload'])//2,len(p['payload'])-1}):
            b=bytearray(p['payload']);b[at]^=1;cases.append(('native-corruption',0,dict(native=bytes(b))))
        for label,script,kw in cases:
            regs,context,flags,vals,rd=execute(p,script,direct=True,**kw);er=vals[:];er[3]=previous|1;er[13]=stack-4
            if regs!=er or struct.unpack('<I',bytes(u.mem_read(stack-4,4)))[0]!=vals[3]:raise ValueError(('040 parent039 register/stack ABI',g['archive'],label))
            counts[label]+=1
    u.mem_write(0x08000000+INSTALL,f['new_stub'])
    if bytes(u.mem_read(0x08000000,len(image)))!=image:raise ValueError('040 read-only fixture changed')
    deps=['tools/bench_typed_selector040_v1.py','tools/fixture_typed040_v1.py','tools/typed_rom_selector040_v1.py','tools/consumer_links040_v1.py',SOURCE+'/selection.json',SOURCE+'/verification_v1.json'];public={k:v for k,v in f.items() if k not in ('new_stub','old_stub')}
    frozen_write(ROOT/SOURCE/'selector_cpu_v1.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),vectors=sum(counts.values()),case_counts=dict(counts),descriptors=len(guards),source_archives=len(pool),fixture_only=public,rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Common4FB90 tail, full UI/communication preset, source LZ/residency/GBA rendering/timing/audio not proven by CPU prefix fixture.','Source BBS argument tail uses fixture UI/post mapping, not natural acquisition or full BBS routine.','Other old field domains are negative/fallback boundaries, not full current field runtime regression.']))
    print('PASS040 three-domain selector PREFIX CPU',sum(counts.values()),'vectors; NO ROM')


if __name__=='__main__':main()
