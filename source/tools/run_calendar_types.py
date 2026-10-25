"""Fresh own-ROM routes and normal five-choice scroll observations."""
import subprocess,sys
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_calendar_types_v1'
PREFIX='calendar-types-v1-'
OUTDIR='calendar_types_v1'
def main():
    import run_roll_calendar_content as base
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    m=read(ROOT/f'poc/output/{STEM}.json');p=ROOT/'poc/runtime'/(PREFIX+'time')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_fixedcell_probe.py'),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+'types-scroll')),'--probe','snapshot','--actions','none:1:7,down:2:90,none:1:10,down:2:90,none:1:10,down:2:90,none:1:10,down:2:90','--timeout','240','--state',str(p/'checkpoint.mss'),'--state-origin',str(p/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
