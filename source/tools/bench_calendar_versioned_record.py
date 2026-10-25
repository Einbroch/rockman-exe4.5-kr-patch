"""Conditional F8 storage writer/reader ABI, not whole-save compatibility."""
import json,struct
from bench_hangul_composer_thumb import *
from hangul_calendar_versioned_record import assemble_writer,assemble_reader,pack,read
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE


def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={}
    for name in ('cpu_calendar_title_record','cpu_record_display'):
        p=base/name/'report.json';d=json.loads(p.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']:raise ValueError('dependency scope')
        for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in d['artifacts'].items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes())
    observed=json.loads((base/'calendar_name_lifetime.json').read_text(encoding='utf8'))
    deps['calendar_name_lifetime.json']=sha((base/'calendar_name_lifetime.json').read_bytes())
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256'])
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,observed['current_rom_sha256'])
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08300000,0x10000);u.mem_map(0x08F09000,4096)
    blobs={};isas={}
    for n,a,make in (('writer.bin',0x0830D000,assemble_writer),('reader.bin',0x0830D200,assemble_reader)):
        blob,isa=make();blobs[n]=blob;isas[n]=isa;u.mem_write(a,blob)
    u.mem_write(0x08309000,(base/'cpu_calendar_title_record/converter.bin').read_bytes())
    u.mem_write(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes())
    u.mem_protect(0x08300000,0x10000,UC_PROT_READ|UC_PROT_EXEC);u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    title,record,display=0x02000100,0x02000200,0x02000300
    sp,stop=0x03007EFC,0x0FF00000;writes=[]
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(writes=0,reads=0,accepted_reads=0,rejected_reads=0,syllable_roundtrips=0,word_domain=0,legacy_E4_payloads=0,collision_controls=0,whole_EWRAM_checks=0,bounds_rejections=0)
    u.hook_add(UC_HOOK_CODE,lambda cpu,a,n,user:cpu.emu_stop() if a==stop else None)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def cpu(start,args,stack):
        u.mem_write(sp-128,b'\x5A'*128);u.reg_write(UC_ARM_REG_CPSR,0x30)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
        u.emu_start(start|1,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('ABI')
        if bytes(u.mem_read(sp-128,128-stack))!=b'\x5A'*(128-stack):raise ValueError('stack bound')
        return u.reg_read(UC_ARM_REG_R0)
    def check(expected,dest,length,stack):
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM isolation')
        if any(not(sp-stack<=a and a+n<=sp) and not(dest<=a and a+n<=dest+length) for a,n in writes):raise ValueError('unexpected write')
        counts['whole_EWRAM_checks']+=1
    def decode(raw,want=None,available=22,out_available=41,dest=display,cap=10,expected_valid=None):
        u.mem_write(record,raw)
        before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before)
        if expected_valid is None:
            try:want=read(raw);valid=available>=22 and len(want)<=out_available and cap==10 and not(record<dest+out_available and dest<record+22)
            except ValueError:valid=False
        else:valid=expected_valid
        if valid:expected[dest-0x02000000:dest-0x02000000+len(want)]=want
        result=cpu(0x0830D200,(record,dest,out_available<<16|available,cap),124)
        if result!=(len(want) if valid else 0):raise ValueError(f'reader result {raw.hex()}')
        check(expected,dest,len(want) if valid else 0,124);counts['reads']+=1;counts['accepted_reads' if valid else 'rejected_reads']+=1
    u.mem_write(0x02000000,b'\xA7'*0x40000)
    for rank in range(11172):
        raw=b'\xF9\xFC'+struct.pack('<H',rank);stream=raw*10+b'\xE5';u.mem_write(title,stream)
        expected=bytearray(u.mem_read(0x02000000,0x40000));want=b'\xF8'+struct.pack('<H',rank)*10+b'\xE5'
        expected[record-0x02000000:record-0x02000000+22]=want
        if cpu(0x0830D000,(title,record,22<<16|41,10),88)!=22:raise ValueError('writer result')
        check(expected,record,22,88);counts['writes']+=1
        # Reader directly consumes CPU writer bytes; no HOST record rewrite.
        expected=bytearray(u.mem_read(0x02000000,0x40000));expected[display-0x02000000:display-0x02000000+41]=stream
        if cpu(0x0830D200,(record,display,41<<16|22,10),124)!=41:raise ValueError('writer/reader roundtrip')
        check(expected,display,41,124);counts['reads']+=1;counts['accepted_reads']+=1;counts['syllable_roundtrips']+=1
        if rank%2048==0:print('versioned roundtrip rank',rank,flush=True)
    for word in range(65536):
        raw=b'\xF8'+struct.pack('<H',word)+b'\xFF\xFF'*9+b'\xE5'
        valid=word<11172 or 0x8000<=word<=0x80E3 or 0x8100<=word<=0x81FF
        want=(b'\xF9\xFC'+struct.pack('<H',word) if word<11172 else bytes([word&255]) if word<=0x80E3 else b'\xE4'+bytes([word&255]))+b'\xE5' if valid else None
        decode(raw,want=want,expected_valid=valid);counts['word_domain']+=1
        if word%16384==0:print('versioned identity domain',word,flush=True)
    for b in range(228):decode(bytes([b,0xE5])+b'\xA7'*20)
    for b in range(256):decode(bytes([0xE4,b,0xE5])+b'\xA7'*19);counts['legacy_E4_payloads']+=1
    for rank in range(11172):decode(b'\xF9\xFC'+struct.pack('<H',rank)+b'\xE5'+b'\xA7'*17)
    for count in range(1,11):
        tagged=b'\xF8'+struct.pack('<H',229)*count+b'\xFF\xFF'*(10-count)+b'\xE5'
        internal=bytes([128+count])+tagged[1:]
        decode(tagged,want=b'\xF9\xFC\xE5\x00'*count+b'\xE5',expected_valid=True)
        decode(internal,want=bytes([128+count,0xE5]),expected_valid=True)
        counts['collision_controls']+=1
    good=b'\xF8'+struct.pack('<H',229)+b'\xFF\xFF'*9+b'\xE5'
    for at in range(22):
        raw=bytearray(good);raw[at]^=255;decode(bytes(raw))
    for count in range(1,11):
        raw=b'\xF8'+b'\xFF\xFF'*count+struct.pack('<H',1)*(10-count)+b'\xE5';decode(raw,expected_valid=False)
    for first in range(0xE5,256):
        if first not in (0xF8,0xF9):decode(bytes([first,0xE5])+b'\xA7'*20)
    for avail in range(22):decode(good,available=avail)
    for out in range(5):decode(good,out_available=out)
    for dest in (record-1,record,record+1):decode(good,dest=dest)
    for cap in (0,6,11):decode(good,cap=cap)
    for args in ((0xFFFFFFF0,display,41<<16|22,10),(record,0xFFFFFFF0,41<<16|22,10)):
        before=bytes(u.mem_read(0x02000000,0x40000))
        if cpu(0x0830D200,args,124)!=0:raise ValueError('reader wrap')
        check(before,display,0,124);counts['bounds_rejections']+=1
    for args in ((title,record,21<<16|41,10),(title,title,22<<16|41,10),(0xFFFFFFF0,record,22<<16|41,10),(title,0xFFFFFFF0,22<<16|41,10),(title,record,22<<16|42,10),(title,record,22<<16|41,6)):
        before=bytes(u.mem_read(0x02000000,0x40000))
        if cpu(0x0830D000,args,88)!=0:raise ValueError('writer boundary rejection')
        check(before,record,0,88);counts['bounds_rejections']+=1
    # Exact old runtime titles; observed fields are legacy, not retroactively
    # interpreted as unversioned binary candidates.
    for name in ('default_meal','friend'):
        raw=bytes.fromhex(observed[name]['registered_RAM_record_hex'])[10:];decode(raw)
    out=base/'cpu_calendar_versioned_record';out.mkdir(exist_ok=True)
    for n,b in blobs.items():(out/n).write_bytes(b)
    result=dict(id='exe45.hangul-keyboard.versioned-calendar-record-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        current_rom_sha256=observed['current_rom_sha256'],source_sha256=profile['sha256'],counts=counts,
        dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_calendar_versioned_record.py','bench_calendar_versioned_record.py')},
        artifacts={n:sha(b) for n,b in blobs.items()},ISA=isas,version_byte=248,record_bytes=22,writer_stack_bytes=88,reader_stack_bytes=124,
        no_HOST_record_rewrite_between_CPU_writer_and_reader=True,
        legacy_domain='Nonempty <=10 logical cells in field22:00..E3, E4+any payload, F9FC+complete rank0..11171, E5 terminator. FirstF8 is not in this declared grammar.',
        limits=['Conditional domain-disjoint tag candidate only. This grammar is NOT established as every original/default/import calendar writer. F8 reservation and whole old-save compatibility NOT adopted.',
                'Internal81..8A count-marker records remain internal and are NOT accepted as persisted NEW records. Their collision prefixes must decode as legacy bytes, not Hangul ranks.',
                'CPU helper ABI only; native commit/readers and versioned field32 record integration not yet connected. No source/playable/save writes, actual screen, save/reset/freshload or release claim.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,observed['current_rom_sha256'])
    print('PASS conditional versioned writer/reader CPU; format NOT adopted',counts,flush=True)


if __name__=='__main__':main()
