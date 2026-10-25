"""Generate tools/build_development_patch_067_v1.py from the 066 generated build (graphics-only stage 067).

Then build with: python -X utf8 tools/next_batch_generic_v1.py 067 build
The generic 066 anchors already drop base patches inside any ' graphic fix: ' region and restore every
'graphics' record's base_hex in the 034..036 view; 067 adds its own install, view and verification.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools/build_development_patch_066_v1.py';OUT=ROOT/'tools/build_development_patch_067_v1.py'
G6="__import__('graphics_stage066_v1')";G7="__import__('graphics_stage067_v1')"
CHANGES=[
 ("        appended,key_patches,keyitem_rom="+G6+".install(source,appended,key_patches,keyitem_rom)",
  "        appended,key_patches,keyitem_rom="+G6+".install(source,appended,key_patches,keyitem_rom)\n        appended,key_patches,keyitem_rom="+G7+".install(source,appended,key_patches,keyitem_rom)"),
 ("verify_final(source,"+G6+".predecessor_view(source,target,keyitem_rom),keyitem_rom) and "+G6+".verify(source,target,keyitem_rom)",
  "verify_final(source,"+G6+".predecessor_view(source,"+G7+".predecessor_view(source,target,keyitem_rom),keyitem_rom),keyitem_rom) and "+G6+".verify(source,target,keyitem_rom) and "+G7+".verify(source,target,keyitem_rom)"),
 ("    parent065="+G6+".predecessor_view(source,target,result['keyitem_rom'])",
  "    parent066="+G7+".predecessor_view(source,target,result['keyitem_rom'])\n    parent065="+G6+".predecessor_view(source,parent066,result['keyitem_rom'])"),
 ("    "+G6+".verify(source,target,result['keyitem_rom'])",
  "    "+G6+".verify(source,target,result['keyitem_rom'])\n    "+G7+".verify(source,target,result['keyitem_rom'])"),
]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


text=BASE.read_text(encoding='utf8')
for a,b in CHANGES:
    if text.count(a)!=1:raise SystemExit('anchor missing: '+a[:80])
    text=text.replace(a,b)
if OUT.exists() and OUT.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+OUT.name)
OUT.write_text(text,encoding='utf8',newline='\n')
spec=dict(base=str(BASE.relative_to(ROOT)),base_sha256=sha(BASE),output=str(OUT.relative_to(ROOT)),output_sha256=sha(OUT),changes=CHANGES,
          component=dict(path='tools/graphics_stage067_v1.py',sha256=sha(ROOT/'tools/graphics_stage067_v1.py')),
          fixes=dict(path='tools/graphics_fix_v2.py',sha256=sha(ROOT/'tools/graphics_fix_v2.py')))
(ROOT/'tools/specs/primary067_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('GENERATED 067')
