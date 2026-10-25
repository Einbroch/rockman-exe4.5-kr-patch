"""CPU-memory-only036 fixture over verified035v2; never emits a GBA ROM."""
import struct,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from bench_chip_library import REGS
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_036_v1 import OUT,BASE,BASE_SHA,baseline,ref
from field_npc_rom_selector_036_v1 import source_population,wrap
from field_npc_rom_product_035_v2 import verify_final as verify035
from inspect_source500_036_v1 import inspect
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL


def main():
    cfg,source,base,m=baseline();verify035(source,base,m['keyitem_rom'])
    s=read(OUT+'/selection.json');v=read(OUT+'/verification_v2.json');loader=read(OUT+'/loader_analysis_v1.json')
    require_hash(ROOT/v['selection']['path'],v['selection']['sha256']);require_hash(ROOT/loader['compile']['path'],loader['compile']['sha256'])
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if inspect(source,base,s,v)!=loader['archives'] or not v['passed'] or v['units']!=500:raise ValueError('036 source/loader prerequisites')
    fields={r['archive']:r for r in loader['archives']};selected={k:r['scene'] for k,r in fields.items()};pool=source_population(source,selected)
    if len(pool)!=84 or len(selected)!=20:raise ValueError('036 declared population')
    # These bytes exist only inside the CPU fixture, not an installed product.
    image=bytearray(base);guards=[]
    def alloc(data):
        image.extend(b'\xff'*(-len(image)%4));at=len(image);image.extend(data);return at
    for ar in v['archives']:
        for name in ['source_tpl','target_tpl','compiled']:require_hash(ROOT/ar[name]['path'],ar[name]['sha256'])
        field=fields[ar['archive']];r=next(r for r in pool if r['archive']==ar['archive']);native=r['payload'];target=(ROOT/ar['compiled']['path']).read_bytes()
        if sha(native)!=ar['source_payload_sha256']:raise ValueError('036 source identity')
        np=alloc(native);cp=alloc(target)
        guards.append(dict(archive=ar['archive'],scene=r['scene'],sub=r['sub'],slot=r['slot'],native=native,target=target,native_at=0x08000000+np,clone=0x08000000+cp))
    desc=alloc(b''.join(struct.pack('<4I',g['clone'],g['native_at'],len(g['native']),g['scene']) for g in guards))
    image.extend(b'\xff'*(-len(image)%4));at=0x08000000+len(image);previous=0x08000000+m['keyitem_rom']['npc035']['code_offset']
    code,proof=wrap(source,at,previous,0x08000000+desc,len(guards));image.extend(code)
    stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=at+1))
    if len(stub)!=12 or proof['caller_lr']!=0x0804F773:raise ValueError('036 caller/stub shape')
    current_stub=base[INSTALL:INSTALL+12];image[INSTALL:INSTALL+12]=stub
    if image[:INSTALL]!=base[:INSTALL] or image[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('036 altered preceding product bytes')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(image)+4095)&~4095);u.mem_write(0x08000000,bytes(image));u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,stack,stop=0x0200FA20,0x02000100,0x03007F00,0x0804FB90
    writes=[];clears=[];case_counts=Counter();checks=0
    def clear(uc,a,n,d):
        dest=uc.reg_read(REGS[0]);length=uc.reg_read(REGS[1]);clears.append((dest,length))
        if (dest,length)!=(ctx,216):raise ValueError('Native clear helper model domain')
        uc.mem_write(dest,bytes(length));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,clear,begin=0x0800090C,end=0x0800090C)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    def execute(g,script,patched,native_call,caller=0x0804F773,scene=None,sub=0,slot=2,root=0x02039800,blob=None,navi=0):
        blob=g['native'] if blob is None else blob;scene=g['scene'] if scene is None else scene
        u.mem_write(0x08000000+INSTALL,stub if patched else current_stub);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(root-4,b'\xAD'*4+blob+b'\xAD'*4);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,struct.pack('<I',0x02000200))
        u.mem_write(0x02000201,bytes([navi]));u.mem_write(0x02000204,bytes([scene,sub]));u.mem_write(0x02003D57,bytes([slot]))
        u.mem_write(ctx-4,b'\xAE'*4+b'\xA7'*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-160,b'\xCC'*160)
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=script if native_call else root;vals[1]=0 if native_call else script;vals[10]=glob;vals[13]=stack;vals[14]=0x08001001 if native_call else caller
        for r,value in zip(REGS,vals):u.reg_write(r,value)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();u.emu_start(0x0804F765 if native_call else 0x08000000+INSTALL+1,0,count=160000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('036 full reader continuation')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-112<=a and a+n<=stack) for a,n in writes):raise ValueError('036 unexpected persistent RAM write')
        if bytes(u.mem_read(root-4,4))+bytes(u.mem_read(root+len(blob),4))!=b'\xAD'*8 or bytes(u.mem_read(root,len(blob)))!=blob:raise ValueError('036 source buffer/canary changed')
        if bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('036 context boundary changed')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    def case(kind,g,script=0,selected_new=False,native_call=False,**kw):
        nonlocal checks
        nr,nc,nf=execute(g,script,False,native_call,**kw);pr,pc,pf=execute(g,script,True,native_call,**kw);er=nr[:];ec=bytearray(nc)
        if selected_new:
            off=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=off
            for offset,value in [(0x30,g['clone']),(0x2C,g['clone']+off),(0x34,g['clone']+off)]:struct.pack_into('<I',ec,offset,value)
        if pr!=er or pc!=bytes(ec) or pf!=nf:raise ValueError(('036 ABI/root/flags',kind,g['archive'],script,kw))
        case_counts[kind]+=1;checks+=1
    for g in guards:
        for script in range(255):case('actual-native-caller-all255',g,script,selected_new=True,native_call=True)
        for scene in sorted(set([0,0x80,0x9F,0xA0,0xA1,0xA2,0xA3,0xB0,255])-{g['scene']}):case('wrong-scene-same-payload',g,scene=scene)
        for pos in sorted({0,1,31,32,509,510,len(g['native'])//2,len(g['native'])-1}):
            b=bytearray(g['native']);b[pos]^=1;case('corrupted-native-identity',g,blob=bytes(b))
        for caller in [0x0804F76F,0x0804F785,0x0804F807,0x08012345]:case('wrong-caller',g,caller=caller)
        for script in [255,256,0xFFFFFFFF]:case('invalid-script',g,script)
        case('wrong-root',g,root=0x02038000)
        for sub in [0,1,2,3,255]:case('loaded-identity-not-mutable-sub',g,sub=sub,selected_new=True)
        for slot in [0,1,2,3,4,5,6,7,8,255]:case('loaded-identity-not-calendar',g,slot=slot,selected_new=True)
        print('PASS036 selector',g['archive'],hex(g['scene']),flush=True)
    g=guards[0]
    for r in pool:
        if r['archive'] not in selected:
            for script in [0,254]:case('unselected-native-population-and-old035-chain',g,script,scene=r['scene'],blob=r['payload'],native_call=True)
    # Exact prior035 clones and all255 native script offsets remain effective.
    for p in m['keyitem_rom']['npc035']['placements']:
        r=next(r for r in pool if r['archive']==p['source_archive'])
        for script in range(255):case('prior035-all255-caller-regression',g,script,scene=0xA0,blob=r['payload'],native_call=True)
    for key,scene in [('hint_archives',0xA3),('b0_hint_archives',0xB0)]:
        for r in m['keyitem_rom'][key]:
            blob=base[r['native_copy_offset']:r['native_copy_offset']+r['native_copy_bytes']]
            for script in [0,10,254]:case('previous-'+key,g,script,root=0x0203D800,caller=0x0804F807,scene=scene,navi=r['navi_index'],blob=blob)
    u.mem_write(0x08000000+INSTALL,stub)
    if bytes(u.mem_read(0x08000000,len(image)))!=bytes(image):raise ValueError('036 fixture ROM bytes modified during execution')
    require_hash(ROOT/BASE,BASE_SHA)
    result=dict(schema=1,status='PROPOSED036_CPU_MEMORY_FIXTURE_PASS_NOT_PRODUCT_OR_GBA_RUNTIME',passed=True,baseline_rom=BASE,baseline_sha256=sha(base),source_sha256=sha(source),source_compile=ref(ROOT/OUT/'verification_v2.json'),loader=ref(ROOT/OUT/'loader_analysis_v1.json'),vectors=checks,case_counts=dict(case_counts),source_population_count=len(pool),descriptor_count=len(guards),wrapper=proof,stub=stub_proof,fixture_only=dict(sha256=sha(bytes(image)),bytes=len(image),descriptor_offset=desc,code_address=at,previous_wrapper_address=previous,code_bytes=len(code)),inputs=[dict(archive=g['archive'],scene=g['scene'],native_sha256=sha(g['native']),target_sha256=sha(g['target']),clone=g['clone']) for g in guards],tools=[ref(ROOT/'tools/bench_npc_selector_036_v1.py'),ref(ROOT/'tools/field_npc_rom_selector_036_v1.py')],native_clear_helper_modeled=True,persistent_ram_bytes=0,rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['CPU-only temporary memory fixture, no GBA image emitted. Source caller executes its real BL and obtainsLR4F773; context216byte clear helper is modeled.','No natural scene/caller acquisition, emulator timing, font/video or saves proved.035 natural actor-selection gate stays open.','Current035 bytes differ only in temporary installation stub; no prior data/font changes. Product installer/build ownership/final writes/repro must still be implemented and checked.'])
    frozen_write(ROOT/'analysis/pending_insertion_500_036_selector_cpu_v1/cpu.json',result)
    print('PASS036 selector CPU',checks,'vectors;NO ROM/NO GBA runtime')


if __name__=='__main__':main()
