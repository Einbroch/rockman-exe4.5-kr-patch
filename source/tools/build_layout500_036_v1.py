"""036 primary invocation from original source; no patch-package generation."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,require_hash,sha
from cumulative_batch500 import read
from build_arguments import save,validate


def validate_version():
    from build_layout500_035_v2 import validate_version as prior
    prior();r=read('tools/specs/primary036_v1_version.json');require_hash(ROOT/r['base'],r['base_sha256'])
    text=(ROOT/r['base']).read_text(encoding='utf8')
    for e in r['edits']:
        if text.count(e['before'])!=1:raise ValueError('036 unique version anchor')
        text=text.replace(e['before'],e['after'])
    require_hash(ROOT/r['output'],r['output_sha256'])
    if text!=(ROOT/r['output']).read_text(encoding='utf8'):raise ValueError('036 unexplained primary difference')
    return sha((ROOT/'tools/specs/primary036_v1_version.json').read_bytes())


def main():
    p=argparse.ArgumentParser();p.add_argument('--repro',action='store_true');a=p.parse_args();validate_version()
    from field_npc_rom_product_036_v1 import require_admission
    require_admission()
    old=read('poc/output/pending500_035_v2.json');r=old['build_argument_manifest'];require_hash(ROOT/r['path'],r['sha256']);args=list(validate(read(r['path'])))
    stem='pending500_036_v1'+('_repro' if a.repro else '')
    if any((ROOT/path).exists() for path in ['poc/work/'+stem,'poc/output/'+stem+'.gba','poc/output/'+stem+'.json']):raise ValueError('Preserve previous036 output/work')
    for flag,value in [('--work','poc/work/'+stem),('--out','poc/output/'+stem+'.gba')]:
        if args.count(flag)!=1:raise ValueError('036 argv output coordinate')
        args[args.index(flag)+1]=value
    path=ROOT/'poc/build_arguments'/(stem+'.json');h=save(path,args)
    subprocess.run([sys.executable,'-X','utf8','tools/build_development_patch_036_v1.py','--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',h],cwd=ROOT,check=True)


if __name__=='__main__':main()
