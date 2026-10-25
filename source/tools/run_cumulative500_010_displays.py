"""Own010 normal NumberMan state; no outcome/real Navi-selection claim."""
import json,subprocess,sys
from build_visibility_poc import ROOT,sha
def main():
    rom=ROOT/'poc/output/exe45_ko_development_pending500_010_v1.gba';h=sha(rom.read_bytes());rt=ROOT/'poc/runtime';prefix='pending500-010-v1'
    def run(case,parent,tool,actions,extra=()):
        out=rt/(prefix+'-'+case);origin=rt/(prefix+'-'+parent)
        if out.exists():raise ValueError('Preserve runtime evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),*extra],cwd=ROOT,check=True)
    complete=json.loads((rt/'native-keyboard-labels-v1-complete/result.json').read_text())['actions'].split(',')
    select=json.loads((rt/'numberman-intro-v1-select-numberman/result.json').read_text())['actions']
    intro=json.loads((rt/'numberman-intro-v1-intro/result.json').read_text())['actions']
    run('number-complete','pagecycle','run_mesen_segment.py',','.join(complete[:23])+','+select+','+intro+',b:2:120')
    for kind,script in [('new-win',1),('new-loss',2),('carry',20)]:
        run('display-'+kind,'number-complete','capture_cumulative500_010_display.py','none:1:7,r:2:180,none:1:180',('--display-kind',kind,'--alert-script',str(script)))
if __name__=='__main__':main()
