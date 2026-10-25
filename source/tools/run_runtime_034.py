"""Serial own034 startup/mail regression and quarantined new-literal samples."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read


def main():
    rom='poc/output/pending500_034_v1.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);h=m['output_sha256']
    proof=read('analysis/pending500_034_v1/integration_pre_repro.json')
    if not proof['passed'] or proof['rom_sha256']!=h:raise ValueError('034 static product prerequisite')
    subprocess.run([sys.executable,'-X','utf8','tools/run_first_mail_regression.py','--rom',rom,'--prefix','pending500-034-v1','--expanded-startup-captures'],cwd=ROOT,check=True)
    prefix='b:2:120,r:2:240,none:1:120,a:2:240,none:1:120'
    cases=[('list-caption',prefix,'3,5'),('query-choice',prefix+',right:2:60,left:2:60','3,5,6,7'),('mission-caption',prefix+',a:2:180,none:1:120','3,5,6,7'),('trader-caption',prefix,'3,5')]
    for case,actions,captures in cases:
        subprocess.run([sys.executable,'-X','utf8','tools/capture_samples_034.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-034-v1-sample-'+case,'--probe','snapshot','--actions',actions,'--timeout','240','--state','poc/runtime/pending500-034-v1-complete/checkpoint.mss','--state-origin','poc/runtime/pending500-034-v1-complete/result.json','--display-case',case,'--capture-steps',captures],cwd=ROOT,check=True)
    print('034 serial capture receipts complete; pixel/model/direct visual verification still required')


if __name__=='__main__':main()
