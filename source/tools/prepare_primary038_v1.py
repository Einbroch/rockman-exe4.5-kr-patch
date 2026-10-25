"""Seven explicit edits compose038 into pinned037 immutable-source primary."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
src=ROOT/'tools/build_development_patch_037_v2.py';dst=ROOT/'tools/build_development_patch_038_v1.py'
meta=read('poc/output/pending500_037_v2.json');require_hash(src,meta['build_tools_sha256'][src.name])
if dst.exists():raise ValueError('Preserve038 primary version')
text=src.read_text(encoding='utf8');changes=[
    ('    from field_native_rom_product_037_v2 import load_inputs as load_inputs037,install as install_native037,finalize as finalize037\n','    from field_native_rom_product_037_v2 import load_inputs as load_inputs037,install as install_native037,finalize as finalize037\n    from field_native_rom_product_038_v1 import load_inputs as load_inputs038,install as install_native038,finalize as finalize038,predecessor_view as predecessor_view038\n'),
    ('    inputs037=load_inputs037(source)\n','    inputs037=load_inputs037(source)\n    inputs038=load_inputs038(source)\n'),
    ('    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)\n',"    for entry038,_ in inputs038:\n        asset038=read_json(ROOT/entry038['asset']['path'])\n        needed.update(ch for u in asset038['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)\n"),
    ("        appended,key_patches,keyitem_rom,native_records037=install_native037(source,appended,key_patches,keyitem_rom,inputs037,common,work/'plugins',work/'native037')\n","        appended,key_patches,keyitem_rom,native_records037=install_native037(source,appended,key_patches,keyitem_rom,inputs037,common,work/'plugins',work/'native037')\n        appended,key_patches,keyitem_rom,native_records038=install_native038(source,appended,key_patches,keyitem_rom,inputs038,common,work/'plugins',work/'native038')\n"),
    ('        from field_native_rom_product_037_v2 import verify_final\n','        from field_native_rom_product_038_v1 import verify_final\n'),
    ('    finalize037(source,target,result,inputs037,native_records037)\n',"    finalize037(source,predecessor_view038(source,target,result['keyitem_rom']),result,inputs037,native_records037)\n    finalize038(source,target,result,inputs038,native_records038)\n"),
]
for before,after in changes:
    if text.count(before)!=1:raise ValueError('038 primary exact anchor '+before[:80])
    text=text.replace(before,after,1)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/primary038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),component=dict(path='tools/field_native_rom_product_038_v1.py',sha256=sha((ROOT/'tools/field_native_rom_product_038_v1.py').read_bytes())),scope='Same immutable original primary and complete write plan. Prior037 whole-image CPU gate receives source-regenerated verified037 prefix/stub projection; actual038 receives separate full CPU-fixture gate. No patched-ROM input or distribution packaging.'))
print('Generated038 primary; original037 full-image check preserved on verified predecessor projection')
