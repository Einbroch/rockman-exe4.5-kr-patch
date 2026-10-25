"""Source/actual032 FD09 native effects; no BIOS/helper substitutions or ROM."""
import struct
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

BASE = 'poc/output/pending500_032_v1.gba'
OUT = 'analysis/pending_insertion_500_033_choice_sfx_cpu_v1/cpu.json'


def main():
    cfg = read('project.json'); sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes()
    meta = read(BASE.replace('.gba', '.json')); require_hash(ROOT/BASE, meta['output_sha256']); rom = (ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    code = [(0x518FC, 0x5190C), (0x519BC, 0x519CA), (0x4FD60, 0x4FD6C), (0x519F4, 0x51A00)]
    data = [(0x50098+4*(0xFD-0xE5), 4), (0x50100+4*(0xFD-0xE5), 4), (0x5190C, 4), (0x51934, 4), (0x51A00, 4), (0x51A28, 4)]
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB); ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB); ranges = []
    for a, b in code:
        raw = source[a:b]; ins = list(cs.disasm(raw, 0x08000000+a))
        if sum(i.size for i in ins) != len(raw) or rom[a:b] != raw: raise ValueError('033 FD09 native code extent/identity')
        for i in ins:
            if i.size not in (2, 4) or i.size == 4 and i.mnemonic != 'bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str, i.address)[0]) != i.bytes:
                raise ValueError('033 FD09 ARMv4T roundtrip')
        ranges.append(dict(offset=a, bytes=b-a, sha256=sha(raw), kind='code'))
    for a, n in data:
        if rom[a:a+n] != source[a:a+n]: raise ValueError('033 FD09 dispatch/table identity')
        ranges.append(dict(offset=a, bytes=n, sha256=sha(source[a:a+n]), kind='data'))
    ptr = lambda at: struct.unpack_from('<I', source, at)[0]
    if [ptr(a) for a in (0x50098+4*(0xFD-0xE5), 0x50100+4*(0xFD-0xE5), 0x5190C, 0x51934, 0x51A00, 0x51A28)] != [0x080518FD, 0x080519F5, 0x08051910, 0x080519BD, 0x08051A04, 2]:
        raise ValueError('033 FD09 exact dispatch binding')
    ctx, stream, stack, stop = 0x0200FA20, 0x02020000, 0x03007F00, 0x080000C0
    cases = []; reference = {}
    for label, image in [('source', source), ('032', rom)]:
        u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T); extent = (len(image)+4095)&~4095
        u.mem_map(0x08000000, extent); u.mem_write(0x08000000, image); u.mem_protect(0x08000000, extent, UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000, 0x40000); u.mem_map(0x03000000, 0x8000); writes = []
        u.hook_add(UC_HOOK_CODE, lambda uc, a, n, d: uc.emu_stop(), begin=stop, end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE, lambda uc, t, a, n, v, d: writes.append((a, n)))
        for high in (0, 0xFF00):
            for low in range(256):
                flag = high|low
                for mode, entry in [('draw', 0x080518FC), ('width', 0x080519F4)]:
                    before = bytearray((i*37+low)&255 for i in range(216)); struct.pack_into('<H', before, 0x3E, flag)
                    wanted = bytearray(before)
                    if mode == 'draw': struct.pack_into('<H', wanted, 0x3E, flag|0x80)
                    u.mem_write(ctx-4, b'\xA6'*4+bytes(before)+b'\xA6'*4); u.mem_write(stream, b'\xFD\x09\xA6\xA6'); u.mem_write(stack-64, b'\xA7'*64)
                    values = [0x1000+i*0x101 for i in range(15)]; values[4] = stream; values[5] = ctx; values[13] = stack; values[14] = stop|1
                    u.reg_write(UC_ARM_REG_CPSR, 0xF0000033)
                    for r, value in zip(REGS, values): u.reg_write(r, value)
                    writes.clear(); u.emu_start(entry|1, 0, count=1000)
                    state = bytes(u.mem_read(ctx, 216)); after = [u.reg_read(r) for r in REGS]
                    if u.reg_read(UC_ARM_REG_PC) != stop or after[13] != stack or after[4] != stream+2 or state != wanted or after[0] != (1 if mode == 'draw' else 2): raise ValueError('033 FD09 native effect/continuation')
                    if any(after[i] != values[i] for i in range(5, 13)) or bytes(u.mem_read(ctx-4, 4))+bytes(u.mem_read(ctx+216, 4)) != b'\xA6'*8 or bytes(u.mem_read(stack-64, 48)) != b'\xA7'*48: raise ValueError('033 FD09 preserved state/canary')
                    if any(not(stack-16 <= a and a+n <= stack or mode == 'draw' and ctx+0x3E <= a and a+n <= ctx+0x40) for a, n in writes): raise ValueError('033 FD09 unmodeled write')
                    full = (after, u.reg_read(UC_ARM_REG_CPSR), state, tuple(writes)); key = (flag, mode)
                    if label == 'source': reference[key] = full
                    elif full != reference[key]: raise ValueError('033 FD09 full source/current effects differ')
                    cases.append(dict(image=label, flags=flag, mode=mode, after_flags=struct.unpack_from('<H', state, 0x3E)[0]))
    frozen_write(ROOT/OUT, dict(schema=1, passed=True, baseline_rom=BASE, baseline_sha256=sha(rom), source_sha256=sha(source),
                 case_count=len(cases), cases=cases, native_ranges=ranges, native_helpers_substituted=[], modeled_services=[],
                 dependencies={'tools/bench_choice_sfx_033.py': sha((ROOT/'tools/bench_choice_sfx_033.py').read_bytes())},
                 rom_written=False, release_eligible=False,
                 limits='FD09 draw only sets0x80 at context+0x3e and advances2; width only advances2. 512flag patterns, all other context bytes/canaries/registers/CPSR/native write effects source/current compared. Not audible sound, selection outcome, caller route, new Korean screen or universal sound-command proof.'))
    print('PASS033 FD09', len(cases), 'native source/032 cases;NO ROM')


if __name__ == '__main__': main()
