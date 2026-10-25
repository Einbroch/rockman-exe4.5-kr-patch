"""Generate tools/build_development_patch_076_v1.py from the 075 generated build (subchip title remnants stage 076).

076 replaces 075's patch of the same block, so every 075 view/verify of the final target first goes through the 076
predecessor view (all occurrences, including the 073/068 checks that already read the 075 view).
Then build with: python -X utf8 tools/next_batch_generic_v1.py 076 build
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools/build_development_patch_075_v1.py';OUT=ROOT/'tools/build_development_patch_076_v1.py'
G0="__import__('graphics_stage075_v1')";G1="__import__('graphics_stage076_v1')"
V1=G1+".predecessor_view(source,target,keyitem_rom)";V2=G1+".predecessor_view(source,target,result['keyitem_rom'])"
CHANGES=[
 ("        appended,key_patches,keyitem_rom="+G0+".install(source,appended,key_patches,keyitem_rom)",
  "        appended,key_patches,keyitem_rom="+G0+".install(source,appended,key_patches,keyitem_rom)\n        appended,key_patches,keyitem_rom="+G1+".install(source,appended,key_patches,keyitem_rom)"),
 (G0+".predecessor_view(source,target,keyitem_rom)",G0+".predecessor_view(source,"+V1+",keyitem_rom)"),
 (G0+".predecessor_view(source,target,result['keyitem_rom'])",G0+".predecessor_view(source,"+V2+",result['keyitem_rom'])"),
 (" and "+G0+".verify(source,target,keyitem_rom)"," and "+G0+".verify(source,"+V1+",keyitem_rom) and "+G1+".verify(source,target,keyitem_rom)"),
 ("    "+G0+".verify(source,target,result['keyitem_rom'])","    "+G0+".verify(source,"+V2+",result['keyitem_rom'])\n    "+G1+".verify(source,target,result['keyitem_rom'])"),
]
MULTI={CHANGES[1][0]:3,CHANGES[2][0]:2}   # chain + 068 + 073 views / parent074 + 073 verify view


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


text=BASE.read_text(encoding='utf8')
for a,b in CHANGES:
    if text.count(a)!=MULTI.get(a,1):raise SystemExit('anchor missing/ambiguous (%d): %s'%(text.count(a),a[:90]))
    text=text.replace(a,b)
if OUT.exists() and OUT.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+OUT.name)
OUT.write_text(text,encoding='utf8',newline='\n')
dep={p:sha(ROOT/'tools'/p) for p in ('graphics_stage076_v1.py',)}
spec=dict(base=str(BASE.relative_to(ROOT)),base_sha256=sha(BASE),output=str(OUT.relative_to(ROOT)),output_sha256=sha(OUT),changes=CHANGES,dependencies=dep)
(ROOT/'tools/specs/primary076_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('GENERATED 076')
