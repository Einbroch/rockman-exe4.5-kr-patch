"""Own-ROM calendar registration and native populated schedule query."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_roll_schedule_time_v1'
PREFIX='roll-schedule-time-v1-'
OUTDIR='roll_schedule_time_v1'
def main():
    import run_roll_schedule as base
    previous=base.STEM,base.PREFIX,base.OUTDIR
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    finally:base.STEM,base.PREFIX,base.OUTDIR=previous
    m=read(ROOT/f'poc/output/{STEM}.json');parent=PREFIX+'roll-intro'
    for name,actions in [('calendar','none:1:7,right:2:90,none:1:90,a:2:90,a:2:90,a:2:90'),('time','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90,a:2:90'),('meal','none:1:7,down:2:90,none:1:10,down:2:90,a:2:90,a:2:90'),('list','none:1:7,left:2:90,l:2:180,none:1:90,a:2:180,none:1:90,a:2:180,none:1:90,a:2:90')]:
        origin=ROOT/'poc/runtime'/parent;out=ROOT/'poc/runtime'/(PREFIX+name)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_schedule_native.py'),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],cwd=ROOT,check=True)
        parent=PREFIX+name
if __name__=='__main__':main()
