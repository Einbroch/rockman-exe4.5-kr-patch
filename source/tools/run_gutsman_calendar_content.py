"""Own full normal chain and actual TV-content / friend-person menu questions."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_calendar_prompts as base
STEM='exe45_ko_development_gutsman_calendar_content_v1'
PREFIX='gutsman-calendar-content-v1-'
OUTDIR='gutsman_calendar_content_v1'
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime'
    for name,parent_name,actions in [('time-stable','calendar','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90,a:2:180'),('person-stable','time-stable','none:1:7,down:4:90'),('person-input','person-stable','none:1:7,a:2:90')]:
        parent=rt/(PREFIX+parent_name);out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve calendar content evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_calendar_prompts.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
