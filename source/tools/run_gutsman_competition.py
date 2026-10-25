"""Own native save/PET regression; real unregistered tournament then return."""
import sys,json,subprocess
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet
STEM='exe45_ko_development_gutsman_competition_v1'
PREFIX='gutsman-competition-v1-'
def main():
    run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman')
    for name,actions in [('tournament-prompt','none:1:60,a:2:120,none:1:60'),('unregistered','none:1:1,a:2:180,none:1:60,a:2:180,none:1:60')]:
        out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve run')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_competition.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        subprocess.run(cmd,check=True,cwd=ROOT);parent=out
if __name__=='__main__':main()
