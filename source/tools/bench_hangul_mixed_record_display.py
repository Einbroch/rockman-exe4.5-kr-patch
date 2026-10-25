"""CPU fixed record->display and encoder pipeline; no game redisplay hook."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from hangul_mixed_record_display import assemble,stream
from hangul_mixed_record import pack_surface

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';dep=base/'cpu_mixed_record/report.json';d=json.loads(dep.read_text(encoding='utf8'))
    if not d['passed'] or d['rom_integrated']:raise ValueError('record dependency')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dep.parent/n,h)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble();out=base/'cpu_record_display';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for a,b in [(0x08F04000,(dep.parent/'encoder.bin').read_bytes()),(0x08F09000,blob)]:
        u.mem_map(a,4096);u.mem_write(a,b);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,8192);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,dst,sp,stop=0x02000101,0x02001103,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(calls=0,rejected=0,word_domain=0,encoder_display_syllables=0,maximum_stream_bytes=0)
    def call(pc,args,stack):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();u.emu_start(pc|1,stop,count=10000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)) or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('record display ABI/stack')
        return u.reg_read(UC_ARM_REG_R0)
    def run(raw,cap,available=None,capacity=41,source=src,target=dst,preloaded=False):
        available=len(raw) if available is None else available
        try:wanted=stream(raw[:min(available,2*cap+2)],cap)
        except (ValueError,TypeError):wanted=None
        if wanted and (capacity<len(wanted) or target+capacity>0xFFFFFFFF or not(source+2*cap+2<=target or target+capacity<=source)):wanted=None
        if not preloaded:u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(source,raw)
        expected=bytearray(u.mem_read(0x02000000,8192))
        if call(0x08F09000,[source,target,available|capacity<<16,cap],80)!=(len(wanted) if wanted else 0):raise ValueError('record display status')
        if wanted:expected[target-0x02000000:target-0x02000000+len(wanted)]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(expected):raise ValueError('record display identity/atomicity')
        if any(not(sp-80<=a and a+n<=sp or wanted and target<=a and a+n<=target+len(wanted)) for a,n in writes):raise ValueError('record display write interval')
        stats['calls']+=1;stats['rejected']+=wanted is None
        if wanted:stats['maximum_stream_bytes']=max(stats['maximum_stream_bytes'],len(wanted))
    def surface(words,cap):
        return bytes([len(words),cap,0,255])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words))))
    for word in range(65536):
        run(b'\x81'+struct.pack('<4H',word,65535,65535,65535)+b'\xE5',4);stats['word_domain']+=1
    for rank in range(11172):
        raw=surface([0]*9+[rank],10)
        u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(0x02000401,raw)
        if call(0x08F04000,[0x02000401,src,24|22<<16,0],96)!=22:raise ValueError('encoder status')
        emitted=bytes(u.mem_read(src,22))
        if emitted!=pack_surface(raw):raise ValueError('encoder record identity')
        run(emitted,10,preloaded=True);stats['encoder_display_syllables']+=1
    for cap in range(1,11):
        for count in range(1,cap+1):
            for word in (0,11171,0x8000,0x80E3,0x8100,0x81FF,0x8198,0x81E5):
                run(pack_surface(surface([word]*count,cap)),cap)
        good=pack_surface(surface([229],cap))
        for value in range(256):
            run(bytes([value])+good[1:],cap);run(good[:-1]+bytes([value]),cap)
        for n in range(len(good)):run(good,cap,available=n)
        full=pack_surface(surface([0]*cap,cap))
        for n in range(4*cap+2):run(full,cap,capacity=n)
        for i in range(1,len(good)-1):
            raw=bytearray(good);raw[i]^=255;run(bytes(raw),cap)
    good=pack_surface(surface([229],4))
    for cap in (0,11,255):run(good,cap)
    for delta in range(-40,len(good)):run(good,4,target=src+delta)
    for a in range(4):
        for b in range(4):run(good,4,source=src+a,target=dst+b)
    run(good,4,target=0xFFFFFFF0)
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source_path=ROOT/profile['filename'];require_hash(source_path,profile['sha256']);original=source_path.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    play_hash='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(play,play_hash)
    if play.read_bytes()[0x32AC6:0x32AD8]!=original[0x32AC6:0x32AD8]:raise ValueError('raw normalizer changed')
    u.mem_map(0x08000000,len(original));u.mem_write(0x08000000,original);u.mem_protect(0x08000000,len(original),UC_PROT_READ|UC_PROT_EXEC)
    adverse=[]
    for word,identity,cut in [(229,'곥',2),(0x81E5,'structural E4/E5 token',1)]:
        raw=pack_surface(surface([word],1));run(raw,1)
        emitted=bytes(u.mem_read(dst,len(stream(raw,1))));before=bytearray(u.mem_read(0x02000000,8192))
        if call(0x08032AC6,[dst,0x02001801,0,0],0)!=cut:raise ValueError('native raw-copy cut')
        expected=emitted[:cut+1];before[0x1801:0x1801+len(expected)]=expected
        if bytes(u.mem_read(0x02000000,8192))!=bytes(before) or any(not(0x02001801<=a and a+n<=0x02001801+len(expected)) for a,n in writes):raise ValueError('native raw-copy write bound')
        adverse.append(dict(identity=identity,display_hex=emitted.hex(),raw_copy_hex=expected.hex(),returned_length=cut))
    report=dict(id='exe45.hangul-keyboard.record-display.v1',passed=True,rom_integrated=False,
                caller_selected_new_format_required=True,format_adopted=False,helper_bytes=len(blob),own_stack_bytes=44,nested_stack_bytes=80,
                counts=stats,ISA=isa,dependencies={'cpu_mixed_record':sha(dep.read_bytes())},
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_mixed_record_display.py','bench_hangul_mixed_record_display.py')},
                artifacts={'helper.bin':sha(blob)},
                limits=['Actual CPU encoder->record display consumes11172 full-cap10 final syllables without HOST rewrite, not game confirmation or native dialogue provider.',
                        'Direct fixed-record expansion requires no transition table or compact history. All structural fields validated before external output.',
                        'Caller selects new format and owns disjoint source/output/stack extents. No original descriptor/normalize replacement, buffer ownership, screen or save/fresh-load proof.'])
    report.update(source_sha256=profile['sha256'],current_rom_sha256=play_hash,
                  original_normalizer_sha256=sha(original[0x32AC6:0x32AD8]),
                  raw_normalizer_counterexamples=adverse)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS selected record -> display',len(blob),stats,flush=True)

if __name__=='__main__':main()
