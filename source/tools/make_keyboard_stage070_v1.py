"""Generate tools/build_development_patch_070_v1.py from the 069 generated build (confirm guard stage 070).

Then build with: python -X utf8 tools/next_batch_generic_v1.py 070 build
070 re-patches the 068 keys stub, so every keyboard068 verify/view is fed the 070-restored image.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools/build_development_patch_069_v1.py';OUT=ROOT/'tools/build_development_patch_070_v1.py'
G8="__import__('keyboard_stage068_v1')";G9="__import__('keyboard_stage069_v1')";G0="__import__('keyboard_stage070_v1')"
CHANGES=[
 ("        appended,key_patches,keyitem_rom="+G9+".install(source,appended,key_patches,keyitem_rom)",
  "        appended,key_patches,keyitem_rom="+G9+".install(source,appended,key_patches,keyitem_rom)\n        appended,key_patches,keyitem_rom="+G0+".install(source,appended,key_patches,keyitem_rom)"),
 (G9+".predecessor_view(source,target,keyitem_rom)",
  G9+".predecessor_view(source,"+G0+".predecessor_view(source,target,keyitem_rom),keyitem_rom)"),
 (" and "+G8+".verify(source,target,keyitem_rom)",
  " and "+G8+".verify(source,"+G0+".predecessor_view(source,target,keyitem_rom),keyitem_rom)"),
 (" and "+G9+".verify(source,target,keyitem_rom)",
  " and "+G9+".verify(source,target,keyitem_rom) and "+G0+".verify(source,target,keyitem_rom)"),
 ("    parent068="+G9+".predecessor_view(source,target,result['keyitem_rom'])",
  "    parent069="+G0+".predecessor_view(source,target,result['keyitem_rom'])\n    parent068="+G9+".predecessor_view(source,parent069,result['keyitem_rom'])"),
 ("    "+G8+".verify(source,target,result['keyitem_rom'])",
  "    "+G8+".verify(source,"+G0+".predecessor_view(source,target,result['keyitem_rom']),result['keyitem_rom'])"),
 ("    "+G9+".verify(source,target,result['keyitem_rom'])",
  "    "+G9+".verify(source,target,result['keyitem_rom'])\n    "+G0+".verify(source,target,result['keyitem_rom'])"),
]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


text=BASE.read_text(encoding='utf8')
for a,b in CHANGES:
    if text.count(a)!=1:raise SystemExit('anchor missing/ambiguous: '+a[:90])
    text=text.replace(a,b)
if OUT.exists() and OUT.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+OUT.name)
OUT.write_text(text,encoding='utf8',newline='\n')
dep={p:sha(ROOT/'tools'/p) for p in ('keyboard_stage070_v1.py','hangul_keyboard_hooks_v3.py','hangul_keyboard_hooks_v1.py','hangul_record_v3.py','hangul_display_hooks_v2.py')}
spec=dict(base=str(BASE.relative_to(ROOT)),base_sha256=sha(BASE),output=str(OUT.relative_to(ROOT)),output_sha256=sha(OUT),changes=CHANGES,dependencies=dep)
(ROOT/'tools/specs/primary070_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('GENERATED 070')
