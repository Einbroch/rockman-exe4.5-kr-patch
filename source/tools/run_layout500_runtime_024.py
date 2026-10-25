"""Own024 cold boot/mail regression and quarantined new raw page samples."""
import argparse
import subprocess
import sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_024_v1.gba')
    p.add_argument('--prefix',default='pending500-024-v1');p.add_argument('--samples-only',action='store_true');a=p.parse_args()
    rom=ROOT/a.rom;m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256']);h=sha(rom.read_bytes())
    if not a.samples_only:
        subprocess.run([sys.executable,'-X','utf8','tools/run_first_mail_regression.py','--rom',str(rom),'--prefix',a.prefix,'--expanded-startup-captures'],cwd=ROOT,check=True)
    parent=ROOT/'poc/runtime'/(a.prefix+'-complete')
    for case,pages in [('windman',2),('pet-quick',1),('new-normal',1)]:
        actions='b:2:120,r:2:240,none:1:120'+',a:2:240,none:1:120'*pages
        steps=','.join(str(i) for i in range(3,4+pages*2,2))
        out=ROOT/'poc/runtime'/(a.prefix+'-raw-'+case)
        subprocess.run([sys.executable,'-X','utf8','tools/capture_layout500_display_024.py',
            '--rom',str(rom),'--expect-rom-sha256',h,'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240',
            '--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),
            '--display-case',case,'--capture-steps',steps],cwd=ROOT,check=True)


if __name__=='__main__':main()
