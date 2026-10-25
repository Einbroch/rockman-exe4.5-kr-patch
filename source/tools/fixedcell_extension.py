"""EXE4.5 big fixed-cell F9 FC extension; legacy slots remain untouched.

Live r0=stream, r2=stage, r3=continue, r4/r5=cell counters, r6=font,
r9=decoded count, r10=context. Native copier owns tint/pixel packing.
Legacy subcommands tail-call the original handler with r7 preserved.
"""
from extended_dialogue import HANGUL_COUNT, assemble_verified, sha


def construct(source: bytes, spec: dict, appended: bytes, cells: dict,
              *, mono_cells: dict | None = None, mono_spec: dict | None = None,
              extra_cells: list | None = None, mono_extra_cells: list | None = None) -> tuple:
    if sha(source) != spec["source_sha256"]:
        raise ValueError("fixed-cell source mismatch")
    for row in spec["protected_code"]:
        if sha(source[row["start"]:row["end"]]) != row["sha256"]:
            raise ValueError("fixed-cell native code/loader drift")
    if set(cells) != {chr(0xAC00 + i) for i in range(HANGUL_COUNT)} or any(len(c) != 64 for c in cells.values()):
        raise ValueError("fixed-cell full glyph supply missing")
    append, layout = bytearray(appended), []
    def alloc(blob, name):
        append.extend(b"\xff" * (-len(append) % 4))
        at = len(source) + len(append)
        append.extend(blob)
        layout.append({"name": name, "offset": at, "size": len(blob), "sha256": sha(blob)})
        return at
    extra_cells = extra_cells or []
    mono_extra_cells = mono_extra_cells or []
    if any(len(c)!=64 for c in extra_cells+mono_extra_cells):raise ValueError('fixed-cell extra record extent')
    if mono_cells is None and mono_extra_cells or mono_cells is not None and len(mono_extra_cells)!=len(extra_cells):raise ValueError('extra provider parity')
    font_at = alloc(b"".join(cells[chr(0xAC00 + i)] for i in range(HANGUL_COUNT))+b''.join(extra_cells), "big fixed-cell Hangul bank")
    mono_at = None
    if (mono_cells is None) != (mono_spec is None):
        raise ValueError('mono cells and source specification required together')
    if mono_cells is not None:
        bank=mono_spec['native_font']
        if mono_spec['source_sha256']!=sha(source) or sha(source[bank['offset']:bank['offset']+bank['bytes']])!=bank['sha256']:
            raise ValueError('mono native provider changed')
        if set(mono_cells)!=set(cells) or any(len(c)!=64 for c in mono_cells.values()):
            raise ValueError('mono full glyph supply missing')
        mono_at=alloc(b''.join(mono_cells[chr(0xAC00+i)] for i in range(HANGUL_COUNT))+b''.join(mono_extra_cells), 'mono fixed-cell Hangul bank')
    code = """ldrb r1, [r0, #1]
cmp r1, #0xfc
beq hangul
ldr r1, legacy
bx r1
hangul:
push {r3, r6, r7, lr}
ldrb r1, [r0, #3]
lsls r1, r1, #8
ldrb r7, [r0, #2]
adds r1, r1, r7
ldr r6, font
ldr r7, copier
mov lr, pc
bx r7
adds r0, #4
mov r7, r9
adds r7, #1
mov r9, r7
pop {r3, r6, r7, pc}
"""
    literals={"legacy": spec["f9_slot"]["handler_address"],
              "font": 0x08000000 + font_at, "copier": spec["copier_address"] | 1}
    if mono_at is not None:
        code=code.replace('ldr r6, font\n', '''ldr r7, mono_native
cmp r6, r7
bne big_font
ldr r6, mono_font
b font_ready
big_font:
ldr r6, font
font_ready:
''',1)
        literals.update(mono_native=0x08000000+mono_spec['native_font']['offset'],mono_font=0x08000000+mono_at)
    next_at = len(source) + ((len(append) + 3) & ~3)
    blob, isa = assemble_verified(code, 0x08000000 + next_at,
                                  literals)
    hook_at = alloc(blob, "fixed-cell F9 FC handler")
    slot = spec["f9_slot"]
    if source[slot["offset"]:slot["offset"] + 4].hex() != slot["expected_hex"]:
        raise ValueError("fixed-cell F9 dispatch drift")
    patch = (slot["offset"], (0x08000001 + hook_at).to_bytes(4, "little"), "fixed-cell F9 FC dispatch")
    metadata={"encoding": "F9 FC + uint16 LE Hangul syllable index",
        "font_offset": font_at, "hook_offset": hook_at, "hangul_syllables": HANGUL_COUNT,
        "cell_bytes": 64, "cell_advance": 8, "layout": layout, "machine_code": isa,
        "native_big_font_unchanged": True, "legacy_f9_tail_call": True,
        "scope": "selected library headers only; no chip-name tilemap or mono extension claim"}
    if mono_at is not None:
        metadata['mono_provider']={'font_offset':mono_at,'native_font':mono_spec['native_font'],
            'roles':mono_spec['roles'],'glyphs':HANGUL_COUNT,'cell_bytes':64,
            'scope':mono_spec['scope'],'runtime_status':'pending translated mono proof'}
    if extra_cells:
        metadata['extra_glyphs']=dict(first_index=HANGUL_COUNT,count=len(extra_cells),bytes=len(extra_cells)*64,big_sha256=sha(b''.join(extra_cells)),mono_sha256=sha(b''.join(mono_extra_cells)) if mono_at is not None else None,runtime_status='pending actual selection and pixels')
    return bytes(append), [patch], metadata
