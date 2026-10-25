"""Mechanical compiler input/self identity update; all strict checks retained."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    base=ROOT/'tools/compile_source500_037_v1.py';v=read('analysis/pending_insertion_500_037_source_only_v1/verification_v1.json');r=next(x for x in v['tools'] if x['path'].replace('\\','/')=='tools/compile_source500_037_v1.py');require_hash(base,r['sha256']);text=base.read_text(encoding='utf8');dest=ROOT/'tools/compile_source500_037_v2.py'
    if dest.exists():raise ValueError('Preserve compiler version')
    changes=[('from prepare_source500_037_v1 import *','from prepare_source500_037_v2 import *'),('tools/compile_source500_037_v1.py','tools/compile_source500_037_v2.py'),('tools/prepare_source500_037_v1.py','tools/prepare_source500_037_v2.py')]
    for old,new in changes:
        if text.count(old)!=1:raise ValueError('037v2 exact compiler identity anchor')
        text=text.replace(old,new,1)
    dest.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/compile037_v2_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),changes=changes,output=str(dest.relative_to(ROOT)),output_sha256=sha(dest.read_bytes()),scope='No compilation/protected-field/encoding/geometry/font check weakened'))
    print('Generated037v2 strict compiler')

if __name__=='__main__':main()
