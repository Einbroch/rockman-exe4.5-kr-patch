"""Exact-ROM normal NumberMan ancestry and middle-dot font diagnostic."""
import subprocess,sys
import run_pending500_006_number as number
from build_visibility_poc import ROOT,sha

def main():
    number.STEM='exe45_ko_development_middle_dot_v1';number.PREFIX='middle-dot-v1';number.main()
    rom=ROOT/f'poc/output/{number.STEM}.gba';origin=ROOT/'poc/runtime/middle-dot-v1-number-complete';out=ROOT/'poc/runtime/middle-dot-v1-glyph'
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_middle_dot.py'),'--rom',str(rom),'--expect-rom-sha256',sha(rom.read_bytes()),
        '--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot',
        '--actions','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180','--timeout','240','--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')],cwd=ROOT,check=True)

if __name__=='__main__':main()
