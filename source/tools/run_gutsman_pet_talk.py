"""Own fresh normal chain, native R pages, then quarantined representative entries."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
import run_gutsman_pet
STEM='exe45_ko_development_gutsman_pet_talk_v1'
PREFIX='gutsman-pet-talk-v1-'
OUTDIR='gutsman_pet_talk_v1'
SCRIPTS=[11,12,17,25,27,33,34]
def main():
    run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'select-gutsman')
    def capture(name,tool,actions,extra=()):
        out=rt/(PREFIX+name)
        if out.exists():raise ValueError('preserve evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),*extra,'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],check=True,cwd=ROOT)
    capture('normal-talk','capture_gutsman_pet_talk.py','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180,a:2:180,none:1:60')
    for script in SCRIPTS:
        actions='none:1:7,r:2:180,none:1:180'
        if script in [17,25,27,34]:actions+=',a:2:180,none:1:180'
        capture(f'script{script}','capture_gutsman_pet_talk_diagnostic.py',actions,['--talk-script',str(script)])
    capture('script31','capture_gutsman_pet_talk_nickname_diagnostic.py','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180',['--talk-script','31'])
if __name__=='__main__':main()
