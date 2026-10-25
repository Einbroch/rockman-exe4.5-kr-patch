"""Treat the project's require_hash SystemExit as a deliberate refusal."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/verify_input_guards038_v1.py';dst=ROOT/'tools/verify_input_guards038_v2.py'
if dst.exists():raise ValueError('Preserve input refusal checker')
text=src.read_text(encoding='utf8');changes=[('except (ValueError,KeyError,IndexError) as e:','except (ValueError,KeyError,IndexError,SystemExit) as e:'),('tools/verify_input_guards038_v1.py','tools/verify_input_guards038_v2.py')]
for old,new in changes:
    if text.count(old)!=1:raise ValueError('038 refusal checker anchor')
    text=text.replace(old,new,1)
dst.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/input_guards038_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),reason='v1 stopped at intended compiled-hash rejection because require_hash raises SystemExit. Accept that exception as refusal in the checker; primary enforcement unchanged; actual files unmodified.'))
