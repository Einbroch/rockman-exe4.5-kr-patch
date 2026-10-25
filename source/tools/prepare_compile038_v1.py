"""Version strict037 compiler for038 source-only contracts, not product input."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

src=ROOT/'tools/compile_source500_037_v2.py';dst=ROOT/'tools/compile_source500_038_v1.py'
v=read('analysis/pending_insertion_500_037_source_only_v2/verification_v1.json')
ref=next(x for x in v['tools'] if x['path'].replace('\\','/')=='tools/compile_source500_037_v2.py');require_hash(src,ref['sha256'])
if dst.exists():raise ValueError('Preserve compiler version')
text=src.read_text(encoding='utf8')
changes=[
    ('from prepare_source500_037_v2 import *','from prepare_source500_038_v5 import *\nfrom normal_navi_tail038_v1 import validate as navi_tail\nfrom normal_store_tail038_v1 import validate as store_tail\nfrom field_hint_capacity import validate as hint_validate'),
    ('validators=dict(VALIDATORS)',"validators=dict(VALIDATORS);validators.update({'normal-navi-tail-geometry':lambda a,b,c,d,e:navi_tail(a,b,c,d,e,88),'normal-store-tail-geometry':lambda a,b,c,d,e:store_tail(a,b,c,d,e,88),'fullbox':lambda a,b,c,d,e:hint_validate(a,b,c,d,e,88)})"),
    ('tools/compile_source500_037_v2.py','tools/compile_source500_038_v1.py'),
    ('tools/prepare_source500_037_v2.py','tools/prepare_source500_038_v5.py'),
    ('PASS source037','PASS source038'),
    ('Actual036 glyph supply ','Actual037 glyph supply '),
    ('Independent037 source-only compile; prior036 filename failure is not a037 attempt','038 source-only targets preserve unselected SOURCE scripts, NOT current037 translations. These targets must NOT replace an existing cumulative archive. Carry/supersession and native tail/branch evidence remain product blockers.'),
]
for old,new in changes:
    count=text.count(old);expected=2 if old=='PASS source037' else 1
    if count!=expected:raise ValueError('038 compiler anchor '+old+': '+str(count))
    text=text.replace(old,new)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/compile038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Strict complete-source/protected-target/binary roundtrips/unselected-source/font checks retained. Geometry-only profiles do not admit native execution or current-clone replacement.'))
print('Generated038 strict source-only compiler')
