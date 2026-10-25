"""Logical query CPU vs original pointer_count leaf; not game/cursor drawing."""
import json, random, struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from hangul_mixed_count_thumb import assemble, count
from hangul_mixed_keyedit_thumb import assemble as assemble_edit
from hangul_mixed_replay_state import MixedReplay, KEYS, apply
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag
from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB


def main():
    root=ROOT/'analysis/hangul_keyboard_v1'
    rp=root/'cpu_mixed_replay/report.json';dependency=json.loads(rp.read_text(encoding='utf8'))
    if not dependency['passed'] or dependency['rom_integrated']:raise ValueError('replay candidate scope')
    for n,h in dependency['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in dependency['artifacts'].items():require_hash(rp.parent/n,h)
    for n,h in dependency['host_dependency'].items():require_hash(ROOT/n,h)
    ep=root/'cpu_mixed_keyedit/report.json';edit_report=json.loads(ep.read_text(encoding='utf8'))
    if not edit_report['passed'] or edit_report['rom_integrated'] or edit_report['dependencies']['cpu_mixed_replay']!=sha(rp.read_bytes()):raise ValueError('keyedit dependency')
    for n,h in edit_report['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in edit_report['artifacts'].items():require_hash(ep.parent/n,h)
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    current=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(current,identity)
    original_code=rom[0x35620:0x3562C]
    if current.read_bytes()[0x35620:0x3562C]!=original_code:raise ValueError('pointer_count drift')
    ip=root/'cpu_editor_init/report.json';init_report=json.loads(ip.read_text(encoding='utf8'))
    if not init_report['passed'] or init_report['source_sha256']!=profile['sha256'] or init_report['current_rom_sha256']!=identity:raise ValueError('source instruction inventory')
    native_scope=next(s for s in init_report['bounded_consumer_regions'] if s['id']=='pointer_count')
    if native_scope['sha256']!=sha(original_code):raise ValueError('pointer_count ISA binding')
    direct_candidates=[]
    for at in range(0,len(rom)-3,2):
        hi=int.from_bytes(rom[at:at+2],'little');lo=int.from_bytes(rom[at+2:at+4],'little')
        if hi&0xF800==0xF000 and lo&0xF800==0xF800:
            delta=(hi&2047)<<12|(lo&2047)<<1
            if delta&0x400000:delta-=0x800000
            if 0x08000000+at+4+delta==0x08035620:direct_candidates.append(at)
    if direct_candidates!=[0x35350,0x35486,0x35496,0x355FA]:raise ValueError('logical count direct BL candidates')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);caller_windows=[]
    product=current.read_bytes()
    for at in direct_candidates:
        data=rom[at-4:at+12];rows=list(cs.disasm(data,0x08000000+at-4))
        if product[at-4:at+12]!=data or sum(i.size for i in rows)!=16:raise ValueError('query caller window')
        for i in rows:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('query caller ARMv4T')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('query caller instruction roundtrip')
        caller_windows.append(dict(call_pc=hex(0x08000000+at),start=hex(0x08000000+at-4),end_exclusive=hex(0x08000000+at+12),sha256=sha(data),instructions=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in rows]))
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=root/'cpu_mixed_count';out.mkdir(exist_ok=True)
    (out/'helper.bin').write_bytes(blob);blob=(out/'helper.bin').read_bytes()
    edit,edit_isa=assemble_edit(0x08803000);(out/'edit_dependency.bin').write_bytes(edit)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08802000,4096);u.mem_write(0x08802000,blob);u.mem_protect(0x08802000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08803000,4096);u.mem_write(0x08803000,edit);u.mem_protect(0x08803000,4096,UC_PROT_READ|UC_PROT_EXEC)
    table=(root/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,editor,sp,stop=0x02000101,0x0200FC40,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    stats=dict(query_calls=0,rejected=0,original_leaf_comparisons=0,syllable_history_queries=0,native_edit_query_paths=0,uninterrupted_queries=0,baseline_differs_from_current=0,malformed_queries=0)
    watching=[False]
    def writes(cpu,access,address,width,value,user):
        if watching[0] and not sp-100<=address<=sp-width:raise ValueError('query wrote outside stack100')
    u.hook_add(UC_HOOK_MEM_WRITE,writes)
    def call(pc,args,stack):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        for reg,val in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):u.reg_write(reg,val)
        for i,reg in enumerate(regs):u.reg_write(reg,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1)
        watching[0]=pc==0x08802000
        try:u.emu_start(pc|1,stop,count=25000)
        finally:watching[0]=False
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('query callee/SP')
        if bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('query stack extent')
        return u.reg_read(UC_ARM_REG_R0),u.reg_read(UC_ARM_REG_R1)
    def query(raw,selector,available=76,pointer=src,initialized=False):
        try:value=count(raw,selector)
        except ValueError:value=None
        if available<76 or available>65535 or pointer+76>0xFFFFFFFF:value=None
        if not initialized:u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(src,raw)
        before=bytes(u.mem_read(0x02000000,8192))
        result=call(0x08802000,[pointer,selector,available,0x09000000],100)
        if result!=((0,0) if value is None else (value,1)):raise ValueError('query result')
        if bytes(u.mem_read(0x02000000,8192))!=before:raise ValueError('query input/bounds write')
        stats['query_calls']+=1;stats['rejected']+=value is None
        if value is not None:
            baseline=raw[1]&15 if selector==20 else raw[0]>>4
            stats['baseline_differs_from_current']+=baseline!=value
        return result
    print('native count/caret original leaf comparison',flush=True)
    for cap in range(1,11):
        for n in range(cap+1):
            for cursor in range(n+1):
                m=MixedReplay(cap);m.load((tag(b'\x9B'),)*n);m.model.state=Snapshot(m.model.state.cells,cursor,None);m._rebase();raw=m.serialize()
                u.mem_write(editor+16,struct.pack('<3I',editor+32,editor+32+cursor*2,editor+32+n*2))
                for selector,wanted in ((20,cursor),(24,n)):
                    native=call(0x08035620,[selector,0,0x12345678,0],0)
                    if native!=(wanted,editor+32):raise ValueError('original pointer count')
                    if query(raw,selector)!=(wanted,1):raise ValueError('new native count')
                    stats['original_leaf_comparisons']+=1
    print('all11172 syllables; real packed history queried, not baseline header',flush=True)
    for l in INITIALS:
        for v in MEDIALS:
            for t in FINALS:
                m=MixedReplay(10)
                path=[l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,))))
                for key in path[:-1]:
                    if not m.press(key):raise ValueError('construction')
                raw=m.serialize();accepted,wanted=apply(raw,'jamo',path[-1])
                if not accepted:raise ValueError('last key')
                u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(src,raw);before=bytearray(u.mem_read(0x02000000,8192))
                result=call(0x08803000,[src,KEYS.index(path[-1]),76,0x09000000],196)
                if result[0]!=1:raise ValueError('native edit result')
                before[src-0x02000000:src-0x02000000+76]=wanted
                if bytes(u.mem_read(0x02000000,8192))!=bytes(before):raise ValueError('native edit expected writes')
                actual=bytes(u.mem_read(src,76))
                for selector in (20,24):query(actual,selector,initialized=True);stats['syllable_history_queries']+=1
                stats['native_edit_query_paths']+=1
    # Accepted/rejected edits and queries on the same host-owned state; not native edit pipeline.
    rng=random.Random(1045);raw=MixedReplay(10).serialize()
    for i in range(1000):
        action=rng.choice(('jamo','move','native','backspace'))
        value=rng.choice(KEYS) if action=='jamo' else rng.choice((-1,1)) if action=='move' else rng.choice((b'\x9B',b'\xE4\x98',b'\xE4\xE5')) if action=='native' else None
        accepted,raw=apply(raw,action,value)
        for selector in (20,24):query(raw,selector);stats['uninterrupted_queries']+=1
    valid=MixedReplay(4).serialize()
    for at in range(76):
        raw=bytearray(valid);raw[at]^=255
        for selector in (20,24):query(bytes(raw),selector);stats['malformed_queries']+=1
    for selector in tuple(range(32))+(0xFFFFFFFF,):
        if selector not in (20,24):query(valid,selector)
    for available in tuple(range(76))+(65536,0xFFFFFFFF):query(valid,20,available)
    query(valid,20,pointer=0xFFFFFFF0)
    for alignment in range(4):
        # query copies the source into the requested unaligned address for this case.
        u.mem_write(src+alignment,valid)
        before=bytes(u.mem_read(0x02000000,8192))
        if call(0x08802000,[src+alignment,24,76,0x09000000],100)!=(0,1):raise ValueError('byte alignment')
        if bytes(u.mem_read(0x02000000,8192))!=before:raise ValueError('aligned read-only')
        stats['query_calls']+=1
    if stats['syllable_history_queries']!=22344 or stats['original_leaf_comparisons']!=570 or stats['baseline_differs_from_current']<22344:raise ValueError('query coverage')
    names=['hangul_mixed_count_thumb.py','bench_hangul_mixed_count.py','hangul_mixed_replay_thumb.py','hangul_mixed_keyedit_thumb.py','hangul_mixed_replay_state.py','hangul_mixed_editor.py','extended_dialogue.py']
    report=dict(id='exe45.hangul-keyboard.mixed-count.v1',passed=True,rom_integrated=False,source_sha256=profile['sha256'],current_rom_sha256=identity,helper_bytes=len(blob),own_stack_bytes=32,nested_stack_bytes=100,counts=stats,ISA=isa,relocated_edit_ISA=edit_isa,original_leaf_sha256=sha(original_code),dependencies={'cpu_mixed_replay':sha(rp.read_bytes()),'cpu_mixed_keyedit':sha(ep.read_bytes())},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in names},artifacts={'helper.bin':sha(blob),'edit_dependency.bin':sha(edit)},limits=['New value/status ABI is not original pointer_count live-out ABI or a game hook.','Original leaf executes only controlled valid pointers; malformed legacy pointer policy unproven.','All11172 final-key paths execute native edit -> query without host rewriting; randomized uninterrupted mixed edits use host model.','Logical cursor/count does not establish glyph pixel advances, original eight-pixel cursor placement, UI drawing/cache or persistence.','Query stack100 and separate keyedit196 checked only in isolated CPU fixtures; actual game/IRQ lifetime unresolved.'])
    report['dependencies']['cpu_editor_init']=sha(ip.read_bytes())
    report['direct_count_BL_candidate_windows']=caller_windows
    report['limits'].append('Four direct BL encoding candidates have bounded windows; raw aligned ROM scan is not indirect-call/reference completeness or full caller execution.')
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(current,identity)
    print('PASS logical query CPU',stats,flush=True)


if __name__=='__main__':main()
