"""Actual friend suffix ROM lookup -> native title caller -> commit -> decode.

CPU fixtures only; coordinated caller rejects failed append before confirmation
initialization. No HOST title/record rewrite between stages.
"""
import json,struct
from bench_hangul_composer_thumb import *
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from hangul_calendar_activity import assemble,assemble_adapter,assemble_failure,assemble_caller
from hangul_calendar_title_record import convert
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE


def main():
    base=ROOT/'analysis/hangul_keyboard_v1';deps={}
    observed=json.loads((base/'calendar_name_lifetime.json').read_text(encoding='utf8'))
    for name in ('cpu_calendar_title_record','cpu_record_display'):
        p=base/name/'report.json';d=json.loads(p.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']:raise ValueError('dependency scope')
        for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in d['artifacts'].items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes())
    deps['calendar_name_lifetime.json']=sha((base/'calendar_name_lifetime.json').read_bytes())
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,observed['current_rom_sha256']);rom=play.read_bytes();clone=bytearray(rom)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    # Native32AA8 uses32AB6 halfword script offsets; use actual patched literal,
    # not the stale original archive or a hard-coded translated suffix address.
    archive=int.from_bytes(rom[0x32AD8:0x32ADC],'little')
    script=observed['friend']['activity_suffix_script'];archive_offset=archive-0x08000000
    delta=int.from_bytes(rom[archive_offset+2*script:archive_offset+2*script+2],'little')
    suffix_address=archive+delta;suffix=bytes.fromhex(observed['friend']['activity_suffix_hex'])
    if rom[suffix_address-0x08000000:suffix_address-0x08000000+len(suffix)]!=suffix:raise ValueError('actual suffix lookup')
    ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);native=[];patches=[]
    for a,b in ((0x33014,0x33052),(0x32E22,0x32E38),(0x32EFE,0x32F26),(0x37366,0x3737A),
                (0x32DD6,0x32DEE),(0x32F2C,0x32F7C),(0x322CC,0x322D8),
                (0x30E82,0x30EAA),(0x35C84,0x35C8A)):
        raw=original[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('native source scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl':raise ValueError('native Thumb1 scope')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native roundtrip')
        native.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    for offset,length,target in ((0x3302A,18,0x0830A200),(0x32E22,4,0x0830A280),(0x32F06,4,0x08308100)):
        final=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #'+hex(target),0x08000000+offset)[0])+bytes.fromhex('c046')*((length-4)//2)
        if len(final)!=length or list(cs.disasm(final[:4],0x08000000+offset))[0].op_str!='#'+hex(target):raise ValueError('placed BL')
        patches.append(dict(offset=offset,expected_hex=rom[offset:offset+length].hex(),final_hex=final.hex()));clone[offset:offset+length]=final
    # Extend only function return into its verified zero alignment halfword;
    # original literals start33054. No moved PC-relative source instructions.
    if original[0x33050:0x33054]!=bytes.fromhex('f0bd0000') or rom[0x33050:0x33054]!=original[0x33050:0x33054]:raise ValueError('success tail guard')
    final,tail_isa=assemble_verified('movs r0, #1\npop {r4, r5, r6, r7, pc}\n',0x08033050,{})
    if len(final)!=4:raise ValueError('success tail length')
    patches.append(dict(offset=0x33050,expected_hex=rom[0x33050:0x33054].hex(),final_hex=final.hex()));clone[0x33050:0x33054]=final
    artifacts={};isas={}
    for n,a in (('converter.bin',0x08309000),('commit.bin',0x08308000),('adapter.bin',0x08308100)):
        blob=(base/'cpu_calendar_title_record'/n).read_bytes();clone[a-0x08000000:a-0x08000000+len(blob)]=blob
    for name,a,make in (('activity.bin',0x0830A000,lambda:assemble(suffix_address,len(suffix))),('activity_adapter.bin',0x0830A200,assemble_adapter),('failure_tail.bin',0x0830A240,assemble_failure),('caller.bin',0x0830A280,assemble_caller)):
        blob,isa=make();artifacts[name]=blob;isas[name]=isa
        if len(blob)>512:raise ValueError('fixture placement')
        clone[a-0x08000000:a-0x08000000+len(blob)]=blob
    # Controlled recipe defects / Hangul suffixes use isolated read-only ROM
    # fixtures and independently assembled helpers, never mutate current ROM.
    recipe_fixtures=[b'\xE4\xE5\xE5',b'\xF9\xFC\xE5\x00\xE5',b'\x01\xE5\x02',b'\xE4',b'\xF9\xFC\x00',b'\xE6\xE5',b'\x01'*5+b'\xE5',b'\xF9\xFC\x00\x00'*5+b'\xE5']
    fixture_helpers=[]
    for i,raw in enumerate(recipe_fixtures):
        addr=0x0830A400+i*256;src=0x0830B000+i*64
        blob,isa=assemble(src,len(raw),addr);name=f'fixture_{i}.bin';artifacts[name]=blob;isas[name]=isa
        clone[addr-0x08000000:addr-0x08000000+len(blob)]=blob;clone[src-0x08000000:src-0x08000000+len(raw)]=raw
        fixture_helpers.append((addr,raw))
    # Native32EFE assumes caller push{lr}; verified Thumb1 veneer supplies it.
    veneer,isa=assemble_verified('push {lr}\nldr r3, entry\nbx r3\n',0x0830C000,dict(entry=0x08032EFF))
    clone[0x30C000:0x30C000+len(veneer)]=veneer
    artifacts['registration_veneer.bin']=veneer;isas['registration_veneer.bin']=isa
    veneer,isa=assemble_verified('push {lr}\nldr r3, entry\nbx r3\n',0x0830C100,dict(entry=0x08032E23))
    clone[0x30C100:0x30C100+len(veneer)]=veneer;artifacts['caller_veneer.bin']=veneer;isas['caller_veneer.bin']=isa
    isas['native_success_tail']=tail_isa
    veneer,isa=assemble_verified('push {lr}\nldr r3, entry\nbx r3\n',0x0830C200,dict(entry=0x08030E83))
    clone[0x30C200:0x30C200+len(veneer)]=veneer;artifacts['parent_veneer.bin']=veneer;isas['parent_veneer.bin']=isa
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(clone)+4095)&~4095);u.mem_write(0x08000000,bytes(clone));u.mem_protect(0x08000000,(len(clone)+4095)&~4095,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08F09000,4096);u.mem_write(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes());u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    pool,stage,ctx,ui,meta,record=0x02026080,0x02026280,0x02014DD0,0x0200F550,0x02000950,0x02001310
    selector_address=int.from_bytes(rom[0x35CA0:0x35CA4],'little')
    if not 0x02000000<=selector_address<=0x0203FFF6:raise ValueError('selector RAM extent')
    exit_literals=[]
    for offset,extent in ((0x32E0C,4),(0x32DF0,4),(0x32DF4,24),(0x35CA0,4)):
        raw=original[offset:offset+extent]
        if rom[offset:offset+extent]!=raw:raise ValueError('native exit literal source')
        exit_literals.append(dict(offset=offset,bytes=extent,sha256=sha(raw)))
    if int.from_bytes(rom[0x32E0C:0x32E10],'little')!=ui or int.from_bytes(rom[0x32DF0:0x32DF4],'little')!=0x08032DF4 or struct.unpack_from('<II',rom,0x32E04)!=(0x08032F2D,0x08032F75):raise ValueError('native exit dispatch targets')
    # The close-script archive is intentionally relocated by the product build,
    # unlike native state table/RAM literals. It must select the same current
    # activity archive, not match the old source pointer.
    if rom[0x32338:0x3233C]!=rom[0x32AD8:0x32ADC] or original[0x32338:0x3233C]!=original[0x32AD8:0x32ADC]:raise ValueError('close/activity archive agreement')
    exit_literals.append(dict(offset=0x32338,bytes=4,source_sha256=sha(original[0x32338:0x3233C]),current_sha256=sha(rom[0x32338:0x3233C]),relocated_archive=archive))
    sp,stop=0x03007EFC,0x0FF00000;writes=[];calls=[];parent_results=[]
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(routes=0,accepted=0,rejected=0,syllable_routes=0,embedded_E5_ranks=0,native_headings=0,registrations=0,CPU_redisplays=0,whole_EWRAM_checks=0,other_type_routes=0,
                rejected_native_exit_frames=0,rejected_native_returns=0,parent_edit_returns=0,parent_selection_returns=0)
    def hook(cpu,a,n,user):
        if a in (0x08029164,0x080554A4,0x08000534,0x08032E60,0x08032FD4,0x0804F7B6):
            if a==0x0804F7B6 and (cpu.reg_read(UC_ARM_REG_R1)!=9 or cpu.reg_read(UC_ARM_REG_R0)!=int.from_bytes(rom[0x32338:0x3233C],'little')):raise ValueError('native close-script selection')
            calls.append((a,cpu.reg_read(UC_ARM_REG_R0)));cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        elif a==0x08030E86:parent_results.append(cpu.reg_read(UC_ARM_REG_R0))
        elif a==0x08035C84:
            if cpu.reg_read(UC_ARM_REG_R0)!=8:raise ValueError('parent selector query')
            calls.append((a,8))  # Execute the real native getter; do not model it.
        elif a==stop:cpu.emu_stop()
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    def cpu(start,args=(),stack=208,r5_context=None):
        u.mem_write(sp-224,b'\x5A'*224);u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved_r5=ui if r5_context is None else r5_context
        for i,r in enumerate(regs):u.reg_write(r,saved_r5 if i==1 else 0x13579000+i)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();calls.clear();parent_results.clear()
        u.emu_start(start|1,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=(saved_r5 if i==1 else 0x13579000+i) for i,r in enumerate(regs)):raise ValueError('ABI')
        if bytes(u.mem_read(sp-224,224-stack))!=b'\x5A'*(224-stack):raise ValueError('stack bound')
        return u.reg_read(UC_ARM_REG_R0)
    def check(expected,allowed):
        if bytes(u.mem_read(0x02000000,0x40000))!=expected:raise ValueError('whole EWRAM isolation')
        if any(not(sp-208<=a and a+n<=sp) and not any(s<=a and a+n<=s+l for s,l in allowed) for a,n in writes):raise ValueError('unexpected write')
        counts['whole_EWRAM_checks']+=1
    def run(person,kind=1,helper=None,recipe=suffix,parent_selector=1):
        u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(pool,person);u.mem_write(stage,b'\x01\x9B\xE5'+b'\x55'*19)
        u.mem_write(ctx+44,struct.pack('<I',record));u.mem_write(record+9,bytes([kind]));u.mem_write(meta+4,b'\x00')
        u.mem_write(ui,b'\x00'*16)
        u.mem_write(selector_address+8,bytes([parent_selector]))
        before=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(before)
        try:
            if kind==1:
                convert(person,6)
                i=0
                while person[i]!=0xE5:i+=4 if person[i]==0xF9 else 2 if person[i]==0xE4 else 1
                title=person[:i]+recipe;want=convert(title,10)
                j=0
                while title[j]!=0xE5:j+=4 if title[j]==0xF9 else 2 if title[j]==0xE4 else 1
                if j+1!=len(title):raise ValueError('suffix trailing data')
            else:title=person;want=convert(title,10)
            valid=True
        except (ValueError,IndexError):valid=False
        allowed=[]
        if valid and kind==1:expected[pool-0x02000000:pool-0x02000000+len(title)]=title;allowed.append((pool,len(title)))
        if not valid and helper is None:
            expected[ui-0x02000000+6]=1;expected[ui-0x02000000+8]=2;allowed.extend(((ui+6,1),(ui+8,1)))
        if helper is None:
            if valid:
                expected[ui-0x02000000]=4;expected[ui-0x02000000+4]=255;expected[ui-0x02000000+5]=24;allowed.extend(((ui,1),(ui+4,2)))
            else:expected[ui-0x02000000:ui-0x02000000+4]=struct.pack('<I',16);allowed.append((ui,4))
        result=cpu(0x0830C100 if helper is None else helper,(pool,),208 if helper is None else 168)
        if helper is None:
            if [a for a,v in calls]!=[0x08029164]+([0x080554A4,0x08032E60] if valid else []):raise ValueError('heading/confirmation failure route')
            counts['native_headings']+=valid
        elif result!=(len(title) if valid else 0):raise ValueError('helper result')
        check(expected,allowed);counts['routes']+=1;counts['accepted' if valid else 'rejected']+=1
        if not valid:
            if helper is None:
                # Uninterrupted native dispatch16 -> native animation ->20 ->
                # return2; do not HOST initialize animation or completion flags.
                frame=0
                while True:
                    expected=bytearray(u.mem_read(0x02000000,0x40000));at=ui-0x02000000
                    state=expected[at];first=state==16 and expected[at+2]==0
                    if state==16:
                        expected[at+2]=4
                        pos=expected[at+4]+expected[at+5]
                        if pos>=255:pos=255;expected[at:at+2]=b'\x14\x00'
                        else:
                            speed=expected[at+5]+1
                            if speed<=24:expected[at+5]=speed
                        expected[at+4]=pos;expected[at+10:at+12]=struct.pack('<H',pos)
                    elif state==20:
                        expected[at+7]=2;ct=ctx-0x02000000
                        expected[ct+1]=28 if parent_selector else 20;expected[ct+10]=1;expected[ct+2:ct+4]=b'\x00\x00'
                    else:raise ValueError('unexpected failed-append continuation state')
                    result=cpu(0x0830C200,stack=20,r5_context=ctx)
                    expected_calls=([0x0804F7B6] if first else [])+[0x08032FD4]+([0x08035C84] if state==20 else [])
                    if [a for a,v in calls]!=expected_calls:raise ValueError('native cancellation services')
                    if parent_results!=[2 if state==20 else 0] or result!=0:raise ValueError('parent cancellation return')
                    check(expected,[(ui,16),(ctx+1,3),(ctx+10,1)]);frame+=1;counts['rejected_native_exit_frames']+=1
                    if state==20:break
                    if frame>32:raise ValueError('native cancellation did not complete')
                if frame!=25:raise ValueError('native failure exit frame count')
                counts['rejected_native_returns']+=1
                counts['parent_edit_returns' if parent_selector else 'parent_selection_returns']+=1
            return
        # Keep pool/person/committed bytes untouched between CPU stages.
        pre=bytearray(u.mem_read(0x02000000,0x40000));expected=bytearray(pre)
        expected[record-0x02000000+10:record-0x02000000+32]=want;expected[record-0x02000000:record-0x02000000+2]=b'\x03\x00';expected[meta-0x02000000+4]=1
        expected[ui-0x02000000:ui-0x02000000+4]=struct.pack('<I',16)
        # Verified caller veneer pushes LR; native final pop restores original SP.
        cpu(0x0830C000,stack=72)
        if calls!=[(0x08000534,128)]:raise ValueError('native registration')
        check(expected,[(record,2),(record+10,22),(meta+4,1),(ui,4)]);counts['registrations']+=1
        redraw=0x02025200;expected=bytearray(u.mem_read(0x02000000,0x40000));expected[redraw-0x02000000:redraw-0x02000000+len(title)]=title
        if cpu(0x08F09000,(record+10,redraw,41<<16|22,10),80)!=len(title):raise ValueError('CPU redisplay length')
        check(expected,[(redraw,len(title))]);counts['CPU_redisplays']+=1
    for rank in range(11172):
        token=b'\xF9\xFC'+struct.pack('<H',rank);run(token*6+b'\xE5');counts['syllable_routes']+=1
        counts['embedded_E5_ranks']+=0xE5 in struct.pack('<H',rank)
        if rank%2048==0:print('activity append rank',rank,flush=True)
    for n in range(1,7):run(b'\xF9\xFC\xE5\x00'*n+b'\xE5')
    for payload in range(256):run(bytes([0xE4,payload,0xE5]))
    for raw in (b'\xE5',b'\xE4',b'\xF9\xFC\x00',b'\xF9\xFC\xA4\x2B\xE5',b'\xF9\xFC\x00\x00'*7+b'\xE5',b'\x01'*25,b'\xE6\xE5',b'\xF9\xFB\x00\x00\xE5'):run(raw)
    run(b'\xE5',parent_selector=0)
    for kind in (0,2,3):run(bytes.fromhex(observed['default_meal']['pool_name_hex']),kind);counts['other_type_routes']+=1
    for helper,recipe in fixture_helpers:run(b'\xF9\xFC\xE5\x00'*6+b'\xE5',helper=helper,recipe=recipe)
    run(b'\x9B\xE5')
    out=base/'cpu_calendar_activity';out.mkdir(exist_ok=True)
    for name,blob in artifacts.items():(out/name).write_bytes(blob)
    result=dict(id='exe45.hangul-keyboard.friend-activity-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
        source_sha256=profile['sha256'],current_rom_sha256=observed['current_rom_sha256'],counts=counts,
        dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('hangul_calendar_activity.py','bench_calendar_activity.py')},
        artifacts={n:sha(blob) for n,blob in artifacts.items()},ISA=isas,native_code=native,fixture_writes=patches,
        suffix=dict(archive=archive,script=script,address=suffix_address,extent=len(suffix),hex=suffix.hex()),helper_stack_bytes=168,native_append_stack_bytes=196,caller_stack_bytes=208,
        no_HOST_title_or_record_rewrite_between_append_registration_redisplay=True,
        native_selector_address=selector_address,
        native_exit_literals=exit_literals,
        limits=['CPU friend recipe only: native33014 dispatch, bounded suffix append, native32EFE/37366 metadata and record decoder. Sprite/heading/sound modeled; no actual pixels or controller interaction.',
                'Coordinated caller32E22 rejects append failure, skips heading/confirmation initializer32E60. Native32DD6 dispatch16/20 then parent30E82 and actual35C84 getter route cancel2 to edit subtype28 or selection20 without HOST UI/pool rewriting. Script service/rendering modeled; actual controller screen/cancellation still unresolved.',
                'Actual source suffix script0x45 still contains original text; this stage fixes byte/token handling, not its prose translation. Full suffix recipe inventory and semantic translation pending.',
                'Legacy/new save version, all consumers/direct3355A, code/RAM/IRQ adoption, ROM hook, actual Korean keyboard screenshot and save/reset/freshload unresolved. No source/playable/save mutation or release claim.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,observed['current_rom_sha256'])
    print('PASS activity -> bounded registration -> CPU redisplay; NOT installed',counts,flush=True)


if __name__=='__main__':main()
