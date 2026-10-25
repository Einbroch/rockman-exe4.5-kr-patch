"""Final-ROM raw/hint display samples: font/OBJ/pixels/waits/lifetime, not events."""
import argparse,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from hint_rom_data import input_entries,verify_final
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('Preserve display evidence')
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes();verify_final(source,rom,m['keyitem_rom']);pages=[];images=[]
    asset=next(e[2] for e in input_entries(source) if e[2]['archive']=='786D38');record=next(r for r in m['keyitem_rom']['hint_archives'] if r['archive']=='786D38')
    hint_native=rom[record['native_copy_offset']:record['native_copy_offset']+record['native_copy_bytes']];timings=[]
    def sample(kind,folder,arc,script,count,steps,**kwargs):
        pool,units,expected,streams,ends=model(rom,m,cfg,arc,script,count,**kwargs);r=read(folder/'result.json')
        if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['normal_play_checkpoint_eligible'] is not False:raise ValueError('022 display receipt')
        if (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('022 checkpoint quarantine')
        for name,h in r['artifacts'].items():require_hash(folder/name,h)
        if kind=='hint':
            d=r['hint_diagnostic'];cycles=d.get('wrapper_cycles',[])
            if {k:v for k,v in d.items() if k!='wrapper_cycles'}!=dict(loads=1,scenes=2,entries=2,calls=2,root=pool,script=script) or len(cycles)!=2 or any(c<=0 for c in cycles):raise ValueError('022 loader/guard/consumer intervention counts/timing')
            timings.append(dict(archive=arc,script=script,wrapper_cycles=cycles,scope='Mesen cpu.cycleCount delta on two diagnostic calls; may include interrupts; muted audio; not every platform/Navi'))
            for i in (1,2):
                if (folder/f'hint_native_{i}.bin').read_bytes()!=hint_native:raise ValueError('022 native payload before both reader selections')
            selected=units*2
        else:
            if r['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('022 raw diagnostic binding')
            selected=units
        if len(steps)!=len(selected):raise ValueError('022 complete selected script pages')
        for step,u in zip(steps,selected):
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();o=read(folder/(cp+'_roll_pet.json'));e={s:expected[s] for s in streams[u['id']]};offsets={};row=0;width=0;widths=[];it=iter(streams[u['id']])
            for ch in u['translation']:
                if ch=='\n':widths.append(width);row+=1;width=0;continue
                s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
                if row>2 or width>(168 if row==2 else 180):raise ValueError('022 full-box geometry bound')
            widths.append(width);draws={d['stream']:d for d in o['draws'] if d['stream'] in e}
            if set(draws)!=set(e) or any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=e[s]['index'] for s,d in draws.items()):raise ValueError('022 glyph geometry')
            ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600') or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('022 native wait/root/origin')
            if kind=='hint' and ram[0x3D800:0x3D800+len(hint_native)]!=hint_native:raise ValueError('022 native RAM residency/lifetime')
            reads={x['index']:x['reads'] for x in o['font_reads']};counts=Counter(g['index'] for g in e.values())
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('022 font CPU consumption')
            proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=(52,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
            for s,g in e.items():
                rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0];occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(52+xx//4,52+xx//4+w))
            vacant={(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138)}-occupied
            if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('022 prior-page residue')
            pages.append(dict(kind=kind,id=u['id'],step=step,row_widths=widths,wait_stream=ptr,vacant_pixels_cleared=len(vacant),receipt_sha256=sha((folder/'result.json').read_bytes()),**proof));images.append(im)
    for script in (11,15):
        folder=ROOT/f'poc/runtime/{a.prefix}-hint-display-{script}';r=read(folder/'result.json');steps=r['capture_steps'];sample('hint',folder,'786D38',script,255,(steps[0],steps[2]),record=record,asset=asset)
        for step in (steps[1],steps[3]):
            ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            if ram[0x3D800:0x3D800+len(hint_native)]!=hint_native:raise ValueError('022 native RAM across exit')
    for case,arc,script,count,steps in [('bass','7CB850',0,23,(3,5,7)),('carry','7CAF40',5,45,(3,5))]:sample('raw',ROOT/f'poc/runtime/{a.prefix}-raw-display-{case}',arc,script,count,steps,asset_folder='analysis/pending_insertion_500_022_cumulative_v1')
    # Ordinary Monday route must retain its own native B0 hint, not the A3 clone.
    folder=ROOT/f'poc/runtime/{a.prefix}-weekday-native-hint';r=read(folder/'result.json')
    from verify_tpi_index import lz77_decompress
    native=lz77_decompress(source,0x78BF28)[0]
    if not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('022 normal fallback receipt')
    for name,h in r['artifacts'].items():require_hash(folder/name,h)
    for step in (7,11):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0x4AD4]!=0xB0 or ram[0x3D800:0x3D800+len(native)]!=native or struct.unpack_from('<I',ram,0xFA50)[0]!=0x0203D800:raise ValueError('022 ordinary wrong-scene fallback/root/native lifetime')
    sheet=Image.new('RGB',(720,((len(images)+2)//3)*160))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    image_path=out.with_suffix('.png')
    if image_path.exists():raise ValueError('Preserve visual sheet')
    out.parent.mkdir(parents=True,exist_ok=True);sheet.save(image_path)
    frozen_write(out,dict(schema=1,passed=True,rom_sha256=m['output_sha256'],pages=pages,hint_wrapper_timing=timings,contact_sheet_sha256=sha(image_path.read_bytes()),ordinary_native_hint_fallback_verified=True,read_alias_diagnostic=True,natural_selected_hint_event_verified=False,release_eligible=False,limits='Two selected hint scripts (two/three rows), each exit/reentry with native source RAM retained, and five raw pages. Loader/scene/table read aliases are diagnostic only. No all500 displays/natural event selection, other Navi/timing/audio targets, Hangul input/save or human semantic approval.'))
    print('PASS actual022 nine sampled pages: font/OBJ/pixels/waits/clearing; hint native RAM/exit/reentry and ordinary fallback')

if __name__=='__main__':main()
