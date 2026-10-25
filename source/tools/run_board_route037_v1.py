"""Own037 normal route segment with source-bound loaded-memory sentinels."""
import argparse,sys,subprocess
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from native037_loaded_guards import arguments


def main():
    p=argparse.ArgumentParser();p.add_argument('--parent',required=True);p.add_argument('--out',required=True);p.add_argument('--actions',required=True);a=p.parse_args()
    rom='poc/output/pending500_037_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);r=read(a.parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('037 normal parent required')
    cmd=[sys.executable,'-X','utf8','tools/capture_board037_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',a.out,'--probe','snapshot','--actions',a.actions,'--state',a.parent+'/checkpoint.mss','--state-origin',a.parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
