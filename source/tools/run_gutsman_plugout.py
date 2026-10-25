"""Fresh cumulative ROM, native save/continue, normal GutsMan R/No/B/Yes path."""
import subprocess,sys
from report_roll_pet import ROOT,read
import run_gutsman_pet as base

STEM='exe45_ko_development_gutsman_plugout_v1'
PREFIX='gutsman-plugout-v1-'
CHOICE_TOOL='capture_roll_plugout.py'

def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime'
    routes=[('jackin-prompt','select-gutsman','capture_keyitem_residency.py','none:1:60,down:2:60,a:2:120,none:1:60'),
            ('jackin','jackin-prompt','capture_keyitem_residency.py','none:1:7,a:2:180,none:1:300,a:2:180,a:2:180,none:1:300'),
            ('choices','jackin',CHOICE_TOOL,read(rt/'roll-plugout-v1-choices/result.json')['actions'])]
    for name,parent,tool,actions in routes:
        out=rt/(PREFIX+name);origin=rt/(PREFIX+parent)
        if out.exists():raise ValueError('preserve plugout runtime evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),
            '--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240',
            '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],check=True,cwd=ROOT)

if __name__=='__main__':main()
