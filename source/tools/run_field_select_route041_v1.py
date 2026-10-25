"""Disambiguate field input transmission before assuming an unavailable UI route."""
import sys,subprocess
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed040_loaded_guards import arguments


def main():
    rom='poc/output/pending500_040_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-040-normal-v1-16';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 exact040 normal field input parent')
    actions='none:1:30,select:10:120,none:1:30,a:4:90,b:4:90'
    cmd=[sys.executable,'-X','utf8','tools/capture_native_inputs041_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-040-native041-select-route-v1','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--probe','snapshot','--actions',actions,'--capture-steps','1,2,3,4,5','--timeout','240']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()


