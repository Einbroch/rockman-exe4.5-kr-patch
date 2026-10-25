"""Eight page-boundary diagnostics; no mission state edits or patch outputs."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash

CASES=[(25,61,1),(25,63,1),(27,34,2),(27,35,1),(27,37,1),(27,38,6),(27,42,5),(27,51,4)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--origin',required=True);p.add_argument('--before',action='store_true');a=p.parse_args()
    if not a.prefix.replace('-','').isalnum():raise ValueError('simple prefix')
    rp=ROOT/a.rom;m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256'])
    origin=ROOT/a.origin
    for index,script,literal in (CASES[1:3] if a.before else CASES):
        actions='b:2:120,down:2:90,down:2:90,down:2:90,down:2:90,a:2:180,a:2:300,a:2:180,a:2:240,a:2:180'+',a:2:180'*literal
        suffix='-setup' if index==25 else ''
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_pending500_mail.py'),'--navi-index',str(index),'--body-script',str(script),'--rom',str(rp),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/f'poc/runtime/{a.prefix}{suffix}-{index}-{script}'),'--expect-rom-sha256',m['output_sha256'],'--probe','snapshot','--actions',actions,'--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),'--capture-steps',f'9,{10+literal}','--timeout','240']
        subprocess.run(cmd,check=True,cwd=ROOT)
        print('Arrow diagnostic captured',index,script,literal,flush=True)

if __name__=='__main__':main()
