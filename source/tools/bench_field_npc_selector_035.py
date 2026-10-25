"""CPU-only035 NPC ROM-reader proposal composed over actual034; no game ROM."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_035 import BASE,BASE_SHA
from field_npc_rom_selector_035 import wrap
from extended_dialogue import assemble_verified
from keyitem_rom_data_024 import verify_final
from keyitem_rom_selector import INSTALL
from verify_tpi_index import lz77_decompress
from bench_chip_library import REGS
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

SELECTION='analysis/pending_insertion_500_035_source500_selection_v1/selection.json'
COMPILE='analysis/pending_insertion_500_035_source_compile500_v1/verification.json'
LOADER='analysis/pending_insertion_500_035_loader_analysis_v1/analysis.json'
OUT='analysis/pending_insertion_500_035_npc_selector_cpu_v1/cpu.json'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();m=read(BASE.replace('.gba','.json'));verify_final(source,rom,m['keyitem_rom'])
    sel=read(SELECTION);compiled=read(COMPILE);loader=read(LOADER)
    for report in (sel,compiled,loader):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    base=0x09000000;tail=bytearray(32*16);guards=[]
    def alloc(b):
        tail.extend(b'\xff'*(-len(tail)%4));a=base+len(tail);tail.extend(b);return a
    for r in compiled['archives']:
        link=r['compiled'];require_hash(ROOT/link['path'],link['sha256']);target=(ROOT/link['path']).read_bytes();native=lz77_decompress(source,int(r['archive'],16))[0]
        field=next(f for f in loader['archives'] if f['archive']==r['archive']);slot=field['sub_area']*8+field['time_selector_slot']
        if field['time_selector_slot']>6 or native[:2]!=b'\xfe\x01' or target[:2]!=b'\xfe\x01':raise ValueError('035 finite NPC255 descriptor')
        np=alloc(native);cp=alloc(target);struct.pack_into('<4I',tail,slot*16,cp,np,len(native),0)
        guards.append(dict(slot=slot,sub=field['sub_area'],selector=field['time_selector_slot'],native=native,target=target,clone=cp,archive=r['archive']))
    if len(guards)!=9:raise ValueError('035 finite nine NPC archives')
    tail.extend(b'\xff'*(-len(tail)%4));at=base+len(tail);code,proof=wrap(source,at,m['keyitem_rom']['entry_address'],base);tail.extend(code)
    stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=at|1))
    if len(stub)!=12 or len(tail)>0x100000:raise ValueError('035 CPU-only map')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_map(base,0x100000);u.mem_write(base,bytes(tail));u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,stack,stop=0x0200FA20,0x02000100,0x03007F00,0x0804FB90;writes=[];clears=[];cases=[]
    def clear_cb(uc,address,size,user):
        dest=uc.reg_read(REGS[0]);n=uc.reg_read(REGS[1]);clears.append((dest,n))
        if (dest,n)!=(ctx,216):raise ValueError('Native context clear model domain')
        uc.mem_write(dest,bytes(n));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE,clear_cb,begin=0x0800090C,end=0x0800090C)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
    old_stub=rom[INSTALL:INSTALL+12]
    def execute(blob,script,caller,scene,sub,selector,root,patched,navi=0):
        u.mem_write(0x08000000+INSTALL,stub if patched else old_stub);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(root-4,b'\xAD'*4+blob+b'\xAD'*4);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,struct.pack('<I',0x02000200))
        u.mem_write(0x02000201,bytes([navi]));u.mem_write(0x02000204,bytes([scene,sub]));u.mem_write(0x02003D57,bytes([selector]))
        u.mem_write(ctx-4,b'\xAE'*4+bytes([0xA7])*216+b'\xAE'*4);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-128,bytes([0xCC])*128)
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=root;vals[1]=script;vals[10]=glob;vals[13]=stack;vals[14]=caller
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();u.emu_start(0x08000000+INSTALL+1,0,count=100000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('035 continuation')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-64<=a and a+n<=stack) for a,n in writes):raise ValueError('035 persistent RAM write')
        if bytes(u.mem_read(root,len(blob)))!=blob or bytes(u.mem_read(root-4,4))+bytes(u.mem_read(root+len(blob),4))!=b'\xAD'*8:raise ValueError('035 native text RAM/canary mutation')
        if bytes(u.mem_read(ctx-4,4))+bytes(u.mem_read(ctx+216,4))!=b'\xAE'*8:raise ValueError('035 context extent')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    def case(kind,g,script=0,caller=0x0804F76F,scene=0xA0,sub=None,selector=None,blob=None,root=0x02039800,selected=True,navi=0):
        blob=g['native'] if blob is None else blob;sub=g['sub'] if sub is None else sub;selector=g['selector'] if selector is None else selector
        nr,nc,nf=execute(blob,script,caller,scene,sub,selector,root,False,navi);pr,pc,pf=execute(blob,script,caller,scene,sub,selector,root,True,navi);er=nr[:];ec=bytearray(nc)
        if selected:
            off=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=off
            for p,v in ((0x30,g['clone']),(0x2C,g['clone']+off),(0x34,g['clone']+off)):struct.pack_into('<I',ec,p,v)
        if pr!=er or pc!=bytes(ec) or pf!=nf:raise ValueError('035 composed ABI '+kind+'/'+g['archive']+'/'+str(script))
        cases.append(dict(kind=kind,archive=g['archive'],script=script,scene=scene,sub=sub,selector=selector,selected=selected))
    for g in guards:
        for script in range(255):case('all255-script-offsets',g,script)
        for pos in sorted({0,1,15,31,32,509,510,len(g['native'])//2,len(g['native'])-1}):
            b=bytearray(g['native']);b[pos]^=1;case('changed-native-byte',g,blob=bytes(b),selected=False)
        for scene in (0,0x80,0x9F,0xA1,0xA3,0xB0,255):case('wrong-scene',g,scene=scene,selected=False)
        for sub in (0,1,2,3,4,255):
            if sub!=g['sub']:case('wrong-sub-area',g,sub=sub,selected=False)
        for selval in range(8):
            if selval!=g['selector']:case('wrong-selector',g,selector=selval,selected=False)
        for selval in (8,255):case('out-of-range-selector',g,selector=selval,selected=False)
        for script in (255,256,0xFFFFFFFF):case('out-of-range-script',g,script,selected=False)
        for caller in (0x0804F781,0x0804F807,0x0804F76D,0x0804F7BD,0x08012345):case('wrong-caller',g,caller=caller,selected=False)
        case('wrong-root',g,root=0x02038000,selected=False)
        print('035 NPC CPU',g['archive'],'PASS',flush=True)
    for archive,root,caller in [('709408',0x02020800,0x0803497F),('709408',0x02031000,0x0804CC31),('6DD9AC',0x0202B2F4,0x0804F7BD)]:
        r=next(a for a in m['archives'] if a['archive']==archive);blob=lz77_decompress(rom,r['rom_offset'])[0]
        for script in (0,10,20):case('retained-previous-reader',guards[0],script,root=root,caller=caller,blob=blob,selected=False)
    for name,scene in [('hint_archives',0xA3),('b0_hint_archives',0xB0)]:
        for r in m['keyitem_rom'][name]:
            blob=rom[r['native_copy_offset']:r['native_copy_offset']+r['native_copy_bytes']]
            for script in (0,10,254):case('retained-'+name,guards[0],script,root=0x0203D800,caller=0x0804F807,scene=scene,navi=r['navi_index'],blob=blob,selected=False)
    u.mem_write(0x08000000+INSTALL,old_stub)
    if bytes(u.mem_read(base,len(tail)))!=bytes(tail) or bytes(u.mem_read(0x08000000,len(rom)))!=rom:raise ValueError('035 CPU-only ROM mutation')
    deps=[SELECTION,COMPILE,LOADER,'tools/bench_field_npc_selector_035.py','tools/field_npc_rom_selector_035.py','tools/keyitem_rom_data_024.py','tools/extended_dialogue.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='CPU_ONLY_NPC_ROM_READER_PROPOSAL_PASS_NOT_PRODUCT',passed=True,baseline_rom=BASE,baseline_rom_sha256=sha(rom),source_sha256=sha(source),vectors=len(cases),case_counts=dict(Counter(c['kind'] for c in cases)),
        wrapper=proof,stub=stub_proof,poc_bytes_sha256=sha(tail),guards=[dict(archive=g['archive'],sub_area=g['sub'],selector=g['selector'],native_bytes=len(g['native']),native_sha256=sha(g['native']),target_sha256=sha(g['target']),clone=g['clone']) for g in guards],cases=cases,
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},persistent_ram_bytes=0,rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,
        limits='CPU-only proposed reader composed over actual034. Original compressed sources/table/loader and RAM byte extents retained. Exact native216-byte context clear helper substituted; no new decompression modeled. Does not prove natural A0 lookup/caller, GBA timing, font/video, primary placement/integration or persistence.'))
    print('035 NPC composed CPU',len(cases),'PASS;NO ROM')

if __name__=='__main__':main()
