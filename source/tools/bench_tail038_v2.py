"""038 native F801/02 and EE30 source/037 CPU boundary, no ROM writer.

Real dispatchers, Navi getter and script-jump code execute. Only0092C's two
bounded zero-fill effects are modeled (two EWRAM blocks), not BIOS/timing/GBA proof.
"""
import sys,struct,re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'external/arm_bench_python'))
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_source500_038_v5 import baseline,OUT as SOURCE,BASE,BASE_SHA
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from field_hint_capacity import events

OUT='analysis/pending_insertion_500_038_native_tails_v1/cpu.json'

def main():
    cfg,source,base,meta=baseline();s=read(SOURCE+'/selection.json');carry_path=ROOT/'analysis/pending_insertion_500_038_carry_v2/verification_v1.json';carry=read(carry_path)
    if not carry['passed'] or carry['new_units']!=500:raise ValueError('038 complete carry prerequisite')
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);native_ranges=[]
    code=[(0xCEC,0xCF4),(0x4FD18,0x4FD5A),(0x4FD6C,0x4FD78),(0x5543C,0x55456),(0x524A8,0x524B8),(0x524E0,0x524F2),(0x524F4,0x5250C),(0x52534,0x52540),(0x507F4,0x50804),(0x50DD0,0x50DF4),(0x50F8C,0x50F96),(0x92C,0x946)]
    data=[(0x500E4,4),(0x5014C,4),(0x524B8,20),(0x52530,4),(0x52540,8),(0x52654+24*4,20),(0x500BC,4),(0x50124,4),(0x50804,4),(0x508C8,4),(0x50F98,4),(0x50FCC,1),(0x55458,16),(0x4FD5C,4)]
    for a,b in code:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if base[a:b]!=raw or sum(x.size for x in ins)!=len(raw):raise ValueError('038 native code identity/coverage')
        for x in ins:
            if x.size not in (2,4) or x.size==4 and x.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+x.mnemonic+' '+x.op_str,x.address)[0])!=x.bytes:raise ValueError('038 native ARMv4T roundtrip')
        native_ranges.append(dict(offset=a,bytes=len(raw),sha256=sha(raw),kind='code'))
    for a,n in data:
        if source[a:a+n]!=base[a:a+n]:raise ValueError('038 source/037 dispatch/literal identity')
        native_ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    word=lambda at:struct.unpack_from('<I',source,at)[0]
    if [word(a) for a in (0x500E4,0x5014C,0x500BC,0x50124,0x50804,0x508C8)]!=[0x080524A9,0x08052535,0x080507F5,0x08050F8D,0x08050808,0x08050DD1]:raise ValueError('038 original dispatch shape')
    if [word(0x52654+4*i) for i in (24,25,26,27,28)]!=[0x02012F19,0x02012F1A,0x02012F1B,0x02012F1C,0x02012F18]:raise ValueError('038 battle scalar destinations')
    # Shared synthetic ROM-only payload placement, never emitted as a game file.
    tail=bytearray();placements={}
    for r in carry['archives']:
        require_hash(ROOT/r['compiled']['path'],r['compiled']['sha256']);blob=(ROOT/r['compiled']['path']).read_bytes();tail.extend(b'\xff'*(-(len(base)+len(tail))%4));placements[r['archive']]=0x08000000+len(base)+len(tail);tail.extend(blob)
    ctx,glob,scene,stream,stack,stop=0x0200FA20,0x02000100,0x02000400,0x02020000,0x03007F00,0x080000C0
    engines=[]
    for label,image in [('source',source+b'\xff'*(len(base)-len(source))+bytes(tail)),('037',base+bytes(tail))]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);u.mem_map(0x06000000,0x20000);writes=[];fills=[]
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d,w=writes:w.append((a,n)))
        def fill(uc,a,n,d,f=fills):
            dest,size=uc.reg_read(REGS[0]),uc.reg_read(REGS[1])
            if (dest,size) not in ((0x02012F50,0xF00),(0x02013E50,0xF00)):raise ValueError('038 bounded clear helper domain')
            f.append((dest,size));uc.mem_write(dest,bytes(size));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
        u.hook_add(UC_HOOK_CODE,fill,begin=0x0800092C,end=0x0800092C);engines.append((label,u,writes,fills))
    counts={};branches=[];stores=[]
    def execute(engine,entry,command,before,navi=0,root=None,pc=None):
        label,u,writes,fills=engine;u.mem_write(ctx,before);u.mem_write(glob+64,struct.pack('<I',scene));u.mem_write(scene,bytes([0,navi])+bytes(14));u.mem_write(stack-128,b'\xA5'*128);u.mem_write(0x02012F10,b'\xB6'*32);u.mem_write(0x02012F50,b'\xC7'*0xF00);u.mem_write(0x02013E50,b'\xC7'*0xF00)
        if pc is None:u.mem_write(stream,command);pc=stream
        vals=[0x1000+i*0x101 for i in range(15)];vals[4]=pc;vals[5]=ctx;vals[10]=glob;vals[13]=stack;vals[14]=stop|1
        for r,v in zip(REGS,vals):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();fills.clear();u.emu_start(entry|1,0,count=3000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack or any(u.reg_read(REGS[i])!=vals[i] for i in (5,6,8,9,10,11,12)):raise ValueError('038 native continuation/preserved registers')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-128<=a and a+n<=stack or 0x02012F18<=a and a+n<=0x02012F1E) for a,n in writes):raise ValueError('038 unexpected CPU persistent write')
        return u,bytes(u.mem_read(ctx,216)),u.reg_read(REGS[4]),list(fills)
    # Exhaust byte stores and word boundaries + every actual cohort word value.
    values16={0,1,255,256,32767,65535};tail_groups=[g for g in s['groups'] if g['profile']=='normal-store-tail-geometry']
    for g in tail_groups:
        for p in g['geometry']:
            for x in p['source_store_tail_retained']:
                if x['command']=='storeGlobal16':values16.add(x['value'])
    for subtype,index,values in [(1,i,range(256)) for i in (24,25,26,28)]+[(2,27,sorted(values16))]:
        dest=word(0x52654+4*index)
        for value in values:
            encoded=value.to_bytes(subtype,'little');cmd=bytes([0xF8,subtype,index])+encoded;before=bytes([0x53])*216
            for engine in engines:
                for entry,width in ((0x080524A8,False),(0x08052534,True)):
                    u,actual,after,fills=execute(engine,entry,cmd,before);expected=bytearray(b'\xB6'*32)
                    if not width:expected[dest-0x02012F10:dest-0x02012F10+subtype]=encoded
                    if actual!=before or after!=stream+len(cmd) or fills or bytes(u.mem_read(0x02012F10,32))!=expected:raise ValueError('038 native store exact effects')
                    counts['store-width' if width else 'store-draw']=counts.get('store-width' if width else 'store-draw',0)+1
        stores.append(dict(subtype=subtype,index=index,destination=dest,values=len(values)))
    # Each real EE30 command, every current Navi, RAM source vs readonly ROM clone.
    byarc={r['archive']:r for r in carry['archives']}
    for g in s['groups']:
        if g['profile']!='normal-navi-tail-geometry':continue
        arc=g['archive'];r=byarc[arc];native=lz77_decompress(source,int(arc,16))[0];target=(ROOT/r['compiled']['path']).read_bytes();sc=g['script'];count=r['script_count'];raw=script_spans(native,count)[sc];translated=script_spans(target,count)[sc]
        for branch in g['geometry'][0]['source_navi_branch_tail_retained']:
            navi,jump=branch['navi'],branch['target'];cmd=bytes([0xEE,0x30,navi,jump,255])
            if jump>=count or raw.count(cmd)!=1 or translated.count(cmd)!=1:raise ValueError('038 branch operand/stream provenance')
            callee=script_spans(target,count)[jump]
            if not callee or not script_spans(native,count)[jump]:raise ValueError('038 branch target not a real script')
            branches.append(dict(archive=arc,script=sc,navi=navi,target=jump,target_prefix_hex=callee[:20].hex()))
            for current in range(23):
                for engine in engines:
                    for mode,blob,root in [('nativeRAM',native,0x0203C800),('carryROM',target,placements[arc])]:
                        u=engine[1]
                        if mode=='nativeRAM':u.mem_write(root,blob)
                        offset=struct.unpack_from('<H',blob,sc*2)[0]+(raw if mode=='nativeRAM' else translated).index(cmd);pc=root+offset;before=bytearray([0x57]*216)
                        struct.pack_into('<I',before,0x30,root);struct.pack_into('<I',before,0x70,0);struct.pack_into('<I',before,0x7C,0);before[0xF]=0;before[0x18]=52;before[0x19]=110;before[8]=2
                        uc,actual,after,fills=execute(engine,0x080507F4,cmd,bytes(before),current,root,pc);expected=bytearray(before)
                        if current==navi:
                            at=root+struct.unpack_from('<H',blob,jump*2)[0];expected[1]=jump
                            for k in (0x2C,0x34):struct.pack_into('<I',expected,k,at)
                            for k in (4,0x12,2,0x17,0x3D,0xF):expected[k]=0
                            for k in (0x64,0x80,0x70,0x7C):struct.pack_into('<I',expected,k,0)
                            struct.pack_into('<I',expected,0x74,1);expected[0x11]=2;expected[0x94]=52;flags=struct.unpack_from('<H',expected,0x3E)[0]&~word(0x4FD5C);struct.pack_into('<H',expected,0x3E,flags)
                            if after!=at or fills!=[(0x02012F50,0xF00),(0x02013E50,0xF00)] or bytes(uc.mem_read(0x02012F50,0xF00))!=bytes(0xF00) or bytes(uc.mem_read(0x02013E50,0xF00))!=bytes(0xF00):raise ValueError('038 original script jump/reset/clear effects')
                        elif after!=pc+5 or fills:raise ValueError('038 false branch continue')
                        if actual!=expected or bytes(uc.mem_read(0x02012F10,32))!=b'\xB6'*32 or uc.reg_read(REGS[0])!=1:raise ValueError('038 native Navi branch context/variables')
                        counts['Navi-match' if current==navi else 'Navi-continue']=counts.get('Navi-match' if current==navi else 'Navi-continue',0)+1
    require_hash(ROOT/BASE,BASE_SHA)
    deps=['tools/bench_tail038_v2.py','tools/normal_store_tail038_v1.py','tools/normal_navi_tail038_v1.py',SOURCE+'/selection.json',SOURCE+'/preflight_v1.json','analysis/pending_insertion_500_038_carry_v2/verification_v1.json']
    frozen_write(ROOT/OUT,dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,case_counts=counts,vectors=sum(counts.values()),native_ranges=native_ranges,store_domains=stores,branch_commands=branches,store_tail_groups=len(tail_groups),Navi_branch_groups=sum(g['profile']=='normal-navi-tail-geometry' for g in s['groups']),zero_fill_model=dict(entry=0x0800092C,domains=[[0x02012F50,0xF00],[0x02013E50,0xF00]]),actual_Navi_getter_and_jump_executed=True,readonly_translated_stream_and_script_offsets_verified=True,geometry_fields_and_battle_globals_verified=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['Source and exact037 native CPU code with synthetic readonly carry payloads, NOT an038 product ROM or GBA gameplay/battle outcome.','0092C fill helper modeled explicitly; real BIOS/audio/timing/frame progression not certified.','Actual038 primary build must enforce current tail operand/provenance/continuation bounds and rerun affected exact-ROM runtime.']))
    print('PASS038 native store/Navi-tail CPU',sum(counts.values()),'vectors; NO ROM')

if __name__=='__main__':main()
