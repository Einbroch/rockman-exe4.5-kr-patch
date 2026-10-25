"""Captured source-native nickname plus literal as one strict page; no fixed name."""
import struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,pixels
from report_roll_pet_license import literal_end
def name_page(path,step,key,requested,m,rom,e,streams,pool,unit_asset='gutsman_pet_talk_ko.json'):
    cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(path/(cp+'_roll_pet.json'))
    if ram[0xFA21]!=requested or struct.unpack_from('<I',ram,0xFA50)[0]!=pool:raise ValueError('active nickname page')
    last={d['stream']:d for d in obs['draws'] if d['stream'] in streams[key]}
    if set(last)!=set(streams[key]):raise ValueError('complete nickname page literal')
    native=sorted({d['stream']:d for d in read(path/(cp+'_return_ram.json'))['draws']}.values(),key=lambda d:d['stream'])
    if not 1<=len(native)<=16 or ram[native[0]['stream']-0x2000000+len(native)]!=0xe5:raise ValueError('captured nickname span/terminator')
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1};native_advance=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    expected=dict(e);width=0;name=''
    for i,d in enumerate(native):
        index=ram[d['stream']-0x2000000];record=source[0x608758+index*96:0x608758+(index+1)*96];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
        if d['stream']!=native[0]['stream']+i or d['glyph_index']!=index or d['offset']!=width*4 or d['context']!=0x0200FA20 or index not in codes or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,native_advance+index*4)[0]:raise ValueError('native nickname source/font/geometry')
        expected[d['stream']]=dict(ch='native nickname',index=index,record=record,id='native_RAM_nickname');width+=advance;name+=codes[index]
    unit=next(u for u in read(ROOT/'translations'/unit_asset)['units'] if u['id']==key);row=0;advance=width;it=iter(streams[key])
    if unit['source'].split('\n')[0]!='、' or unit['translation'].split('\n')[0]!='、':raise ValueError('nickname suffix first line')
    for ch in unit['translation']:
        if ch=='\n':row+=1;advance=0;continue
        stream=next(it)
        if last[stream]['offset']!=row*10752+advance*4 or last[stream]['context']!=0x0200FA20:raise ValueError('combined nickname literal geometry')
        advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
        if advance>132:raise ValueError('combined nickname line overflow')
    end=literal_end(rom,streams[key],e)
    if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x8000000:end-0x8000000+3]!=bytes.fromhex('e600f1'):raise ValueError('nickname keyWait boundary')
    draws=[last[x] for x in streams[key]]+native;counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('nickname CPU glyph reads')
    proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');occupied=set()
    for d in draws:
        row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
    a,b,k=struct.unpack_from('<HHH',(path/(cp+'_gbaSpriteRam.bin')).read_bytes(),0);arrow=set()
    if k&1023==1016 and k>>12==14:
        if (a,b)!=(141,16609):raise ValueError('unknown nickname wait arrow')
        arrow={(x,y) for y in range(141,157) for x in range(225,240)}
    if occupied&arrow:raise ValueError('nickname glyph footprint/native arrow overlap')
    baseline=Image.open(ROOT/'poc/runtime/numberman-intro-v1-select-numberman-full/step_008.png').convert('RGB')
    if any(im.getpixel((x,y))!=baseline.getpixel((x,y)) for y in range(110,140) for x in [234,235]):raise ValueError('nickname page right border')
    blank={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied|arrow}
    if any(im.getpixel(xy)!=im.getpixel((231,112)) for xy in blank):raise ValueError('nickname vacant page clearing')
    return dict(unit=key,step=step,route=path.name,native_nickname=name,nickname_width=width,native_nickname_bytes=ram[native[0]['stream']-0x2000000:native[0]['stream']-0x2000000+len(native)+1].hex(),wait_cursor=end,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**proof)
