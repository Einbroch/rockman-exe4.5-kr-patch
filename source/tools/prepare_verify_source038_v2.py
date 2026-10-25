"""Fix helper/loop name shadowing without weakening any preflight check."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/verify_source038_v1.py';dst=ROOT/'tools/verify_source038_v2.py'
if dst.exists():raise ValueError('Preserve verifier')
text=src.read_text(encoding='utf8');changes=[('def ref(p):','def receipt(p):'),('=ref(','=receipt('),('tools/verify_source038_v1.py','tools/verify_source038_v2.py')]
for old,new in changes:
    if text.count(old)!=(3 if old=='=ref(' else 1):raise ValueError('Exact verifier anchor')
    text=text.replace(old,new)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/verify_source038_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Receipt helper naming only; all source/table/roundtrip/carry/alias checks unchanged.'))
