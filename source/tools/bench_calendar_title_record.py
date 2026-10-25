"""Final-title conversion plus native pool registration, CPU clones only."""
import json,struct
from bench_hangul_composer_thumb import *
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from hangul_calendar_title_record import assemble,assemble_commit,convert
from hangul_calendar_bounded_commit import assemble_adapter
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE


def main():
    base=ROOT/'analysis/hangul_keyboard_v1'
    lifetime=base/'calendar_name_lifetime.json'; observed=json.loads(lifetime.read_text(encoding='utf8'))
    if not observed['passed']:raise ValueError('lifetime evidence')
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256'])
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,observed['current_rom_sha256'])
    rom=play.read_bytes(); original=source.read_bytes(); clone=bytearray(rom)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    native=[]
    for a,b in ((0x32EFE,0x32F26),(0x37366,0x3737A)):
        raw=original[a:b]; ins=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('native source')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl':raise ValueError('native Thumb1')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native ISA roundtrip')
        native.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x08308100',0x08032F06)[0])
    if len(patch)!=4 or list(cs.disasm(patch,0x08032F06))[0].op_str!='#0x8308100':raise ValueError('placed BL')
    clone[0x32F06:0x32F0A]=patch
    artifacts={};isas={}
    for name,address,make in (('converter.bin',0x08309000,assemble),('commit.bin',0x08308000,lambda:assemble_commit(0x08308000)),('adapter.bin',0x08308100,assemble_adapter)):
        blob,isa=make();artifacts[name]=blob;isas[name]=isa
        if len(blob)>256:raise ValueError('fixture placement')
        clone[address-0x08000000:address-0x08000000+len(blob)]=blob
    dep=base/'cpu_record_display/report.json';d=json.loads(dep.read_text())
    if not d['passed']:raise ValueError('decoder dependency')
    for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
    for n,h in d.get('artifacts',{}).items():require_hash(dep.parent/n,h)
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(clone)+4095)&~4095);u.mem_write(0x08000000,bytes(clone));u.mem_protect(0x08000000,(len(clone)+4095)&~4095,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08F09000,4096);u.mem_write(0x08F09000,(dep.parent/'helper.bin').read_bytes());u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    pool,stage,ctx,ui,meta=0x02026080,0x02026280,0x02014DD0,0x0200F550,0x02000950
    sp,stop=0x03007EFC,0x0FF00000;writes=[];sounds=[]
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(converter_calls=0,registrations=0,accepted=0,rejected=0,syllable_titles=0,whole_EWRAM_checks=0,CPU_redisplays=0,escaped_payloads=0)
    def hook(cpu,a,n,user):
        if a==0x08000534:
            sounds.append(cpu.reg_read(UC_ARM_REG_R0));cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        elif a==stop:cpu.emu_stop()
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def cpu(start,args,outer=False,stack=44):
        u.mem_write(sp-128,b'\x5A'*128);u.mem_write(sp,struct.pack('<I',stop|1))
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for i,r in enumerate(regs):u.reg_write(r,ui if i==1 else 0x13579000+i)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();sounds.clear()
        u.emu_start(start|1,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp+4*outer or any(u.reg_read(r)!=(ui if i==1 else 0x13579000+i) for i,r in enumerate(regs)):raise ValueError('ABI')
        if bytes(u.mem_read(sp-128,128-stack))!=b'\x5A'*(128-stack):raise ValueError('stack bound')
        return u.reg_read(UC_ARM_REG_R0)
    def check(expected,allowed):
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM isolation')
        if any(not (sp-80<=a and a+n<=sp) and not any(s<=a and a+n<=s+l for s,l in allowed) for a,n in writes):raise ValueError('unexpected write')
        counts['whole_EWRAM_checks']+=1
    def run(raw,cap=10,available=None,out_available=None,dest=None,registration=False,slot=9,counter=0,record_override=None):
        if available is None:available=len(raw)
        width=cap*2+2
        if out_available is None:out_available=width
        record=0x020011F0+slot*32 if record_override is None else record_override
        output=record+10 if registration else 0x02025000 if dest is None else dest
        try:want=convert(raw[:available],cap);valid=1<=available<=41 and out_available>=width and not (pool<output+out_available and output<pool+available)
        except ValueError:want=None;valid=False
        if registration:valid=valid and 0x020011F0<=record<0x020031D0 and (record-0x020011F0)%32==0
        u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(pool,raw)
        # Stale/default or person-only bytes deliberately differ from final pool.
        u.mem_write(stage,bytes.fromhex(observed['default_meal']['stage_untouched']))
        if registration:
            u.mem_write(ctx+44,struct.pack('<I',record));u.mem_write(meta+4,bytes([counter]))
        before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before);allowed=[]
        if valid:expected[output-0x02000000:output-0x02000000+width]=want;allowed.append((output,width))
        if registration:
            at=record-0x02000000
            if valid:expected[at:at+2]=bytes([3,counter]);expected[meta-0x02000000+4]=(counter+1)&255;allowed.extend(((record,2),(meta+4,1)))
            else:
                expected[ui-0x02000000+6]=1;expected[ui-0x02000000+8]=2;allowed.extend(((ui+6,1),(ui+8,1)))
            expected[ui-0x02000000:ui-0x02000000+4]=struct.pack('<I',16);allowed.append((ui,4))
            cpu(0x08032EFE,(),True,68)
            if sounds!=[128 if valid else 127]:raise ValueError('registration sound/failure')
            counts['registrations']+=1
        else:
            result=cpu(0x08309000,(pool,output,out_available<<16|available,cap))
            if result!=(width if valid else 0):raise ValueError(f'converter result {raw.hex()} cap{cap} avail{available}')
            counts['converter_calls']+=1
        check(expected,allowed);counts['accepted' if valid else 'rejected']+=1
        if valid:
            # Execute saved-record decoder without HOST rewriting committed bytes.
            redraw=0x02025200;pre=bytearray(u.mem_read(0x02000000,0x40000))
            # Independent token-length scanner: E5 payload is not a terminator.
            i=0
            while raw[i]!=0xE5:i+=4 if raw[i]==0xF9 else 2 if raw[i]==0xE4 else 1
            stream=raw[:i+1];pre[redraw-0x02000000:redraw-0x02000000+len(stream)]=stream
            result=cpu(0x08F09000,(output,redraw,41<<16|width,cap),stack=80)
            if result!=len(stream):raise ValueError('redisplay length')
            check(pre,[(redraw,len(stream))]);counts['CPU_redisplays']+=1
    for rank in range(11172):
        token=b'\xF9\xFC'+struct.pack('<H',rank)
        run(token*10+b'\xE5',registration=True)
        run(token*6+bytes.fromhex(observed['friend']['activity_suffix_hex']),registration=True)
        counts['syllable_titles']+=2
        if rank%2048==0:print('final-title rank',rank,flush=True)
    for payload in range(256):run(bytes([0xE4,payload,0xE5]),registration=True);counts['escaped_payloads']+=1
    for b in range(228):run(bytes([b,0xE5]))
    for cap in range(1,11):
        for count in (1,cap,cap+1):run(b'\xF9\xFC\xE5\x00'*count+b'\xE5',cap)
    for rank in (11172,11212,65535):run(b'\xF9\xFC'+struct.pack('<H',rank)+b'\xE5',registration=True)
    good=b'\xF9\xFC\xE5\x00'*10+b'\xE5'
    for available in range(41):run(good,available=available)
    for cap in (0,11):run(b'\x01\xE5',cap)
    for raw in (b'\xE5',b'\xE4',b'\xF9',b'\xF9\xFC',b'\xF9\xFC\x00',b'\xF9\xFB\x00\x00\xE5',b'\xE6\xE5',b'\xFF\xE5',b'\x01'*41):run(raw,registration=True)
    for avail in (0,21):run(good,out_available=avail)
    for dest in (pool,pool+1,pool-1):run(good,dest=dest)
    for command in range(0xE6,256):
        if command!=0xF9:run(bytes([command,0xE5]))
    for args in ((0xFFFFFFF0,0x02025000,22<<16|41,10),
                 (pool,0xFFFFFFF0,22<<16|41,10),
                 (pool,0x02025000,22<<16|42,10)):
        u.mem_write(0x02000000,b'\xA7'*0x40000);pre=bytes(u.mem_read(0x02000000,0x40000))
        if cpu(0x08309000,args)!=0:raise ValueError('overflow/oversize accepted')
        check(pre,[]);counts['converter_calls']+=1;counts['rejected']+=1
    for slot in range(255):run(good,registration=True,slot=slot)
    for record in (0,0xFFFFFFFF,0x020011D0,0x020011F1,0x020031D0,stage):run(good,registration=True,record_override=record)
    for counter in (254,255):run(good,registration=True,counter=counter)
    for raw in (bytes.fromhex(observed['default_meal']['pool_name_hex']),bytes.fromhex(observed['friend']['final_title_hex'])):run(raw,registration=True)
    out=base/'cpu_calendar_title_record';out.mkdir(exist_ok=True)
    for name,blob in artifacts.items():(out/name).write_bytes(blob)
    result=dict(id='exe45.hangul-keyboard.final-title-record-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        current_rom_sha256=observed['current_rom_sha256'],source_sha256=profile['sha256'],counts=counts,
        dependencies={'calendar_name_lifetime.json':sha(lifetime.read_bytes()),'cpu_record_display/report.json':sha(dep.read_bytes())},
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_calendar_title_record.py','bench_calendar_title_record.py','hangul_calendar_bounded_commit.py')},
        artifacts={n:sha(blob) for n,blob in artifacts.items()},ISA=isas,native_code=native,
        fixture_hook=dict(offset=0x32F06,expected_hex=rom[0x32F06:0x32F0A].hex(),final_hex=patch.hex()),
        converter_stack_bytes=44,commit_stack_bytes=60,adapter_stack_bytes=68,outer_stack_excluded_bytes=4,
        limits=['Final title is fixture-supplied. Native33014 activity-suffix scanner is still byte-oriented and MUST be coordinated before installation; no claim that native append accepts all Hangul ranks.',
                'Explicit NEW conversion at32F06 only, not persistent format detection. Old-save/version dispatch, other calendar consumers and direct3355A route unresolved.',
                'Native32EFE/37366 metadata and CPU record redisplay executed; sound modeled, placements unadopted. Default/person baseline untouched, no HOST record rewrite before redisplay.',
                'No source/playable/save mutation, new keyboard screen, save/reset/freshload or whole-game/release claim.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,observed['current_rom_sha256'])
    print('PASS final title -> bounded record -> native registration -> CPU redisplay; NOT installed',counts,flush=True)


if __name__=='__main__':main()
