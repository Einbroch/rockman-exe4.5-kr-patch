"""Own cumulative normal chain and isolated calendar deletion/overwrite routes."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_calendar_navigation as base
STEM='exe45_ko_development_gutsman_calendar_management_v1'
PREFIX='gutsman-calendar-management-v1-'
OUTDIR='gutsman_calendar_management_v1'
def capture(name,parent_name,actions):
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';out=rt/(PREFIX+name);parent=rt/(PREFIX+parent_name)
    if out.exists():raise ValueError('preserve management runtime evidence')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_calendar_management.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
ROUTES=[
    ('delete-selector','self-yes-accept','none:1:7,down:2:90,none:1:7,down:2:90,a:2:90'),
    ('delete-focus-anniversary','delete-selector','none:1:7,down:2:90'),
    ('delete-list-anniversary','delete-focus-anniversary','none:1:7,a:2:90'),
    ('delete-first-page','delete-list-anniversary','none:1:7,a:2:90'),
    ('delete-confirm','delete-first-page','none:1:7,a:2:90'),
    ('delete-no-focus','delete-confirm','none:1:7,right:2:90'),
    ('delete-no-accept','delete-no-focus','none:1:7,a:2:90'),
    ('delete-b-cancel','delete-confirm','none:1:7,b:2:90'),
    ('delete-yes-accept','delete-confirm','none:1:7,a:2:90'),
    ('delete-schedule-empty','delete-selector','none:1:7,a:2:90'),
    ('overwrite-candidate','self-yes-accept','none:1:7,a:2:90,a:2:90,down:2:90,a:2:90,a:2:90'),
    ('overwrite-after-confirm','overwrite-candidate','none:1:7,a:2:90'),
    ('help-navigation','select-gutsman','none:1:7,down:2:90,none:1:7,down:2:90,none:1:7,down:2:90,none:1:7,down:2:90,none:1:7,down:2:90,none:1:7,down:2:90'),
]
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    for name,parent,actions in ROUTES:capture(name,parent,actions)
if __name__=='__main__':main()
