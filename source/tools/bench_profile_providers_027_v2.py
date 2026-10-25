"""Source/026 profile cap-load, native editor boundary, commit and F90C read.

Controlled valid legacy editor fixtures, not natural caller/save evidence.
Only fixed CpuSet clear and sound services are modeled; native parameter
window, initializer, input handler, flatten, commit, copy and reader execute.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from profile_provider_bounds_027 import bounds,FIELDS
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_INTR,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import *

OUT='analysis/pending_insertion_500_027_profile_cpu_v2/cpu.json'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/'poc/output/pending500_026_v1.gba';require_hash(rp,'bf66382b7897f1313a9dba55333512e46f46e5e036a6905d049693ac0af80adf');rom=rp.read_bytes();limits=bounds(source,rom)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x38D9C,0x38DA6),(0x355B6,0x355F6),(0x90C,0x926),(0xEC144,0xEC148),(0x353B0,0x35582),(0x35620,0x3564E),(0x35000,0x35032),(0x32AC6,0x32AD8),(0x517D0,0x5181C),(0x94C,0x956)]
    data=[(0x38DE4,16),(0x3B0D0,16*16),(0x526D0,28*8),(0x5290C,441*4),(0x3574C,4),(0x35034,4),(0x5181C,4),(0x518F8,4),(0x928,4)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in code:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('027 native source/026 code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('027 bounded ARMv4T roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in data:
        if rom[a:a+n]!=source[a:a+n]:raise ValueError('027 native source/026 data identity')
        regions.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    # The registered common UI archive is relocated in026. Validate the
    # consumer's actual three token pages, not an obsolete absolute address.
    meta=read(rp.with_suffix('.json'));ar=next(r for r in meta['archives'] if r['archive']=='6368E8')
    old_base=struct.unpack_from('<I',source,0x35748)[0]-0x08000000
    new_base=struct.unpack_from('<I',rom,0x35748)[0]-0x08000000
    if old_base!=0x6368E8 or new_base!=ar['rom_offset'] or 0x35748 not in ar['pointers']:raise ValueError('027 registered selector relocation')
    covering=[w for w in meta['expected_writes'] if w['offset']<=0x35748 and 0x3574C<=w['offset']+w['bytes']]
    if len(covering)!=1:raise ValueError('027 selector expected writer')
    w=covering[0];delta=0x35748-w['offset']
    if bytes.fromhex(w['expected_hex'])[delta:delta+4]!=source[0x35748:0x3574C] or bytes.fromhex(w['final_hex'])[delta:delta+4]!=rom[0x35748:0x3574C]:raise ValueError('027 selector expected bytes')
    selector_pages=[]
    for page in range(3):
        contents=[]
        for data_image,base in ((source,old_base),(rom,new_base)):
            a=base+struct.unpack_from('<H',data_image,base+4+2*page)[0];pos=a;tokens=[]
            while data_image[pos]!=0xE5:
                n=2 if data_image[pos]==0xE4 else 1
                tokens.append(data_image[pos:pos+n]);pos+=n
                if len(tokens)>105:raise ValueError('027 bounded native selector population')
            contents.append((tokens,data_image[a:pos+1],a))
        if contents[0][0]!=contents[1][0]:raise ValueError('027 relocated selector semantics changed')
        selector_pages.append(dict(page=page,cells=len(contents[0][0]),source_offset=contents[0][2],current_offset=contents[1][2],sha256=sha(contents[0][1])))
    editor,ctx,stream,stack,stop=0x0200FC40,0x0200FA20,0x02020000,0x03007F00,0x080000C0
    params,glob,keys,ui=0x02020100,0x02000100,0x02000200,0x0200F550;cases=[];references={};service_counts=dict(CpuSet=0,sound=0)
    for image_name,image in [('source',source),('026',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        writes=[];allowed=[];sounds=[]
        def hook(uc,a,n,d):
            if a in (stop,0x08038DA6):uc.emu_stop()
            elif a==0x08000534:
                sounds.append(uc.reg_read(REGS[0]));service_counts['sound']+=1;uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
        def interrupt(uc,number,d):
            if number!=2 or uc.reg_read(UC_ARM_REG_PC)!=0x080EC146 or uc.reg_read(REGS[1])!=editor or uc.reg_read(REGS[2])!=0x05000018 or bytes(uc.mem_read(uc.reg_read(REGS[0]),4))!=bytes(4):raise ValueError('027 unexpected BIOS interrupt')
            uc.mem_write(editor,bytes(96));service_counts['CpuSet']+=1
        u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_INTR,interrupt)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append((a,n)))
        def run(entry,registers,write_ranges,expected_stop=stop):
            u.mem_write(stack-128,b'\xA7'*128);values=[0x1000+i*0x101 for i in range(15)];values[13]=stack;values[14]=stop|1
            for k,v in registers.items():values[k]=v
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();sounds.clear();u.emu_start(entry|1,0,count=20000)
            if u.reg_read(UC_ARM_REG_PC)!=expected_stop or u.reg_read(REGS[13])!=stack:raise ValueError('027 native return/stack')
            if any(not(any(lo<=a and a+n<=hi for lo,hi in write_ranges) or stack-64<=a and a+n<=stack) for a,n in writes):raise ValueError('027 write outside declared fixture')
            if bytes(u.mem_read(stack-128,64))!=b'\xA7'*64:raise ValueError('027 stack canary')
        def init(name):
            info=limits[name];u.mem_write(editor-4,b'\xA6'*104);u.mem_write(params,bytes(12));u.mem_write(params+4,struct.pack('<I',info['source_field']-1))
            run(0x08038D9C,{6:0x0803B0D0+info['profile_index']*16,7:params},[(editor,editor+96)],0x08038DA6)
            e=bytes(u.mem_read(editor-4,104))
            if e[:4]!=b'\xA6'*4 or e[-4:]!=b'\xA6'*4 or e[8]!=info['logical_cap'] or struct.unpack_from('<I',e,32)[0]!=info['source_field']-1:raise ValueError('027 actual table->editor cap/destination')
            return info
        for name in FIELDS:
            info=limits[name];cap=info['logical_cap'];field=info['source_field'];size=info['descriptor_bytes']
            for token in (b'\x9B',b'\xE4\x06'):
                word=token+b'\x00' if len(token)==1 else token
                for count in range(cap+1):
                    init(name);buffer=editor+32;u.mem_write(buffer,word*count+b'\xE5\x00');u.mem_write(editor+20,struct.pack('<II',buffer+2*count,buffer+2*count))
                    encoded=token*count+b'\xE5';u.mem_write(field-2,b'\xA6'*(size+4));u.mem_write(editor+64,b'\xA7'*32)
                    run(0x0803562C,{},[(editor+64,editor+96)])
                    if bytes(u.mem_read(editor+64,len(encoded)))!=encoded:raise ValueError('027 native flatten')
                    run(0x08035000,{},[(field-1,field-1+size+1),(0x02014E74,0x02014E74+size)])
                    if bytes(u.mem_read(field-1,len(encoded)+1))!=b'\x01'+encoded or bytes(u.mem_read(field-2,1))!=b'\xA6' or bytes(u.mem_read(field+size,2))!=b'\xA6'*2:raise ValueError('027 native commit record/canaries')
                    before=bytes(u.mem_read(field,size));u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xF9,12,info['descriptor_index']]));u.mem_write(0x02010ABC,b'\xA6'*136)
                    run(0x080517D0,{4:stream,5:ctx},[(ctx,ctx+216),(0x02010AC0,0x02010AC0+size)])
                    after=bytes(u.mem_read(ctx,216));copied=bytes(u.mem_read(0x02010AC0,size))
                    if copied!=before or u.reg_read(REGS[4])!=0x02010AC0 or after[5]!=1 or struct.unpack_from('<I',after,0x44)[0]!=stream+3 or bytes(u.mem_read(0x02010ABC,4))!=b'\xA6'*4 or bytes(u.mem_read(0x02010AC0+size,4))!=b'\xA6'*4:raise ValueError('027 F90C native reader chain')
                    key=(name,token.hex(),count);result=(copied,after)
                    if image_name=='source':references[key]=result
                    elif references[key]!=result:raise ValueError('027 source/026 chain differs')
                    cases.append(dict(image=image_name,kind='cap-load-flatten-commit-reader',provider=name,logical_cap=cap,count=count,token=token.hex()))
            for count in (0,cap-1,cap):
                init(name);buffer=editor+32;u.mem_write(buffer,b'\x9B\x00'*count+b'\xE5\x00');u.mem_write(editor+20,struct.pack('<II',buffer+2*count,buffer+2*count));u.mem_write(glob+4,struct.pack('<I',keys));u.mem_write(keys+2,b'\x01\x00');u.mem_write(ui,bytes(32));before=bytes(u.mem_read(editor,96))
                run(0x080353B0,{5:ui,10:glob},[(editor,editor+96)])
                after=bytes(u.mem_read(editor,96));end=struct.unpack_from('<I',after,24)[0]
                if count==cap:
                    if after!=before or sounds:raise ValueError('027 extra glyph at full cap accepted')
                elif end!=buffer+(count+1)*2 or sounds!=[126]:raise ValueError('027 normal input cap boundary')
                cases.append(dict(image=image_name,kind='actual-A-input-boundary',provider=name,count=count,accepted=count<cap))
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),tool_sha256=sha((ROOT/'tools/bench_profile_providers_027_v2.py').read_bytes()),provider_bounds=limits,selector_relocation=selector_pages,native_ranges=regions,cases=cases,case_count=len(cases),modeled_services=service_counts,native_helpers_substituted=[],rom_written=False,release_eligible=False,limits='Controlled valid native legacy state, source/026 direct single fields only. Real native cap-load/initializer/input/flatten/commit/copy/F90C reader; fixed CpuSet clear and sound services modeled. Not whole BIOS, natural caller or complete writer/default/import audit, save/reset/fresh reload, array-backed providers, malformed save safety, full input repertoire or Hangul name support. Width bound is logical source profile cap times maximum441 source metric11, not descriptor-byte count.'))
    print('PASS027 direct profile CPU',len(cases),'fixtures',service_counts,'NO ROM written')

if __name__=='__main__':main()
