"""041 subchip102 selector CPU-memory fixture, NOT a ROM or GBA screen test.

Execute original41D84 argument provider through common4FB8E; stop at4FB90.
Only exact native216-byte CpuSet zero is modeled. Native common tail,
default setup after its return, game LZ, glyph rendering and timings are not run.
"""
import sys,struct
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import frozen_write
from fixture_subchip041_v2 import construct,SOURCE
from keyitem_rom_selector import INSTALL


def main():
    source,base,meta,image,guards,f=construct();previous=f['previous_wrapper_address'];stop=0x0804FB90
    if unicorn.__version__!='2.1.4':raise ValueError('041 CPU dependency version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,ui,stack=0x0200FA20,0x02000100,0x02001000,0x03007F00;writes=[];reads=[];calls=[];bios=[];counts=Counter();boundary=False
    def cpuset(uc,a,n,d):
        src,dest,mode=[uc.reg_read(REGS[i]) for i in range(3)];bios.append((src,dest,mode))
        if dest!=ctx or mode!=0x05000036 or not stack-192<=src<stack or bytes(uc.mem_read(src,4))!=bytes(4):raise ValueError('041 exact original CpuSet zero')
        uc.mem_write(ctx,bytes(216));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,cpuset,begin=0x080EC144,end=0x080EC144)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop() if boundary else None,begin=previous,end=previous)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:calls.append(tuple(uc.reg_read(REGS[i]) for i in (0,1,14))),begin=0x08000000+INSTALL,end=0x08000000+INSTALL)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    u.hook_add(UC_HOOK_MEM_READ,lambda uc,t,a,n,v,d:reads.append((a,n)) if f['code_address']<=uc.reg_read(UC_ARM_REG_PC)<f['code_address']+f['wrapper']['proof']['code_bytes'] else None)
    def execute(g,script,patched=True,direct=False,root=None,caller=None,outer=None,native=None,flags=0):
        root=g['root'] if root is None else root;caller=g['caller_lr'] if caller is None else caller;outer=g['outer_lr'] if outer is None else outer;native=g['native'] if native is None else native
        u.mem_write(0x08000000+INSTALL,f['new_stub'] if patched else f['old_stub']);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(g['root']-4,b'\xAD'*0x1008);u.mem_write(g['root'],native);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,bytes(4));u.mem_write(ui,bytes(64));u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-256,b'\xCC'*288)
        if direct:u.mem_write(stack+16,struct.pack('<I',outer))
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=root if direct else script;vals[1]=script if direct else vals[1];vals[5]=ui;vals[10]=glob;vals[13]=stack;vals[14]=caller if direct else 0x080000C1
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,flags|0x33);writes.clear();reads.clear();calls.clear();bios.clear();u.emu_start((0x08000000+INSTALL if direct else 0x08041D84)|1,0,count=1500000)
        if u.reg_read(UC_ARM_REG_PC)!=(previous if boundary else stop) or calls!=[(root,script,caller)] or len(bios)!=(0 if boundary else 1):raise ValueError(('041 original provider/common prefix',g['archive'],script,calls,bios))
        if any(not(ctx<=a and a+n<=ctx+216 or stack-192<=a and a+n<=stack) for a,n in writes):raise ValueError('041 unexpected persistent CPU write')
        if bytes(u.mem_read(g['root']-4,len(native)+8))!=b'\xAD'*4+native+b'\xAD'*4 or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('041 native/context canaries')
        for a,n in reads:
            if not(0x08000000<=a and a+n<=0x08000000+len(image) or stack-60<=a and a+n<=stack+20 or g['root']<=a and a+n<=g['root']+len(native)):raise ValueError(('041 selector read outside declared ROM/stack/native',hex(a),n))
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR),vals,list(reads)
    for g in guards:
        for script in range(g['scripts']):
            nr,nc,nf,_,_=execute(g,script,patched=False);pr,pc,pf,_,rd=execute(g,script);er=nr[:];ec=bytearray(nc)
            selected=script in g['selected_scripts']
            if selected:
                off=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=off
                for at,value in [(0x30,g['clone']),(0x2C,g['clone']+off),(0x34,g['clone']+off)]:struct.pack_into('<I',ec,at,value)
                touched={a+i for a,n in rd for i in range(n) if g['root']<=a+i<g['root']+len(g['native'])}
                if touched!=set(range(g['root'],g['root']+len(g['native']))):raise ValueError('041 successful native comparison must read every source byte')
            if pr!=er or pc!=bytes(ec) or pf!=nf:raise ValueError(('041 source prefix differential registers/context/flags',g['archive'],script))
            counts['selected-script' if selected else 'unselected-script-fallback']+=1
        print('PASS041 subchip CPU',g['archive'],len(g['selected_scripts']),'selected /',g['scripts'],'scripts',flush=True)
    boundary=True
    for g in guards:
        script=g['selected_scripts'][0];cases=[]
        for root in (0,0x02024000,0x02032000,0x0202BA7C,0x02039800,0x04000130):cases.append(('wrong-root',script,dict(root=root)))
        for caller in (0x08047963,0x0804B5AF,0x0804F773,0x08012345):cases.append(('wrong-caller',script,dict(caller=caller)))
        for outer in (0,g['outer_lr']-2,g['outer_lr']+2,0x080448C7,0x0803EFBF):cases.append(('wrong-outer',script,dict(outer=outer)))
        for n in sorted({0,1,2,3,4,5,g['scripts'],31,32,255,256,0xFFFFFFFF}):cases.append(('unselected-or-invalid-script',n,{}))
        for at in sorted({0,1,g['scripts']*2-1,g['scripts']*2,len(g['native'])//2,len(g['native'])-1}):
            b=bytearray(g['native']);b[at]^=1;cases.append(('native-corruption',script,dict(native=bytes(b))))
        for label,n,kw in cases:
            regs,context,flags,vals,rd=execute(g,n,direct=True,**kw);er=vals[:];er[3]=previous|1;er[13]=stack-4
            if regs!=er or struct.unpack('<I',bytes(u.mem_read(stack-4,4)))[0]!=vals[3] or context!=b'\xA7'*76+struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB)+b'\xA7'*(216-92):raise ValueError(('041 exact040 fallback register/stack/context ABI',g['archive'],label,n))
            if label in ('wrong-root','wrong-caller','wrong-outer') and any(g['root']<=a<g['root']+len(g['native']) for a,z in rd):raise ValueError('041 reject wrong ABI before native dereference')
            counts[label]+=1
    u.mem_write(0x08000000+INSTALL,f['new_stub'])
    if bytes(u.mem_read(0x08000000,len(image)))!=image:raise ValueError('041 read-only CPU fixture mutated')
    second=construct()
    if image!=second[3] or f!=second[5]:raise ValueError('041 independently repeated fixture nondeterminism')
    deps=['tools/bench_subchip_selector041_v2.py','tools/fixture_subchip041_v2.py','tools/subchip_rom_component041_v1.py','tools/fixture_subchip041_v1.py','tools/subchip_rom_selector041_v1.py','tools/extended_dialogue.py',SOURCE+'/selection.json',SOURCE+'/verification_v3.json',SOURCE+'/carry_verification_v2.json',SOURCE+'/subchip_boundary_v1.json'];public={k:v for k,v in f.items() if k not in ('new_stub','old_stub')}
    frozen_write(ROOT/SOURCE/'subchip_selector_cpu_v2.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),vectors=sum(counts.values()),case_counts=dict(counts),native_consumer_units=102,descriptors=len(guards),fixture_only=public,independent_fixture_byte_identical=True,selected_mask_prevents_other_scripts=True,whole_native_bytes_compared=True,source_RAM_unchanged=True,all_registers_and_flags_source_prefix_differential=True,rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['CPU-memory-only component, not a041 ROM or full500 integration.','Natural item acquisition and new Hangul rendering, default after common return, shared-state lifetime, full original UI and timings/audio are not established here.','Wrong-context probes stop at unchanged040 wrapper entry, not a whole-game fallback runtime claim.']))
    print('PASS041 subchip102 PREFIX CPU',sum(counts.values()),'vectors; no ROM written')


if __name__=='__main__':main()


