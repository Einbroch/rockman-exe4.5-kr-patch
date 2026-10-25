"""Normalize serialized Windows path separators, keeping every hash/state edge."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/verify_communication_boundary039_v1.py';dst=ROOT/'tools/verify_communication_boundary039_v2.py'
if dst.exists():raise ValueError('Preserve039 boundary verifier')
changes=[("chain[-1]['path'].endswith('pending500-038-normal-v1-01/result.json')","chain[-1]['path'].replace('\\\\','/').endswith('pending500-038-normal-v1-01/result.json')"),('tools/verify_communication_boundary039_v1.py','tools/verify_communication_boundary039_v2.py'),('baseline_boundary_v1.json','baseline_boundary_v2.json')]
text=src.read_text(encoding='utf8');counts=[]
for a,b in changes:
    n=text.count(a)
    if not n:raise ValueError('Boundary verifier version anchor')
    counts.append(n);text=text.replace(a,b)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/communication_boundary039_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),cause='Windows Path serializes ancestry using backslash; suffix test used slash. Normalize separators only for the final identity test; no chain/hash applicability check removed.',ROM_written=False))
print('Prepared039 platform-neutral ancestry suffix check')
