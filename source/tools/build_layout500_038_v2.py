"""038 corrected metadata primary/rebuild, original source and exact500 only."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,require_hash,sha
from cumulative_batch500 import read
from build_arguments import save,validate

def validate_version():
    from build_layout500_038_v1 import validate_version as prior
    prior();spec=read('tools/specs/primary038_v2_version.json')
    for r in spec['changes']:
        require_hash(ROOT/r['base'],r['base_sha256']);require_hash(ROOT/r['output'],r['output_sha256']);text=(ROOT/r['base']).read_text(encoding='utf8')
        for (before,after),count in zip(r['changes'],r['replacement_counts']):
            if text.count(before)!=count:raise ValueError('038v2 generation anchor')
            text=text.replace(before,after)
        if text!=(ROOT/r['output']).read_text(encoding='utf8'):raise ValueError('038v2 unexplained generated edit')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--repro',action='store_true');a=p.parse_args();validate_version()
    from field_native_rom_product_038_v2 import require_admission
    require_admission();old=read('poc/output/pending500_037_v2.json');r=old['build_argument_manifest'];require_hash(ROOT/r['path'],r['sha256']);args=list(validate(read(r['path'])))
    stem='pending500_038_v2'+('_repro' if a.repro else '')
    if any((ROOT/path).exists() for path in ['poc/work/'+stem,'poc/output/'+stem+'.gba','poc/output/'+stem+'.json']):raise ValueError('Preserve038v2 work/output')
    for flag,value in [('--work','poc/work/'+stem),('--out','poc/output/'+stem+'.gba')]:
        if args.count(flag)!=1:raise ValueError('038v2 output coordinate')
        args[args.index(flag)+1]=value
    path=ROOT/'poc/build_arguments'/(stem+'.json');h=save(path,args)
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch_038_v2.py','--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],cwd=ROOT,check=True)

if __name__=='__main__':main()
