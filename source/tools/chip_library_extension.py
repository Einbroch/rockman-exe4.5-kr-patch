"""Guarded EXE4.5 library name clone and per-row Hangul tile working set.

The source pool, all catalogued pointers, native font and five-row parser stay
unchanged. No scene-independent allocator or total-repertoire restriction.
"""
import struct
from archive_scripts import script_spans, verify_untouched_scripts
from extended_dialogue import HANGUL_COUNT, assemble_verified, sha
from korean_codec import encode_syllable, decode_syllable
from tpl_literals import resolve_units


def decode_name(blob, table):
    chars, at = [], 0
    while at < len(blob):
        code = blob[at]
        if code == 0xE5 and at == len(blob) - 1:
            if len(chars) > 8:
                raise ValueError("chip name exceeds eight cells")
            return "".join(chars)
        if blob[at:at + 2] == b"\xf9\xfc":
            char, at = decode_syllable(blob, at)
        elif code < 0xE5 and code in table:
            char, at = table[code], at + 1
        else:
            raise ValueError("invalid chip-name character/control")
        chars.append(char)
    raise ValueError("missing terminal E5")


def encode_name(text, table):
    if not 1 <= len(text) <= 8:
        raise ValueError("chip name requires 1..8 cells")
    reverse = {v: k for k, v in table.items()}
    data = bytearray()
    for ch in text:
        if 0xAC00 <= ord(ch) < 0xAC00 + HANGUL_COUNT:
            data.extend(encode_syllable(ch))
        elif ch in reverse and reverse[ch] <= 0x82:
            data.append(reverse[ch])
        else:
            raise ValueError(f"unmapped resident chip-name glyph: {ch!r}")
    data.append(0xE5)
    if decode_name(data, table) != text:
        raise ValueError("chip-name semantic roundtrip failed")
    return bytes(data)


def compile_clone(source, spec, asset, table):
    pool = spec["pool"]
    native = source[pool["offset"]:pool["offset"] + pool["bytes"]]
    if (sha(native) != pool["sha256"] or asset["source_archive_sha256"] != sha(native)
            or asset["source_sha256"] != sha(source) or asset["archive"] != f'{pool["offset"]:X}'
            or asset["policy"] != "development-draft; NON-DISTRIBUTION"
            or asset["consumer"] != spec.get('clone_consumer','library-seven-row-tilemap') or asset["review"]["release_eligible"] is not False):
        raise ValueError("chip-name source/consumer/development policy mismatch")
    spans = script_spans(native, pool["scripts"])
    # Full source denominator, including empty offset slots, not selected samples.
    for blob in spans:
        if blob and (any(c >= 0xE5 for c in blob[:-1]) or len(blob) > 9):
            raise ValueError("native chip-name source grammar changed")
        if blob:
            decode_name(blob, table)
    selected, records = set(), []
    for unit in resolve_units(asset):
        archive, index, literal = unit["id"].split(":")
        index = int(index)
        if archive != asset["archive"] or literal != "0" or index in selected or not 0 <= index < len(spans):
            raise ValueError("invalid/duplicate chip-name identity")
        if unit["state"] != "needs_review" or spans[index].hex() != asset["source_script_hex"][str(index)] or decode_name(spans[index], table) != unit["source"]:
            raise ValueError("protected chip-name source/state mismatch")
        if [c for c in unit["source"] if c.isascii() and c.isdigit()] != [c for c in unit["translation"] if c.isascii() and c.isdigit()]:
            raise ValueError("chip-name numeric identity changed")
        encoded = encode_name(unit["translation"], table)
        spans[index] = encoded
        selected.add(index)
        records.append({"id": unit["id"], "script": index, "text": unit["translation"],
                        "encoded_hex": encoded.hex(), "cells": len(unit["translation"]), "state": unit["state"]})
    if not selected:
        raise ValueError("empty chip-name translation selection")
    if set(asset["source_script_hex"]) != {str(i) for i in selected}:
        raise ValueError("protected source-byte denominator mismatch")
    offsets, position = bytearray(), len(spans) * 2
    for blob in spans:
        if position > 0xFFFF:
            raise ValueError("chip-name clone exceeds uint16 offsets")
        offsets.extend(struct.pack("<H", position))
        position += len(blob)
    if position > 0xFFFF:
        raise ValueError("chip-name clone exceeds uint16 offsets")
    clone = bytes(offsets) + b"".join(spans)
    if script_spans(clone, pool["scripts"]) != spans:
        raise ValueError("chip-name clone binary roundtrip failed")
    preserved = verify_untouched_scripts(native, clone, pool["scripts"], selected)
    return clone, {"units": records, "unselected_scripts": preserved, "source_bytes": len(native),
                   "clone_bytes": len(clone), "clone_sha256": sha(clone)}


