"""040 immutable-source cumulative primary/repro entry; old ROM comparison only."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from build_arguments import save,validate


def validate_version():
    from build_layout500_039_v1 import validate_version as prior
    prior();spec=read('tools/specs/primary040_v1_version.json')
    require_hash(ROOT/spec['base'],spec['base_sha256']);require_hash(ROOT/spec['output'],spec['output_sha256']);require_hash(ROOT/spec['component']['path'],spec['component']['sha256']);text=(ROOT/spec['base']).read_text(encoding='utf8')
    for before,after in spec['changes']:
        if text.count(before)!=1:raise ValueError('040 primary generation anchor')
        text=text.replace(before,after)
    if text!=(ROOT/spec['output']).read_text(encoding='utf8'):raise ValueError('040 unexplained primary edit')
    return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--repro',action='store_true');a=p.parse_args();validate_version()
    from typed_rom_product040_v1 import require_admission
    require_admission();old=read('poc/output/pending500_039_v1.json');r=old['build_argument_manifest'];require_hash(ROOT/r['path'],r['sha256']);args=list(validate(read(r['path'])));stem='pending500_040_v1'+('_repro' if a.repro else '')
    if any((ROOT/path).exists() for path in ['poc/work/'+stem,'poc/output/'+stem+'.gba','poc/output/'+stem+'.json']):raise ValueError('Preserve040 work/output')
    for flag,value in [('--work','poc/work/'+stem),('--out','poc/output/'+stem+'.gba')]:
        if args.count(flag)!=1:raise ValueError('040 output coordinate')
        args[args.index(flag)+1]=value
    path=ROOT/'poc/build_arguments'/(stem+'.json');h=save(path,args)
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch_040_v1.py','--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],cwd=ROOT,check=True)


if __name__=='__main__':main()
