"""Fresh current-ROM normal registration plus friend-promise name prompt."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_roll_calendar_content_v1'
PREFIX='roll-calendar-content-v1-'
OUTDIR='roll_calendar_content_v1'
def main():
    import run_roll_calendar_dialogue as base
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    m=read(ROOT/f'poc/output/{STEM}.json');parent=ROOT/'poc/runtime'/(PREFIX+'time')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_calendar_dialogue.py'),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+'promise')),'--probe','snapshot','--actions','none:1:7,down:2:90,a:2:90','--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
