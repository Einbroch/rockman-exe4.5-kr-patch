"""Controlled native FC0F array selection -> cache -> F90C, source/028.

No ROM writes, helper replacement, natural caller, editor, or persistence claim.
Only BIOS Div is modeled, with nonnegative native 16-bit random inputs.
"""
import hashlib
import struct
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

OUT = 'analysis/pending_insertion_500_029_array_cpu_v1/cpu.json'
ROM = 'poc/output/pending500_028_v1.gba'
ROM_SHA = '66d93c8f0142f2d5e5a48e112af995af5f40e7d031627b9c362878573a95f3ef'
NAMES = {1:'printOlderBro',2:'printYoungerBro',3:'printOlderSis',4:'printYoungerSis',5:'printFriend',7:'printHobby',12:'printFavShow',15:'printWish'}

def random_word(seed):
    return ((((seed<<1)&0xFFFFFFFF)+(seed>>31)+1)&0xFFFFFFFF)^0x873CA9E5

def main():
    cfg=read('project.json'); path=ROOT/cfg['source_profile']['filename']
    require_hash(path,cfg['source_profile']['sha256']); source=path.read_bytes()
    require_hash(ROOT/ROM,ROM_SHA); product=(ROOT/ROM).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x51C54,0x51C64),(0x51DD4,0x51DFA),(0x38A94,0x38A9E),(0x38B94,0x38C10),
          (0x287B2,0x287CA),(0x137C,0x1392),(0x32AC6,0x32AD8),(0x517D0,0x5181C),(0x94C,0x956)]
    data=[(0x500F4,4),(0x51C64,4),(0x51CA4,4),(0x38DE4,12),(0x1400,8),
          (0x3B0D0,256),(0x526D0,31*8),(0x5181C,4),(0x518F8,4)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB); ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB); ranges=[]
    for start,end in code:
        raw=source[start:end]; ins=list(cs.disasm(raw,0x08000000+start))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('Incomplete native code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('ARMv4T roundtrip')
        ranges.append(dict(offset=start,bytes=len(raw),sha256=sha(raw),kind='code'))
    for start,size in data:ranges.append(dict(offset=start,bytes=size,sha256=sha(source[start:start+size]),kind='data'))
    for item in ranges:
        a,n=item['offset'],item['bytes']
        if product[a:a+n]!=source[a:a+n]:raise ValueError('Source/product native range drift')
    def ptr(at):return struct.unpack_from('<I',source,at)[0]
    if (ptr(0x500F4),ptr(0x51C64),ptr(0x51CA4),ptr(0x1400))!=(0x08051C55,0x08051C68,0x08051DD5,0x02003F6C):raise ValueError('Native dispatch chain')
    fields=[]
    for row,name in NAMES.items():
        raw=source[0x3B0D0+16*row:0x3B0E0+16*row]; count,index,cap=raw[:3]
        cache,size=struct.unpack_from('<II',source,0x526D0+8*index)
        if count not in (3,4,8) or cap not in (6,8) or size!=2*cap+1:raise ValueError('Native array table shape')
        fields.append(dict(provider=name,row=row,count=count,index=index,cap=cap,cache=cache,size=size,
                           flag=struct.unpack_from('<H',raw,12)[0],base=0x02000950+struct.unpack_from('<H',raw,14)[0]))
    stop,stack,glob,flags,ctx,stream=0x080000C0,0x03007F00,0x02000100,0x02002000,0x0200FA20,0x02020000
    aggregate=[]; reference={}; total=0; div_calls=0
    for label,image in [('source',source),('028',product)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image)
        u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        u.mem_write(glob+0x48,struct.pack('<I',flags)); writes=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append((a,n)))
        def intr(uc,number,d):
            nonlocal div_calls
            if number!=2 or uc.reg_read(UC_ARM_REG_PC)!=0x08038BE4:raise ValueError('Unexpected BIOS service')
            a,b=uc.reg_read(REGS[0]),uc.reg_read(REGS[1])
            if not 0<=a<=65535 or not 1<=b<=8:raise ValueError('Div domain')
            uc.reg_write(REGS[0],a//b);uc.reg_write(REGS[1],a%b);uc.reg_write(REGS[3],a//b);div_calls+=1
        u.hook_add(UC_HOOK_INTR,intr)
        def run(entry,registers,allowed):
            values=[0x1000+i*0x101 for i in range(15)];values[13]=stack;values[14]=stop|1;values[10]=glob
            for k,v in registers.items():values[k]=v
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.mem_write(stack-160,b'\xA7'*160);u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear()
            u.emu_start(entry|1,0,count=6000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack:raise ValueError('Native return/stack')
            if any(not(stack-96<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('Unexpected native write '+str(writes))
            if bytes(u.mem_read(stack-160,64))!=b'\xA7'*64:raise ValueError('Stack canary')
            if any(u.reg_read(REGS[i])!=values[i] for i in (5,6,7,8,9,10,11,12)):raise ValueError('Preserved register drift')
        for f in fields:
            digest=hashlib.sha256(); cases=0; selection_coverage=set(); rejection_count=0
            count,cap,base,cache,size=f['count'],f['cap'],f['base'],f['cache'],f['size'];stride=2*cap+2
            enabled_address=flags+f['flag']//8;enabled_mask=0x80>>(f['flag']%8)
            for enabled in (False,True):
                u.mem_write(enabled_address,bytes([enabled_mask if enabled else 0]))
                for mask in range(1<<count):
                    active=[i for i in range(count) if mask>>i&1]
                    if not enabled or not active:
                        fixtures=[(0,0,b'\x9B')]
                    else:
                        seeds={}
                        for candidate in range(131072):
                            seed=(candidate//2)|(0x80000000 if candidate%2 else 0)
                            rem=(random_word(seed)&65535)%len(active)
                            seeds.setdefault(rem,seed)
                            if len(seeds)==len(active):break
                        if len(seeds)!=len(active):raise ValueError('Native RNG selection coverage')
                        fixtures=[(seed,n,t) for seed in seeds.values() for n in range(cap+1) for t in (b'\x9B',b'\xE4\x06')]
                    for seed,n,token in fixtures:
                        records=bytearray()
                        for i in range(count):
                            # Distinguish each selected record without exceeding n logical glyphs.
                            encoded=(bytes([0x9B+i])+token*(n-1) if n else b'')+b'\xE5'
                            records+=bytes([bool(mask>>i&1)])+encoded+b'\xA4'*(size-len(encoded))
                        u.mem_write(base,bytes(records));u.mem_write(cache-4,b'\xA6'*(size+8))
                        u.mem_write(0x02003F6C,struct.pack('<I',seed));u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xFC,0x0F,f['index'],255,255]))
                        run(0x08051C54,{4:stream,5:ctx},[(cache,cache+size),(0x02003F6C,0x02003F70)])
                        actual=bytes(u.mem_read(cache,size)); success=enabled and bool(active)
                        if success:
                            selected=active[(random_word(seed)&65535)%len(active)]
                            encoded=bytes(records[selected*stride+1:(selected+1)*stride]).split(b'\xE5',1)[0]+b'\xE5'
                            wanted=encoded+b'\xA6'*(size-len(encoded));selection_coverage.add((mask,selected));advance=n*11
                            if advance>cap*11:raise ValueError('Logical glyph bound')
                        else:wanted=b'\xA6'*size;rejection_count+=1
                        if actual!=wanted or u.reg_read(REGS[4])!=stream+5 or u.reg_read(REGS[0])!=1:raise ValueError('FC0F selection/cache/continue')
                        if bytes(u.mem_read(base,len(records)))!=records or bytes(u.mem_read(cache-4,4))+bytes(u.mem_read(cache+size,4))!=b'\xA6'*8:raise ValueError('Record/canary changed')
                        if success:
                            u.mem_write(stream,bytes([0xF9,12,f['index']]));u.mem_write(0x02010ABC,b'\xA6'*(size+8))
                            run(0x080517D0,{4:stream,5:ctx},[(ctx,ctx+216),(0x02010AC0,0x02010AC0+size)])
                            c=bytes(u.mem_read(ctx,216));copied=bytes(u.mem_read(0x02010AC0,size))
                            if copied!=wanted or c[5]!=1 or struct.unpack_from('<I',c,0x44)[0]!=stream+3 or u.reg_read(REGS[4])!=0x02010AC0:raise ValueError('F90C reader effects')
                            if bytes(u.mem_read(0x02010ABC,4))+bytes(u.mem_read(0x02010AC0+size,4))!=b'\xA6'*8:raise ValueError('Reader canary')
                        digest.update(struct.pack('<III?',mask,seed,n,enabled)+token+actual);cases+=1
            expected_pairs=sum(mask.bit_count() for mask in range(1<<count))
            if len(selection_coverage)!=expected_pairs:raise ValueError('Missing mask/slot fixture')
            result=dict(provider=f['provider'],image=label,cases=cases,mask_selected_slot_pairs=len(selection_coverage),rejections=rejection_count,effects_sha256=digest.hexdigest())
            if label=='source':reference[f['provider']]=result['effects_sha256']
            elif reference[f['provider']]!=result['effects_sha256']:raise ValueError('Source/product effects differ')
            aggregate.append(result);total+=cases;print(label,f['provider'],cases,'PASS',flush=True)
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=ROM,baseline_sha256=sha(product),tool_sha256=sha((ROOT/'tools/bench_profile_arrays_029.py').read_bytes()),native_ranges=ranges,fields=fields,results=aggregate,case_count=total,modeled_services=dict(BIOS_Div=div_calls),native_helpers_substituted=[],rom_written=False,product_admitted=False,release_eligible=False,limits=['Controlled valid terminated legacy records only; native editor capacities from source table, not descriptor-derived glyph counts.','Every enabled/disabled flag and active-record mask; every active selection; lengths0..cap with two native token fixtures.','FC0F both target255 continuation only; non255 script dispatch not covered.','No natural caller/cache lifetime audit, actual GBA display, all input repertoire/default/import/writer coverage, Hangul record support or persistence.','Not permission to enable array providers in a production translation model.']))
    print('PASS029 array CPU',total,'NO ROM written')

if __name__=='__main__':main()
