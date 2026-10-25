"""Actual019 full-box nickname, next-page clearing and return diagnostic."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_019_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes()
    pool,units,expected,streams,ends=model(rom,m,cfg,'66BF44',23,28,asset_folder='analysis/pending_insertion_500_019_cumulative_v1')
    if len(units)!=2:raise ValueError('Two native pages required')
    folder=ROOT/'poc/runtime/pending500-019-v1-name-food';r=read(folder/'result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['normal_play_checkpoint_eligible'] is not False or r['display_diagnostic']!={'roots':1,'entries':1,'navi':0,'root':pool,'script':23}:raise ValueError('Diagnostic identity')
    if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Diagnostic quarantine')
    for name,h in r['artifacts'].items():require_hash(folder/name,h)
    pages=[]
    for ordinal,step in enumerate((3,5)):
        cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(folder/(cp+'_roll_pet.json'));native=read(folder/(cp+'_return_ram.json'))['draws'];u=units[ordinal]
        e={s:expected[s] for s in streams[u['id']]};offsets={};row=0;width=0
        if ram[0x952]!=1 or ram[0xE50:0xE58]!=b'\x01'+b'\x9D'*6+b'\xE5':raise ValueError('Native owner identity')
        if ordinal==0:
            name_bytes=b'\x9D'*6+bytes.fromhex('ABE406CAE5')
            if ram[0x10AC0:0x10AC0+len(name_bytes)]!=name_bytes:raise ValueError('Native nickname residency')
            for s,i in zip([0x02010AC0+j for j in range(8)]+[0x02010AC9],[157]*6+[171,234,202]):
                record=rom[m['extension']['normal_font_offset']+i*96:m['extension']['normal_font_offset']+(i+1)*96]
                if record!=source[0x608758+i*96:0x608758+(i+1)*96]:raise ValueError('Native font identity')
                e[s]=dict(ch='native name',id='native_nickname',index=i,record=record);offsets[s]=width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0]
            if width!=99:raise ValueError('Native six-glyph plus honorific width')
        it=iter(streams[u['id']]);widths=[]
        for ch in u['translation']:
            if ch=='\n':widths.append(width);row+=1;width=0;continue
            s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
            if width>132 or row>2:raise ValueError('Aggregate geometry')
        widths.append(width)
        if ordinal==0 and widths[0]!=111:raise ValueError('Comma boundary')
        draws={d['stream']:d for d in obs['draws']+native if d['stream'] in e}
        if set(draws)!=set(e) or any(d['context']!=0x0200FA20 or d['glyph_index']!=e[s]['index'] or d['offset']!=offsets[s] for s,d in draws.items()):raise ValueError('Actual glyph geometry')
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+3]!=bytes.fromhex('E600F1') or tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('Full-box native wait/origin')
        counts=Counter(g['index'] for g in e.values());reads={x['index']:x['reads'] for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU font reads')
        proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=(52,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
        for s,g in e.items():
            rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0]
            occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(52+xx//4,52+xx//4+w))
        vacant={(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138)}-occupied
        if any(im.getpixel(p)!=im.getpixel((233,110)) for p in vacant):raise ValueError('Page residue')
        pages.append(dict(step=step,id=u['id'],row_widths=widths,wait_stream=ptr,vacant_pixels_cleared=len(vacant),**proof))
    ram=(folder/'step_007_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
    # The guarded 380D0 entry is Rockman's mail-alert lookup (65E8B8).
    # After the script ends, native execution selects Rockman's PET menu
    # via its separate 3809C lookup (65A608), not Roll's 65FA58 archive.
    ar=next(a for a in m['archives'] if a['archive']=='65A608')
    if struct.unpack_from('<I',source,0x380D0)[0]!=0x0865E8B8 or struct.unpack_from('<I',source,0x3809C)[0]!=0x0865A608 or 0x3809C not in ar['pointers']:raise ValueError('Own Rockman lookup identity')
    if root!=struct.unpack_from('<I',rom,0x3809C)[0] or root!=0x08000000+ar['rom_offset'] or root==pool or not root<=ptr<root+ar['compiled_bytes'] or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('Native return to own PET archive')
    frozen_write(ROOT/'analysis/pending500_019_v1/full_name_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],receipt_sha256=sha((folder/'result.json').read_bytes()),pages=pages,return_to_own_pet_archive=True,read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,limits='One native full-box two-page diagnostic, source portrait and controls retained. No natural meal-alarm route, all221 profiles, other Navi nickname provider, reentry, Hangul input/save or human semantic approval.'))
    print('PASS full-box nickname111px/two pages/clearing/keyWait/native PET return')

if __name__=='__main__':main()
