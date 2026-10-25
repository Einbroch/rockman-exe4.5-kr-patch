"""New-ROM native save/continue and normal GutsMan profile question route."""
import subprocess,sys
import run_gutsman_plugout as base
from report_roll_pet import ROOT,read

STEM='exe45_ko_development_gutsman_profile_v1'
PREFIX='gutsman-profile-v1-'

def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.CHOICE_TOOL='capture_gutsman_profile.py';base.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime';origin=rt/(PREFIX+'choices');out=rt/(PREFIX+'weak')
    if out.exists():raise ValueError('preserve profile runtime evidence')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_profile.py'),
        '--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],
        '--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),
        '--probe','snapshot','--actions','none:1:30,a:2:180,a:2:180,none:1:120','--timeout','240',
        '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],check=True,cwd=ROOT)

if __name__=='__main__':main()
