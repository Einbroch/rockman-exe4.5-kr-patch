"""Fresh cumulative normal chains plus same-ROM calendar date intro."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_calendar_date_v1'
PREFIX='calendar-date-v1-'
OUTDIR='calendar_date_v1'
def main():
    import run_calendar_types as base
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    m=read(ROOT/f'poc/output/{STEM}.json');p=ROOT/'poc/runtime'/(PREFIX+'roll-intro')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_calendar_date.py'),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+'date-font2')),'--probe','snapshot','--actions','none:1:7,right:2:90,none:1:90','--timeout','240','--state',str(p/'checkpoint.mss'),'--state-origin',str(p/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
