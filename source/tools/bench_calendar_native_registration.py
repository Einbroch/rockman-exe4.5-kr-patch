"""Reproduce unsafe calendar registration in the unchanged native CPU path.

This is a negative integration experiment, NOT a safe registration hook.
The source pool fixture is explicitly typed; no automatic format detection.
No ROM/save files are written. Sound service only is modeled.
"""
import json, struct
from bench_hangul_composer_thumb import *
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB


def main():
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename']; require_hash(source,profile['sha256']); original=source.read_bytes()
    play=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity=json.loads((ROOT/'analysis/hangul_keyboard_v1/cpu_calendar_record_transfer/report.json').read_text())['current_rom_sha256']
    require_hash(play,identity); rom=play.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB); ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB); scopes=[]
    for a,b in ((0x32EFE,0x32F26),(0x32AC6,0x32AD8),(0x37366,0x3737A)):
        raw=original[a:b]; ins=list(cs.disasm(raw,0x08000000+a))
        if rom[a:b]!=raw or sum(i.size for i in ins)!=len(raw): raise ValueError('native scope/source')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl': raise ValueError('Thumb1 scope')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes: raise ValueError('native ISA roundtrip')
        scopes.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    literals={0x32F28:0x02014DD0,0x32FCC:0x02026080,0x37400:0x02000950}
    if any(struct.unpack_from('<I',original,a)[0]!=v or rom[a:a+4]!=original[a:a+4] for a,v in literals.items()): raise ValueError('literal identities')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(len(rom)+4095)&~4095); u.mem_write(0x08000000,rom)
    u.mem_map(0x02000000,0x40000); u.mem_map(0x03007000,4096); u.mem_map(0x0FF00000,4096)
    from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
    pool,record,ctx,metadata,sp,stop=0x02026080,0x02001310,0x02014DD0,0x02000950,0x03007EFC,0x0FF00000
    writes=[]; sounds=[]
    def hook(cpu,a,n,user):
        if a==0x08000534:
            sounds.append(cpu.reg_read(UC_ARM_REG_R0)); cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        elif a==stop: cpu.emu_stop()
    u.hook_add(UC_HOOK_CODE,hook)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    counts=dict(native_registrations=0,whole_EWRAM_checks=0,binary_routes=0,binary_early_terminations=0,
                display_routes=0,display_early_terminations=0,display_neighbor_overflows=0,legacy_controls=0,counter_wraps=0)
    examples=[]
    def run(raw,kind,rank=None,counter=0):
        u.mem_write(0x02000000,b'\xA7'*0x40000); u.mem_write(pool,raw)
        u.mem_write(ctx+0x2C,struct.pack('<I',record)); u.mem_write(metadata+4,bytes([counter]))
        before=bytes(u.mem_read(0x02000000,0x40000)); expected=bytearray(before)
        # Native semantics oracle: byte copier includes first E5; no token/field bound.
        copied=raw[:raw.index(0xE5)+1]
        at=record-0x02000000
        expected[at+10:at+10+len(copied)]=copied
        expected[at:at+2]=bytes([3,counter]); expected[metadata-0x02000000+4]=(counter+1)&255
        expected[ctx-0x02000000:ctx-0x02000000+4]=struct.pack('<I',16)
        u.mem_write(sp-32,b'\x5A'*32); u.mem_write(sp,struct.pack('<I',stop|1))
        saved=[ctx if i==1 else 0x13579000+i for i in range(8)]
        registers=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip(registers,saved): u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp); writes.clear(); sounds.clear()
        u.emu_start(0x08032EFF,stop,count=4000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp+4 or sounds!=[128] or any(u.reg_read(r)!=v for r,v in zip(registers,saved)): raise ValueError('native registration ABI')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected: raise ValueError('whole EWRAM registration semantics')
        allowed=[(record,2),(record+10,len(copied)),(metadata+4,1),(ctx,4),(sp-4,4)]
        if any(not any(s<=a and a+n<=s+l for s,l in allowed) for a,n in writes): raise ValueError('unexpected CPU write')
        if bytes(u.mem_read(sp-32,28))!=b'\x5A'*28: raise ValueError('stack bound')
        counts['native_registrations']+=1; counts['whole_EWRAM_checks']+=1; counts['counter_wraps']+=counter==255
        if kind=='binary':
            counts['binary_routes']+=1; counts['binary_early_terminations']+=len(copied)!=22
        elif kind=='display':
            counts['display_routes']+=1; counts['display_early_terminations']+=len(copied)!=len(raw)
            counts['display_neighbor_overflows']+=len(copied)>22
        else: counts['legacy_controls']+=1
        if rank in (228,229,11171): examples.append(dict(kind=kind,rank=rank,input_bytes=len(raw),copied_bytes=len(copied),neighbor_bytes=max(0,len(copied)-22),registered_despite_defect=len(copied)!=len(raw) or len(copied)>22))
    for rank in range(11172):
        word=struct.pack('<H',rank)
        run(b'\x8A'+word*10+b'\xE5','binary',rank)
        run((b'\xF9\xFC'+word)*10+b'\xE5','display',rank)
        if rank%2048==0: print('native registration rank',rank,flush=True)
    for raw in (b'\x81\xE5',b'\x01'*10+b'\xE5',b'\xE4\x01'*10+b'\xE5'):
        for counter in (0,254,255): run(raw,'legacy',counter=counter)
    out=ROOT/'analysis/hangul_keyboard_v1/cpu_calendar_native_registration'; out.mkdir(exist_ok=True)
    result=dict(id='exe45.hangul-keyboard.native-registration-negative-CPU.v1',passed=True,safe_registration=False,rom_integrated=False,
        source_sha256=profile['sha256'],current_rom_sha256=identity,counts=counts,native_code=scopes,
        literals=[dict(offset=a,value=v) for a,v in literals.items()],examples=examples,tools={Path(__file__).name:sha(Path(__file__).read_bytes())},
        name_field=dict(offset=10,bytes=22,record_stride=32),
        conclusion='Pool cannot be the untyped canonical binary record and redisplay stream simultaneously. Native registration does not validate capacity or format and still marks malformed/truncated/overflowed names registered.',
        limits=['CPU experiment; sound modeled, native byte copy and metadata registration executed unchanged. Source pool/record/context are explicit fixtures; no natural allocation/IRQ/persistence proof.',
                'Entire11172 cap10 repeated-rank binary and F9FC display routes; fixed-width binary retains marker only when native source begins at marker. Earlier keyboard transfer source+1 issue is separate.',
                'Neighbor writes are intentional negative reproductions inside isolated CPU memory, never user save/ROM. This PASS proves unsafe alternatives rejected, NOT a working save implementation.',
                'Static follow-up also found3355A copying stage02026280+1 to record+10 before3737A/37386 metadata routes. That separate path is NOT executed by this bench; stage-only canonical design cannot be assumed safe for all callers.',
                'Separate canonical ownership, explicit legacy/new selection, all default/import/query consumers and bounded commit remain unresolved. No ROM installation, actual Hangul keyboard screenshot or save/reload claim.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']); require_hash(play,identity)
    print('PASS unsafe native registration counterexamples; NOT safe commit',counts,flush=True)


if __name__=='__main__': main()
