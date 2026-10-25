"""Five changed body routes, own native setup; quarantined same-ROM states."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash

CASES=[(26,41,[9,10,11,12]),(26,49,[9,10,11,12,13]),(26,55,[9,10,11,12,13,14]),
       (28,36,[9,10,11,12,13]),(24,33,[9,10,11,12])]


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--origin',required=True);a=p.parse_args()
    rp=ROOT/a.rom;meta=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,meta['output_sha256'])
    origin=ROOT/a.origin
    for index,script,steps in CASES:
        folder=ROOT/f'poc/runtime/{a.prefix}-{index}-{script}'
        actions='b:2:120,down:2:90,down:2:90,down:2:90,down:2:90,a:2:180,a:2:300,a:2:180,a:2:240,a:2:180'+',a:2:180'*(max(steps)-10)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_pending500_mail.py'),
            '--navi-index',str(index),'--body-script',str(script),'--rom',str(rp),
            '--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(folder),
            '--expect-rom-sha256',meta['output_sha256'],'--probe','snapshot','--actions',actions,
            '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),
            '--capture-steps',','.join(map(str,steps)),'--timeout','240'],check=True,cwd=ROOT)
        print('New500 diagnostic captured',index,script,flush=True)


if __name__=='__main__':main()
