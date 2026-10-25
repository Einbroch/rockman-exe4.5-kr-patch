"""Original resident provider with selective copy-pointer CPU shim fixture."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE,UC_HOOK_CODE
from hangul_keyboard_copy_shim import assemble
from hangul_mixed_cache_bridge import stream
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB


def main():
    root=ROOT/'analysis/hangul_keyboard_v1';dep=root/'cpu_cache_bridge/report.json'
    d=json.loads(dep.read_text(encoding='utf8'))
    if not d['passed'] or d['rom_integrated']:raise ValueError('cache scope')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dep.parent/n,h)
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(play,identity);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    composer=root/'cpu_composer/report.json';co=json.loads(composer.read_text(encoding='utf8'))
    for n,h in co['artifacts'].items():require_hash(composer.parent/n,h)
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b,pc in ((0x1EF91C,0x1EF966,0x03006A1C),(0x94C,0x956,0x0800094C)):
        raw=rom[a:b]
        if current[a:b]!=raw:raise ValueError('native source changed')
        ins=list(cs.disasm(raw,pc))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('native boundaries')
        for i in ins:
            if i.size!=2 or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native Thumb roundtrip')
        regions.append(dict(offset=a,bytes=len(raw),sha256=sha(raw)))
    if struct.unpack_from('<I',rom,0x1EF96C)[0]!=0x0800094D:raise ValueError('copy literal source')
    blob,isa=assemble();out=root/'cpu_copy_shim';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    table=(root/'cpu_composer/transitions.bin').read_bytes()
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08F03000,4096);u.mem_write(0x08F03000,blob);u.mem_protect(0x08F03000,4096,UC_PROT_READ|UC_PROT_EXEC)
    n=(len(table)+4095)&~4095;u.mem_map(0x09000000,n);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,n,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_map(0x0FF00000,4096)
    u.mem_protect(0x03005000,0x2000,UC_PROT_READ|UC_PROT_EXEC)
    src,ctx,script,sp,stop=0x0200FC54,0x0200FBE0,0x02003000,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(new_layout_calls=0,empty_fallbacks=0,legacy_provider_comparisons=0,direct_copy_ABI_checks=0,maximum_stream_bytes=0)
    def run(index,slot,new=None,patched=True):
        overlay=bytearray(rom[0x1EE700:0x1EFF74])
        if patched:struct.pack_into('<I',overlay,0x6A6C-0x5800,0x08F03001)
        u.mem_write(0x03005800,bytes(overlay))
        u.ctl_remove_cache(0x03005800,0x03007000)
        u.mem_write(0x02000000,bytes(range(256))*1024)
        ptr,length=struct.unpack_from('<II',rom,0x526D0+index*8)
        payload=bytes((i*7+33)&255 for i in range(length));u.mem_write(ptr,payload)
        u.mem_write(script,bytes([249,12,index]));u.mem_write(ctx,b'\0'*64)
        u.mem_write(ctx+0x2C,struct.pack('<II',7,slot));dest=0x020155F0+slot*128
        u.mem_write(dest-4,b'\xA7'*(max(length,41)+8))
        if new is not None:u.mem_write(src,new)
        before=bytearray(u.mem_read(0x02000000,0x40000))
        if new is not None:
            try:wanted=stream(new)
            except ValueError:wanted=b'\xE5';stats['empty_fallbacks']+=1
        else:wanted=payload
        before[dest-0x02000000:dest-0x02000000+len(wanted)]=wanted
        for offset,value in ((0x24,dest),(0x28,script+3),(0x2C,8),(0x30,slot+1)):
            struct.pack_into('<I',before,ctx-0x02000000+offset,value)
        u.mem_write(sp-180,b'\x5A'*180);u.reg_write(UC_ARM_REG_CPSR,0x30)
        initial=[script]+[0x13579000+i for i in range(1,13)]
        for r,v in zip(regs,initial):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
        u.emu_start(0x03006A1D,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or bytes(u.mem_read(sp-180,4))!=b'\x5A'*4:raise ValueError('provider stack/return')
        final=tuple(u.reg_read(r) for r in regs)+(u.reg_read(UC_ARM_REG_CPSR)&0xF0000000,)
        if final!=(dest,*initial[1:],0):raise ValueError('native provider live-outs')
        if bytes(u.mem_read(0x02000000,0x40000))!=bytes(before):raise ValueError('provider source/context/cache write mismatch')
        if any(not(dest<=a and a+n<=dest+len(wanted) or ctx+0x24<=a and a+n<=ctx+0x34 or sp-176<=a and a+n<=sp) for a,n in writes):raise ValueError('unexpected provider write')
        return final,bytes(before),tuple(writes)
    # Old calls include512-byte generic buffers: gate must not reinterpret them.
    for index in range(32):
        for slot in (0,1,3):
            if index==0 and slot==0:continue
            expected=run(index,slot,patched=False);actual=run(index,slot)
            if expected[:2]!=actual[:2]:raise ValueError('legacy provider regression')
            stats['legacy_provider_comparisons']+=1
    for cap in range(1,11):
        for n in range(cap+1):
            for w in (0,11171,11172,11190,tag(b'\x9B'),tag(b'\xE4\x98'),tag(b'\xE4\xE5')):
                c=MixedReplay(cap);c.model.state=Snapshot((w,)*n,0,None);c._rebase();raw=c.serialize()
                run(0,0,raw);stats['new_layout_calls']+=1;stats['maximum_stream_bytes']=max(stats['maximum_stream_bytes'],len(stream(raw)))
    valid=MixedReplay(4).serialize()
    for at in range(76):
        raw=bytearray(valid);raw[at]^=255;run(0,0,bytes(raw));stats['new_layout_calls']+=1
    # Direct leaf ABI check: provider's final ADDS would hide copy NZCV errors.
    leaf_stop=[0]
    u.hook_add(UC_HOOK_CODE,lambda cpu,pc,size,user:cpu.emu_stop() if pc==leaf_stop[0] else None)
    for oldsrc,dest,length,lr,new in (
        (0x0200FC80,0x020155F0,32,0x03006A4C,valid),
        (0x0200FC80,0x020155F0,32,0x03006A4C,b'\0'*76),
        (0x0200FC81,0x020155F0,32,stop,None),
        (0x0200FC80,0x02015670,32,stop,None),
        (0x0200FC80,0x020155F0,31,stop,None),
        (0x0200FC80,0x020155F0,32,stop,None),
        (0x02026080,0x020155F0,512,stop,None)):
        u.mem_write(0x02000000,bytes(range(256))*1024)
        if new is not None:u.mem_write(src,new)
        before=bytearray(u.mem_read(0x02000000,0x40000))
        oldbyte=before[oldsrc-0x02000000]
        if new is None:wanted=bytes(u.mem_read(oldsrc,length))
        else:
            try:wanted=stream(new)
            except ValueError:wanted=b'\xE5'
        before[dest-0x02000000:dest-0x02000000+len(wanted)]=wanted
        u.mem_write(sp-136,b'\x5A'*136);u.reg_write(UC_ARM_REG_CPSR,0x30)
        initial=[oldsrc,dest,length,0x0800094D]+[0x13579000+i for i in range(4,13)]
        for r,v in zip(regs,initial):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,lr);writes.clear()
        leaf_stop[0]=lr&~1
        u.ctl_remove_cache(0x03005800,0x03007000);u.ctl_remove_cache(0x08F03000,0x08F04000)
        try:u.emu_start(0x08F03001,lr&~1,count=50000)
        except Exception as exc:raise ValueError(f'direct leaf execution {oldsrc:x}/{dest:x}/{length}/{lr:x}, pc={u.reg_read(UC_ARM_REG_PC):x}') from exc
        final=tuple(u.reg_read(r) for r in regs)
        if final!=(oldsrc,dest,0,oldbyte,*initial[4:]) or u.reg_read(UC_ARM_REG_CPSR)&0xF0000000!=0x60000000 or u.reg_read(UC_ARM_REG_LR)!=lr or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_PC)!=lr&~1:raise ValueError('direct copy live-outs/NZCV')
        if bytes(u.mem_read(0x02000000,0x40000))!=bytes(before) or bytes(u.mem_read(sp-136,4))!=b'\x5A'*4:raise ValueError('direct copy bounds')
        if any(not(dest<=a and a+n<=dest+len(wanted) or sp-132<=a and a+n<=sp) for a,n in writes):raise ValueError('direct copy writes')
        stats['direct_copy_ABI_checks']+=1
    report=dict(id='exe45.hangul-keyboard.copy-shim.v1',passed=True,rom_integrated=False,source_sha256=profile['sha256'],current_rom_sha256=identity,helper_bytes=len(blob),counts=stats,own_stack_bytes=20,nested_stack_bytes=132,original_provider_with_shim_stack_bytes=176,selector=dict(source='0x0200FC80',destination='0x020155F0',length=32,LR='0x03006A4C'),fixture_literal=dict(source_offset='0x1EF96C',IWRAM='0x03006A6C',expected_hex='4d090008',fixture_final_hex='0130f008'),dependencies={'cpu_cache_bridge':sha(dep.read_bytes()),'cpu_composer':sha(composer.read_bytes())},ISA=isa,native_code=regions,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['hangul_keyboard_copy_shim.py','bench_keyboard_copy_shim.py','hangul_mixed_cache_bridge.py','hangul_mixed_keyedit_thumb.py','hangul_mixed_replay_state.py','hangul_mixed_editor.py']},artifacts={'helper.bin':sha(blob)},limits=['Selected route requires caller-established new editor layout; pointer/length/LR gate is NOT format discrimination. Must never install while old editor is live.','Fixture changes one copy-pointer literal in Unicorn only, not ROM/product build. Source0200FC54/cache41/table09000000/code08F03000 are caller-owned fixture locations, not adopted free space.','Old descriptor0 at nonzero slots remains legacy; no proof all game descriptor0 calls are slot0. Invalid compact emits emptyE5 for memory safety, not an adopted player-facing rejection UI.','Provider live-outs checked, but full indirect caller population, writer/cache/IRQ lifetime, actual rendering/selection/record/save/fresh-load unresolved.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS original provider selective copy ABI',stats,len(blob),flush=True)


if __name__=='__main__':main()
