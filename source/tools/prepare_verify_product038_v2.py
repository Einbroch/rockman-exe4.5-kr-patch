"""Bind the existing full artifact audit to corrected product component v2."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
spec=read('tools/specs/verify_product038_v1_version.json');src=ROOT/spec['output'];require_hash(src,spec['output_sha256']);dst=ROOT/'tools/verify_native_product038_v2.py'
if dst.exists():raise ValueError('Preserve audit version')
text=src.read_text(encoding='utf8');changes=[('field_native_rom_product_038_v1','field_native_rom_product_038_v2'),('tools/verify_native_product038_v1.py','tools/verify_native_product038_v2.py'),('tools/specs/primary038_v1_version.json','tools/specs/primary038_v2_version.json')]
for old,new in changes:
    expected=2 if old=='field_native_rom_product_038_v1' else 1
    if text.count(old)!=expected:raise ValueError('038v2 audit anchor')
    text=text.replace(old,new)
dst.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/verify_product038_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Component/primary identity only; full-write/old578/exact500/carry/rebuild checks unchanged.'))
