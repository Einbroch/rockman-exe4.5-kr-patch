"""Native list dispatcher -> initialization -> guarded prefill, CPU only.

Graphics/audio services modeled. No installed ROM, pixels or save/reload claim.
"""
import json, re, struct
from bench_hangul_composer_thumb import *
from extended_dialogue import Ks,Cs,KS_ARCH_ARM,KS_MODE_THUMB,CS_ARCH_ARM,CS_MODE_THUMB
from hangul_calendar_prefill_guard import assemble_adapter,assemble_guard
from hangul_calendar_versioned_record import pack,read
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE


def main(reentry=False):
    base=ROOT/'analysis/hangul_keyboard_v1';dependencies={};reports={}
    for name in ('cpu_calendar_versioned_prefill','cpu_calendar_versioned_record','cpu_calendar_title_record','cpu_record_display'):
        p=base/name/'report.json';d=json.loads(p.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']:raise ValueError('dependency scope')
        for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in d['artifacts'].items():require_hash(p.parent/n,h)
        dependencies[name+'/report.json']=sha(p.read_bytes());reports[name]=d
    def check_ip(value):
        if isinstance(value,dict):
            if 'operands' in value and re.search(r'\b(ip|r12)\b',value['operands']):raise ValueError('transient status clobber')
            for v in value.values():check_ip(v)
        elif isinstance(value,list):
            for v in value:check_ip(v)
    for name in ('cpu_calendar_versioned_record','cpu_calendar_title_record','cpu_record_display'):
        check_ip(reports[name]['ISA'])
    if reentry:
        p=base/'cpu_calendar_prefill_guard/report.json';d=json.loads(p.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']:raise ValueError('guard regression dependency')
        for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in d['artifacts'].items():require_hash(p.parent/n,h)
        dependencies['cpu_calendar_prefill_guard/report.json']=sha(p.read_bytes())
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    identity=reports['cpu_calendar_versioned_prefill']['current_rom_sha256']
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(play,identity);rom=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);native=[]
    for a,b in ((0x30F0C,0x30F6E),(0x330C6,0x330DE),(0x33100,0x33152),(0x3317C,0x3318A),
                (0x332F8,0x33334),(0x33334,0x3338E),(0x33398,0x333D4),
                (0x3739A,0x373FA),(0x37404,0x3741E),(0x32AA8,0x32AD8),(0x35C84,0x35C8A),
                (0x3A3B0,0x3A3BC),(0x90C,0x926),(0xEC144,0xEC148),(0x330C0,0x330C6)):
        raw=original[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('native boundaries/source')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl':raise ValueError('native Thumb1')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('native roundtrip')
            if re.search(r'\b(ip|r12)\b',i.op_str):raise ValueError('native transient status clobber')
        native.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    artifacts={};isas={};clone=bytearray(rom)
    for name,address,make in (('adapter.bin',0x0830E000,assemble_adapter),('guard.bin',0x0830E100,assemble_guard)):
        blob,isa=make();artifacts[name]=blob;isas[name]=isa
        clone[address-0x08000000:address-0x08000000+len(blob)]=blob
    hooks=list(reports['cpu_calendar_versioned_prefill']['fixture_hooks'])
    ins=list(cs.disasm(rom[0x33114:0x33118],0x08033114))
    if len(ins)!=1 or ins[0].op_str!='#0x8033334':raise ValueError('native prefill caller')
    patch=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x830e100',0x08033114)[0])
    if len(patch)!=4 or list(cs.disasm(patch,0x08033114))[0].op_str!='#0x830e100':raise ValueError('placed caller')
    hooks.append(dict(offset=0x33114,expected_hex=rom[0x33114:0x33118].hex(),final_hex=patch.hex()))
    for h in hooks:
        at=h['offset'];expected=bytes.fromhex(h['expected_hex'])
        if rom[at:at+len(expected)]!=expected:raise ValueError('hook source')
        clone[at:at+len(expected)]=bytes.fromhex(h['final_hex'])
    for address,path in ((0x0830D000,base/'cpu_calendar_versioned_record/writer.bin'),
                         (0x0830D200,base/'cpu_calendar_versioned_record/reader.bin'),
                         (0x08309000,base/'cpu_calendar_title_record/converter.bin')):
        raw=path.read_bytes();clone[address-0x08000000:address-0x08000000+len(raw)]=raw
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    extent=(len(clone)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,bytes(clone))
    u.mem_map(0x08F09000,4096);u.mem_write(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes());u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03007000,4096);u.mem_map(0x0FF00000,4096)
    pool,arena,meta,date,ui,ctx,gfx,sp,stop=0x02026080,0x020011F0,0x02000950,0x02014DEC,0x0200F550,0x02000020,0x02000100,0x03007EFC,0x0FF00000
    parent=0x02014DD0
    services={0x08055C3E,0x08029164,0x080554A4,0x08035EF0,0x0803438A,0x080016F4,0x080016D8,0x08034364,0x08000534,0x0802871E}
    if struct.unpack_from('<I',rom,0x3A418)[0]!=ui or struct.unpack_from('<I',rom,0x928)[0]!=0x05000000:raise ValueError('reset literals')
    writes=[];calls=[];prefill_calls=[];returned=[];cleanup=[];reset_requests=[]
    def hook(cpu,a,n,user):
        if a==stop:cpu.emu_stop();return
        if a==0x080EC144:
            src=cpu.reg_read(UC_ARM_REG_R0);dest=cpu.reg_read(UC_ARM_REG_R1);control=cpu.reg_read(UC_ARM_REG_R2)
            if not(sp-160<=src<=sp-4) or dest!=ui or control!=0x05000004 or bytes(cpu.mem_read(src,4))!=bytes(4):raise ValueError('modeled reset BIOS admission')
            reset_requests.append((dest,16));cpu.mem_write(dest,bytes(16));writes.append((dest,16))
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1);return
        if a==0x08030F44:returned.append((cpu.reg_read(UC_ARM_REG_R0),bool(cpu.reg_read(UC_ARM_REG_CPSR)&(1<<30))))
        if a==0x0802871E:cleanup.append((cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)))
        if a in (0x08033344,0x0803335A,0x0803336E):prefill_calls.append(a)
        if a in services:
            calls.append((a,cpu.reg_read(UC_ARM_REG_R0)))
            cpu.reg_write(UC_ARM_REG_R0,0);cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    default=bytes.fromhex(reports['cpu_calendar_versioned_prefill']['default']['hex'])
    counts=dict(routes=0,initializer_continued=0,rejected=0,unprotected_failure_advance=0,whole_EWRAM_checks=0,
                initial_entries=0,empty_default_routes=0,reset_requests=0,reentry_cycles=0,writer_repairs=0)
    examples=[]
    def run(fields,mode=0,guarded=True,positions=(0,1,2),filters=None,initial=False,fresh=True):
        u.mem_write(0x08033114,patch if guarded else rom[0x33114:0x33118]);u.ctl_remove_cache(0x08033100,0x08033152)
        if fresh:
            u.mem_write(0x02000000,b'\xA7'*0x40000);u.mem_write(arena,bytes(255*32))
            u.mem_write(meta+5,bytes([len(fields)]));u.mem_write(meta+6,b'\xAA');u.mem_write(date,b'\x01\x02\x03')
            u.mem_write(ui,b'\xA7'*16 if initial else bytes(16))
            if not initial:u.mem_write(ui+6,bytes([mode]))
            u.mem_write(ctx+8,struct.pack('<I',gfx));u.mem_write(0x02014E34,bytes(9))
            u.mem_write(parent,bytes(16));u.mem_write(parent+2,bytes([0 if initial else 4]));u.mem_write(parent+10,bytes([mode]))
            for index,(field,position) in enumerate(zip(fields,positions)):
                flags,day=(4,b'\x01\x02\x03') if filters is None else filters[index]
                u.mem_write(arena+32*position,bytes([flags,index])+day+bytes(5)+field)
        else:
            if not initial or bytes(u.mem_read(parent+2,2))!=bytes(2):raise ValueError('re-entry baseline')
            mode=cpu_mode=bytes(u.mem_read(parent+10,1))[0]
            if cpu_mode not in (0,1):raise ValueError('re-entry mode')
            for field,position in zip(fields,positions):
                if bytes(u.mem_read(arena+32*position+10,22))!=field:raise ValueError('uninterrupted record identity')
        before=bytes(u.mem_read(0x02000000,0x40000));expected=bytearray(before);regions=[]
        def put(a,b):expected[a-0x02000000:a-0x02000000+len(b)]=b;regions.append((a,len(b)))
        found=[i for i in range(len(fields)) if filters is None or filters[i][0]&4 and not filters[i][0]&8 and filters[i][1]==b'\x01\x02\x03']
        empty=initial and not found
        cursor=0;valid=bool(found);visits=[]
        for slot in range(3):
            if empty:break
            index=next((i for i in found if i>=cursor),None)
            if index is None:
                if slot==0:visits.append(0x08033344)
                break
            cursor=index+1;visits.append((0x08033344,0x0803335A,0x0803336E)[slot])
            try:value=read(fields[index])
            except ValueError:valid=False;break
            put(pool+128*slot,value)
            if slot==0:put(pool+128,default);put(pool+256,default)
        if not empty:put(gfx,rom[0x33154:0x33156]);put(gfx+20,bytes(4))
        rejected=guarded and not valid and not empty
        new_ui=bytearray(16) if initial and not empty else bytearray(before[ui-0x02000000:ui-0x02000000+16])
        if initial and not empty:new_ui[6]=mode
        if empty:
            put(pool+128,default);put(pool+256,default);put(parent+50,b'\0');put(parent+1,b'\x3C\0\0')
        elif rejected:
            for slot in range(3):put(pool+128*slot,b'\xE5'+bytes(40))
            new_ui[:4]=struct.pack('<I',20);new_ui[4:9]=bytes([255,24,1,2,2]);new_ui[10:14]=bytes(4)
            put(parent+1,b'\x04\0\0');put(parent+10,b'\x01')
        else:
            if initial:put(parent+2,b'\x04')
            cursor=max(found)+1 if found else 0
            new_ui[0]=4;new_ui[4:6]=bytes([255,24]);new_ui[12]=0 if mode or len(found)>2 else len(found);new_ui[13]=len(found)
            new_ui[10:12]=struct.pack('<H',(-255)&65535 if mode else 255)
        put(ui,bytes(new_ui));put(meta+6,bytes([cursor]))
        u.mem_write(sp-192,b'\x5A'*192);u.mem_write(sp,struct.pack('<I',stop|1));u.reg_write(UC_ARM_REG_CPSR,0x30)
        values=[ctx if r==UC_ARM_REG_R10 else parent if r==UC_ARM_REG_R5 else 0x13579000+i for i,r in enumerate(regs)]
        for r,v in zip(regs,values):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_R12,1);u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear();calls.clear();prefill_calls.clear();returned.clear();cleanup.clear();reset_requests.clear()
        u.emu_start(0x08030F0D,stop,count=100000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,values)):raise ValueError('dispatcher ABI')
        if bytes(u.mem_read(sp-192,32))!=b'\x5A'*32:raise ValueError('stack160 guard')
        actual=bytes(u.mem_read(0x02000000,0x40000))
        if actual!=expected:
            diff=[(hex(0x02000000+i),a,b) for i,(a,b) in enumerate(zip(actual,expected)) if a!=b]
            raise ValueError('whole EWRAM '+str(diff[:16]))
        if any(not(sp-160<=a and a+n<=sp) and not any(s<=a and a+n<=s+l for s,l in regions) for a,n in writes):raise ValueError('write bounds')
        if prefill_calls!=visits:raise ValueError('prefill selection')
        wanted=[] if empty else [0x08055C3E]+([0x08000534] if rejected else [0x08029164]+[0x080554A4]*3+[0x08035EF0])+[0x0803438A,0x080016F4,0x080016D8,0x08034364]+([0x0802871E]*2 if rejected else [])
        if [a for a,v in calls]!=wanted or rejected and (0x08000534,127) not in calls:raise ValueError('feedback/heading dispatch')
        if returned!=([] if empty else [(2 if rejected else 0,not rejected)]) or cleanup!=([(14,79),(14,80)] if rejected else []):raise ValueError('parent return/cancel consumption')
        if reset_requests!=([(ui,16)] if initial and not empty else []):raise ValueError('native reset route')
        counts['routes']+=1;counts['rejected' if rejected else 'initializer_continued']+=1;counts['whole_EWRAM_checks']+=1
        if not guarded and not valid:counts['unprotected_failure_advance']+=1
        counts['initial_entries']+=initial;counts['empty_default_routes']+=empty;counts['reset_requests']+=len(reset_requests)
        if rejected and len(examples)<4:examples.append(dict(field_hex=[f.hex() for f in fields],mode=mode,return_code=2,headings=0,sound=127,pool_empty=True))
    good=pack(b'\xF9\xFC\xE5\0\xE5');bad=good[:-1]+b'\0'
    run([good,bad,good],guarded=False)
    for mode in (0,1):
        for rank in (0,152,229,255,256,11171):
            for length in range(1,11):
                field=pack((b'\xF9\xFC'+struct.pack('<H',rank))*length+b'\xE5');run([field]*3,mode)
        for n in range(4):run([good]*n,mode)
        run([good]*3,mode,positions=(0,127,254))
        for invalid in (bad,b'\xF8'+b'\xFF'*20+b'\xE5',b'\xE4'*22,b'\xE6\xE5'+bytes(20)):
            for slot in range(3):
                fields=[good]*3;fields[slot]=invalid;run(fields,mode)
        for flags,day in ((0,b'\x01\x02\x03'),(12,b'\x01\x02\x03'),(4,b'\x02\x02\x03')):
            for slot in range(3):
                filters=[(4,b'\x01\x02\x03')]*3;filters[slot]=(flags,day);run([good]*3,mode,filters=filters)
        for payload in (0,152,229,255):run([bytes([228,payload,229])+bytes(19)]*3,mode)
    if reentry:
        def repair(slot,title):
            stage=0x02026280;body=arena+32*slot+10;wanted=pack(title)
            u.mem_write(stage,title);expected=bytearray(u.mem_read(0x02000000,0x40000))
            expected[body-0x02000000:body-0x02000000+22]=wanted
            u.mem_write(sp-192,b'\x5A'*192);u.reg_write(UC_ARM_REG_CPSR,0x30)
            values=[0x13579000+i for i in range(8)]
            for r,v in zip(regs,values):u.reg_write(r,v)
            for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),(stage,body,22<<16|len(title),10)):u.reg_write(r,v)
            u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1);writes.clear()
            u.emu_start(0x0830D001,stop,count=50000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or u.reg_read(UC_ARM_REG_R0)!=22 or any(u.reg_read(r)!=v for r,v in zip(regs,values)):raise ValueError('repair writer ABI')
            if bytes(u.mem_read(0x02000000,0x40000))!=expected or bytes(u.mem_read(sp-192,104))!=b'\x5A'*104:raise ValueError('repair writer EWRAM/stack')
            if any(not(sp-88<=a and a+n<=sp) and not(body<=a and a+n<=body+22) for a,n in writes):raise ValueError('repair write range')
            counts['writer_repairs']+=1;counts['whole_EWRAM_checks']+=1
            return wanted
        for mode in (0,1):
            for n in range(4):run([good]*n,mode,initial=True)
            for rank in (0,229,11171):
                title=(b'\xF9\xFC'+struct.pack('<H',rank))*10+b'\xE5'
                for slot in range(3):
                    fields=[good]*3;fields[slot]=bad
                    run(fields,mode,initial=True)
                    run(fields,initial=True,fresh=False)
                    fields[slot]=repair(slot,title)
                    run(fields,initial=True,fresh=False)
                    counts['reentry_cycles']+=1
            filters=[(12,b'\x01\x02\x03')]*3
            run([good]*3,mode,filters=filters,initial=True)
    out=base/('cpu_calendar_prefill_reentry' if reentry else 'cpu_calendar_prefill_guard');out.mkdir(exist_ok=True)
    for n,b in artifacts.items():(out/n).write_bytes(b)
    report=dict(id='exe45.hangul-keyboard.prefill-'+('reentry' if reentry else 'guard')+'-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,
                source_sha256=profile['sha256'],current_rom_sha256=identity,counts=counts,dependencies=dependencies,
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('bench_calendar_prefill_guard.py','hangul_calendar_prefill_guard.py','hangul_calendar_prefill.py')},
                artifacts={n:sha(b) for n,b in artifacts.items()},ISA=isas,native_code=native,fixture_hooks=hooks,stack_bound_bytes=160,examples=examples,
                limits=['Native30F0C parent with existing-initialized substate4 fixture ->330C6 dispatcher/33100 initializer/prefill/getter/count executed; graphics/audio/flag cleanup services modeled, no pixels/VRAM or audible test.',
                        'Guard failure empties three display streams, skips count/headings/selection, emits error-sound127 request and cancel-return2. Native parent consumes return2 into substate4/import flag1 and requests flag14:79/80 cleanup. No Korean error dialog, initial parent entry, re-entry or natural reachability proof.',
                        'No new persistent RAM flag; R12 status confined to verified native/helper paths. IRQ lifetime and real ROM code placement not adopted.',
                        'Records/metadata are HOST fixtures; F8 remains conditional; actual keyboard output, all writers/readers and save/reset/fresh-load remain pending.'])
    if reentry:
        report['limits']=[
            'Native30F0C first entry/count/empty-default or3A3B0->090C->BIOS-reset request->330C0->list executed. BIOS CpuSet zero16 is modeled with exact admitted args; graphics/audio/flag cleanup services modeled, no runtime screen/audio.',
            '18 cycles: failing initial entry -> same-record failing re-invocation -> emitted writer repairs one body -> successful re-invocation. No HOST UI/parent/metadata/pool/record rewrites between phases; HOST supplies writer source stream. Re-invocation is at a verified routine boundary, not natural menu traversal.',
            'Empty/deleted-record first entry keeps native default path with no list/guard/error; prior pool slot0/UI state are not cleared by that original path. Downstream default/edit consumers remain pending.',
            'Conditional F8 and transient R12/IRQ/ROM placement remain unadopted. No actual keyboard input, save/reset/fresh-load or product ROM.']
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(play,identity)
    print('PASS prefill failure propagation CPU; NOT ROM/runtime/save',counts)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--reentry',action='store_true')
    main(parser.parse_args().reentry)
