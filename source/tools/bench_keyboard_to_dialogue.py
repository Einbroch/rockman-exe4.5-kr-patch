"""Uninterrupted CPU jamo edit -> compact commit -> native dialogue provider.

Fixture supplies initial editor/context and keys only. No HOST rewrite of
compact, committed record or display stream between CPU stages. NOT gameplay,
automatic format discrimination, UI, save or Korean pixel verification.
"""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
from hangul_mixed_keyedit_thumb import assemble as assemble_key
from hangul_mixed_replay_state import MixedReplay, KEYS
from hangul_mixed_editor import Snapshot
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_SPLIT
from hangul_mixed_commit_bridge import record

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={};reports={}
    for name in ('cpu_mixed_keyedit','cpu_commit_bridge','cpu_dialogue_record_copy','cpu_record_display','cpu_composer'):
        path=base/name/'report.json';d=read(path)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('pipeline dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(path.parent/n,h)
        deps[name]=sha(path.read_bytes());reports[name]=d
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity=reports['cpu_dialogue_record_copy']['current_rom_sha256'];require_hash(play,identity)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    key,isa=assemble_key(0x08F0B000);out=base/'cpu_keyboard_to_dialogue';out.mkdir(exist_ok=True);(out/'keyedit.bin').write_bytes(key)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom)
    f=reports['cpu_dialogue_record_copy']['fixture_BL'];patch=bytes.fromhex(f['fixture_hex'])
    if rom[f['offset']:f['offset']+4].hex()!=f['expected_hex']:raise ValueError('provider fixture source')
    u.mem_write(0x08000000+f['offset'],patch)
    u.mem_write(0x08300000,(base/'cpu_dialogue_record_copy/helper.bin').read_bytes())
    u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for a,b in [(0x08F0B000,key),(0x08F06000,(base/'cpu_commit_bridge/helper.bin').read_bytes()),(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes())]:
        u.mem_map(a,4096);u.mem_write(a,b);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    table=(base/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    compact,rec,ctx,script,sp,stop=0x02004001,0x020010A6,0x0200FA20,0x02003000,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    seed=bytes(range(256))*1024;stats=dict(syllable_pipelines=0,CPU_key_actions=0,partial_commit_rejections=0,successful_commits=0,native_provider_calls=0,maximum_stream_bytes=0)
    def call(pc,args,stack,preserved=True):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        initial=[0x13579000+i for i in range(13)]
        for i,v in enumerate(args):initial[i]=v
        for r,v in zip(regs,initial):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();u.emu_start(pc|1,stop,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('pipeline return/stack')
        if preserved and any(u.reg_read(r)!=initial[i] for i,r in enumerate(regs) if 4<=i<=11):raise ValueError('pipeline preserved registers')
        return u.reg_read(UC_ARM_REG_R0)
    def check(before,regions,stack):
        expected=bytearray(before)
        for a,raw in regions:expected[a-0x02000000:a-0x02000000+len(raw)]=raw
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('pipeline external memory identity')
        if any(not (sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(raw) for s,raw in regions)) for a,n in writes):raise ValueError('pipeline write bounds')
    initial=MixedReplay(4);initial.model.state=Snapshot((0,0,0),3,None);initial._rebase();initial_bytes=initial.serialize()
    for rank in range(11172):
        l=INITIALS[rank//588];v=MEDIALS[rank//28%21];t=FINALS[rank%28]
        path=[l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,))))
        model=MixedReplay.restore(initial_bytes)
        u.mem_write(0x02000000,seed);u.mem_write(compact,initial_bytes)
        slot=rank%8;dst=0x02010AC0+slot*128
        u.mem_write(script,b'\xF9\x0C\x10');u.mem_write(ctx+0x64,struct.pack('<H',slot));u.mem_write(ctx+5,b'\xFE')
        for n,k in enumerate(path):
            before=bytes(u.mem_read(0x02000000,0x40000))
            if not model.press(k) or call(0x08F0B000,[compact,KEYS.index(k),76,0x09000000],196)!=1:raise ValueError('CPU accepted key path')
            check(before,[(compact,model.serialize())],196);stats['CPU_key_actions']+=1
            if n==0:
                before=bytes(u.mem_read(0x02000000,0x40000))
                if call(0x08F06000,[compact,rec,76|10<<16,0x09000000],140)!=0:raise ValueError('partial committed')
                check(before,[],140);stats['partial_commit_rejections']+=1
        if model.model.state.cells!=(0,0,0,rank):raise ValueError('final canonical identity')
        raw=record(model.serialize());before=bytes(u.mem_read(0x02000000,0x40000))
        if call(0x08F06000,[compact,rec,76|10<<16,0x09000000],140)!=10:raise ValueError('CPU commit')
        check(before,[(rec,raw)],140);stats['successful_commits']+=1
        # Only registers are set here. No record/cache/string HOST writes.
        before=bytes(u.mem_read(0x02000000,0x40000));args=[0,0,0,0,script,ctx]
        if call(0x080517D0,args,104,False)!=1 or u.reg_read(UC_ARM_REG_R4)!=dst or u.reg_read(UC_ARM_REG_R5)!=ctx:raise ValueError('native provider live-outs')
        wanted=(b'\xF9\xFC\0\0'*3)+b'\xF9\xFC'+struct.pack('<H',rank)+b'\xE5'
        check(before,[(dst,wanted),(ctx+5,b'\xFF'),(ctx+0x64,struct.pack('<H',slot+1)),(ctx+0x2C,struct.pack('<I',dst)),(ctx+0x44,struct.pack('<I',script+3))],104)
        if any(u.reg_read(regs[i])!=0x13579000+i for i in range(6,13)):raise ValueError('native preserved high registers')
        stats['native_provider_calls']+=1;stats['syllable_pipelines']+=1;stats['maximum_stream_bytes']=max(stats['maximum_stream_bytes'],len(wanted))
    report=dict(id='exe45.hangul-keyboard.keyboard-to-dialogue-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,caller_selected_mixed_format_required=True,no_HOST_surface_rewrite_between_CPU_stages=True,
        counts=stats,ISA=isa,dependencies=deps,tools={'bench_keyboard_to_dialogue.py':sha((ROOT/'tools/bench_keyboard_to_dialogue.py').read_bytes())},artifacts={'keyedit.bin':sha(key)},
        limits=['Initial three complete syllables/cursor3/editor76/context/native script are HOST fixtures; all last-slot jamo inputs and commits execute CPU machine code.',
                'Partial-after-initial rejection, fullcap4 final syllables11172 and native provider slots0..7. Not full editing-command coverage or actual keyboard grid/confirm UI.',
                'Fixture source-clone code/BL changes only; not ROM placement/free space adoption.',
                'No marker discrimination/save-version adoption, selected-record refresh hooks, cache writer/lifetime/IRQ budget, actual glyph pixels, ROM installation or save/reload.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS uninterrupted CPU keyboard->commit->native dialogue provider',stats,flush=True)

if __name__=='__main__':main()
