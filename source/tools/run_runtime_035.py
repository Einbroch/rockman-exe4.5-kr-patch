"""Own035 normal regressions then actual new NPC clone display diagnostics."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_035_v1.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);h=m['output_sha256']
    audit=read('analysis/pending500_035_v1/integration_pre_repro.json')
    if not audit['passed'] or audit['rom_sha256']!=h:raise ValueError('035 static prerequisite')
    subprocess.run([sys.executable,'-X','utf8','tools/run_first_mail_regression.py','--rom',rom,'--prefix','pending500-035-v1','--expanded-startup-captures'],cwd=ROOT,check=True)
    prefix='b:2:120,r:2:240,none:1:120';page=',a:2:180,none:1:90'
    for case,n in [('plaza',4),('portraits',4),('weekend',2)]:
        subprocess.run([sys.executable,'-X','utf8','tools/capture_npc_displays_035_v2.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-035-v1-npc-display-'+case,'--probe','snapshot','--actions',prefix+page*(n-1),'--capture-steps',','.join(str(3+2*i) for i in range(n)),'--state','poc/runtime/pending500-035-v1-complete/checkpoint.mss','--state-origin','poc/runtime/pending500-035-v1-complete/result.json','--display-case',case,'--timeout','240'],cwd=ROOT,check=True)
    print('035 own normal + new NPC glyph sample receipts completed; checkers/direct review pending')

if __name__=='__main__':main()
