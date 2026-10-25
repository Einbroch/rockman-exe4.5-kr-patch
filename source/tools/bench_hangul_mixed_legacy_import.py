"""Bounded legacy import CPU, original leaf comparison and edit connection."""
import json
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from hangul_mixed_legacy_import import assemble, import_legacy
from hangul_mixed_replay_state import MixedReplay, KEYS
from hangul_native_tokens import from_native_word
from hangul_mixed_keyedit_thumb import assemble as assemble_keyedit
from hangul_mixed_rebase_thumb import assemble as assemble_rebase
from hangul_mixed_dispatch_thumb import assemble as assemble_dispatch


def main():
    root = ROOT / 'analysis/hangul_keyboard_v1'; deps = {}
    for name in ('cpu_mixed_rebase', 'cpu_composer'):
        p = root / name / 'report.json'; r = json.loads(p.read_text(encoding='utf8'))
        if not r['passed'] or r.get('rom_integrated', False): raise ValueError('dependency scope')
        for n, h in r['tools'].items(): require_hash(ROOT / 'tools' / n, h)
        for n, h in r['artifacts'].items(): require_hash(p.parent / n, h)
        deps[name] = sha(p.read_bytes())
    legacy_path = root / 'legacy_edit.json'; legacy = json.loads(legacy_path.read_text(encoding='utf8'))
    for n, h in legacy['tools'].items(): require_hash(ROOT / 'tools' / n, h)
    profile = json.loads((ROOT / 'project.json').read_text(encoding='utf8'))['source_profile']
    source_path = ROOT / profile['filename']; require_hash(source_path, profile['sha256']); rom = source_path.read_bytes()
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll', '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob, isa = assemble(0x08800000)
    out = root / 'cpu_mixed_legacy_import'; out.mkdir(exist_ok=True)
    (out / 'helper.bin').write_bytes(blob); blob = (out / 'helper.bin').read_bytes()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, len(rom)); u.mem_write(0x08000000, rom); u.mem_protect(0x08000000, len(rom), UC_PROT_READ | UC_PROT_EXEC)
    u.mem_map(0x08800000, 16384); u.mem_write(0x08800000, blob)
    placed = {}
    for name, address, emitter in (('keyedit', 0x08801000, assemble_keyedit), ('rebase', 0x08803000, assemble_rebase), ('dispatch', 0x08802000, assemble_dispatch)):
        code, proof = emitter(address); placed[name] = proof; u.mem_write(address, code)
    u.mem_protect(0x08800000, 16384, UC_PROT_READ | UC_PROT_EXEC)
    for address, name in ((0x09000000, 'transitions.bin'), (0x09200000, 'deletions.bin')):
        data = (root / 'cpu_composer' / name).read_bytes()
        u.mem_map(address, (len(data)+4095)&~4095); u.mem_write(address, data); u.mem_protect(address, (len(data)+4095)&~4095, UC_PROT_READ)
    u.mem_map(0x09300000, 4096); u.mem_write(0x09300000, struct.pack('<IIII', 0x09000000, 0x09200000, 0x08801001, 0x08803001)); u.mem_protect(0x09300000, 4096, UC_PROT_READ)
    u.mem_map(0x02000000, 0x40000); u.mem_protect(0x02000000, 4096, UC_PROT_READ)
    u.mem_map(0x03007000, 4096); u.mem_map(0x0FF00000, 4096)
    src, dest, sp, stop = 0x02000101, 0x02001103, 0x03007F00, 0x0FF00000
    regs = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
    counts = dict(import_calls=0, rejected=0, byte_pair_domain=0, token_capacity_slot_paths=0,
                  original_leaf_comparisons=0, native_import_edit_undo_paths=0, edit_calls=0)

    def call(pc, args, stack, native=False):
        u.mem_write(sp-stack-4, b'\x5A'*(stack+4)); u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for reg, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args): u.reg_write(reg, val)
        saved = [0x0200FC40 if native and r == UC_ARM_REG_R4 else 0x13579000+i for i, r in enumerate(regs)]
        for reg, val in zip(regs, saved): u.reg_write(reg, val)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop|1); u.emu_start(pc|1, stop, count=30000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)): raise ValueError('ABI')
        if bytes(u.mem_read(sp-stack-4,4))!=b'\x5A'*4: raise ValueError('stack bound')
        return u.reg_read(UC_ARM_REG_R0)

    def run(raw, cap, available=None, output_available=76, source=src, output=dest, pointer=None):
        available = len(raw) if available is None else available
        try: wanted = import_legacy(raw[:available], cap)
        except ValueError: wanted = None
        effective = min(available, 2*cap+2) if 1<=cap<=10 else 0
        if output_available<76 or pointer is not None or not(output+76<=source or source+effective<=output) or output+76>0xFFFFFFFF: wanted=None
        u.mem_write(0x02000000,b'\xA7'*8192); u.mem_write(source,raw)
        before=bytearray(u.mem_read(0x02000000,8192))
        if call(0x08800000,[source if pointer is None else pointer,output,available|output_available<<16,cap],96)!=int(wanted is not None): raise ValueError(f'import status {raw.hex()} cap{cap}')
        if wanted is not None: before[output-0x02000000:output-0x02000000+76]=wanted
        if bytes(u.mem_read(0x02000000,8192))!=bytes(before): raise ValueError('atomic write/source extent')
        counts['import_calls']+=1;counts['rejected']+=wanted is None
        return wanted

    tokens=[bytes([i]) for i in range(228)]+[bytes([228,i]) for i in range(256)]
    print('legacy import484 tokens at each capacity/slot',flush=True)
    for cap in range(1,11):
        for slot in range(cap):
            for token in tokens:
                ts=[b'\x9B']*cap;ts[slot]=token;raw=b'\x00'+b''.join(ts)+b'\xE5'
                wanted=run(raw,cap);counts['token_capacity_slot_paths']+=1
                if cap==10:
                    editor,cells=0x0200FC40,0x0200FC60
                    u.mem_write(editor,b'\xA7'*96)
                    for off,val in ((16,cells),(20,cells),(24,cells)):u.mem_write(editor+off,struct.pack('<I',val))
                    call(0x0803558C,[src],4,native=True)
                    words=struct.unpack('<10H',bytes(u.mem_read(cells,20)))
                    decoded=MixedReplay.restore(wanted)
                    if tuple(from_native_word(w) for w in words)!=decoded.model.state.cells or u.mem_read(editor+20,4)!=struct.pack('<I',cells):raise ValueError('original leaf comparison')
                    counts['original_leaf_comparisons']+=1
        print('capacity',cap,flush=True)
    print('legacy first two body bytes full65536 domain',flush=True)
    for pair in range(65536):run(b'\x00'+pair.to_bytes(2,'little')+b'\xE5',2);counts['byte_pair_domain']+=1
    for marker in range(256):run(bytes([marker])+b'\x9B\xE4\xE5\xE5\xAA',2)
    for cap in range(1,11):
        run(b'\x00\xE5',cap)
        run(b'\x00'+b'\xE4\x00'*cap+b'\xE5',cap)
        run(b'\x00'+b'\x9B'*(cap+1)+b'\xE5',cap)
        for token in tokens:
            original=run(b'\x00'+token+b'\xE5',cap)
            expected=MixedReplay.restore(original)
            for action,key in ((KEYS.index('ㄱ'),'ㄱ'),(40,None)):
                accepted=expected.press(key) if key else expected.backspace()
                before=bytearray(u.mem_read(0x02000000,8192));wanted=expected.serialize()
                if call(0x08802000,[dest,action,76,0x09300000],196)!=int(accepted):raise ValueError('native import/edit status')
                before[dest-0x02000000:dest-0x02000000+76]=wanted
                if bytes(u.mem_read(0x02000000,8192))!=bytes(before):raise ValueError('actual imported state edit')
                counts['edit_calls']+=1
            if bytes(u.mem_read(dest,76))!=original:raise ValueError('native overwritten cell restoration')
            counts['native_import_edit_undo_paths']+=1
    for raw in (b'',b'\x00',b'\x00\xE4',b'\x00\xE4\x00',b'\x00\xF9\xE5',b'\x00\x98\xE5'):
        run(raw,1)
    maximum=b'\x00'+b'\xE4\xE5'*10+b'\xE5'
    for size in range(len(maximum)+1):run(maximum,10,available=size)
    for size in range(76):run(maximum,10,output_available=size)
    for cap in (0,11,255,0xFFFFFFFF):run(b'\x00\xE5',cap)
    for a in range(4):
        for b in range(4):run(maximum,10,source=src+a,output=dest+b)
    for delta in range(-75,22):run(maximum,10,output=src+delta)
    run(maximum,10,pointer=0xFFFFFFF0)
    run(maximum,10,output=0xFFFFFFF0)
    names=['hangul_mixed_legacy_import.py','bench_hangul_mixed_legacy_import.py','hangul_mixed_keyedit_thumb.py','hangul_mixed_rebase_thumb.py','hangul_mixed_dispatch_thumb.py','hangul_mixed_replay_state.py','hangul_native_tokens.py','extended_dialogue.py']
    report=dict(id='exe45.hangul-keyboard.mixed-legacy-import-cpu.v1',passed=True,counts=counts,helper_bytes=len(blob),stack_bytes=96,state_bytes=76,ISA=isa,placed_helpers_ISA=placed,rom_integrated=False,caller_selected_legacy_required=True,legacy_marker_ignored=True,empty_initialization_supported=True,source_sha256=profile['sha256'],dependencies=deps,legacy_source_dependency=sha(legacy_path.read_bytes()),tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in names},artifacts={'helper.bin':sha(blob)},limits=['Not format discrimination, new Hangul record import, save compatibility or actual nonempty game import evidence.','Bounded grammar accepts structural484 tokens; not glyph/input eligibility.','Original capacity-blind overflow is deliberately rejected, not used as a game RAM allocation.','Editor UI/destination initialization and full96-byte lifecycle/writer integration still pending.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS bounded legacy import CPU',counts,flush=True)


if __name__=='__main__':main()
