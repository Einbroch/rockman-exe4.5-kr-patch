"""Canonical stage -> display pool -> two bounded native registration routes.

No HOST rewriting canonical/pool between decode and registration. Explicit NEW
session premise only; legacy dispatch, stage lifetime and persistence pending.
"""
import json,struct
from bench_hangul_composer_thumb import *
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from hangul_calendar_bounded_commit import assemble,assemble_adapter
from hangul_mixed_record import unpack_selected_record
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE


def main():
    base=ROOT/'analysis/hangul_keyboard_v1'
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity=json.loads((base/'cpu_calendar_native_registration/report.json').read_text())['current_rom_sha256'];require_hash(play,identity);rom=play.read_bytes()
    deps={}
    for name in ('cpu_mixed_record_import','cpu_record_display'):
        p=base/name/'report.json';d=json.loads(p.read_text())
        if not d['passed'] or d.get('rom_integrated',False):raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes())
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);scopes=[]
    for a,b in ((0x32EFE,0x32F26),(0x3354A,0x335AC),(0x37366,0x3739A)):
        raw=original[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('native source scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl':raise ValueError('Thumb1 native scope')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native roundtrip')
        scopes.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    patches=[];clone=bytearray(rom);artifacts={};isas={}
    for offset,length,target in ((0x32F06,4,0x08308100),(0x3354A,20,0x08308200)):
        final=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #'+hex(target),0x08000000+offset)[0])+bytes.fromhex('c046')*((length-4)//2)
        if len(final)!=length or list(cs.disasm(final[:4],0x08000000+offset))[0].op_str!='#'+hex(target):raise ValueError('final BL placement')
        patches.append(dict(offset=offset,expected_hex=rom[offset:offset+length].hex(),final_hex=final.hex()));clone[offset:offset+length]=final
    for name,address,make in (('copier.bin',0x08308000,assemble),('pool_adapter.bin',0x08308100,assemble_adapter),('direct_adapter.bin',0x08308200,lambda:assemble_adapter(True))):
        blob,isa=make()
        if len(blob)>256:raise ValueError('fixture code slot')
        clone[address-0x08000000:address-0x08000000+len(blob)]=blob;artifacts[name]=blob;isas[name]=isa
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(clone)+4095)&~4095);u.mem_write(0x08000000,bytes(clone))
    for name,address in (('cpu_mixed_record_import',0x08F05000),('cpu_record_display',0x08F09000)):
        u.mem_map(address,4096);u.mem_write(address,(base/name/'helper.bin').read_bytes());u.mem_protect(address,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    stage,pool,ctx,metadata,sp,stop=0x02026280,0x02026080,0x02014DD0,0x02000950,0x03007EFC,0x0FF00000
    ui=0x0200F550  # Observed native r5 is NOT record-pointer context02014DD0.
    calls=[];writes=[];mode=[1];boundary=[stop]
    def hook(cpu,a,n,user):
        if a in (0x08000534,0x08035C84,0x08037440):
            calls.append((a,cpu.reg_read(UC_ARM_REG_R0)))
            if a==0x08035C84:
                if cpu.reg_read(UC_ARM_REG_R0)!=2:raise ValueError('selector request')
                cpu.reg_write(UC_ARM_REG_R0,mode[0])
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        elif a==boundary[0]:cpu.emu_stop()
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(routes=0,accepted=0,rejected=0,display_decodes=0,whole_EWRAM_checks=0,syllable_routes=0,arena_slots=0,direct_mode1=0,direct_mode2=0,counter_wraps=0)
    def cpu(start,args,outer=False):
        saved=[ui if i==1 else 0x13579000+i for i in range(8)]
        u.mem_write(sp-232,b'\x5A'*232);u.mem_write(sp,struct.pack('<I',stop|1));u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip(regs,saved):u.reg_write(r,v)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);calls.clear();writes.clear()
        u.emu_start(start|1,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp+4*outer or any(u.reg_read(r)!=v for r,v in zip(regs,saved)):raise ValueError('ABI')
        if bytes(u.mem_read(sp-232,4))!=b'\x5A'*4:raise ValueError('stack bound')
    def run(raw,direct=False,selector=1,slot=9,counter=0,record_override=None,field_override=None,do_decode=True):
        record=0x020011F0+slot*32 if record_override is None else record_override
        field=record+10 if field_override is None else field_override
        try:unpack_selected_record(raw,10);valid=True
        except ValueError:valid=False
        valid=valid and 0x020011F0<=record<0x020031D0 and (record-0x020011F0)%32==0 and field==record+10
        u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(stage,raw);u.mem_write(ctx+0x2C,struct.pack('<I',record));u.mem_write(metadata+4,bytes([counter]));u.mem_write(metadata+5,bytes([counter]))
        if valid and do_decode:
            before=bytearray(u.mem_read(0x02000000,0x40000))
            cpu(0x08F09000,(stage,pool,41<<16|22,10));length=u.reg_read(UC_ARM_REG_R0)
            if not 1<=length<=41:raise ValueError('decode result')
            # Expectation is independently constructed from fixture identities.
            count=raw[0]-128;words=struct.unpack_from('<10H',raw,1);stream=bytearray()
            for word in words[:count]:
                if word<11172:stream+=b'\xF9\xFC'+struct.pack('<H',word)
                elif word<=0x80E3:stream+=bytes([word&255])
                else:stream+=bytes([0xE4,word&255])
            stream+=b'\xE5';before[pool-0x02000000:pool-0x02000000+len(stream)]=stream
            if length!=len(stream) or bytes(u.mem_read(0x02000000,0x40000))!=before:raise ValueError('canonical->display isolation')
            counts['display_decodes']+=1;counts['whole_EWRAM_checks']+=1
        before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before);mode[0]=selector
        at=record-0x02000000
        if valid:
            expected[at+10:at+32]=raw;expected[at:at+2]=bytes([3 if not direct else 53 if selector==1 else 5,counter])
            if direct and selector==1:expected[at+9]=1
            expected[metadata-0x02000000+(5 if direct else 4)]=(counter+1)&255
        else:expected[ui-0x02000000+8]=2;expected[ui-0x02000000+6]=1
        if field_override is None:
            expected[ui-0x02000000:ui-0x02000000+4]=struct.pack('<I',16)
            cpu(0x0803354A if direct else 0x08032EFE,(),True)
            sounds=[v for a,v in calls if a==0x08000534]
            if sounds!=[128 if valid else 127] or any(a==0x08035C84 for a,v in calls)!=(direct and valid):raise ValueError('success/failure routing')
            if direct and valid:counts['direct_mode'+str(selector)]+=1
        else:
            # Direct helper boundary tests; no metadata/sound/state transition.
            expected=before;cpu(0x08308000,(pool,field))
            if u.reg_read(UC_ARM_REG_R0)!=0:raise ValueError('invalid field accepted')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('commit whole EWRAM')
        allowed=[(sp-228,228),(ui,4)]
        if valid:allowed +=[(record,2),(record+10,22),(metadata+(5 if direct else 4),1)]+([(record+9,1)] if direct and selector==1 else [])
        else:allowed +=[(ui+6,1),(ui+8,1)]
        if any(not any(s<=a and a+n<=s+l for s,l in allowed) for a,n in writes):raise ValueError('commit writes')
        counts['routes']+=1;counts['accepted' if valid else 'rejected']+=1;counts['whole_EWRAM_checks']+=1;counts['counter_wraps']+=valid and counter==255
    for rank in range(11172):
        raw=b'\x8A'+struct.pack('<H',rank)*10+b'\xE5'
        run(raw);run(raw,True,1+rank%2);counts['syllable_routes']+=2
        if rank%2048==0:print('bounded canonical commit rank',rank,flush=True)
    good=b'\x8A'+struct.pack('<H',229)*10+b'\xE5'
    for slot in range(255):run(good,slot=slot);counts['arena_slots']+=1
    for direct in (False,True):
        for count in range(1,11):
            for word in (0,11171,0x80E3,0x81E5):run(bytes([128+count])+struct.pack('<H',word)*count+b'\xFF\xFF'*(10-count)+b'\xE5',direct)
        for j in range(22):
            raw=bytearray(good);raw[j]^=255;run(bytes(raw),direct)
        for record in (0,0xFFFFFFFF,0x020011D0,0x020011F1,0x020031D0,stage):run(good,direct,record_override=record)
        for counter in (254,255):run(good,direct,counter=counter)
    for field in (0,0xFFFFFFFF,0x02001319,0x0200131B,stage,pool):run(good,field_override=field,do_decode=False)
    out=base/'cpu_calendar_bounded_commit';out.mkdir(exist_ok=True)
    for name,blob in artifacts.items():(out/name).write_bytes(blob)
    result=dict(id='exe45.hangul-keyboard.bounded-canonical-commit-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=counts,native_code=scopes,fixture_writes=patches,
        helper_stack_bytes=220,adapter_nested_stack_bytes=228,outer_stack_excluded_bytes=4,ISA=isas,
        dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_calendar_bounded_commit.py','bench_calendar_bounded_commit.py')},artifacts={n:sha(v) for n,v in artifacts.items()},
        explicit_new_session_required=True,no_HOST_canonical_pool_rewrite_between_decode_and_registration=True,
        limits=['Selected NEW cap10 session only. Canonical stage lifetime/IRQ/other writers, default/import/preload, legacy/new persistent discriminator and save ABI NOT adopted. Stage is fixture-owned, not proved available throughout real menu routes.',
                'Both native registration paths execute copy adapters and actual37366/3737A/37386 metadata. Sound/selector/37440 post-registration update modeled. Direct selector0 RTC/config route NOT exercised; selector1/2 only.',
                'All11172 repeated-rank ten-syllable names decoded into separate display pool then registered from canonical stage with no HOST rewrites between. Full EWRAM checks preserve cache/canonical/neighbor; invalid source/destination skips registration. No natural UI/error dialog clearing or whole-game memory claim.',
                'CPU-only code clones at unadopted ROM placements. No source/playable/save mutation, actual keyboard screenshot, save/reset/freshload, old-save compatibility or release claim.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS bounded canonical commit CPU; NOT installed/persistent',counts,flush=True)


if __name__=='__main__':main()
