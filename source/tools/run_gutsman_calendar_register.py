"""Own full normal chain plus registration-type focus, cancel, and accept branches."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_calendar_home as base
STEM='exe45_ko_development_gutsman_calendar_register_v1'
PREFIX='gutsman-calendar-register-v1-'
OUTDIR='gutsman_calendar_register_v1'
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime'
    routes=[
        ('register-menu','select-gutsman','none:1:7,right:2:90,none:1:90,a:2:90,a:2:90'),
        ('register-menu-second','register-menu','none:1:7,down:2:90'),
        ('register-menu-cancel','register-menu','none:1:7,b:2:90'),
        ('register-schedule-accept','register-menu','none:1:7,a:2:90'),
        ('register-anniversary-accept','register-menu-second','none:1:7,a:2:90'),
    ]
    for name,parent_name,actions in routes:
        parent=rt/(PREFIX+parent_name);out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve calendar register evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_calendar_prompts.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
