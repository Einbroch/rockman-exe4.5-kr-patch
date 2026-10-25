"""Canonical JSON geometry comparison, preserving failed compile_v1."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/compile_communication039_v1.py';dst=ROOT/'tools/compile_communication039_v2.py'
if dst.exists():raise ValueError('Preserve039 compiler version')
changes=[('import re\n','import re,json\n'),("OUT/'compile_v1'","OUT/'compile_v2'"),("validate(original,replace_exact(original,subset),[g['script']],set(g['ids']))!=g['geometry']","json.loads(json.dumps(validate(original,replace_exact(original,subset),[g['script']],set(g['ids'])),ensure_ascii=False))!=g['geometry']"),('tools/compile_communication039_v1.py','tools/compile_communication039_v2.py'),("OUT/'verification_v1.json'","OUT/'verification_v2.json'")]
text=src.read_text(encoding='utf8');counts=[]
for a,b in changes:
    n=text.count(a)
    if not n:raise ValueError('Compiler039 version anchor')
    counts.append(n);text=text.replace(a,b)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/compile_communication039_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),cause='PREFIX tuples serialize to JSON arrays. Compare live geometry in its canonical JSON representation with the report, without dropping any fields. v1 stopped before archive compile; partial directory and source/tool retained.',ROM_written=False))
print('Prepared039 JSON-representation geometry comparison')
