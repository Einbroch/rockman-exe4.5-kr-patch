"""Same-slot native 21-name OBJ bank; no loader, palette or selection edits."""
import json,re,struct
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import lz77_decompress
from lz10_optimal import encode
from startup_footer_graphics import FONT_SHA

BASE=0x639208
STORED=1045
DIGEST='5bbe6f4b6e224c43e8d4cf16b62930e764cf3604d439feebc00deabbcd5ebeb2'
NAMES=['록맨','롤','거츠맨','윈드맨','서치맨','파이어맨','썬더맨','브루스','넘버맨','메탈맨','정크맨','아쿠아맨','우드맨','스타맨','섀도맨','나이트맨','네이팜맨','아이스맨','일렉맨','플랜트맨','포르테']

def pixels(payload,index):
    return [[(payload[4+index*128+(x//8)*32+y*4+x%8//2]>>(4*(x%2)))&15 for x in range(32)] for y in range(8)]

def construct(source,asset):
    if sha(source)!='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8':raise ValueError('Navi source identity')
    if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False or asset['names']!=NAMES or asset['font_sha256']!=FONT_SHA:raise ValueError('Navi wording/font/policy')
    old=source[BASE:BASE+STORED]
    if sha(old)!=DIGEST:raise ValueError('Navi compressed source extent')
    payload,used=lz77_decompress(old,0)
    if used!=STORED or len(payload)!=2692 or payload[:4]!=bytes.fromhex('00840a00'):raise ValueError('Navi bank population/header')
    refs=[m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+BASE)),source)]
    if refs!=[0x39760]:raise ValueError('Navi source references')
    if set(v for b in payload[4:] for v in (b&15,b>>4))!={0,5,6,12}:raise ValueError('Navi palette roles')
    font=ROOT/asset['font'];require_hash(font,FONT_SHA);wanted=set(''.join(NAMES));glyphs={}
    for block in font.read_text(encoding='utf8').split('STARTCHAR ')[1:]:
        ch=chr(int(re.search(r'^ENCODING (\d+)',block,re.M)[1]))
        if ch not in wanted:continue
        w,h,dx,dy=map(int,re.search(r'^BBX (.*)',block,re.M)[1].split())
        rows=[int(s,16) for s in block.split('BITMAP\n')[1].split('ENDCHAR')[0].strip().splitlines()]
        if w>7 or h>7 or dx!=0 or dy<0 or h+dy>7 or len(rows)!=h:raise ValueError('Navi glyph boundary')
        glyphs[ch]=(w,h,dy,rows)
    if set(glyphs)!=wanted:raise ValueError('Navi missing font glyph')
    final=bytearray(payload[:4]);records=[]
    for i,text in enumerate(NAMES):
        rows=[[0]*32 for _ in range(8)];ink=set();pen=(32-8*len(text))//2
        for ch in text:
            w,h,dy,bitmap=glyphs[ch]
            for y,bits in enumerate(bitmap):
                for x in range(w):
                    if bits&(1<<(7-x)):ink.add((pen+x,7-h-dy+y))
            pen+=8
        for x,y in ink:
            for dx,dy in [(1,0),(0,1),(1,1)]:
                if not(0<=x+dx<32 and 0<=y+dy<8):raise ValueError('Navi shadow overflow')
                rows[y+dy][x+dx]=12
        for x,y in ink:rows[y][x]=6
        packed=bytearray(128)
        for y in range(8):
            for x in range(32):packed[(x//8)*32+y*4+x%8//2]|=rows[y][x]<<(4*(x%2))
        final.extend(packed)
        if pixels(final,i)!=rows:raise ValueError('Navi tile roundtrip')
        records.append(dict(index=i,translation=text,tile_base=640+4*i,payload_offset=4+i*128,bytes=128))
    if final[:4]!=payload[:4] or len(final)!=len(payload):raise ValueError('Navi protected header/capacity')
    packed=encode(bytes(final),stored_limit=STORED);padded=packed+bytes(STORED-len(packed))
    if lz77_decompress(padded,0)[0]!=final:raise ValueError('Navi compressed roundtrip')
    return padded,dict(source_offset=BASE,bytes=STORED,source_sha256=DIGEST,target_sha256=sha(padded),payload_sha256=sha(final),compressed_bytes=len(packed),payload_bytes=len(final),records=records,native_references=refs,native_vram_offset=0x15000,native_palette=13,loader_palette_selection_unchanged=True,runtime_verified=False)

if __name__=='__main__':
    source=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
    print(json.dumps(construct(source,json.loads((ROOT/'translations/navi_card_graphics_ko.json').read_text(encoding='utf8')))[1],ensure_ascii=False,indent=2))
