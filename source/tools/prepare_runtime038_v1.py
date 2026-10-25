"""Version read-only runtime probes and own coldboot recipes for actual038."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

spec=[];meta=read('poc/output/pending500_037_v2.json')
for srcname,dstname in [
    ('tools/native037_loaded_guards.py','tools/native038_loaded_guards.py'),
    ('tools/capture_field_loader_037_v1.py','tools/capture_field_loader_038_v1.py'),
    ('tools/run_normal037_v2.py','tools/run_normal038_v1.py'),
    ('tools/verify_normal037_v1.py','tools/verify_normal038_v1.py'),
]:
    src,dst=ROOT/srcname,ROOT/dstname
    if dst.exists():raise ValueError('Preserve038 runtime tool')
    if src.name in meta['build_tools_sha256']:require_hash(src,meta['build_tools_sha256'][src.name])
    text=src.read_text(encoding='utf8');changes=[('037','038')]
    if src.name=='capture_field_loader_037_v1.py':changes.append(("if s['cpu.r0']==0x02039800 or s['cpu.r0']==0x0203C800 then","if s['cpu.r0']==0x02039800 or s['cpu.r0']==0x0203C800 or s['cpu.r0']==0x0203D800 then"))
    if src.name=='verify_normal037_v1.py':changes.append(('tools/run_normal038_v2.py','tools/run_normal038_v1.py'))
    counts=[]
    for old,new in changes:
        n=text.count(old)
        if n<1:raise ValueError('038 runtime exact anchor')
        counts.append(n);text=text.replace(old,new)
    dst.write_text(text,encoding='utf8');spec.append(dict(base=srcname,base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=dstname,output_sha256=sha(dst.read_bytes())))
frozen_write(ROOT/'tools/specs/runtime038_v1_version.json',dict(changes=spec,scope='Read-only exact038 loader/reader/three-root selector/font probe and loaded guards. Historical036 inputs only, coldboot then own038 states; no old-state reuse, aliases or source/RAM modifications. Normal route does not prove new three-class displayed targets.'))
print('Generated038 own coldboot16/read-only probes; no emulator launched')
