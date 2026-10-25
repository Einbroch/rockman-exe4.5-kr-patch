"""Same-ROM, normal-button GutsMan selection then equipment guide observation."""
import json,subprocess,sys
from build_visibility_poc import ROOT,sha

def main():
    stem='exe45_ko_development_pending500_003_v2';prefix='pending500-003-v2'
    rom=ROOT/f'poc/output/{stem}.gba';h=sha(rom.read_bytes());runtime=ROOT/'poc/runtime'
    complete=json.loads((runtime/'native-keyboard-labels-v1-complete/result.json').read_text())['actions'].split(',')
    routes=[('guts-complete',prefix+'-pagecycle','run_mesen_segment.py',','.join(complete[:23]+['right:2:90','right:2:90']+complete[23:]),list(range(23,37))),
        ('guts-equipment',prefix+'-guts-complete','capture_equipment_guides.py',json.loads((runtime/'equipment-labels-v2-equipment/result.json').read_text())['actions'],list(range(1,16)))]
    for name,parent,tool,actions,captures in routes:
        folder=runtime/(prefix+'-'+name);origin=runtime/parent
        if folder.exists():raise ValueError('Preserve previous runtime')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--mesen',str(runtime/'isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(folder),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240',
            '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),'--capture-steps',','.join(map(str,captures))]
        subprocess.run(cmd,cwd=ROOT,check=True)
        print('Verified GutsMan segment receipt:',name,flush=True)

if __name__=='__main__':main()
