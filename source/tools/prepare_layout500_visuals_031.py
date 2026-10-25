"""Derived exact031 screenshot contact sheets; no game graphics edits."""
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rp=ROOT/'poc/output/pending500_031_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    out=ROOT/'analysis/pending500_031_v1';prefix='pending500-031-v1'
    groups={
        'startup': [('boot',s) for s in (2,3,8,9)]+[('pagecycle',s) for s in (6,7,9)]+[('complete',s) for s in (14,15,16,17,18,19,20,21,22,23,24,34)]+[('selection',s) for s in (26,29,32)],
        'mail': [('read',p['step']) for p in read(out/'normal_runtime.json')['first_mail_body_pages'][:23]],
        'opponent': [(case,s) for case in ('opponent-lost-chip-max','opponent-defeated-chip-max') for s in read(ROOT/'poc/runtime'/(prefix+'-'+case)/'result.json')['capture_steps']],
    }
    groups['calendar']=[('calendar-'+name,step) for name,step in [('meal',7),('first',2),('confirm',2),('no',2),('cancel',2),('yes',2),('reentry',2)]]
    refs=[]
    for name,items in groups.items():
        sheet=Image.new('RGB',(960,((len(items)+3)//4)*180),'#20232a');draw=ImageDraw.Draw(sheet)
        for i,(segment,step) in enumerate(items):
            folder=ROOT/'poc/runtime'/('pending500-031-'+segment if segment.startswith('calendar-') else prefix+'-'+segment);receipt=read(folder/'result.json')
            if not receipt['complete'] or receipt['rom_sha256']!=m['output_sha256']:raise ValueError('031 screenshot applicability')
            filename=f'step_{step:03}.png';require_hash(folder/filename,receipt['artifacts'][filename])
            im=Image.open(folder/filename).convert('RGB')
            if im.size!=(240,160):raise ValueError('031 native screenshot canvas')
            x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+4,y+3),segment+' '+str(step),fill='white')
        target=out/(name+'_contact.png')
        if target.exists():raise ValueError('Preserve031 contact sheet')
        sheet.save(target);refs.append(dict(kind=name,path=str(target.relative_to(ROOT)),sha256=sha(target.read_bytes()),screens=len(items)))
    frozen_write(out/'visual_inputs.json',dict(schema=1,rom_sha256=m['output_sha256'],sheets=refs,visual_reviewed=False,release_eligible=False))
    print('Prepared031 exact-ROM visual review sheets',[(r['kind'],r['screens']) for r in refs])


if __name__=='__main__':main()
