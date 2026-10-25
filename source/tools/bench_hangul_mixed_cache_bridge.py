"""Compact->cache CPU bounds/atomic composition, not native descriptor ABI."""
import json
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from hangul_mixed_cache_bridge import assemble, stream
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_editor import Snapshot
from hangul_native_tokens import tag


def main():
    root=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_mixed_replay','cpu_mixed_display'):
        path=root/name/'report.json';r=json.loads(path.read_text(encoding='utf8'))
        if not r['passed'] or r['rom_integrated']:raise ValueError('cache dependencies')
        for n,h in r['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in r['artifacts'].items():require_hash(path.parent/n,h)
        deps[name]=sha(path.read_bytes())
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=root/'cpu_cache_bridge';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    table=(root/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08F01000,4096);u.mem_write(0x08F01000,blob);u.mem_protect(0x08F01000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,8192);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,dst,sp,stop=0x02000101,0x02001103,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];stats=dict(calls=0,rejected=0,maximum_stream_bytes=0,packed_history_paths=0)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def run(raw,available=76,capacity=41,source=src,target=dst,pointer=None):
        try:wanted=stream(raw)
        except ValueError:wanted=None
        if available<76 or capacity<41 or source+76>0xFFFFFFFF or target+41>0xFFFFFFFF or not(source+76<=target or target+41<=source) or pointer is not None:wanted=None
        u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(source,raw);expected=bytearray(u.mem_read(0x02000000,8192))
        u.mem_write(sp-116,b'\x5A'*116);u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(source if pointer is None else pointer,target,available|capacity<<16,0x09000000)):u.reg_write(r,v)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
        u.emu_start(0x08F01001,stop,count=30000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('bridge ABI')
        if u.reg_read(UC_ARM_REG_R0)!=(len(wanted) if wanted else 0):raise ValueError('bridge return')
        if wanted:expected[target-0x02000000:target-0x02000000+len(wanted)]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(expected) or bytes(u.mem_read(sp-116,4))!=b'\x5A'*4:raise ValueError('bridge atomic/stack')
        if any(not(sp-112<=a and a+n<=sp or wanted is not None and target<=a and a+n<=target+len(wanted)) for a,n in writes):raise ValueError('bridge unexpected write')
        stats['calls']+=1;stats['rejected']+=wanted is None
        if wanted:stats['maximum_stream_bytes']=max(stats['maximum_stream_bytes'],len(wanted))
    for cap in range(1,11):
        for n in range(cap+1):
            for word in (0,11171,11172,11190,tag(b'\x9B'),tag(b'\xE4\x98'),tag(b'\xE4\xE5')):
                c=MixedReplay(cap)
                c.model.state=Snapshot((word,)*n,0,None)
                c.model._validate(c.model.state);c._rebase();run(c.serialize())
    c=MixedReplay(10)
    for key in 'ㄱㄱㅗㅏㅣㄹㄱ'*10:
        if not c.press(key):raise ValueError('maximum history')
        run(c.serialize());stats['packed_history_paths']+=1
    valid=MixedReplay(4).serialize()
    for at in range(76):
        raw=bytearray(valid);raw[at]^=255;run(bytes(raw))
    for n in range(76):run(valid,available=n)
    for n in range(41):run(valid,capacity=n)
    for delta in range(-40,76):run(valid,target=src+delta)
    for a in range(4):
        for b in range(4):run(valid,source=src+a,target=dst+b)
    run(valid,pointer=0xFFFFFFF0);run(valid,target=0xFFFFFFF0)
    report=dict(id='exe45.hangul-keyboard.cache-bridge.v1',passed=True,rom_integrated=False,helper_bytes=len(blob),own_stack_bytes=44,nested_stack_bytes=112,required_cache_extent=41,counts=stats,ISA=isa,dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['hangul_mixed_cache_bridge.py','bench_hangul_mixed_cache_bridge.py','hangul_mixed_replay_thumb.py','hangul_mixed_display.py','hangul_mixed_keyedit_thumb.py','hangul_mixed_replay_state.py']},artifacts={'helper.bin':sha(blob)},limits=['Caller-owned cache/source/table and disjoint stack fixture only; no descriptor0 ABI, game/cache allocation or lifetime adoption.','Two verified helpers execute sequentially; no native parser/queue/VRAM included in this new bridge fixture.','Cache requires41bytes even for short/empty strings; actual descriptor32 replacement remains uninstalled.','Stack112 is CPU fixture depth, not game caller/IRQ budget.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS compact -> bounded edit cache CPU',stats,flush=True)


if __name__=='__main__':main()
