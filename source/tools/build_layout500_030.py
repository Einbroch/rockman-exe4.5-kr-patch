"""Current primary invocation: immutable source, frozen023 args,024 inputs."""
import argparse
import subprocess
import sys
from build_visibility_poc import ROOT, require_hash, sha
from cumulative_batch500 import read
from build_arguments import save, validate


def validate_version():
    from build_layout500_029 import validate_version as validate024
    validate024()
    recipe=read('tools/specs/primary030_version.json')
    for item in recipe['files']:
        require_hash(ROOT/item['base'],item['base_sha256'])
        text=(ROOT/item['base']).read_text(encoding='utf-8')
        for edit in item['edits']:
            if text.count(edit['before'])!=1:raise ValueError('025 version anchor nonunique')
            text=text.replace(edit['before'],edit['after'])
        if text!=(ROOT/item['output']).read_text(encoding='utf-8'):
            raise ValueError('025 unexplained primary version difference')
    return sha((ROOT/'tools/specs/primary030_version.json').read_bytes())


def main():
    p=argparse.ArgumentParser();p.add_argument('--repro',action='store_true');a=p.parse_args()
    validate_version()
    baseline=read('poc/output/pending500_029_v1.json');ref=baseline['build_argument_manifest']
    require_hash(ROOT/ref['path'],ref['sha256']);args=list(validate(read(ref['path'])))
    stem='pending500_030_v1'+('_repro' if a.repro else '')
    for flag,value in (('--work','poc/work/'+stem),('--out','poc/output/'+stem+'.gba')):
        if args.count(flag)!=1:raise ValueError('023 argv output coordinate')
        args[args.index(flag)+1]=value
    path=ROOT/'poc/build_arguments'/(stem+'.json');h=save(path,args)
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch_030.py',
        '--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],cwd=ROOT,check=True)


if __name__=='__main__':main()
