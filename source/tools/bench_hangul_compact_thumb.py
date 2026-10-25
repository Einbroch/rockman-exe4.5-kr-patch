"""Isolated ARMv4T compact wrapper tests. Not game runtime evidence."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from hangul_compact_state import CompactComposer
from hangul_compact_thumb import assemble

def main():
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    dependency=ROOT/'analysis/hangul_keyboard_v1/cpu_composer'
    report=json.loads((dependency/'report.json').read_text(encoding='utf8'))
    if not report['passed']:raise ValueError('backend not passed')
    for n,h in report['artifacts'].items():require_hash(dependency/n,h)
    for n,h in report['tools'].items():require_hash(ROOT/'tools'/n,h)
    blob,isa=assemble()
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,16384)
    for addr,n in [(0x08000000,'feed.bin'),(0x08001000,'undo.bin')]:u.mem_write(addr,(dependency/n).read_bytes())
    u.mem_write(0x08002000,blob)
    u.mem_write(0x08003000,struct.pack('<4I',0x08000001,0x08001001,0x09000000,0x09200000))
    u.mem_protect(0x08000000,16384,UC_PROT_READ|UC_PROT_EXEC)
    for addr,n in [(0x09000000,'transitions.bin'),(0x09200000,'deletions.bin')]:
        data=(dependency/n).read_bytes();size=(len(data)+4095)&~4095
        u.mem_map(addr,size);u.mem_write(addr,data);u.mem_protect(addr,size,UC_PROT_READ)
    u.mem_map(0x02000000,4096);u.mem_map(0x02002000,4096,UC_PROT_READ)
    u.mem_map(0x03007000,4096);u.mem_map(0x0ff00000,4096)
    state=0x02000100;baseline=0x02002000;stack=0x03007f00;stop=0x0ff00000
    preserved=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(calls=0,rejected=0,malformed=0)
    def execute(raw,base,action,expected,accepted,state_ptr=state,base_ptr=baseline):
        u.mem_write(state-4,b'\xa7'*4+raw+b'\xa7'*4);u.mem_write(baseline,base)
        u.mem_write(stack-448,b'\xa9'*4)
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for reg,value in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],[state_ptr,base_ptr,action,0x08003000]):u.reg_write(reg,value)
        for i,reg in enumerate(preserved):u.reg_write(reg,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,stack);u.reg_write(UC_ARM_REG_LR,stop|1)
        u.emu_start(0x08002001,stop,count=100000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_R0)!=int(accepted) or u.reg_read(UC_ARM_REG_SP)!=stack or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(preserved)):raise ValueError(f'ABI action={action} raw={raw.hex()} status={u.reg_read(UC_ARM_REG_R0)}')
        if bytes(u.mem_read(state-4,72))!=b'\xa7'*4+expected+b'\xa7'*4:raise ValueError(f'state action={action} raw={raw.hex()} actual={bytes(u.mem_read(state,64)).hex()} expected={expected.hex()}')
        if bytes(u.mem_read(baseline,20))!=base or bytes(u.mem_read(stack-448,4))!=b'\xa9'*4:raise ValueError('baseline/stack bounds')
        counts['calls']+=1;counts['rejected']+=not accepted
    def base(c):
        m=Composer(c.limit);m.load(c.baseline);return encode_state(m)[:20]
    def step(c,action):
        before=c.serialize()
        accepted=c.press(KEYS[action]) if action<40 else c.backspace() if action==40 else action==41
        execute(before,base(c),action,c.serialize(),accepted)
        return accepted
    print('compact wrapper full syllable CPU paths',flush=True)
    for li,l in enumerate(INITIALS):
        for vi,v in enumerate(MEDIALS):
            for ti,t in enumerate(FINALS):
                c=CompactComposer(1)
                for key in [l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,)))):
                    if not step(c,KEYS.index(key)):raise ValueError('creation reject')
                if c.candidate()!=chr(0xac00+li*588+vi*28+ti):raise ValueError('candidate')
                step(c,41)
                while step(c,40):pass
                c=CompactComposer(1,chr(0xac00+li*588+vi*28+ti))
                while step(c,40):pass
        print('initial',li+1,'/19',flush=True)
    for limit in range(1,9):
        for key in range(40):step(CompactComposer(limit,'가'*limit),key)
    c=CompactComposer(8,chr(0xac00+588+10*28+9)*8)
    while step(c,40):pass
    if c.deletions!=56:raise ValueError('baseline bound')
    for key in 'ㄱㄱㅗㅏㅣㄹㄱ'*8:
        if not step(c,KEYS.index(key)):raise ValueError('maximum path rejected')
    if len(c.keys)!=56:raise ValueError('key boundary')
    step(c,0);step(c,41)
    # Every packed slot crosses the same byte boundaries on the native path.
    maximum=c.serialize()
    for slot in range(56):
        bits=int.from_bytes(maximum[20:62],'little')
        bits=(bits&~(63<<(slot*6)))|(63<<(slot*6))
        bad=maximum[:20]+bits.to_bytes(42,'little')+maximum[62:]
        execute(bad,base(c),41,bad,False);counts['malformed']+=1
    while step(c,40):pass
    for text in ['ㄱㅜㄱㅇㅓ','ㄷㅏㄹㄱㅏ','ㄲㅘㅣㄹㄱㅏ']:
        c=CompactComposer(4)
        for key in text:step(c,KEYS.index(key))
        for key in range(40):step(c,key)
        while step(c,40):pass
    c=CompactComposer(4);raw=c.serialize();b=base(c)
    for slot in range(56):
        bad=raw[:20]+(1<<(slot*6)).to_bytes(42,'little')+raw[62:]
        execute(bad,b,41,bad,False);counts['malformed']+=1
    loaded=CompactComposer(4,'국');wrong=CompactComposer(4,'가')
    execute(loaded.serialize(),base(wrong),41,loaded.serialize(),False);counts['malformed']+=1
    for offset,values in [(0,[1,9]),(1,[0,9]),(2,[1,57]),(3,[1,2]),(4,[0]),(20,[40,63]),(61,[4]),(62,[1,57]),(63,[1,255])]:
        for value in values:
            bad=bytearray(raw);bad[offset]=value
            for action in [0,40,41]:execute(bytes(bad),b,action,bytes(bad),False);counts['malformed']+=1
    for off,values in [(0,[9]),(1,[0,5]),(2,[1]),(3,[1]),(4,[0])]:
        for value in values:
            bad=bytearray(b);bad[off]=value;execute(raw,bytes(bad),41,raw,False);counts['malformed']+=1
    for action in [42,255,0xffffffff]:execute(raw,b,action,raw,False)
    for sp,bp in [(state+1,baseline),(state,baseline+1),(state,state),(state,state+60)]:execute(raw,b,41,raw,False,sp,bp)
    out=ROOT/'analysis/hangul_keyboard_v1/cpu_compact';out.mkdir(parents=True,exist_ok=True)
    (out/'wrapper.bin').write_bytes(blob)
    result=dict(id='exe45.hangul-keyboard.native-compact.v1',passed=True,rom_integrated=False,compact_state_bytes=64,baseline_bytes=20,stack_bytes_including_nested_calls=444,complete_syllable_paths=11172,counts=counts,machine_code=isa,dependency_report_sha256=sha((dependency/'report.json').read_bytes()),artifacts={'wrapper.bin':sha(blob)},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['hangul_compact_thumb.py','bench_hangul_compact_thumb.py','hangul_compact_state.py']},limits=['Isolated caller-owned aligned state and immutable baseline; descriptor and pointer extents trusted.','Game stack budget, state ownership, baseline bridge, hooks, rendering and save compatibility unresolved.','Malformed vectors are boundary examples, not exhaustive invalid-domain coverage.'])
    (out/'report.json').write_text(json.dumps(result,indent=2),encoding='utf8');print('PASS',counts,flush=True)

if __name__=='__main__':main()
