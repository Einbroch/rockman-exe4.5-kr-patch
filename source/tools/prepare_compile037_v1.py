"""Mechanical version of the existing strict archive-identity compiler."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    base=ROOT/'tools/compile_source500_036_v2.py';record=read('analysis/pending_insertion_500_036_source_only_v1/verification_v2.json');ref=next(r for r in record['tools'] if r['path'].replace('\\','/')=='tools/compile_source500_036_v2.py');require_hash(base,ref['sha256']);text=base.read_text(encoding='utf8');dest=ROOT/'tools/compile_source500_037_v1.py'
    if dest.exists():raise ValueError('Preserve source compiler version')
    if text.count('from prepare_source500_036_v1 import *')!=1:raise ValueError('Compiler context import anchor')
    new='\"\"\"037 strict source/target archive identity compiler; no product writer.\"\"\"\n'+text[text.index('from prepare_source500_036_v1 import *'):]
    changes=[('from prepare_source500_036_v1 import *','from prepare_source500_037_v1 import *'),('tools/compile_source500_036_v2.py','tools/compile_source500_037_v1.py'),('tools/prepare_source500_036_v1.py','tools/prepare_source500_037_v1.py'),('source036','source037'),('Actual035','Actual036'),("out=ROOT/OUT/'compile_v2'","out=ROOT/OUT/'compile_v1'"),("ROOT/OUT/'verification_v2.json'","ROOT/OUT/'verification_v1.json'"),("previous_attempt=dict(path=OUT+'/compile/79CF04',failure='Archive basename target changed reverse IDs; binary bytes matched but protected ID/topology validation failed. Corrected filename, no reverse/source normalization.')","preparation_scope='Independent037 source-only compile; prior036 filename failure is not a037 attempt'")]
    for old,value in changes:
        if old not in new:raise ValueError('037 exact mechanical compiler anchor '+old)
        new=new.replace(old,value)
    dest.write_text(new,encoding='utf8')
    frozen_write(ROOT/'tools/specs/compile037_v1_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),replacements=changes,header_replaced=True,output=str(dest.relative_to(ROOT)),output_sha256=sha(dest.read_bytes()),scope='Same source/target binary/control/ID roundtrip, untouched scripts and current-ROM glyph contracts; no product writer'))
    print('Generated037 strict source-only compiler')

if __name__=='__main__':main()
