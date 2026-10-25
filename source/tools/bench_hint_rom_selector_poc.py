"""CPU-only composed 021/hint-wrapper experiment; does not emit a game ROM."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from hint_rom_selector_poc import wrap
from extended_dialogue import assemble_verified
from keyitem_rom_data import verify_final
from keyitem_rom_selector import INSTALL
from verify_tpi_index import lz77_decompress
from bench_chip_library import REGS
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/'poc/output/pending500_021_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();verify_final(source,rom,m['keyitem_rom'])
    pre=read('analysis/pending_insertion_500_022_preflight_v1/preflight.json');require_hash(ROOT/pre['selection']['path'],pre['selection']['sha256'])
    base=0x09000000;tail=bytearray(23*16);guards=[]
    def alloc(b):
        tail.extend(b'\xff'*(-len(tail)%4));address=base+len(tail);tail.extend(b);return address
    for r in pre['archives']:
        if len(r['source_pointers'])!=1 or r['source_pointers'][0] not in range(0x54180,0x541D4,4):continue
        navi=(r['source_pointers'][0]-0x54180)//4;native=lz77_decompress(source,int(r['archive'],16))[0];folder=ROOT/'analysis/pending_insertion_500_022_preflight_v1'/r['archive'];require_hash(folder/'rebuilt.msg',r['compiled_sha256']);target=(folder/'rebuilt.msg').read_bytes()
        if int.from_bytes(native[:2],'little')!=510 or int.from_bytes(target[:2],'little')!=510:raise ValueError('255-entry descriptor')
        np=alloc(native);cp=alloc(target);struct.pack_into('<4I',tail,navi*16,cp,np,len(native),0)
        guards.append(dict(navi=navi,native=native,target=target,clone=cp,archive=r['archive']))
    if len(guards)!=19:raise ValueError('Finite selected descriptor scope')
    tail.extend(b'\xff'*(-len(tail)%4));at=base+len(tail);code,proof=wrap(source,at,m['keyitem_rom']['entry_address'],base);tail.extend(code)
    stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=at|1))
    if len(stub)!=12 or len(tail)>0x100000:raise ValueError('PoC mapping/stub')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_map(base,0x100000);u.mem_write(base,bytes(tail));u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx=0x0200FA20;glob=0x02000100;stack=0x03007F00;stop=0x0804FB90;writes=[];clears=[];cases=[]
    def stop_cb(uc,address,size,user):uc.emu_stop()
    def clear_cb(uc,address,size,user):
        dest=uc.reg_read(REGS[0]);n=uc.reg_read(REGS[1]);clears.append((dest,n))
        if (dest,n)!=(ctx,216):raise ValueError('Native context clear')
        uc.mem_write(dest,bytes(n));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,stop_cb,begin=stop,end=stop);u.hook_add(UC_HOOK_CODE,clear_cb,begin=0x0800090C,end=0x0800090C);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,user:writes.append((a,n)))
    old_stub=rom[INSTALL:INSTALL+12]
    def execute(g,blob,script,caller,scene,navi,root,patched):
        u.mem_write(0x08000000+INSTALL,stub if patched else old_stub);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12);u.mem_write(root,blob);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,struct.pack('<I',0x02000200));u.mem_write(0x02000201,bytes([navi]));u.mem_write(0x02000204,bytes([scene]));u.mem_write(ctx,bytes([0xA7])*216);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-128,bytes([0xCC])*128)
        vals=[0x1000+i*0x101 for i in range(15)];vals[0]=root;vals[1]=script;vals[10]=glob;vals[13]=stack;vals[14]=caller
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();u.emu_start(0x08000000+INSTALL+1,0,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('Continuation')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-64<=a and a+n<=stack) for a,n in writes):raise ValueError('New persistent RAM write')
        if bytes(u.mem_read(root,len(blob)))!=blob:raise ValueError('Text RAM mutation')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    def case(kind,g,script=11,caller=0x0804F807,scene=0xA3,navi=None,blob=None,root=0x0203D800,selected=True):
        blob=g['native'] if blob is None else blob;navi=g['navi'] if navi is None else navi
        nr,nc,nf=execute(g,blob,script,caller,scene,navi,root,False);pr,pc,pf=execute(g,blob,script,caller,scene,navi,root,True)
        er=nr[:];ec=bytearray(nc)
        if selected:
            off=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=off
            for p,v in ((0x30,g['clone']),(0x2c,g['clone']+off),(0x34,g['clone']+off)):struct.pack_into('<I',ec,p,v)
        if pr!=er or pc!=bytes(ec) or pf!=nf:raise ValueError(f'ABI mismatch {kind}/{g["archive"]}/{script}')
        cases.append(dict(kind=kind,archive=g['archive'],script=script,navi=navi,selected=selected))
    for g in guards:
        for script in range(255):case('selected-script',g,script)
        for pos in sorted({0,1,15,31,32,len(g['native'])//2,len(g['native'])-1}):
            b=bytearray(g['native']);b[pos]^=1;case('changed-native-byte',g,blob=bytes(b),selected=False)
        for scene in (0,0x80,0xA0,0xA2,0xA4,255):case('wrong-scene',g,scene=scene,selected=False)
        for navi in range(23):
            if navi!=g['navi']:case('wrong-navi',g,navi=navi,selected=False)
        for script in (255,256,0xFFFFFFFF):case('wrong-script',g,script,selected=False)
        for caller in (0x0804F805,0x0804F7BD,0x08012345):case('wrong-caller',g,caller=caller,selected=False)
        case('wrong-root',g,root=0x02038000,selected=False)
    # Earlier roots must still select exactly as 021 did, through the old chain.
    for archive,root,caller in [('709408',0x02020800,0x0803497F),('709408',0x02031000,0x0804CC31),('6DD9AC',0x0202B2F4,0x0804F7BD)]:
        r=next(a for a in m['archives'] if a['archive']==archive);b=lz77_decompress(rom,r['rom_offset'])[0]
        for script in (0,10,20):case('retained-reader',guards[0],script,root=root,caller=caller,blob=b,selected=False)
    if bytes(u.mem_read(base,len(tail)))!=bytes(tail):raise ValueError('PoC ROM data mutated')
    out=ROOT/'analysis/pending_insertion_500_022_selector_poc_v1/cpu.json';frozen_write(out,dict(schema=1,passed=True,baseline_rom_sha256=sha(rom),source_sha256=sha(source),vectors=len(cases),case_counts=dict(Counter(c['kind'] for c in cases)),wrapper=proof,stub=stub_proof,poc_bytes_sha256=sha(tail),guards=[dict(archive=g['archive'],navi=g['navi'],native_bytes=len(g['native']),native_sha256=sha(g['native']),target_sha256=sha(g['target']),clone=g['clone']) for g in guards],cases=cases,persistent_ram_bytes=0,rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits='CPU analysis only. Native216-byte clear helper substituted. New selector guards/composed native ABI and 021 fallback verified, not GBA storage/residency/glyphs/timing or natural event proof.'))
    print('PASS hint selector CPU',len(cases),'vectors; no product ROM emitted')

if __name__=='__main__':main()
