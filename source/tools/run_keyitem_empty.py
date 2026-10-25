"""Own cold/save/continue and normal empty-item exit/reentry route."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet as base

STEM='exe45_ko_development_keyitem_empty_v1'
PREFIX='keyitem-empty-v1-'
CAPTURE_TOOL='capture_keyitem_empty.py'
ROUTES=[
    ('inventory','select-gutsman','none:1:7,left:2:90'),
    ('empty','inventory','none:1:7,a:2:90'),
    ('empty-hold','empty','none:1:180'),
    ('empty-close','empty-hold','none:1:7,b:2:90'),
    ('empty-reenter','empty-close','none:1:7,a:2:90'),
]
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    rt=ROOT/'poc/runtime'
    for name,parent,actions in ROUTES:
        out=rt/(PREFIX+name);prior=rt/(PREFIX+parent)
        if out.exists():raise ValueError('preserve keyitem runtime evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/CAPTURE_TOOL),
            '--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],
            '--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),
            '--probe','snapshot','--actions',actions,'--timeout','240',
            '--state',str(prior/'checkpoint.mss'),'--state-origin',str(prior/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
