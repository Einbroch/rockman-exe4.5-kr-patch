"""Reproduce isolated39-page renderer/quantity diagnostic, not normal routes."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT
from capture_keyitem_rom_matrix import CASES

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--suffix',default='matrix-r3');a=ap.parse_args()
    rt=ROOT/'poc/runtime';name='keyitem-full-rom-v1-';rp=ROOT/'poc/output/exe45_ko_development_keyitem_full_rom_v1.gba';m=json.loads(rp.with_suffix('.json').read_text())
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_keyitem_rom_matrix.py'),
        '--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
        '--out',str(rt/(name+a.suffix)),'--probe','snapshot','--actions',','.join(['none:1:7,a:2:60,none:1:30,b:2:60']*len(CASES)),
        '--capture-steps',','.join(map(str,[2+4*i for i in range(len(CASES))]+[4*len(CASES)])),'--timeout','600',
        '--state',str(rt/(name+'inventory')/'checkpoint.mss'),'--state-origin',str(rt/(name+'inventory')/'result.json'),
        '--lookup-evidence',str(rt/(name+'empty'))],check=True,cwd=ROOT)
if __name__=='__main__':main()
