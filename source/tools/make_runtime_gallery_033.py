"""Contact sheets of exact033 captured screens; no visual approval inferred."""
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rom=ROOT/'poc/output/pending500_033_v1.gba';m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256'])
    out=ROOT/'analysis/pending500_033_v1/visual_review_v1'
    if out.exists():raise ValueError('Preserve gallery evidence')
    files=[]
    for folder in sorted((ROOT/'poc/runtime').glob('pending500-033-v1-*')):
        receipt=read(folder/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=m['output_sha256']:raise ValueError('033 complete own-ROM receipt')
        for p in sorted(folder.glob('step_*.png')):
            require_hash(p,receipt['artifacts'][p.name]);files.append(p)
    if not files:raise ValueError('033 screenshots required')
    out.mkdir();sheets=[];entries=[]
    for first in range(0,len(files),12):
        group=files[first:first+12];sheet=Image.new('RGB',(960,540),(32,32,32));draw=ImageDraw.Draw(sheet)
        for n,p in enumerate(group):
            im=Image.open(p).convert('RGB')
            if im.size!=(240,160):raise ValueError('033 native screenshot canvas')
            x=n%4*240;y=n//4*180;sheet.paste(im,(x,y+20))
            label=p.parent.name.replace('pending500-033-v1-','')+'/'+p.stem
            draw.text((x+2,y+3),label,fill=(255,255,255))
            entries.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()),sheet=len(sheets)+1,cell=n))
        dest=out/f'sheet_{len(sheets)+1:02}.png';sheet.save(dest)
        sheets.append(dict(path=str(dest.relative_to(ROOT)),sha256=sha(dest.read_bytes())))
    frozen_write(out/'index.json',dict(schema=1,rom_sha256=m['output_sha256'],screens=len(entries),entries=entries,sheets=sheets,agent_visual_review_pending=True,release_eligible=False))
    print('033 gallery',len(entries),'screens',len(sheets),'sheets; direct review pending')


if __name__=='__main__':main()
