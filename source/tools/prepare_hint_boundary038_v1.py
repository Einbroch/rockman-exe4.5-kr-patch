"""Version qualified resident boundary probe for real L-hint caller."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/capture_native_boundary037_v1.py';dst=ROOT/'tools/capture_hint_boundary038_v1.py'
if dst.exists():raise ValueError('Preserve hint boundary observer')
text=src.read_text(encoding='utf8')
changes=[('037','038'),('qualified_native_001.bin','qualified_hint_001.bin'),("p['source_class']!='native-NPC' or p['scene'] not in (0xA1,0xA2,0xA3)","p['source_class']!='navi-hint' or archive!='78AE58' or p['scene']!=0xA3"),('0x02039800','0x0203D800'),('0x0804F773','0x0804F807'),('original NPC caller','original hint caller'),('native A0 actor/caller','native A0 L-hint caller'),('NOT natural target scene/actor acquisition','NOT natural A3/ShadowMan acquisition'),('Borrowed actor scene applicability','Borrowed hint scene applicability')]
counts=[]
for a,b in changes:
    n=text.count(a)
    if n<1:raise ValueError('Hint boundary generation anchor: '+a)
    counts.append(n);text=text.replace(a,b)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/hint_boundary038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Qualified full-native byte/scene aliases at038 selector only; own038 native LZ prerequisite; actual original L provider/BL/root preserved. Not natural acquisition.'))
print('Prepared038 hint resident-boundary probe, not executed')
