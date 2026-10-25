"""Fix TextPet archive-name provenance by naming the input799314.msg, etc."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write

src=ROOT/'tools/compile_carry038_v1.py';dst=ROOT/'tools/compile_carry038_v2.py'
if dst.exists():raise ValueError('Preserve carry version')
text=src.read_text(encoding='utf8')
changes=[("OUT='analysis/pending_insertion_500_038_carry_v1'","OUT='analysis/pending_insertion_500_038_carry_v2'"),("bp=f/(arc+'_current037.msg');bp.write_bytes(before);","parent_dir=f/'parent';parent_dir.mkdir();bp=parent_dir/(arc+'.msg');bp.write_bytes(before);"),('tools/compile_carry038_v1.py','tools/compile_carry038_v2.py')]
for old,new in changes:
    if text.count(old)!=1:raise ValueError('Exact carry version anchor')
    text=text.replace(old,new,1)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/carry038_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),reason='v1 parent bytes rebuilt identical, but TextPet derives @archive from suffixed input filename, so protected header comparison correctly failed. Correct input basename, never weaken skeleton/binary checks.'))
print('Generated038 carryv2 input-name correction')
