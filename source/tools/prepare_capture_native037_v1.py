"""Version field observation for037 typed root/caller, no state interventions."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_native_product037_v1 import create


def main():
    base='tools/capture_field_loader_036_v1.py';history=read('analysis/pending500_036_v1/normal_field_progress_v2.json');require_hash(ROOT/base,history['dependencies'][base]);text=(ROOT/base).read_text(encoding='utf8')
    edits=[
      ('036','037',text.count('036')),
      ('{0x0804F76E,0x0804F780,0x0804F802}','{0x0804F76E,0x0804F780,0x0804F802,0x0806A502}',1),
      ("if s['cpu.r0']==0x02039800 then","if s['cpu.r0']==0x02039800 or s['cpu.r0']==0x0203C800 then",1),
      ("selectorPending={start=s['cpu.cycleCount'],script=s['cpu.r1'],frame=frame,caller=s['cpu.r14']}","selectorPending={start=s['cpu.cycleCount'],script=s['cpu.r1'],frame=frame,caller=s['cpu.r14'],native_root=s['cpu.r0']}",1),
      ('\"caller_lr\":%d}\',selectorPending.frame,selectorPending.script,root,s[\'cpu.cycleCount\']-selectorPending.start,selectorPending.caller)', '\"caller_lr\":%d,\"native_root\":%d}\',selectorPending.frame,selectorPending.script,root,s[\'cpu.cycleCount\']-selectorPending.start,selectorPending.caller,selectorPending.native_root)',1),
    ]
    r=create('tools/capture_field_loader_037_v1.py',base,text,edits)
    frozen_write(ROOT/'tools/specs/field_capture037_v1_version.json',dict(change=r,generator_sha256=sha((ROOT/'tools/prepare_capture_native037_v1.py').read_bytes())))
    print('PASS037 read-only observation tool generated')


if __name__=='__main__':main()
