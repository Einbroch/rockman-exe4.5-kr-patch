"""Own normal save/PET/alarm regressions followed by native calendar time/type."""
import sys,json,subprocess
from build_visibility_poc import ROOT,require_hash
import run_gutsman_alarm_meal as base
STEM='exe45_ko_development_gutsman_calendar_prompts_v1'
PREFIX='gutsman-calendar-prompts-v1-'
OUTDIR='gutsman_calendar_prompts_v1'
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman')
    for name,actions in [('calendar','none:1:7,right:2:90,none:1:90,a:2:90,a:2:90,a:2:90'),('time','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90,a:2:90')]:
        out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve calendar evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_calendar_prompts.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT);parent=out
if __name__=='__main__':main()
