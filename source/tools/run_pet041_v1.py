"""Own041: normal16 -> select route -> field intro/PET -> subchip menu, then diagnostic subchip use message.

Same controller recipes as the040 route; parents are only own041 checkpoints.
The final count-alias segment is DIAGNOSTIC (read aliases), never a normal parent.
"""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed041_loaded_guards import arguments

ROM='poc/output/pending500_041_v1.gba'
SEGMENTS=[('select-route-v1','run_mesen_segment.py','none:1:30,select:10:120,none:1:30,a:4:90,b:4:90',5),
          ('field-intro-v1','run_mesen_segment.py','none:1:600,a:2:120,a:2:120,a:2:120,a:2:120,a:2:120,a:2:120,a:2:120,none:1:120,start:4:180',10),
          ('subchip-menu-v1','run_mesen_segment.py','a:2:90,a:2:150,a:2:90,b:2:90,b:2:90,none:1:30',6)]


def main():
    m=read(ROM.replace('.gba','.json'));require_hash(ROOT/ROM,m['output_sha256']);parent=read('analysis/pending500_041_v1/normal_recipe_receipts_v1.json')['latest_checkpoint'].rsplit('/',1)[0];g=arguments(ROM,m)
    def go(name,tool,actions,steps,par):
        out='poc/runtime/pending500-041-'+name
        cmd=[sys.executable,'-X','utf8','tools/'+tool,'--rom',ROM,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',out,'--state',par+'/checkpoint.mss','--state-origin',par+'/result.json','--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,range(1,steps+1))),'--timeout','240']+g
        subprocess.run(cmd,cwd=ROOT,check=True);print('041',name,'complete',flush=True);return out
    for name,tool,actions,steps in SEGMENTS:
        out=go(name,tool,actions,steps,parent)
        if name=='field-intro-v1':pet=out
        parent=out
    go('subchip-count-diag-v1','capture_subchip_count041_v4.py','a:2:90,a:2:90,none:1:30,b:2:90,b:2:90,none:1:30',6,pet)


if __name__=='__main__':main()
