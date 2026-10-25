"""Mechanical039 extension of pinned038 primary path; no product ROM writer."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from build_layout500_038_v2 import validate_version


def main():
    validate_version();src=ROOT/'tools/build_development_patch_038_v2.py';dst=ROOT/'tools/build_development_patch_039_v1.py'
    if dst.exists():raise ValueError('Preserve039 primary')
    import038='    from field_native_rom_product_038_v2 import load_inputs as load_inputs038,install as install_native038,finalize as finalize038,predecessor_view as predecessor_view038'
    install038="        appended,key_patches,keyitem_rom,native_records038=install_native038(source,appended,key_patches,keyitem_rom,inputs038,common,work/'plugins',work/'native038')"
    final037="    finalize037(source,predecessor_view038(source,target,result['keyitem_rom']),result,inputs037,native_records037)"
    final038='    finalize038(source,target,result,inputs038,native_records038)'
    changes=[
        (import038,import038+'\n    from communication_rom_product039_v1 import load_inputs as load_inputs039,install as install_communication039,finalize as finalize039,predecessor_view as predecessor_view039'),
        ('    inputs038=load_inputs038(source)','    inputs038=load_inputs038(source)\n    inputs039=load_inputs039(source)'),
        ('    for entry038,_ in inputs038:',"    for entry039,_ in inputs039:\n        asset039=read_json(ROOT/entry039['asset']['path'])\n        needed.update(ch for u in asset039['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    for entry038,_ in inputs038:"),
        (install038,install038+"\n        appended,key_patches,keyitem_rom,communication_records039=install_communication039(source,appended,key_patches,keyitem_rom,inputs039,common,work/'plugins',work/'communication039')"),
        ('        from field_native_rom_product_038_v2 import verify_final','        from communication_rom_product039_v1 import verify_final'),
        (final037,"    parent038=predecessor_view039(source,target,result['keyitem_rom'])\n    finalize037(source,predecessor_view038(source,parent038,result['keyitem_rom']),result,inputs037,native_records037)"),
        (final038,'    finalize038(source,parent038,result,inputs038,native_records038)\n    finalize039(source,target,result,inputs039,communication_records039)'),
    ]
    text=src.read_text(encoding='utf8')
    for before,after in changes:
        if text.count(before)!=1:raise ValueError('039 primary exact mechanical anchor '+before)
        text=text.replace(before,after)
    dst.write_text(text,encoding='utf8')
    component=ROOT/'tools/communication_rom_product039_v1.py'
    frozen_write(ROOT/'tools/specs/primary039_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),changes=changes,component=dict(path=str(component.relative_to(ROOT)),sha256=sha(component.read_bytes())),scope='039 communication precise caller extension; preserve all parent gates via hash-verified038 projection; new+500 only; no distribution packages'))
    print('Generated039 primary with inherited gates, no ROM')


if __name__=='__main__':main()
