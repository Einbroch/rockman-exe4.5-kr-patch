"""Learn normal hint controls on existing own037, never transfer its state038."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native037_loaded_guards import arguments

rom='poc/output/pending500_037_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-037-normal-v1-16';origin=read(parent+'/result.json')
if not origin['complete'] or origin['rom_sha256']!=m['output_sha256'] or origin.get('normal_play_checkpoint_eligible') is False:raise ValueError('037 normal source-control baseline')
cmd=[sys.executable,'-X','utf8','tools/capture_hint_observe037_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-037-hint-controls-observe-v1','--probe','snapshot','--actions','l:2:180,a:2:180,r:2:90,b:2:90','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
subprocess.run(cmd,cwd=ROOT,check=True)
