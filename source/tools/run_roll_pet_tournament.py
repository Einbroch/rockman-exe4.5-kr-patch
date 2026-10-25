"""Own-ROM focused regressions and tournament page transition diagnostics."""
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read
import run_roll_pet_keyquest as keyquest
STEM='exe45_ko_development_roll_pet_tournament_v1'
PREFIX='roll-pet-tournament-v1-'
OUTDIR='roll_pet_tournament_v1'

def diagnostics(stem=STEM,prefix=PREFIX,parent=None):
    m=read(ROOT/f'poc/output/{stem}.json');origin=ROOT/'poc/runtime'/(parent or prefix+'roll-intro')
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('tournament own-ROM parent')
    def run(s):
        actions='none:1:7,r:2:180,none:1:180'+(',a:2:180,none:1:180' if s==34 else '')
        args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_pet_tournament.py'),'--talk-script',str(s),'--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/f'{prefix}script{s}'),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        subprocess.run(args,cwd=ROOT,check=True)
    with ThreadPoolExecutor(max_workers=2) as executor:list(executor.map(run,[30,34]))

def main():
    previous=keyquest.STEM,keyquest.PREFIX,keyquest.OUTDIR
    try:keyquest.STEM=STEM;keyquest.PREFIX=PREFIX;keyquest.OUTDIR=OUTDIR;keyquest.main()
    finally:keyquest.STEM,keyquest.PREFIX,keyquest.OUTDIR=previous
    diagnostics(STEM,PREFIX)

if __name__=='__main__':main()
