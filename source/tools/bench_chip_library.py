#!/usr/bin/env python3
"""Execute final chip-name Thumb bytes with synthetic CPU/memory fixtures.

NOT a GBA runtime or timing proof. Unicorn TI925T executes the Thumb code; the
source CpuSet helper is replaced with its bounded byte-copy contract. Mesen
normal-play evidence must independently verify real BIOS/VRAM consumption.
"""
import argparse
import json
import struct
import sys
from pathlib import Path
from build_visibility_poc import ROOT, require_hash, sha
from archive_scripts import script_spans
from korean_codec import encode_syllable

sys.path.insert(0, str(ROOT / "external/arm_bench_python"))
import unicorn
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument('--consumer', choices=('library','folder'), default='library')
    args = ap.parse_args()
    if args.out.exists():
        raise ValueError("refusing to overwrite CPU bench report")
    if unicorn.__version__ != "2.1.4":
        raise ValueError("CPU bench engine version drift")
    require_hash(ROOT / "external/arm_bench_python/unicorn/lib/unicorn.dll", "010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1")
    require_hash(ROOT / "external/arm_bench_python/unicorn/unicorn_py3/unicorn.py", "b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb")
    manifest = json.loads(args.rom.with_suffix(".json").read_text(encoding="utf-8"))
    require_hash(args.rom, manifest["output_sha256"])
    rom = args.rom.read_bytes()
    folder = args.consumer == 'folder'
    ext = manifest['chip_folder_extension' if folder else 'chip_library_extension']
    spec = json.loads((ROOT / ('tools/specs/exe45_chip_folder_v1.json' if folder else 'tools/specs/exe45_chip_library_v1.json')).read_text(encoding='utf-8'))
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    uc.mem_map(0x08000000, (len(rom) + 0xFFF) & ~0xFFF)
    uc.mem_write(0x08000000, rom)
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_map(0x06000000, 0x18000)
    uc.mem_map(0x0FF00000, 0x1000)
    stop = 0x0FF00000
    writes, copies = [], []
    word_copy = ext.get("copy_policy") == "experimental-inline-16-words"
    cache = ext.get("cache")
    def write_hook(engine, access, address, size, value, user):
        writes.append((address, size))
    uc.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    def helper(engine, address, size, user):
        src, dst, count = [engine.reg_read(r) for r in REGS[:3]]
        if word_copy:
            count = 64
        if count != 64 or not ext["vram"]["start"] <= dst <= ext["vram"]["start"] + ext["vram"]["bytes"] - 64:
            raise ValueError("unbounded glyph copy")
        if (src - 0x08000000 - ext["font_offset"]) % 64 or not 0 <= src - 0x08000000 - ext["font_offset"] < 11172 * 64:
            raise ValueError("glyph copy outside Hangul bank")
        if not word_copy:
            engine.mem_write(dst, bytes(engine.mem_read(src, count)))
        copies.append((src, dst, count))
        if not word_copy:
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR) | 1)
    copy_entry = spec["copy_helper"] & ~1
    if ext.get('copy_policy') == 'experimental-native-fast-bios-16-words':
        copy_entry = 0x0800097C
    if word_copy:
        loads = [i for i in ext["machine_code"][0]["instructions"] if i["mnemonic"] in ("ldm", "ldmia")]
        expected_bursts = 3 if ext.get('copy_variant') == '6+6+4' else 8
        if len(loads) != expected_bursts:
            raise ValueError("word-copy instruction count drift")
        copy_entry = loads[0]["address"]
    stack_renderer = ext.get('stack_renderer')
    if stack_renderer:
        relocated_entry = [None]
        def capture_stack(engine, address, size, user):
            base = engine.reg_read(UC_ARM_REG_R7) & ~1
            if base % 4 or not 0x03000000 <= base <= 0x03008000-stack_renderer['frame_bytes']:
                raise ValueError('stack execution bounds/alignment')
            template = rom[stack_renderer['template_offset']:stack_renderer['template_offset']+stack_renderer['frame_bytes']]
            if bytes(engine.mem_read(base, stack_renderer['frame_bytes'])) != template:
                raise ValueError('stack template supply mismatch')
            relocated_entry[0] = base + copy_entry - ext['machine_code'][0]['address']
        def relocated_copy(engine, address, size, user):
            if address == relocated_entry[0]:
                helper(engine, address, size, user)
        uc.hook_add(UC_HOOK_CODE, capture_stack, begin=stack_renderer['invoke_address'], end=stack_renderer['invoke_address'])
        uc.hook_add(UC_HOOK_CODE, relocated_copy, begin=0x03000000, end=0x03007FFF)
    else:
        uc.hook_add(UC_HOOK_CODE, helper, begin=copy_entry, end=copy_entry)
    def stop_hook(engine, address, size, user):
        engine.emu_stop()
    uc.hook_add(UC_HOOK_CODE, stop_hook, begin=stop, end=stop)
    uc.hook_add(UC_HOOK_CODE, stop_hook, begin=ext["install"]["continuation"] & ~1, end=ext["install"]["continuation"] & ~1)
    total, glyph_copies = 0, 0

    def case(blob, row=0, palette=0xE000, selector=None, count=7, shift=0, lower_shift=0, warm=False,
             owner_context=True, owner_job=28, owner_menu=0, owner_phase=16):
        nonlocal total, glyph_copies
        if folder:
            palette += 16
        top = spec["buffer"]["start"] + row * 32 + shift
        bottom = top + 16 + lower_shift
        stream = 0x02022000
        uc.mem_write(stream, blob)
        if not warm:
            uc.mem_write(0x06000000, b"\xA7" * 0x18000)
            if cache:
                uc.mem_write(cache['tags'], b'\0' * cache['bytes'])
        before_vram = bytes(uc.mem_read(0x06000000, 0x18000))
        uc.mem_write(0x0201E400, b"\xCC" * 0x600)
        before = [0x1230 + n * 4 for n in range(15)]
        before[0], before[2], before[3], before[6] = stream, top, bottom, palette
        before[9], before[13], before[14] = count, 0x03007000, stop | 1
        if folder and ext.get('owner_guard'):
            context=ext['owner_guard']['context']
            before[10]=context if owner_context else context-4
            uc.mem_write(context,struct.pack('<I',0x0200FD50))
            uc.mem_write(context+0x34,struct.pack('<I',0x0200F970))
            uc.mem_write(0x0200FD50,bytes([owner_job]))
            uc.mem_write(0x0200F970,bytes([owner_menu,owner_phase]))
        expected_stream = stream
        if selector:
            root, index, private = selector
            before[0], before[1] = root, index if folder else index << 24
            selected_pool = 0x08000000 + ext["clone_offset"] if private else root
            expected_stream = selected_pool + int.from_bytes(uc.mem_read(selected_pool + index * 2, 2), "little")
            before[14] = 0x08041111
        for r, value in zip(REGS, before):
            uc.reg_write(r, value)
        writes.clear(); copies.clear()
        start = ext["install"]["offset"] if selector else ext["renderer_offset"]
        uc.emu_start(0x08000001 + start, 0, count=20000)
        expected_pc = ext["install"]["continuation"] & ~1 if selector else stop
        if uc.reg_read(UC_ARM_REG_PC) != expected_pc:
            raise ValueError("CPU bench did not reach the declared return")
        after = [uc.reg_read(r) for r in REGS]
        if any(after[n] != before[n] for n in range(4, 14)) or after[2:4] != [top + 16, bottom + 16] or after[0] != expected_stream + len(blob) - 1:
            raise ValueError(f"register/stream ABI failed in vector {total}: {before} -> {after}")
        if selector and after[14] != ext["install"]["continuation"]:
            raise ValueError("selector LR differs from overwritten BL")
        native = bool(selector and not selector[2])
        expected_top, expected_bottom, expected_copies, at, cell = [], [], [], 0, 0
        expected_tags = []
        while blob[at] != 0xE5:
            if blob[at:at + 2] == b"\xF9\xFC":
                index = int.from_bytes(blob[at + 2:at + 4], "little")
                dst = ext["vram"]["start"] + row * 512 + cell * 64
                src = 0x08000000 + ext["font_offset"] + index * 64
                tile = (dst - ext["vram"]["char_base"]) // 32
                if folder:
                    tile -= palette & 0xFFF
                tag_at = cache['tags'] - 0x06000000 + (row * 8 + cell) * 2 if cache else None
                hit = cache and int.from_bytes(before_vram[tag_at:tag_at+2], 'little') == index + 1
                if not hit:
                    expected_copies.append((src, dst, 64))
                if cache:
                    expected_tags.append((tag_at, index + 1))
                if bytes(uc.mem_read(dst, 64)) != rom[src - 0x08000000:src - 0x08000000 + 64]:
                    raise ValueError("glyph pixels did not reach bounded cell")
                at += 4
            else:
                tile = blob[at] * 2
                at += 1
            expected_top.append(palette + tile); expected_bottom.append(palette + tile + 1); cell += 1
        expected_top += [0] * (8 - cell); expected_bottom += [0] * (8 - cell)
        if bytes(uc.mem_read(top, 16)) != struct.pack("<8H", *expected_top) or bytes(uc.mem_read(bottom, 16)) != struct.pack("<8H", *expected_bottom) or copies != expected_copies:
            raise ValueError("tile/padding/copy contract mismatch")
        if after[1] != 0xE5:
            raise ValueError("terminal register changed")
        for address, size in writes:
            if cache and cache['tags'] <= address and address + size <= cache['tags'] + cache['bytes']:
                continue
            if word_copy and any(dst <= address and address + size <= dst + n for src, dst, n in expected_copies):
                continue
            # Selector 20 + invocation 36 + renderer 20 + miss/burst 36.
            stack_low = 0x03007000 - (stack_renderer['frame_bytes'] + 112) if stack_renderer else 0x03006F80
            if not (top <= address and address + size <= top + 16 or bottom <= address and address + size <= bottom + 16 or stack_low <= address and address + size <= 0x03007000):
                raise ValueError("unintended CPU memory write")
        expected_vram = bytearray(before_vram)
        for src, dst, size in expected_copies:
            expected_vram[dst - 0x06000000:dst - 0x06000000 + size] = rom[src - 0x08000000:src - 0x08000000 + size]
        for at, tag in expected_tags:
            expected_vram[at:at+2] = tag.to_bytes(2, 'little')
        if bytes(uc.mem_read(0x06000000, 0x18000)) != expected_vram:
            raise ValueError("VRAM collateral change")
        total += 1; glyph_copies += len(copies)

    vectors = [b"\xE5", b"\x02" * 8 + b"\xE5", encode_syllable("가") * 8 + b"\xE5",
               encode_syllable("힣") * 8 + b"\xE5", encode_syllable("괜") + b"\x02" + encode_syllable("찮") + b"\xE5"]
    for row in range(7):
        for palette in (0, 0xD000, 0xE000, 0xF000):
            for blob in vectors:
                case(blob, row, palette)
    boundaries = total
    for index in range(11172):
        blob = b"\x02" * (index % 8) + encode_syllable(chr(0xAC00 + index)) + b"\xE5"
        case(blob, index % 7)
        if cache:
            case(blob, index % 7, warm=True)
            case(b"\x02" * (index % 8) + encode_syllable(chr(0xAC00 + (index + 1) % 11172)) + b"\xE5", index % 7, warm=True)
    pool = spec["pool"]
    native_spans = script_spans(rom[pool["offset"]:pool["offset"] + pool["bytes"]], pool["scripts"])
    private_spans = script_spans(rom[ext["clone_offset"]:ext["clone_offset"] + ext["clone"]["clone_bytes"]], pool["scripts"])
    for index, blob in enumerate(private_spans):
        if blob:
            case(blob, index % 7, selector=(0x08000000 + pool["offset"], index, True))
    guards = [dict(count=5), dict(shift=0x100), dict(shift=2), dict(lower_shift=2), dict(palette=0xE002)]
    if folder and ext.get('owner_guard'):
        guards += [dict(owner_context=False),dict(owner_job=16),dict(owner_menu=8),dict(owner_phase=12)]
    for values in guards:
        case(native_spans[1], selector=(0x08000000 + pool["offset"], 1, False), **values)
    secondary = script_spans(rom[0x765B18:0x765B18 + 1103], 137)
    for index, blob in enumerate(secondary):
        if blob:
            case(blob, selector=(0x08765B18, index, False))
    result = {"schema": 1, "rom_sha256": sha(rom), "tool_sha256": sha(Path(__file__).read_bytes()),
              "scope": "synthetic CPU execution, not normal play or GBA timing; bounded CpuSet helper substituted",
              "engine": "Unicorn 2.1.4, TI925T model", "vectors": total, "boundary_vectors": boundaries,
              "hangul_indices": 11172, "glyph_copies": glyph_copies, "register_memory_tile_checks": True,
              "selector_guard_vectors": len(guards), "source_pointer_updates": 0}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if word_copy:
        result["scope"] = "synthetic CPU execution of actual inline word loads/stores; NOT GBA runtime or timing"
        result["copy_policy"] = ext["copy_policy"]
    if stack_renderer:
        result['stack_execution'] = 'actual copied Thumb bytes; template supply, alignment, bounded stack and register checks'
    if ext.get('copy_policy') == 'experimental-native-fast-bios-16-words':
        result['scope'] = 'synthetic CPU execution; bounded native fast BIOS copy contract substituted; NOT GBA runtime or timing'
        result['copy_policy'] = ext['copy_policy']
    if cache and folder:
        for test in range(15 if ext.get('owner_guard') else 3):
            fill=(0,0xA7,0xFF)[test%3]
            mode=test//3
            before = [0x1230+n*4 for n in range(15)]
            before[5],before[13],before[14]=0x0200F970,0x03007000,0x0803D941
            for reg,value in zip(REGS,before):
                uc.reg_write(reg,value)
            uc.mem_write(before[5],b'\xCC'*0x100)
            if ext.get('owner_guard'):
                context=ext['owner_guard']['context']
                before[10]=context if mode!=1 else context-4
                uc.reg_write(REGS[10],before[10])
                uc.mem_write(context,struct.pack('<I',0x0200FD50))
                uc.mem_write(context+0x34,struct.pack('<I',before[5]))
                uc.mem_write(0x0200FD50,bytes([16 if mode==2 else 28]))
                uc.mem_write(before[5],bytes([8 if mode==3 else 0,12 if mode==4 else 16]))
            before_menu=bytes(uc.mem_read(before[5],0x100))
            uc.mem_write(before[13],struct.pack('<I',stop|1))
            uc.mem_write(0x06000000,bytes([fill])*0x18000)
            writes.clear()
            uc.emu_start(0x08000001+cache['reset_install'],0,count=2000)
            after=[uc.reg_read(reg) for reg in REGS]
            expected=before.copy()
            expected[0]=0x7FFF;expected[13]+=4
            if after!=expected or uc.reg_read(UC_ARM_REG_PC)!=stop:
                raise ValueError('folder native initializer POP-PC reset ABI')
            menu=bytearray(before_menu);menu[0x48:0x4C]=struct.pack('<I',0x7FFF)
            if bytes(uc.mem_read(before[5],0x100))!=menu:
                raise ValueError('folder reset source store/collateral')
            video=bytearray(bytes([fill])*0x18000)
            at=cache['tags']-0x06000000
            if mode==0:
                video[at:at+cache['bytes']]=b'\0'*cache['bytes']
            if bytes(uc.mem_read(0x06000000,0x18000))!=video:
                raise ValueError('folder reset tag extent')
            stack_low=0x03006FEC if ext.get('owner_guard') else 0x03006FF0
            if any(not (cache['tags']<=a and a+n<=cache['tags']+cache['bytes'] or before[5]+0x48<=a and a+n<=before[5]+0x4C or stack_low<=a and a+n<=0x03007000) for a,n in writes):
                raise ValueError('folder reset unintended write')
        result['cache_checks']={'cold_hit_change_each_hangul':11172,'reset_vectors':15 if ext.get('owner_guard') else 3,
                                'actual_native_pop_pc':True,'runtime_invalidation':'pending'}
        result['consumer']='folder-seven-row-tilemap'
    if cache and not folder:
        uc.hook_add(UC_HOOK_CODE, stop_hook, begin=cache['reset_continuation'] & ~1, end=cache['reset_continuation'] & ~1)
        lz_calls = []
        def lz_contract(engine, address, size, user):
            lz_calls.append((engine.reg_read(REGS[0]), engine.reg_read(REGS[1])))
            for reg, value in zip(REGS[:4], (0x2011110, 0x2022220, 0x3333, 0x4444)):
                engine.reg_write(reg, value)
            # Substitute only SWI work; execute the actual BX LR at EC15A.
            # Forcing LR|1 here hid the v1 interworking defect.
            engine.reg_write(UC_ARM_REG_PC, 0x080EC15B)
        uc.hook_add(UC_HOOK_CODE, lz_contract, begin=0x080EC158, end=0x080EC158)
        for fill in (0, 0xA7, 0xFF):
            before = [0x1230 + n * 4 for n in range(15)]
            before[13] = 0x03007000
            for reg, value in zip(REGS, before):
                uc.reg_write(reg, value)
            uc.mem_write(0x06000000, bytes([fill]) * 0x18000)
            writes.clear()
            uc.emu_start(0x08000001 + cache['reset_install'], 0, count=2000)
            after = [uc.reg_read(reg) for reg in REGS]
            if after[:4] != [0x2011110, 0x2022220, 0x3333, 0x4444] or after[4:14] != before[4:14] or after[14] != cache['reset_continuation']:
                raise ValueError('reset hook ABI')
            if uc.reg_read(UC_ARM_REG_PC) != cache['reset_continuation'] & ~1:
                raise ValueError('reset return')
            expected = bytearray(bytes([fill]) * 0x18000)
            at = cache['tags'] - 0x06000000
            expected[at:at+cache['bytes']] = b'\0' * cache['bytes']
            if bytes(uc.mem_read(0x06000000, 0x18000)) != expected:
                raise ValueError('reset tag extent')
            if any(not (cache['tags'] <= a and a+n <= cache['tags']+cache['bytes'] or 0x03006F80 <= a and a+n <= 0x03007000) for a,n in writes):
                raise ValueError('reset collateral write')
        pointers = tuple(struct.unpack_from('<I', rom, at)[0] for at in (0x428E8, 0x428EC))
        if lz_calls != [pointers] * 3:
            raise ValueError('reset native loader arguments')
        result['cache_checks'] = {'cold_hit_change_each_hangul': 11172, 'reset_vectors': 3,
                                  'native_lz_contract_substituted': True, 'runtime_invalidation': 'pending'}
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"CPU bench passed {total} vectors / {glyph_copies} bounded glyph copies")


if __name__ == "__main__":
    main()
