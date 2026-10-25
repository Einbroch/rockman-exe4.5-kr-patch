"""Controller-only normal031 anniversary route, immutable named segments."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read


def main():
    p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--parent',required=True);p.add_argument('--actions',required=True);a=p.parse_args()
    if not a.name.replace('-','').isalnum() or not a.parent.replace('-','').isalnum():raise ValueError('032 safe segment name')
    rp=ROOT/'poc/output/pending500_031_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);parent=ROOT/'poc/runtime'/a.parent
    subprocess.run([sys.executable,'-X','utf8','tools/capture_event_buffers_product_031.py','--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out','poc/runtime/calendar-anniversary-032-'+a.name+'-v1','--probe','snapshot','--actions',a.actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')],cwd=ROOT,check=True)


if __name__=='__main__':main()
