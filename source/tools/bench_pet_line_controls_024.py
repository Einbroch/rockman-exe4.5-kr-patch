"""Execute source/023 native LF, width-LF, clear and hold handlers unchanged.

CPU fixture only, not GBA rendering. CpuFastSet is the sole substituted helper;
its concrete destination/size/zero-fill contract is recorded and checked.
"""
import struct
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from bench_chip_library import REGS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_TI925T


def main(out='analysis/pending_insertion_500_024_native_controls_v2/cpu.json'):
    cfg = read('project.json')
    sp = ROOT/cfg['source_profile']['filename']
    require_hash(sp, cfg['source_profile']['sha256'])
    source = sp.read_bytes()
    path = 'poc/output/pending500_023_v1.gba'
    expected = '6e6d9104db33fd927714b4a06cd6a1093fd4b6ef6d4f77c6ecd206daa44a39ec'
    require_hash(ROOT/path, expected)
    rom = (ROOT/path).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    # Fixed source coordinates from the E5-based normal/width dispatch tables.
    slots = {op: (struct.unpack_from('<I', source, 0x50098+(op-0xE5)*4)[0], struct.unpack_from('<I', source, 0x50100+(op-0xE5)*4)[0]) for op in (0xE8, 0xED, 0xF1)}
    if slots != {0xE8: (0x08050381, 0x080503B1), 0xED: (0x08050755, 0x080507F1), 0xF1: (0x080510BD, 0x08051125)}:
        raise ValueError('Native command dispatch identity')
    ranges = [(table+(op-0xE5)*4, 4) for table in (0x50098, 0x50100) for op in slots] + [(0x4FD60, 0x18), (0x50380, 0x3E), (0x50754, 0x9A), (0x510BC, 0x6C), (0x553E8, 0x30), (0x5543C, 0x2C), (0x92C, 0x20), (0x4F6E8, 8), (0xEC140,4)]
    for off, size in ranges:
        if source[off:off+size] != rom[off:off+size]:
            raise ValueError('023 native control applicability')
    if struct.unpack_from('<I', source, 0x503AC)[0] != 0x0804F6E8 or struct.unpack_from('<2I', source, 0x4F6E8) != (10752, 21504):
        raise ValueError('LF two additional physical rows')
    ctx, stream, stack, stop = 0x0200FA20, 0x02020000, 0x03007F00, 0x080000C0
    effects = {}
    cases = []
    for label, image in (('source', source), ('023', rom)):
        u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        u.mem_map(0x08000000, (len(image)+4095)&~4095)
        u.mem_write(0x08000000, image)
        u.mem_map(0x02000000, 0x40000)
        u.mem_map(0x03000000, 0x8000)
        u.mem_map(0x06000000, 0x20000)
        writes, fills = [], []
        u.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, data: writes.append((address, size)))
        u.hook_add(UC_HOOK_CODE, lambda uc, a, n, data: uc.emu_stop(), begin=stop, end=stop)
        def cpuset(uc, address, size, data):
            src, dst, flags = (uc.reg_read(REGS[i]) for i in range(3))
            count = (flags & 0x1FFFF)*4
            if flags != 0x010003C0 or dst not in (0x02012F50, 0x02013E50) or bytes(uc.mem_read(src, 4)) != bytes(4):
                raise ValueError('Native clear CpuFastSet exact contract '+str((hex(src),hex(dst),hex(flags),bytes(uc.mem_read(src,4)).hex())))
            uc.mem_write(dst, bytes(count))
            fills.append(dict(destination=dst, bytes=count, value=0))
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(REGS[14]))
        u.hook_add(UC_HOOK_CODE, cpuset, begin=0x080EC140, end=0x080EC140)
        def execute(entry, command, row, width, flags=0, speed=0):
            u.mem_write(ctx, bytes(216))
            u.mem_write(ctx+0xF, bytes([row]))
            u.mem_write(ctx+8, bytes([speed]))
            u.mem_write(ctx+0x18, bytes([92, 110]))
            u.mem_write(ctx+0x3E, struct.pack('<H', flags))
            u.mem_write(ctx+0x70, struct.pack('<I', width))
            u.mem_write(ctx+0x7C, struct.pack('<I', row*10752+width*4))
            u.mem_write(ctx+0x8C, struct.pack('<I', 0xAABBCCDD))
            u.mem_write(ctx+0x34, struct.pack('<I', stream-25))
            u.mem_write(0x0200FB24, bytes(4))
            u.mem_write(stream, command)
            u.mem_write(0x02012F50-4, b'LEFT'+b'\xA5'*7680+b'RGHT')
            for i, reg in enumerate(REGS):
                u.reg_write(reg, 0x12340000+i)
            for i, value in ((4, stream), (5, ctx), (13, stack), (14, stop|1)):
                u.reg_write(REGS[i], value)
            u.reg_write(UC_ARM_REG_CPSR, 0xF0000033)
            writes.clear(); fills.clear()
            u.emu_start(entry, 0, count=1000)
            if u.reg_read(UC_ARM_REG_PC) != stop or u.reg_read(REGS[13]) != stack or u.reg_read(REGS[5]) != ctx:
                raise ValueError('Control return/stack/context ABI')
            for at, n in writes:
                if not (ctx <= at and at+n <= ctx+216 or 0x0200FB24 <= at and at+n <= 0x0200FB28 or stack-128 <= at and at+n <= stack):
                    raise ValueError('Unexpected persistent write '+hex(at))
            result = dict(row=bytes(u.mem_read(ctx+0xF, 1))[0], width=struct.unpack('<I', u.mem_read(ctx+0x70, 4))[0], render_offset=struct.unpack('<I', u.mem_read(ctx+0x7C, 4))[0], overflow=struct.unpack('<I', u.mem_read(ctx+0x8C, 4))[0], flags=struct.unpack('<H', u.mem_read(ctx+0x3E, 2))[0], stream=u.reg_read(REGS[4]), fills=list(fills))
            return result
        def keep(kind, row, width, r):
            key = (kind, row, width)
            if label == 'source':
                effects[key] = r
            elif r != effects[key]:
                raise ValueError('023 differs from source native effect')
            cases.append(dict(image=label, kind=kind, input_row=row, input_width=width, **r))
        for row in range(3):
            for width in (0, 12, 132):
                r = execute(slots[0xE8][0], b'\xE8\xE6\x00', row, width, flags=0x100)
                if (r['row'], r['width'], r['flags'], r['stream']) != (row+1, width, 0x101, stream+1):
                    raise ValueError('LF effect')
                if row < 2:
                    if r['render_offset'] != (row+1)*10752 or r['overflow'] != 0xAABBCCDD:
                        raise ValueError('LF row extent')
                elif r['overflow'] != 1 or r['render_offset'] != row*10752+width*4:
                    raise ValueError('LF fourth-row overflow sentinel')
                keep('draw-LF', row, width, r)
                r = execute(slots[0xE8][1], b'\xE8', row, width)
                if (r['row'], r['width'], r['stream']) != (row+1, 0, stream+1):
                    raise ValueError('Width LF effect')
                keep('width-LF', row, width, r)
                r = execute(slots[0xF1][0], b'\xF1\xED\xFF\x00\x00', row, width)
                if r['row'] or r['width'] or r['render_offset'] or r['stream'] != stream+1 or r['fills'] != [dict(destination=0x02012F50, bytes=3840, value=0), dict(destination=0x02013E50, bytes=3840, value=0)]:
                    raise ValueError('Clear reset contract')
                if bytes(u.mem_read(0x02012F50-4, 7688)) != b'LEFT'+bytes(7680)+b'RGHT':
                    raise ValueError('Clear extent/guard')
                keep('clear-all-rows', row, width, r)
                r = execute(slots[0xED][0], b'\xED\xFF\x00\x00', row, width)
                if r['stream'] != stream or r['row'] != row or r['width'] != width or not r['flags'] & 1 or fills:
                    raise ValueError('Terminal hold progression')
                keep('terminal-hold', row, width, r)
    frozen_write(ROOT/out, dict(schema=1, passed=True, source_sha256=sha(source), baseline_rom=path, baseline_sha256=sha(rom), native_ranges=[dict(offset=o, bytes=n, sha256=sha(source[o:o+n])) for o,n in ranges], native_slots=slots, row_offsets=[0,10752,21504], overflow_on_fourth_row=True, source_and_023_effects_identical=True, cases=cases, case_count=len(cases), substituted_helpers=['0x080EC140 CpuFastSet SWI0C, exact zero-fill destination/count contract only'], dependencies={'tools/bench_pet_line_controls_024.py':sha((ROOT/'tools/bench_pet_line_controls_024.py').read_bytes())}, rom_written=False, runtime_tested=False, release_eligible=False, limits='Actual native instruction CPU fixture of LF/width/clear/hold; not glyph pixels, actual BIOS DMA, normal quick-window reachability or candidate024 ROM. Additional LF is viable only within3 aggregate rows; production layout policy/source-binding and GBA display/clear/reentry evidence still required.'))
    print('PASS source/023 native control CPU', len(cases), 'cases;3rows, fourth-row overflow, full clear, terminal hold;no ROM written')


if __name__ == '__main__':
    main()
