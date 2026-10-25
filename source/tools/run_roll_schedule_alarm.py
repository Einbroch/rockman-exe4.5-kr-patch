"""Exact-ROM normal regressions and separately quarantined alarm diagnostics."""
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_roll_schedule_alarm_v1'
PREFIX='roll-schedule-alarm-v1-'
OUTDIR='roll_schedule_alarm_v1'

def main():
    import run_roll_pet_license as routes
    previous=routes.STEM,routes.PREFIX,routes.OUTDIR,routes.SCRIPTS
    try:routes.STEM=STEM;routes.PREFIX=PREFIX;routes.OUTDIR=OUTDIR;routes.SCRIPTS=[];routes.focused()
    finally:routes.STEM,routes.PREFIX,routes.OUTDIR,routes.SCRIPTS=previous
    m=read(ROOT/f'poc/output/{STEM}.json');parent=ROOT/'poc/runtime'/(PREFIX+'roll-intro')
    def capture(script):
        # Stop at keyWait. In particular script6 must not dispatch an event
        # without a real registered schedule population.
        args=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_schedule_alarm.py'),'--alarm-script',str(script),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+f'script{script}')),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180','--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        subprocess.run(args,cwd=ROOT,check=True)
    with ThreadPoolExecutor(max_workers=3) as executor:list(executor.map(capture,[3,4,6]))

if __name__=='__main__':main()
