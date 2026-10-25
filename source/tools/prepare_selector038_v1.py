"""Version the typed selector for a third source-decoded caller, no ROM write."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

src=ROOT/'tools/field_native_rom_selector_037_v2.py';dst=ROOT/'tools/field_native_rom_selector_038_v1.py'
proof=read('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json');p=next(p for p in proof['tools'] if p['path'].replace('\\','/')=='tools/field_native_rom_selector_037_v2.py');require_hash(src,p['sha256'])
if dst.exists():raise ValueError('Preserve selector version')
text=src.read_text(encoding='utf8')
hint_contract='''    hint = list(decoder.disasm(source[0x4F7FC:0x4F808], 0x0804F7FC))
    if [(i.mnemonic, i.op_str) for i in hint] != [
        ('push','{r4, r5, r6, r7, lr}'),('adds','r1, r0, #0'),
        ('ldr','r0, [pc, #4]'),('bl','#0x804fb4c'),('pop','{r4, r5, r6, r7, pc}')]:
        raise ValueError('038 original hint argument provider')
'''
old_pool="""    for kind, lookup in [('native-NPC', native_lookup(source)), ('field-board', board_lookup(source))]:
        for archive, refs in lookup.items():
            payload = lz77_decompress(source, int(archive, 16))[0]
            for ref in refs:
                pool.append(dict(archive=archive, source_class=kind, payload=payload, **ref, caller_lr=abi[kind]['caller_lr']))
"""
new_pool="""    for archive, refs in typed_lookup(source).items():
        payload = lz77_decompress(source, int(archive, 16))[0]
        for ref in refs:
            kind=ref['source_class']
            if (ref['root'],ref['caller_lr'])!=(abi[kind]['root'],abi[kind]['caller_lr']):
                raise ValueError('038 lookup/caller contract mismatch')
            pool.append(dict(archive=archive, payload=payload, **ref))
"""
old_gate='''board_gate:
ldr r3,board_caller
cmp r2,r3
bne fallback
ldr r3,board_root
cmp r0,r3
bne fallback
script_gate:'''
new_gate='''board_gate:
ldr r3,board_caller
cmp r2,r3
bne hint_gate
ldr r3,board_root
cmp r0,r3
bne fallback
b script_gate
hint_gate:
ldr r3,hint_caller
cmp r2,r3
bne fallback
ldr r3,hint_root
cmp r0,r3
bne fallback
script_gate:'''
changes=[
    ('from prepare_source500_037_v2 import native_lookup, board_lookup','from prepare_source500_038_v3 import typed_lookup'),
    ("('field-board', 0x0806A4FC, 0x0806A502, 0x6A50C, 0x0203C800),","('field-board', 0x0806A4FC, 0x0806A502, 0x6A50C, 0x0203C800),\n        ('navi-hint', 0x0804F7FC, 0x0804F802, 0x4F808, 0x0203D800),"),
    ('    return result\n',hint_contract+'    return result\n'),
    (old_pool,new_pool),(old_gate,new_gate),
    ("board_root=abi['field-board']['root']))","board_root=abi['field-board']['root'], hint_caller=abi['navi-hint']['caller_lr'], hint_root=abi['navi-hint']['root']))"),
]
for old,new in changes:
    if text.count(old)!=1:raise ValueError('038 selector exact anchor '+old[:80])
    text=text.replace(old,new,1)
text=text.replace('037','038').replace('Finite four-scene lookup population','Finite explicit source lookup-index population').replace('NPC/board','NPC/board/hint')
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/selector038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Add original source hint entry4F7FC/BL4F802/LR4F807/root0203D800. Keep caller/root/script filters before scene dereference and unchanged seven-word descriptor comparison, ABI and previous-wrapper composition. Not CPU/product/runtime admission.'))
print('Generated038 three-caller typed selector; no ROM')
