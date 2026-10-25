"""Extend the same strict survey to finite A4/B0/B1 source lookup paths."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write

src=ROOT/'tools/prepare_source500_038_v1.py';dst=ROOT/'tools/prepare_source500_038_v4.py'
if dst.exists():raise ValueError('Preserve prior version')
text=src.read_text(encoding='utf8')
changes=[
    ('from archive_scripts import script_spans','from archive_scripts import script_spans\nfrom prepare_source500_038_v3 import typed_lookup'),
    ("OUT='analysis/pending_insertion_500_038_source_only_v1'","OUT='analysis/pending_insertion_500_038_source_only_v4'"),
    ('lookup=native_lookup(source);boards=board_lookup(source);templates={};drafts={};good=[];bad=[]',"typed=typed_lookup(source);lookup={a:r for a,r in typed.items() if {x['source_class'] for x in r}=={'native-NPC'}};boards={a:r for a,r in typed.items() if {x['source_class'] for x in r}=={'field-board'}};templates={};drafts={};good=[];bad=[]"),
    ('tools/prepare_source500_038_v1.py','tools/prepare_source500_038_v4.py'),
    ("deps=[CENSUS,","deps=['tools/prepare_source500_038_v3.py','tools/specs/source038_v4_version.json',CENSUS,"),
    ('Already owned archives require full carry and supersession integration; source-only target must never replace current translated archive.','A4/B0/B1 lookups are finite static source paths, not natural acquisition. Already owned archives require full carry and supersession integration; source-only target must never replace current translated archive.'),
]
for old,new in changes:
    if text.count(old)!=1:raise ValueError('038 v4 exact anchor '+old)
    text=text.replace(old,new,1)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/source038_v4_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Source-only survey uses same normal/tail geometry rules on explicit additional NPC/board lookup index paths; no runtime/product admission.'))
print('Generated038v4 typed NPC/board survey')
