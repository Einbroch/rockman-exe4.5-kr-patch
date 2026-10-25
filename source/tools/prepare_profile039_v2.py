"""Version profile analysis with a separate visible-page EDFF-hold model."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/prepare_profile039_v1.py';dst=ROOT/'tools/prepare_profile_source039_v2.py'
if dst.exists():raise ValueError('Preserve039 profile source analysis')
changes=[('from pet_quick_capacity import PREFIX,validate','from pet_quick_capacity import PREFIX\nfrom profile_quick_geometry039_v1 import validate'),('pending_insertion_500_039_profile_source_v1','pending_insertion_500_039_profile_source_v2'),("profile='pet-quick-explicit132'","profile='profile-quick-zero-speed-visible-hold132'"),('tools/prepare_profile039_v1.py','tools/prepare_profile_source039_v2.py'),("'tools/profile_layout039_v1.py'","'tools/profile_layout039_v1.py','tools/profile_quick_geometry039_v1.py'"),('No translated archive compiled/reinserted yet; source roundtrip','Visible-page EDFF hold and zero text speed are distinct source controls, not ordinary quick dialogue; external option/input overlap is unresolved. No translated archive compiled/reinserted yet; source roundtrip')]
text=src.read_text(encoding='utf8');counts=[]
for a,b in changes:
    n=text.count(a)
    if not n:raise ValueError('039 profile generation anchor')
    counts.append(n);text=text.replace(a,b)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/profile_source039_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),cause='v1 ordinary quick validator correctly rejected native profile textSpeed0 and visible EDFF hold. Distinct analysis-only consumer model added; old validator untouched. External menu interaction proof still missing.',ROM_written=False))
print('Prepared distinct profile source-geometry investigation')
