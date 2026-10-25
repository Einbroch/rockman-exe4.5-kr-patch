"""Correct the second native clear destination from its actual LDR literal."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write,read
import struct
src=ROOT/'tools/bench_tail038_v1.py';dst=ROOT/'tools/bench_tail038_v2.py'
if dst.exists():raise ValueError('Preserve tail bench version')
cfg=read('project.json');original=(ROOT/cfg['source_profile']['filename']).read_bytes()
if struct.unpack_from('<I',original,0x55464)[0]!=0x02013E50:raise ValueError('Second clear decoded literal')
text=src.read_text(encoding='utf8');changes=[('0x06016900','0x02013E50'),('EWRAM/VRAM','two EWRAM blocks'),('tools/bench_tail038_v1.py','tools/bench_tail038_v2.py')]
counts=[]
for old,new in changes:
    count=text.count(old)
    if count<1:raise ValueError('Exact tail bench anchor')
    counts.append(count);text=text.replace(old,new)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/tail038_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),reason='Original5544E LDR points at literal55464=02013E50, not adjacent unused06016900 word. v1 domain check rejected execution before any report/ROM output. Preserve strict native fill-domain enforcement.'))
