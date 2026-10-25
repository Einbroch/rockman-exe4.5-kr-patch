"""Contact sheets of unchanged emulator screenshots for local visual QA."""
import argparse,json,math
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash

def main():
    p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);p.add_argument('--mode',choices=['normal','remaining','header'],required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('preserve local QA gallery')
    out.mkdir();items=[]
    choices=([('boot',list(range(1,11))),('pagecycle',[6,7,9]),('complete',[19,20,21,22,23,24,34]),('selection',[23,26,29,32]),('read',list(range(1,38)))] if a.mode=='normal'
             else [(f'official{s}',list(range(9,11+n))) for s,n in [(11,13),(12,9),(13,8),(14,9)]] if a.mode=='remaining'
             else [(f'header-pair{s}',[9]) for s in [1,2,3,8,9,10,11,12,13,14]])
    for suffix,steps in choices:
        folder=ROOT/f'poc/runtime/{a.prefix}-{suffix}'
        r=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if not r['complete']:raise ValueError('incomplete capture folder')
        for step in steps:
            path=folder/f'step_{step:03}.png'
            require_hash(path,r['artifacts'][path.name]);items.append((f'{suffix} step{step:03}',path))
    sheets=[]
    for batch in range(math.ceil(len(items)/9)):
        group=items[batch*9:batch*9+9];canvas=Image.new('RGB',(1440,3*352),(20,20,20));draw=ImageDraw.Draw(canvas)
        for k,(label,path) in enumerate(group):
            x=(k%3)*480;y=(k//3)*352
            draw.text((x+8,y+5),label,fill='white')
            with Image.open(path) as im:
                if im.size!=(240,160):raise ValueError('expected native GBA screenshot')
                canvas.paste(im.convert('RGB').resize((480,320),Image.Resampling.NEAREST),(x,y+28))
        path=out/f'sheet_{batch+1:02}.png';canvas.save(path);sheets.append(dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes())))
    (out/'index.json').write_text(json.dumps(dict(mode=a.mode,images=[dict(label=l,path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes())) for l,p in items],sheets=sheets),indent=2)+'\n',encoding='utf8')
    print('Local unchanged screenshot gallery',len(items),'images',len(sheets),'sheets')

if __name__=='__main__':main()
