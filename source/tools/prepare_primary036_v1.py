"""Deterministic mechanical version expansion, preserving all pinned tools."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

BASE='tools/build_development_patch_035_v2.py'
TARGET='tools/build_development_patch_036_v1.py'
EDITS=[
('    from field_npc_rom_product_035_v2 import load_inputs as load_inputs035,install as install_npc035,finalize as finalize035\n',
 '    from field_npc_rom_product_035_v2 import load_inputs as load_inputs035,install as install_npc035,finalize as finalize035\n    from field_npc_rom_product_036_v1 import load_inputs as load_inputs036,install as install_npc036,finalize as finalize036\n'),
('    inputs035=load_inputs035(source)\n','    inputs035=load_inputs035(source)\n    inputs036=load_inputs036(source)\n'),
("    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)\n", "    for entry036,_ in inputs036:\n        asset036=read_json(ROOT/entry036['asset']['path'])\n        needed.update(ch for u in asset036['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)\n"),
("        appended,key_patches,keyitem_rom,npc_records035=install_npc035(source,appended,key_patches,keyitem_rom,inputs035,common,work/'plugins',work/'npc035')\n", "        appended,key_patches,keyitem_rom,npc_records035=install_npc035(source,appended,key_patches,keyitem_rom,inputs035,common,work/'plugins',work/'npc035')\n        appended,key_patches,keyitem_rom,npc_records036=install_npc036(source,appended,key_patches,keyitem_rom,inputs036,common,work/'plugins',work/'npc036')\n"),
('        from field_npc_rom_product_035_v2 import verify_final\n','        from field_npc_rom_product_036_v1 import verify_final\n'),
('    finalize035(source,target,result,inputs035,npc_records035)\n','    finalize035(source,target,result,inputs035,npc_records035)\n    finalize036(source,target,result,inputs036,npc_records036)\n'),
]


def main():
    m=read('poc/output/pending500_035_v2.json');h=m['build_tools_sha256']['build_development_patch_035_v2.py'];require_hash(ROOT/BASE,h)
    text=(ROOT/BASE).read_text(encoding='utf8')
    for before,after in EDITS:
        if text.count(before)!=1:raise ValueError('036 nonunique primary expansion anchor')
        text=text.replace(before,after)
    out=ROOT/TARGET
    if out.exists() and out.read_text(encoding='utf8')!=text:raise ValueError('Preserve previous036 primary')
    if not out.exists():out.write_text(text,encoding='utf8',newline='\n')
    frozen_write(ROOT/'tools/specs/primary036_v1_version.json',dict(schema=1,base=BASE,base_sha256=h,output=TARGET,output_sha256=sha(out.read_bytes()),edits=[dict(before=a,after=b) for a,b in EDITS],generator_sha256=sha((ROOT/'tools/prepare_primary036_v1.py').read_bytes()),scope='Only036 input/glyph/installation/verification/finalization composition; unchanged035 primary bytes otherwise'))
    print('PASS036 primary mechanical expansion, six scoped edits; old tools unchanged')


if __name__=='__main__':main()
