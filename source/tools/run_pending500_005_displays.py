"""Same-ROM normal checkpoint; display only, no option confirmation/HP reward."""
import json,subprocess,sys
from build_visibility_poc import ROOT,sha

def main():
    rom=ROOT/'poc/output/exe45_ko_development_pending500_005_v1.gba';prefix='pending500-005-v1';h=sha(rom.read_bytes());rt=ROOT/'poc/runtime';origin=rt/(prefix+'-complete')
    cases={'communication':'b:2:120,r:2:240,none:1:120,down:2:90,none:1:60,up:2:90,none:1:60',
        'aqua':'b:2:120,r:2:240,none:1:120,a:2:240,none:1:60,a:2:240,none:1:60'}
    for case,actions in cases.items():
        out=rt/(prefix+'-display-'+case)
        if out.exists():raise ValueError('Preserve prior runtime')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_pending500_005_display.py'),'--display-case',case,'--rom',str(rom),
            '--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240',
            '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
