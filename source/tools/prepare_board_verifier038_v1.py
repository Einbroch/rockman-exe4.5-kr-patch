"""Version exact new038 rock-script board consumer audit from037 verifier."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write

src=ROOT/'tools/verify_board_qualified037_v1.py'
dst=ROOT/'tools/verify_board_qualified038_v1.py'
if dst.exists():raise ValueError('Preserve038 board verifier')
text=src.read_text(encoding='utf8')
changes=[
 ('037','038'),
 ('pending_insertion_500_038_native_inputs_v2','pending_insertion_500_038_native_inputs_v1'),
 ('model(rom,m,cfg,arc,3,20','model(rom,m,cfg,arc,1,20'),
 ("'799314:3:0'","'799314:1:0'"),
 ('source[table+3]!=3','source[table+1]!=1'),
 ('Original F3 table target','Original F1 table target'),
 ('pending500-038-board-qualified-v2','pending500-038-board-qualified-v1'),
 ("tile=read(d/'board_tile_alias.json')['reads'];flags=read(d/'board_flag_alias.json')['reads']","tile=read(d/'board_tile_alias.json')['reads'];flags=[]"),
 ("returned=0xF3) for f in (0,300)] or flags!=[dict(frame=f,address=0x02004FA4,original=0x30,returned=0x20) for f in (0,300)]","returned=0xF1) for f in (0,300)]"),
 ('!=(f,3,3,0x02004AD0)','!=(f,1,1,0x02004AD0)'),
 ('[0,0,0,0,3]+[0]*11','[0,0,0,0,1]+[0]*11'),
 ('!=(f,0x0203C800,3)','!=(f,0x0203C800,1)'),
 ('!=(0x0806A502,0x0203C800,3)','!=(0x0806A502,0x0203C800,1)'),
 ('!=(f,3,pool,0x0806A507,0x0203C800)','!=(f,1,pool,0x0806A507,0x0203C800)'),
 ("'tools/capture_board_qualified038_v2.py',",''),
 ('capture_board_event038_v2.py','capture_board_event038_v1.py'),
 ('run_board_qualified038_v2.py','run_board_qualified038_v1.py'),
 ('Two read-result aliases at exact original dispatch/flag instructions; no natural tree event/progression proof.','One tile-read alias at original dispatch instruction, repeated twice; no flag alias or natural rock acquisition proof.'),
 ('not all137 board literals/70archives or all500 actual screens','not all224 board literals/66archives or all500 actual screens'),
 ('source511bytes','full native source'),
 ('qualified tile/flag reads','qualified tile read only'),
 ('natural_tree_acquisition_verified','natural_rock_acquisition_verified'),
]
counts=[]
for a,b in changes:
    count=text.count(a)
    if count<1:raise ValueError('038 board verifier anchor: '+a)
    counts.append(count);text=text.replace(a,b)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/board_verifier038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Actual038 board799314 script1 default Navi branch, native LZ ancestry / real caller / font OBJ pixels / close-reentry-movement. Diagnostic tile alias only; no natural acquisition claim.'))
print('Prepared038 rock-script board audit, not executed')
