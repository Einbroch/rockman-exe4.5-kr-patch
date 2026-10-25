"""Own041: normal16 -> the040 communication route01..05 -> folder edit (remove one Cannon) -> B equipment warning70.

Controller recipes only, own041 parents. Checks the composed selector on the native equipment RAM path
(6E1068 native match -> clone, unselected70 must render the same as040).
"""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed041_loaded_guards import arguments

ROM='poc/output/pending500_041_v1.gba'


def main():
    m=read(ROM.replace('.gba','.json'));require_hash(ROOT/ROM,m['output_sha256']);parent=read('analysis/pending500_041_v1/normal_recipe_receipts_v1.json')['latest_checkpoint'].rsplit('/',1)[0];g=arguments(ROM,m)
    steps=[('communication-v1-%02d'%i,read('poc/runtime/pending500-040-communication-v1-%02d/result.json'%i)) for i in range(1,6)]+[('equipment-error-v1',read('poc/runtime/pending500-040-native041-equipment-error-v9/result.json'))]
    for name,old in steps:
        out='poc/runtime/pending500-041-'+name
        cmd=[sys.executable,'-X','utf8','tools/run_mesen_segment.py','--rom',ROM,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',out,'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--timeout','300']+g
        subprocess.run(cmd,cwd=ROOT,check=True);print('041',name,'complete',flush=True);parent=out


if __name__=='__main__':main()
