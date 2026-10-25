"""Native state dispatch/animation + new init/confirm, CPU clone only.

Rendering, state12 input and preload services are deliberately modeled here.
This does NOT combine the earlier state12 pixel bench with these transitions.
Destination is an owned test buffer, NOT evidence of game/save record extent.
"""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from hangul_mixed_editor_init import initialize
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_commit_bridge import record
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB


def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_keyboard_reentry','cpu_confirm_shim','cpu_commit_bridge','cpu_composer'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes())
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename']
    require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity=read(base/'cpu_confirm_shim/report.json')['current_rom_sha256'];require_hash(play,identity);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);scopes=[]
    # Separate instruction ranges from literal pools/dispatch tables.
    for a,b in ((0x34E34,0x34E62),(0x34E80,0x34EBE),(0x34EC4,0x34EFE),(0x34F68,0x34F7A),(0x34FB4,0x34FFC)):
        data=rom[a:b];ins=list(cs.disasm(data,0x08000000+a))
        if current[a:b]!=data or sum(i.size for i in ins)!=len(data):raise ValueError('native code scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('Thumb1 scope')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native roundtrip')
        scopes.append(dict(offset=a,bytes=b-a,sha256=sha(data)))
    old=rom[0x34F7C:0x34F80]
    if old!=struct.pack('<I',0x08034F85) or current[0x34F7C:0x34F80]!=old:raise ValueError('confirm dispatch pointer')
    clone=bytearray(rom);clone[0x34F7C:0x34F80]=struct.pack('<I',0x08F08001)
    initshim=(base/'cpu_keyboard_reentry/init_shim.bin').read_bytes();clone[0x301000:0x301000+len(initshim)]=initshim
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(clone));u.mem_write(0x08000000,bytes(clone));u.mem_protect(0x08000000,len(clone),UC_PROT_READ|UC_PROT_EXEC)
    for a,p in ((0x08F0C000,'cpu_keyboard_reentry/init.bin'),(0x08F08000,'cpu_confirm_shim/helper.bin'),(0x08F06000,'cpu_commit_bridge/helper.bin')):
        u.mem_map(a,4096);u.mem_write(a,(base/p).read_bytes());u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    table=(base/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    ed,glob,display,flag,dest,sp,stop=0x0200FC40,0x02000200,0x02000400,0x02000500,0x02001000,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];services=[];control=dict(busy=False,choice=0)
    modeled={0x08055C3E:'preload',0x080356CC:'page-upload',0x08035718:'palette-heading-upload',0x08034EFE:'input-state12',0x080355F6:'legacy-pad',0x0803562C:'legacy-flatten',0x08035380:'refresh',0x08035676:'page-map',0x0803564E:'field-map'}
    def hook(cpu,a,n,user):
        if a==stop:cpu.emu_stop();return
        if a in modeled:services.append((modeled[a],))
        elif a==0x08055408:
            services.append(('busy',cpu.reg_read(UC_ARM_REG_R0)))
            cpu.reg_write(UC_ARM_REG_CPSR,0x30|(0 if control['busy'] else 0x40000000))
        elif a==0x08055418:services.append(('choice',control['choice']));cpu.reg_write(UC_ARM_REG_R0,control['choice'])
        elif a==0x08000534:services.append(('sound',cpu.reg_read(UC_ARM_REG_R0)))
        else:return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(initializations=0,frames=0,entry_frames=0,exit_frames=0,commits=0,no_returns=0,busy_frames=0,partial_rejections=0,reentries=0,cancel_exits=0,counter_wraps=0)
    def execute(pc,regions,stack,args=()):
        before=bytes(u.mem_read(0x02000000,0x40000));expected=bytearray(before)
        for a,b in regions:expected[a-0x02000000:a-0x02000000+len(b)]=b
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved=[ed if r==UC_ARM_REG_R5 else glob if r==UC_ARM_REG_R10 else 0x13579000+i for i,r in enumerate(regs)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();services.clear()
        u.emu_start(pc|1,stop,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('ABI/stack')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError(f'whole EWRAM at {pc:08X}')
        if any(not(sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(b) for s,b in regions)) for a,n in writes):raise ValueError('write interval')
    post=[(modeled[a],) for a in (0x080355F6,0x0803562C,0x08035380,0x08035676,0x0803564E)]
    def frame():
        before=bytes(u.mem_read(ed,96));ui=bytearray(before);state=ui[0];extra=[];want=[]
        if state==0:
            d=bytearray(u.mem_read(display,24));struct.pack_into('<H',d,0,0x1D40);struct.pack_into('<H',d,8,0x1E4A)
            for at in (2,20,22):struct.pack_into('<H',d,at,0)
            extra=[(display,bytes(d)),(flag,b'\0')];want=[('preload',),('page-upload',),('palette-heading-upload',)]
            ui[11]=255;ui[12]=24;ui[0]=4
            struct.pack_into('<h',ui,2,-255 if ui[10]==2 else 255)
        elif state==4:
            v=ui[11]-ui[12]
            if v<0:ui[11]=0;ui[0]=8
            else:ui[11]=v;ui[12]-=int(ui[12]>8)
            struct.pack_into('<h',ui,2,-ui[11] if ui[10]==2 else ui[11])
        elif state==8:ui[0]=12
        elif state==12:want=[('input-state12',)]
        elif state==16:
            want=[('busy',128)]
            if control['busy']:stats['busy_frames']+=1
            elif ui[1]==4:ui[:2]=b'\x0C\0'
            elif ui[1]==0:
                wanted=None
                if control['choice'] not in (1,2):
                    try:wanted=record(bytes(ui[20:]))
                    except ValueError:pass
                want += [('choice',control['choice']),('sound',128 if wanted else 127)]
                ui[:2]=bytes([20 if wanted else 12,0])
                if wanted:extra.append((dest,wanted));stats['commits']+=1
                elif control['choice'] in (1,2):stats['no_returns']+=1
                else:stats['partial_rejections']+=1
            else:raise ValueError('unsupported confirm substate')
        elif state==20:
            v=ui[11]+ui[12]
            if v>=255:ui[11]=255;ui[13]=ui[14]
            else:ui[11]=v;ui[12]=min(24,ui[12]+1)
            struct.pack_into('<h',ui,2,-ui[11] if ui[10] else ui[11])
        else:raise ValueError('uncovered lifecycle state')
        stats['counter_wraps']+=ui[15]==255;ui[15]=(ui[15]+1)&255
        execute(0x08034E34,[(ed,bytes(ui)),*extra],172)
        if services!=want+post:raise ValueError(f'service order state{state}: {services}')
        if u.reg_read(UC_ARM_REG_R0)!=ui[13] or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)!=(ui[13]==0):raise ValueError('exit liveout r0/Z')
        stats['frames']+=1;stats['entry_frames']+=state in (0,4,8);stats['exit_frames']+=state==20
    def init(cap,value,reentry=False):
        wanted=initialize(struct.pack('<4I',cap,33,dest,value));execute(0x08301000,[(ed,wanted)],140,(cap,33,dest,value))
        if services or u.reg_read(UC_ARM_REG_R0)!=1:raise ValueError('init result')
        stats['initializations']+=1;stats['reentries']+=reentry
    def enter():
        for i in range(64):
            if bytes(u.mem_read(ed,1))==b'\x0C':break
            frame()
        else:raise ValueError('entry stalled')
        frame()
    def confirm(choice,busy=False,substate=0):
        # Fixture enters dialog state; raw Start->dialog already has own bench.
        u.mem_write(ed,b'\x10'+bytes([substate]));control.update(choice=choice,busy=busy);frame()
    for cap in range(1,11):
        for value in (0,1,2):
            for variant in (0,128):
                u.mem_write(0x02000000,b'\xA7'*0x40000)
                u.mem_write(glob+8,struct.pack('<I',display));u.mem_write(glob+32,struct.pack('<I',flag))
                init(cap|variant,value);enter()
                c=MixedReplay(cap);c.load([0]*(cap-1)+[11171]);raw=c.serialize();u.mem_write(ed+20,raw)
                # Busy and No cannot mutate compact or destination; next Yes
                # is executed without HOST compact/record rewriting.
                confirm(0,True);confirm(1);confirm(2);confirm(0)
                for i in range(64):
                    if bytes(u.mem_read(ed+13,1))!=b'\0':break
                    frame()
                else:raise ValueError('exit stalled')
                saved=bytes(u.mem_read(dest,2*cap+2));init(cap|variant,value,True);enter()
                if bytes(u.mem_read(dest,len(saved)))!=saved:raise ValueError('reentry erased committed buffer')
                partial=MixedReplay(cap);partial.press('ㄱ');u.mem_write(ed+20,partial.serialize());confirm(0)
                confirm(0,True,4);confirm(0,False,4)
                # Cancel-start state is injected, not an observed empty-B
                # route. Completion must propagate2 rather than success1.
                u.mem_write(ed,b'\x14\0');u.mem_write(ed+14,b'\x02\xFF')
                for i in range(64):
                    if bytes(u.mem_read(ed+13,1))!=b'\0':break
                    frame()
                else:raise ValueError('cancel exit stalled')
                if bytes(u.mem_read(ed+13,1))!=b'\x02' or bytes(u.mem_read(dest,len(saved)))!=saved:raise ValueError('cancel result/destination')
                stats['cancel_exits']+=1
    out=base/'cpu_keyboard_lifecycle';out.mkdir(exist_ok=True)
    report=dict(id='exe45.hangul-keyboard.lifecycle-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,frame_stack_bytes=172,init_stack_bytes=140,
        native_code=scopes,dependencies=deps,tools={'bench_keyboard_lifecycle.py':sha((ROOT/'tools/bench_keyboard_lifecycle.py').read_bytes())},
        fixture_confirm_pointer=dict(offset=0x34F7C,expected_hex=old.hex(),final_hex=struct.pack('<I',0x08F08001).hex()),
        init_shim_fixture=dict(offset=0x301000,source_sha256=sha(rom[0x301000:0x301000+len(initshim)]),bytes=len(initshim),sha256=sha(initshim)),
        no_HOST_compact_or_destination_rewrite_between_busy_No_Yes=True,
        limits=['Native main034E34 dispatch, state0/4/8 animation, state16 confirm and state20 exit execute. Rendering/preload/state12 input services modeled, NOT combined frame/pixel evidence.',
                'New init shim called directly; native metadata caller is a separate bench. Dialog-state entries and initial full/partial compact values are HOST fixtures, not natural button entry.',
                'Cap1..10, alternate heading bit, caller values0/1/2, busy/No/Yes/partial/substate4/reentry covered. Disjoint destination is test-owned; cap10 game/save extent and all redisplay consumers unresolved.',
                'Exit sets completion byte but does not prove resource release/IRQ queue lifetime.172byte stack bound excludes modeled rendering and is not game/IRQ budget.',
                '08301000/08F08000 are fixture addresses, not free ROM proof. No playable ROM hooks, actual Hangul screen, save/reset/fresh-load or release claim.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS lifecycle CPU (render/input modeled)',stats,flush=True)


if __name__=='__main__':main()
