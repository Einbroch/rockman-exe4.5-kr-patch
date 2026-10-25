"""Actual natural B0 default hint: original dispatch, font/OBJ/pixels and lifetime."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from field_b0_rom_data import input_entries
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    rp=ROOT/'poc/output/pending500_023_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    record=next(r for r in m['keyitem_rom']['b0_hint_archives'] if r['archive']=='78BF28')
    asset=next(a for _,_,a,_,_,_ in input_entries(source) if a['archive']=='78BF28')
    pool,units,expected,streams,ends=model(rom,m,cfg,'78BF28',10,255,record=record,asset=asset)
    if [u['id'] for u in units]!=['78BF28:10:0']:raise ValueError('Default hint literal scope')
    u=units[0];native=rom[record['native_copy_offset']:record['native_copy_offset']+record['native_copy_bytes']]
    folder=ROOT/'poc/runtime/pending500-023-v1-natural-b0-hint';receipt=read(folder/'result.json');d=receipt['natural_b0_hint']
    if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or not receipt['observer_only'] or receipt['loader_scene_table_flag_aliases'] or not receipt['normal_play_checkpoint_eligible']:
        raise ValueError('Normal-play observation provenance')
    if (d['calls'],d['entries'],d['selections'],d['root'])!=(2,2,2,pool) or len(d['wrapper_cycles'])!=2 or any(c<=0 for c in d['wrapper_cycles']):raise ValueError('Native caller/default selection counts')
    for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
    for i in (1,2):
        if (folder/f'b0_native_{i}.bin').read_bytes()!=native:raise ValueError('Native RAM before reader selections')
    pages=[];images=[];previous_last=-1
    for step in (7,11):
        cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();observer=read(folder/(cp+'_roll_pet.json'))
        if ram[0x4AD4]!=0xB0 or ram[0x4AD1]!=0 or ram[0x3D800:0x3D800+len(native)]!=native:raise ValueError('Natural B0/Navi0/native RAM residency')
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=pool or ptr!=ends[u['id']] or ram[0xFA21]!=10 or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600') or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('Original script0 jump/guard/default10/wait/origin')
        offsets={};row=width=0;it=iter(streams[u['id']]);widths=[]
        for ch in u['translation']:
            if ch=='\n':widths.append(width);row+=1;width=0;continue
            at=next(it);offsets[at]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[at]['index']*4)[0]
        widths.append(width)
        draws={e['stream']:e for e in observer['draws'] if e['stream'] in expected}
        if set(draws)!=set(expected) or any(e['context']!=0x0200FA20 or e['offset']!=offsets[at] or e['glyph_index']!=expected[at]['index'] or e['frame']<=previous_last for at,e in draws.items()):raise ValueError('Current execution glyph stream/geometry')
        previous_last=max(e['frame'] for e in draws.values())
        reads={e['index']:e['reads'] for e in observer['font_reads']};counts=Counter(e['index'] for e in expected.values())
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Actual font CPU reads')
        proof=pixels(folder,step,list(draws.values()),expected,rom,m,origin=(52,110))
        im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
        for at,g in expected.items():
            rr,xx=divmod(offsets[at],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0]
            occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(52+xx//4,52+xx//4+w))
        vacant={(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138)}-occupied
        if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('Native page clearing/translated residue')
        pages.append(dict(id=u['id'],step=step,script=10,widths=widths,wait_pointer=ptr,root=root,vacant_pixels_cleared=len(vacant),**proof));images.append(im)
    exits=[]
    for step in (9,13):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0x3D800:0x3D800+len(native)]!=native:raise ValueError('Native source lifetime after closing')
        exits.append(dict(step=step,native_ram_unchanged=True));images.append(Image.open(folder/f'step_{step:03}.png').convert('RGB'))
    out=ROOT/'analysis/pending500_023_v1';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(480,320))
    for i,im in enumerate(images):sheet.paste(im,((i%2)*240,(i//2)*160))
    image_path=out/'natural_b0_pages.png'
    if image_path.exists():raise ValueError('Preserve natural display evidence')
    sheet.save(image_path)
    frozen_write(out/'natural_b0_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),receipt=dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())),pages=pages,exits=exits,wrapper_cycles=d['wrapper_cycles'],ordinary_L_caller=True,original_script0_dispatch_and_default10_wait=True,loader_scene_script_table_progress_aliases=False,native_source_ram_preserved=True,normal_exit_and_reentry=True,contact_sheet_sha256=sha(image_path.read_bytes()),release_eligible=False,limits='Two normal executions of MegaMan B0 default hint only. Static500 capacity and CPU all-Navi/descriptor guards are separate evidence. Other branches, names/chip inserted display/provider states, A3 natural events, timing/audio/hardware and automatic Hangul entry/save remain open. Exit screenshots require visual review; no whole500 semantic approval.'))
    print('PASS normal B0 script0/default10 twice: font/OBJ/pixels/keyWait/clearing/native lifetime/exit/reentry')


if __name__=='__main__':main()
