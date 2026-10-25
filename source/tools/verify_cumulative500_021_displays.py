"""Actual021 long full-box pages, font/OBJ pixels, waits and clearing."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_021_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');pages=[];images=[]
    for case,arc,script,count,steps in [('guarded','7C0F8C',13,255,(3,5,7)),('reflow','768800',10,13,(3,5,7,9,11,13)),('break','76C944',137,144,(3,))]:
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,count,asset_folder='analysis/pending_insertion_500_021_cumulative_v1');folder=ROOT/f'poc/runtime/pending500-021-v1-display-{case}';r=read(folder/'result.json');diagnostic=dict(roots=1,entries=1,navi=0,root=pool,script=script)
        if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['normal_play_checkpoint_eligible'] is not False or r['display_diagnostic']!=diagnostic:raise ValueError('021 diagnostic binding')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('021 checkpoint quarantine')
        for name,h in r['artifacts'].items():require_hash(folder/name,h)
        if len(steps)!=len(units):raise ValueError('Complete selected pages')
        for step,u in zip(steps,units):
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();o=read(folder/(cp+'_roll_pet.json'));e={s:expected[s] for s in streams[u['id']]};offsets={};row=0;width=0;widths=[];it=iter(streams[u['id']])
            for ch in u['translation']:
                if ch=='\n':widths.append(width);row+=1;width=0;continue
                s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
                if row>2 or width>(168 if row==2 else 180):raise ValueError('Full-box model extent')
            widths.append(width);draws={d['stream']:d for d in o['draws'] if d['stream'] in e}
            if set(draws)!=set(e) or any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=e[s]['index'] for s,d in draws.items()):raise ValueError('Actual full-box renderer geometry')
            ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('E600') or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('Full-box native wait')
            reads={x['index']:x['reads'] for x in o['font_reads']};counts=Counter(g['index'] for g in e.values())
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Full-box CPU font reads')
            proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=(52,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
            for s,g in e.items():
                rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0];occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(52+xx//4,52+xx//4+w))
            vacant={(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138)}-occupied
            if any(im.getpixel(p)!=im.getpixel((233,110)) for p in vacant):raise ValueError('Full-box previous-page residue')
            pages.append(dict(case=case,id=u['id'],step=step,row_widths=widths,wait_stream=ptr,vacant_pixels_cleared=len(vacant),receipt_sha256=sha((folder/'result.json').read_bytes()),**proof));images.append(im)
    out=ROOT/'analysis/pending500_021_v1';sheet=Image.new('RGB',(720,((len(images)+2)//3)*160))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    path=out/'fullbox_pages_v1.png'
    if path.exists():raise ValueError('Preserve visual evidence')
    sheet.save(path)
    frozen_write(out/'fullbox_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],pages=pages,contact_sheet_sha256=sha(path.read_bytes()),read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,limits='Ten full-box pages: original guarded prelude and portrait changes plus21 selected same-wording placements represented by two reflow scripts. Not all500 literal displays, natural events/flags/acquisition, Hangul input/save or semantic approval.'))
    print('PASS actual021 full-box180px/font/OBJ/pixels/keyWait/clearing')
if __name__=='__main__':main()
