"""Execute native print-buffer handler with CPU-only selected copy replacement."""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
from hangul_dialogue_record_copy import assemble
from hangul_mixed_record import pack_surface
from hangul_mixed_record_display import stream

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';dep=base/'cpu_record_display/report.json';d=read(dep)
    if not d['passed'] or d['rom_integrated']:raise ValueError('record display scope')
    for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
    for n,h in d['artifacts'].items():require_hash(dep.parent/n,h)
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,d['current_rom_sha256']);current=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x517D0,0x5181C),(0x94C,0x956)]:
        raw=rom[a:b]
        if current[a:b]!=raw:raise ValueError('native provider changed')
        ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw):raise ValueError('native code extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native ISA')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    for a,value in [(0x5181C,0x080526D0),(0x518F8,0x02010AC0)]:
        if struct.unpack_from('<I',rom,a)[0]!=value or current[a:a+4]!=rom[a:a+4]:raise ValueError('native literal')
    if struct.unpack_from('<II',rom,0x52750)!=(0x020010A7,9) or current[0x52750:0x52758]!=rom[0x52750:0x52758]:raise ValueError('descriptor16')
    blob,isa=assemble();out=base/'cpu_dialogue_record_copy';out.mkdir(exist_ok=True);(out/'helper.bin').write_bytes(blob)
    if not -0x400000<=0x08300000-(0x08051800+4)<0x400000:raise ValueError('ARMv4T BL range')
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x08300000',0x08051800)[0]);decoded=list(cs.disasm(patch,0x08051800))
    if len(patch)!=4 or len(decoded)!=1 or decoded[0].mnemonic!='bl' or decoded[0].op_str!='#0x8300000' or int.from_bytes(patch[:2],'little')&0xF800!=0xF000 or int.from_bytes(patch[2:],'little')&0xF800!=0xF800 or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+decoded[0].mnemonic+' '+decoded[0].op_str,0x08051800)[0])!=patch:raise ValueError('fixture BL placement')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom));u.mem_write(0x08000000,rom);u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    # Source clone modification at08300000 is fixture-only, not free ROM space.
    u.mem_write(0x08300000,blob)
    for a,b in [(0x08F09000,(dep.parent/'helper.bin').read_bytes())]:
        u.mem_map(a,4096);u.mem_write(a,b);u.mem_protect(a,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
    ctx,script,sp,stop=0x0200FA20,0x02003000,0x03007F00,0x0FF00000
    writes=[];u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(syllables=0,selected_calls=0,rejected_records=0,legacy_comparisons=0,variable_selector_calls=0)
    seed=bytes(range(256))*1024
    def execute(raw,index,slot,patched,variable=False):
        u.mem_write(0x02000000,seed);u.mem_write(0x020010A6,raw)
        u.mem_write(script,bytes([249,12,128 if variable else index]));u.mem_write(ctx+0x4C,struct.pack('<I',index))
        u.mem_write(ctx+0x64,struct.pack('<H',slot));u.mem_write(ctx+5,b'\xFE')
        before=bytearray(u.mem_read(0x02000000,0x40000));dst=0x02010AC0+128*slot
        oldsrc,bound=struct.unpack_from('<II',rom,0x526D0+8*index)
        if patched and index==16:
            try:wanted=stream(raw,4)
            except ValueError:wanted=b'\xE5'
        else:wanted=bytes(u.mem_read(oldsrc,bound))
        expected=bytearray(before);expected[dst-0x02000000:dst-0x02000000+len(wanted)]=wanted
        expected[ctx+5-0x02000000]=255
        struct.pack_into('<H',expected,ctx+0x64-0x02000000,slot+1)
        struct.pack_into('<I',expected,ctx+0x2C-0x02000000,dst)
        struct.pack_into('<I',expected,ctx+0x44-0x02000000,script+3)
        u.mem_write(sp-108,b'\x5A'*108);u.mem_write(0x08051800,patch if patched else rom[0x51800:0x51804]);u.ctl_remove_cache(0x080517D0,0x08051820)
        initial=[0x13579000+i for i in range(13)];initial[4]=script;initial[5]=ctx
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip(regs,initial):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
        try:u.emu_start(0x080517D1,stop,count=20000)
        except Exception as exc:raise ValueError(f'provider execution pc={u.reg_read(UC_ARM_REG_PC):08x} lr={u.reg_read(UC_ARM_REG_LR):08x} cpsr={u.reg_read(UC_ARM_REG_CPSR):08x}') from exc
        final=[u.reg_read(r) for r in regs]
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or final[0]!=1 or final[4]!=dst or final[5:13]!=initial[5:13]:raise ValueError('native provider live-out')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected or bytes(u.mem_read(sp-108,4))!=b'\x5A'*4:raise ValueError('dialogue cache/source/stack identity')
        fields=[(ctx+5,1),(ctx+0x64,2),(ctx+0x2C,4),(ctx+0x44,4),(dst,len(wanted)),(sp-104,104)]
        if any(not any(a>=s and a+n<=s+l for s,l in fields) for a,n in writes):raise ValueError('native provider write bounds')
        return final,u.reg_read(UC_ARM_REG_CPSR),bytes(expected)
    for rank in range(11172):
        surface=bytes([4,4,0,255])+struct.pack('<10H',0,0,0,rank,*([65535]*6));raw=pack_surface(surface)
        execute(raw,16,rank%8,True);stats['syllables']+=1;stats['selected_calls']+=1
    good=pack_surface(bytes([1,4,0,255])+struct.pack('<10H',229,*([65535]*9)))
    for slot in range(8):
        for variable in (False,True):
            execute(good,16,slot,True,variable);stats['selected_calls']+=1;stats['variable_selector_calls']+=variable
            for index in (0,1,2,3,15,17,28,29,30):
                native=execute(good,index,slot,False,variable);new=execute(good,index,slot,True,variable)
                if native!=new:raise ValueError('unchanged descriptor provider ABI/NZCV/memory')
                stats['legacy_comparisons']+=1
    for at in range(10):
        bad=bytearray(good);bad[at]^=255
        execute(bytes(bad),16,0,True);stats['selected_calls']+=1
        try:stream(bytes(bad),4)
        except ValueError:stats['rejected_records']+=1
    report=dict(id='exe45.hangul-keyboard.dialogue-record-copy.v1',passed=True,rom_integrated=False,
        caller_selected_mixed_format_required=True,format_adopted=False,source_sha256=profile['sha256'],current_rom_sha256=d['current_rom_sha256'],
        helper_bytes=len(blob),nested_stack_bytes=92,original_provider_with_helper_stack_bytes=104,counts=stats,ISA=isa,native_code=regions,
        fixture_BL=dict(offset=0x51800,expected_hex=rom[0x51800:0x51804].hex(),fixture_hex=patch.hex(),installed=False),
        selector=dict(source='0x020010A7',record='0x020010A6',bound=9,capacity=4,LR='0x08051805'),
        dependencies={'cpu_record_display':sha(dep.read_bytes())},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_dialogue_record_copy.py','bench_dialogue_record_copy.py')},artifacts={'helper.bin':sha(blob)},
        limits=['Original native printStringBuffer handler executes including variable-index lookup, context buffer/counter and continuation; fixture replaces one BL only in Unicorn.',
                'Helper08300000 overwrites a source-clone range only in Unicorn; NOT free ROM space. Actual expanded-ROM installation needs a verified veneer/long-call plan.',
                'Selected fixed single-record weak-subject descriptor16 only. Gate is not format discrimination and cannot be installed while legacy format remains active.',
                '128byte stride and native cache base are static source facts, not complete cache capacity/lifetime/all-slot/IRQ ownership proof. CPU fixtures cover slots0..7 only.',
                'Malformed selected records emit emptyE5, not adopted player-facing rejection behavior.',
                'Record source and temporary counter untouched. No original refresh replacement, render/font/pacing pixels, save/reload or ROM installation.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,d['current_rom_sha256'])
    print('PASS native dialogue handler -> selected record cache',len(blob),stats,flush=True)

if __name__=='__main__':main()
