"""Own008 normal state, display/cursor checks, no choice confirmation."""
import subprocess,sys
from build_visibility_poc import ROOT,sha
def main():
    rom=ROOT/'poc/output/exe45_ko_development_pending500_008_v1.gba';h=sha(rom.read_bytes());rt=ROOT/'poc/runtime';prefix='pending500-008-v1';origin=rt/(prefix+'-complete')
    cases={'prog':'b:2:120,r:2:240,none:1:120,a:2:240,none:1:60,a:2:240,none:1:60',
           'communication':'b:2:120,r:2:240,none:1:120,down:2:90,none:1:60,up:2:90,none:1:60'}
    for case,actions in cases.items():
        out=rt/(prefix+'-display-'+case)
        if out.exists():raise ValueError('Preserve runtime evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_cumulative500_008_display.py'),'--display-case',case,'--rom',str(rom),'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],cwd=ROOT,check=True)
if __name__=='__main__':main()
