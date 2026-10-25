"""Own-ROM native keyboard, common confirmation and Yes/No/B/edit branches."""
import subprocess,sys
import run_gutsman_profile as normal
from report_roll_pet import ROOT,read
STEM='exe45_ko_development_input_confirmation_v1'
PREFIX='input-confirmation-v1-'
def main():
    normal.STEM=STEM;normal.PREFIX=PREFIX;normal.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime'
    def run(name,parent,actions,tool='capture_input_confirmation.py'):
        out=rt/(PREFIX+name);origin=rt/(PREFIX+parent)
        if out.exists():raise ValueError('preserve input evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],check=True,cwd=ROOT)
    run('typed','weak','none:1:30,a:2:60,none:1:30,start:2:90,none:1:30')
    run('confirmation','typed','a:2:120,none:1:30')
    run('yes','confirmation','a:2:180,none:1:60')
    run('no-settled','confirmation','none:1:7,right:2:60,a:2:120,none:1:30')
    run('cancel','confirmation','b:2:120,none:1:30')
    run('reconfirm-after-no-settled','no-settled','none:1:7,a:2:120,none:1:30')
    run('regression-choices','jackin',read(rt/(PREFIX+'choices')/'result.json')['actions'],'capture_roll_plugout.py')
if __name__=='__main__':main()
