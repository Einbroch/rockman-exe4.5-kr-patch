"""Corrected034 sample input boundary: initial diagnostic already enters atR."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read


def main():
    rom='poc/output/pending500_034_v1.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);h=m['output_sha256']
    parent='poc/runtime/pending500-034-v1-complete';receipt=read(parent+'/result.json')
    if not receipt['complete'] or receipt['rom_sha256']!=h:raise ValueError('034 own normal parent checkpoint')
    prefix='b:2:120,r:2:240,none:1:120'
    cases=[('list-caption',prefix,'3'),('query-choice',prefix+',right:2:60,left:2:60','3,4,5'),('mission-caption',prefix+',a:2:180,none:1:120','3,4,5'),('trader-caption',prefix,'3')]
    for case,actions,captures in cases:
        subprocess.run([sys.executable,'-X','utf8','tools/capture_samples_034.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-034-v1-sample-v2-'+case,'--probe','snapshot','--actions',actions,'--timeout','240','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--display-case',case,'--capture-steps',captures],cwd=ROOT,check=True)
    print('034 corrected sample captures complete; model/pixel verification pending')


if __name__=='__main__':main()
