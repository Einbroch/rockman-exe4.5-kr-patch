"""Own exact-ROM normal chain, calendar return menu and query branches."""
import json
from build_visibility_poc import ROOT,require_hash
import run_gutsman_calendar_anniversary_confirmation as base
STEM='exe45_ko_development_gutsman_calendar_navigation_v1'
PREFIX='gutsman-calendar-navigation-v1-'
OUTDIR='gutsman_calendar_navigation_v1'
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime'
    routes=[
        ('return-menu-first','anniversary-cancel','none:1:7,up:2:90'),
        ('return-menu-schedule','return-menu-first','none:1:7,a:2:90'),
        ('return-menu-anniversary','anniversary-cancel','none:1:7,a:2:90'),
        ('return-menu-cancel','anniversary-cancel','none:1:7,b:2:90'),
        ('query-date','self-yes-accept','none:1:7,down:2:90,a:2:90'),
        ('query-cancel','query-date','none:1:7,b:2:90'),
    ]
    for name,parent,actions in routes:base.base.capture(rp,m['output_sha256'],rt,name,parent,actions)
if __name__=='__main__':main()
