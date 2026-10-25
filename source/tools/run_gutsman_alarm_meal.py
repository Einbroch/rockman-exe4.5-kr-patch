"""Own alarm regressions followed by native-nickname meal renderer samples."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_alarm_followup as base
STEM='exe45_ko_development_gutsman_alarm_meal_v1'
PREFIX='gutsman-alarm-meal-v1-'
OUTDIR='gutsman_alarm_meal_v1'
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman');out=rt/(PREFIX+'script3')
    if out.exists():raise ValueError('preserve meal evidence')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_alarm_names.py'),'--alarm-script','3','--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180','--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
