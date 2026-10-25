"""Own native GutsMan/PET regression followed by normal plug-in attempt."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet

STEM='exe45_ko_development_gutsman_operations_v1'
PREFIX='gutsman-operations-v1-'

def main():
    run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman')
    # Release the preceding selection input before moving the menu cursor.
    # Keep the initial rejected tournament attempt in its original folders.
    for name,actions in [('jackin-prompt-r2','none:1:60,down:2:60,a:2:120,none:1:60'),('transmission-r2','none:1:1,a:1:0,'+','.join(['none:1:0']*100)+',none:1:240')]:
        out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve run')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_operations.py'),'--operation-archive','6664D0','--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        subprocess.run(cmd,check=True,cwd=ROOT);parent=out

if __name__=='__main__':main()
