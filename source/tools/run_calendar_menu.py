"""Own-ROM normal calendar menu and existing registered-meal query regression."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_calendar_menu_v1'
PREFIX='calendar-menu-v1-'
OUTDIR='calendar_menu_v1'
def main():
    import run_roll_pet_license as base
    previous=base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS
    try:base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.SCRIPTS=[];base.focused()
    finally:base.STEM,base.PREFIX,base.OUTDIR,base.SCRIPTS=previous
    m=read(ROOT/f'poc/output/{STEM}.json');parent=PREFIX+'roll-intro'
    segments=[('calendar','capture_fixedcell_probe.py','none:1:7,right:2:90,none:1:90,a:2:90,a:2:90,a:2:90'),('time','capture_roll_schedule_native.py','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90,a:2:90'),('meal','capture_roll_schedule_native.py','none:1:7,down:2:90,none:1:10,down:2:90,a:2:90,a:2:90'),('list','capture_roll_schedule_native.py','none:1:7,left:2:90,l:2:180,none:1:90,a:2:180,none:1:90,a:2:180,none:1:90,a:2:90')]
    for name,tool,actions in segments:
        origin=ROOT/'poc/runtime'/parent;out=ROOT/'poc/runtime'/(PREFIX+name)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],check=True,cwd=ROOT)
        parent=PREFIX+name
if __name__=='__main__':main()
