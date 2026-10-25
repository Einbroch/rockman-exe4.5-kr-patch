"""Original initializer with modeled clear service vs editor96 staging CPU.

Not whole clear/BIOS execution, game runtime, complete writer audit or hook.
"""
import json
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB
from hangul_mixed_editor_init import assemble, initialize
from hangul_mixed_editor_init_shim import assemble as assemble_shim


def main():
    root=ROOT/'analysis/hangul_keyboard_v1'
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(product,identity);current=product.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    # Manual consumer boundaries, explicitly excluding inline tables/pools.
    regions=[('per_frame_input',0x34EFE,0x34F68),('commit',0x35000,0x35032),
             ('answer_compare',0x35038,0x35086),('cursor_draw',0x35344,0x35376),
             ('input_handler',0x353B0,0x35582),('legacy_import',0x3558C,0x355AE),
             ('caller_option',0x355AE,0x355B6),('initializer',0x355B6,0x355F6),
             ('padding',0x355F6,0x3561A),('pointer_count',0x35620,0x3562C),
             ('flatten',0x3562C,0x3564E),('page_draw',0x35676,0x356BA),('page_transfer',0x356D0,0x356E2)]
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    header='.syntax unified\n.cpu arm7tdmi\n.thumb\n';scope=[]
    for name,start,end in regions:
        data=rom[start:end]
        if current[start:end]!=data:raise ValueError('consumer source drift '+name)
        ins=list(cs.disasm(data,0x08000000+start))
        if sum(i.size for i in ins)!=end-start:raise ValueError('bounded instruction coverage')
        rows=[]
        for i in ins:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('non ARMv4T opcode')
            if bytes(ks.asm(header+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('instruction roundtrip')
            rows.append(dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
        scope.append(dict(id=name,start=hex(0x08000000+start),end_exclusive=hex(0x08000000+end),sha256=sha(data),instructions=rows))
    # Aligned encoding scan includes data as well as code; not indirect-call coverage.
    direct_candidates=[]
    for at in range(0,len(rom)-3,2):
        hi=int.from_bytes(rom[at:at+2],'little');lo=int.from_bytes(rom[at+2:at+4],'little')
        if hi&0xF800==0xF000 and lo&0xF800==0xF800:
            delta=(hi&2047)<<12|(lo&2047)<<1
            if delta&0x400000:delta-=0x800000
            if 0x08000000+at+4+delta==0x080355B6:direct_candidates.append(at)
    if direct_candidates!=[0x30EC8,0x3101C,0x38DA2,0x39E3E,0x3A1DE]:raise ValueError('direct initializer BL candidate population')
    caller_windows=[]
    for at in direct_candidates:
        end=at+(18 if at==0x3A1DE else 16)  # Do not split trailing 4-byte BL.
        data=rom[at-16:end];rows=list(cs.disasm(data,0x08000000+at-16))
        if current[at-16:end]!=data or sum(i.size for i in rows)!=len(data):raise ValueError('caller window identity/extent')
        for i in rows:
            if i.size not in (2,4) or i.size==4 and (i.mnemonic!='bl' or int.from_bytes(i.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(i.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('caller ARMv4T')
            if bytes(ks.asm(header+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('caller instruction roundtrip')
        caller_windows.append(dict(call_pc=hex(0x08000000+at),start=hex(0x08000000+at-16),end_exclusive=hex(0x08000000+end),sha256=sha(data),instructions=[dict(pc=hex(i.address),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in rows]))
    blob,isa=assemble();out=root/'cpu_editor_init';out.mkdir(exist_ok=True)
    (out/'helper.bin').write_bytes(blob);blob=(out/'helper.bin').read_bytes()
    shim,shim_isa=assemble_shim();(out/'shim.bin').write_bytes(shim)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08800000,4096);u.mem_write(0x08800000,blob);u.mem_protect(0x08800000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08801000,4096);u.mem_write(0x08801000,shim);u.mem_protect(0x08801000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_protect(0x02000000,4096,UC_PROT_READ)
    u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    src,dest,editor,sp,stop=0x02000101,0x02001103,0x0200FC40,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(original_initializer_calls=0,modeled_clear_calls=0,staging_initializer_calls=0,rejected=0,UI16_native_comparisons=0)
    counts.update(shim_calls=0,shim_rejected=0,shim_original_liveout_comparisons=0)
    watching=[False]
    def shim_write(cpu,access,address,size,value,user):
        if watching[0] and not (editor<=address and address+size<=editor+96 or sp-140<=address and address+size<=sp):
            raise ValueError('shim write outside editor96/stack140')
    u.hook_add(UC_HOOK_MEM_WRITE,shim_write)
    def clear_service(cpu,address,size,user):
        if (cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1))!=(editor,96):raise ValueError('clear service contract')
        cpu.mem_write(editor,bytes(96));counts['modeled_clear_calls']+=1
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
    u.hook_add(UC_HOOK_CODE,clear_service,begin=0x0800090C,end=0x0800090C)
    def call(pc,args,stack):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        for reg,val in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):u.reg_write(reg,val)
        for i,reg in enumerate(regs):u.reg_write(reg,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);u.emu_start(pc|1,stop,count=10000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('ABI')
        if bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('stack extent')
        return u.reg_read(UC_ARM_REG_R0)
    def liveouts():
        return [u.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3)]+[u.reg_read(UC_ARM_REG_CPSR)&0xF0000000]
    def bridge(args,wanted,original_liveout=None):
        u.mem_write(editor-4,b'\xA7'*104);watching[0]=True
        try:result=call(0x08801000,args,140)
        finally:watching[0]=False
        if result!=int(wanted is not None):raise ValueError('shim return')
        expected=b'\xA7'*4+(wanted if wanted is not None else b'\xA7'*96)+b'\xA7'*4
        if bytes(u.mem_read(editor-4,104))!=expected:raise ValueError('shim editor96/atomic/canary')
        if original_liveout is not None:
            if liveouts()!=original_liveout:raise ValueError('shim original register/NZCV liveouts')
            counts['shim_original_liveout_comparisons']+=1
        counts['shim_calls']+=1;counts['shim_rejected']+=wanted is None
    def staging(params,available=16,output_available=96,source=src,output=dest,mode=0,pointer=None):
        try:wanted=initialize(params)
        except ValueError:wanted=None
        if available<16 or output_available<96 or mode or pointer is not None or output+96>0xFFFFFFFF or not(output+96<=source or source+16<=output):wanted=None
        u.mem_write(0x02000000,b'\xA7'*8192);u.mem_write(source,params);before=bytearray(u.mem_read(0x02000000,8192))
        if call(0x08800000,[source if pointer is None else pointer,output,available|output_available<<16,mode],116)!=int(wanted is not None):raise ValueError('staging return')
        if wanted is not None:before[output-0x02000000:output-0x02000000+96]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(before):raise ValueError('staging atomic/bounds')
        counts['staging_initializer_calls']+=1;counts['rejected']+=wanted is None
        return wanted
    print('original UI16/destination vs compact editor staging',flush=True)
    for cap in list(range(1,11))+list(range(129,139)):
        for component in (1,3):
            for value in range(256):
                args=[cap,33,0x020010A6,0];args[component]=0xABCDEF00|value
                params=struct.pack('<4I',*args);wanted=staging(params)
                u.mem_write(editor-4,b'\xA7'*104);call(0x080355B6,args,24)
                original_liveout=liveouts()
                if original_liveout!=[1,int(cap>=128),editor+32,args[3],0]:raise ValueError('original valid-domain liveouts')
                expected=wanted[:16]+struct.pack('<4I',editor+32,editor+32,editor+32,args[2])+bytes(64)
                if bytes(u.mem_read(editor-4,104))!=b'\xA7'*4+expected+b'\xA7'*4:raise ValueError('original initializer/UI16')
                counts['original_initializer_calls']+=1;counts['UI16_native_comparisons']+=1
                bridge(args,wanted,original_liveout)
        print('capacity flag',cap,flush=True)
    valid=struct.pack('<4I',4,33,0x020010A6,0)
    for cap in (0,11,128,139,255,256,0xFFFFFFFF):staging(struct.pack('<4I',cap,33,0,0))
    for cap in range(256):
        if cap not in tuple(range(1,11))+tuple(range(129,139)):bridge([cap,33,0x020010A6,0],None)
    for cap in (256,0x80000004,0xFFFFFFFF):bridge([cap,33,0x020010A6,0],None)
    for size in range(16):staging(valid,available=size)
    for size in range(96):staging(valid,output_available=size)
    for mode in (1,255,0xFFFFFFFF):staging(valid,mode=mode)
    for a in range(4):
        for b in range(4):staging(valid,source=src+a,output=dest+b)
    for delta in range(-95,16):staging(valid,output=src+delta)
    staging(valid,pointer=0xFFFFFFF8);staging(valid,output=0xFFFFFFF0)
    if counts['modeled_clear_calls']!=10240:raise ValueError('clear call population')
    names=['hangul_mixed_editor_init.py','hangul_mixed_editor_init_shim.py','bench_keyboard_editor_init_contract.py','hangul_mixed_replay_state.py','hangul_mixed_editor.py','extended_dialogue.py']
    report=dict(id='exe45.hangul-keyboard.editor-init-contract.v1',passed=True,rom_integrated=False,source_sha256=profile['sha256'],current_rom_sha256=identity,counts=counts,helper_bytes=len(blob),editor_bytes=96,stack_bytes=116,ISA=isa,bounded_consumer_regions=scope,actual_game_layout_adopted=False,clear_service_modeled=True,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in names},artifacts={'helper.bin':sha(blob)},limits=['Original initializer clear-service call is modeled; not BIOS/whole-clear routine or maximum game stack evidence.','Instruction inventory is bounded explicit regions, not whole-ROM control-flow/reference/writer completeness.','Staging helper takes params16, not original register ABI; no game hook.', 'Old pointers+16/+20/+24/+28 overlap new destination/compact; entire consumer group must be replaced atomically.', 'Answer comparison scans raw flat bytes with98/E5/zero handling; mixed glyph bytes cannot be passed unchanged.','No game UI/cache/commit/save/fresh-load or96-byte memory lifetime adoption.'])
    report.update(shim_bytes=len(shim),shim_own_stack_bytes=24,shim_nested_stack_bytes=140,shim_ISA=shim_isa,shim_valid_liveouts=['r0=1','r1=capacityFlag>=128','r2=editor+32 (compatibility value, NOT usable legacy buffer)','r3=original callerValue','NZCV=0 for tested EWRAM editor'],shim_original_register_ABI_fixture=True)
    report['direct_initializer_BL_candidate_windows']=caller_windows
    report['limits'].append('Five aligned direct BL encoding candidates have bounded source instruction windows; this is not indirect-call coverage, whole caller execution, dynamic capacity proof or a complete caller/writer audit.')
    report['artifacts']['shim.bin']=sha(shim)
    report['limits'][2]='Staging helper is bridged to original register argument/live-out ABI only in CPU fixtures; no game hook. r2 compatibility pointer must not reach old consumers.'
    report['limits'].append('Unsupported capacities fail atomically with r0=0; no real caller failure handling or complete caller-domain audit established. Shim stack140 is a fixture extent, not game/IRQ budget.')
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('PASS editor init contract CPU',counts,flush=True)


if __name__=='__main__':main()
