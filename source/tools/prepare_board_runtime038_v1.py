"""Prepare038 new board1 default-branch diagnostic, no emulator launch."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
spec=[]
for srcname,dstname in [
    ('tools/capture_board037_v1.py','tools/capture_board038_v1.py'),
    ('tools/capture_board_event037_v2.py','tools/capture_board_event038_v1.py'),
    ('tools/capture_board_qualified037_v1.py','tools/capture_board_qualified038_v1.py'),
]:
    src,dst=ROOT/srcname,ROOT/dstname
    if dst.exists():raise ValueError('Preserve board runtime version')
    text=src.read_text(encoding='utf8');changes=[('037','038')]
    if 'event037' in srcname:pass
    if 'qualified037' in srcname:
        changes += [('capture_board_event038_v2','capture_board_event038_v1'),('source[table+3]!=3','source[table+1]!=1'),('0xF3','0xF1'),('F3','F1'),('returned\\":243','returned\\":241'),('tree','rock')]
        # The JSON literal in Lua is not backslash escaped in Python raw text.
        changes=[(a,b) for a,b in changes if a!='returned\\":243']+ [('"returned":243','"returned":241')]
    counts=[]
    for old,new in changes:
        n=text.count(old)
        if n<1:raise ValueError('038 board runtime anchor '+old)
        counts.append(n);text=text.replace(old,new)
    dst.write_text(text,encoding='utf8');spec.append(dict(base=srcname,base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=dstname,output_sha256=sha(dst.read_bytes())))
frozen_write(ROOT/'tools/specs/board_runtime038_v1_version.json',dict(changes=spec,scope='Exact038 board1 via original F1 source-event table and tile-read alias only. No F3 disabled-flag alias, no Navi/ROM/RAM write. Default MegaMan branch/close/reentry/movement scope, not natural rock access or Guts battle/event completion.'))
print('Generated038 qualified board1 read-alias diagnostic')
