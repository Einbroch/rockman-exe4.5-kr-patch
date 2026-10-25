"""Fresh product native input route plus mono header and edit/confirmation QA."""
import subprocess,sys
import run_gutsman_profile as normal
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_input_heading_v1'
PREFIX='input-heading-v1-'

def main():
    normal.STEM=STEM;normal.PREFIX=PREFIX;normal.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime'
    def run(name,parent,actions,tool):
        out=rt/(PREFIX+name);origin=rt/(PREFIX+parent)
        if out.exists():raise ValueError('preserve evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],check=True,cwd=ROOT)
    run('header','choices','none:1:30,a:2:180,a:2:180,none:1:120','capture_fixedcell_probe.py')
    run('typed','header','none:1:7,a:2:60,none:1:7,b:2:60,none:1:7,a:2:60,start:2:90,none:1:7','capture_input_confirmation.py')
    run('confirmation','typed','a:2:120,none:1:30','capture_input_confirmation.py')
    run('no','confirmation','none:1:7,right:2:60,a:2:120,none:1:30','capture_input_confirmation.py')
    run('yes','confirmation','none:1:7,a:2:180,none:1:60','capture_input_confirmation.py')
if __name__=='__main__':main()
