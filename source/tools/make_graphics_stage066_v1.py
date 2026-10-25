"""Generate tools/build_development_patch_066_v1.py from the 065 generated build (graphics-only stage).

Then build with: python -X utf8 tools/next_batch_generic_v1.py 066 build
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools/build_development_patch_065_v1.py';OUT=ROOT/'tools/build_development_patch_066_v1.py'
G="__import__('graphics_stage066_v1')"
CHANGES=[
 ("        appended,key_patches,keyitem_rom,typed_records065=install_typed065(source,appended,key_patches,keyitem_rom,inputs065,common,work/'plugins',work/'typed065')",
  "        appended,key_patches,keyitem_rom,typed_records065=install_typed065(source,appended,key_patches,keyitem_rom,inputs065,common,work/'plugins',work/'typed065')\n        appended,key_patches,keyitem_rom="+G+".install(source,appended,key_patches,keyitem_rom)"),
 ("    target, allowed, writes = bytearray(source + appended), bytearray(len(source)), []",
  "    _own=[(_p[0],_p[0]+len(_p[1])) for _p in patches if "+G+".TAG in _p[2]]\n    patches=[_p for _p in patches if "+G+".TAG in _p[2] or not any(_a<=_p[0] and _p[0]+len(_p[1])<=_b for _a,_b in _own)]\n    target, allowed, writes = bytearray(source + appended), bytearray(len(source)), []"),
 ("    nolabel=bytes(nolabel)\n    finalize034(",
  "    for _v in result['keyitem_rom'].values():\n        for _r in (_v.get('graphics',[]) if isinstance(_v,dict) else []):nolabel[_r['offset']:_r['offset']+_r['size']]=bytes.fromhex(_r['base_hex'])\n    nolabel=bytes(nolabel)\n    finalize034("),
 ("        keyitem_rom['final_placement_verified']=verify_final(source,target,keyitem_rom)",
  "        keyitem_rom['final_placement_verified']=verify_final(source,"+G+".predecessor_view(source,target,keyitem_rom),keyitem_rom) and "+G+".verify(source,target,keyitem_rom)"),
 ("    parent064=predecessor_view065(source,target,result['keyitem_rom'])",
  "    parent065="+G+".predecessor_view(source,target,result['keyitem_rom'])\n    parent064=predecessor_view065(source,parent065,result['keyitem_rom'])"),
 ("    finalize065(source,target,result,inputs065,typed_records065)",
  "    finalize065(source,parent065,result,inputs065,typed_records065)\n    "+G+".verify(source,target,result['keyitem_rom'])"),
]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


text=BASE.read_text(encoding='utf8')
for a,b in CHANGES:
    if text.count(a)!=1:raise SystemExit('anchor missing: '+a[:80])
    text=text.replace(a,b)
if OUT.exists() and OUT.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+OUT.name)
OUT.write_text(text,encoding='utf8',newline='\n')
spec=dict(base=str(BASE.relative_to(ROOT)),base_sha256=sha(BASE),output=str(OUT.relative_to(ROOT)),output_sha256=sha(OUT),changes=CHANGES,
          component=dict(path='tools/graphics_stage066_v1.py',sha256=sha(ROOT/'tools/graphics_stage066_v1.py')),
          fixes=dict(path='tools/graphics_fix_v1.py',sha256=sha(ROOT/'tools/graphics_fix_v1.py')))
(ROOT/'tools/specs/primary066_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('GENERATED 066')
