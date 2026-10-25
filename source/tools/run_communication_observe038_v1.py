"""Normal jackout -> PET communication menu, stop before connection choices."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native038_loaded_guards import arguments

def main():
    rom='poc/output/pending500_038_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-038-normal-v1-16';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own038 normal state')
    actions='r:2:120,a:2:180,none:1:60,down:2:30,down:2:30,down:2:30,down:2:30,a:2:180,none:1:120'
    cmd=[sys.executable,'-X','utf8','tools/capture_communication038_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-038-communication-observe-v1','--probe','snapshot','--actions',actions,'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
