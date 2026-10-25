"""Compare a batch's own coldboot captures with the041 replay: report pixel-diff boxes per capture.

Clock, cursor blink and sprite animation phase differ with timing; a capture counts as the same scene when <=35% of pixels differ (palette-animated floors).
Usage: compare_coldboot_generic_v1.py BATCH [REFERENCE=041]
"""
import sys,glob,json
from pathlib import Path
from PIL import Image,ImageChops
from build_visibility_poc import ROOT


def main():
    b=sys.argv[1];ref=sys.argv[2] if len(sys.argv)>2 else '041';out=[]
    for i in range(1,17):
        for pa in sorted(glob.glob(str(ROOT/f'poc/runtime/pending500-{ref}-normal-v1-{i:02d}/step_*.png'))):
            pb=pa.replace(f'pending500-{ref}-',f'pending500-{b}-')
            if not Path(pb).exists():out.append(dict(segment=i,step=Path(pa).name,missing=True));continue
            d=ImageChops.difference(Image.open(pa).convert('RGB'),Image.open(pb).convert('RGB'));box=d.getbbox()
            frac=sum(1 for px in d.get_flattened_data() if px!=(0,0,0))/(d.width*d.height)
            out.append(dict(segment=i,step=Path(pa).name,diff_box=box,diff_fraction=round(frac,4),clock_only=box is not None and frac<=0.35))
    bad=[x for x in out if x.get('missing') or (x['diff_box'] and not x['clock_only'])]
    rep=dict(batch=b,reference=ref,captures=len(out),identical=sum(1 for x in out if not x.get('missing') and x['diff_box'] is None),clock_only=sum(1 for x in out if x.get('clock_only')),other=bad)
    (ROOT/f'analysis/pending500_{b}_v1/coldboot_compare_v1.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(rep,other=len(bad)),ensure_ascii=False));[print(' ',x) for x in bad[:10]]


if __name__=='__main__':main()