def construct(source, spec, appended, clone, font_at, word_copy=False, cache=False, burst_copy=False, fast_copy=False, stack_renderer=False, late_wait=False, owner_guard=False, secondary_clone=None):
    folder = spec.get('consumer') == 'folder-seven-row-tilemap'
    if owner_guard and not folder:
        raise ValueError('owner guard is specific to confirmed folder dispatch')
    if folder and (late_wait or stack_renderer or fast_copy):
        raise ValueError('folder consumer excludes library wait, stack and fast-copy experiments')
    if late_wait and not cache:
        raise ValueError('library late wait requires the cache candidate')
    if stack_renderer and (not burst_copy or fast_copy):
        raise ValueError('stack renderer requires burst copy and excludes fast BIOS copy')
    if fast_copy and (not word_copy or burst_copy):
        raise ValueError('fast BIOS copy requires word option and excludes burst copy')
    if burst_copy and not word_copy:
        raise ValueError('burst copy requires inline word copy')
    if cache and not word_copy:
        raise ValueError("experimental tags require word copy")
    if sha(source) != spec["source_sha256"] or spec["policy"] != "development-draft; NON-DISTRIBUTION":
        raise ValueError("chip-name source profile mismatch")
    for item in spec["protected_code"]:
        if sha(source[item["start"]:item["end"]]) != item["sha256"]:
            raise ValueError("chip-name protected source code drift")
    install, buf, vram = spec["install"], spec["buffer"], spec["vram"]
    if (buf["rows"], buf["stride"], buf["cells"], vram["bytes"]) != (7, 32, 8, 56 * 64):
        raise ValueError("unsupported library working-set geometry")
    install_bytes = len(bytes.fromhex(install['expected_hex']))
    if install_bytes != (14 if folder else 12):
        raise ValueError('consumer source instruction cover extent')
    if source[install["offset"]:install["offset"] + install_bytes].hex() != install["expected_hex"]:
        raise ValueError("chip-name installation bytes changed")
    append, layout, isa = bytearray(appended), [], []
    def alloc(blob, name):
        append.extend(b"\xff" * (-len(append) % 4))
        at = len(source) + len(append)
        append.extend(blob)
        layout.append({"name": name, "offset": at, "size": len(blob), "sha256": sha(blob)})
        return at
    def code(text, literals, name):
        at = len(source) + ((len(append) + 3) & ~3)
        blob, proof = assemble_verified(text, 0x08000000 + at, literals)
        isa.append(proof)
        return alloc(blob, name)
    clone_at = alloc(clone, "private library chip-name clone")
    secondary_at = alloc(secondary_clone,'private secondary name clone') if secondary_clone is not None else None
    renderer = """push {r4, r5, r6, r7, lr}
movs r4, #0
ldr r5, row_buffer
subs r5, r2, r5
lsrs r5, r5, #1
ldr r7, tile_start
adds r5, r5, r7
next_cell:
ldrb r1, [r0]
cmp r4, #8
beq done
cmp r1, #0xf9
beq escape
cmp r1, #0xe5
bge pad
lsls r7, r1, #1
adds r7, r7, r6
adds r0, #1
b store
escape:
ldrb r7, [r0, #1]
cmp r7, #0xfc
bne pad
push {r0, r2, r3}
ldrb r1, [r0, #3]
lsls r1, r1, #8
ldrb r7, [r0, #2]
adds r1, r1, r7
lsls r1, r1, #6
ldr r0, font
adds r0, r0, r1
lsls r1, r5, #5
ldr r7, char_base
adds r1, r1, r7
movs r2, #64
ldr r7, copy_helper
mov lr, pc
bx r7
pop {r0, r2, r3}
adds r0, #4
adds r7, r5, r6
store:
strh r7, [r2]
adds r7, #1
strh r7, [r3]
adds r2, #2
adds r3, #2
adds r5, #2
adds r4, #1
b next_cell
pad:
cmp r4, #8
beq done
movs r7, #0
strh r7, [r2]
strh r7, [r3]
adds r2, #2
adds r3, #2
adds r4, #1
b pad
done:
pop {r4, r5, r6, r7, pc}
"""
    if word_copy:
        if font_at % 4 or vram["start"] % 4:
            raise ValueError("word-copy requires aligned font and cell destinations")
        # r0/r2/r3 are saved immediately above; r1 is scratch. Eight pairs
        # transfer exactly 16 words, with no new RAM state or cache lifetime.
        renderer = renderer.replace("movs r2, #64\nldr r7, copy_helper\nmov lr, pc\nbx r7\n",
                                    "ldmia r0!, {r2, r3}\nstmia r1!, {r2, r3}\n" * 8)
        if burst_copy:
            # Preserve the row counter, tile cursor, palette and temporary r7.
            # 6 + 6 + 4 words still transfer exactly one 64-byte glyph.
            renderer = renderer.replace("ldmia r0!, {r2, r3}\nstmia r1!, {r2, r3}\n" * 8,
                "push {r4, r5, r6, r7}\n" +
                "ldmia r0!, {r2, r3, r4, r5, r6, r7}\nstmia r1!, {r2, r3, r4, r5, r6, r7}\n" * 2 +
                "ldmia r0!, {r2, r3, r4, r5}\nstmia r1!, {r2, r3, r4, r5}\npop {r4, r5, r6, r7}\n")
        if fast_copy:
            if source[0x97C:0x990].hex() != '0fb5034b92081a43ebf0dcfb0fbd000000000000':
                raise ValueError('native fast-copy helper source drift')
            if source[0xEC140:0xEC144].hex() != '0cdf7047':
                raise ValueError('native fast-copy SWI boundary drift')
            renderer = renderer.replace("ldmia r0!, {r2, r3}\nstmia r1!, {r2, r3}\n" * 8,
                'movs r2, #64\nldr r7, copy_helper\nmov lr, pc\nbx r7\n')
    literals = {"row_buffer": buf["start"], "tile_start": (vram["start"] - vram["char_base"]) // 32,
                                "font": 0x08000000 + font_at, "char_base": vram["char_base"],
                                "copy_helper": spec["copy_helper"]}
    if folder:
        # Native glyphs keep their resident-font +16 bias. Private Hangul cells
        # use only the palette bits, because tile 514 already names the cell.
        if renderer.count('adds r7, r5, r6\nstore:') != 1:
            raise ValueError('folder Hangul palette boundary drift')
        renderer = renderer.replace('adds r7, r5, r6\nstore:',
            'ldr r7, palette_mask\nands r7, r6\nadds r7, r7, r5\nstore:')
        literals['palette_mask'] = 0xF000
    if fast_copy:
        literals['copy_helper'] = 0x0800097D
    tags = vram["start"] + vram["bytes"]
    if cache:
        if (tags, vram["bytes"]) != (0x06008E40, 3584):
            raise ValueError("cache evidence geometry changed")
        literals["tag_bias"] = tags - literals["tile_start"]
        renderer = renderer.replace("lsls r1, r1, #6\n", """ldr r7, tag_bias
adds r7, r7, r5
ldrh r2, [r7]
adds r1, #1
cmp r2, r1
beq cache_hit
push {r1, r7}
subs r1, #1
lsls r1, r1, #6
""")
        renderer = renderer.replace("pop {r0, r2, r3}\n", """pop {r1, r7}
strh r1, [r7]
cache_hit:
pop {r0, r2, r3}
""")
    render_at = code(renderer, literals, "library per-cell renderer")
    if burst_copy:
        instructions = isa[-1]['instructions']
        loads = [i['operands'] for i in instructions if i['mnemonic'] in ('ldm', 'ldmia')]
        stores = [i['operands'] for i in instructions if i['mnemonic'] in ('stm', 'stmia')]
        registers = ['{r2, r3, r4, r5, r6, r7}'] * 2 + ['{r2, r3, r4, r5}']
        if loads != ['r0!, ' + r for r in registers] or stores != ['r1!, ' + r for r in registers]:
            raise ValueError('burst glyph transfer must preserve the verified 6+6+4 words')
    stack_record = {}
    if stack_renderer:
        template_at = render_at
        template = bytes(append[template_at-len(source):])
        relocated, relocation_proof = assemble_verified(renderer, 0x03000000, literals)
        if relocated != template:
            raise ValueError('stack renderer must be position independent at a word-aligned address')
        frame_bytes = (len(template) + 31) & ~31
        if not 0 < frame_bytes <= 448:
            raise ValueError('stack renderer exceeds the verified Thumb frame/address immediates')
        append.extend(b'\xff' * (frame_bytes - len(template)))
        wrapper = f"""push {{r0, r1, r2, r3, r4, r5, r6, r7, lr}}
sub sp, #{frame_bytes}
ldr r0, template
mov r1, sp
movs r2, #{frame_bytes // 8}
copy_template:
ldmia r0!, {{r3, r4}}
stmia r1!, {{r3, r4}}
subs r2, #1
bne copy_template
add r7, sp, #{frame_bytes}
ldmia r7!, {{r0, r1, r2, r3, r4, r5, r6}}
mov r7, sp
adds r7, #1
mov lr, pc
bx r7
push {{r0, r1, r2, r3}}
add r0, sp, #{frame_bytes + 32}
ldmia r0!, {{r4, r5, r6, r7}}
pop {{r0, r1, r2, r3}}
add sp, #{frame_bytes}
add sp, #32
pop {{pc}}
"""
        render_at = code(wrapper, {'template': 0x08000000 + template_at}, 'private stack renderer invocation')
        calls = [i['address'] for i in isa[-1]['instructions'] if i['mnemonic'] == 'bx']
        if len(calls) != 1:
            raise ValueError('stack invocation boundary changed')
        stack_record = {'stack_renderer': {'status': 'experimental; runtime pending',
            'template_offset': template_at, 'template_bytes': len(template), 'frame_bytes': frame_bytes,
            'maximum_stack_bytes_from_selector_entry': frame_bytes + 112,
            'wrapper_offset': render_at, 'invoke_address': calls[0], 'alignment': 4,
            'scope': 'private live stack frame; template copied on every row invocation',
            'position_independent_bytes_verified': True, 'relocation_proof': relocation_proof}}
    selector = """pop {r7}
push {r4, r5, r6, r7, lr}
lsrs r1, r1, #24
mov r4, r9
cmp r4, #7
bne native
ldr r4, row_buffer
cmp r2, r4
blt native
ldr r4, buffer_end
cmp r2, r4
bge native
movs r4, #31
ands r4, r2
bne native
adds r4, r2, #0
adds r4, #16
cmp r3, r4
bne native
ldr r4, base_mask
ands r4, r6
bne native
ldr r4, source_pool
cmp r0, r4
bne native
ldr r0, private_pool
lsls r1, r1, #1
ldrh r1, [r0, r1]
adds r0, r0, r1
ldr r7, renderer
mov lr, pc
bx r7
b restore
native:
lsls r1, r1, #1
ldrh r1, [r0, r1]
adds r0, r0, r1
ldr r7, native_parser
mov lr, pc
bx r7
restore:
pop {r4, r5, r6, r7}
add sp, #4
push {r1}
ldr r1, continuation
mov lr, r1
pop {r1}
bx lr
"""
    if folder:
        selector = selector.replace('ands r4, r6\nbne native', 'ands r4, r6\ncmp r4, #16\nbne native')
        selector = selector.replace('lsrs r1, r1, #24\nmov r4, r9', 'lsls r1, r1, #24\nlsrs r1, r1, #24\nmov r4, r9')
    selector_literals = {"row_buffer": buf["start"], "buffer_end": buf["start"] + 7 * 32,
                                  "base_mask": 0xFFF, "source_pool": 0x08000000 + spec["pool"]["offset"],
                                  "private_pool": 0x08000000 + clone_at, "renderer": 0x08000001 + render_at,
                                  "native_parser": spec["native_parser"], "continuation": install["continuation"]}
    if secondary_at is not None:
        selector=selector.replace('ldr r4, source_pool\ncmp r0, r4\nbne native\nldr r0, private_pool\n',
            'ldr r4, source_pool\ncmp r0, r4\nbeq primary_clone\nldr r4, secondary_source\ncmp r0, r4\nbne native\ncmp r1, #136\nbhi native\nldr r0, secondary_private\nb selected_clone\nprimary_clone:\nldr r0, private_pool\nselected_clone:\n')
        selector_literals.update(secondary_source=0x08765B18,secondary_private=0x08000000+secondary_at)
    if owner_guard:
        if struct.unpack_from('<I',source,0x3B918)[0]!=0x0803C1C1 or struct.unpack_from('<I',source,0x3C1E4)[0]!=0x0803D855:
            raise ValueError('folder owner dispatch table drift')
        selector = selector.replace('cmp r4, #7\nbne native\n',"""cmp r4, #7
bne native
mov r4, r10
ldr r7, owner_context
cmp r4, r7
bne native
ldr r4, [r4]
ldrb r4, [r4]
cmp r4, #28
bne native
mov r4, r10
ldr r4, [r4, #0x34]
ldrb r7, [r4]
cmp r7, #0
bne native
ldrb r4, [r4, #1]
cmp r4, #16
bne native
""")
        selector_literals['owner_context']=0x0200F2C0
    selector_at = code(selector, selector_literals,
                       "guarded library name selector")
    thunk, proof = assemble_verified("push {r7}\nldr r7, target\nbx r7\n", 0x08000000 + install["offset"],
                                    {"target": 0x08000001 + selector_at})
    if len(thunk) != 12:
        raise ValueError("library installation extent drift")
    if folder:
        # Cover the complete native 14-byte sequence through its two-halfword
        # BL. Aligned 12-byte thunk plus an unreachable MOV r0,r0, not half a BL.
        thunk += b'\x00\x46'
    isa.append(proof)
    patches = [(install["offset"], thunk, "guarded library private chip-name selector")]
    wait_record = {}
    if late_wait:
        if source[0x25C:0x264].hex() != '00f08af800f070f8':
            raise ValueError('native two-call wait site drift')
        if (struct.unpack_from('<I', source, 0x2FC)[0], struct.unpack_from('<I', source, 0x3B920)[0],
            struct.unpack_from('<I', source, 0x3B914)[0], struct.unpack_from('<I', source, 0x368)[0],
            struct.unpack_from('<I', source, 0x36C)[0]) != (0x0803B8F9, 0x08042321, 0x0803B918, 0x02010210, 0x0200F808):
            raise ValueError('library dispatch/wait-counter profile drift')
        if source[0x374:0x388].hex() != '00b50348012201881142fcd100bd000004000004':
            raise ValueError('native wait-out loop drift')
        wait_at = code("""push {r3, lr}
mov r0, r10
ldr r3, context
cmp r0, r3
bne normal_wait
ldr r0, [r0]
ldrb r0, [r0]
cmp r0, #28
bne normal_wait
mov r0, r10
ldr r0, [r0, #0x34]
ldrb r1, [r0]
cmp r1, #8
bne normal_wait
ldrb r1, [r0, #1]
cmp r1, #4
bne normal_wait
ldr r0, display_status
ldrh r0, [r0]
movs r1, #1
tst r0, r1
beq normal_wait
ldr r0, threshold
ldr r0, [r0]
cmp r0, #1
bne normal_wait
ldr r0, counter
ldr r0, [r0]
cmp r0, #1
bne normal_wait
b next_wait
normal_wait:
ldr r3, wait_out
mov lr, pc
bx r3
next_wait:
ldr r3, wait_next
mov lr, pc
bx r3
pop {r3}
add sp, #4
push {r3}
ldr r3, continuation
mov lr, r3
pop {r3}
bx lr
""", {'context': 0x0200F2C0, 'display_status': 0x04000004,
       'threshold': 0x0200F808, 'counter': 0x02010210,
       'wait_out': 0x08000375, 'wait_next': 0x08000345, 'continuation': 0x08000265},
       'guarded active-library late VBlank wait')
        skip_sites = [i['address'] for i in isa[-1]['instructions'] if i['mnemonic'] == 'b']
        if len(skip_sites) != 1:
            raise ValueError('late wait decision boundary changed')
        wait_thunk, wait_proof = assemble_verified('ldr r0, target\nbx r0\n', 0x0800025C,
            {'target': 0x08000001 + wait_at})
        if len(wait_thunk) != 8:
            raise ValueError('late wait install extent changed')
        isa.append(wait_proof)
        patches.append((0x25C, wait_thunk, 'guarded active-library late wait'))
        wait_record = {'late_wait': {'status': 'experimental; runtime pending', 'install': 0x25C,
            'offset': wait_at, 'skip_address': skip_sites[0], 'continuation': 0x08000265,
            'context': 0x0200F2C0, 'job': 28, 'menu': 8, 'phase': 4,
            'counter': 0x02010210, 'threshold': 0x0200F808,
            'rule': 'active library; DISPSTAT VBlank; counter==threshold==1; reuse native wait-next and counter reset'}}
    cache_record = {}
    if cache and folder:
        reset_site = 0x3D978
        if source[reset_site:reset_site+8].hex() != '0b48a86400bd0000' or source[0x3D9A8:0x3D9AC].hex() != 'ff7f0000':
            raise ValueError('folder initialization completion profile drift')
        reset_code = """ldr r0, original_literal
ldr r0, [r0]
str r0, [r5, #0x48]
push {r0, r1, r2, r3}
ldr r0, tags
movs r1, #0
movs r2, #56
folder_clear_tags:
strh r1, [r0]
adds r0, #2
subs r2, #1
bne folder_clear_tags
pop {r0, r1, r2, r3}
pop {pc}
"""
        reset_literals={'original_literal':0x0803D9A8,'tags':tags}
        if owner_guard:
            reset_code=reset_code.replace('push {r0, r1, r2, r3}\nldr r0, tags',"""push {r0, r1, r2, r3, r7}
mov r0, r10
ldr r7, owner_context
cmp r0, r7
bne folder_reset_done
ldr r0, [r0]
ldrb r0, [r0]
cmp r0, #28
bne folder_reset_done
mov r0, r10
ldr r0, [r0, #0x34]
ldrb r1, [r0]
cmp r1, #0
bne folder_reset_done
ldrb r0, [r0, #1]
cmp r0, #16
bne folder_reset_done
ldr r0, tags""")
            reset_code=reset_code.replace('pop {r0, r1, r2, r3}\npop {pc}',
                                          'folder_reset_done:\npop {r0, r1, r2, r3, r7}\npop {pc}')
            reset_literals['owner_context']=0x0200F2C0
        reset_at = code(reset_code,reset_literals,'folder initialization completion cache reset')
        final_pop = [i['address'] for i in isa[-1]['instructions'] if i['mnemonic']=='pop' and i['operands']=='{pc}']
        if len(final_pop)!=1:
            raise ValueError('folder reset return boundary')
        reset_thunk, reset_proof = assemble_verified('ldr r0, target\nbx r0\n',0x08000000+reset_site,
                                                     {'target':0x08000001+reset_at})
        if len(reset_thunk)!=8:
            raise ValueError('folder reset install extent')
        isa.append(reset_proof)
        patches.append((reset_site,reset_thunk,'folder initialization completion cache reset'))
        cache_record={'cache':{'status':'experimental; runtime pending','tags':tags,'bytes':112,
            'encoding':'uint16 LE; zero invalid, Hangul index+1 valid','reset_offset':reset_at,'reset_install':reset_site,
            'reset_kind':'folder-init-native-pop-pc','reset_probe':final_pop[0],
            'evidence':'analysis/exe45_chip_folder_lifetime_v1.json'},'native_tile_bias':16}
        if owner_guard:
            cache_record['owner_guard']={'context':0x0200F2C0,'job':28,'menu':0,'phase':16,
                'scope':'selector and init tag reset; other owners use native names and unchanged tags'}
    if cache and not folder:
        reset_site = 0x427A0
        if source[reset_site:reset_site+8].hex() != "51485249a9f0d8fc":
            raise ValueError("cache reset source instructions changed")
        # Replay the two source pointer loads and native LZ call, using live
        # pointer storage so archive relocation remains owned by the main build.
        reset_address = 0x08000000 + len(source) + ((len(append) + 3) & ~3)
        reset_at = code("""push {r7}
ldr r0, source_pointer
ldr r0, [r0]
ldr r1, destination_pointer
ldr r1, [r1]
ldr r7, lz_return
mov lr, r7
ldr r7, native_lz
bx r7
pop {r7}
push {r0, r1, r2, r3}
ldr r0, tags
movs r1, #0
movs r2, #56
clear_tags:
strh r1, [r0]
adds r0, #2
subs r2, #1
bne clear_tags
pop {r0, r1, r2, r3}
push {r0}
ldr r0, continuation
mov lr, r0
pop {r0}
bx lr
""", {"source_pointer": 0x080428E8, "destination_pointer": 0x080428EC,
       "native_lz": 0x080EC159, "lz_return": reset_address + 18 + 1,
       "tags": tags, "continuation": 0x080427A9}, "library cache reset after assets")
        returns = [i['address'] for i in isa[-1]['instructions'] if i['mnemonic'] == 'pop' and i['operands'] == '{r7}']
        if returns != [reset_address + 18] or not isa[-1]['literal_values']['lz_return'] & 1:
            raise ValueError('native BX LR Thumb return boundary drift')
        reset_thunk, reset_proof = assemble_verified("ldr r0, target\nbx r0\n", 0x08000000 + reset_site,
                                                    {"target": 0x08000001 + reset_at})
        if len(reset_thunk) != 8:
            raise ValueError("cache reset thunk extent changed")
        isa.append(reset_proof)
        patches.append((reset_site, reset_thunk, "experimental library cache reset"))
        cache_record = {"cache": {"status": "experimental; runtime pending", "tags": tags, "bytes": 112,
                                 "encoding": "uint16 LE; zero invalid, Hangul index+1 valid",
                                 "reset_offset": reset_at, "reset_install": reset_site,
                                 "reset_continuation": 0x080427A9,
                                 "evidence": "analysis/exe45_chip_cache_ownership_v1.json"}}
    return bytes(append), patches, {
        "clone_offset": clone_at, "renderer_offset": render_at, "selector_offset": selector_at,
        "secondary_clone_offset": secondary_at,
        "font_offset": font_at, "install": install, "buffer": buf, "vram": vram,
        "layout": layout, "machine_code": isa, "source_pools_and_pointers_unchanged": True,
        "translated_units": 0, "runtime": "pending", "scope": "guarded seven-row folder only; other consumers remain native" if folder else "guarded seven-row library only; other consumers remain native", **cache_record, **stack_record, **wait_record}
