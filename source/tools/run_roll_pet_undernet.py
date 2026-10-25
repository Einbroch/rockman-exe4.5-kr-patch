"""Own-ROM focused regressions and two-page undernet renderer diagnostic."""
import subprocess,sys
from report_roll_pet import ROOT,read
import run_roll_pet_mail as mail
STEM='exe45_ko_development_roll_pet_undernet_v1'
PREFIX='roll-pet-undernet-v1-'
OUTDIR='roll_pet_undernet_v1'

def diagnostics(stem=STEM,prefix=PREFIX,parent=None):
    m=read(ROOT/f'poc/output/{stem}.json');origin=ROOT/'poc/runtime'/(parent or prefix+'roll-intro')
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('undernet own-ROM parent')
    args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_pet_undernet.py'),'--talk-script','27','--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/f'{prefix}script27'),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180','--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
    subprocess.run(args,cwd=ROOT,check=True)

def main():
    previous=mail.STEM,mail.PREFIX,mail.OUTDIR
    try:mail.STEM=STEM;mail.PREFIX=PREFIX;mail.OUTDIR=OUTDIR;mail.main()
    finally:mail.STEM,mail.PREFIX,mail.OUTDIR=previous
    diagnostics(STEM,PREFIX)

if __name__=='__main__':main()
