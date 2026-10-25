"""Actual024 new raw normal/quick geometry, glyph CPU->OBJ->pixels/waits."""
import argparse
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_024_v1.gba')
    p.add_argument('--prefix',default='pending500-024-v1');p.add_argument('--out',default='analysis/pending500_024_v1/raw_displays.json');a=p.parse_args()
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    pages=[];images=[];returns=[]
    for case,arc,script,count,steps,origin in [
        ('windman','7C802C',3,21,(3,5),(52,110)),
        ('pet-quick','65B9E8',94,97,(3,),(92,110)),
        ('new-normal','778CC0',48,80,(3,),(52,110))]:
        owner=[r for r in m['translation_assets'] if r.get('archive')==arc and not r.get('scope','').startswith('read-only inherited')]
        if len(owner)!=1:raise ValueError('024 sampled effective input owner')
        require_hash(ROOT/owner[0]['path'],owner[0]['sha256']);asset=read(owner[0]['path'])
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,count,asset=asset)
        folder=ROOT/'poc/runtime'/(a.prefix+'-raw-'+case);receipt=read(folder/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] is not False or receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):
            raise ValueError('024 raw diagnostic provenance')
        if (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists() or len(units)!=len(steps):
            raise ValueError('024 quarantine/full sampled script pages')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        for step,u in zip(steps,units):
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'))
            e={s:expected[s] for s in streams[u['id']]};offsets={};row=width=0;it=iter(streams[u['id']]);widths=[]
            for ch in u['translation']:
                if ch=='\n':widths.append(width);row+=1;width=0;continue
                s=next(it);offsets[s]=row*10752+width*4
                width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
                limit=132 if origin[0]==92 else 168 if row==2 else 180
                if row>2 or width>limit:raise ValueError('024 sampled native extent')
            widths.append(width)
            draws={d['stream']:d for d in trace['draws'] if d['stream'] in e}
            if set(draws)!=set(e) or any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=e[s]['index'] for s,d in draws.items()):
                raise ValueError('024 actual glyph stream/offset')
            ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600') or tuple(ram[0xFA38:0xFA3A])!=origin:
                raise ValueError('024 native wait/root/origin')
            reads={r['index']:r['reads'] for r in trace['font_reads']};counts=Counter(g['index'] for g in e.values())
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('024 font CPU reads')
            proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=origin)
            im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
            for s,g in e.items():
                rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0]
                occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(origin[0]+xx//4,origin[0]+xx//4+w))
            vacant={(x,y) for y in range(110,150) for x in range(origin[0],234) if not(x>=224 and y>=138)}-occupied
            if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('024 sampled page residue')
            pages.append(dict(case=case,id=u['id'],step=step,widths=widths,wait_pointer=ptr,vacant_pixels_cleared=len(vacant),**proof));images.append(im)
        last=receipt['capture_steps'][-1];ram=(folder/f'step_{last:03}_gbaExtWorkRam.bin').read_bytes()
        own=next(r for r in m['archives'] if r['archive']=='65A608');root=struct.unpack_from('<I',ram,0xFA50)[0]
        if root!=0x08000000+own['rom_offset']:raise ValueError('024 original own PET return')
        returns.append(dict(case=case,step=last,original_pet_root=root));images.append(Image.open(folder/f'step_{last:03}.png').convert('RGB'))
    out=ROOT/a.out;image_path=out.with_suffix('.png')
    if image_path.exists():raise ValueError('Preserve024 contact sheet')
    sheet=Image.new('RGB',(720,((len(images)+2)//3)*160))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    out.parent.mkdir(parents=True,exist_ok=True);sheet.save(image_path)
    frozen_write(out,dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,returns=returns,
        contact_sheet=dict(path=str(image_path.relative_to(ROOT)),sha256=sha(image_path.read_bytes())),
        read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,
        limits='New raw four-page samples only; PET root/table read aliases preserve actual native initializer '
               'and rendering but do not prove native event/character selection, branch/flag effects, all500 '
               'semantics, save behavior or automatic Hangul commit/save/redisplay.'))
    print('PASS024 new raw4pages glyphCPU/OBJ/pixels/waits/clearing;3 original PET returns')


if __name__=='__main__':main()
