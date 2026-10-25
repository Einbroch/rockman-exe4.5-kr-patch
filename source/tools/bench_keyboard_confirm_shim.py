"""CPU confirmation candidate with modeled native dialog/sound services."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from hangul_keyboard_confirm_shim import assemble
from hangul_mixed_commit_bridge import record
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';dep=base/'cpu_commit_bridge/report.json';d=json.loads(dep.read_text(encoding='utf8'))
    if not d['passed'] or d['rom_integrated']:raise ValueError('commit dependency')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dep.parent/n,h)
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(play,identity)
    if play.read_bytes()[0x34F84:0x34FB4]!=rom[0x34F84:0x34FB4]:raise ValueError('confirm body drift')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=base/'cpu_confirm_shim';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for a,b in [(0x08F06000,(dep.parent/'helper.bin').read_bytes()),(0x08F08000,blob)]:
        u.mem_map(a,4096);u.mem_write(a,b);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    table=(base/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    pages=(0x02000000,0x0200F000,0x02014000)
    for a in pages:u.mem_map(a,4096)
    u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    editor,dest,sp,stop=0x0200FC40,0x02001000-0x200,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    services=[];writes=[];control={}
    def hook(cpu,a,n,user):
        if a==0x08055408:
            services.append(('busy',cpu.reg_read(UC_ARM_REG_R0)))
            flags=0x00000000 if control['busy'] else 0x40000000
            cpu.reg_write(UC_ARM_REG_CPSR,0x30|flags)
        elif a==0x08055418:services.append(('choice',control['choice']));cpu.reg_write(UC_ARM_REG_R0,control['choice'])
        elif a==0x08000534:services.append(('sound',cpu.reg_read(UC_ARM_REG_R0)))
        else:return
        # ARMv4T native Thumb services return without interworking; host PC
        # assignment must preserve Thumb even when MOV lr,pc produced even LR.
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(calls=0,successful_commits=0,rejected_commits=0,busy_passthroughs=0,cancel_paths=0,original_passthrough_comparisons=0,syllable_paths=0)
    def run(raw,cap,choice=0,busy=False,original=False,target=dest):
        for a in pages:u.mem_write(a,b'\xA7'*4096)
        ui=bytearray(16);ui[:2]=b'\x10\x00';ui[4]=cap
        u.mem_write(editor,bytes(ui)+struct.pack('<I',target)+raw)
        expected={a:bytearray(u.mem_read(a,4096)) for a in pages}
        wanted=None
        if not busy and choice not in (1,2) and 1<=cap<=10 and cap==raw[0]&15:
            try:wanted=record(raw)
            except ValueError:pass
        if wanted and (target+len(wanted)>0xFFFFFFFF or not(target+len(wanted)<=editor or editor+96<=target)):wanted=None
        if original and wanted:raise ValueError('only original noncommit route compared')
        control.update(choice=choice,busy=busy);services.clear();writes.clear()
        u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1)
        saved=[editor if r==UC_ARM_REG_R5 else 0x13579000+i for i,r in enumerate(regs)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3):u.reg_write(r,0)
        u.mem_write(sp-152,b'\x5A'*152)
        u.emu_start(0x08034F85 if original else 0x08F08001,stop,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)):raise ValueError('confirm ABI')
        if not busy:
            state=20 if wanted else 12
            expected[0x0200F000][editor-0x0200F000:editor-0x0200F000+2]=struct.pack('<H',state)
            if wanted:expected[0x02000000][target-0x02000000:target-0x02000000+len(wanted)]=wanted
        if any(bytes(u.mem_read(a,4096))!=bytes(data) for a,data in expected.items()):raise ValueError('confirm external writes')
        if bytes(u.mem_read(sp-152,4))!=b'\x5A'*4:raise ValueError('confirm nested stack')
        if any(not(sp-148<=a and a+n<=sp or not busy and editor<=a and a+n<=editor+2 or wanted and target<=a and a+n<=target+len(wanted)) for a,n in writes):raise ValueError('confirm write interval')
        expected_services=[('busy',128)]
        if not busy:expected_services.extend([('choice',choice),('sound',128 if wanted else 127)])
        if services!=expected_services:raise ValueError('confirm service order')
        result=tuple(u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3))+ (u.reg_read(UC_ARM_REG_CPSR)&0xF0000000,)
        if not original:
            stats['calls']+=1;stats['busy_passthroughs']+=busy
            stats['successful_commits']+=wanted is not None
            stats['cancel_paths']+=not busy and choice in (1,2)
            stats['rejected_commits']+=not busy and choice not in (1,2) and wanted is None
        return result
    for rank in range(11172):
        c=MixedReplay(4);c.load([0,0,0,rank]);run(c.serialize(),4);stats['syllable_paths']+=1
    c=MixedReplay(4);c.load([0]);valid=c.serialize()
    for choice in range(256):
        run(valid,4,choice)
        a=run(valid,4,choice,busy=True);b=run(valid,4,choice,busy=True,original=True)
        if a!=b:raise ValueError('original busy liveouts')
        stats['original_passthrough_comparisons']+=1
        if choice in (1,2):
            if run(valid,4,choice)!=run(valid,4,choice,original=True):raise ValueError('original cancel liveouts')
            stats['original_passthrough_comparisons']+=1
    for cap in range(256):run(valid,cap)
    for cap in range(1,11):
        for count in range(cap+1):
            for word in (0,11171,11172,11190,0x809B,0x8198,0x81E5):
                c=MixedReplay(cap);c.model.state=Snapshot((word,)*count,0,None);c.model._validate(c.model.state);c._rebase();run(c.serialize(),cap)
    for i in range(76):
        raw=bytearray(valid);raw[i]^=255;run(bytes(raw),4)
    for delta in range(-9,96):run(valid,4,target=editor+delta)
    run(valid,4,target=0xFFFFFFFC)
    report=dict(id='exe45.hangul-keyboard.confirm-shim.v1',passed=True,rom_integrated=False,new_layout_required=True,
                format_adopted=False,native_dialog_and_sound_services_modeled=True,original_commit_called=False,
                source_sha256=profile['sha256'],current_rom_sha256=identity,original_handler_sha256=sha(rom[0x34F84:0x34FB4]),
                helper_bytes=len(blob),own_stack_bytes=8,nested_stack_bytes=148,counts=stats,ISA=isa,
                dependencies={'cpu_commit_bridge':sha(dep.read_bytes())},
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_keyboard_confirm_shim.py','bench_keyboard_confirm_shim.py')},
                artifacts={'helper.bin':sha(blob)},
                limits=['Candidate handler invoked directly in CPU, original busy/choice/sound service effects modeled. No source ROM handler patch or actual Hangul UI.',
                        'All11172 syllables confirm into fixedcap4 record; partial/empty/malformed reject to state0C. Busy/cancel liveouts match original under same service models.',
                        'No native temporary-normalize write; downstream consumers must switch to packed records. Format selection, real table/destination/layout/IRQ ownership, save and fresh-load remain unresolved.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS confirmation handler candidate',stats,flush=True)

if __name__=='__main__':main()
