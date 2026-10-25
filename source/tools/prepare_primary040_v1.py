"""Mechanical040 extension of pinned039 primary; no alternate ROM writer."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from build_layout500_039_v1 import validate_version


def main():
    validate_version();src=ROOT/'tools/build_development_patch_039_v1.py';dst=ROOT/'tools/build_development_patch_040_v1.py'
    if dst.exists():raise ValueError('Preserve040 primary')
    import039='    from communication_rom_product039_v1 import load_inputs as load_inputs039,install as install_communication039,finalize as finalize039,predecessor_view as predecessor_view039'
    install039="        appended,key_patches,keyitem_rom,communication_records039=install_communication039(source,appended,key_patches,keyitem_rom,inputs039,common,work/'plugins',work/'communication039')"
    changes=[
        (import039,import039+'\n    from typed_rom_product040_v1 import load_inputs as load_inputs040,install as install_typed040,finalize as finalize040,predecessor_view as predecessor_view040'),
        ('    inputs039=load_inputs039(source)','    inputs039=load_inputs039(source)\n    inputs040=load_inputs040(source)'),
        ('    for entry039,_ in inputs039:',"    for entry040,_ in inputs040:\n        asset040=read_json(ROOT/entry040['asset']['path'])\n        needed.update(ch for u in asset040['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    for entry039,_ in inputs039:"),
        (install039,install039+"\n        appended,key_patches,keyitem_rom,typed_records040=install_typed040(source,appended,key_patches,keyitem_rom,inputs040,common,work/'plugins',work/'typed040')"),
        ('        from communication_rom_product039_v1 import verify_final','        from typed_rom_product040_v1 import verify_final'),
        ("    parent038=predecessor_view039(source,target,result['keyitem_rom'])","    parent039=predecessor_view040(source,target,result['keyitem_rom'])\n    parent038=predecessor_view039(source,parent039,result['keyitem_rom'])"),
        ('    finalize039(source,target,result,inputs039,communication_records039)','    finalize039(source,parent039,result,inputs039,communication_records039)\n    finalize040(source,target,result,inputs040,typed_records040)'),
    ]
    text=src.read_text(encoding='utf8')
    for before,after in changes:
        if text.count(before)!=1:raise ValueError('040 primary exact mechanical anchor '+before)
        text=text.replace(before,after)
    dst.write_text(text,encoding='utf8')
    component=ROOT/'tools/typed_rom_product040_v1.py'
    frozen_write(ROOT/'tools/specs/primary040_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),changes=changes,component=dict(path=str(component.relative_to(ROOT)),sha256=sha(component.read_bytes())),scope='040 source500 pluscarry8 typed extension; all parent gates preserved via039 projection; no distribution packages'))
    print('Generated040 primary preserving039 gates; NO ROM')


if __name__=='__main__':main()
