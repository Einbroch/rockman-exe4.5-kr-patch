"""Fresh own-ROM normal chain and isolated selected schedule literal consumers."""
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_roll_schedule_v1'
PREFIX='roll-schedule-v1-'
OUTDIR='roll_schedule_v1'

def main():
    import run_roll_pet_license as routes
    previous=routes.STEM,routes.PREFIX,routes.OUTDIR,routes.SCRIPTS
    try:routes.STEM=STEM;routes.PREFIX=PREFIX;routes.OUTDIR=OUTDIR;routes.SCRIPTS=[];routes.focused()
    finally:routes.STEM,routes.PREFIX,routes.OUTDIR,routes.SCRIPTS=previous
    m=read(ROOT/f'poc/output/{STEM}.json');parent=ROOT/'poc/runtime'/(PREFIX+'roll-intro')
    def capture(script):
        actions='none:1:7,r:2:180,none:1:180'
        # Do not enter script2's event-name path without a registered-event
        # recipe. Script1 lead-in stops at the source keyWait boundary.
        if script!=1:actions+=',a:2:180,none:1:180,a:2:180,none:1:180'
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_schedule.py'),'--schedule-script',str(script),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+f'script{script}')),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],cwd=ROOT,check=True)
    with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(capture,[1,3,10,12]))

if __name__=='__main__':main()
