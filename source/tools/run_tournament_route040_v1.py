"""Own039 PET: cancel communication prompt and choose first tournament item."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from communication039_loaded_guards import arguments


def main():
    rom='poc/output/pending500_039_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent='poc/runtime/pending500-039-communication-v1-06';r=read(parent+'/result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('Own039 normal PET prerequisite')
    actions=','.join(['b:2:90']+['up:2:30']*5+['a:2:180','none:1:120','a:2:180','none:1:120'])
    cmd=[sys.executable,'-X','utf8','tools/capture_tournament_route040_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/pending500-039-tournament-route040-v1','--probe','snapshot','--actions',actions,'--capture-steps','1,6,7,8,9,10','--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','180']+arguments(rom,m)
    subprocess.run(cmd,cwd=ROOT,check=True)


if __name__=='__main__':main()
