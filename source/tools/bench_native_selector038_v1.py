"""038 three original BL callers, complete valid scripts and ABI refusals.

CPU memory fixture only. The original216-byte initializer clear is modeled.
No product ROM or game screenshots are emitted by this tool.
"""
import sys,struct
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from fixture_native038_v1 import construct
from keyitem_rom_selector import INSTALL

OUT='analysis/pending_insertion_500_038_selector_cpu_v1/cpu.json'

def main():
    source,base,meta,image,guards,pool,f=construct();stub,oldstub=f['new_stub'],f['old_stub'];previous=f['previous_wrapper_address']
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(image)+4095)&~4095);u.mem_write(0x08000000,image);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,actor,stack,stop=0x0200FA20,0x02000100,0x02001000,0x03007F00,0x0804FB90;writes=[];clears=[];callers=[];counts=Counter();boundary=False
    def clear(uc,a,n,d):
        dest,size=uc.reg_read(REGS[0]),uc.reg_read(REGS[1]);clears.append((dest,size))
        if (dest,size)!=(ctx,216):raise ValueError('038 exact native clear216 model')
        uc.mem_write(dest,bytes(size));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,clear,begin=0x0800090C,end=0x0800090C);u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop() if boundary else None,begin=previous,end=previous)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:callers.append((uc.reg_read(REGS[0]),uc.reg_read(REGS[1]),uc.reg_read(REGS[14]))),begin=0x08000000+INSTALL,end=0x08000000+INSTALL)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    def execute(g,script,patched=True,native_call=True,scene=None,root=None,caller=None,blob=None,sub=0,day=2,scene_ready=True):
        root=g['root'] if root is None else root;caller=g['caller'] if caller is None else caller;scene=g['scene'] if scene is None else scene;blob=g['native'] if blob is None else blob
        u.mem_write(0x08000000+INSTALL,stub if patched else oldstub);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        for a in (0x02039800,0x0203C800,0x0203D800):u.mem_write(a-4,b'\xAD'*0x1008)
        u.mem_write(root-4,b'\xAD'*4+blob+b'\xAD'*4);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,struct.pack('<I',0x02000200 if scene_ready else 0));u.mem_write(0x02000204,bytes([scene,sub]));u.mem_write(0x02003D57,bytes([day]));u.mem_write(actor,bytes(32))
        if native_call and g['source_class']=='field-board':u.mem_write(actor+4,bytes([script]))
        u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-160,b'\xCC'*160)
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=script if native_call else root;vals[1]=0 if native_call else script;vals[5]=actor if native_call and g['source_class']=='field-board' else vals[5];vals[10]=glob;vals[13]=stack;vals[14]=0x08001001 if native_call else caller
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();callers.clear()
        entry={'native-NPC':0x0804F764,'field-board':0x0806A4FC,'navi-hint':0x0804F7FC}[g['source_class']] if native_call else 0x08000000+INSTALL
        u.emu_start(entry|1,0,count=300000)
        if u.reg_read(UC_ARM_REG_PC)!=(previous if boundary else stop) or callers!=[(root,script,caller)] or clears!=([] if boundary else [(ctx,216)]):raise ValueError(('038 actual caller/initializer boundary',g['archive'],script,callers,clears))
        if any(not(ctx<=a and a+n<=ctx+216 or stack-128<=a and a+n<=stack) for a,n in writes):raise ValueError('038 unexpected persistent RAM write')
        if bytes(u.mem_read(root-4,len(blob)+8))!=b'\xAD'*4+blob+b'\xAD'*4 or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('038 source/context canaries')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR),vals
    def full(g,script,kind,selected=True,**kw):
        nr,nc,nf,_=execute(g,script,patched=False,**kw);pr,pc,pf,_=execute(g,script,**kw);er=nr[:];ec=bytearray(nc)
        if selected:
            effective=next(p for p in guards if (p['scene'],p['root'],p['caller'],p['native'])==(g['scene'],g['root'],g['caller'],g['native']))
            if effective['target']!=g['target'] or effective['scripts']!=g['scripts']:raise ValueError('038 native alias full targets differ')
            off=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=off
            for k,v in [(0x30,effective['clone']),(0x2C,effective['clone']+off),(0x34,effective['clone']+off)]:struct.pack_into('<I',ec,k,v)
        if pr!=er or pc!=bytes(ec) or pf!=nf:raise ValueError(('038 full ABI/context/flags',g['archive'],script,kind))
        counts[kind]+=1
    for g in guards:
        for script in range(g['scripts']):full(g,script,'actual-'+g['source_class']+'-all-valid-scripts')
        for sub in (0,1,2,3,15,255):full(g,0,'resident-identity-independent-of-sub',sub=sub)
        for day in (0,1,2,3,4,5,6,7,255):full(g,0,'resident-identity-independent-of-day',day=day)
        boundary=True;cases=[]
        for scene in (0,0x80,255):cases.append(('wrong-scene',dict(scene=scene)))
        for caller in sorted({0x0804F773,0x0806A507,0x0804F807,0x0804F785,0x08012345}-{g['caller']}):cases.append(('wrong-caller',dict(caller=caller)))
        for root in sorted({0x02038000,0x02039800,0x0203C800,0x0203D800}-{g['root']}):cases.append(('wrong-root',dict(root=root)))
        for script in (g['scripts'],256,0xFFFFFFFF):cases.append(('unsigned-script-bound',dict(script=script)))
        for pos in sorted({0,1,len(g['native'])//2,len(g['native'])-1}):
            blob=bytearray(g['native']);blob[pos]^=1;cases.append(('native-byte-corruption',dict(blob=bytes(blob))))
        cases += [('null-scene-unrelated-caller',dict(caller=0x0804F785,scene_ready=False)),('null-scene-wrong-root',dict(root=0x02038000,scene_ready=False)),('null-scene-invalid-script',dict(script=256,scene_ready=False))]
        for kind,kw in cases:
            kw=dict(kw);script=kw.pop('script',0);regs,context,flags,vals=execute(g,script,native_call=False,**kw);er=vals[:];er[3]=previous|1;er[13]=stack-4
            if regs!=er or struct.unpack('<I',bytes(u.mem_read(stack-4,4)))[0]!=vals[3]:raise ValueError(('038 predecessor stack/register ABI',g['archive'],kind))
            counts[kind]+=1
        boundary=False;print('PASS038 CPU',g['archive'],g['source_class'],g['scripts'],flush=True)
    # Old descriptors not superseded still select through the original chain.
    selected_arcs={g['archive'] for g in guards}
    for key in ('npc035','npc036','npc037'):
        if key not in meta['keyitem_rom']:continue
        for p in meta['keyitem_rom'][key]['placements']:
            arc=p['source_archive']
            if arc in selected_arcs:continue
            matches=[r for r in pool if r['archive']==arc]
            if len(matches)!=1:raise ValueError('038 prior source context lookup')
            r=matches[0];g=dict(guards[0],archive=arc,native=r['payload'],scene=r['scene'],root=r['root'],caller=r['caller_lr'],source_class=r['source_class'])
            for script in (0,1):full(g,script,'prior-'+key+'-consumer',selected=False)
    u.mem_write(0x08000000+INSTALL,stub)
    if bytes(u.mem_read(0x08000000,len(image)))!=image:raise ValueError('038 CPU fixture ROM modified')
    deps=['tools/bench_native_selector038_v1.py','tools/fixture_native038_v1.py','tools/field_native_rom_selector_038_v1.py','tools/prepare_source500_038_v3.py','analysis/pending_insertion_500_038_source_only_v5/preflight_v1.json','analysis/pending_insertion_500_038_native_tails_v1/cpu.json','analysis/pending_insertion_500_038_carry_v2/verification_v1.json']
    public={k:v for k,v in f.items() if k not in ('new_stub','old_stub')}
    frozen_write(ROOT/OUT,dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),vectors=sum(counts.values()),case_counts=dict(counts),descriptor_count=len(guards),source_population_count=len(pool),fixture_only=public,inputs=[{k:(sha(v) if k in ('native','target') else v) for k,v in g.items()} for g in guards],actual_three_original_BL_callers_verified=True,persistent_ram_bytes=0,negative_scope='Stop at original037 wrapper entry before allowing invalid roots/scripts into original consumers',native_clear216_modeled=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['Synthetic native buffers and CPU-only full image, not actual GBA lookup/LZ/residency, screen, timing or038 product build.','Prior unsuperseded typed consumers sampled0/1 only; legacy full population and all500 gameplay not certified.','Primary build must regenerate037 from immutable source, compose guarded carry and enforce exact500 delta/complete writes/rebuild/actual-ROM runtime.']))
    print('PASS038 three caller CPU',sum(counts.values()),'vectors; NO ROM')

if __name__=='__main__':main()
