"""Version A4 welcome new038 NPC representative; qualified, not natural."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
spec=[]
for base,dest in [('capture_native_load037_v1.py','capture_native_load038_v1.py'),('capture_native_boundary037_v1.py','capture_native_boundary038_v1.py')]:
    src=ROOT/'tools'/base;dst=ROOT/'tools'/dest
    if dst.exists():raise ValueError('Preserve038 NPC runtime observer')
    changes=[('037','038'),('prepare_native_inputs038_v2','prepare_native_inputs038_v1'),("row['scene'] not in (0xA1,0xA2,0xA3)","row['scene']!=0xA4"),("entry['scene'] not in (0xA1,0xA2,0xA3)","entry['scene']!=0xA4"),("p['scene'] not in (0xA1,0xA2,0xA3)","p['scene']!=0xA4"),('len(row[\'payload\'])>=0x1000','len(row[\'payload\'])>0x3000'),('A1/A2/A3','A4')]
    text=src.read_text(encoding='utf8');applied=[];counts=[]
    for a,b in changes:
        n=text.count(a)
        if n:text=text.replace(a,b);applied.append([a,b]);counts.append(n)
    dst.write_text(text,encoding='utf8');spec.append(dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=applied,replacement_counts=counts,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes())))
frozen_write(ROOT/'tools/specs/npc_runtime038_v1_version.json',dict(changes=spec,scope='A4 new NPC welcome diagnostic. Original scene/sub/day lookup and LZ -> full native boundary in one run; original cached actor/caller -> selector in another, joined only by payload identity. Not natural A4 acquisition.'))
print('Prepared038 A4 qualified NPC load and boundary, not executed')
