"""Native finite chip lookup->stats writer->F90C, source/actual029 CPU.

Controlled valid native history. No helper/BIOS replacement or ROM writes.
Not natural multiplayer/battle history, Korean chip names or persistence.
"""
import struct,hashlib
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from inspect_profile_chip_pools_030 import OUT as CENSUS
ROM='poc/output/pending500_030_v1.gba'
ROM_SHA=read((ROOT/ROM).with_suffix('.json'))['output_sha256']

OUT='analysis/pending500_030_v1/chip_cpu.json'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/ROM,ROM_SHA);rom=(ROOT/ROM).read_bytes();c=read(CENSUS)
    for p,h in c['dependencies'].items():require_hash(ROOT/p,h)
    if c['source_sha256']!=sha(source) or c['baseline_sha256']!='a089f2e0abd7fa2fc9af25549dbce6737f37487fc5a304434c5893b05dce4ff5' or c['name_count']!=393 or c['maximum_advance']!=88:raise ValueError('030 finite pool identity')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x3864C,0x3866A),(0x387FE,0x388D0),(0x389D8,0x38A0C),(0x28722,0x2873C),(0x32AC6,0x32AD8),(0x94C,0x956),(0x517D0,0x5181C)]
    data=[(0x3866C,12),(0x38A0C,0x88),(0x526D0,31*8),(0x3B0D0+21*16,5*16),(0x5181C,4),(0x518F8,4)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in code:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('030 complete code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('030 ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in data:ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    for r in ranges:
        a,n=r['offset'],r['bytes']
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('030 native path source/product drift')
    stop,stack,glob,flags,ctx,stream=0x080000C0,0x03007F00,0x02000100,0x02002000,0x0200FA20,0x02020000
    reports=[];reference={};count=0
    for label,image in [('source',source),('030',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_write(glob+0x48,struct.pack('<I',flags));writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append((a,n)))
        def run(entry,regs,allowed):
            values=[0x1000+i*0x101 for i in range(15)];values[10]=glob;values[13]=stack;values[14]=stop|1
            for k,v in regs.items():values[k]=v
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.mem_write(stack-256,b'\xA7'*256);u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(entry|1,0,count=10000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack:raise ValueError('030 native return/stack')
            if any(not(stack-128<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('030 unexpected write '+str(writes))
            if bytes(u.mem_read(stack-256,128))!=b'\xA7'*128:raise ValueError('030 stack canary')
            if any(u.reg_read(REGS[i])!=values[i] for i in (5,6,7,8,9,10,11,12)):raise ValueError('030 preserved registers')
        for name,f in c['fields'].items():
            digest=hashlib.sha256()
            for record in c['names']:
                encoded=bytes.fromhex(record['raw_hex']);field,size=f['field'],f['bytes'];hist=f['history'];flag_at=flags+f['flag']//8;flag_mask=0x80>>(f['flag']%8)
                u.mem_write(hist-4,bytes(136));u.mem_write(field-2,b'\xA6'*(size+4));u.mem_write(flags,bytes(0x1000))
                run(0x0803864C,{0:record['chip_id']},[]);ptr=u.reg_read(REGS[0])
                if ptr!=0x08000000+record['source_offset'] or bytes(u.mem_read(ptr,len(encoded)))!=encoded:raise ValueError('030 actual native lookup')
                if f['category'] in (5,8,9):
                    run(0x080387FE,{0:f['category'],1:ptr},[(hist,hist+128),(field-1,field+size),(flag_at,flag_at+1)])
                else:
                    # Native valid pre-ranked history slot, copied from the
                    # exact lookup result; not a fabricated encoded name.
                    rank=f['category']-5;at=hist+32*rank
                    u.mem_write(at,struct.pack('<I',1));u.mem_write(at+4,encoded)
                    run(0x080389D8,{0:f['category'],1:rank,2:0},[(field-1,field+size),(flag_at,flag_at+1)])
                expected=encoded+b'\xA6'*(size-len(encoded))
                if bytes(u.mem_read(field,size))!=expected or bytes(u.mem_read(field-1,1))!=b'\x01' or u.mem_read(flag_at,1)[0]!=flag_mask:raise ValueError('030 native stats record/flag')
                if bytes(u.mem_read(field-2,1))+bytes(u.mem_read(field+size,2))!=b'\xA6'*3:raise ValueError('030 stats canary')
                u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xF9,12,f['index']]));u.mem_write(0x02010ABC,b'\xA6'*(size+8))
                run(0x080517D0,{4:stream,5:ctx},[(ctx,ctx+216),(0x02010AC0,0x02010AC0+size)])
                actual=bytes(u.mem_read(0x02010AC0,size));state=bytes(u.mem_read(ctx,216))
                if actual!=expected or u.reg_read(REGS[4])!=0x02010AC0 or state[5]!=1 or struct.unpack_from('<I',state,0x44)[0]!=stream+3:raise ValueError('030 actual F90C continuation/effects')
                if bytes(u.mem_read(0x02010ABC,4))+bytes(u.mem_read(0x02010AC0+size,4))!=b'\xA6'*8:raise ValueError('030 reader canary')
                digest.update(struct.pack('<I',record['chip_id'])+actual+state);count+=1
            key=name;value=digest.hexdigest()
            if label=='source':reference[key]=value
            elif reference[key]!=value:raise ValueError('030 source/product chain effects differ')
            reports.append(dict(image=label,provider=name,cases=393,effects_sha256=value));print(label,name,393,'PASS',flush=True)
        run(0x0803864C,{0:65535},[])
        if u.reg_read(REGS[0])!=0:raise ValueError('030 native sentinel')
        count+=1
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=ROM,baseline_sha256=sha(rom),tool_sha256=sha((ROOT/'tools/bench_profile_chips_product_030.py').read_bytes()),census=dict(path=CENSUS,sha256=sha((ROOT/CENSUS).read_bytes())),native_ranges=ranges,fields=c['fields'],case_count=count,results=reports,native_helpers_substituted=[],modeled_services=[],rom_written=False,product_admitted=False,release_eligible=False,limits=['Controlled native393 name lookup, stats promotion/update and F90C with exact source/product effects. Standard2/3 consume pre-ranked valid native history slots; other3 run the real frequency updater/sorter.','Not natural battle history/acquisition, arbitrary corrupt/imported records, GBA presentation, Korean chip-name values, Hangul records or save/reset/reload.','Source shared chip-name pools and this consumer stay Japanese; Korean private library/battle clones are not silently used.']))
    print('PASS030 native chip stats CPU',count,'NO ROM written')

if __name__=='__main__':main()
