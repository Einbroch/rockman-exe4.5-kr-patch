"""CPU-only composed B0-reader experiment; NO product ROM is written."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from hint_rom_selector import wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL
from keyitem_rom_data import verify_final
from bench_chip_library import REGS
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR


def main():
    extraction_path='analysis/field_b0_hints_v1/extraction.json'
    compiled_path='analysis/pending_insertion_500_023_b0_compile_v3/verification.json'
    e=read(extraction_path);compiled=read(compiled_path)
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,e['source_sha256']);source=sp.read_bytes()
    rp=ROOT/e['baseline_rom'];require_hash(rp,e['baseline_sha256']);base=rp.read_bytes();m=read(rp.with_suffix('.json'))
    verify_final(source,base,m['keyitem_rom'])
    if compiled['baseline_sha256']!=sha(base) or not compiled['passed'] or compiled['rom_written']:raise ValueError('Mechanical payload binding')
    by={r['archive']:r for r in compiled['archives']}
    fixture=bytearray(base);records=[];table=[(0,0,0,0)]*23
    def alloc(blob):
        fixture.extend(b'\xff'*(-len(fixture)%4));at=len(fixture);fixture.extend(blob);return at
    for r in e['archives']:
        arc=r['archive'];path=by[arc]['compiled'];require_hash(ROOT/path['path'],path['sha256']);target=(ROOT/path['path']).read_bytes()
        native_path=ROOT/'analysis/field_b0_hints_v1'/arc/(arc+'.msg');require_hash(native_path,r['source_payload_sha256']);native=native_path.read_bytes()
        np=alloc(native);cp=alloc(target);table[r['navi_index']]=(cp+0x08000000,np+0x08000000,len(native),0)
        records.append(dict(archive=arc,navi=r['navi_index'],native=native,target=target,clone=cp+0x08000000))
    table_at=alloc(b''.join(struct.pack('<4I',*row) for row in table))
    fixture.extend(b'\xff'*(-len(fixture)%4));code_at=0x08000000+len(fixture)
    blob,proof=wrap(source,code_at,m['keyitem_rom']['entry_address'],0x08000000+table_at,scene=0xB0)
    fixture.extend(blob)
    stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=code_at|1))
    original_stub=base[INSTALL:INSTALL+12]
    if len(stub)!=12:raise ValueError('Single composed reader installer extent')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version drift')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u.mem_map(0x08000000,(len(fixture)+4095)&~4095);u.mem_write(0x08000000,bytes(fixture))
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    ctx,glob,state,stack,stop=0x0200FA20,0x02000100,0x02000200,0x03007F00,0x0804FB90
    writes=[];clears=[];cases=[]
    def clear(uc,a,n,data):
        dest,size=uc.reg_read(REGS[0]),uc.reg_read(REGS[1])
        if (dest,size)!=(ctx,216):raise ValueError('Native reader216-byte clear contract')
        clears.append((dest,size));uc.mem_write(dest,bytes(size));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,clear,begin=0x0800090C,end=0x0800090C)
    u.hook_add(UC_HOOK_CODE,lambda uc,a,n,data:uc.emu_stop(),begin=stop,end=stop)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,data:writes.append((a,n)))
    def execute(g,script,caller,scene,navi,native,root,enabled):
        u.mem_write(0x08000000+INSTALL,stub if enabled else original_stub);u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(root,native);u.mem_write(glob+44,struct.pack('<I',ctx));u.mem_write(glob+64,struct.pack('<I',state));u.mem_write(state+1,bytes([navi]));u.mem_write(state+4,bytes([scene]));u.mem_write(ctx,bytes([0xA7])*216);u.mem_write(ctx+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-128,bytes([0xCC])*128)
        values=[0x1000+i*0x101 for i in range(15)];values[0]=root;values[1]=script;values[10]=glob;values[13]=stack;values[14]=caller
        for r,v in zip(REGS,values):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear()
        u.emu_start(0x08000000+INSTALL+1,0,count=45000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(ctx,216)]:raise ValueError('Reader continuation/clear')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-96<=a and a+n<=stack) for a,n in writes):raise ValueError('Reader unexpected persistent RAM write')
        if bytes(u.mem_read(root,len(native)))!=native:raise ValueError('Native text RAM mutation')
        return [u.reg_read(r) for r in REGS],bytes(u.mem_read(ctx,216)),u.reg_read(UC_ARM_REG_CPSR)
    def case(kind,g,script=10,caller=0x0804F807,scene=0xB0,navi=None,native=None,root=0x0203D800,selected=True):
        navi=g['navi'] if navi is None else navi;native=g['native'] if native is None else native
        nr,nc,nf=execute(g,script,caller,scene,navi,native,root,False);ar,ac,af=execute(g,script,caller,scene,navi,native,root,True)
        er=nr[:];ec=bytearray(nc)
        if selected:
            offset=struct.unpack_from('<H',g['target'],script*2)[0];er[1]=offset
            for pos,value in ((0x30,g['clone']),(0x2C,g['clone']+offset),(0x34,g['clone']+offset)):struct.pack_into('<I',ec,pos,value)
        if ar!=er or ac!=bytes(ec) or af!=nf:raise ValueError('Composed ABI/fallback '+kind+'/'+g['archive']+'/'+str(script))
        cases.append(dict(kind=kind,archive=g['archive'],script=script,navi=navi,selected=selected))
    for g in records:
        for script in range(255):case('selected-script',g,script)
        for pos in sorted({0,1,31,len(g['native'])//2,len(g['native'])-1}):
            changed=bytearray(g['native']);changed[pos]^=1;case('changed-native-byte',g,native=bytes(changed),selected=False)
        for scene in (0,0xA3,0xAF,0xB1,255):case('wrong-scene',g,scene=scene,selected=False)
        for navi in range(23):
            if navi!=g['navi']:case('wrong-navi',g,navi=navi,selected=False)
        for script in (255,256,0xFFFFFFFF):case('wrong-script',g,script,selected=False)
        for caller in (0x0804F805,0x0804F7BD,0x08012345):case('wrong-caller',g,caller=caller,selected=False)
        case('wrong-root',g,root=0x02038000,selected=False)
    # Real baseline A3 clones must stay selected by the preceding chain.
    for old in m['keyitem_rom']['hint_archives']:
        native=base[old['native_copy_offset']:old['native_copy_offset']+old['native_copy_bytes']]
        g=dict(archive=old['archive'],navi=old['navi_index'],native=native,target=b'',clone=0)
        for script in (0,10,11,15,254):case('retained-A3-reader',g,script,scene=0xA3,selected=False)
    u.mem_write(0x08000000+INSTALL,original_stub)
    if bytes(u.mem_read(0x08000000,len(fixture)))!=bytes(fixture):raise ValueError('CPU experiment mutated unrelated ROM bytes')
    deps=[extraction_path,compiled_path,'tools/hint_rom_selector.py','tools/bench_field_b0_reader_023.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_023_reader_v1/cpu.json',dict(schema=1,passed=True,baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(base),source_sha256=sha(source),fixture_bytes=len(fixture),fixture_sha256=sha(fixture),fixture_materialization='CPU memory only; not a product ROM',dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},wrapper=proof,stub=stub_proof,descriptor_slots=23,archives=21,vectors=len(cases),case_counts=dict(Counter(c['kind'] for c in cases)),cases=cases,native_ram_byte_identity=True,previous_A3_chain_preserved=True,persistent_ram_bytes=0,only_substituted_helper='Native216-byte clear CPU contract',rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits='Composed CPU reader selection/ABI only, using canonical-LF mechanical023 payloads in a fixture appended beyond022. Final candidate-layout clones, product write plan/registry, own-ROM GBA load/branch/variable/display/clearing/reentry remain required.'))
    require_hash(rp,e['baseline_sha256'])
    print('PASS composed B0 reader CPU',len(cases),'vectors; retained A3 path; no product ROM written')


if __name__=='__main__':main()
