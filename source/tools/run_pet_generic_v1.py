"""Own-ROM PET screens for a batch: normal16 -> select route -> field intro/PET -> subchip menu,
subchip count diagnostic (READ alias only, never a normal parent). The plugged-in PET menu has no
communication entry (its last item is save), so no menu walk beyond the subchip screen.

Usage: run_pet_generic_v1.py BATCH -> poc/runtime/pending500-<B>-{select-route,field-intro,subchip-menu,
subchip-count-diag}-v1. Controller input only; parents are this ROM's own checkpoints.
"""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from typed040_loaded_guards import arguments


def main():
    b=sys.argv[1];rom=f'poc/output/pending500_{b}_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);g=arguments(rom,m)
    def go(name,tool,actions,steps,par):
        out=f'poc/runtime/pending500-{b}-'+name
        cmd=[sys.executable,'-X','utf8','tools/'+tool,'--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',out,'--state',par+'/checkpoint.mss','--state-origin',par+'/result.json','--probe','snapshot','--actions',actions,'--capture-steps',','.join(map(str,range(1,steps+1))),'--timeout','240']+g
        subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.DEVNULL);print(b,name,'complete',flush=True);return out
    parent=f'poc/runtime/pending500-{b}-normal-v1-16'
    route=go('select-route-v1','run_mesen_segment.py','none:1:30,select:10:120,none:1:30,a:4:90,b:4:90',5,parent)
    pet=go('field-intro-v1','run_mesen_segment.py','none:1:600,a:2:120,a:2:120,a:2:120,a:2:120,a:2:120,a:2:120,a:2:120,none:1:120,start:4:180',10,route)
    go('subchip-menu-v1','run_mesen_segment.py','a:2:90,a:2:150,a:2:90,b:2:90,b:2:90,none:1:30',6,pet)
    go('subchip-count-diag-v1','capture_subchip_count041_v4.py','a:2:90,a:2:90,none:1:30,b:2:90,b:2:90,none:1:30',6,pet)


if __name__=='__main__':main()
