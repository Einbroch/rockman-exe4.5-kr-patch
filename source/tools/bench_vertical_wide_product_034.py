"""F608 widths11..13 in explicit normal flags2/0x82, source/actual032 CPU."""
import struct
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T

OUT = 'analysis/pending500_034_v1/vertical_wide_cpu.json'


def main():
    cfg = read('project.json'); sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes()
    base = 'poc/output/pending500_034_v1.gba'; m = read(base.replace('.gba', '.json')); require_hash(ROOT/base, m['output_sha256']); rom = (ROOT/base).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB); ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB); ranges = []
    for a, b in [(0x520A4, 0x520F6), (0x52134, 0x5213E), (0x3B3B8, 0x3B3C2), (0x4FD78, 0x4FD82)]:
        raw = source[a:b]; ins = list(cs.disasm(raw, 0x08000000+a))
        if rom[a:b] != raw or sum(i.size for i in ins) != len(raw): raise ValueError('033 wide vertical code applicability')
        for i in ins:
            if i.size not in (2, 4) or i.size == 4 and i.mnemonic != 'bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str, i.address)[0]) != i.bytes: raise ValueError('033 wide vertical ARMv4T roundtrip')
        ranges.append(dict(offset=a, bytes=b-a, sha256=sha(raw), kind='code'))
    for a, n in [(0x500DC, 4), (0x50144, 4), (0x51F64, 4), (0x3B468, 4), (0x52140, 14)]:
        if source[a:a+n] != rom[a:a+n]: raise ValueError('033 wide vertical dispatch/literal identity')
        ranges.append(dict(offset=a, bytes=n, sha256=sha(source[a:a+n]), kind='data'))
    ptr = lambda at: struct.unpack_from('<I', source, at)[0]
    if [ptr(a) for a in (0x500DC, 0x50144, 0x51F64)] != [0x08051F31, 0x08052135, 0x080520A5]: raise ValueError('033 wide vertical dispatch binding')
    ctx, stream, stack, stop = 0x0200FA20, 0x02020000, 0x03007F00, 0x080000C0; query = ptr(0x3B468)
    cases = []; reference = {}
    for label, image in [('source', source), ('032', rom)]:
        u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T); extent = (len(image)+4095)&~4095
        u.mem_map(0x08000000, extent); u.mem_write(0x08000000, image); u.mem_protect(0x08000000, extent, UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000, 0x40000); u.mem_map(0x03000000, 0x8000); writes = []
        u.hook_add(UC_HOOK_CODE, lambda uc, a, n, d: uc.emu_stop(), begin=stop, end=stop)
        u.hook_add(UC_HOOK_MEM_WRITE, lambda uc, t, a, n, v, d: writes.append((a, n)))
        for width in (11, 12, 13):
            for flags in (2, 0x82):
                for mode in (0, 1):
                    for row in range(3):
                        for phase, entry in [('draw', 0x080520A4), ('width', 0x08052134)]:
                            before = bytearray(216); before[0x18] = 52; struct.pack_into('<H', before, 0x3E, flags); struct.pack_into('<I', before, 0x7C, row*10752)
                            allocation = 11*width+8; relative = ((166 if mode else 176)-allocation)//2; wanted = bytearray(before)
                            if not 0 <= relative or not 8 <= 52+relative < 52+relative+allocation <= 234: raise ValueError('033 declared wide vertical normal geometry')
                            if phase == 'draw':
                                wanted[0x94] = 52+relative; struct.pack_into('<I', wanted, 0x7C, row*10752+4*relative)
                            u.mem_write(ctx-4, b'\xA6'*4+bytes(before)+b'\xA6'*4); u.mem_write(query+8, struct.pack('<I', mode)); u.mem_write(stream, bytes([0xF6, 8, width])); u.mem_write(stack-64, b'\xA7'*64)
                            values = [0x1000+i*0x101 for i in range(15)]; values[4] = stream; values[5] = ctx; values[13] = stack; values[14] = stop|1
                            u.reg_write(UC_ARM_REG_CPSR, 0xF0000033)
                            for r, value in zip(REGS, values): u.reg_write(r, value)
                            writes.clear(); u.emu_start(entry|1, 0, count=1000); state = bytes(u.mem_read(ctx, 216)); regs = [u.reg_read(r) for r in REGS]
                            if u.reg_read(UC_ARM_REG_PC) != stop or regs[13] != stack or regs[4] != stream+3 or state != wanted: raise ValueError('033 native wide vertical context/continuation')
                            if any(regs[i] != values[i] for i in range(5, 13)) or bytes(u.mem_read(ctx-4, 4))+bytes(u.mem_read(ctx+216, 4)) != b'\xA6'*8 or bytes(u.mem_read(stack-64, 32)) != b'\xA7'*32: raise ValueError('033 wide vertical registers/canaries')
                            if any(not(ctx <= a and a+n <= ctx+216 or stack-32 <= a and a+n <= stack) for a, n in writes): raise ValueError('033 wide vertical unknown write')
                            key = (width, flags, mode, row, phase); effect = (regs, u.reg_read(UC_ARM_REG_CPSR), state, tuple(writes))
                            if label == 'source': reference[key] = effect
                            elif reference[key] != effect: raise ValueError('033 source/current wide vertical effects')
                            cases.append(dict(image=label, width=width, flags=flags, mode=mode, row=row, phase=phase, allocation=allocation, relative_x=relative))
    frozen_write(ROOT/OUT, dict(schema=1, passed=True, baseline_rom=base, baseline_sha256=sha(rom), source_sha256=sha(source), case_count=len(cases), cases=cases,
                  native_ranges=ranges, dependencies={'tools/bench_vertical_wide_product_034.py': sha((ROOT/'tools/bench_vertical_wide_product_034.py').read_bytes())},
                  native_helpers_substituted=[], modeled_services=[], rom_written=False, release_eligible=False,
                  limits='Only F608 widths11..13 with flags2/0x82, origin52, normal display modes0/1 and rows0..2. Not unpositioned quick, all flags/origins, EA/EC three-choice input/branch outcomes, target label fit, GBA cursor/pixels, clear or product integration.'))
    print('PASS033 wide vertical', len(cases), 'source/032 CPU cases;NO ROM')


if __name__ == '__main__': main()
