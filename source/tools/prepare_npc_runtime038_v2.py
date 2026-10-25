"""Correct diagnostic observer import to adopted038 selector v1; no ROM edit."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
spec=[]
for srcname,dstname,changes in [
 ('capture_native_load038_v1.py','capture_native_load038_v2.py',[('field_native_rom_selector_038_v2','field_native_rom_selector_038_v1')]),
 ('run_npc_runtime038_v1.py','run_npc_runtime038_v2.py',[('capture_native_load038_v1.py','capture_native_load038_v2.py')]),
 ('verify_qualified038_v1.py','verify_qualified038_v2.py',[('tools/capture_native_load038_v1.py','tools/capture_native_load038_v2.py'),('tools/verify_qualified038_v1.py','tools/verify_qualified038_v2.py')]),
]:
    src=ROOT/'tools'/srcname;dst=ROOT/'tools'/dstname
    if dst.exists():raise ValueError('Preserve NPC diagnostic correction')
    text=src.read_text(encoding='utf8');counts=[]
    for a,b in changes:
        n=text.count(a)
        if not n:raise ValueError('NPC correction anchor')
        counts.append(n);text=text.replace(a,b)
    dst.write_text(text,encoding='utf8');spec.append(dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes())))
frozen_write(ROOT/'tools/specs/npc_runtime038_v2_version.json',dict(changes=spec,cause='037 base import v2 was mechanically renamed038_v2 although adopted038 selector is v1. Found by direct import inspection before emulator execution; no failed ROM or runtime claim.',scope='Diagnostic import correction only. Original/adopted product, ROM, selector and wording unchanged. Preserve v1 tools.'))
print('Prepared NPC diagnostic v2 with adopted selector v1 import')
