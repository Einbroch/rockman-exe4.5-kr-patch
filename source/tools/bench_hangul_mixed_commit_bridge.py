"""CPU compact confirmation incl partial rejection; not game save/commit."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from hangul_mixed_commit_bridge import assemble,record
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_mixed_record','cpu_mixed_replay'):
        path=base/name/'report.json';d=json.loads(path.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']:raise ValueError('commit dependencies')
        for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in d['artifacts'].items():require_hash(path.parent/n,h)
        deps[name]=sha(path.read_bytes())
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=base/'cpu_commit_bridge';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    table=(base/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08F06000,4096);u.mem_write(0x08F06000,blob);u.mem_protect(0x08F06000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,8192);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,dst,sp,stop=0x02000101,0x02001103,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(calls=0,rejected=0,syllable_capacity_paths=0,history_paths=0,maximum_record_bytes=0)
    def run(raw,available=76,capacity=22,source=src,target=dst):
        try:wanted=record(raw)
        except ValueError:wanted=None
        if available<76 or wanted is not None and (capacity<len(wanted) or not(source+76<=target or target+len(wanted)<=source)):wanted=None
        u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(source,raw);expected=bytearray(u.mem_read(0x02000000,8192))
        u.mem_write(sp-144,b'\x5A'*144);u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(source,target,available|capacity<<16,0x09000000)):u.reg_write(r,v)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();u.emu_start(0x08F06001,stop,count=30000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_R0)!=(len(wanted) if wanted else 0) or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('commit ABI')
        if wanted:expected[target-0x02000000:target-0x02000000+len(wanted)]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(expected) or bytes(u.mem_read(sp-144,4))!=b'\x5A'*4:raise ValueError('commit atomicity/stack')
        if any(not(sp-140<=a and a+n<=sp or wanted and target<=a and a+n<=target+len(wanted)) for a,n in writes):raise ValueError('commit write bound')
        stats['calls']+=1;stats['rejected']+=wanted is None
        if wanted:stats['maximum_record_bytes']=max(stats['maximum_record_bytes'],len(wanted))
    for cap in (4,10):
        for rank in range(11172):
            c=MixedReplay(cap);c.load([0]*(cap-1)+[rank]);run(c.serialize());stats['syllable_capacity_paths']+=1
    for cap in range(1,11):
        for count in range(cap+1):
            for word in (0,11171,11172,11190,tag(b'\x9B'),tag(b'\xE4\x98'),tag(b'\xE4\xE5')):
                c=MixedReplay(cap);c.model.state=Snapshot((word,)*count,0,None);c.model._validate(c.model.state);c._rebase();run(c.serialize())
    c=MixedReplay(10)
    for key in 'ㄱㄱㅗㅏㅣㄹㄱ'*10:
        if not c.press(key):raise ValueError('history fixture')
        run(c.serialize());stats['history_paths']+=1
    for _ in range(70):
        if not c.backspace():raise ValueError('history undo')
        run(c.serialize());stats['history_paths']+=1
    c=MixedReplay(4);c.load([0]);valid=c.serialize()
    for i in range(76):
        raw=bytearray(valid);raw[i]^=255;run(bytes(raw))
    for n in range(76):run(valid,available=n)
    for n in range(10):run(valid,capacity=n)
    for delta in range(-9,76):run(valid,target=src+delta)
    for a in range(4):
        for b in range(4):run(valid,source=src+a,target=dst+b)
    report=dict(id='exe45.hangul-keyboard.commit-bridge.v1',passed=True,rom_integrated=False,
                original_commit_ABI=False,format_adopted=False,caller_selected_new_format_required=True,
                helper_bytes=len(blob),own_stack_bytes=44,nested_stack_bytes=140,counts=stats,ISA=isa,dependencies=deps,
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_mixed_commit_bridge.py','bench_hangul_mixed_commit_bridge.py')},
                artifacts={'helper.bin':sha(blob)},
                limits=['CPU compact replay->fixed record only; source/record/table and disjoint stack owned by caller.',
                        'HOST produces compact history fixture; native bridge replays it and rejects partial/empty. Not actual game keypad or original commit ABI/UI rejection.',
                        'Format selection/all writers/normalize/readers/save migration/fresh-load unresolved; no ROM integration.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS compact -> selected fixed record',len(blob),stats,flush=True)

if __name__=='__main__':main()
