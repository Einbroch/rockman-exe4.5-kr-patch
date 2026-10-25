"""Own full normal chain plus anniversary-label focus, cancel, and accept routes."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_calendar_register as base

STEM='exe45_ko_development_gutsman_calendar_anniversary_v1'
PREFIX='gutsman-calendar-anniversary-v1-'
OUTDIR='gutsman_calendar_anniversary_v1'

def capture(rp,rom_sha,rt,name,parent_name,actions):
    parent=rt/(PREFIX+parent_name);out=rt/(PREFIX+name)
    if out.exists():raise ValueError('preserve calendar anniversary evidence')
    subprocess.run([
        sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_calendar_prompts.py'),
        '--rom',str(rp),'--expect-rom-sha256',rom_sha,
        '--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
        '--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240',
        '--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')
    ],check=True,cwd=ROOT)

def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text())
    require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime'
    routes=[
        ('anniversary-second','register-anniversary-accept','none:1:7,down:2:90'),
        ('anniversary-third','anniversary-second','none:1:7,down:2:90'),
        ('anniversary-cancel','register-anniversary-accept','none:1:7,b:2:90'),
        ('anniversary-self-accept','register-anniversary-accept','none:1:7,a:2:90'),
        ('anniversary-school-accept','anniversary-second','none:1:7,a:2:90'),
        ('anniversary-other-accept','anniversary-third','none:1:7,a:2:90'),
    ]
    for name,parent_name,actions in routes:capture(rp,m['output_sha256'],rt,name,parent_name,actions)

if __name__=='__main__':main()
