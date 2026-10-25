"""Qualified039 BBS: dismiss source new-post notification, select first post."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from communication039_loaded_guards import arguments


def main():
    rom='poc/output/pending500_039_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-039-normal-v1-16';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own039 normal field parent')
    actions=','.join(['none:1:179','a:2:118','none:1:120','a:2:118']+['up:2:30']*9+['a:2:180','none:1:60','a:2:90','none:1:60','b:2:120'])
    cmd=[sys.executable,'-X','utf8','tools/capture_bbs_boundary040_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-039-bbs-boundary040-v2','--probe','snapshot','--actions',actions,'--capture-steps','3,4,13,14,15,16,17,18','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
