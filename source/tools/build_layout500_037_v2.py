"""037 development primary from immutable original; no package creation."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,require_hash,sha
from cumulative_batch500 import read
from build_arguments import save,validate


def validate_version():
    from build_layout500_036_v1 import validate_version as prior
    prior()
    for name in ['native037_v2_version.json','primary037_v1_version.json','primary037_v2_version.json']:
        r=read('tools/specs/'+name)
        for c in r['changes']:
            require_hash(ROOT/c['base'],c['base_sha256']);require_hash(ROOT/c['output'],c['output_sha256']);text=(ROOT/c['base']).read_text(encoding='utf8')
            for edit in c['edits']:
                before,after=edit['before'],edit['after'];n=edit.get('occurrences',text.count(before))
                if text.count(before)!=n or n<1:raise ValueError('037 version anchor')
                text=text.replace(before,after)
            if text!=(ROOT/c['output']).read_text(encoding='utf8'):raise ValueError('037 unexplained generated difference')
    return True


def main():
    p=argparse.ArgumentParser();p.add_argument('--repro',action='store_true');a=p.parse_args();validate_version()
    from field_native_rom_product_037_v2 import require_admission
    require_admission()
    old=read('poc/output/pending500_036_v1.json');r=old['build_argument_manifest'];require_hash(ROOT/r['path'],r['sha256']);args=list(validate(read(r['path'])))
    stem='pending500_037_v2'+('_repro' if a.repro else '')
    if any((ROOT/path).exists() for path in ['poc/work/'+stem,'poc/output/'+stem+'.gba','poc/output/'+stem+'.json']):raise ValueError('Preserve prior037 output/work')
    for flag,value in [('--work','poc/work/'+stem),('--out','poc/output/'+stem+'.gba')]:
        if args.count(flag)!=1:raise ValueError('037 output coordinate')
        args[args.index(flag)+1]=value
    path=ROOT/'poc/build_arguments'/(stem+'.json');h=save(path,args)
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch_037_v2.py','--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],cwd=ROOT,check=True)


if __name__=='__main__':main()
