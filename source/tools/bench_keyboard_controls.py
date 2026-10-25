"""New-layout logical controls with modeled services; not raw-key/UI hook."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from hangul_keyboard_control_shim import assemble
from hangul_mixed_count_thumb import assemble as count
from hangul_mixed_editor_init import initialize
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot
from hangul_mixed_commit_bridge import record

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_commit_bridge','cpu_mixed_count','cpu_confirm_shim','cpu_composer'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes())
    native=read(base/'control_routes.json');deps['control_routes.json']=sha((base/'control_routes.json').read_bytes())
    for n,h in native['tools'].items():require_hash(ROOT/'tools'/n,h)
    if any(r['entry_lengths']!=[0] for r in native['comparison_lists']):raise ValueError('empty-only native confirm list applicability')
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,native['current_rom_sha256'])
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    helper,isa=assemble();query,qisa=count(0x08F11000);out=base/'cpu_keyboard_controls';out.mkdir(exist_ok=True)
    (out/'helper.bin').write_bytes(helper);(out/'query.bin').write_bytes(query)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for a,b in [(0x08F10000,helper),(0x08F11000,query),(0x08F06000,(base/'cpu_commit_bridge/helper.bin').read_bytes()),(0x08F08000,(base/'cpu_confirm_shim/helper.bin').read_bytes())]:
        u.mem_map(a,4096);u.mem_write(a,b);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    b=(base/'cpu_composer/transitions.bin').read_bytes();size=(len(b)+4095)&~4095;u.mem_map(0x09000000,size);u.mem_write(0x09000000,b);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    ed,dest,sp,stop=0x0200FC40,0x020010A6,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11];writes=[];services=[];choice=[0]
    def service(cpu,pc,size,user):
        if pc==0x08000534:services.append(('sound',cpu.reg_read(UC_ARM_REG_R0)))
        elif pc==0x080356D0:services.append(('page',bytes(cpu.mem_read(ed+8,1))[0]))
        elif pc==0x080322CC:services.append(('dialog',cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)))
        elif pc==0x08055408:cpu.reg_write(UC_ARM_REG_CPSR,0x40000030)
        elif pc==0x08055418:cpu.reg_write(UC_ARM_REG_R0,choice[0])
        else:return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,service);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(controls=0,complete_requests=0,partial_rejections=0,empty_requests=0,cancel_exits=0,page_changes=0,Yes_commits=0,No_returns=0)
    def call(pc,command=0,stack=180):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved=[ed if r==UC_ARM_REG_R5 else 0x13579000+i for i,r in enumerate(regs)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_R0,command);u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();services.clear();u.emu_start(pc|1,stop,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('control ABI/stack')
        return u.reg_read(UC_ARM_REG_R0)
    def memory(before,regions,stack):
        expected=bytearray(before)
        for a,b in regions:expected[a-0x02000000:a-0x02000000+len(b)]=b
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM expected writes')
        if any(not(sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(b) for s,b in regions)) for a,n in writes):raise ValueError('control writes')
    seed=bytes(range(256))*1024
    def run(raw,cmd,page=0,col=15,row=5,flag=1,queue_count=0):
        u.mem_write(0x02000000,seed);ui=bytearray(initialize(struct.pack('<4I',raw[0]&15,33,dest,1)));ui[0]=12;ui[6:9]=bytes([col,row,page]);ui[14]=flag;ui[20:]=raw;u.mem_write(ed,bytes(ui))
        u.mem_write(0x02010724,struct.pack('<I',queue_count))
        wanted=bytearray(ui);expected_services=[];accepted=True
        try:model=MixedReplay.restore(raw)
        except ValueError:model=None
        if cmd<4:
            if page>2 or queue_count>=96:accepted=False
            else:
                nxt=((page-1)%3 if cmd==0 else (page+1)%3 if cmd==1 else 1 if page==0 else 0) if cmd<3 else 1 if page==2 else 2
                wanted[8]=nxt;expected_services=[('page',nxt),('sound',466)];stats['page_changes']+=1
        elif cmd in (4,5):
            if model is None:accepted=False
            elif cmd==5:
                if model.model.state.cells:accepted=False
                elif flag!=2:wanted[0]=20;wanted[10]=0;wanted[14]=2;expected_services=[('sound',127)];stats['cancel_exits']+=1
            elif (col,row)!=(15,5):wanted[6:8]=bytes([15,5]);expected_services=[('sound',466)]
            elif not model.model.state.cells:wanted[:2]=bytes([16,4]);expected_services=[('sound',105),('dialog',11,4)];stats['empty_requests']+=1
            else:
                try:record(raw);complete=True
                except ValueError:complete=False
                if complete:wanted[:2]=bytes([16,0]);expected_services=[('sound',467),('dialog',10,0)];stats['complete_requests']+=1
                else:expected_services=[('sound',127)];stats['partial_rejections']+=1
        else:accepted=False
        before=bytes(u.mem_read(0x02000000,0x40000))
        if call(0x08F10000,cmd)!=int(accepted) or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)==accepted or services!=expected_services:raise ValueError('control status/services')
        memory(before,[(ed,bytes(wanted))],180);stats['controls']+=1
        return bytes(wanted)
    for cap in (4,6,8,10):
        c=MixedReplay(cap);empty=c.serialize();c.press('ㄱ');partial=c.serialize();c.press('ㅏ');complete=c.serialize()
        for raw in (empty,partial,complete):
            for page in range(4):
                for cmd in range(4):run(raw,cmd,page)
            for cmd in (4,5,6,255):run(raw,cmd)
            run(raw,4,col=0,row=0);run(raw,5,flag=2)
        for offset,value in [(2,71),(75,0)]:
            bad=bytearray(complete);bad[offset]=value;run(bytes(bad),4);run(bytes(bad),5)
    for rank in range(11172):
        c=MixedReplay(4);c.load((0,0,0,rank));raw=c.serialize();run(raw,4)
        # Request performed only dry-run into stack. Then existing Yes/No handler
        # consumes SAME compact bytes, without HOST writes between CPU stages.
        before=bytes(u.mem_read(0x02000000,0x40000));choice[0]=rank%2
        call(0x08F08000,stack=148)
        memory(before,[(ed,struct.pack('<H',12 if choice[0] else 20))]+([] if choice[0] else [(dest,record(raw))]),148)
        if choice[0]:stats['No_returns']+=1
        else:stats['Yes_commits']+=1
        if rank%2048==0:print('request->Yes/No syllable',rank,flush=True)
    report=dict(id='exe45.hangul-keyboard.logical-controls-CPU.v1',passed=True,rom_integrated=False,new_layout_required=True,
        source_sha256=profile['sha256'],current_rom_sha256=native['current_rom_sha256'],counts=stats,nested_stack_bytes=180,
        no_HOST_editor_or_record_rewrite_between_request_and_Yes_No=True,services_modeled=True,raw_key_integration=False,
        page_upload_queue_guard=True,ISA=isa,query_ISA=qisa,dependencies=deps,
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_keyboard_control_shim.py','bench_keyboard_controls.py','hangul_mixed_count_thumb.py','hangul_mixed_editor_init.py')},
        artifacts={'helper.bin':sha(helper),'query.bin':sha(query)},
        limits=['Logical command ABI only, no raw-key action adapter installation or full native input handler replacement.',
                'Page service is modeled. Actual page assets/upload/Latin selection/input membership unresolved; no Korean keypad pixels claim.',
                'Empty-only comparison-list behavior preserved via validated logical count; partial requests reject with sound7F. No human visual/feedback judgment or malformed UX adoption.',
                'Dry-run commit writes own stack only; original record remains unchanged until CPU Yes. All11172 cap4 last syllables request->alternating Yes/No without HOST rewrites.',
                'Native sound/dialog/busy/choice services modeled.180-byte fixture stack not actual game/IRQ budget; no format/save/runtime hook or fresh-load.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,native['current_rom_sha256'])
    print('PASS logical keyboard controls request->Yes/No CPU',stats,flush=True)

if __name__=='__main__':main()
