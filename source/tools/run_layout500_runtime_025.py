"""Own025 normal startup then finite choice/nickname diagnostic runs."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

def main():
    p=argparse.ArgumentParser();p.add_argument('--samples-only',action='store_true');a=p.parse_args()
    rom=ROOT/'poc/output/pending500_025_v2.gba';m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256']);h=sha(rom.read_bytes())
    proof=read('analysis/pending500_025_v2/integration_pre_repro.json')
    if not proof['passed'] or proof['rom_sha256']!=h:raise ValueError('025 independent product prerequisite')
    if not a.samples_only:
        subprocess.run([sys.executable,'-X','utf8','tools/run_first_mail_regression.py','--rom',str(rom),'--prefix','pending500-025-v2','--expanded-startup-captures'],cwd=ROOT,check=True)
    parent=ROOT/'poc/runtime/pending500-025-v2-complete'
    prefix='b:2:120,r:2:240,none:1:120'
    cases=[('choice-confirm','choice-three-row',prefix+',right:2:60,left:2:60,down:2:60,up:2:60,right:2:60,a:2:180,none:1:120','3,4,5,6,7,8,9,10'),
           ('choice-cancel','choice-three-row',prefix+',right:2:60,b:2:180,none:1:120','3,4,5,6'),
           ('nickname','nickname',prefix+',a:2:240,none:1:120,a:2:240,none:1:120','3,5,7')]
    for name,case,actions,captures in cases:
        out=ROOT/'poc/runtime'/('pending500-025-v2-raw-'+name)
        subprocess.run([sys.executable,'-X','utf8','tools/capture_layout500_display_025.py','--rom',str(rom),'--expect-rom-sha256',h,
            '--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot',
            '--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),
            '--display-case',case,'--capture-steps',captures],cwd=ROOT,check=True)

if __name__=='__main__':main()
