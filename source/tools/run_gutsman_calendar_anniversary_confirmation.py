"""Own normal chain and birthday/school confirmation choice/commit/query routes."""
import json
from build_visibility_poc import ROOT,require_hash
import run_gutsman_calendar_anniversary as base
STEM='exe45_ko_development_gutsman_calendar_anniversary_confirmation_v1'
PREFIX='gutsman-calendar-anniversary-confirmation-v1-'
OUTDIR='gutsman_calendar_anniversary_confirmation_v1'
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime'
    routes=[]
    for kind in ['self','school']:
        parent='anniversary-'+kind+'-accept'
        routes += [
            (kind+'-no-focus',parent,'none:1:7,right:2:90'),
            (kind+'-no-accept',kind+'-no-focus','none:1:7,a:2:90'),
            (kind+'-b-cancel',parent,'none:1:7,b:2:90'),
            (kind+'-yes-accept',parent,'none:1:7,a:2:90'),
            (kind+'-query',kind+'-yes-accept','none:1:7,down:2:90,a:2:90,a:2:90'),
        ]
    for name,parent,actions in routes:base.capture(rp,m['output_sha256'],rt,name,parent,actions)
if __name__=='__main__':main()
