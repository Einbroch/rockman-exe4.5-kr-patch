"""Execute native guard handlers/providers; CPU evidence, not GBA render proof."""
import struct
from collections import Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
import extended_dialogue
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from bench_chip_library import REGS
import unicorn
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR

OUT = 'analysis/pending_insertion_500_023_guard_v1/native_guard_cpu.json'


def main():
    cfg = read('project.json')
    sp = ROOT / cfg['source_profile']['filename']
    require_hash(sp, cfg['source_profile']['sha256'])
    source = sp.read_bytes()
    rp = ROOT / 'poc/output/pending500_022_v2.gba'
    meta = read(rp.with_suffix('.json'))
    require_hash(rp, meta['output_sha256'])
    rom = rp.read_bytes()
    # Exact, separately bounded code/data regions. None of these native paths
    # may inherit changes from an existing patch when evidence is reused.
    regions = [(0x500BC, 4), (0x507F4, 20), (0x50808+0x2D*4, 12),
        (0x50C48, 76), (0x50CD4+0x24*2, 8), (0x50DB0, 30),
        (0x496D4, 98), (0xCEC, 8), (0x287B2, 24),
        (0x2E580, 16), (0x4FD18, 96), (0x5543C, 44), (0x92C,32), (0xEC140,4)]
    # Read the provider table from the verified weekday-handler literal.
    table = struct.unpack_from('<I', source, 0x50C90)[0]
    regions[4] = (table - 0x08000000 + 0x24*2, 8)
    code_refs = []
    for at, n in regions:
        if rom[at:at+n] != source[at:at+n]:
            raise ValueError('Actual022 native guard/provider code changed')
        code_refs.append(dict(offset=at, bytes=n, sha256=sha(source[at:at+n])))
    if (struct.unpack_from('<I',source,0x500BC)[0] != 0x080507F5
            or struct.unpack_from('<I',source,0x50804)[0] != 0x08050808
            or struct.unpack_from('<I',source,0x50808+0x2D*4)[0] != 0x08050C49
            or struct.unpack_from('<I',source,0x50808+0x2F*4)[0] != 0x08050DB1
            or struct.unpack_from('<II',source,table-0x08000000+0x24*2) != (0,0x0802E581)):
        raise ValueError('Source dispatch/provider contract')
    date_base = struct.unpack_from('<I',source,0x2E58C)[0]
    if not 0x02000000 <= date_base < 0x0203F000:
        raise ValueError('Native weekday data basis')
    if unicorn.__version__ != '2.1.4':
        raise ValueError('CPU version drift')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base, n in ((0x08000000,(len(rom)+4095)&~4095),(0x02000000,0x40000),(0x03000000,0x8000),(0x04000000,0x1000),(0x05000000,0x1000),(0x06000000,0x20000),(0x07000000,0x1000)):
        u.mem_map(base,n)
    u.mem_write(0x08000000,rom)
    ctx,glob,navictx,flags,archive,stream,stack,stop = 0x02020000,0x02000100,0x02000200,0x02010000,0x02030000,0x02035000,0x03007E00,0x0203F000
    fake = b''.join(struct.pack('<H',510+i*4) for i in range(255)) + bytes([0xE5])*1020
    u.mem_write(archive,fake)
    u.mem_write(glob+64,struct.pack('<I',navictx))
    u.mem_write(glob+72,struct.pack('<I',flags))
    writes, visited, clears = [], set(), []
    def fast_clear(uc,a,n,data):
        src,dst,mode = [uc.reg_read(REGS[i]) for i in (0,1,2)]
        count = (mode & 0x1FFFFF) * 4
        if mode & ~0x1FFFFF != 0x01000000 or count!=0xF00 or dst not in (0x02012F50,0x02013E50) or bytes(uc.mem_read(src,4))!=bytes(4):
            raise ValueError(f'Original jump CpuFastSet clear contract: src={src:X} dst={dst:X} mode={mode:X}')
        uc.mem_write(dst,bytes(count));writes.append((dst,count));clears.append((dst,count))
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,fast_clear,begin=0x080EC140,end=0x080EC140)
    u.hook_add(UC_HOOK_CODE, lambda uc,a,n,data: uc.emu_stop(), begin=stop,end=stop)
    u.hook_add(UC_HOOK_CODE, lambda uc,a,n,data: visited.add(a))
    u.hook_add(UC_HOOK_MEM_WRITE, lambda uc,access,a,n,v,data: writes.append((a,n)))
    cases=[]
    def run(blob,navi,flag_bits,weekday,branch):
        u.mem_write(stream,blob)
        u.mem_write(navictx+1,bytes([navi]))
        fb=bytearray(0x1000)
        for bit in range(4):
            if flag_bits&(1<<bit):
                index=0x5C+navi*4+bit
                fb[index//8] |= 0x80>>(index%8)
        u.mem_write(flags,bytes(fb))
        u.mem_write(date_base+11,bytes([weekday]))
        original=bytearray([0xA7]*216)
        struct.pack_into('<I',original,0x30,archive)
        u.mem_write(ctx,bytes(original))
        u.mem_write(stack-128,bytes([0xCC])*128)
        values=[0x1100+i*0x101 for i in range(15)]
        values[4]=stream;values[5]=ctx;values[10]=glob;values[13]=stack;values[14]=stop|1
        for r,v in zip(REGS,values):u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_CPSR,0xA0000033)
        writes.clear();visited.clear();clears.clear()
        try:
            u.emu_start(0x080507F5,0,count=2000)
        except unicorn.UcError as ex:
            raise ValueError(f'CPU fixture fault pc={u.reg_read(UC_ARM_REG_PC):08X} lr={u.reg_read(REGS[14]):08X} command={blob.hex()} navi={navi} bits={flag_bits} visited={sorted(visited)[-15:]}') from ex
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[0])!=1 or u.reg_read(REGS[13])!=stack:
            raise ValueError('Native guard return/stack contract')
        now=bytes(u.mem_read(ctx,216))
        if branch==255:
            if now!=original or u.reg_read(REGS[4])!=stream+len(blob) or 0x0804FD18 in visited or clears:
                raise ValueError('Continue modifies message state or length')
        else:
            destination=archive+510+branch*4
            if u.reg_read(REGS[4])!=destination or now[1]!=branch or any(struct.unpack_from('<I',now,p)[0]!=destination for p in (0x2C,0x34)) or 0x0804FD18 not in visited or clears!=[(0x02012F50,0xF00),(0x02013E50,0xF00)]:
                raise ValueError('Original script jump/offset consumer')
        if any(not(ctx<=a and a+n<=ctx+216 or stack-96<=a and a+n<=stack or (a,n) in clears) for a,n in writes):
            raise ValueError('Guard writes outside native context/temporary stack/original clear buffers')
        if bytes(u.mem_read(stream,len(blob)))!=blob or bytes(u.mem_read(archive,len(fake)))!=fake:
            raise ValueError('Guard changes stream/archive')
        if any(u.reg_read(REGS[r])!=values[r] for r in (5,8,9,10,11,12)):
            raise ValueError('Guard preserved native registers')
    # All registration bit patterns for every native Navi, tested mask4 used by
    # selected script10. Exercise each jump-slot as target and FF continuation.
    for navi in range(23):
        for bits in range(16):
            first=next((i for i in range(4) if bits&(1<<i)),None)
            answer=0 if first is None else 1 if first==2 else 2
            for continuation in range(8):
                targets=[255 if continuation&(1<<i) else 29+i for i in range(3)]
                run(bytes([0xEE,0x2F,4,*targets]),navi,bits,1,targets[answer])
                cases.append(dict(kind='tournament',navi=navi,flag_bits=bits,targets=targets,branch=targets[answer]))
    # The two singleton ranges actually used by selected scripts26/29.
    for day in range(7):
        for check_day in (0,6):
            for yes,no in ((34,255),(255,34),(34,30),(255,255)):
                branch=yes if day==check_day else no
                run(bytes([0xEE,0x2D,0x24,check_day,check_day,yes,no]),0,0,day,branch)
                cases.append(dict(kind='weekday',weekday=day,range=[check_day,check_day],targets=[yes,no],branch=branch))
    if bytes(u.mem_read(0x08000000,len(rom)))!=rom:
        raise ValueError('CPU fixture mutated ROM')
    d=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    native_isa=[]
    for at,n in ((0x507F4,16),(0x50C48,70),(0x50DB0,30),(0x496D4,48),(0x49708,44),(0xCEC,8),(0x287B2,24),(0x2E580,6)):
        ins=list(d.disasm(source[at:at+n],0x08000000+at))
        if sum(i.size for i in ins)!=n:
            raise ValueError('Native code boundaries')
        native_isa.append(dict(offset=at,bytes=n,instructions=[dict(address=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins]))
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),native_code=code_refs,decoded_regions=native_isa,weekday_provider_data=date_base,case_counts=dict(Counter(c['kind'] for c in cases)),cases=cases,all_native_providers_executed=True,only_substituted_helper='BIOS CpuFastSet via native080EC140; exact zero-fill two original0xF00 buffers on branch',continue_message_context_byte_identical=True,branch_uses_original_script_jump=True,branch_original_context_and_graphics_clear_retained=True,rom_written=False,release_eligible=False,limits='Synthetic Unicorn TI925T Thumb fixtures on actual022 native code. Mask4, all23 Navi and16 registration patterns, seven valid weekday values and ranges0/6. Native providers/command dispatch/jump/clear callers run unchanged; BIOS fast-clear substituted with checked memory contract. No GBA drawing, natural event reachability, timing, complete guard-prefix integration or new product ROM claim.'))
    print('PASS native guard CPU',len(cases),'vectors; native providers; BIOS-only clear substitution; no ROM written')


if __name__=='__main__':main()
