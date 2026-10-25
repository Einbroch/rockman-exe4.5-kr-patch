"""Own cold/native continue; genuine GutsMan and all seven cancelled prompts."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

STEM='exe45_ko_development_gutsman_pet_v1'
PREFIX='gutsman-pet-v1-'

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/run_numberman_seasonal_normal.py'),'--stem',STEM,'--prefix',PREFIX],check=True,cwd=ROOT)
    rt=ROOT/'poc/runtime';base=rt/(PREFIX+'normal-reload-select');parent=base
    selection='none:1:60,left:2:60,'+','.join(['a:2:300']*7)
    prompts=json.loads((rt/'numberman-pet-v1-prompts/result.json').read_text())['actions']
    for name,tool,actions in [('intro-regression','capture_gutsman_intro.py',selection),('select-gutsman','capture_gutsman_pet.py',selection),('prompt-seed','capture_gutsman_pet.py','a:2:300,none:1:60'),('prompts','capture_gutsman_pet.py',prompts)]:
        out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve run')
        if name=='select-gutsman':parent=base
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        subprocess.run(cmd,check=True,cwd=ROOT);parent=out

if __name__=='__main__':main()
