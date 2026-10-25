"""Fresh normal PET/save chain, then three separately quarantined result pages."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet
STEM='exe45_ko_development_gutsman_battle_results_v1'
PREFIX='gutsman-battle-results-v1-'
OUTDIR='gutsman_battle_results_v1'
def main():
    run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman')
    for script in [1,2,3]:
        out=rt/(PREFIX+f'script{script}')
        if out.exists():raise ValueError('preserve evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_battle_results.py'),'--battle-script',str(script),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180','--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
