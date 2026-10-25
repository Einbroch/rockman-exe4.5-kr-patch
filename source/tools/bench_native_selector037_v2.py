"""CPU-only037 cumulative fixture; actual original NPC and board BL callers.

No GBA image is emitted. Negative inputs stop at the predecessor ABI boundary
instead of allowing invalid scripts/roots into the game's original reader.
"""
import struct, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from bench_chip_library import REGS
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_source500_037_v2 import OUT, BASE, BASE_SHA, baseline, ref
from field_native_rom_selector_037_v2 import source_population, wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL


def main():
    cfg, source, base, meta = baseline()
    selection = read(OUT+'/selection.json'); compiled = read(OUT+'/verification_v1.json'); pre = read(OUT+'/preflight_v2.json')
    board_cpu = read(OUT+'/board_caller_cpu_v1.json')
    for p,h in selection['dependencies'].items(): require_hash(ROOT/p,h)
    for p,h in pre['dependencies'].items(): require_hash(ROOT/p,h)
    for t in compiled['tools']: require_hash(ROOT/t['path'],t['sha256'])
    if not all(r['passed'] for r in (compiled,pre,board_cpu)) or pre['units'] != 500 or board_cpu['vectors'] != 190:
        raise ValueError('037 exact500 source/actual-board prerequisites')
    fields = {r['archive']:r for r in pre['archives_detail']}
    compiled_by = {r['archive']:r for r in compiled['archives']}
    pool = source_population(source, {a:dict(source_class=r['source_class'],scene=r['source_reference']['scene'],target_sha256=compiled_by[a]['compiled']['sha256'],script_count=r['script_count']) for a,r in fields.items()})
    image=bytearray(base); guards=[]
    def alloc(data):
        image.extend(b'\xff'*(-len(image)%4)); at=len(image); image.extend(data); return at
    for ar in compiled['archives']:
        for key in ('source_tpl','target_tpl','compiled'): require_hash(ROOT/ar[key]['path'], ar[key]['sha256'])
        r=next(p for p in pool if p['archive']==ar['archive']); native=r['payload']; target=(ROOT/ar['compiled']['path']).read_bytes(); f=fields[ar['archive']]
        if sha(native)!=ar['source_payload_sha256'] or len(native)>=0x1000 or not 1<=ar['script_count']<=256:
            raise ValueError('037 source/size/script capacity')
        np=alloc(native); cp=alloc(target)
        guards.append(dict(archive=ar['archive'],scene=r['scene'],root=r['root'],caller=r['caller_lr'],source_class=r['source_class'],native=native,target=target,native_at=0x08000000+np,clone=0x08000000+cp,scripts=ar['script_count']))
    desc=alloc(b''.join(struct.pack('<7I',g['clone'],g['native_at'],len(g['native']),g['scene'],g['root'],g['caller'],g['scripts']) for g in guards))
    image.extend(b'\xff'*(-len(image)%4)); address=0x08000000+len(image); previous=0x08000000+meta['keyitem_rom']['npc036']['code_offset']
    code,proof=wrap(source,address,previous,0x08000000+desc,len(guards)); image.extend(code)
    stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=address|1))
    if len(stub)!=12 or len(guards)!=70: raise ValueError('037 fixture/stub population')
    oldstub=base[INSTALL:INSTALL+12]; image[INSTALL:INSTALL+12]=stub
    if image[:INSTALL]!=base[:INSTALL] or image[INSTALL+12:len(base)]!=base[INSTALL+12:]: raise ValueError('037 predecessor bytes')
    if unicorn.__version__!='2.1.4': raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(image)+4095)&~4095); u.mem_write(0x08000000,bytes(image)); u.mem_map(0x02000000,0x40000); u.mem_map(0x03000000,0x8000)
    ctx,glob,actor,stack,stop=0x0200FA20,0x02000100,0x02001000,0x03007F00,0x0804FB90
    writes=[]; clears=[]; callers=[]; counts=Counter(); boundary=False
    def clear(uc,a,n,d):
        dest=uc.reg_read(REGS[0]); size=uc.reg_read(REGS[1]); clears.append((dest,size))
        if (dest,size)!=(ctx,216): raise ValueError('Exact native216 clear model')
        uc.mem_write(dest,bytes(size)); uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    def predecessor(uc,a,n,d):
        if boundary: uc.emu_stop()
    u.hook_add(UC_HOOK_CODE,clear,begin=0x0800090C,end=0x0800090C)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE,predecessor,begin=previous,end=previous)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:callers.append((uc.reg_read(REGS[0]),uc.reg_read(REGS[1]),uc.reg_read(REGS[14]))),begin=0x08000000+INSTALL,end=0x08000000+INSTALL)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    def execute(g,script,patched=True,native_call=True,scene=None,root=None,caller=None,blob=None,sub=0,day=2,scene_ready=True):
        root=g['root'] if root is None else root; caller=g['caller'] if caller is None else caller; scene=g['scene'] if scene is None else scene; blob=g['native'] if blob is None else blob
        u.mem_write(0x08000000+INSTALL,stub if patched else oldstub); u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        # Clear the entire root domain so prior longer inputs cannot match tails.
        for native_root in (0x02039800,0x0203C800): u.mem_write(native_root-4,b'\xAD'*0x1008)
        u.mem_write(root-4,b'\xAD'*4+blob+b'\xAD'*4); u.mem_write(glob+44,struct.pack('<I',ctx)); u.mem_write(glob+64,struct.pack('<I',0x02000200 if scene_ready else 0))
        u.mem_write(0x02000204,bytes([scene,sub])); u.mem_write(0x02003D57,bytes([day])); u.mem_write(actor,b'\x00'*32)
        if native_call and g['source_class']=='field-board': u.mem_write(actor+4,bytes([script]))
        u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4); u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB)); u.mem_write(stack-160,b'\xCC'*160)
        vals=[0x1000+i*0x101 for i in range(15)]; vals[0]=script if native_call else root; vals[1]=0 if native_call else script; vals[5]=actor if native_call and g['source_class']=='field-board' else vals[5]; vals[10]=glob; vals[13]=stack; vals[14]=0x08001001 if native_call else caller
        for r,v in zip(REGS,vals): u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033); writes.clear(); clears.clear(); callers.clear()
        entry=(0x0804F764 if g['source_class']=='native-NPC' else 0x0806A4FC) if native_call else 0x08000000+INSTALL
        u.emu_start(entry|1,0,count=220000)
        expected_stop=previous if boundary else stop
        if u.reg_read(UC_ARM_REG_PC)!=expected_stop: raise ValueError(('037 stop',g['archive'],script,hex(u.reg_read(UC_ARM_REG_PC))))
        if callers!=[(root,script,caller)]: raise ValueError('037 actual BL/arguments')
        if clears != ([] if boundary else [(ctx,216)]): raise ValueError('037 modeled context clear count')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-128<=a and a+n<=stack) for a,n in writes): raise ValueError('037 unexpected persistent RAM write')
        if bytes(u.mem_read(root-4,len(blob)+8))!=b'\xAD'*4+blob+b'\xAD'*4 or bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8: raise ValueError('037 source/context canary')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR),vals
    def full(g,script,kind,selected=True,**kw):
        nr,nc,nf,_=execute(g,script,patched=False,**kw); pr,pc,pf,_=execute(g,script,**kw); er=nr[:]; ec=bytearray(nc)
        if selected:
            effective=next(p for p in guards if (p['scene'],p['root'],p['caller'],p['native'])==(g['scene'],g['root'],g['caller'],g['native']))
            if effective['target']!=g['target'] or effective['scripts']!=g['scripts']: raise ValueError('037 native alias target bytes differ')
            off=struct.unpack_from('<H',g['target'],script*2)[0]; er[1]=off
            for k,v in [(0x30,effective['clone']),(0x2C,effective['clone']+off),(0x34,effective['clone']+off)]: struct.pack_into('<I',ec,k,v)
        if pr!=er or pc!=bytes(ec) or pf!=nf: raise ValueError(('037 full ABI/context/flags',g['archive'],script,kind))
        counts[kind]+=1
    for g in guards:
        for script in range(g['scripts']): full(g,script,'actual-'+g['source_class']+'-all-valid-scripts')
        for sub in (0,1,2,3,255): full(g,0,'identity-independent-of-sub',sub=sub)
        for day in (0,1,2,3,4,5,6,7,255): full(g,0,'identity-independent-of-day',day=day)
        boundary=True
        cases=[]
        for scene in sorted({0,0x80,0xA0,0xA1,0xA2,0xA3,255}-{g['scene']}): cases.append(('wrong-scene',dict(scene=scene)))
        for caller in (0x0804F76F,0x0804F785,0x0804F807,0x08012345,0x0806A507 if g['source_class']=='native-NPC' else 0x0804F773): cases.append(('wrong-caller',dict(caller=caller)))
        for root in (0x02038000,0x0203C800 if g['source_class']=='native-NPC' else 0x02039800): cases.append(('wrong-root',dict(root=root)))
        for s in (g['scripts'],256,0xFFFFFFFF): cases.append(('unsigned-script-bound',dict(script=s)))
        for pos in sorted({0,1,len(g['native'])//2,len(g['native'])-1}):
            b=bytearray(g['native']); b[pos]^=1; cases.append(('native-byte-corruption',dict(blob=bytes(b))))
        cases += [('uninitialized-scene-unrelated-caller',dict(caller=0x0804F785,scene_ready=False)),('uninitialized-scene-wrong-root',dict(root=0x02038000,scene_ready=False)),('uninitialized-scene-invalid-script',dict(script=256,scene_ready=False))]
        for kind,kw in cases:
            kw=dict(kw); script=kw.pop('script',0); regs,context,flags,vals=execute(g,script,native_call=False,**kw)
            # SP is intentionally stack-4 at wrapper chaining boundary.
            er=vals[:]; er[3]=previous|1; er[13]=stack-4
            if regs!=er or struct.unpack('<I',bytes(u.mem_read(stack-4,4)))[0]!=vals[3]: raise ValueError(('037 predecessor ABI',kind,g['archive'],regs,er))
            counts[kind]+=1
        boundary=False
        print('PASS037',g['archive'],g['source_class'],g['scripts'],flush=True)
    # Existing036 archives still go through their original wrapper after037 misses.
    for p in meta['keyitem_rom']['npc036']['placements']:
        r=next(r for r in pool if r['archive']==p['source_archive']); g=dict(guards[0],native=r['payload'],scene=r['scene'],root=r['root'],caller=r['caller_lr'],source_class='native-NPC')
        for script in (0,1,127,254): full(g,script,'previous036-reader-regression',selected=False)
    u.mem_write(0x08000000+INSTALL,stub)
    if bytes(u.mem_read(0x08000000,len(image)))!=bytes(image): raise ValueError('037 fixture ROM modified')
    require_hash(ROOT/BASE,BASE_SHA)
    result=dict(schema=1,status='CPU_ONLY037_TYPED_SELECTOR_PASS_NOT_PRODUCT_OR_GBA_RUNTIME',passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(base),source_compile=ref(ROOT/OUT/'verification_v1.json'),preflight=ref(ROOT/OUT/'preflight_v2.json'),board_caller=ref(ROOT/OUT/'board_caller_cpu_v1.json'),vectors=sum(counts.values()),case_counts=dict(counts),descriptor_count=len(guards),source_population_count=len(pool),wrapper=proof,stub=stub_proof,fixture_only=dict(sha256=sha(bytes(image)),bytes=len(image),descriptor_offset=desc,code_address=address,previous_wrapper_address=previous,code_bytes=len(code)),inputs=[dict(archive=g['archive'],scene=g['scene'],root=g['root'],caller=g['caller'],scripts=g['scripts'],clone=g['clone'],native_sha256=sha(g['native']),target_sha256=sha(g['target'])) for g in guards],tools=[ref(ROOT/'tools/bench_native_selector037_v2.py'),ref(ROOT/'tools/field_native_rom_selector_037_v2.py')],native_clear216_modeled=True,negative_scope='Stops at predecessor entry; no invalid original-reader script/root dereference claimed',persistent_ram_bytes=0,rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['CPU memory fixture only; native source buffers are prepared inputs, not actual game LZ acquisition.','Real original NPC and board BL execute; rendering, acquisition, timing, save, product write ownership and rebuild remain unverified.'])
    frozen_write(ROOT/'analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json',result)
    print('PASS037 CPU',sum(counts.values()),'vectors; NO ROM written')


if __name__=='__main__': main()
