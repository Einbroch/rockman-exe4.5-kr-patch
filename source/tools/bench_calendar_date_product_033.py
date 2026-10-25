"""Native event date producers, formatter and weekday F90C on source/031.

Controlled valid legacy date domains only; no ROM writes or title admission.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T

BASE='poc/output/pending500_033_v1.gba'
OUT='analysis/pending500_033_v1/date_cpu.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256']);rom=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in [(0x340AA,0x340F4),(0x32AA8,0x32AD8),(0x51E5C,0x51E72),(0x516AC,0x516F8),(0x52150,0x521D0),(0xA0C,0xA3A),(0xA68,0xA7E),(0x517D0,0x5181C),(0x94C,0x956)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('032 date bounded native code')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('032 date ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in [(0x34134,12),(0x51E74,4),(0x5258C+37*4,6*4),(0x526D0+67*8,8),(0x5181C,4),(0x518F8,4),(0x51594,4),(0x516F8,4),(0xA3C,44)]:
        if rom[a:a+n]!=source[a:a+n]:raise ValueError('032 date native literal/dispatch')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    if [struct.unpack_from('<I',source,0x5258C+x*4)[0] for x in (37,38,39,42)]!=[0x080340AB,0x080340B3,0x080340BB,0x080340E1]:raise ValueError('032 date dispatch identity')
    stop,stack,ctx,stream,record,buffer=0x080000C0,0x03007F00,0x0200FA20,0x02020000,0x02001310,0x02014E54;cases=[];bodies=[];reference={}
    for label,image in [('source',source),('031',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def run(entry,allowed):
            before=[0x1000+i*0x101 for i in range(15)];before[4]=stream;before[5]=ctx;before[13]=stack;before[14]=stop|1;u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
            for r,v in zip(REGS,before):u.reg_write(r,v)
            u.mem_write(stack-256,b'\xA7'*256);writes.clear();u.emu_start(entry|1,0,count=5000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack or bytes(u.mem_read(stack-256,128))!=b'\xA7'*128:raise ValueError('032 date return/stack canary')
            if any(not(stack-128<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('032 date allowed writes')
            return tuple(u.reg_read(r) for r in REGS),u.reg_read(UC_ARM_REG_CPSR)
        for kind,command,field,values,flag in [('year',37,2,range(100),0xC2),('month',38,3,range(1,13),0x82),('day',39,4,range(1,32),0x82)]:
            for value in values:
                for slot in range(5):
                    rec=bytearray(32);rec[field]=value;u.mem_write(record,bytes(rec));u.mem_write(0x02014DFC,struct.pack('<I',record));u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xFC,3,command,0]));run(0x08051E5C,[(ctx+0x4C,ctx+0x50)])
                    if struct.unpack('<I',u.mem_read(ctx+0x4C,4))[0]!=value or bytes(u.mem_read(record,32))!=bytes(rec):raise ValueError('032 event date producer')
                    scratch=0x02010AC0+slot*128;u.mem_write(ctx+0x64,struct.pack('<H',slot));u.mem_write(scratch-4,b'\xA6'*13);u.mem_write(stream,bytes([0xF9,3,flag,1]));effect=run(0x080516AC,[(ctx,ctx+216),(scratch,scratch+5)])
                    text=f'{value:02}' if kind=='year' else f'{value:2}';expected=bytes(0 if ch==' ' else int(ch)+1 for ch in text)+b'\xE5\0\0';state=bytes(u.mem_read(ctx,216));around=bytes(u.mem_read(scratch-4,13))
                    if around!=b'\xA6'*4+expected+b'\xA6'*4 or effect[0][4]!=scratch or struct.unpack_from('<I',state,0x44)[0]!=stream+4 or struct.unpack_from('<H',state,0x64)[0]!=slot+1:raise ValueError('032 date numeric body/canary/continuation')
                    key=(kind,value,slot);full=(effect,state,around)
                    if label=='source':reference[key]=full
                    elif full!=reference[key]:raise ValueError('032 date source/current full numeric effects')
                    cases.append(dict(image=label,kind=kind,value=value,slot=slot,raw_hex=expected.hex(),maximum_width=22))
        pool=struct.unpack_from('<I',image,0x32AD8)[0]
        for weekday in range(7):
            script=112+weekday;at=pool+struct.unpack_from('<H',image,pool-0x08000000+script*2)[0];off=at-0x08000000;end=image.index(b'\xE5',off,off+32)+1;body=image[off:end];pos=0;width=0;glyphs=[]
            while pos<len(body)-1:
                index=body[pos];pos+=1
                if index==0xE4:index=228+body[pos];pos+=1
                elif index>=0xE5:raise ValueError('032 weekday unmodeled command')
                width+=struct.unpack_from('<I',image,(0x5290C if label=='source' else m['extension']['advance_offset'])+index*4)[0];glyphs.append(index)
            if pos!=len(body)-1 or width>11:raise ValueError('032 weekday native single glyph bound')
            bodies.append(dict(image=label,weekday=weekday,script=script,raw_hex=body.hex(),width=width,glyphs=glyphs))
            for slot in range(5):
                rec=bytes(5)+bytes([weekday])+bytes(26);u.mem_write(record,rec);u.mem_write(0x02014DFC,struct.pack('<I',record));u.mem_write(ctx,bytes(216));u.mem_write(buffer-4,b'\xA6'*40);u.mem_write(stream,bytes([0xFC,3,42,0]));run(0x08051E5C,[(buffer,buffer+32)])
                if bytes(u.mem_read(buffer-4,40))!=b'\xA6'*4+body+b'\xA6'*(36-len(body)):raise ValueError('032 weekday producer and canaries')
                scratch=0x02010AC0+slot*128;u.mem_write(scratch-4,b'\xA6'*40);u.mem_write(ctx+0x64,struct.pack('<H',slot));u.mem_write(stream,bytes([0xF9,12,67]));run(0x080517D0,[(ctx,ctx+216),(scratch,scratch+32)])
                if bytes(u.mem_read(scratch-4,40))!=b'\xA6'*4+body+b'\xA6'*(36-len(body)) or bytes(u.mem_read(record,32))!=rec:raise ValueError('032 weekday F90C/residency/record')
                cases.append(dict(image=label,kind='weekday',value=weekday,slot=slot,raw_hex=body.hex(),width=width))
    deps=['tools/bench_calendar_date_product_033.py'];frozen_write(ROOT/OUT,dict(schema=1,passed=True,baseline_rom=BASE,baseline_sha256=sha(rom),source_sha256=sha(source),case_count=len(cases),cases=cases,weekday_bodies=bodies,native_ranges=ranges,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_helpers_substituted=[],modeled_services=[],rom_written=False,release_eligible=False,limits=['Controlled year00..99/month1..12/day1..31/weekday0..6 only, five slots each, not real RTC origin, leap-year/calendar validation, corrupt/imported state or all dates.','Shared weekday pools remain native Japanese single glyphs.','No annotation/title producer or GBA/choice/save proof and no new translations applied.']))
    print('032 date native producer/formatter/weekday PASS',len(cases),'source/current cases; no ROM')


if __name__=='__main__':main()
