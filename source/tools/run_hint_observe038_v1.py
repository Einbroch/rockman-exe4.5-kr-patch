"""Read-only original L hint route from exact038 own normal state."""
import subprocess, sys
from build_visibility_poc import ROOT, require_hash
from cumulative_batch500 import read
from native038_loaded_guards import arguments

def main():
    rom='poc/output/pending500_038_v2.gba'
    m=read(rom.replace('.gba','.json'))
    require_hash(ROOT/rom,m['output_sha256'])
    audit=read('analysis/pending500_038_v2/integration.json')
    normal=read('analysis/pending500_038_v2/normal_path_v1.json')
    if not audit['passed'] or not audit['independent_rebuild_byte_identical'] or audit['rom_sha256']!=m['output_sha256'] or not normal['passed'] or normal['rom_sha256']!=m['output_sha256']:
        raise ValueError('Actual038 integration and own normal route required')
    parent='poc/runtime/pending500-038-normal-v1-16'
    r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:
        raise ValueError('Own038 normal state required')
    cmd=[sys.executable,'-X','utf8','tools/capture_hint_observe038_v1.py',
         '--rom',rom,'--expect-rom-sha256',m['output_sha256'],
         '--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe',
         '--out','poc/runtime/pending500-038-hint-controls-observe-v1',
         '--probe','snapshot','--actions','none:1:179,l:2:180,a:2:180,down+right:10:30',
         '--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json',
         '--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)

if __name__=='__main__':main()
