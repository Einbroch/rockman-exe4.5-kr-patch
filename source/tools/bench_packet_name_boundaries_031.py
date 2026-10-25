"""Native selector/edit/commit and bounded 12byte link-copy experiments.

Source/030, controlled CPU RAM only. No transport service replacement, game
state writes or ROM output. Stops before sound/link-control/outer returns.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T

BASE='poc/output/pending500_030_v1.gba'
OUT='analysis/pending_insertion_500_031_packet_cpu_v1/cpu.json'

def tokens(image):
    base=struct.unpack_from('<I',image,0x35748)[0]-0x08000000;result=[]
    for page,off in enumerate(struct.unpack_from('<3H',image,base+4)):
        rows=[];at=base+off
        while image[at]!=0xE5:
            n=2 if image[at]==0xE4 else 1;rows.append(image[at:at+n].hex());at+=n
            if len(rows)>105:raise ValueError('031 native selector extent')
        result.append(rows)
    return result

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256']);rom=(ROOT/BASE).read_bytes()
    if tokens(source)!=tokens(rom) or tokens(source)[0][81]!='e406' or tokens(source)[0][0]!='9b':raise ValueError('031 actual source/current native selector fixtures')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code=[(0x35494,0x354F2),(0x355F6,0x3561A),(0x35620,0x3564E),(0x35000,0x35032),(0x32AC6,0x32AD8),(0x35E7A,0x35E82),(0x910E,0x911A),(0x9134,0x915C),(0x94C,0x956),(0x39E2C,0x39E42)]
    data=[(0x35582,4),(0x3574C,4),(0x3561C,4),(0x35034,4),(0x353AC,4),(0x35E9C,4),(0x35EA4,4),(0x9360,4),(0x936C,16)]
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    for a,b in code:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('031 code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('031 ARMv4T code roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in data:ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    for r in ranges:
        a,n=r['offset'],r['bytes']
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('031 source/030 native range drift')
    stop,stack,editor,cells,flat,owner,glob,state=0x080000C0,0x03007F00,0x0200FC40,0x0200FC60,0x0200FC80,0x02000E50,0x02000100,0x02000400
    reports=[];reference={};count=0
    for label,image in [('source',source),('030',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);writes=[];ends={stop,0x080354EC,0x0803557E,0x0800911A,0x0800915C}
        def codehook(uc,a,n,d):
            if a in ends:uc.emu_stop()
        u.hook_add(UC_HOOK_CODE,codehook);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,a,n,v,d:writes.append((a,n)))
        def run(entry,regs,allowed,expect=stop):
            values=[0x1000+i*0x101 for i in range(15)];values[10]=glob;values[13]=stack;values[14]=stop|1
            for k,v in regs.items():values[k]=v
            for r,v in zip(REGS,values):u.reg_write(r,v)
            u.mem_write(stack-256,b'\xA7'*256);u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();u.emu_start(entry|1,0,count=12000)
            if u.reg_read(UC_ARM_REG_PC)!=expect or u.reg_read(REGS[13])!=stack:raise ValueError('031 block stop/stack '+hex(entry))
            if any(not(stack-128<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('031 unexpected bounded block write '+str(writes))
            if bytes(u.mem_read(stack-256,128))!=b'\xA7'*128:raise ValueError('031 block stack canary')
        for tok,cell in ((b'\x9B',0),(b'\xE4\x06',81)):
            for length in range(7):
                u.mem_write(editor,bytes(96));u.mem_write(editor+4,bytes([6]));u.mem_write(editor+6,bytes([cell%15,cell//15,0]));u.mem_write(owner-4,b'\xA6'*22)
                for off in (0x10,0x14,0x18):u.mem_write(editor+off,struct.pack('<I',cells))
                u.mem_write(editor+0x1C,struct.pack('<I',owner));u.mem_write(glob+0x18,struct.pack('<I',state))
                for n in range(length):
                    run(0x08035494,{4:editor},[(editor+0x14,editor+0x1C),(cells,cells+12)],0x080354EC)
                    if u.reg_read(REGS[2])!=cells+2*(n+1) or bytes(u.mem_read(cells+2*n,2))!=tok.ljust(2,b'\x00'):raise ValueError('031 actual native picker/append')
                if length==6:
                    before=bytes(u.mem_read(editor,96));run(0x08035494,{4:editor},[],0x0803557E)
                    if bytes(u.mem_read(editor,96))!=before:raise ValueError('031 seventh native glyph rejection')
                run(0x080355F6,{},[(cells,cells+13)])
                run(0x0803562C,{},[(flat,flat+32)])
                run(0x08035000,{},[(owner,owner+14),(0x02014E74,0x02014E94)])
                name=tok*length+b'\xE5'
                if bytes(u.mem_read(owner,14))!=b'\x01'+name+b'\xA6'*(13-len(name)) or bytes(u.mem_read(owner-4,4))!=b'\xA6'*4 or bytes(u.mem_read(owner+14,4))!=b'\xA6'*4:raise ValueError('031 actual commit/canaries')
                u.mem_write(0x0203A1EC,b'\xA6'*20)
                run(0x0800910E,{},[(0x0203A1F0,0x0203A1FC)],0x0800911A)
                wire=bytes(u.mem_read(0x0203A1F0,12));wanted=bytes(u.mem_read(owner+1,12))
                if wire!=wanted or bytes(u.mem_read(0x0203A1EC,4))+bytes(u.mem_read(0x0203A1FC,4))!=b'\xA6'*8:raise ValueError('031 actual export12/canaries')
                has_end=0xE5 in wire
                if has_end!=(len(name)<=12):raise ValueError('031 exact12 E5 presence')
                for side in (0,1):
                    for outside in (0,0xE5,0xA6):
                        u.mem_write(state+0xD,bytes([side]));u.mem_write(0x0203C840,wire);u.mem_write(0x0203C940,wire);u.mem_write(0x0200F56C,b'\xA6'*40)
                        for at in (0x0200F57C,0x0200F58C):u.mem_write(at,bytes([outside]))
                        run(0x08009134,{},[(0x0200F570,0x0200F57C),(0x0200F580,0x0200F58C)],0x0800915C)
                        for at in (0x0200F570,0x0200F580):
                            if bytes(u.mem_read(at,13))!=wire+bytes([outside]):raise ValueError('031 import12 leaves13th unowned')
                        if bytes(u.mem_read(0x0200F56C,4))+bytes(u.mem_read(0x0200F57D,3))+bytes(u.mem_read(0x0200F58D,7))!=b'\xA6'*14:raise ValueError('031 import canaries')
                        item=dict(image=label,token=tok.hex(),length=length,local_side=side,preexisting_13th=outside,committed_name_hex=name.hex(),wire12_hex=wire.hex(),E5_in_wire12=has_end,import_13th_unchanged=True)
                        key=(tok.hex(),length,side,outside)
                        if label=='source':reference[key]={k:v for k,v in item.items() if k!='image'}
                        elif reference[key]!={k:v for k,v in item.items() if k!='image'}:raise ValueError('031 source/030 effects differ')
                        reports.append(item);count+=1
    paths=['tools/bench_packet_name_boundaries_031.py','analysis/pending500_030_v1/batch_status.json']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,meaning='Bounded-copy/terminator ownership experiment assertions pass, NOT multiplayer/Hangul feature pass',source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),native_ranges=ranges,selector_pages=tokens(source),case_count=count,native_edit_commit_export_prefix_fixtures=28,native_helpers_substituted=[],modeled_services=[],results=reports,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},rom_written=False,product_admitted=False,release_eligible=False,conclusions=['Native page0cell81 can append E406 six times; seventh is rejected. Native padding/flatten/commit produces12namebytes+E5 in13byte field.','Export910E..911A and import9134..915C copy12bytes. SixE406 omitsE5 in wire payload. Import leaves destination13th byte unchanged in both side settings.','Shorter names includeE5 inside12; a claim about all natural network names requires the missing initialization/transport13th-byte ownership link.'],limits=['Controlled editor initial state uses source capacity6; no full initializer/sound/outer-frame or normal native sixE406 input path execution.','Transport service calls9128/9130, peer buffers and link-control transition before/after bounded slices are not executed.','Both peer inputs equal wire fixture; tests prove two side branches/copy destinations, not distinguishable peer identity or natural serial transfer.','Not a confirmed original-game bug, malformed-record safety, all input repertoire/default/import/save state audit, GBA statistics display or031ROM integration.']))
    print('PASS031 packet boundary experiment',count,'cases; sixE406 losesE5 from12byte payload; destination13th unowned by these copies; NO ROM written')

if __name__=='__main__':main()
