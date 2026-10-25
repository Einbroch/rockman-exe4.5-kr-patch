"""Actual024 newly added A3 pages, native loader/guard/font/OBJ and lifetime."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    rp=ROOT/'poc/output/pending500_024_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json')
    record=next(r for r in m['keyitem_rom']['hint_archives'] if r['archive']=='786D38')
    require_hash(ROOT/record['asset_path'],record['asset_sha256']);asset=read(record['asset_path'])
    native=rom[record['native_copy_offset']:record['native_copy_offset']+record['native_copy_bytes']]
    pages=[];exits=[];images=[]
    for script in (10,26):
        pool,units,expected,streams,ends=model(rom,m,cfg,'786D38',script,255,record=record,asset=asset)
        if len(units)!=1 or units[0]['id'] not in record['cumulative024']['new_ids']:raise ValueError('024 newly inserted A3 sample identity')
        u=units[0];folder=ROOT/f'poc/runtime/pending500-024-v1-hint-display-{script}';receipt=read(folder/'result.json');d=receipt['hint_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] is not False:
            raise ValueError('024 hint diagnostic provenance')
        if {k:v for k,v in d.items() if k!='wrapper_cycles'}!=dict(loads=1,scenes=2,entries=2,calls=2,root=pool,script=script) or len(d['wrapper_cycles'])!=2:
            raise ValueError('024 native loader/reader counts')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        for i in (1,2):
            if (folder/f'hint_native_{i}.bin').read_bytes()!=native:raise ValueError('024 native source before hint selection')
        if (folder/'checkpoint.mss').exists():raise ValueError('024 diagnostic checkpoint quarantine')
        for step in receipt['capture_steps'][::2]:
            cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'))
            if ram[0x3D800:0x3D800+len(native)]!=native:raise ValueError('024 A3 native residency')
            offsets={};width=row=0;it=iter(streams[u['id']]);widths=[]
            for ch in u['translation']:
                if ch=='\n':widths.append(width);row+=1;width=0;continue
                s=next(it);offsets[s]=row*10752+width*4
                width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
                if row>2 or width>(168 if row==2 else 180):raise ValueError('024 A3 geometry')
            widths.append(width);draws={d['stream']:d for d in trace['draws'] if d['stream'] in expected}
            if set(draws)!=set(expected) or any(d['context']!=0x0200FA20 or d['offset']!=offsets[s] or d['glyph_index']!=expected[s]['index'] for s,d in draws.items()):raise ValueError('024 A3 actual glyphs')
            ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool or ptr!=ends[u['id']] or tuple(ram[0xFA38:0xFA3A])!=(52,110) or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('024 A3 wait/root')
            reads={r['index']:r['reads'] for r in trace['font_reads']};counts=Counter(g['index'] for g in expected.values())
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('024 A3 font CPU reads')
            proof=pixels(folder,step,list(draws.values()),expected,rom,m,origin=(52,110))
            im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
            for s,g in expected.items():
                rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0]
                occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(52+xx//4,52+xx//4+w))
            vacant={(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138)}-occupied
            if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('024 A3 page residue')
            pages.append(dict(id=u['id'],step=step,widths=widths,**proof));images.append(im)
        for step in receipt['capture_steps'][1::2]:
            ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();oam=(folder/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
            if ram[0x3D800:0x3D800+len(native)]!=native or ram[0xFA20]!=0:raise ValueError('024 A3 native lifetime/closed context')
            for i in range(128):
                attr,_,tile=struct.unpack_from('<3H',oam,i*8)
                if not attr&0x2300 and tile>>12==14:raise ValueError('024 A3 closed text/cursor OBJ residue')
            exits.append(dict(script=script,step=step,native_ram_unchanged=True,context_inactive=True,dialog_OBJ_cleared=True))
    out=ROOT/'analysis/pending500_024_v1';sheet=Image.new('RGB',(480,320))
    for i,im in enumerate(images):sheet.paste(im,(i%2*240,i//2*160))
    image=out/'a3_pages.png'
    if image.exists():raise ValueError('Preserve024 A3 sheet')
    sheet.save(image)
    frozen_write(out/'a3_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,exits=exits,
        contact_sheet=dict(path=str(image.relative_to(ROOT)),sha256=sha(image.read_bytes())),
        read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,
        limits='Two newly added A3 scripts each twice with native compressed load, exact source guard, '
               'font/OBJ/pixels/waits/clear/exit/reentry. Loader/scene/table read aliases are quarantined; '
               'no natural A3 event/provider/branch or all500 semantic claim.'))
    print('PASS024 new A3 two scripts twice;native loader/guard/residency/glyphCPU/OBJ/pixels/waits/4 exits')


if __name__=='__main__':main()
