"""Own-ROM focused regressions and events page transition diagnostics."""
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read
import run_roll_pet_tournament as tournament
STEM='exe45_ko_development_roll_pet_events_v1'
PREFIX='roll-pet-events-v1-'
OUTDIR='roll_pet_events_v1'

def diagnostics(stem=STEM,prefix=PREFIX,parent=None):
    m=read(ROOT/f'poc/output/{stem}.json');origin=ROOT/'poc/runtime'/(parent or prefix+'roll-intro')
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('events own-ROM parent')
    def run(s):
        actions='none:1:7,r:2:180,none:1:180'
        args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_pet_events.py'),'--talk-script',str(s),'--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/f'{prefix}script{s}'),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        subprocess.run(args,cwd=ROOT,check=True)
    with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(run,[16,18,19,20,21,22]))

def main():
    previous=tournament.STEM,tournament.PREFIX,tournament.OUTDIR
    try:tournament.STEM=STEM;tournament.PREFIX=PREFIX;tournament.OUTDIR=OUTDIR;tournament.main()
    finally:tournament.STEM,tournament.PREFIX,tournament.OUTDIR=previous
    diagnostics(STEM,PREFIX)

if __name__=='__main__':main()
