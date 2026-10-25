"""Three quarantined current-ROM NPC display classes, cancel-only choices."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_036_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    audit=read('analysis/pending500_036_v1/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=m['output_sha256']:raise ValueError('036 static prerequisite')
    prefix='b:2:120,r:2:240,none:1:120'
    plans={'a0':prefix+',a:2:180,none:1:90,a:2:60',
           'a1':prefix+',a:2:180,none:1:90,a:2:180,none:1:90,right:2:90,b:2:180,none:1:90,a:2:60',
           'a3':prefix+',a:2:180,none:1:90,right:2:90,b:2:180,a:2:180,a:2:60'}
    for case,actions in plans.items():
        cmd=[sys.executable,'-X','utf8','tools/capture_npc_displays_036_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-036-v1-display-'+case,'--probe','snapshot','--actions',actions,'--state','poc/runtime/pending500-036-v1-complete/checkpoint.mss','--state-origin','poc/runtime/pending500-036-v1-complete/result.json','--display-case',case,'--timeout','240']
        subprocess.run(cmd,cwd=ROOT,check=True)
    print('036 display receipts completed; actual waits/pixels/choices require verification')

if __name__=='__main__':main()
