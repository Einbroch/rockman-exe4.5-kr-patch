"""Execute immutable original import/flatten/edit blocks in synthetic CPU RAM.

Not emulator runtime, no injected live state, ROM edits or save changes.
Import/flatten are complete leaf calls. Delete/overwrite stop before sound
calls and therefore prove only those bounded original blocks, not whole ABI.
"""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from bench_hangul_composer_thumb import *
from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB, KS_VERSION, CS_VERSION
from hangul_native_tokens import tag, untag, from_native_word, to_native_word, verify_contract


def main():
    profile = json.loads((ROOT / 'project.json').read_text(encoding='utf8'))['source_profile']
    source = ROOT / profile['filename']; require_hash(source, profile['sha256']); rom = source.read_bytes()
    product = ROOT / 'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    identity = '5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    require_hash(product, identity); patched = product.read_bytes()
    require_hash(ROOT / 'external/arm_bench_python/unicorn/lib/unicorn.dll',
                 '010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    if (KS_VERSION, CS_VERSION) != ('0.9.2', '5.0.7'):
        raise ValueError('toolchain drift')
    regions = [(0x3558C, 0x355AE), (0x35620, 0x3562C), (0x3562C, 0x3564E),
               (0x353C0, 0x353DE), (0x353EE, 0x35408), (0x354C8, 0x354EC),
               (0x354A4, 0x354B6), (0x35748, 0x35750)]
    guards = []
    ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB); cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    header = '.syntax unified\n.cpu arm7tdmi\n.thumb\n'
    decoded = []
    for a, b in regions:
        if a < 0x35748 and rom[a:b] != patched[a:b]:
            raise ValueError('native profile differs from play product')
        guards.append(dict(start=hex(a), end=hex(b), sha256=sha(rom[a:b]), current_product_sha256=sha(patched[a:b])))
        if a >= 0x35748:
            continue  # Explicit literal, not instructions.
        ins = list(cs.disasm(rom[a:b], 0x08000000 + a))
        if sum(i.size for i in ins) != b - a:
            raise ValueError('native instruction extent')
        for i in ins:
            if i.size != 2 or bytes(ks.asm(header + i.mnemonic + ' ' + i.op_str, i.address)[0]) != i.bytes:
                raise ValueError('native instruction roundtrip')
            decoded.append(dict(address=hex(i.address), hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str))
    table_address = struct.unpack_from('<I', rom, 0x35748)[0]
    table = table_address - 0x08000000
    pages = []
    for page, off in enumerate(struct.unpack_from('<3H', rom, table + 4)):
        tokens = []; i = table + off
        while rom[i] != 0xE5:
            n = 2 if rom[i] == 0xE4 else 1
            tokens.append(rom[i:i + n]); i += n
            if len(tokens) > 105:
                raise ValueError('selector page bound')
        pages.append(dict(page=page, offset=hex(table + off), cells=len(tokens),
                          tokens=[t.hex() for t in tokens],
                          region_sha256=sha(rom[table + off:i + 1])))
    product_table_address = struct.unpack_from('<I', patched, 0x35748)[0]
    product_table = product_table_address - 0x08000000
    if rom[0x3574C:0x35750] != patched[0x3574C:0x35750]:
        raise ValueError('editor literal changed')
    for page, off in enumerate(struct.unpack_from('<3H', patched, product_table + 4)):
        actual = []; i = product_table + off; start = i
        while patched[i] != 0xE5:
            n = 2 if patched[i] == 0xE4 else 1
            actual.append(patched[i:i + n].hex()); i += n
            if len(actual) > 105:
                raise ValueError('current product selector bound')
        if actual != pages[page]['tokens']:
            raise ValueError('product selector tokens differ from source')
        pages[page]['current_product_offset'] = hex(start)
        pages[page]['current_product_region_sha256'] = sha(patched[start:i + 1])
    tokens = sorted({bytes.fromhex(t) for p in pages for t in p['tokens']})
    mixed_identity = verify_contract()
    if any(len(t) not in (1, 2) or len(t) == 2 and t[0] != 0xE4 for t in tokens):
        raise ValueError('native token shape')
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000, len(rom)); u.mem_write(0x08000000, rom)
    u.mem_protect(0x08000000, len(rom), UC_PROT_READ | UC_PROT_EXEC)
    u.mem_map(0x02000000, 0x40000); u.mem_map(0x03000000, 0x8000)
    u.mem_map(0x0FF00000, 4096)
    editor, cells, flat, record, selected, sp, stop = 0x0200FC40, 0x0200FC60, 0x0200FC80, 0x02026280, 0x02026300, 0x030076C8, 0x0FF00000
    counts = dict(import_calls=0, flatten_calls=0, count_calls=0, delete_blocks=0, overwrite_blocks=0)
    preserved = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                 UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]

    def call(pc, end=stop, args=(), check_abi=True):
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        for r, val in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3], args):
            u.reg_write(r, val)
        for i, r in enumerate(preserved):
            u.reg_write(r, editor if r == UC_ARM_REG_R4 else 0x13579000 + i)
        u.mem_write(sp - 8, b'\x5A' * 4)
        u.reg_write(UC_ARM_REG_SP, sp); u.reg_write(UC_ARM_REG_LR, stop | 1)
        u.emu_start(pc | 1, end, count=10000)
        if u.reg_read(UC_ARM_REG_PC) != end or u.reg_read(UC_ARM_REG_SP) != sp or bytes(u.mem_read(sp - 8, 4)) != b'\x5A' * 4:
            raise ValueError('native block return/stack boundary')
        if check_abi and any(u.reg_read(r) != (editor if r == UC_ARM_REG_R4 else 0x13579000 + i) for i, r in enumerate(preserved)):
            raise ValueError('native leaf preserved registers')

    def seed(ts, cap=10, marker=0):
        raw = bytes([marker]) + b''.join(ts) + b'\xE5'
        u.mem_write(editor - 4, b'\xA7' * 104)
        for off, val in [(0x10, cells), (0x14, cells), (0x18, cells), (0x1C, record)]:
            u.mem_write(editor + off, struct.pack('<I', val))
        u.mem_write(editor + 4, bytes([cap])); u.mem_write(record, raw)
        before = bytearray(u.mem_read(editor - 4, 104))
        call(0x0803558C, args=[record]); counts['import_calls'] += 1
        words = [int.from_bytes(t, 'little') for t in ts]
        tagged = [from_native_word(w) for w in words]
        if tagged != [tag(t) for t in ts] or [to_native_word(w) for w in tagged] != words or b''.join(untag(w) for w in tagged) != b''.join(ts):
            raise ValueError('mixed native-cell identity preservation')
        expected = b''.join(struct.pack('<H', w) for w in words) + b'\xE5\x00'
        before[36:36 + len(expected)] = expected
        before[28:32] = struct.pack('<I', cells + len(ts) * 2)
        if bytes(u.mem_read(editor - 4, 104)) != bytes(before) or bytes(u.mem_read(record, len(raw))) != raw:
            raise ValueError('native import word/end/cursor/record mismatch')
        call(0x08035620, args=[0x18]); counts['count_calls'] += 1
        if u.reg_read(UC_ARM_REG_R0) != len(ts):
            raise ValueError('native imported count')
        before = bytearray(u.mem_read(editor - 4, 104))
        call(0x0803562C); counts['flatten_calls'] += 1
        body = b''.join(ts) + b'\xE5'; before[68:68 + len(body)] = body
        if bytes(u.mem_read(editor - 4, 104)) != bytes(before):
            raise ValueError('native import->flatten exact roundtrip')
        return words

    # Every token actually stored in the three native page strings at every
    # ten-cell position. This is a bounded selector-table population, not all
    # Japanese fonts/text controls or proof of natural selector reachability.
    for slot in range(10):
        for token in tokens:
            ts = [b'\x9B'] * 10; ts[slot] = token; seed(ts)
    for marker in range(256):
        seed([b'\x9B', b'\xE4\x00', b'\x5E'], marker=marker)
    for count in range(11):
        seed([b'\xE4\x00'] * count)
    # Source decoder itself does not enforce capacity. Keep the adversarial
    # example within its physical32-byte word buffer and report the breach.
    over = seed([b'\x9B'] * 5, cap=4)
    if len(over) != 5:
        raise ValueError('capacity-blind import not reproduced')
    cases = [[], [b'\x9B'], [b'\x9B', b'\xE4\x00', b'\x5E'], [b'\xE4\x00'] * 10]
    for ts in cases:
        if not ts:
            continue
        for cursor in range(len(ts) + 1):
            words = seed(ts); u.mem_write(editor + 0x14, struct.pack('<I', cells + cursor * 2))
            before = bytearray(u.mem_read(editor - 4, 104))
            call(0x080353C0, 0x08035408, check_abi=False); counts['delete_blocks'] += 1
            removed = 0 if cursor == 0 else cursor - 1
            remainder = words[:removed] + words[removed + 1:]
            # Original shifts occupied cells, not terminator/cleared tail.
            for i in range(removed, len(remainder)):
                before[36 + 2 * i:38 + 2 * i] = struct.pack('<H', remainder[i])
            before[24:28] = struct.pack('<I', cells + max(0, cursor - 1) * 2)
            before[28:32] = struct.pack('<I', cells + (len(ts) - 1) * 2)
            if bytes(u.mem_read(editor - 4, 104)) != bytes(before):
                raise ValueError('native interior delete shift/cursor')
    for cursor in range(4):
        for token in tokens:
            words = seed(cases[2]); u.mem_write(editor + 0x14, struct.pack('<I', cells + cursor * 2))
            u.mem_write(selected, token); before = bytearray(u.mem_read(editor - 4, 104))
            call(0x080354C8, 0x080354EC, args=[0, 0, 0, selected], check_abi=False)
            counts['overwrite_blocks'] += 1
            before[36 + cursor * 2:38 + cursor * 2] = struct.pack('<H', int.from_bytes(token, 'little'))
            before[24:28] = struct.pack('<I', cells + (cursor + 1) * 2)
            if cursor == len(words):
                before[28:32] = struct.pack('<I', cells + (len(words) + 1) * 2)
            if bytes(u.mem_read(editor - 4, 104)) != bytes(before):
                raise ValueError('native overwrite not insert')
    out = ROOT / 'analysis/hangul_keyboard_v1/legacy_edit.json'
    report = dict(id='exe45.hangul-keyboard.legacy-edit-source.v1', passed=True,
                  source_sha256=profile['sha256'], current_rom_sha256=identity, rom_integrated=False,
                  evidence_class='immutable source CPU synthetic-call investigation, NOT game runtime',
                  counts=counts, selector_table=dict(address=hex(table_address), current_product_address=hex(product_table_address), pages=pages, unique_tokens=len(tokens)),
                  native_guards=guards, decoded_instructions=decoded,
                  findings=dict(marker_ignored_on_import=True, imported_cursor='start, unchanged',
                                byte_to_cell='single b => 00bb; E4 xx => xxE4 little-endian',
                                flatten_exact_for_selector_tokens=True, import_checks_capacity=False,
                                capacity_breach=dict(declared=4, imported=5),
                                interior_delete='before cursor; cursor0 deletes first occupied cell; shifts later occupied cells left',
                                overwrite='replaces existing cell; appends only at end; advances cursor',
                                source_cursor_endpoints_preserved=True),
                  mixed_identity_candidate=mixed_identity,
                  tools={n: sha((ROOT / 'tools' / n).read_bytes()) for n in ['analyze_keyboard_legacy_edit.py', 'hangul_native_tokens.py']},
                  limits=['Import/flatten/count leaf functions tested; delete/overwrite stop before sound calls, not whole handler ABI.',
                          'Source page bytes prove a bounded token population, not font coverage or selector UI reachability.',
                          'No real nonempty import, save or emulator intervention/normal-play evidence.',
                          'Pure Hangul keylog baseline cannot encode these opaque legacy cells or arbitrary cursor operations.',
                          'Future adapter must preserve legacy tokens and cursor semantics or obtain an explicit human UX scope decision.'],
                  next='Design mixed native-token/Hangul cell identity with cursor-aware replay; observe actual nonempty imports, record widths and stack before ROM installation.')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
    require_hash(source, profile['sha256']); require_hash(product, identity)
    print('PASS bounded original legacy import/flatten/delete/overwrite', counts, 'pages', [p['cells'] for p in pages], 'tokens', len(tokens))


if __name__ == '__main__':
    main()
