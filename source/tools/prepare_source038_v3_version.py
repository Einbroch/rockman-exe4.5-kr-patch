"""Mechanical static lookup index-scope correction; preserve failed v2."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write

src=ROOT/'tools/prepare_source500_038_v2.py';dst=ROOT/'tools/prepare_source500_038_v3.py'
if dst.exists():raise ValueError('Preserve existing version')
text=src.read_text(encoding='utf8')
changes=[
    ("OUT='analysis/pending_insertion_500_038_source_only_v2'","OUT='analysis/pending_insertion_500_038_source_only_v3'"),
    ("for scene in (0xA0,0xA1,0xA2,0xA3,0xB0,0xB1):","for scene,subcount in ((0xA0,4),(0xA1,4),(0xA2,4),(0xA3,4),(0xA4,2),(0xB0,1),(0xB1,16)):\n        # Explicit finite lookup-index scope, NOT natural scene/sub validity proof."),
    ('for sub in range(4):','for sub in range(subcount):'),
    ('tools/prepare_source500_038_v2.py','tools/prepare_source500_038_v3.py'),
    ('B0/B1 source lookups and A4 hint root/caller are static classifications. Natural A4 field acquisition is NOT inferred from its hint table; NPC table is null.','A4/B0/B1 NPC and board plus navi-hint lookups are static index-path classifications, NOT natural acquisition. Earlier prose claiming A4 NPC table null was incorrect: actual top53790=08053B18; old classification JSON already records false.'),
]
for old,new in changes:
    count=text.count(old)
    expected=2 if old=='for sub in range(4):' else 1
    if count!=expected:raise ValueError('Exact version anchor '+old)
    text=text.replace(old,new)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/source038_v3_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Static lookup finite index counts corrected; no geometry/protected-field/whole500 gate weakened. Natural sub-area validity remains unverified.'))
print('Generated038 v3 finite typed lookup preparation')
