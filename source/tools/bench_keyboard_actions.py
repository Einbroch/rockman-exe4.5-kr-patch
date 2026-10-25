"""Original353B0 BL+BNE executes new candidate A/B action shim in CPU only."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from extended_dialogue import Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB
from hangul_keyboard_action_shim import assemble
from hangul_mixed_dispatch_thumb import assemble as dispatch
from hangul_mixed_keyedit_thumb import assemble as keyedit
from hangul_mixed_rebase_thumb import assemble as rebase
from hangul_mixed_replay_state import MixedReplay,KEYS,apply
from hangul_mixed_editor import Snapshot
from hangul_keyboard_model import INITIALS,MEDIALS,FINALS,FINAL_SPLIT
from hangul_mixed_editor_init import initialize

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_mixed_rebase','cpu_composer','cpu_editor_init'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes())
    plan=read(base/'candidates/plan.json');require_hash(ROOT/'tools/prepare_hangul_keyboard_candidates.py',plan['tool_sha256'])
    if len(plan['selectors'])!=105 or tuple(plan['glyph_order'])!=KEYS:raise ValueError('candidate source plan')
    cells=plan['selectors'][:90];selectors=bytes(s['glyph_index'] if s['active'] else 255 for s in cells)
    if sum(v<40 for v in selectors)!=40:raise ValueError('all40 selectors within native6rows')
    deps['candidates/plan.json']=sha((base/'candidates/plan.json').read_bytes())
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(play,identity);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);pc=0x08034F08;end=0x08034F0E
    original=rom[0x34F08:0x34F0E]
    if current[0x34F08:0x34F0E]!=original:raise ValueError('original caller window identity')
    ins=list(cs.disasm(original,pc))
    if [(i.mnemonic,i.op_str) for i in ins]!=[('bl','#0x80353b0'),('bne','#0x8034f66')]:raise ValueError('original BL/BNE contract')
    for i in ins:
        if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native semantic roundtrip')
    target=0x08303000
    if not -(1<<22)<=target-(pc+4)<(1<<22):raise ValueError('ARMv4T BL range')
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl '+hex(target),pc)[0]);decoded=list(cs.disasm(patch,pc))
    if len(patch)!=4 or int.from_bytes(patch[:2],'little')&0xF800!=0xF000 or int.from_bytes(patch[2:],'little')&0xF800!=0xF800 or len(decoded)!=1 or decoded[0].op_str!='#0x8303000':raise ValueError('final BL profile/target')
    blobs={};isas={}
    for n,fn,a in [('shim.bin',assemble,0x08303000),('dispatch.bin',dispatch,0x08F0D000),('keyedit.bin',keyedit,0x08F0E000),('rebase.bin',rebase,0x08F0F000)]:blobs[n],isas[n]=fn(a)
    out=base/'cpu_keyboard_actions';out.mkdir(exist_ok=True)
    blobs['selectors.bin']=selectors
    for n,b in blobs.items():(out/n).write_bytes(b)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_write(pc,patch);u.mem_write(target,blobs['shim.bin']);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for a,n in [(0x08F0D000,'dispatch.bin'),(0x08F0E000,'keyedit.bin'),(0x08F0F000,'rebase.bin')]:
        u.mem_map(a,4096);u.mem_write(a,blobs[n]);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    for a,n in [(0x09000000,'transitions.bin'),(0x09200000,'deletions.bin')]:
        b=(base/'cpu_composer'/n).read_bytes();size=(len(b)+4095)&~4095;u.mem_map(a,size);u.mem_write(a,b);u.mem_protect(a,size,UC_PROT_READ)
    u.mem_map(0x09300000,8192);u.mem_write(0x09300000,struct.pack('<4I',0x09000000,0x09200000,0x08F0E001,0x08F0F001));u.mem_write(0x09301000,selectors);u.mem_protect(0x09300000,8192,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096)
    ed,glob,keys,sp=0x0200FC40,0x02000200,0x02000300,0x03007F00
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(calls=0,accepted_edits=0,rejected_consumed=0,unhandled=0,syllable_paths=0,CPU_key_actions=0)
    seed=bytes(range(256))*1024
    def step(raw,mask,col=0,row=0,page=0,preloaded=False,ui_cap=None):
        if not preloaded:
            u.mem_write(0x02000000,seed);u.mem_write(ed,initialize(struct.pack('<4I',raw[0]&15,33,0x020010A6,0))[:20]+raw)
        elif bytes(u.mem_read(ed+20,76))!=raw:raise ValueError('uninterrupted editor drift')
        u.mem_write(ed+6,bytes([col,row,page]));u.mem_write(glob+4,struct.pack('<I',keys));u.mem_write(keys+2,struct.pack('<H',mask))
        if ui_cap is not None:u.mem_write(ed+4,bytes([ui_cap]))
        consumed=bool(mask&3);action=None
        if consumed and ui_cap is None:
            if mask&2:action=('backspace',None)
            elif col==15 and row in (2,3):action=('move',1 if row==2 else -1)
            elif page==0 and col<15 and row<6:
                v=selectors[row*15+col]
                if v<40:action=('jamo',KEYS[v])
        wanted=raw;accepted=False
        if action:
            try:accepted,wanted=apply(raw,*action)
            except ValueError:pass
        before=bytearray(u.mem_read(0x02000000,0x40000));before[ed+20-0x02000000:ed+96-0x02000000]=wanted
        u.mem_write(sp-212,b'\x5A'*212);u.reg_write(UC_ARM_REG_CPSR,0x30)
        initial=[0x13579000+i for i in range(8)];initial[1]=ed;initial[6]=glob
        for r,v in zip(regs,initial):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);writes.clear()
        # Observe either next navigation instruction or original taken-branch target.
        dest=0x08034F66 if consumed else end
        u.emu_start(pc|1,dest,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=dest or u.reg_read(UC_ARM_REG_R0)!=int(consumed) or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)==consumed:raise ValueError('native BNE/handled flag')
        if u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,initial)) or bytes(u.mem_read(sp-212,4))!=b'\x5A'*4:raise ValueError('ABI/stack208')
        if bytes(u.mem_read(0x02000000,0x40000))!=before:raise ValueError('whole EWRAM expected edit/atomicity')
        if any(not(sp-208<=a and a+n<=sp or accepted and ed+20<=a and a+n<=ed+96) for a,n in writes):raise ValueError('write interval')
        stats['calls']+=1;stats['accepted_edits']+=accepted;stats['rejected_consumed']+=consumed and not accepted;stats['unhandled']+=not consumed
        return wanted
    states=[MixedReplay(4).serialize()]
    c=MixedReplay(4)
    for k in 'ㄱㅗㅏㄹㄱ':c.press(k)
    states.append(c.serialize());loaded=MixedReplay(4);loaded.load((229,0x809B,11171));states.append(loaded.serialize())
    for raw in states:
        for page in range(3):
            for row in range(6):
                for col in range(16):step(raw,1,col,row,page)
        for mask in range(1024):step(raw,mask)
        for col,row,page in [(16,0,0),(255,0,0),(0,6,0),(0,255,0),(0,0,255)]:step(raw,1,col,row,page)
        for cap in (0,1,10,255):step(raw,1,ui_cap=cap)
    # Every complete syllable built through native BL/BNE+A grid selection.
    positions={KEYS[v]:(i%15,i//15) for i,v in enumerate(selectors) if v<40}
    initial=MixedReplay(4);initial.model.state=Snapshot((0,0,0),3,None);initial._rebase();raw0=initial.serialize()
    for rank in range(11172):
        l=INITIALS[rank//588];v=MEDIALS[rank//28%21];t=FINALS[rank%28];path=[l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,))))
        raw=raw0
        for n,k in enumerate(path):
            col,row=positions[k];raw=step(raw,1,col,row,0,preloaded=n>0);stats['CPU_key_actions']+=1
        if MixedReplay.restore(raw).model.state.cells!=(0,0,0,rank):raise ValueError('grid canonical identity')
        # B must undo last actual key, not erase whole composed syllable.
        step(raw,3,preloaded=True);stats['syllable_paths']+=1
        if rank%2048==0:print('native A/B syllable',rank,flush=True)
    for off,val in [(75,0),(2,71),(1,0xFF)]:
        bad=bytearray(states[0]);bad[off]=val
        step(bytes(bad),1);step(bytes(bad),2)
    names=('hangul_keyboard_action_shim.py','bench_keyboard_actions.py','hangul_mixed_dispatch_thumb.py','hangul_mixed_keyedit_thumb.py','hangul_mixed_rebase_thumb.py','hangul_mixed_replay_state.py','hangul_mixed_editor_init.py')
    report=dict(id='exe45.hangul-keyboard.actions-CPU.v1',passed=True,rom_integrated=False,actual_game_layout_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=stats,nested_stack_bytes=208,selector_cells=90,active_jamo_cells=40,
        native_caller=dict(offset=0x34F08,bytes=6,sha256=sha(original),expected_hex=original.hex(),fixture_BL_hex=patch.hex(),unhandled_next='0x08034F0E',handled_next='0x08034F66'),
        no_HOST_compact_rewrites_between_syllable_keys=True,ISA=isas,dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in names},artifacts={n:sha(b) for n,b in blobs.items()},
        limits=['Only original BL+BNE caller window executes; outer drawing/navigation not executed. Source/current window guarded; source clone only.',
                'Forty jamo actions derived from existing unapproved layout candidate first six rows. Seventh candidate row is outside native navigation and all inactive.',
                'A/B priority, inactive selectors, loaded canonical delete, key-history undo and left/right connected in CPU fixtures. Initial editor/UI/key registers/pointers are HOST fixtures.',
                'Only candidate page0 jamo support. Other pages/commands consumed without edits: no page/Latin/comma/confirm/cancel/sound/rejection-feedback implementation or UI claim.',
                'All11172 last-slot syllables compose through grid+A and then B (A+B mask) without HOST compact rewriting. No natural gamepad/emulator pixel/commit/save verification.',
                'Fixture code addresses are not free ROM. No installed hook, RAM lifetime/IRQ stack budget or product layout adoption.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS native A/B BL+BNE CPU',stats,flush=True)

if __name__=='__main__':main()
