"""From each ROM's OWN coldboot final checkpoint (Internet1 next to the green Navi), press A to talk.

Usage: run_npc_talk_generic_v1.py BATCH [BATCH...]  -> poc/runtime/pending500-<B>-npc-talk-v1
Controller input only, own-ROM parents only; captures are compared by eye across batches.
"""
import sys,subprocess
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed040_loaded_guards import arguments

ACTIONS='a:2:150,a:2:150,a:2:150,a:2:150,a:2:150,b:2:90'


def main():
    for b in sys.argv[1:]:
        rom=f'poc/output/pending500_{b}_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
        parent=f'poc/runtime/pending500-{b}-normal-v1-16';out=f'poc/runtime/pending500-{b}-npc-talk-v1'
        cmd=[sys.executable,'-X','utf8','tools/run_mesen_segment.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',out,'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--probe','snapshot','--actions',ACTIONS,'--capture-steps','1,2,3,4,5,6','--timeout','240']+arguments(rom,m)
        subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.DEVNULL);print('NPC talk',b,'captured',flush=True)


if __name__=='__main__':main()
