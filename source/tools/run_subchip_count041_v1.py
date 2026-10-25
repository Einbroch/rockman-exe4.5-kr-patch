"""Same040 pre-subchip normal parent; qualified empty-count alias only, no save."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed040_loaded_guards import arguments


def main():
    rom='poc/output/pending500_040_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-040-native041-field-intro-v1';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 original normal pre-subchip parent')
    cmd=[sys.executable,'-X','utf8','tools/capture_subchip_count041_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-040-native041-subchip-count-v1','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--probe','snapshot','--actions','a:2:90,a:2:90,none:1:30,b:2:90,b:2:90,none:1:30','--capture-steps','1,2,3,4,5,6','--timeout','240']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
