"""Fresh own-ROM cold chain and normal calendar registration, no aliases."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_roll_calendar_dialogue_v1'
PREFIX='roll-calendar-dialogue-v1-'
OUTDIR='roll_calendar_dialogue_v1'
def main():
    import run_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[];base.focused()
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    m=read(ROOT/f'poc/output/{STEM}.json');parent=PREFIX+'roll-intro'
    segments=[('calendar','none:1:7,right:2:90,none:1:90,a:2:90,a:2:90,a:2:90'),('time','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90,a:2:90'),('meal','none:1:7,down:2:90,none:1:10,down:2:90,a:2:90,a:2:90'),('list','none:1:7,left:2:90,l:2:180,none:1:90,a:2:180,none:1:90,a:2:180,none:1:90,a:2:90')]
    for name,actions in segments:
        origin=ROOT/'poc/runtime'/parent;out=ROOT/'poc/runtime'/(PREFIX+name);tool='capture_roll_schedule_native.py' if name=='list' else 'capture_roll_calendar_dialogue.py'
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],check=True,cwd=ROOT)
        parent=PREFIX+name
if __name__=='__main__':main()
