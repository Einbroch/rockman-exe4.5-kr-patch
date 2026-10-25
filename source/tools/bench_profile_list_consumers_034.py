"""Connect native list prefix/dispatcher/reset to guarded F90C copies.

Stops before graphics initialization and before taken-script dispatch. These
stops are observation boundaries, never substituted services or returns.
"""
import hashlib
import re
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from inspect_remaining_034 import BASE,BASE_SHA
from keyitem_rom_data_024 import verify_final

from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_INTR,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T

OUT='analysis/pending_insertion_500_034_list_consumers_cpu_v1/cpu.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);product=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'))
    prior='analysis/pending_insertion_500_034_list_formatter_cpu_v1/cpu.json';proof=read(prior)
    if not proof['passed'] or proof['baseline_sha256']!=BASE_SHA:raise ValueError('List formatter baseline')
    require_hash(ROOT/'tools/bench_profile_list_formatter_034.py',proof['tool_sha256'])
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    verify_final(source,product,meta['keyitem_rom'])
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in [(0x37EF6,0x37F00),(0x37F04,0x37F56),(0x4F7B6,0x4F7CC),(0x4FB58,0x4FB70),(0x90C,0x926),(0xEC144,0xEC148),(0x94C,0x956),(0x509D0,0x509FA),(0x517D0,0x5181C)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or product[a:b]!=raw:raise ValueError('List consumer native range')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('List consumer ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in [(0x37F70,4),(0x38038,4),(0x509FC,4),(0x52654,48),(0x5181C,4),(0x518F8,4),(0x526D0+28*8,24),(0x928,4)]:
        if source[a:a+n]!=product[a:a+n]:raise ValueError('List native literal drift')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    if struct.unpack_from('<I',source,0x509FC)[0]!=0x08052654 or struct.unpack_from('<I',source,0x52654+5*4)[0]!=0x0200FA6C:raise ValueError('checkGlobal5 count pointer')
    # Decode the literal operand of08037F18, not the adjacent first Navi array.
    table=struct.unpack_from('<I',source,0x38038)[0]
    if table!=0x0803803C:raise ValueError('PET archive table literal')
    roots=[]
    for navi in range(23):
        array=struct.unpack_from('<I',source,table-0x08000000+navi*4)[0];at=array-0x08000000+10*4
        arc=f'{struct.unpack_from("<I",source,at)[0]-0x08000000:X}'
        current=next(a for a in meta['archives'] if a['archive']==arc)
        if struct.unpack_from('<I',product,at)[0]!=0x08000000+current['rom_offset']:raise ValueError('Actual033 profile table root')
        roots.append(dict(navi=navi,source_archive=arc,pointer_offset=at,current_pointer=0x08000000+current['rom_offset']))
    stop,reset_stop,jump_stop=0x080000C0,0x0804FB70,0x0804FD18
    ctx,glob,flags,stack,stream=0x0200FA20,0x02000100,0x02002000,0x03007F00,0x02020000
    srclo,srchi,scratch=0x0202607C,0x02026384,0x02010AC0
    results=[];reference={};total=0;bios_calls=0
    for label,image in [('source',source),('033',product)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[];wanted_stops=set()
        def halt(uc,a,n,d):
            if a in wanted_stops:uc.emu_stop()
        u.hook_add(UC_HOOK_CODE,halt);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def bios(uc,number,d):
            nonlocal bios_calls
            src,dest,control=[uc.reg_read(REGS[i]) for i in range(3)]
            if number!=2 or uc.reg_read(UC_ARM_REG_PC)!=0x080EC146 or dest!=ctx or control!=0x05000036 or src%4 or not stack-192<=src<stack or bytes(uc.mem_read(src,4))!=bytes(4):raise ValueError('Unexpected BIOS CpuSet domain')
            # Only this fixed CpuSet32 fill(54 zero words) is modeled. The ROM
            # helper and BIOS trampoline execute; no native function is replaced.
            uc.mem_write(dest,bytes(216));writes.append((dest,216));bios_calls+=1
        u.hook_add(UC_HOOK_INTR,bios)
        def registers(overrides):
            values=[0x1000+i*0x101 for i in range(15)];values[10]=glob;values[13]=stack;values[14]=stop|1
            for i,v in overrides.items():values[i]=v
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.mem_write(stack-256,b'\xA7'*256)
            return values
        def execute(entry,stops,allowed):
            wanted_stops.clear();wanted_stops.update(stops);writes.clear();u.emu_start(entry|1,0,count=18000)
            if u.reg_read(UC_ARM_REG_PC) not in stops:raise ValueError('Native list bounded execution')
            if any(not(stack-192<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('List consumer write extent '+str(writes))
            if bytes(u.mem_read(stack-256,64))!=b'\xA7'*64:raise ValueError('Consumer stack canary')
        for f in proof['fields']:
            digest=hashlib.sha256();cases=0;transitions=[]
            for n in range(f['count']+1):
                cap,base=f['cap'],f['base'];stride=2*cap+2
                records=b''.join(bytes([int(i<n)])+bytes([0x9B+i])+b'\xE4\x06'*(cap-1)+b'\xE5'+b'\xA4' for i in range(f['count']))
                if len(records)!=stride*f['count']:raise ValueError('Native maximum record fixture')
                # Live producer sets count then calls the actual dispatcher and
                # current composed initializer. Stop after zero/reset/restore,
                # before graphics/sound initialization begins.
                u.mem_write(glob+0x48,struct.pack('<I',flags));u.mem_write(glob+0x2C,struct.pack('<I',ctx));u.mem_write(flags,bytes(8192))
                u.mem_write(ctx,b'\x5A'*216);u.mem_write(base,records);u.mem_write(srclo,b'\xA6'*(srchi-srclo))
                pet=0x02014DD0;u.mem_write(pet,bytes(0x80));u.mem_write(pet+0x12,b'\x07')
                registers({0:f['row'],1:7})
                execute(0x08038CD8,{reset_stop},[(ctx,ctx+216),(srclo+4,srchi-4),(pet,pet+0x80)])
                state=bytes(u.mem_read(ctx,216));count=struct.unpack_from('<I',state,0x4C)[0]
                if count!=((0x5A5A5A00)|n) or state[:0x4C]!=bytes(0x4C) or state[0x5C:]!=bytes(216-0x5C):raise ValueError('Native reset count preservation/zero extent')
                if state[0x50:0x5C]!=b'\x5A'*12:raise ValueError('Native other global buffers preserved')
                # r0 now denotes the actual selected root; r1 is the script.
                root=roots[0]['source_archive'];selector=f['list_selector'] if n else f['empty_selector']
                wanted_root=0x08000000+int(root,16) if label=='source' else roots[0]['current_pointer']
                if u.reg_read(REGS[0])!=wanted_root or u.reg_read(REGS[1])!=selector[0]:raise ValueError('Producer -> native dispatcher -> actual root')
                # checkGlobal reads ONE byte, not the preserved 32-bit high bytes.
                source_buffers=bytes(u.mem_read(srclo,srchi-srclo));u.mem_write(scratch-4,b'\xA9'*(1024+8));expected=bytearray(b'\xA9'*1024)
                u.mem_write(ctx,bytes(216));u.mem_write(ctx+0x4C,struct.pack('<I',count))
                visited=[]
                if n:
                    for page in range((n+2)//3):
                        # Native guards occur after pages1/2. Taken branches are
                        # observed at their actual dispatch entry, never stubbed.
                        if page:
                            branch=False
                            for value in range((page-1)*3+1,page*3+1):
                                command=bytes([0xEE,3,5,value,selector[0]+1,255]);u.mem_write(stream,command)
                                before=bytes(u.mem_read(ctx,216));registers({4:stream,5:ctx})
                                execute(0x080509D0,{stop,jump_stop},[])
                                branch=u.reg_read(UC_ARM_REG_PC)==jump_stop
                                if branch!=(n==value) or bytes(u.mem_read(ctx,216))!=before:raise ValueError('Native guard/global5 branch')
                                if branch:
                                    if u.reg_read(REGS[1])!=selector[0]+1:raise ValueError('Native guard jump argument')
                                    break
                                if u.reg_read(REGS[4])!=stream+6:raise ValueError('Native guard fallthrough')
                            if branch:raise ValueError('Initialized page incorrectly skipped')
                        u.mem_write(stream,bytes([0xF9,12,28+page]));registers({4:stream,5:ctx})
                        before=bytes(u.mem_read(ctx,216));slot=struct.unpack_from('<H',before,0x64)[0];dest=scratch+slot*128
                        execute(0x080517D0,{stop},[(ctx,ctx+216),(dest,dest+512)])
                        raw=bytes(u.mem_read(0x02026080+page*128,512));expected[slot*128:slot*128+512]=raw
                        if bytes(u.mem_read(scratch,1024))!=expected or bytes(u.mem_read(scratch-4,4))+bytes(u.mem_read(scratch+1024,4))!=b'\xA9'*8:raise ValueError('Native full512 scratch copy/canary')
                        state=bytes(u.mem_read(ctx,216))
                        if u.reg_read(REGS[4])!=dest or struct.unpack_from('<I',state,0x44)[0]!=stream+3 or struct.unpack_from('<H',state,0x64)[0]!=slot+1:raise ValueError('Native list F90C stream/slot')
                        for oldpage in range(page+1):
                            at=0x02026080+oldpage*128;chunk=bytes(u.mem_read(at,128));end=chunk.index(0xE5)+1
                            if bytes(u.mem_read(scratch+oldpage*128,end))!=chunk[:end]:raise ValueError('Earlier useful page overwritten')
                        visited.append(page+1)
                    # Next page (if present in the source family) must be skipped
                    # for counts1..3 and4..6, so stale buffers cannot be consumed.
                    if n<=6 and f['count']>3:
                        threshold=3 if n<=3 else 6;branch=False
                        for value in range(threshold-2,threshold+1):
                            u.mem_write(stream,bytes([0xEE,3,5,value,selector[0]+1,255]));registers({4:stream,5:ctx})
                            execute(0x080509D0,{stop,jump_stop},[])
                            branch=u.reg_read(UC_ARM_REG_PC)==jump_stop
                            if branch:
                                if value!=n:raise ValueError('Wrong final page guard')
                                break
                        if not branch:raise ValueError('Stale unused page not guarded')
                if bytes(u.mem_read(srclo,srchi-srclo))!=source_buffers or bytes(u.mem_read(base,len(records)))!=records:raise ValueError('Readers changed producer/records')
                digest.update(struct.pack('<II',n,count)+source_buffers+bytes(expected));cases+=1
                transitions.append(dict(active_names=n,pages_read=visited,slot_count=len(visited),selected_script=selector[0],selected_root=wanted_root,count_preserved_at_native_reset=True))
            result=dict(image=label,field=f['name'],cases=cases,transitions=transitions,effects_sha256=digest.hexdigest())
            if label=='source':reference[f['row']]=result['effects_sha256']
            elif reference[f['row']]!=result['effects_sha256']:raise ValueError('Source/current list consumer effects')
            results.append(result);total+=cases;print(label,f['name'],cases,'PASS',flush=True)
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),native_ranges=ranges,roots=roots,case_count=total,results=results,dependencies={p:sha((ROOT/p).read_bytes()) for p in [prior,'tools/bench_profile_list_consumers_034.py','tools/keyitem_rom_data_024.py']},native_helpers_substituted=[],modeled_services=dict(BIOS_CpuSet32_zero216=bios_calls),rom_written=False,product_admitted=False,release_eligible=False,
        limits=['Controlled valid maximum-length legacy records; full mask/length prefix denominator is separate formatter proof.','Native producer -> dispatcher -> actual Navi0 archive -> composed VM reset executed, stopped0804FB70 before graphics/sound remainder and editor initialization. Fixed BIOS CpuSet32 zero216 ONLY is modeled; this is not whole BIOS execution.','Readers execute after controlled context setup preserving actual count and buffers; no claim of full page-clear/keyWait lifetime, renderer or editor/save path.','EE03 taken branch observed before0804FD18; no called native helper replaced. F90C actual512-byte copy and prior useful-page retention verified.','23 root pointers verified statically; other Navis and candidate source-script guards still require population binding and GBA runtime.']))
    print('034 list consumers',total,'PASS; NO ROM/admission')


if __name__=='__main__':main()
