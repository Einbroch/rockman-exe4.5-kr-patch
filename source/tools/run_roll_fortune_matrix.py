"""Fresh own-ROM normal chains and read-only fortune/PET regressions."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from run_roll_equipment_guides_matrix import main as roll,RECIPE_ROM
from run_equipment_guides_matrix import main as rockman

STEM='exe45_ko_development_roll_fortune_v1'
PREFIX='roll-fortune-v1-'

def segment(tool,out,parent,actions,captures=None):
    rom=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    args=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/'poc/runtime'/out),'--probe','snapshot','--actions',actions,'--timeout','240']
    if captures:args+=['--capture-steps',','.join(map(str,captures))]
    p=ROOT/'poc/runtime'/parent;args+=['--state',str(p/'checkpoint.mss'),'--state-origin',str(p/'result.json')]
    subprocess.run(args,cwd=ROOT,check=True)

def main():
    if roll(STEM,PREFIX+'roll-',pet_probe=True,intro_probe=True):return 1
    for name,parent,recipe in [('fortune-select','roll-navi-menu','roll-equipment-v1-select-roll'),('fortune-intro','fortune-select','roll-equipment-v1-roll-intro')]:
        r=json.loads((ROOT/'poc/runtime'/recipe/'result.json').read_text())
        if r['rom_sha256']!=RECIPE_ROM or not r['complete']:raise ValueError('input recipe identity')
        segment('capture_roll_fortune.py',PREFIX+name,PREFIX+parent,r['actions'])
    segment('capture_roll_pet.py',PREFIX+'seed',PREFIX+'roll-intro','none:1:60,b:2:90,a:2:180,none:1:180')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/run_roll_pet_prompts.py'),'--stem',STEM,'--origin','poc/runtime/'+PREFIX+'seed','--out','poc/runtime/'+PREFIX+'prompts'],cwd=ROOT,check=True)
    return rockman(STEM,PREFIX+'rockman-',weapons=True,caption=True)

if __name__=='__main__':raise SystemExit(main())
