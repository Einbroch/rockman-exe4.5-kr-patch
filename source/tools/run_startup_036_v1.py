"""Own036 normal startup and keyboard/page/Navi controls; no old-ROM states."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read


def main():
    rom='poc/output/pending500_036_v1.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);parent=None
    boot='none:1:900,start:2:90,'+','.join(['a:2:180']*8)
    complete=read('poc/runtime/native-keyboard-labels-v1-complete/result.json')['actions'];page=read('poc/runtime/native-keyboard-labels-v1-pagecycle/result.json')['actions']
    for suffix,actions,captures in [('boot',boot,None),('pagecycle',page,None),('complete',complete,'14,15,16,17,18,19,20,21,22,23,24,34')]:
        folder='poc/runtime/pending500-036-v1-'+suffix
        cmd=[sys.executable,'-X','utf8','tools/run_mesen_segment.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--actions',actions,'--probe','snapshot','--timeout','240']
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        if captures:cmd+=['--capture-steps',captures]
        subprocess.run(cmd,cwd=ROOT,check=True);parent=folder
    print('036 own normal startup completed; visual checks/scene-specific displays still require separate evidence')


if __name__=='__main__':main()
