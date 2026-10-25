"""Derived034 exact-ROM screenshot contact sheets; no game graphic edits."""
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    out=ROOT/'analysis/pending500_034_v1';m=read('poc/output/pending500_034_v1.json');require_hash(ROOT/'poc/output/pending500_034_v1.gba',m['output_sha256']);prefix='pending500-034-v1-'
    groups={'startup':[(prefix+'boot',s) for s in (2,3,8,9)]+[(prefix+'pagecycle',s) for s in (6,7,9)]+[(prefix+'complete',s) for s in (14,15,16,17,18,19,20,21,22,23,24,34)]+[(prefix+'selection',s) for s in (26,29,32)],'mail':[(prefix+'read',p['step']) for p in read(out/'normal_runtime.json')['first_mail_body_pages'][:23]],'samples':[(prefix+'sample-v2-'+name,s) for name,steps in [('list-caption',(3,)),('query-choice',(3,4,5)),('mission-caption',(3,4,5)),('trader-caption',(3,))] for s in steps]}
    refs=[]
    for name,items in groups.items():
        sheet=Image.new('RGB',(960,((len(items)+3)//4)*180),'#20232a');draw=ImageDraw.Draw(sheet)
        for i,(segment,step) in enumerate(items):
            folder=ROOT/'poc/runtime'/segment;r=read(folder/'result.json');filename=f'step_{step:03}.png'
            if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('034 exact screenshot applicability')
            require_hash(folder/filename,r['artifacts'][filename]);im=Image.open(folder/filename).convert('RGB')
            if im.size!=(240,160):raise ValueError('034 native screenshot canvas')
            x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+4,y+3),segment.removeprefix(prefix)+' '+str(step),fill='white')
        target=out/(name+'_contact_v2.png')
        if target.exists():raise ValueError('034 preserve contact sheet')
        sheet.save(target);refs.append(dict(kind=name,path=str(target.relative_to(ROOT)),sha256=sha(target.read_bytes()),screens=len(items)))
    frozen_write(out/'visual_inputs_v2.json',dict(schema=1,rom_sha256=m['output_sha256'],sheets=refs,visual_reviewed=False,release_eligible=False))
    print('034 contact sheets',[(s['kind'],s['screens']) for s in refs])


if __name__=='__main__':main()
