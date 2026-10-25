"""Actual038 corruption checker: all descriptor fields in each caller class."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/verify_integrity037_v1.py';dst=ROOT/'tools/verify_integrity038_v1.py'
if dst.exists():raise ValueError('Preserve integrity checker')
text=src.read_text(encoding='utf8');changes=[('037','038'),('npc036','npc037'),("classes=sorted({(p['source_class'],p['scene']) for p in n['placements']})","classes=[(kind,next(p['scene'] for p in n['placements'] if p['source_class']==kind)) for kind in sorted({p['source_class'] for p in n['placements']})]"),('prior036-wrapper','prior037-wrapper')]
counts=[]
for old,new in changes:
    n=text.count(old)
    if n<1:raise ValueError('038 integrity anchor '+old)
    counts.append(n);text=text.replace(old,new)
dst.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/integrity038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Actual038 full validator. Representative first descriptor in each of3 caller classes, all7 fields/native-target source boundaries/source pointer+LZ, stub/wrapper/prior037 chain/missing placement. Not every scene/index fault or malformed input. No corruption saved to disk.'))
print('Generated038 actual-image corruption checker; not run yet')
