"""Native metadata caller -> new init/import -> recommit, CPU fixture only.

Patches two BLs ONLY in Unicorn's source clone.08301000/08302000 NOT free ROM.
Explicit new-format selection, not marker detection or natural gameplay/save.
"""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from hangul_mixed_editor_init import assemble as assemble_init,initialize
from hangul_mixed_editor_init_shim import assemble as assemble_init_shim
from hangul_keyboard_import_shim import assemble as assemble_import_shim
from hangul_mixed_record import pack_surface,unpack_selected_record

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={};reports={}
    for name in ('cpu_editor_init','cpu_mixed_record_import','cpu_commit_bridge','cpu_composer'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes());reports[name]=d
    native=read(base/'setup_import_caller.json');deps['setup_import_caller.json']=sha((base/'setup_import_caller.json').read_bytes())
    for n,h in native['tools'].items():require_hash(ROOT/'tools'/n,h)
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,native['current_rom_sha256']);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    for region in native['native_code']:
        a=region['offset'];b=a+region['bytes']
        if sha(rom[a:b])!=region['sha256'] or current[a:b]!=rom[a:b]:raise ValueError('native source guard')
    blobs={};isas={}
    blobs['init.bin'],isas['init']=assemble_init(0x08F0C000)
    blobs['init_shim.bin'],isas['init_shim']=assemble_init_shim(0x08301000,helper=0x08F0C001)
    blobs['import_shim.bin'],isas['import_shim']=assemble_import_shim()
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);patches=[]
    for pc,target,original in [(0x0803A1DE,0x08301000,0x080355B6),(0x0803A1E4,0x08302000,0x0803558C)]:
        if not -(1<<22)<=target-(pc+4)<(1<<22):raise ValueError('Thumb1 BL range')
        old=rom[pc-0x08000000:pc-0x08000000+4];oldins=list(cs.disasm(old,pc))
        if len(oldins)!=1 or oldins[0].mnemonic!='bl' or int(oldins[0].op_str.lstrip('#'),16)!=original:raise ValueError('old BL semantic guard')
        raw=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl '+hex(target),pc)[0]);ins=list(cs.disasm(raw,pc))
        if len(raw)!=4 or int.from_bytes(raw[:2],'little')&0xF800!=0xF000 or int.from_bytes(raw[2:],'little')&0xF800!=0xF800 or len(ins)!=1 or ins[0].mnemonic!='bl' or int(ins[0].op_str.lstrip('#'),16)!=target:raise ValueError('final BL profile')
        patches.append(dict(offset=pc-0x08000000,expected_hex=old.hex(),fixture_hex=raw.hex(),target=hex(target)))
    out=base/'cpu_keyboard_reentry';out.mkdir(exist_ok=True)
    for n,b in blobs.items():(out/n).write_bytes(b)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom)
    for p in patches:u.mem_write(0x08000000+p['offset'],bytes.fromhex(p['fixture_hex']))
    for a,n in [(0x08301000,'init_shim.bin'),(0x08302000,'import_shim.bin')]:u.mem_write(a,blobs[n])
    u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for a,b in [(0x08F0C000,blobs['init.bin']),(0x08F05000,(base/'cpu_mixed_record_import/helper.bin').read_bytes()),(0x08F06000,(base/'cpu_commit_bridge/helper.bin').read_bytes())]:
        u.mem_map(a,4096);u.mem_write(a,b);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    table=(base/'cpu_composer/transitions.bin').read_bytes();size=(len(table)+4095)&~4095
    u.mem_map(0x09000000,size);u.mem_write(0x09000000,table);u.mem_protect(0x09000000,size,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    ctx,ed,sp,stop=0x0200F550,0x0200FC40,0x03007F00,0x0FF00000
    regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[];heading_calls=[0];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def dynamic_heading(cpu,pc,size,user):
        heading_calls[0]+=1;cpu.reg_write(UC_ARM_REG_R0,33);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,dynamic_heading,begin=0x08038DB8,end=0x08038DB8)
    def execute(pc,args,end,stack,caller=False):
        u.mem_write(sp-stack-4,b'\x5A'*(stack+4));u.reg_write(UC_ARM_REG_CPSR,0x30)
        initial=[0x13579000+i for i in range(12)]
        for i,v in enumerate(args):initial[i]=v
        if caller:initial[5]=ctx
        for r,v in zip(regs,initial):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();u.emu_start(pc|1,end,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=end or u.reg_read(UC_ARM_REG_SP)!=sp or bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4:raise ValueError('return/stack')
        for i in range(5 if caller else 4,12):
            if u.reg_read(regs[i])!=initial[i]:raise ValueError('preserved registers')
        return u.reg_read(UC_ARM_REG_R0)
    def check(before,regions,stack):
        expected=bytearray(before)
        for a,b in regions:expected[a-0x02000000:a-0x02000000+len(b)]=b
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM/atomicity')
        if any(not(sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(b) for s,b in regions)) for a,n in writes):raise ValueError('write interval')
    stats=dict(caller_imports=0,syllable_reentries=0,CPU_recommits=0,caller_rejections=0,adapter_rejections=0)
    seed=bytes(range(256))*1024
    def run(row,raw,valid=True,commit=False):
        cap=row['capacity'];ptr=int(row['destination'],16);selector=row['setup_selector']
        wanted=initialize(struct.pack('<4I',cap,row['heading'],ptr,0))
        if valid:wanted=wanted[:20]+unpack_selected_record(raw,cap)
        u.mem_write(0x02000000,seed);u.mem_write(ptr,raw);state=bytearray(16);struct.pack_into('<I',state,4,ptr);state[8]=selector;u.mem_write(ctx,bytes(state))
        before=bytes(u.mem_read(0x02000000,0x40000))
        if execute(0x0803A1C2,[],0x0803A1E8,140,True)!=int(valid):raise ValueError('caller import result')
        check(before,[(ed,wanted)],140);stats['caller_imports']+=1;stats['caller_rejections']+=not valid
        if commit:
            before=bytes(u.mem_read(0x02000000,0x40000))
            if execute(0x08F06000,[ed+20,ptr,76|len(raw)<<16,0x09000000],stop,140)!=len(raw):raise ValueError('recommit result')
            check(before,[(ptr,raw)],140);stats['CPU_recommits']+=1
    def packed(words,cap):return pack_surface(bytes([len(words),cap,0,255])+struct.pack('<10H',*(tuple(words)+(65535,)*(10-len(words)))))
    for row in native['rows']:
        cap=row['capacity']
        for words in ([229],[0]*(cap-1)+[11171],[0x809B,0x8100]):run(row,packed(words,cap),commit=True)
        good=packed([229],cap)
        for raw in (bytes(len(good)),b'\x80'+b'\xFF'*(len(good)-2)+b'\xE5',good[:-1]+b'\x00',good[:1]+b'\xA4\x2B'+good[3:]):run(row,raw,False)
    row=next(r for r in native['rows'] if r['descriptor']==16)
    for rank in range(11172):
        run(row,packed([0]*3+[rank],4),commit=True);stats['syllable_reentries']+=1
        if rank%2048==0:print('reentry syllable',rank,flush=True)
    # Adapter rejection must preserve even UI/destination bytes, not just compact.
    for cap in (0,11,255,4):
        for ptr in (ed-9,ed-1,ed,ed+16,ed+20,ed+95,0x01FFFFFF,0x0203FFF9,0xFFFFFFFF):
            ui=bytearray(initialize(struct.pack('<4I',4,33,0x020010A6,0)));ui[4]=cap;struct.pack_into('<I',ui,16,ptr)
            u.mem_write(0x02000000,seed);u.mem_write(ed,bytes(ui));before=bytes(u.mem_read(0x02000000,0x40000))
            if execute(0x08302000,[ptr],stop,132)!=0:raise ValueError('unsafe adapter accepted')
            check(before,[],132);stats['adapter_rejections']+=1
    u.mem_write(ed,initialize(struct.pack('<4I',4,33,0x020010A6,0)));before=bytes(u.mem_read(0x02000000,0x40000))
    if execute(0x08302000,[0x020010A7],stop,132)!=0:raise ValueError('wrong destination accepted')
    check(before,[],132);stats['adapter_rejections']+=1
    names=('hangul_keyboard_import_shim.py','bench_keyboard_reentry.py','hangul_mixed_editor_init.py','hangul_mixed_editor_init_shim.py','hangul_mixed_record.py')
    report=dict(id='exe45.hangul-keyboard.reentry-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=native['current_rom_sha256'],caller_selected_mixed_format_required=True,
        no_HOST_rewrite_between_import_and_recommit=True,counts=stats,dynamic_heading_modeled_calls=heading_calls[0],
        caller_stack_bytes=140,import_adapter_nested_stack_bytes=132,ISA=isas,fixture_BLs=patches,
        dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in names},artifacts={n:sha(b) for n,b in blobs.items()},
        limits=['Original metadata caller window executes with two fixture-only BL replacements; metadata0 heading service modeled. Source/current code guards checked; CPU clone uses source image only.',
                'All11172 complete syllables at final fullcap4 slot reenter and recommit unchanged without HOST editor/record writes between CPU stages. Initial records/setup context are fixtures.',
                'Sixteen coherent descriptor2..17 rows tested, no complete setup caller graph or record writer/consumer/save audit.',
                'Malformed/empty records return0 leaving initialized empty editor. Original caller ignores return: no adopted failure/cancel UX or empty legacy migration.',
                'Explicit new-format selection only; no automatic marker discrimination. Whole-editor overlap rejected. Stack extents are fixture bounds, not actual game/IRQ budget.',
                '08301000/08302000 are not free ROM. No real hook, keypad rendering/interaction, actual Korean pixels, persistence or fresh-load evidence.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,native['current_rom_sha256'])
    print('PASS native caller new init/import/recommit CPU',stats,flush=True)

if __name__=='__main__':main()
