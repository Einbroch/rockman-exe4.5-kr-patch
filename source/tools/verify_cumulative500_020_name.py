"""Corrected possessive suffix following the native six-glyph nickname."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_020_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/cfg['source_profile']['filename'],m['source_sha256'])
    pool,units,expected,streams,ends=model(rom,m,cfg,'66CA84',21,97,asset_folder='analysis/pending_insertion_500_020_cumulative_v1');u=units[-1]
    if u['id']!='66CA84:21:3' or not u['translation'].startswith('의\n'):raise ValueError('Corrected wording identity')
    folder=ROOT/'poc/runtime/pending500-020-v1-name-possessive';r=read(folder/'result.json');d=dict(roots=1,entries=1,navi=0,root=pool,script=21)
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['normal_play_checkpoint_eligible'] is not False or r['display_diagnostic']!=d:raise ValueError('Name diagnostic identity')
    if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Name checkpoint quarantine')
    for name,h in r['artifacts'].items():require_hash(folder/name,h)
    step=9;cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(folder/(cp+'_roll_pet.json'));native=read(folder/(cp+'_return_ram.json'))['draws'];name_bytes=b'\x9D'*6+bytes.fromhex('ABE406CAE5')
    if ram[0x952]!=1 or ram[0xE50:0xE58]!=b'\x01'+b'\x9D'*6+b'\xE5' or ram[0x10AC0:0x10AC0+len(name_bytes)]!=name_bytes:raise ValueError('Native name identity')
    e={s:expected[s] for s in streams[u['id']]};offsets={};width=0;row=0
    for s,i in zip([0x02010AC0+j for j in range(8)]+[0x02010AC9],[157]*6+[171,234,202]):
        record=rom[m['extension']['normal_font_offset']+i*96:m['extension']['normal_font_offset']+(i+1)*96]
        if record!=source[0x608758+i*96:0x608758+(i+1)*96]:raise ValueError('Native font identity')
        e[s]=dict(ch='native name',id='native_nickname',index=i,record=record);offsets[s]=width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0]
    if width!=99:raise ValueError('Native nickname bound')
    it=iter(streams[u['id']]);widths=[]
    for ch in u['translation']:
        if ch=='\n':widths.append(width);row+=1;width=0;continue
        s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
        if width>132 or row>2:raise ValueError('Name aggregate layout')
    widths.append(width)
    if widths[0]!=111:raise ValueError('Possessive boundary')
    draws={x['stream']:x for x in obs['draws']+native if x['stream'] in e}
    if set(draws)!=set(e) or any(x['context']!=0x0200FA20 or x['offset']!=offsets[s] or x['glyph_index']!=e[s]['index'] for s,x in draws.items()):raise ValueError('Actual name renderer geometry')
    ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
    if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('E600') or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('Name keyWait')
    reads={x['index']:x['reads'] for x in obs['font_reads']};counts=Counter(g['index'] for g in e.values())
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Name CPU font reads')
    proof=pixels(folder,step,list(draws.values()),e,rom,m,origin=(92,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
    for s,g in e.items():
        rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0];occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(92+xx//4,92+xx//4+w))
    vacant={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138)}-occupied
    if any(im.getpixel(p)!=im.getpixel((233,110)) for p in vacant):raise ValueError('Name page residue')
    frozen_write(ROOT/'analysis/pending500_020_v1/name_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],id=u['id'],row_widths=widths,receipt_sha256=sha((folder/'result.json').read_bytes()),step=step,read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,limits='One corrected possessive page with native6glyph Rockman/female provider. Source WindMan scene is selected diagnostically; not natural profile/Navi-provider/Hangul input/save or human semantic approval.',**proof))
    print('PASS actual020 native6glyph+possessive111px CPU/font/OBJ/pixels/wait/clearing')
if __name__=='__main__':main()
