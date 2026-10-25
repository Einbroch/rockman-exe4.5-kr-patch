"""License render diagnostics remain quarantined from same-ROM normal chains."""
import argparse,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read
from run_roll_pet_talk import ACTIONS
import run_roll_pet_talk as talk
STEM='exe45_ko_development_roll_pet_license_v1'
PREFIX='roll-pet-license-v1-'
OUTDIR='roll_pet_license_v1'
SCRIPTS=[11,12,14,15]

def diagnostics(stem=STEM,prefix=PREFIX,parent=None):
    m=read(ROOT/f'poc/output/{stem}.json');parent=parent or prefix+'roll-intro';origin=ROOT/'poc/runtime'/parent
    if read(origin/'result.json')['rom_sha256']!=m['output_sha256']:raise ValueError('license own-ROM parent')
    def run(script):
        args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_pet_license.py'),'--talk-script',str(script),'--rom',str(ROOT/f'poc/output/{stem}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/f'{prefix}script{script}'),'--probe','snapshot','--actions',ACTIONS,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        subprocess.run(args,cwd=ROOT,check=True)
    with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(run,SCRIPTS))

def main():
    previous=talk.STEM,talk.PREFIX,talk.OUTDIR
    try:talk.STEM=STEM;talk.PREFIX=PREFIX;talk.OUTDIR=OUTDIR;talk.main()
    finally:talk.STEM,talk.PREFIX,talk.OUTDIR=previous
    diagnostics(STEM,PREFIX)

def focused():
    from run_roll_equipment_guides_matrix import main as roll
    import run_roll_fortune_matrix as matrix
    if roll(STEM,PREFIX+'roll-',pet_probe=True,intro_probe=True):raise ValueError('license focused cold chain')
    matrix.STEM=STEM
    matrix.segment('capture_roll_pet.py',PREFIX+'seed',PREFIX+'roll-intro','none:1:60,b:2:90,a:2:180,none:1:180')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/run_roll_pet_prompts.py'),'--stem',STEM,'--origin','poc/runtime/'+PREFIX+'seed','--out','poc/runtime/'+PREFIX+'prompts'],cwd=ROOT,check=True)
    matrix.segment('capture_roll_pet_talk.py',PREFIX+'talk',PREFIX+'roll-intro',ACTIONS)
    diagnostics(STEM,PREFIX)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--focused',action='store_true');a=ap.parse_args()
    focused() if a.focused else main()
