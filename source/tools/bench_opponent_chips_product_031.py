"""Source/030 native opponent-chip record producer and F90C. Analysis only.

Controlled valid matching opponent/history. Does not establish multiplayer
packet origin, all histories, natural battle acquisition or Korean chip values.
"""
import struct,hashlib
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T

BASE='poc/output/pending500_031_v1.gba'
OUT='analysis/pending500_031_v1/opponent_chip_cpu.json'
FIELDS={
    'printMostLostToOpponentsChip':dict(row=18,index=20,entry=0x3872C,history=0x02000B50,previous=0x02000B70,opponent=0x020010F4,record=0x0200112C,flag=0xEBF,name_flag=0xEBE),
    'printMostDefeatedOpponentsChip':dict(row=20,index=22,entry=0x38678,history=0x02000C50,previous=0x02000C70,opponent=0x0200113E,record=0x02001176,flag=0xEC1,name_flag=0xEC0),
}

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256']);rom=(ROOT/BASE).read_bytes()
    census_path='analysis/pending_insertion_500_030_chip_pools_v1/census.json';c=read(census_path)
    if c['source_sha256']!=sha(source) or c['name_count']!=393 or c['maximum_advance']!=88:raise ValueError('031 finite native pool')
    for p,h in c['dependencies'].items():require_hash(ROOT/p,h)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x3864C,0x3866A),(0x38678,0x38716),(0x3872C,0x387CA),(0x388B4,0x388D0),(0x2871E,0x2873C),(0x2874E,0x2876C),(0x287AE,0x287CA),(0x32AC6,0x32AD8),(0x94C,0x956),(0x517D0,0x5181C)]
    data=[(0x3866C,12),(0x38718,20),(0x387CC,20),(0x38A90,4),(0x3B0D0+18*16,3*16),(0x526D0+20*8,3*8),(0x5181C,4),(0x518F8,4)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in code:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('031 complete code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('031 ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in data:ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    for r in ranges:
        a,n=r['offset'],r['bytes']
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('031 native source/030 drift')
    for name,f in FIELDS.items():
        row=source[0x3B0D0+16*f['row']:0x3B0E0+16*f['row']];field,size=struct.unpack_from('<II',source,0x526D0+8*f['index'])
        if row[:3]!=bytes([1,f['index'],8]) or field!=f['record']+1 or size!=17 or struct.unpack_from('<H',row,12)[0]!=f['flag'] or 0x02000950+struct.unpack_from('<H',row,14)[0]!=f['record']:raise ValueError('031 source field/table binding')
    stop,stack,glob,flags,ctx,stream,packet=0x080000C0,0x03007F00,0x02000100,0x02002000,0x0200FA20,0x02020000,0x0200F560
    reference={};results=[];count=0;negative=[]
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
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack:raise ValueError('031 native return/stack')
            if any(not(stack-128<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('031 unexpected write '+str(writes))
            if bytes(u.mem_read(stack-256,128))!=b'\xA7'*128:raise ValueError('031 stack canary')
            if any(u.reg_read(REGS[i])!=values[i] for i in (5,6,7,8,9,10,11,12)):raise ValueError('031 preserved registers')
        def flag_value(f):return flags+f//8,0x80>>(f%8)
        for name,f in FIELDS.items():
            digest=hashlib.sha256();field,size=f['record']+1,17;flag_at,flag_mask=flag_value(f['flag']);name_at,name_mask=flag_value(f['name_flag'])
            def setup(chip_id):
                u.mem_write(flags,bytes(0x1000));u.mem_write(name_at,bytes([name_mask]));native_name=b'\x9B'*6+b'\xE5'
                # Native previous-opponent snapshot includes presence byte.
                # `previous` here is the separate temporary chip record,
                # copied to the persistent field after native lookup.
                snapshot=b'\x01'+native_name
                u.mem_write(f['history'],snapshot+b'\xA4'*(32-len(snapshot)))
                u.mem_write(f['previous'],b'\x00'+b'\xA6'*31)
                u.mem_write(f['opponent'],b'\x01'+native_name+b'\xA4'*6)
                u.mem_write(packet,bytes(0x40));u.mem_write(packet+0x20,native_name);u.mem_write(packet+0xE,struct.pack('<H',chip_id))
                u.mem_write(field-2,b'\xA6'*(size+4));return native_name
            for record in c['names']:
                encoded=bytes.fromhex(record['raw_hex']);native_name=setup(record['chip_id'])
                run(0x08000000+f['entry'],{},[(flag_at,flag_at+1),(field-1,field+size),(f['previous'],f['previous']+32)])
                expected=encoded+b'\xA6'*(size-len(encoded))
                if bytes(u.mem_read(field,size))!=expected or bytes(u.mem_read(field-1,1))!=b'\x01' or u.mem_read(flag_at,1)[0]&(flag_mask|name_mask)!=(flag_mask|name_mask):raise ValueError('031 producer record/flag')
                if bytes(u.mem_read(field-2,1))+bytes(u.mem_read(field+size,2))!=b'\xA6'*3 or bytes(u.mem_read(f['previous'],32))!=b'\x01'+encoded+b'\xA6'*(31-len(encoded)):raise ValueError('031 record canary/temporary chip')
                u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xF9,12,f['index']]));u.mem_write(0x02010ABC,b'\xA6'*(size+8))
                run(0x080517D0,{4:stream,5:ctx},[(ctx,ctx+216),(0x02010AC0,0x02010AC0+size)])
                actual=bytes(u.mem_read(0x02010AC0,size));state=bytes(u.mem_read(ctx,216))
                if actual!=expected or u.reg_read(REGS[4])!=0x02010AC0 or state[5]!=1 or struct.unpack_from('<I',state,0x44)[0]!=stream+3:raise ValueError('031 F90C continuation/effects')
                if bytes(u.mem_read(0x02010ABC,4))+bytes(u.mem_read(0x02010AC0+size,4))!=b'\xA6'*8:raise ValueError('031 F90C canary')
                digest.update(struct.pack('<I',record['chip_id'])+actual+state);count+=1
            for condition in ('opponent-mismatch','sentinel'):
                setup(65535 if condition=='sentinel' else 9)
                if condition=='opponent-mismatch':u.mem_write(packet+0x20,b'\x9C'*6+b'\xE5')
                run(0x08000000+f['entry'],{},[(flag_at,flag_at+1),(field-1,field+size),(f['previous'],f['previous']+32)])
                if bytes(u.mem_read(field-2,size+4))!=b'\xA6'*(size+4) or u.mem_read(flag_at,1)[0]&flag_mask:raise ValueError('031 disqualified chip unexpectedly written')
                negative.append(dict(image=label,provider=name,condition=condition,record_unchanged=True,chip_flag_clear=True));count+=1
            value=digest.hexdigest()
            if label=='source':reference[name]=value
            elif reference[name]!=value:raise ValueError('031 source/030 producer+reader effects differ')
            results.append(dict(image=label,provider=name,positive_cases=393,effects_sha256=value));print(label,name,'393+2 PASS',flush=True)
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),tool_sha256=sha((ROOT/'tools/bench_opponent_chips_product_031.py').read_bytes()),census=dict(path=census_path,sha256=sha((ROOT/census_path).read_bytes())),native_ranges=ranges,fields=FIELDS,case_count=count,positive_cases=1572,negative_cases=negative,results=results,native_helpers_substituted=[],modeled_services=[],rom_written=False,product_admitted=False,release_eligible=False,limits=['Controlled matching native opponent/previous histories plus each393 pool name, source and030. Opponent mismatch andFFFFsentinel leave record untouched and chip flag clear.','Does not establish packet origin or multiplayer player-name glyph bound, reset/default/import/corrupt-save states, all sorting/history changes, no-flag/changed-history clearing branch or natural battle acquisition.','Not GBA display, Korean chip-name serialization, Hangul record support, persistence or permission to admit031 input.']))
    print('PASS031 native opponent-chip producer+F90C',count,'analysis only; no ROM written')

if __name__=='__main__':main()
