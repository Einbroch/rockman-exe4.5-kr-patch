"""Normal-input PET confirmation/no/B routes; never accepts save or link Yes."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from capture_pet_menu_qa import route

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stem',default='exe45_ko_development_roll_pet_v2');ap.add_argument('--origin',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    rom=ROOT/f'poc/output/{a.stem}.gba';m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256']);origin=ROOT/a.origin;out=ROOT/a.out;steps=route('prompts')
    cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_roll_pet.py'),'--rom',str(rom),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),'--probe','snapshot','--actions',','.join(f'{k}:{h}:{w}' for k,h,w,_ in steps),'--capture-steps',','.join(str(i) for i in range(1,len(steps)+1)),'--timeout','240']
    rc=subprocess.call(cmd,cwd=ROOT)
    if not rc:(out/'route_expectations.json').write_text(json.dumps({'scope':'expected controller route only, not visual pass','steps':[{'step':i,'expected':n} for i,(_,_,_,n) in enumerate(steps,1)]},ensure_ascii=False,indent=2),encoding='utf-8')
    return rc

if __name__=='__main__':raise SystemExit(main())
