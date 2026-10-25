"""Unchanged calendar FC03 producers -> descriptor67 -> native F90C.

Controlled CPU fixtures, NOT calendar acquisition, GBA pixels or save proof.
No native helper, copy routine or BIOS service is substituted.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from korean_codec import encode_hangul

BASE='poc/output/pending500_032_v1.gba'
OUT='analysis/pending500_032_v1/event_cpu.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    meta=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,meta['output_sha256']);rom=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in [(0x340C2,0x340E0),(0x340F4,0x3410E),(0x34122,0x34132),(0x32AA8,0x32AD8),(0x51E5C,0x51E72),(0x517D0,0x5181C),(0x94C,0x956)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('event complete code boundary')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('event ARMv4T roundtrip')
        if rom[a:b]!=raw:raise ValueError('event source/030 code drift')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    for a,n in [(0x34134,12),(0x51E74,4),(0x5258C+40*4,6*4),(0x526D0+67*8,8),(0x5181C,4),(0x518F8,4)]:
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('event source/030 data drift')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n])))
    if struct.unpack_from('<II',source,0x526D0+67*8)!=(0x02014E54,32):raise ValueError('descriptor67')
    if [struct.unpack_from('<I',source,0x5258C+4*x)[0] for x in (40,41,43,45)]!=[0x080340C3,0x080340D3,0x080340F5,0x08034123]:raise ValueError('FC03 dispatch identity')
    stop,stack,ctx,stream,record,buffer=0x080000C0,0x03007F00,0x0200FA20,0x02020000,0x02001310,0x02014E54
    cases=[];presets=[]
    for label,image in [('source',source),('030',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def run(entry,regs,allowed):
            before=[0x1000+i*0x101 for i in range(15)];before[13]=stack;before[14]=stop|1
            for k,v in regs.items():before[k]=v
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
            for r,v in zip(REGS,before):u.reg_write(r,v)
            u.mem_write(stack-256,b'\xA7'*256);writes.clear();u.emu_start(entry|1,0,count=2000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack:raise ValueError('event return/stack')
            if any(not(stack-128<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('event unexpected write '+str(writes))
            if bytes(u.mem_read(stack-256,128))!=b'\xA7'*128:raise ValueError('event stack canary')
            if any(u.reg_read(REGS[i])!=before[i] for i in (5,6,8,9,10,11,12)):raise ValueError('event preserved registers')
        def setup(command):
            u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xFC,3,command,0]));u.mem_write(0x02014DFC,struct.pack('<I',record))
        def producer(command):run(0x08051E5C,{4:stream,5:ctx},[(buffer,buffer+32),(0x0200FA6C,0x0200FA70)])
        def consume(body,slot):
            scratch=0x02010AC0+slot*128;u.mem_write(scratch-4,b'\xA6'*40);u.mem_write(stream+4,bytes([0xF9,12,67]));u.mem_write(ctx+100,struct.pack('<H',slot))
            run(0x080517D0,{4:stream+4,5:ctx},[(ctx,ctx+216),(scratch,scratch+32)])
            expected=body+b'\xA6'*(32-len(body))
            if bytes(u.mem_read(scratch,32))!=expected or bytes(u.mem_read(scratch-4,4))+bytes(u.mem_read(scratch+32,4))!=b'\xA6'*8:raise ValueError('event F90C bytes/canaries')
            state=bytes(u.mem_read(ctx,216))
            if u.reg_read(REGS[4])!=scratch or struct.unpack_from('<I',state,0x44)[0]!=stream+7 or state[5]!=1 or struct.unpack_from('<H',state,100)[0]!=slot+1:raise ValueError('event F90C continuation')
        names=[(f'native-{len(token)}byte-{n}',token*n+b'\xE5') for token in (b'\x9B',b'\xE4\x06') for n in range(11)]
        pool=struct.unpack_from('<I',image,0x32AD8)[0]
        for script in (62,63):
            at=pool+struct.unpack_from('<H',image,pool-0x08000000+2*script)[0];off=at-0x08000000;end=image.index(b'\xE5',off,off+22)+1;body=image[off:end]
            if label=='030' and body!=encode_hangul('식사' if script==62 else '학원')+b'\xE5':raise ValueError('actual030 preset drift')
            names.append((f'actual-preset-{script}',body));presets.append(dict(image=label,script=script,address=at,raw_hex=body.hex()))
        for name,body in names:
            if len(body)>22:raise ValueError('controlled name field size')
            for slot in (0,3):
                setup(45);original_record=bytes(range(10))+body+b'\xA4'*(22-len(body));u.mem_write(record,original_record);u.mem_write(buffer-4,b'\xA6'*40)
                producer(45)
                if bytes(u.mem_read(buffer,32))!=body+b'\xA6'*(32-len(body)) or bytes(u.mem_read(buffer-4,4))+bytes(u.mem_read(buffer+32,4))!=b'\xA6'*8 or bytes(u.mem_read(record,32))!=original_record or u.reg_read(REGS[4])!=stream+4:raise ValueError('event name producer/canary/record')
                consume(body,slot);cases.append(dict(image=label,kind='name',fixture=name,bytes=len(body),slot=slot))
        for hour in range(24):
            for minute in range(60):
                setup(40);u.mem_write(record,bytes([0]*6+[hour,minute]+[0]*24));producer(40)
                if struct.unpack('<I',u.mem_read(0x0200FA6C,4))[0]!=(hour-12 if hour>=13 else hour):raise ValueError('native12hour value')
                setup(41);producer(41)
                if struct.unpack('<I',u.mem_read(0x0200FA6C,4))[0]!=minute:raise ValueError('native minute value')
                cases.append(dict(image=label,kind='numeric',hour=hour,minute=minute))
        for hour in range(24):
            setup(43);u.mem_write(record,bytes([0]*6+[hour]+[0]*25));u.mem_write(buffer-4,b'\xA6'*40);producer(43)
            script=110 if hour<=12 else 111;at=pool+struct.unpack_from('<H',image,pool-0x08000000+script*2)[0];off=at-0x08000000;end=image.index(b'\xE5',off,off+32)+1;body=image[off:end]
            if bytes(u.mem_read(buffer,32))!=body+b'\xA6'*(32-len(body)):raise ValueError('native AMPM script lookup')
            consume(body,2);cases.append(dict(image=label,kind='AMPM',hour=hour,script=script,body_hex=body.hex()))
    result=dict(schema=1,passed=True,policy='controlled CPU; NON-DISTRIBUTION',release_eligible=False,rom_written=False,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),cases=len(cases),case_details=cases,native_ranges=ranges,presets=presets,descriptor=dict(index=67,address=buffer,copy_bytes=32),dependencies={'tools/bench_event_buffers_product_032.py':sha((ROOT/'tools/bench_event_buffers_product_032.py').read_bytes())},limits=['Names are controlled E5-terminated record fixtures, not all native producers or corrupted/imported records.','Two actual presets only; other preset/suffix-generated titles not bounded here.','Native hour13..23 subtract12; native AMPM uses hour>12. This records original behavior, not an approved time conversion.','No numeric printBuffer formatting, gameplay caller lifetime, GBA pixels, RTC, save or Hangul input/persistence proof.','No new literal units admitted or applied.'])
    frozen_write(ROOT/OUT,result);print('event producer/F90C CPU PASS',len(cases),'no ROM written',flush=True)


if __name__=='__main__':main()
