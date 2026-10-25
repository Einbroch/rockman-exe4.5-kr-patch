"""Generate tools/build_development_patch_068_v1.py from the 067 generated build (keyboard stage 068).

Then build with: python -X utf8 tools/next_batch_generic_v1.py 068 build
The 066 anchors already drop base patches inside any ' graphic fix: ' region (the native keyboard page 0 tiles/map)
and restore every 'graphics' record's base_hex in the 034..036 view; 068 adds install, view and verification.
"""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tools/build_development_patch_067_v1.py';OUT=ROOT/'tools/build_development_patch_068_v1.py'
G7="__import__('graphics_stage067_v1')";G8="__import__('keyboard_stage068_v1')"
CHANGES=[
 ("        appended,key_patches,keyitem_rom="+G7+".install(source,appended,key_patches,keyitem_rom)",
  "        appended,key_patches,keyitem_rom="+G7+".install(source,appended,key_patches,keyitem_rom)\n        appended,key_patches,keyitem_rom="+G8+".install(source,appended,key_patches,keyitem_rom)"),
 (G7+".predecessor_view(source,target,keyitem_rom)",
  G7+".predecessor_view(source,"+G8+".predecessor_view(source,target,keyitem_rom),keyitem_rom)"),
 (" and "+G7+".verify(source,target,keyitem_rom)",
  " and "+G7+".verify(source,target,keyitem_rom) and "+G8+".verify(source,target,keyitem_rom)"),
 ("    parent066="+G7+".predecessor_view(source,target,result['keyitem_rom'])",
  "    parent067="+G8+".predecessor_view(source,target,result['keyitem_rom'])\n    parent066="+G7+".predecessor_view(source,parent067,result['keyitem_rom'])"),
 ("    "+G7+".verify(source,target,result['keyitem_rom'])",
  "    "+G7+".verify(source,target,result['keyitem_rom'])\n    "+G8+".verify(source,target,result['keyitem_rom'])"),
]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


text=BASE.read_text(encoding='utf8')
for a,b in CHANGES:
    if text.count(a)!=1:raise SystemExit('anchor missing/ambiguous: '+a[:90])
    text=text.replace(a,b)
if OUT.exists() and OUT.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+OUT.name)
OUT.write_text(text,encoding='utf8',newline='\n')
dep={p:sha(ROOT/'tools'/p) for p in ('keyboard_stage068_v1.py','hangul_keyboard_hooks_v1.py','keyboard_page_v1.py','hangul_record_v3.py','hangul_editor_v1.py','hangul_display_hooks_v2.py')}
spec=dict(base=str(BASE.relative_to(ROOT)),base_sha256=sha(BASE),output=str(OUT.relative_to(ROOT)),output_sha256=sha(OUT),changes=CHANGES,dependencies=dep)
(ROOT/'tools/specs/primary068_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('GENERATED 068')
