"""CPU selected-record import and encoder->importer, not native game saves."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from hangul_mixed_record_import import assemble
from hangul_mixed_record import pack_surface,unpack_selected_record

def main():
    base=ROOT/'analysis/hangul_keyboard_v1'
    dep=base/'cpu_mixed_record/report.json';d=json.loads(dep.read_text(encoding='utf8'))
    if not d['passed'] or d['format_adopted'] or d['rom_integrated']:raise ValueError('record dependency')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dep.parent/n,h)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=base/'cpu_mixed_record_import';out.mkdir(exist_ok=True)
    (out/'helper.bin').write_bytes(blob)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08F04000,8192);u.mem_write(0x08F04000,(dep.parent/'encoder.bin').read_bytes());u.mem_write(0x08F05000,blob)
    u.mem_protect(0x08F04000,8192,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,8192);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,dst,sp,stop=0x02000101,0x02001103,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(calls=0,rejected=0,word_domain=0,encoder_import_syllables=0)
    def call(pc,args,stack):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();u.emu_start(pc|1,stop,count=10000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('import ABI/stack')
        return u.reg_read(UC_ARM_REG_R0)
    def run(record,cap,available=None,capacity=76,source=src,target=dst,preloaded=False):
        available=len(record) if available is None else available
        try:wanted=unpack_selected_record(record[:min(available,2*cap+2)],cap)
        except (ValueError,TypeError):wanted=None
        if capacity<76 or wanted is not None and not(source+len(record)<=target or target+76<=source):wanted=None
        if not preloaded:u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(source,record)
        expected=bytearray(u.mem_read(0x02000000,8192))
        if call(0x08F05000,[source,target,available|capacity<<16,cap],124)!=int(wanted is not None):raise ValueError('import return')
        if wanted:expected[target-0x02000000:target-0x02000000+76]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(expected):raise ValueError('import identity/atomicity')
        if any(not(sp-124<=a and a+n<=sp or wanted and target<=a and a+n<=target+76) for a,n in writes):raise ValueError('import write bound')
        stats['calls']+=1;stats['rejected']+=wanted is None
    def surface(words,cap):
        return bytes([len(words),cap,0,255])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words))))
    for word in range(65536):
        record=b'\x81'+struct.pack('<4H',word,65535,65535,65535)+b'\xE5'
        run(record,4);stats['word_domain']+=1
    # No HOST rewrite between native encoder and native importer.
    for rank in range(11172):
        raw=surface([0]*9+[rank],10)
        u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(0x02000401,raw)
        if call(0x08F04000,[0x02000401,src,24|22<<16,0],96)!=22:raise ValueError('encoder return')
        emitted=bytes(u.mem_read(src,22))
        if emitted!=pack_surface(raw):raise ValueError('encoder bytes')
        run(emitted,10,preloaded=True);stats['encoder_import_syllables']+=1
    for cap in range(1,11):
        good=pack_surface(surface([229],cap))
        for count in range(1,cap+1):
            for word in (0,11171,0x8000,0x80E3,0x8100,0x81FF):
                run(pack_surface(surface([word]*count,cap)),cap)
        for value in range(256):
            run(bytes([value])+good[1:],cap);run(good[:-1]+bytes([value]),cap)
        for i in range(1,len(good)-1):
            corrupt=bytearray(good);corrupt[i]^=255;run(bytes(corrupt),cap)
        for n in range(len(good)):run(good,cap,available=n)
        for n in range(76):run(good,cap,capacity=n)
    good=pack_surface(surface([0],4))
    for cap in (0,11,255):run(good,cap)
    for delta in range(-75,len(good)):run(good,4,target=src+delta)
    for a in range(4):
        for b in range(4):run(good,4,source=src+a,target=dst+b)
    report=dict(id='exe45.hangul-keyboard.mixed-record-import-candidate.v1',passed=True,
                rom_integrated=False,format_adopted=False,caller_selected_new_format_required=True,
                native_record_importer=True,helper_bytes=len(blob),own_stack_bytes=88,nested_stack_bytes=124,
                counts=stats,ISA=isa,dependencies={'cpu_mixed_record':sha(dep.read_bytes())},
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_mixed_record_import.py','bench_hangul_mixed_record_import.py')},
                artifacts={'helper.bin':sha(blob)},
                limits=['CPU encoder->selected importer handles all11172 syllables in final full-cap10 slot without HOST rewrite. This is not the game commit/reader/save pipeline.',
                        'Format selected by caller, no automatic legacy discrimination or migration. Structural native tags do not establish active keyboard/glyph membership.',
                        'Caller owns disjoint input/output/stack extents. Game layout, all consumers, normalization, actual screen and save/fresh-load remain unresolved.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS mixed record native import and encoder->import',stats,flush=True)

if __name__=='__main__':main()
