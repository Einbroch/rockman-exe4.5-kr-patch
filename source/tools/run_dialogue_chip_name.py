"""Own-ROM focused normal routes and guarded Korean name renderer diagnostic."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_dialogue_chip_name_v1'
PREFIX='dialogue-chip-name-v1-'
OUTDIR='dialogue_chip_name_v1'

def main():
    import run_roll_chipquest as routes
    previous=routes.STEM,routes.PREFIX,routes.OUTDIR
    try:routes.STEM=STEM;routes.PREFIX=PREFIX;routes.OUTDIR=OUTDIR;routes.main()
    finally:routes.STEM,routes.PREFIX,routes.OUTDIR=previous
    m=read(ROOT/f'poc/output/{STEM}.json');parent=ROOT/'poc/runtime'/(PREFIX+'roll-intro')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_dialogue_chip_name.py'),'--talk-script','13','--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+'name-script13')),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180','--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],cwd=ROOT,check=True)

if __name__=='__main__':main()
