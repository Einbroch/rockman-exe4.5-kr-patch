"""Derived exact032 capture contact sheets; no game graphic editing."""
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    m=read('poc/output/pending500_032_v1.json');require_hash(ROOT/'poc/output/pending500_032_v1.gba',m['output_sha256']);out=ROOT/'analysis/pending500_032_v1';prefix='pending500-032-v1-'
    groups={
        'startup':[(prefix+'boot',s) for s in (2,3,8,9)]+[(prefix+'pagecycle',s) for s in (6,7,9)]+[(prefix+'complete',s) for s in (14,15,16,17,18,19,20,21,22,23,24,34)]+[(prefix+'selection',s) for s in (26,29,32)],
        'mail':[(prefix+'read',p['step']) for p in read(out/'normal_runtime.json')['first_mail_body_pages'][:23]],
        'menus':[('pending500-032-menu-'+n,s) for n,s in [('home',3),('register',3),('second',2),('cancel',2),('time-edit',2),('time',6),('meal',5),('meal',7),('inventory',2),('inventory-cancel',2),('inventory-reentry',2),('inventory-accept',2)]],
        'anniversary':[('calendar-anniversary-032-product-'+n+'-v1',s) for n,s in [('ten',11),('ten',12),('register',4),('delete-first',2),('delete-confirm',2),('delete-no',3),('delete-yes',2)]],
    };refs=[]
    for name,items in groups.items():
        sheet=Image.new('RGB',(960,((len(items)+3)//4)*180),'#20232a');draw=ImageDraw.Draw(sheet)
        for i,(segment,step) in enumerate(items):
            folder=ROOT/'poc/runtime'/segment;r=read(folder/'result.json');filename=f'step_{step:03}.png'
            if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('032 exact screenshot applicability')
            require_hash(folder/filename,r['artifacts'][filename]);im=Image.open(folder/filename).convert('RGB')
            if im.size!=(240,160):raise ValueError('032 native screen canvas')
            x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+4,y+3),segment.replace('pending500-032-','').replace('calendar-anniversary-032-product-','anniv-')+' '+str(step),fill='white')
        target=out/(name+'_contact.png')
        if target.exists():raise ValueError('Preserve032 contact sheet')
        sheet.save(target);refs.append(dict(kind=name,path=str(target.relative_to(ROOT)),sha256=sha(target.read_bytes()),screens=len(items)))
    frozen_write(out/'visual_inputs.json',dict(schema=1,rom_sha256=m['output_sha256'],sheets=refs,visual_reviewed=False,release_eligible=False));print('032 visual sheets prepared',[(s['kind'],s['screens']) for s in refs])


if __name__=='__main__':main()
