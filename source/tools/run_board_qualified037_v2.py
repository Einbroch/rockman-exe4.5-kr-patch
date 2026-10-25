"""037 original-event diagnostic; no ROM/RAM write, state quarantined."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native037_loaded_guards import arguments

def main():
    rom='poc/output/pending500_037_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    parent='poc/runtime/pending500-037-board-stair-route-v1';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own037 normal parent')
    cmd=[sys.executable,'-X','utf8','tools/capture_board_qualified037_v2.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-037-board-qualified-v2','--probe','snapshot','--actions','none:1:179,a:2:118,none:1:179,a:2:118,down+right:20:60','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
