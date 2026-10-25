"""Original calendar success caller -> fixed NEW record transfer CPU clone.

Includes original rawE5 counterexample. Does NOT write game or save files.
Pool slots0..2 are a bounded fixture domain, not allocator/save ownership.
"""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from hangul_calendar_record_transfer import assemble,assemble_finalizer
from hangul_mixed_record import pack_surface

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';dep=base/'cpu_mixed_record_import/report.json';d=read(dep)
    if not d['passed'] or d.get('rom_integrated',False):raise ValueError('import dependency scope')
    for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
    for n,h in d.get('artifacts',{}).items():require_hash(dep.parent/n,h)
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=read(base/'cpu_keyboard_lifecycle/report.json')['current_rom_sha256'];require_hash(play,identity);rom=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);scopes=[]
    for a,b in ((0x31040,0x3105E),(0x32AC6,0x32AD8),(0x33334,0x3338E),(0x33864,0x33882),(0x33C94,0x33CB8),(0x373A2,0x373FA)):
        raw=original[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('native source scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('native Thumb1')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native roundtrip')
        scopes.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    if struct.unpack_from('<II',rom,0x31060)!=(0x02026280,0x02026080):raise ValueError('calendar literal bounds')
    old=list(cs.disasm(rom[0x3104E:0x31052],0x0803104E))
    if len(old)!=1 or old[0].mnemonic!='bl' or old[0].op_str!='#0x8032ac6':raise ValueError('caller BL source')
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x8306000',0x0803104E)[0]);i=list(cs.disasm(patch,0x0803104E))
    if len(i)!=1 or i[0].mnemonic!='bl' or i[0].op_str!='#0x8306000' or len(patch)!=4:raise ValueError('final placed BL')
    blob,isa=assemble();finalizer,final_isa=assemble_finalizer()
    suffix=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x8306100',0x08031052)[0])+bytes.fromhex('c046')*4
    if len(blob)>256 or len(suffix)!=12 or list(cs.disasm(suffix[:4],0x08031052))[0].op_str!='#0x8306100':raise ValueError('coordinated caller placement')
    clone=bytearray(rom);clone[0x3104E:0x31052]=patch;clone[0x31052:0x3105E]=suffix
    clone[0x306000:0x306000+len(blob)]=blob;clone[0x306100:0x306100+len(finalizer)]=finalizer
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    size=(len(clone)+4095)&~4095;u.mem_map(0x08000000,size);u.mem_write(0x08000000,bytes(clone))
    u.mem_map(0x08F05000,4096);u.mem_write(0x08F05000,(dep.parent/'helper.bin').read_bytes());u.mem_protect(0x08F05000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    ctx,stage,pool,sp,stop=0x0200F550,0x02026280,0x02026080,0x03007EFC,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];boundary=[stop];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    u.hook_add(UC_HOOK_CODE,lambda cpu,a,n,user:cpu.emu_stop() if a==boundary[0] else None)
    stats=dict(syllable_routes=0,original_truncations=0,marker_loss_cases=0,accepted_transfers=0,rejections=0,whole_EWRAM_checks=0,atomic_cancel_branches=0,unguarded_failure_advance_reproduced=0)
    def packed(words):return pack_surface(bytes([len(words),10,0,255])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words)))))
    def run(raw,slot=0,patched=True,valid=True,direct=False,src=stage+1,target=None,guarded=True):
        # Code mutation is clone-only; invalidate translated blocks on variant.
        u.mem_write(0x0803104E,patch if patched else rom[0x3104E:0x31052]);u.ctl_remove_cache(0x08031040,0x08031060)
        u.mem_write(0x08031052,suffix if patched and guarded else rom[0x31052:0x3105E]);u.ctl_remove_cache(0x08031040,0x08031060)
        u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(stage,raw);u.mem_write(ctx+0x32,bytes([slot]))
        before=bytes(u.mem_read(0x02000000,0x40000));expected=bytearray(before);dest=pool+slot*128 if target is None else target
        if patched:wanted=raw if valid else b''
        else:
            wanted=raw[1:raw.index(229,1)+1]
            stats['original_truncations']+=len(wanted)!=len(raw)-1;stats['marker_loss_cases']+=True
        if wanted:expected[dest-0x02000000:dest-0x02000000+len(wanted)]=wanted
        if not direct:
            cancel=patched and guarded and not valid
            expected[ctx-0x02000000+1:ctx-0x02000000+4]=bytes([60 if cancel else 36,0,0]);expected[ctx-0x02000000+10]=int(cancel)
            stats['atomic_cancel_branches']+=cancel
            stats['unguarded_failure_advance_reproduced']+=patched and not guarded and not valid
        u.mem_write(sp-224,b'\x5A'*224);u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved=[ctx if r==UC_ARM_REG_R5 else 0x13579000+j for j,r in enumerate(regs)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_R0,src);u.reg_write(UC_ARM_REG_R1,dest);u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1)
        boundary[0]=stop if direct else 0x0803105E;writes.clear()
        u.emu_start(0x08306001 if direct else 0x08031041,boundary[0],count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=boundary[0] or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-224,4))!=b'\x5A'*4:raise ValueError('caller/helper ABI/stack')
        if direct and u.reg_read(UC_ARM_REG_R0)!=(22 if valid else 0):raise ValueError('direct result')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM/source/staging/adjacent slots')
        allowed=[(dest,len(wanted))] if wanted else []
        if not direct:allowed += [(ctx+1,3),(ctx+10,1)]
        if any(not(sp-220<=a and a+n<=sp or any(s<=a and a+n<=s+l for s,l in allowed)) for a,n in writes):raise ValueError('CPU write interval')
        stats['whole_EWRAM_checks']+=1
        if patched:stats['accepted_transfers' if valid else 'rejections']+=1
    # Last cap10 slot covers every Hangul identity, rotating bounded pool slots.
    for rank in range(11172):
        raw=packed([0]*9+[rank]);run(raw,rank%3,False);run(raw,rank%3);stats['syllable_routes']+=1
        if rank%2048==0:print('calendar transfer syllable',rank,flush=True)
    for slot in range(3):
        for count in range(1,11):
            for word in (0,11171,0x80E3,0x81E5):run(packed([word]*count),slot)
    good=packed([229]*10)
    for j in range(22):
        raw=bytearray(good);raw[j]^=255;raw=bytes(raw)
        from hangul_mixed_record import unpack_selected_record
        try:unpack_selected_record(raw,10);valid=True
        except ValueError:valid=False
        run(raw,valid=valid)
    for slot in (3,4,127,255):run(good,slot,valid=False)
    for src in (stage,stage+2,0,0xFFFFFFFF):run(good,direct=True,src=src,valid=False)
    for target in (pool-1,pool+1,pool+384,stage,0xFFFFFFFF):run(good,direct=True,target=target,valid=False)
    run(bytes(22),valid=False,guarded=False)
    run(bytes(22),valid=False)
    out=base/'cpu_calendar_record_transfer';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob);(out/'finalizer.bin').write_bytes(finalizer)
    report=dict(id='exe45.hangul-keyboard.calendar-transfer-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,helper_stack_bytes=220,caller_push_excluded_bytes=4,
        native_code=scopes,ISA=isa,finalizer_ISA=final_isa,helper_bytes=len(blob),fixture_BL=dict(offset=0x3104E,expected_hex=rom[0x3104E:0x31052].hex(),final_hex=patch.hex()),
        fixture_finalizer=dict(offset=0x31052,expected_hex=rom[0x31052:0x3105E].hex(),final_hex=suffix.hex()),
        dependencies={'cpu_mixed_record_import/report.json':sha(dep.read_bytes())},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_calendar_record_transfer.py','bench_calendar_record_transfer.py')},artifacts={'helper.bin':sha(blob),'finalizer.bin':sha(finalizer)},
        selected_new_format_required=True,pool_slots_fixture_domain=[0,1,2],record_width=22,
        limits=['Original calendar success caller31040..3105E executes with fixture-only BL. Every11172 final-slot cap10 syllable tested; native byte copier loses marker in all cases and truncates43 embeddedE5 cases.',
                'Helper validates whole cap10 fixed22 record before writing all22 bytes, including marker. Source/stage/adjacent pool bytes preserved. Patch is not global raw copier replacement.',
                'New-format selection remains explicit; default/import writers and legacy discrimination unresolved. Original success-only suffix incorrectly advances on failed transfer (negative variant reproduced); coordinated finalizer uses original cancel state3C/flag1 while leaving pool unchanged. No explanatory failure dialog or natural runtime UX adoption.',
                'Only bounded pool slots0..2 admitted. Their full allocation/other writers/release/save ownership is NOT proved. Marked binary pool text cannot be consumed by unchanged confirmation/display/default/record-copy routes.',
                'Persistent calendar records have prior observed32byte stride/name offset10/field22, but this bench does not write that record or prove save/reset/freshload. No actual Korean screenshot or ROM hook.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS selected calendar record transfer CPU; NOT save/redisplay',stats,flush=True)

if __name__=='__main__':main()
