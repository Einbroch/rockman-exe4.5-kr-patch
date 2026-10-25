"""Conditional F8 writer -> native registration -> native detail/count.

CPU clone only. No HOST field or pool rewrite between registration and readers.
Legacy records enter detail independently. No save/ROM installation claim.
"""
import json, struct
from bench_hangul_composer_thumb import *
from extended_dialogue import assemble_verified, Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB
from hangul_calendar_title_record import COMMIT
from hangul_calendar_display_shim import CODE
from hangul_calendar_bounded_commit import assemble_adapter
from hangul_calendar_versioned_record import pack, read


def main():
    base = ROOT/'analysis/hangul_keyboard_v1'
    deps = {}; reports = {}
    for name in ('cpu_calendar_versioned_record', 'cpu_calendar_title_record', 'cpu_record_display', 'cpu_calendar_record_display', 'cpu_calendar_activity'):
        path = base/name/'report.json'; d = json.loads(path.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']: raise ValueError('dependency scope')
        for n, h in d.get('tools', {}).items(): require_hash(ROOT/'tools'/n, h)
        for n, h in d.get('artifacts', {}).items(): require_hash(path.parent/n, h)
        reports[name] = d; deps[name+'/report.json'] = sha(path.read_bytes())
    lifetime = base/'calendar_name_lifetime.json'; observed = json.loads(lifetime.read_text(encoding='utf8'))
    if not observed['passed']: raise ValueError('lifetime scope')
    deps['calendar_name_lifetime.json'] = sha(lifetime.read_bytes())
    profile = json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source = ROOT/profile['filename']; require_hash(source, profile['sha256'])
    play = ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    require_hash(play, observed['current_rom_sha256']); rom = play.read_bytes(); original = source.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB); cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    native = []
    for a, b in ((0x32EFE,0x32F26), (0x37366,0x3737A), (0x33C94,0x33CB8)):
        raw = original[a:b]; ins = list(cs.disasm(raw,0x08000000+a))
        if rom[a:b] != raw or sum(i.size for i in ins) != len(raw): raise ValueError('native source')
        for i in ins:
            if i.size not in (2,4) or i.size == 4 and i.mnemonic != 'bl': raise ValueError('native Thumb1')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0]) != i.bytes: raise ValueError('native roundtrip')
        native.append(dict(offset=a, bytes=b-a, sha256=sha(raw)))
    artifacts = {}; isas = {}; clone = bytearray(rom); hooks = []
    def put(name, address, result):
        blob, isa = result; artifacts[name] = blob; isas[name] = isa
        clone[address-0x08000000:address-0x08000000+len(blob)] = blob
    put('commit.bin',0x08308000,assemble_verified(COMMIT,0x08308000,dict(context=0x02014DD0,arena=0x020011F0,arena_bytes=255*32,pool=0x02026080,extents=22<<16|41,converter=0x0830D001)))
    put('adapter.bin',0x08308100,assemble_adapter())
    put('shim.bin',0x08307000,assemble_verified(CODE,0x08307000,dict(extents=41<<16|22,decoder=0x0830D201,continuation=0x08033CB7)))
    for name, address, path in (('writer',0x0830D000,base/'cpu_calendar_versioned_record/writer.bin'),('reader',0x0830D200,base/'cpu_calendar_versioned_record/reader.bin'),('converter',0x08309000,base/'cpu_calendar_title_record/converter.bin')):
        blob = path.read_bytes(); clone[address-0x08000000:address-0x08000000+len(blob)] = blob
    for at, target in ((0x32F06,0x08308100),(0x33C9A,0x08307000)):
        if list(cs.disasm(rom[at:at+4],0x08000000+at))[0].op_str != '#0x8032ac6': raise ValueError('source BL guard')
        patch = bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #'+hex(target),0x08000000+at)[0])
        if len(patch) != 4 or list(cs.disasm(patch,0x08000000+at))[0].op_str != '#'+hex(target): raise ValueError('placed BL')
        clone[at:at+4] = patch; hooks.append(dict(offset=at,expected_hex=rom[at:at+4].hex(),final_hex=patch.hex()))
    activity_report = reports['cpu_calendar_activity']
    suffix = bytes.fromhex(activity_report['suffix']['hex'])
    suffix_at = activity_report['suffix']['address']-0x08000000
    if rom[suffix_at:suffix_at+len(suffix)] != suffix: raise ValueError('activity suffix identity')
    # Consume the verified activity write specification, not a second hook plan.
    # Its old32F06 writer is deliberately replaced by the versioned writer above.
    for patch in activity_report['fixture_writes']:
        at = patch['offset']
        if at == 0x32F06: continue
        expected = bytes.fromhex(patch['expected_hex']); final = bytes.fromhex(patch['final_hex'])
        if rom[at:at+len(expected)] != expected: raise ValueError('activity expected source')
        if any(max(at,h['offset']) < min(at+len(final),h['offset']+len(bytes.fromhex(h['final_hex']))) for h in hooks): raise ValueError('fixture overlap')
        clone[at:at+len(final)] = final; hooks.append(patch)
    for name,address in (('activity.bin',0x0830A000),('activity_adapter.bin',0x0830A200),('failure_tail.bin',0x0830A240),('caller.bin',0x0830A280),('caller_veneer.bin',0x0830C100)):
        blob = (base/'cpu_calendar_activity'/name).read_bytes()
        clone[address-0x08000000:address-0x08000000+len(blob)] = blob
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    extent = (len(clone)+4095)&~4095; u.mem_map(0x08000000,extent); u.mem_write(0x08000000,bytes(clone)); u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x08F09000,4096); u.mem_write(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes()); u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000); u.mem_map(0x03007000,4096); u.mem_map(0x0FF00000,4096)
    pool,stage,ctx,ui,meta = 0x02026080,0x02026280,0x02014DD0,0x0200F550,0x02000950
    sp,stop = 0x03007EFC,0x0FF00000
    regs = [UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[]; sounds=[]; heads=[]; sprites=[]; activity_calls=[]
    from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
    def hook(cpu,a,n,user):
        if a == stop: cpu.emu_stop(); return
        if a == 0x08000534: sounds.append(cpu.reg_read(UC_ARM_REG_R0))
        elif a in (0x08029164,0x08032E60): activity_calls.append(a)
        elif a == 0x080554A4: heads.append(tuple(cpu.reg_read(r) for r in (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,*regs[:4])))
        elif a == 0x080291C4: sprites.append((cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1),bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R2),6))))
        else: return
        cpu.reg_write(UC_ARM_REG_R0,0); cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
    u.hook_add(UC_HOOK_CODE,hook); u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    stats=dict(registrations=0,accepted_registrations=0,rejected_registrations=0,details=0,legacy_details=0,rejected_details=0,counts=0,whole_EWRAM_checks=0,syllables=0,activity_routes=0,activity_accepted=0,activity_rejected=0,activity_syllables=0)
    def execute(pc,args,stack,outer=False):
        u.mem_write(sp-256,b'\x5A'*256); u.mem_write(sp,struct.pack('<I',stop|1)); u.reg_write(UC_ARM_REG_CPSR,0x30)
        values = [ui if i==1 else 0x13579000+i for i in range(8)]
        for r,v in zip(regs,values): u.reg_write(r,v)
        for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),args): u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp); u.reg_write(UC_ARM_REG_LR,stop|1); writes.clear(); sounds.clear(); heads.clear(); sprites.clear(); activity_calls.clear()
        u.emu_start(pc|1,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp+4*outer or any(u.reg_read(r)!=v for r,v in zip(regs,values)): raise ValueError('ABI')
        if bytes(u.mem_read(sp-256,256-stack)) != b'\x5A'*(256-stack): raise ValueError('stack bound')
    def check(before,regions,stack):
        expected=bytearray(before)
        for a,b in regions: expected[a-0x02000000:a-0x02000000+len(b)]=b
        if bytes(u.mem_read(0x02000000,0x40000)) != expected: raise ValueError('whole EWRAM')
        if any(not(sp-stack<=a and a+n<=sp or any(s<=a and a+n<=s+len(b) for s,b in regions)) for a,n in writes): raise ValueError('write interval')
        stats['whole_EWRAM_checks']+=1
    def detail(field,row=0,legacy=False):
        raw=bytes(u.mem_read(field,22))
        try: wanted=read(raw); valid=True
        except ValueError: wanted=b''; valid=False
        before=bytes(u.mem_read(0x02000000,0x40000)); execute(0x08033C94,(field,row),152); check(before,[(pool,wanted)] if valid else [],152)
        if valid:
            archive,draw,target,font=struct.unpack_from('<4I',rom,0x33CB8)
            if heads != [(archive,72,draw+(row<<10),target+(row<<10),10,1,font,0)]: raise ValueError('heading request')
            i=0; count=0
            while wanted[i]!=229: i+=4 if wanted[i]==249 else 2 if wanted[i]==228 else 1; count+=1
            before=bytes(u.mem_read(0x02000000,0x40000)); execute(0x08032F7C,(10,20),36); check(before,[],36)
            if len(sprites)!=1 or sprites[0][:2]!=(130-4*count,20) or sprites[0][2][:2]!=bytes([count,1]) or sprites[0][2][4:]!=b'\x02\0': raise ValueError('logical count')
            stats['counts']+=1
        elif heads: raise ValueError('malformed record reached heading')
        stats['details']+=1; stats['legacy_details']+=legacy; stats['rejected_details']+=not valid
    def register(raw,slot=9,override=None,prepared=False):
        record=0x020011F0+32*slot if override is None else override
        try: wanted=pack(raw); valid=0x020011F0<=record<0x020031D0 and (record-0x020011F0)%32==0
        except ValueError: wanted=b''; valid=False
        if prepared:
            if bytes(u.mem_read(pool,len(raw))) != raw or int.from_bytes(u.mem_read(ctx+44,4),'little') != record: raise ValueError('uninterrupted activity output')
        else:
            u.mem_write(0x02000000,b'\xA7'*0x40000); u.mem_write(pool,raw); u.mem_write(stage,bytes.fromhex(observed['default_meal']['stage_untouched']))
            u.mem_write(ctx+44,struct.pack('<I',record)); u.mem_write(meta+4,b'\xFE')
        before=bytes(u.mem_read(0x02000000,0x40000)); regions=[(ui,struct.pack('<I',16))]
        if valid: regions += [(record+10,wanted),(record,b'\x03\xFE'),(meta+4,b'\xFF')]
        else: regions += [(ui+6,b'\x01'),(ui+8,b'\x02')]
        execute(0x08032EFE,(),112,True); check(before,regions,112)
        if sounds != [128 if valid else 127]: raise ValueError('native registration status')
        stats['registrations']+=1; stats['accepted_registrations']+=valid; stats['rejected_registrations']+=not valid
        if valid: detail(record+10,slot%2)
    def activity(person):
        from hangul_calendar_title_record import convert
        record = 0x020011F0+9*32
        u.mem_write(0x02000000,b'\xA7'*0x40000); u.mem_write(pool,person)
        # Person stage is a deliberately distinct re-entry baseline. It must
        # survive append, commit and detail; HOST supplies this initial fixture.
        u.mem_write(stage,b'\x01\x9B\xE5'+b'\x55'*19)
        u.mem_write(ctx+44,struct.pack('<I',record)); u.mem_write(record+9,b'\x01'); u.mem_write(meta+4,b'\xFE'); u.mem_write(ui,bytes(16))
        try:
            convert(person,6); i=0
            while person[i]!=229: i+=4 if person[i]==249 else 2 if person[i]==228 else 1
            title=person[:i]+suffix; pack(title); valid=True
        except (ValueError,IndexError): valid=False
        before=bytes(u.mem_read(0x02000000,0x40000))
        regions=[(pool,title),(ui,b'\x04'),(ui+4,b'\xFF\x18')] if valid else [(ui,struct.pack('<I',16)),(ui+6,b'\x01'),(ui+8,b'\x02')]
        execute(0x0830C100,(pool,),208); check(before,regions,208)
        if activity_calls != [0x08029164]+([0x08032E60] if valid else []) or len(heads)!=int(valid): raise ValueError('activity confirmation/heading branch')
        stats['activity_routes']+=1; stats['activity_accepted']+=valid; stats['activity_rejected']+=not valid
        if valid: register(title,prepared=True)
    for rank in range(11172):
        register((b'\xF9\xFC'+struct.pack('<H',rank))*10+b'\xE5'); stats['syllables']+=1
        if rank%2048==0: print('native versioned rank',rank,flush=True)
    for payload in range(256): register(bytes([228,payload,229]))
    for raw in (bytes.fromhex(observed['default_meal']['pool_name_hex']),bytes.fromhex(observed['friend']['final_title_hex'])): register(raw)
    for slot in range(255): register(b'\xF9\xFC\xE5\0\xE5',slot)
    for raw in (b'\xE5',b'\xE4',b'\xF9\xFC\xA4\x2B\xE5',b'\x01'*41,b'\x01'*11+b'\xE5'): register(raw)
    for bad in (0,0xFFFFFFFF,0x020011F1,0x020031D0,stage): register(b'\x01\xE5',override=bad)
    for rank in range(11172):
        activity((b'\xF9\xFC'+struct.pack('<H',rank))*6+b'\xE5'); stats['activity_syllables']+=1
        if rank%2048==0: print('activity versioned rank',rank,flush=True)
    for n in range(1,7): activity(b'\xF9\xFC\xE5\0'*n+b'\xE5')
    for payload in range(256): activity(bytes([228,payload,229]))
    activity(b'\x9B\xE5')
    for raw in (b'\xE5',b'\xE4',b'\xF9\xFC\0',b'\xF9\xFC\xA4\x2B\xE5',b'\x01'*7+b'\xE5',b'\xE6\xE5'): activity(raw)
    field=0x0200131A
    for raw in (bytes.fromhex(observed['default_meal']['pool_name_hex']),bytes.fromhex(observed['friend']['final_title_hex']),b'\x81\xE5',b'\xE4\xE5\xE5'):
        u.mem_write(0x02000000,b'\xA7'*0x40000); u.mem_write(field,raw.ljust(22,b'\0')); detail(field,legacy=True)
    good=pack(b'\xF9\xFC\xE5\0\xE5')
    for raw in (b'\xF8'+b'\xFF'*20+b'\xE5',good[:-1]+b'\0',good[:1]+b'\xFF\x7F'+good[3:],good[:3]+b'\0\0'+good[5:]):
        u.mem_write(0x02000000,b'\xA7'*0x40000); u.mem_write(field,raw); detail(field)
    out=base/'cpu_calendar_versioned_native'; out.mkdir(exist_ok=True)
    for n,b in artifacts.items(): (out/n).write_bytes(b)
    report=dict(id='exe45.hangul-keyboard.versioned-native-CPU.v1',passed=True,rom_integrated=False,format_adopted=False,source_sha256=profile['sha256'],current_rom_sha256=observed['current_rom_sha256'],counts=stats,dependencies=deps,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('bench_calendar_versioned_native.py','hangul_calendar_bounded_commit.py','hangul_calendar_title_record.py','hangul_calendar_display_shim.py','hangul_calendar_versioned_record.py')},artifacts={n:sha(b) for n,b in artifacts.items()},ISA=isas,native_code=native,fixture_hooks=hooks,registration_stack_bytes=112,registration_outer_stack_bytes=4,detail_stack_bytes=152,counter_stack_bytes=36,activity_caller_stack_bytes=208,no_HOST_record_or_pool_rewrite_between_registration_detail_count=True,no_HOST_record_or_pool_rewrite_between_activity_registration_detail_count=True,limits=['Native32EFE/37366 -> F8 field22 -> native33C94 and F9FC counter executed in CPU clone. Sound, heading and sprite services modeled; no pixels/VRAM/screen.', 'Activity routes execute native32E22/33014 with coordinated bounded append then versioned registration/detail/count. Initial person pool and distinct re-entry stage are HOST fixtures, not keyboard output. Other default/direct/import writers, prefill and other record consumers remain unresolved. F8 grammar is conditional, not globally adopted.', 'Legacy controls read observed meal/friend fields and 81 E5 prefix as legacy. Malformed F8 does not fall back; row clearing and visible error feedback not established.', 'No original/playable/save modification, no new keyboard runtime/save/reset/freshload, no whole-memory or release PASS.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']); require_hash(play,observed['current_rom_sha256'])
    print('PASS native versioned registration/detail/count CPU; NOT ROM/screen/save',stats,flush=True)


if __name__=='__main__': main()
