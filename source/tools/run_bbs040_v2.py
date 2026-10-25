"""Qualified040 BBS0 post9 ten pages -> automatic list -> A reentry."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed040_loaded_guards import arguments


def main():
    rom='poc/output/pending500_040_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-040-normal-v1-16';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('040 own normal field prerequisite')
    actions=','.join(['none:1:179','a:2:118','none:1:120','a:2:118']+['up:2:30']*9+['a:2:180','none:1:60']+['a:2:180']*10+['a:2:180','none:1:60'])
    steps=list(range(13,28));cmd=[sys.executable,'-X','utf8','tools/capture_bbs040_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-040-bbs-v2','--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,steps)),'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
