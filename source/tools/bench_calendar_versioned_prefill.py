"""Execute native getter/default/prefill with conditional F8 reader adapters.

No ROM or save is written. Real native default script68 and record search run;
fixture records/metadata are HOST inputs, not loaded persistent saves.
"""
import json
import struct
from bench_hangul_composer_thumb import *
from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB
from hangul_calendar_versioned_record import pack, read
from hangul_calendar_prefill import assemble
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE


def main():
    base = ROOT/'analysis/hangul_keyboard_v1'
    dependencies = {}
    for name in ('cpu_calendar_versioned_record', 'cpu_calendar_title_record', 'cpu_record_display'):
        p = base/name/'report.json'
        d = json.loads(p.read_text(encoding='utf8'))
        if not d['passed'] or d['rom_integrated']:
            raise ValueError('dependency scope')
        for n, h in d['tools'].items(): require_hash(ROOT/'tools'/n, h)
        for n, h in d['artifacts'].items(): require_hash(p.parent/n, h)
        dependencies[name+'/report.json'] = sha(p.read_bytes())
    profile = json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source = ROOT/profile['filename']; require_hash(source, profile['sha256'])
    original = source.read_bytes()
    identity = json.loads((base/'calendar_name_lifetime.json').read_text(encoding='utf8'))['current_rom_sha256']
    play = ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    require_hash(play, identity); rom = play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB); ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    native = []
    for a, b in ((0x33334,0x3338E),(0x3739A,0x373FA),(0x32AA8,0x32AD8)):
        raw = original[a:b]; instructions = list(cs.disasm(raw, 0x08000000+a))
        if rom[a:b] != raw or sum(i.size for i in instructions) != len(raw):
            raise ValueError('native identity/boundaries')
        for i in instructions:
            if i.size not in (2,4) or i.size == 4 and i.mnemonic != 'bl':
                raise ValueError('native Thumb1')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0]) != i.bytes:
                raise ValueError('native roundtrip')
        native.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    literals = {0x33390:0x02026080,0x33394:0x02014DEC,0x373FC:0x020011F0,0x37400:0x02000950}
    if any(struct.unpack_from('<I',rom,a)[0] != v or rom[a:a+4] != original[a:a+4] for a,v in literals.items()):
        raise ValueError('native literals')
    blob, isa = assemble(); clone = bytearray(rom); hooks = []
    clone[0x30E000:0x30E000+len(blob)] = blob
    for at in (0x33344,0x3335A,0x3336E):
        ins = list(cs.disasm(rom[at:at+4],0x08000000+at))
        if len(ins) != 1 or ins[0].mnemonic != 'bl' or ins[0].op_str != '#0x8032ac6':
            raise ValueError('copy call')
        patch = bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x830e000',0x08000000+at)[0])
        if len(patch) != 4 or list(cs.disasm(patch,0x08000000+at))[0].op_str != '#0x830e000':
            raise ValueError('placed call')
        clone[at:at+4] = patch
        hooks.append(dict(offset=at,expected_hex=rom[at:at+4].hex(),final_hex=patch.hex()))
    for address,path in ((0x0830D000,base/'cpu_calendar_versioned_record/writer.bin'),
                         (0x0830D200,base/'cpu_calendar_versioned_record/reader.bin'),
                         (0x08309000,base/'cpu_calendar_title_record/converter.bin')):
        raw = path.read_bytes(); clone[address-0x08000000:address-0x08000000+len(raw)] = raw
    u = Uc(UC_ARCH_ARM,UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    extent = (len(clone)+4095)&~4095
    u.mem_map(0x08000000,extent); u.mem_write(0x08000000,bytes(clone))
    u.mem_map(0x08F09000,4096); u.mem_write(0x08F09000,(base/'cpu_record_display/helper.bin').read_bytes())
    u.mem_protect(0x08F09000,4096,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_map(0x02000000,0x40000); u.mem_map(0x03007000,4096); u.mem_map(0x0FF00000,4096)
    arena,pool,meta,date,sp,stop = 0x020011F0,0x02026080,0x02000950,0x02014DEC,0x03007EFC,0x0FF00000
    # Default copies execute unchanged native lookup and raw copier. Its exact
    # default script is source-derived, not replaced by a service stub.
    archive = struct.unpack_from('<I',rom,0x32AD8)[0]-0x08000000
    default_at = archive+struct.unpack_from('<H',rom,archive+68*2)[0]
    default = rom[default_at:rom.index(b'\xE5',default_at)+1]
    regs = [UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes=[]; visits=[]
    def hook(cpu,a,n,user):
        if a == stop: cpu.emu_stop()
        if a in (0x08033344,0x0803335A,0x0803336E): visits.append(a)
    u.hook_add(UC_HOOK_CODE,hook)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    counts=dict(routes=0,syllables=0,slot_decodes=0,legacy_routes=0,malformed_routes=0,
                null_routes=0,getter_filters=0,whole_EWRAM_checks=0,source_raw_mismatch=0,
                writer_prefill_routes=0,writer_calls=0)
    def run(fields,positions=(0,1,2),patched=True,filters=None,titles=None):
        for h in hooks:
            u.mem_write(0x08000000+h['offset'],bytes.fromhex(h['final_hex'] if patched else h['expected_hex']))
        u.ctl_remove_cache(0x08033334,0x0803338E)
        u.mem_write(0x02000000,b'\xA7'*0x40000)
        u.mem_write(arena,bytes(255*32)); u.mem_write(meta+5,bytes([len(fields)])); u.mem_write(meta+6,b'\xAA')
        u.mem_write(date,b'\x01\x02\x03')
        for index, (field,position) in enumerate(zip(fields,positions)):
            flags,record_date = (4,b'\x01\x02\x03') if filters is None else filters[index]
            record=arena+32*position
            u.mem_write(record,bytes([flags,index])+record_date+bytes(5)+(field if titles is None else bytes(22)))
        if titles is not None:
            for index, (field,position) in enumerate(zip(fields,positions)):
                record=arena+32*position
                title=titles[index]
                if pack(title)!=field: raise ValueError('writer oracle identity')
                stage=0x02026280; u.mem_write(stage,title)
                writer_before=bytearray(u.mem_read(0x02000000,0x40000))
                writer_expected=bytearray(writer_before)
                writer_expected[record+10-0x02000000:record+32-0x02000000]=field
                u.mem_write(sp-160,b'\x5A'*160); u.reg_write(UC_ARM_REG_CPSR,0x30)
                for i,r in enumerate(regs): u.reg_write(r,0x13579000+i)
                for r,v in zip((UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3),
                               (stage,record+10,22<<16|len(title),10)): u.reg_write(r,v)
                u.reg_write(UC_ARM_REG_SP,sp); u.reg_write(UC_ARM_REG_LR,stop|1); writes.clear()
                u.emu_start(0x0830D001,stop,count=50000)
                if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_R0)!=22 or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):
                    raise ValueError('writer ABI')
                if bytes(u.mem_read(sp-160,72))!=b'\x5A'*72 or bytes(u.mem_read(0x02000000,0x40000))!=writer_expected:
                    raise ValueError('writer EWRAM/stack88 guard')
                if any(not(sp-88<=a and a+n<=sp) and not(record+10<=a and a+n<=record+32) for a,n in writes):
                    raise ValueError('writer write bounds')
                counts['writer_calls']+=1; counts['whole_EWRAM_checks']+=1
        # No HOST record-body or pool rewrite follows any writer call.
        before = bytes(u.mem_read(0x02000000,0x40000)); expected = bytearray(before)
        cursor=0; calls=[]; decoded=0; malformed=False; initialized=False
        regions=[]
        def put(a,b):
            expected[a-0x02000000:a-0x02000000+len(b)] = b
            regions.append((a,len(b)))
        # Independent expected native traversal: ascending index, matching
        # active/not-deleted flags and three date bytes; first-match arena order.
        found=[]
        for index in range(len(fields)):
            valid=[i for i in range(len(fields)) if i==index and (filters is None or
                   filters[i][0]&4 and not filters[i][0]&8 and filters[i][1]==b'\x01\x02\x03')]
            if valid: found.append(valid[0])
        for slot in range(3):
            index = next((i for i in found if i>=cursor),None)
            if index is None:
                if slot==0:
                    # Original caller unconditionally adds10 to NULL; adapter
                    # arena admission rejects it before memory access.
                    calls.append(0x08033344)
                break
            cursor=index+1
            calls.append((0x08033344,0x0803335A,0x0803336E)[slot])
            try: value = read(fields[index]) if patched else fields[index][:fields[index].index(229)+1]
            except ValueError:
                malformed=True; break
            put(pool+128*slot,value); decoded+=1
            if slot==0:
                put(pool+128,default); put(pool+256,default); initialized=True
        put(meta+6,bytes([cursor]))
        u.mem_write(sp-160,b'\x5A'*160); u.mem_write(sp,struct.pack('<I',stop|1))
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for i,r in enumerate(regs): u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp); u.reg_write(UC_ARM_REG_LR,stop|1); writes.clear(); visits.clear()
        u.emu_start(0x08033335,stop,count=50000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):
            raise ValueError('prefill ABI')
        if bytes(u.mem_read(sp-160,24))!=b'\x5A'*24: raise ValueError('stack136 guard')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected or visits!=calls:
            raise ValueError('native prefill EWRAM/route')
        if any(not(sp-136<=a and a+n<=sp) and not any(s<=a and a+n<=s+l for s,l in regions) for a,n in writes):
            raise ValueError('prefill write bounds')
        counts['routes']+=1; counts['whole_EWRAM_checks']+=1; counts['slot_decodes']+=decoded
        counts['malformed_routes']+=malformed; counts['null_routes']+=not found
        counts['writer_prefill_routes']+=titles is not None
        return bytes(u.mem_read(pool,128))
    tagged=pack(b'\xF9\xFC\xE5\0\xE5')
    unpatched=run([tagged],patched=False)
    if unpatched[:len(read(tagged))] == read(tagged): raise ValueError('raw counterexample missing')
    counts['source_raw_mismatch']+=1
    for rank in range(11172):
        title=(b'\xF9\xFC'+struct.pack('<H',rank))*10+b'\xE5'
        field=pack(title)
        run([field,field,field],titles=[title]*3); counts['syllables']+=1
        if rank%2048==0: print('prefill rank',rank,flush=True)
    for payload in range(256):
        field=bytes([228,payload,229])+b'\xA7'*19
        run([field]*3); counts['legacy_routes']+=1
    for byte in range(228):
        run([(bytes([byte,229])+b'\xA7'*20)]*3); counts['legacy_routes']+=1
    for n in range(4): run([tagged]*n)
    run([tagged]*3,positions=(0,127,254))
    for bad in (b'\xF8'+b'\xFF'*20+b'\xE5',tagged[:-1]+b'\0',b'\xE4'*22):
        for slot in range(3):
            fields=[tagged]*3; fields[slot]=bad; run(fields)
    for flags,wrongdate in ((0,b'\x01\x02\x03'),(12,b'\x01\x02\x03'),(4,b'\x02\x02\x03')):
        for slot in range(3):
            filters=[(4,b'\x01\x02\x03')]*3; filters[slot]=(flags,wrongdate)
            run([tagged]*3,filters=filters); counts['getter_filters']+=1
    out=base/'cpu_calendar_versioned_prefill'; out.mkdir(exist_ok=True)
    (out/'adapter.bin').write_bytes(blob)
    report=dict(id='exe45.hangul-keyboard.versioned-prefill-CPU.v1',passed=True,
                rom_integrated=False,format_adopted=False,source_sha256=profile['sha256'],
                current_rom_sha256=identity,counts=counts,dependencies=dependencies,
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in
                       ('bench_calendar_versioned_prefill.py','hangul_calendar_prefill.py','hangul_calendar_versioned_record.py')},
                artifacts={'adapter.bin':sha(blob)},ISA=isa,native_code=native,
                fixture_hooks=hooks,stack_bound_bytes=136,
                no_HOST_record_or_pool_rewrite_between_writer_and_prefill=True,
                default=dict(script=68,address=0x08000000+default_at,hex=default.hex()),
                limits=['CPU-only native33334,33374,3739A/373A2,32AA8/32AC6; no service stubs.',
                        'All11172 syllables execute emitted writer in all three slots then native prefill without HOST record/pool rewrite. Source streams/date/metadata and other record tests are HOST fixtures, not native save reload or keyboard output.',
                        'Invalid field aborts remaining prefill without copying malformed bytes; prior valid/default slot writes remain. Error feedback and editor transition are not implemented.',
                        'F8 remains conditional; other writers/list readers/provider population, RAM/IRQ placement and save/reset/fresh-load remain unresolved.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']); require_hash(play,identity)
    print('PASS native versioned prefill CPU; NOT ROM/save',counts,flush=True)


if __name__ == '__main__': main()
