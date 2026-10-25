"""New-ROM normal NumberMan selection, then two quarantined two-page displays."""
import json,subprocess,sys
from build_visibility_poc import ROOT,sha
STEM='exe45_ko_development_pending500_006_v1'
PREFIX='pending500-006-v1'

def main():
    prefix=PREFIX;rom=ROOT/f'poc/output/{STEM}.gba';h=sha(rom.read_bytes());rt=ROOT/'poc/runtime'
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
    for case in ('return','draw'):
        run('number-'+case,'number-complete','capture_pending500_006_number.py',
            'none:1:7,r:2:180,none:1:180,a:2:180,none:1:180',('--number-case',case))

if __name__=='__main__':main()
