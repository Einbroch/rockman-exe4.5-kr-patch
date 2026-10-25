"""Exact-ROM normal NumberMan selection then two quarantined alert display routes."""
import json,subprocess,sys
from build_visibility_poc import ROOT,sha

def main():
    prefix='pending500-004-v1';rom=ROOT/'poc/output/exe45_ko_development_pending500_004_v1.gba';h=sha(rom.read_bytes());rt=ROOT/'poc/runtime'
    def run(name,parent,tool,actions,extra=()):
        out=rt/(prefix+'-'+name);origin=rt/(prefix+'-'+parent)
        if out.exists():raise ValueError('Preserve previous runtime')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240',
            '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),*extra]
        subprocess.run(cmd,cwd=ROOT,check=True)
    complete=json.loads((rt/'native-keyboard-labels-v1-complete/result.json').read_text())['actions'].split(',')
    select=json.loads((rt/'numberman-intro-v1-select-numberman/result.json').read_text())['actions']
    intro=json.loads((rt/'numberman-intro-v1-intro/result.json').read_text())['actions']
    run('number-complete','pagecycle','run_mesen_segment.py',','.join(complete[:23])+','+select+','+intro+',b:2:120')
    for script in (1,2):
        run('number-alert'+str(script),'number-complete','capture_pending500_004_alert.py',
            'none:1:7,r:2:180,none:1:180,a:2:180,none:1:180,a:2:180,none:1:180,a:2:180,none:1:180',('--alert-script',str(script)))

if __name__=='__main__':main()
