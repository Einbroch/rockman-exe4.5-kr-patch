"""Translate native kana command graphics without replacing the keyboard."""
import json,re,struct
from build_visibility_poc import ROOT,sha,require_hash
from prepare_keyboard_page_graphics import decode,encode
from startup_footer_graphics import FONT_SHA

PAGES=[(6532084,9600,'252d6a507a5efdc4117bf6d5dfa75af938364a9ada89163a2aec711ee8f43fba',6558420,'ff5b7486a23a05cfb4bccaacbcd0ab22e6fab58c8336370c2f0551937419d775'),(6541684,9440,'d14b8fbfd26d5a8c6e346ca3a5cf3bdde6469fa95c98f34152e9c61772965586',6559620,'27411505b1701ef4f19977faf198d7f3d61bbef43e5f787b428e888508d4abab'),(6551124,7232,'b31250a37f65b9059dcaf958378ed8c5001123405ccd188df034d5d664fed58e',6560820,'5fd390a1db1be4bd5c0e0edc7eed820b6e3904a21e19e3f3b6b9306e43da8103')]
LABELS=[['가타카나','기호','오른쪽','왼쪽','공백','확인'],['히라가나','기호','오른쪽','왼쪽','공백','확인'],['히라가나','가타카나','오른쪽','왼쪽','공백','확인']]

def construct(source,asset):
    if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False or asset['pages']!=LABELS or asset['font_sha256']!=FONT_SHA:raise ValueError('native command input policy/wording')
    font=ROOT/asset['font'];require_hash(font,FONT_SHA);wanted=set(''.join(''.join(p) for p in LABELS));glyphs={}
    for block in font.read_text(encoding='utf8').split('STARTCHAR ')[1:]:
        ch=chr(int(re.search(r'^ENCODING (\d+)',block,re.M)[1]))
        if ch not in wanted:continue
        w,h,dx,dy=map(int,re.search(r'^BBX (.*)',block,re.M)[1].split())
        rows=[int(s,16) for s in block.split('BITMAP\n')[1].split('ENDCHAR')[0].strip().splitlines()]
        if w>7 or h>7 or dx!=0 or dy<0 or h+dy>7 or len(rows)!=h:raise ValueError('native command glyph boundary')
        glyphs[ch]=(w,h,dy,rows)
    if set(glyphs)!=wanted:raise ValueError('native command missing glyph')
    patches=[];records=[]
    for page,(at,n,bh,mp,mh) in enumerate(PAGES):
        bank=source[at:at+n];mapping=source[mp:mp+1200]
        if sha(bank)!=bh or sha(mapping)!=mh:raise ValueError('native page source identity')
        descriptor=0x356E8+page*16;mapref=0x356C0+page*4
        if struct.unpack_from('<4I',source,descriptor)!=(0x08000000+at,0x06008000,n,0) or struct.unpack_from('<I',source,mapref)[0]!=0x08000000+mp:raise ValueError('native page load descriptor')
        for target,refs in [(at,[descriptor]),(mp,[mapref])]:
            if [m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+target)),source)]!=refs:raise ValueError('native page reference population')
        original=decode(bank,mapping);reb,m=encode(original)
        if decode(reb,m)!=original:raise ValueError('native page unchanged roundtrip')
        pixels=[r[:] for r in original]
        for row,text in enumerate(LABELS[page]):
            y0=56+16*row;pen=196+(28-7*len(text))//2
            for y in range(y0,y0+16):
                for x in range(196,224):
                    bg=5 if (x+y)%4==3 else 9;v=original[y][x]
                    if v not in (5,8,9,11) or v in (5,9) and v!=bg:raise ValueError('native command background classification')
                    pixels[y][x]=bg
            for ch in text:
                w,h,dy,rows=glyphs[ch]
                for y,bits in enumerate(rows):
                    for x in range(w):
                        if bits&(1<<(7-x)):pixels[y0+4+7-h-dy+y][pen+x]=11
                pen+=7
        if any(pixels[y][x]!=original[y][x] for y in range(160) for x in range(240) if not(196<=x<224 and 56<=y<152)):raise ValueError('native keyboard protected pixel changed')
        reb,newmap=encode(pixels)
        if len(reb)>n:raise ValueError('native keyboard tile slot overflow')
        newbank=reb+bytes(n-len(reb))
        if decode(newbank,newmap)!=pixels:raise ValueError('native keyboard final pixel roundtrip')
        patches.extend([(at,newbank,f'native keyboard page{page} Korean command tiles'),(mp,newmap,f'native keyboard page{page} reindexed map')])
        records.append(dict(page=page,bank_offset=at,bank_bytes=n,map_offset=mp,map_bytes=1200,descriptor_offset=descriptor,map_reference=mapref,source_bank_sha256=bh,source_map_sha256=mh,target_bank_sha256=sha(newbank),target_map_sha256=sha(newmap),used_tiles=len(reb)//32,labels=LABELS[page],protected_pixels_identical=True))
    return patches,dict(pages=records,editable_rect=[196,56,28,96],native_input_and_save_unchanged=True,slot_sizes_and_descriptors_unchanged=True,runtime_verified=False)
