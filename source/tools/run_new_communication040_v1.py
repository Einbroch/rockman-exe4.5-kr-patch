"""Own040 qualified new communication6F8D00 help16 and Bcancel; no foreign state."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed040_loaded_guards import arguments


def main():
    rom='poc/output/pending500_040_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-040-communication-v1-06';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own040 normal PET prerequisite')
    actions='a:2:180,none:1:120,down:2:90,up:2:90,b:2:180,none:1:60';cmd=[sys.executable,'-X','utf8','tools/capture_new_communication040_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-040-new-communication-v1','--probe','snapshot','--actions',actions,'--capture-steps','1,2,3,4,5,6','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
