"""Hash-bound screenshot contact sheets; review evidence only, no game graphics edit."""
import argparse,math
from PIL import Image
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);p.add_argument('--natural-b0',action='store_true');a=p.parse_args()
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True);records=[]
    def sheet(name,groups,columns):
        images=[];refs=[]
        for suffix,steps in groups:
            folder=ROOT/f'poc/runtime/{a.prefix}-{suffix}';r=read(folder/'result.json')
            if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('022 visual receipt binding')
            for step in steps:
                path=folder/f'step_{step:03}.png';require_hash(path,r['artifacts'][path.name]);images.append(Image.open(path).convert('RGB'));refs.append(str(path.relative_to(ROOT)))
        target=out/name
        if target.exists():raise ValueError('Preserve visual evidence')
        im=Image.new('RGB',(columns*240,math.ceil(len(images)/columns)*160))
        for i,image in enumerate(images):im.paste(image,(i%columns*240,i//columns*160))
        im.save(target);records.append(dict(contact_sheet=str(target.relative_to(ROOT)),sources=refs))
    sheet('startup_pages_v1.png',[('boot',[2,3,8,9]),('pagecycle',[6,7,9]),('complete',[14,15,16,17,18,19,20,21,22,23,24,34])],4)
    sheet('mail_visual_pages_v1.png',[('read',list(range(10,33)))],5)
    if a.natural_b0:sheet('natural_b0_exits_v1.png',[('natural-b0-hint',[7,9,11,13])],4)
    else:sheet('hint_exits_v1.png',[(f'hint-display-{s}',read(f'poc/runtime/{a.prefix}-hint-display-{s}/result.json')['capture_steps']) for s in (11,15)],4)
    frozen_write(out/'visual_sheet_inputs.json',dict(schema=1,rom_sha256=m['output_sha256'],contact_sheets=records,visual_review_performed=False,release_eligible=False))
    print('Prepared exact-ROM startup/mail/hint-exit contact sheets; not visual approval')

if __name__=='__main__':main()
