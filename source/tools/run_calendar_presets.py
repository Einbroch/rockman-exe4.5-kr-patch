"""Fresh own-ROM normal routes for meal/school default confirmation, commit and query."""
import sys,subprocess
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_calendar_presets_poc_v1'
PREFIX='calendar-presets-poc-v1-'

def main():
    import run_calendar_date as base
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR='calendar_presets_poc_v1';base.main()
    m=read(ROOT/f'poc/output/{STEM}.json')
    def run(name,parent,actions):
        p=ROOT/'poc/runtime'/(PREFIX+parent)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_calendar_presets.py'),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/(PREFIX+name)),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(p/'checkpoint.mss'),'--state-origin',str(p/'result.json')],check=True,cwd=ROOT)
    run('meal-register','time','none:1:7,down:2:90,none:1:10,down:2:90,a:2:90,none:1:10,a:2:90')
    run('meal-query','meal-register','none:1:7,left:2:90,l:2:180,none:1:90,a:2:180,none:1:90,a:2:180,none:1:90,a:2:90')
    run('school-register','time','none:1:7,down:2:90,none:1:10,down:2:90,none:1:10,down:2:90,a:2:90,none:1:10,a:2:90')
    run('school-query','school-register','none:1:7,left:2:90,l:2:180,none:1:90,a:2:180,none:1:90,a:2:180,none:1:90,a:2:90')

if __name__=='__main__':main()
