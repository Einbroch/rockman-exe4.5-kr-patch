"""Fresh immutable-ROM controller-only seasonal and regression capture."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

STEM='exe45_ko_development_gutsman_seasonal_v1'
PREFIX='gutsman-seasonal-v1-'

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/run_numberman_seasonal_normal.py'),'--stem',STEM,'--prefix',PREFIX],check=True,cwd=ROOT)
    rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'normal-reload-select')
    for name,actions in [('select-gutsman','none:1:60,left:2:60,'+','.join(['a:2:180']*16)),('gutsman-advance','none:1:60,'+','.join(['a:2:180']*8))]:
        out=rt/(PREFIX+name)
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_numberman_seasonal.py'),'--seasonal-archive','66A234','--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        subprocess.run(cmd,check=True,cwd=ROOT);parent=out

if __name__=='__main__':main()
