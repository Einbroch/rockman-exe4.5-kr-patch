"""Generate tools/build_development_patch_071_v1.py from the 070 generated build (page 0 navigation stage 071).

Then build with: python -X utf8 tools/next_batch_generic_v1.py 071 build
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools/build_development_patch_070_v1.py';OUT=ROOT/'tools/build_development_patch_071_v1.py'
G0="__import__('keyboard_stage070_v1')";G1="__import__('keyboard_stage071_v1')"
CHANGES=[
 ("        appended,key_patches,keyitem_rom="+G0+".install(source,appended,key_patches,keyitem_rom)",
  "        appended,key_patches,keyitem_rom="+G0+".install(source,appended,key_patches,keyitem_rom)\n        appended,key_patches,keyitem_rom="+G1+".install(source,appended,key_patches,keyitem_rom)"),
 (G0+".predecessor_view(source,target,keyitem_rom)",
  G0+".predecessor_view(source,"+G1+".predecessor_view(source,target,keyitem_rom),keyitem_rom)"),
 (" and "+G0+".verify(source,target,keyitem_rom)",
  " and "+G0+".verify(source,target,keyitem_rom) and "+G1+".verify(source,target,keyitem_rom)"),
 ("    parent069="+G0+".predecessor_view(source,target,result['keyitem_rom'])",
  "    parent070="+G1+".predecessor_view(source,target,result['keyitem_rom'])\n    parent069="+G0+".predecessor_view(source,parent070,result['keyitem_rom'])"),
 ("    "+G0+".verify(source,target,result['keyitem_rom'])",
  "    "+G0+".verify(source,target,result['keyitem_rom'])\n    "+G1+".verify(source,target,result['keyitem_rom'])"),
]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


text=BASE.read_text(encoding='utf8')
MULTI={G0+".predecessor_view(source,target,keyitem_rom)":2}   # the view chain and the keyboard068 verify view
for a,b in CHANGES:
    if text.count(a)!=MULTI.get(a,1):raise SystemExit('anchor missing/ambiguous (%d): %s'%(text.count(a),a[:90]))
    text=text.replace(a,b)
if OUT.exists() and OUT.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+OUT.name)
OUT.write_text(text,encoding='utf8',newline='\n')
dep={p:sha(ROOT/'tools'/p) for p in ('keyboard_stage071_v1.py',)}
spec=dict(base=str(BASE.relative_to(ROOT)),base_sha256=sha(BASE),output=str(OUT.relative_to(ROOT)),output_sha256=sha(OUT),changes=CHANGES,dependencies=dep)
(ROOT/'tools/specs/primary071_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('GENERATED 071')
