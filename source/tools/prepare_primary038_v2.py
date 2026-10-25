"""Separate historical parent identity from live consumer records in metadata."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

spec=read('tools/specs/primary038_v1_version.json');require_hash(ROOT/spec['component']['path'],spec['component']['sha256']);records=[]
for srcname,dstname,changes in [
    ('tools/field_native_rom_product_038_v1.py','tools/field_native_rom_product_038_v2.py',[
        ("supersedes_parent_record=r['parent_record']","supersedes_parent_record=(dict(archive=r['parent_record']['archive'],rom_offset=r['parent_record']['rom_offset'],compiled_sha256=r['parent_record']['compiled_sha256']) if r['parent_record'] else None)"),
        ('tools/build_development_patch_038_v1.py','tools/build_development_patch_038_v2.py')]),
    ('tools/build_development_patch_038_v1.py','tools/build_development_patch_038_v2.py',[
        ('field_native_rom_product_038_v1','field_native_rom_product_038_v2')]),
    ('tools/bench_product_component038_v1.py','tools/bench_product_component038_v2.py',[
        ('field_native_rom_product_038_v1','field_native_rom_product_038_v2'),
        ('analysis/pending_insertion_500_038_component_fixture_v1','analysis/pending_insertion_500_038_component_fixture_v2'),
        ('tools/bench_product_component038_v1.py','tools/bench_product_component038_v2.py')]),
]:
    src,dst=ROOT/srcname,ROOT/dstname
    if dst.exists():raise ValueError('Preserve038 v2 files')
    text=src.read_text(encoding='utf8');counts=[]
    for old,new in changes:
        n=text.count(old);expected=2 if old=='field_native_rom_product_038_v1' else 1
        if n!=expected:raise ValueError('038v2 exact anchor '+old+':'+str(n))
        counts.append(n);text=text.replace(old,new)
    dst.write_text(text,encoding='utf8');records.append(dict(base=srcname,base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=dstname,output_sha256=sha(dst.read_bytes())))
frozen_write(ROOT/'tools/specs/primary038_v2_version.json',dict(changes=records,reason='v1 embedded24 full parent clone dicts under ancestry; recursive consumer inventory counted24 extra non-live records. v2 retains only archive/offset/hash historical identity. No compiled payload, selector byte or fixture ROM hash changes; source038 remains exact500. v1 builds stopped before ROM output and all attempted files preserved.'))
print('Generated038 v2: historical identities no longer look like live consumers')
