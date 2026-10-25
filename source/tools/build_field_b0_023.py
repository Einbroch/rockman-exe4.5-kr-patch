"""Primary immutable-source build invocation from pinned022 argv plus B0 scope."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from build_arguments import save,validate


def main():
    p=argparse.ArgumentParser();p.add_argument('--repro',action='store_true');a=p.parse_args()
    baseline=read('poc/output/pending500_022_v2.json');ref=baseline['build_argument_manifest'];require_hash(ROOT/ref['path'],ref['sha256'])
    args=list(validate(read(ref['path'])))
    stem='pending500_023_v1'+('_repro' if a.repro else '')
    for flag,value in (('--work','poc/work/'+stem),('--out','poc/output/'+stem+'.gba')):
        if args.count(flag)!=1:raise ValueError('022 argv output coordinate')
        args[args.index(flag)+1]=value
    args+=['--field-b0-hints-023']
    path=ROOT/'poc/build_arguments'/(stem+'.json');h=save(path,args)
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch.py','--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],cwd=ROOT,check=True)


if __name__=='__main__':main()
