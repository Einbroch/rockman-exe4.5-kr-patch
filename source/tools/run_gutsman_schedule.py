"""Own native save/PET regression then normal L schedule query."""
import sys,json,subprocess
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet
STEM='exe45_ko_development_gutsman_schedule_v1'
PREFIX='gutsman-schedule-v1-'
def main():
    run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman');out=rt/(PREFIX+'today')
    if out.exists():raise ValueError('preserve run')
    actions='none:1:60,l:2:180,none:1:60,a:2:180,none:1:60,a:2:180,none:1:60'
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_schedule.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
