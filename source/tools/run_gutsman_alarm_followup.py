"""Fresh own normal chain then second-page renderer diagnostics; no event writes."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet
STEM='exe45_ko_development_gutsman_alarm_followup_v1'
PREFIX='gutsman-alarm-followup-v1-'
OUTDIR='gutsman_alarm_followup_v1'
def main():
    run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman')
    for script in [1,2,4,6]:
        out=rt/(PREFIX+f'script{script}')
        if out.exists():raise ValueError('preserve evidence')
        actions='none:1:7,r:2:180,none:1:180'
        if script!=6:actions+=',a:2:180,none:1:180'
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_alarm_followup.py'),'--alarm-script',str(script),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
    out=rt/(PREFIX+'chip13')
    if out.exists():raise ValueError('preserve chip evidence')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_gutsman_chipquest.py'),'--talk-script','13','--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180,r:2:180,none:1:180','--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
if __name__=='__main__':main()
