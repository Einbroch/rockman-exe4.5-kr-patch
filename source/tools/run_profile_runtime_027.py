"""Own027 coldboot route then two quarantined max native-profile pages."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read


def main():
    p=argparse.ArgumentParser();p.add_argument('--samples-only',action='store_true');a=p.parse_args()
    rom=ROOT/'poc/output/pending500_027_v1.gba';m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256']);h=sha(rom.read_bytes())
    proof=read('analysis/pending500_027_v1/integration_pre_repro.json')
    if not proof['passed'] or proof['rom_sha256']!=h:raise ValueError('027 independent product prerequisite')
    if not a.samples_only:
        subprocess.run([sys.executable,'-X','utf8','tools/run_first_mail_regression.py','--rom',str(rom),'--prefix','pending500-027-v1','--expanded-startup-captures'],cwd=ROOT,check=True)
    parent=ROOT/'poc/runtime/pending500-027-v1-complete';prefix='b:2:120,r:2:240,none:1:120'
    for case,actions,captures in [
        ('school-max',prefix+',a:2:240,none:1:120,a:2:180,none:1:120','3,5,7'),
        ('subject-max',prefix+',a:2:180,none:1:120','3,5'),
    ]:
        subprocess.run([sys.executable,'-X','utf8','tools/capture_profile_display_027.py','--rom',str(rom),'--expect-rom-sha256',h,'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/('pending500-027-v1-raw-'+case)),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),'--display-case',case,'--capture-steps',captures],cwd=ROOT,check=True)


if __name__=='__main__':main()
