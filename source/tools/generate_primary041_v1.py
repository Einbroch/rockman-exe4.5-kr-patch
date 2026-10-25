"""Generate build_development_patch_041_v1.py from040_v2 by exact anchored edits; writes spec."""
import json
from build_visibility_poc import ROOT,sha

BASE='tools/build_development_patch_040_v2.py';OUT='tools/build_development_patch_041_v1.py';SPEC='tools/specs/primary041_v1_version.json';COMP='tools/typed_rom_product041_v1.py'
CHANGES=[
 ("    from typed_rom_product040_v2 import load_inputs as load_inputs040,install as install_typed040,finalize as finalize040,predecessor_view as predecessor_view040",
  "    from typed_rom_product040_v2 import load_inputs as load_inputs040,install as install_typed040,finalize as finalize040,predecessor_view as predecessor_view040\n    from typed_rom_product041_v1 import load_inputs as load_inputs041,install as install_typed041,finalize as finalize041,predecessor_view as predecessor_view041"),
 ("    inputs040=load_inputs040(source)","    inputs040=load_inputs040(source)\n    inputs041=load_inputs041(source)"),
 ("    for entry040,_ in inputs040:",
  "    for entry041,*_ in inputs041:\n        asset041=read_json(ROOT/entry041['asset']['path'])\n        needed.update(ch for u in asset041['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    for entry040,_ in inputs040:"),
 ("        appended,key_patches,keyitem_rom,typed_records040=install_typed040(source,appended,key_patches,keyitem_rom,inputs040,common,work/'plugins',work/'typed040')",
  "        appended,key_patches,keyitem_rom,typed_records040=install_typed040(source,appended,key_patches,keyitem_rom,inputs040,common,work/'plugins',work/'typed040')\n        appended,key_patches,keyitem_rom,typed_records041=install_typed041(source,appended,key_patches,keyitem_rom,inputs041,common,work/'plugins',work/'typed041')"),
 ("        from typed_rom_product040_v2 import verify_final","        from typed_rom_product041_v1 import verify_final"),
 ("    parent039=predecessor_view040(source,target,result['keyitem_rom'])",
  "    parent040=predecessor_view041(source,target,result['keyitem_rom'])\n    parent039=predecessor_view040(source,parent040,result['keyitem_rom'])"),
 ("    finalize040(source,target,result,inputs040,typed_records040)",
  "    finalize040(source,parent040,result,inputs040,typed_records040)\n    finalize041(source,target,result,inputs041,typed_records041)"),
]

def main():
    text=(ROOT/BASE).read_text(encoding='utf8')
    for before,after in CHANGES:
        if text.count(before)!=1:raise ValueError('041 anchor: '+before[:60])
        text=text.replace(before,after)
    out=ROOT/OUT
    if out.exists() and out.read_text(encoding='utf8')!=text:raise ValueError('Preserve existing041 primary')
    out.write_text(text,encoding='utf8',newline='\n')
    spec=dict(base=BASE,base_sha256=sha((ROOT/BASE).read_bytes()),output=OUT,output_sha256=sha(out.read_bytes()),changes=CHANGES,component=dict(path=COMP,sha256=sha((ROOT/COMP).read_bytes())),scope='041 exact500 new + carry156 over53 archives; one composed root/full-bytes selector over040; no distribution packages')
    (ROOT/SPEC).write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS generated',OUT,spec['output_sha256'])

if __name__=='__main__':main()
