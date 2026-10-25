"""Finite038 new-board1 default continuation diagnostic; state quarantined."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native038_loaded_guards import arguments

def main():
    rom='poc/output/pending500_038_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-038-normal-v1-16';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own038 normal parent required')
    cmd=[sys.executable,'-X','utf8','tools/capture_board_qualified038_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-038-board-qualified-v1','--probe','snapshot','--actions','none:1:179,a:2:118,none:1:179,a:2:118,down+right:20:60','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
