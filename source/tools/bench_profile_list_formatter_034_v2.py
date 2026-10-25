"""Controlled native profile-list formatter prefix, not product admission.

Execute 08038CD8 through the real native flag helper, stopping BEFORE the
dialogue dispatcher. No helper substitution and no game/ROM writes.
"""
import hashlib
import struct
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
from inspect_remaining_034 import BASE, BASE_SHA
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

OUT = 'analysis/pending_insertion_500_034_list_formatter_cpu_v2/cpu.json'
ROWS = {1:'older_brother',2:'younger_brother',3:'older_sister',4:'younger_sister',5:'friend',7:'hobby',12:'favourite_show',15:'wish'}


def main():
    cfg = read('project.json'); sp = ROOT/cfg['source_profile']['filename']
    require_hash(sp,cfg['source_profile']['sha256']); source=sp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA); product=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB); ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB); ranges=[]
    for a,b in [(0x38CD8,0x38DB8),(0x287B2,0x287CA)]:
        raw=source[a:b]; ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('Incomplete formatter code')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('ARMv4T formatter roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in [(0x38DD4,28),(0x3B0D0,26*16)]:ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    for r in ranges:
        a,n=r['offset'],r['bytes']
        if product[a:a+n]!=source[a:a+n]:raise ValueError('Native formatter source/current drift')
    if struct.unpack_from('<7I',source,0x38DD4)!=(0x02026080,0x02026100,0x02026180,0x0200FA6C,0x0803B0D0,0x080526D0,0x02000950):raise ValueError('Formatter literal binding')
    fields=[]
    for row,name in ROWS.items():
        raw=source[0x3B0D0+16*row:0x3B0E0+16*row];count,index,cap=raw[:3]
        if count not in (3,4,8) or cap not in (6,8):raise ValueError('Profile list table shape')
        fields.append(dict(row=row,name=name,count=count,cap=cap,flag=struct.unpack_from('<H',raw,12)[0],base=0x02000950+struct.unpack_from('<H',raw,14)[0],empty_selector=list(raw[4:6]),list_selector=list(raw[6:8])))
    # The bounded source region includes the native final byte written immediately
    # before unused buffers for active counts exactly three or six.
    lo,hi=0x0202607C,0x02026384
    stack,glob,flags,countptr,stop,dispatch=0x03007F00,0x02000100,0x02002000,0x0200FA6C,0x080000C0,0x08038D8A
    results=[];reference={};total=0
    for label,image in [('source',source),('033',product)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        u.mem_write(glob+0x48,struct.pack('<I',flags));writes=[]
        def halt(uc,a,n,d):
            if a in (stop,dispatch):uc.emu_stop()
        u.hook_add(UC_HOOK_CODE,halt)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        for f in fields:
            digest=hashlib.sha256();cases=0;counts=set();boundary_writes=set();max_extent=[0,0,0]
            count,cap,base=f['count'],f['cap'],f['base'];stride=2*cap+2
            flagaddr=flags+f['flag']//8;flagmask=0x80>>(f['flag']%8)
            for enabled in (False,True):
                u.mem_write(flagaddr,bytes([flagmask if enabled else 0]))
                for mask in range(1<<count):
                    # A set native flag takes the refusal return before reading names.
                    lengths=[0] if enabled else range(cap+1)
                    for length in lengths:
                        for token in ([b'\x9B'] if enabled else [b'\x9B',b'\xE4\x06']):
                            records=bytearray();names=[]
                            for i in range(count):
                                name=((bytes([0x9B+i]) if len(token)==1 else bytes([0xE4,0x06+i]))+token*(length-1)) if length else b''
                                names.append(name)
                                records+=bytes([bool(mask>>i&1)])+name+b'\xE5'+b'\xA4'*(2*cap-len(name))
                            if len(records)!=count*stride:raise ValueError('Fixture record shape')
                            u.mem_write(base-4,b'\xA3'*4+bytes(records)+b'\xA3'*4)
                            initial=bytes((i*13+0x51)&255 for i in range(hi-lo));u.mem_write(lo,initial)
                            u.mem_write(countptr-4,b'\xA8'*9);u.mem_write(stack-128,b'\xA7'*128)
                            values=[0x1000+i*0x101 for i in range(15)]
                            values[0]=f['row'];values[1]=7;values[10]=glob;values[13]=stack;values[14]=stop|1
                            for r,v in zip(REGS,values):u.reg_write(r,v)
                            u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(0x08038CD9,0,count=12000)
                            pc=u.reg_read(UC_ARM_REG_PC);expected=bytearray(initial)
                            active=[i for i in range(count) if mask>>i&1];n=len(active)
                            if enabled:
                                if pc!=stop or u.reg_read(REGS[0])!=1 or u.reg_read(REGS[13])!=stack:raise ValueError('Native refusal return')
                                wanted_count=0xA8
                                if any(u.reg_read(REGS[i])!=values[i] for i in range(4,13)):raise ValueError('Refusal preserved registers')
                            else:
                                if pc!=dispatch or u.reg_read(REGS[13])!=stack-52:raise ValueError('Formatter dispatcher boundary')
                                expected_selector=f['list_selector'] if n else f['empty_selector']
                                if [u.reg_read(REGS[i]) for i in (0,1,2)]!=expected_selector+[7]:raise ValueError('Native selector/priority')
                                first_empty=next((base+i*stride for i in range(count) if not mask>>i&1),0)
                                if struct.unpack('<I',u.mem_read(stack-48,4))[0]!=first_empty:raise ValueError('Native first empty record')
                                for j in range(0,n,3):
                                    group=active[j:j+3];data=b'\xE8'.join(names[i] for i in group)+b'\xE5';at=0x02026080+(j//3)*128
                                    expected[at-lo:at-lo+len(data)]=data
                                    # Each appended LF first receives a following E5.
                                    # Final replacement leaves this extra E5 beyond the
                                    # first terminator, still inside the initialized page.
                                    expected[at-lo+len(data)]=0xE5
                                    max_extent[j//3]=max(max_extent[j//3],len(data)+1)
                                    if len(group)>3 or length*11>cap*11 or len(data)+1>128:raise ValueError('Declared finite native list bounds')
                                if n and n%3==0:
                                    at=0x02026080+(n//3)*128-1;expected[at-lo]=0xE5;boundary_writes.add(hex(at))
                                wanted_count=n;counts.add(n)
                                if any(u.reg_read(REGS[i])!=values[i] for i in range(8,13)):raise ValueError('Formatter high register preservation')
                            actual=bytes(u.mem_read(lo,hi-lo))
                            if actual!=bytes(expected):raise ValueError('Native formatter bytes '+str((label,f['row'],enabled,mask,length,token.hex())))
                            if bytes(u.mem_read(base-4,len(records)+8))!=b'\xA3'*4+bytes(records)+b'\xA3'*4:raise ValueError('Native records mutated')
                            if bytes(u.mem_read(countptr-4,9))!=b'\xA8'*4+bytes([wanted_count])+b'\xA8'*4:raise ValueError('Global count/canary')
                            if bytes(u.mem_read(stack-128,64))!=b'\xA7'*64:raise ValueError('Native stack canary')
                            allowed=[] if enabled else [(lo+4,hi-4),(countptr,countptr+1)]
                            if any(not(stack-64<=a and a+size<=stack or any(a0<=a and a+size<=a1 for a0,a1 in allowed)) for a,size in writes):raise ValueError('Unexpected formatter write')
                            digest.update(struct.pack('<II??',mask,length,enabled,len(token)==2)+actual+bytes([wanted_count])+struct.pack('<I',pc));cases+=1
            if counts!=set(range(count+1)):raise ValueError('Missing active count boundary')
            result=dict(image=label,field=f['name'],cases=cases,active_counts=sorted(counts),max_initialized_page_bytes=max_extent,boundary_write_addresses=sorted(boundary_writes),effects_sha256=digest.hexdigest())
            if label=='source':reference[f['row']]=result['effects_sha256']
            elif reference[f['row']]!=result['effects_sha256']:raise ValueError('Source/current formatter effects drift')
            results.append(result);total+=cases;print(label,f['name'],cases,'PASS',flush=True)
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,tool_sha256=sha((ROOT/'tools/bench_profile_list_formatter_034_v2.py').read_bytes()),native_ranges=ranges,fields=fields,results=results,case_count=total,native_helpers_substituted=[],modeled_services=[],rom_written=False,product_admitted=False,release_eligible=False,
        limits=['Controlled native-valid E5-terminated legacy records only; per-field capacities are source metadata, not 512-byte descriptor glyph widths.','All active masks, lengths0..cap and one-/two-byte native fixtures; source enabled flag refuses before formatting.','Normal route stops at08038D8A BEFORE dialogue dispatcher; no callee or editor is stubbed, invoked, or proven.','Unused page buffers remain stale. Counts exactly3/6 also write E5 immediately before the next unused buffer; not evidence of a visible defect.','VM global comparison, page guards, F90C512-byte scratch-copy lifetime, actual GBA display, Hangul record support and persistence remain unverified for this list path.']))
    print('034 list formatter prefix',total,'PASS; NO ROM/admission')


if __name__=='__main__':main()


