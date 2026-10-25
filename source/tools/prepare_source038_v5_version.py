"""Compose strict known hint geometry with cleared-page Navi-tail projection."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write

src=ROOT/'tools/prepare_source500_038_v4.py';dst=ROOT/'tools/prepare_source500_038_v5.py'
if dst.exists():raise ValueError('Preserve prior version')
text=src.read_text(encoding='utf8')
changes=[
    ('from prepare_source500_038_v3 import typed_lookup','from prepare_source500_038_v3 import typed_lookup\nfrom normal_navi_tail038_v1 import validate as navi_tail\nfrom field_hint_capacity import validate as hint_validate'),
    ("OUT='analysis/pending_insertion_500_038_source_only_v4'","OUT='analysis/pending_insertion_500_038_source_only_v5'"),
    ("if {x['source_class'] for x in r}=={'native-NPC'}","if {x['source_class'] for x in r} in ({'native-NPC'},{'navi-hint'})"),
    ("validators=[('normal-pages',","validators=[('normal-navi-tail-geometry',lambda a,b,c,d,e:navi_tail(a,b,c,d,e,88)),('fullbox',lambda a,b,c,d,e:hint_validate(a,b,c,d,e,88)),('normal-pages',"),
    ("source_native_lookup_candidates=lookup.get(arc,[]),source_board_lookup_candidates=boards.get(arc,[]),","source_lookup_candidates=typed[arc],source_class=typed[arc][0]['source_class'],"),
    ('tools/prepare_source500_038_v4.py','tools/prepare_source500_038_v5.py'),
    ("deps=['tools/prepare_source500_038_v3.py'","deps=['tools/normal_navi_tail038_v1.py','tools/field_hint_capacity.py','tools/specs/source038_v5_version.json','tools/prepare_source500_038_v3.py'"),
    ('Store native code/CPU effects and battle outcomes unverified for new scope.','Store native code/CPU effects, cleared-page Navi branch continuations and battle outcomes unverified for new scope.'),
    ('A4/B0/B1 lookups are finite static source paths, not natural acquisition.','A4/B0/B1 NPC/board and navi-hint lookups are finite static source paths, not natural acquisition. A4 NPC table is NOT null:53790=08053B18. Earlier prose was incorrect; old classification JSON records false.'),
]
for old,new in changes:
    if text.count(old)!=1:raise ValueError('038v5 exact anchor '+old)
    text=text.replace(old,new,1)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/source038_v5_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Source-only geometry composition. Protected words/commands preserved; native semantics and cumulative carry NOT admitted.'))
print('Generated038v5 source preparation')
