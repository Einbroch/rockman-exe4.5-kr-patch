"""CPU native BL/BNE -> raw keys -> edit/control -> Yes/No pipeline."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB
from hangul_keyboard_raw_router import assemble
from hangul_mixed_editor_init import initialize
from hangul_mixed_replay_state import MixedReplay,KEYS,apply
from hangul_mixed_editor import Snapshot
from hangul_keyboard_model import INITIALS,MEDIALS,FINALS,FINAL_SPLIT
from hangul_mixed_commit_bridge import record

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={};reports={}
    for name in ('cpu_keyboard_actions','cpu_keyboard_controls','cpu_confirm_shim','cpu_composer'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes());reports[name]=d
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=reports['cpu_keyboard_actions']['current_rom_sha256'];require_hash(play,identity)
    f=reports['cpu_keyboard_actions']['native_caller'];pc=0x08000000+f['offset'];original=rom[f['offset']:f['offset']+6]
    if original.hex()!=f['expected_hex'] or play.read_bytes()[f['offset']:f['offset']+6]!=original:raise ValueError('native caller identity')
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);target=0x08304000
    if not -(1<<22)<=target-(pc+4)<(1<<22):raise ValueError('Thumb1 BL range')
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl '+hex(target),pc)[0]);ins=list(cs.disasm(patch,pc))
    if len(patch)!=4 or int.from_bytes(patch[:2],'little')&0xF800!=0xF000 or int.from_bytes(patch[2:],'little')&0xF800!=0xF800 or len(ins)!=1 or ins[0].op_str!='#0x8304000':raise ValueError('BL final profile')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=base/'cpu_keyboard_raw_router';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_write(pc,patch);u.mem_write(target,blob);u.mem_write(0x08303000,(base/'cpu_keyboard_actions/shim.bin').read_bytes());u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for a,p in [(0x08F0D000,'cpu_keyboard_actions/dispatch.bin'),(0x08F0E000,'cpu_keyboard_actions/keyedit.bin'),(0x08F0F000,'cpu_keyboard_actions/rebase.bin'),(0x08F10000,'cpu_keyboard_controls/helper.bin'),(0x08F11000,'cpu_keyboard_controls/query.bin'),(0x08F06000,'cpu_commit_bridge/helper.bin'),(0x08F08000,'cpu_confirm_shim/helper.bin')]:
        u.mem_map(a,4096);u.mem_write(a,(base/p).read_bytes());u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    for a,n in [(0x09000000,'transitions.bin'),(0x09200000,'deletions.bin')]:
        b=(base/'cpu_composer'/n).read_bytes();size=(len(b)+4095)&~4095;u.mem_map(a,size);u.mem_write(a,b);u.mem_protect(a,size,UC_PROT_READ)
    selectors=(base/'cpu_keyboard_actions/selectors.bin').read_bytes();u.mem_map(0x09300000,8192);u.mem_write(0x09300000,struct.pack('<4I',0x09000000,0x09200000,0x08F0E001,0x08F0F001));u.mem_write(0x09301000,selectors);u.mem_protect(0x09300000,8192,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    ed,glob,keys,dest,sp,stop=0x0200FC40,0x02000200,0x02000300,0x020010A6,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11];writes=[];services=[];choice=[0]
    def service(cpu,at,size,user):
        if at==0x08000534:services.append(('sound',cpu.reg_read(UC_ARM_REG_R0)))
        elif at==0x080356D0:services.append(('page',bytes(cpu.mem_read(ed+8,1))[0]))
        elif at==0x080322CC:services.append(('dialog',cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)))
        elif at==0x08055408:cpu.reg_write(UC_ARM_REG_CPSR,0x40000030)
        elif at==0x08055418:cpu.reg_write(UC_ARM_REG_R0,choice[0])
        else:return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,service);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(raw_calls=0,consumed=0,unhandled=0,mask_domain_cases=0,syllable_pipelines=0,CPU_jamo_keys=0,Yes_commits=0,No_returns=0)
    seed=bytes(range(256))*1024
    def call(start,end,stack):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30);saved=[ed if r==UC_ARM_REG_R5 else glob if r==UC_ARM_REG_R10 else 0x13579000+i for i,r in enumerate(regs)]
        for r,v in zip(regs,saved):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();services.clear();u.emu_start(start|1,end,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=end or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('router ABI/stack')
    def check(before,regions,stack):
        expected=bytearray(before)
        for a,b in regions:expected[a-0x02000000:a-0x02000000+len(b)]=b
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM writes')
        if any(not(sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(b) for s,b in regions)) for a,n in writes):raise ValueError('CPU write interval')
    def init(raw):
        u.mem_write(0x02000000,seed);ui=bytearray(initialize(struct.pack('<4I',raw[0]&15,33,dest,1)));ui[0]=12;ui[20:]=raw;u.mem_write(ed,bytes(ui));u.mem_write(glob+4,struct.pack('<I',keys))
        u.mem_write(0x02010724,bytes(4))
    def step(mask,col=None,row=None,page=None):
        for off,v in [(6,col),(7,row),(8,page)]:
            if v is not None:u.mem_write(ed+off,bytes([v]))
        u.mem_write(keys+2,struct.pack('<H',mask));ui=bytearray(u.mem_read(ed,96));wanted=bytearray(ui);raw=bytes(ui[20:]);consumed=bool(mask&0x30B);expected_services=[];command=None;action=None
        try:c=MixedReplay.restore(raw)
        except ValueError:c=None
        if ui[4]==raw[0]&15 and 1<=ui[4]<=10 and consumed:
            if mask&2:
                if c and not c.model.state.cells:command=5
                elif c:action=('backspace',None)
            elif mask&1:
                if ui[6]==15 and ui[7] in (0,1,5):command={0:2,1:3,5:4}[ui[7]]
                elif ui[6]==15 and ui[7] in (2,3):action=('move',1 if ui[7]==2 else -1)
                elif ui[6]<15 and ui[7]<6 and ui[8]==0:
                    index=selectors[ui[7]*15+ui[6]]
                    if index<40:action=('jamo',KEYS[index])
            elif mask&8:command=4
            elif mask&0x200:command=0
            elif mask&0x100:command=1
        if action:
            try:accepted,updated=apply(raw,*action);wanted[20:]=updated
            except ValueError:pass
        if command is not None:
            if command<4 and ui[8]<=2:
                p=ui[8];n=(p-1)%3 if command==0 else (p+1)%3 if command==1 else (1 if p==0 else 0) if command==2 else (1 if p==2 else 2)
                wanted[8]=n;expected_services=[('page',n),('sound',466)]
            elif command==5 and c and not c.model.state.cells and ui[14]!=2:
                wanted[0]=20;wanted[10]=0;wanted[14]=2;expected_services=[('sound',127)]
            elif command==4 and c:
                if (ui[6],ui[7])!=(15,5):wanted[6:8]=bytes([15,5]);expected_services=[('sound',466)]
                elif not c.model.state.cells:wanted[:2]=bytes([16,4]);expected_services=[('sound',105),('dialog',11,4)]
                else:
                    try:record(raw);complete=True
                    except ValueError:complete=False
                    if complete:wanted[:2]=bytes([16,0]);expected_services=[('sound',467),('dialog',10,0)]
                    else:expected_services=[('sound',127)]
        before=bytes(u.mem_read(0x02000000,0x40000));end=0x08034F66 if consumed else 0x08034F0E;call(pc,end,220)
        if u.reg_read(UC_ARM_REG_R0)!=int(consumed) or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)==consumed or services!=expected_services:raise ValueError('raw priority/BNE/services '+hex(mask))
        check(before,[(ed,bytes(wanted))],220);stats['raw_calls']+=1;stats['consumed']+=consumed;stats['unhandled']+=not consumed
        return bytes(wanted[20:])
    empty=MixedReplay(4).serialize();c=MixedReplay(4);c.press('ㄱ');partial=c.serialize();c.press('ㅏ');complete=c.serialize()
    for raw in (empty,partial,complete):
        for col,row in [(0,0),(15,0),(15,1),(15,5)]:
            for mask in range(1024):init(raw);step(mask,col,row,0);stats['mask_domain_cases']+=1
        for page in (0,1,2,255):
            for mask in (1,2,3,8,0x100,0x200,0x300):init(raw);step(mask,15,5,page)
    for offset,value in [(2,71),(75,0),(1,255)]:
        bad=bytearray(complete);bad[offset]=value
        for mask in (1,2,8):init(bytes(bad));step(mask,15,5,0)
    # Sequential page switch and first/second Start use unchanged compact.
    init(complete);step(0x100);step(0x200);step(8,0,0);step(8)
    positions={KEYS[v]:(i%15,i//15) for i,v in enumerate(selectors) if v<40}
    c=MixedReplay(4);c.model.state=Snapshot((0,0,0),3,None);c._rebase();initial=c.serialize()
    for rank in range(11172):
        init(initial);l=INITIALS[rank//588];v=MEDIALS[rank//28%21];t=FINALS[rank%28]
        for k in [l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,)))):
            col,row=positions[k];raw=step(1,col,row,0);stats['CPU_jamo_keys']+=1
        if MixedReplay.restore(raw).model.state.cells!=(0,0,0,rank):raise ValueError('canonical composed identity')
        step(8);step(8)
        before=bytes(u.mem_read(0x02000000,0x40000));choice[0]=rank%2;call(0x08F08000,stop,148)
        check(before,[(ed,struct.pack('<H',12 if choice[0] else 20))]+([] if choice[0] else [(dest,record(raw))]),148)
        stats['Yes_commits' if not choice[0] else 'No_returns']+=1;stats['syllable_pipelines']+=1
        if rank%2048==0:print('raw compose/Start/Yes-No syllable',rank,flush=True)
    report=dict(id='exe45.hangul-keyboard.raw-router-CPU.v1',passed=True,rom_integrated=False,new_layout_required=True,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,nested_stack_bytes=220,
        raw_pressed_mask_routing=True,no_HOST_compact_or_record_rewrites_between_CPU_stages=True,services_modeled=True,
        ISA=isa,native_caller=dict(offset=f['offset'],bytes=6,sha256=sha(original),expected_hex=original.hex(),fixture_BL_hex=patch.hex()),dependencies=deps,
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_keyboard_raw_router.py','bench_keyboard_raw_router.py','hangul_mixed_editor_init.py','hangul_mixed_replay_state.py')},artifacts={'helper.bin':sha(blob)},
        limits=['Native BL+BNE executes raw pressed-mask routing in source clone only, not full outer drawing/navigation or natural gameplay. Input global/key pointer fixtures are caller-owned.',
                'B>A>Start>L>R priority; all1024 low10bit masks in four cells and three editing states. Consumed invalid keys return1/Z0, repeated empty cancel intentionally consumes unlike original flag2/Z1 quirk.',
                'Page0 candidate jamo selection; other-page Latin/space glyph and selector supply unresolved. Page/sound/dialog/busy/choice services modeled; original page uploader must not run unmodified against new assets.',
                'All11172 fullcap4 final syllables compose via A, two Start presses, alternating Yes/No without HOST compact/record writes. Initial three characters, cell positions and key masks are fixtures.',
                '220-byte stack is a CPU fixture bound, not actual game/IRQ budget. No code-space adoption, actual Korean UI pixels, format discriminator, ROM installation or native save/fresh-load.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity);print('PASS raw keys->compose->Start->Yes/No CPU',stats,flush=True)

if __name__=='__main__':main()
