"""Rebuild from pinned explicit inputs; change output/work paths only, never reuse compilation."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from build_arguments import validate,save
from cumulative_batch500 import read,frozen_write

def main():
    p=argparse.ArgumentParser();p.add_argument('--parent',required=True);p.add_argument('--parent-sha256',required=True);p.add_argument('--name',required=True);a=p.parse_args()
    if not a.name.replace('_','').isalnum():raise ValueError('Simple artifact name')
    parent=ROOT/a.parent;require_hash(parent,a.parent_sha256);original=validate(read(parent));args=original[:]
    for option,new in [('--work',f'poc/build/{a.name}'),('--out',f'poc/output/{a.name}.gba')]:
        if args.count(option)!=1:raise ValueError('Exact output/work argument population')
        args[args.index(option)+1]=new
    if [i for i,(x,y) in enumerate(zip(original,args)) if x!=y]!=sorted([original.index('--work')+1,original.index('--out')+1]):raise ValueError('Only output/work paths may change')
    work=ROOT/args[args.index('--work')+1];out=ROOT/args[args.index('--out')+1]
    if work.exists() or out.exists() or out.with_suffix('.json').exists():raise ValueError('Preserve all earlier builds')
    path=ROOT/f'poc/build_arguments/{a.name}.json';h=save(path,args)
    frozen_write(path.with_suffix('.lineage.json'),dict(schema=1,parent=str(parent.relative_to(ROOT)),parent_sha256=a.parent_sha256,derived_sha256=h,changed_fields=['--work','--out'],reuse_compiled_artifacts=False,product_build_checks_unchanged=True))
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch.py','--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],check=True,cwd=ROOT)

if __name__=='__main__':main()
