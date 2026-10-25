"""Graphic-label fixes from user screenshots (2026-10-25), as whole-region final bytes over a predecessor ROM.

* Date-input footer (OBJ bank 0x539E54, 1120 bytes): the first kana of each old word (ふ/つ/も) sat alone in
  the 8x8 cells at x=52/132/180, y=113, outside the old edit rectangles; those three cells are cleared.
  The ellipsis dots live in the icon sprites and are untouched.
* Plugged-in PET menu buttons サブチップ / キーアイテム (raw OBJ tiles after the 7-button block 0x6303B8):
  redrawn as 서브칩 / 키 아이템 with the same Galmuri7 glyphs, roles (bg 1, ink 4) and centring rules as
  pet_graphics_font.construct; frame pixels outside rows 1..8 / columns 1..63 are protected.
"""
from build_visibility_poc import ROOT,sha
from startup_footer_graphics import OFFSET as FOOTER,SIZE as FOOTER_SIZE,locations
from prepare_pet_graphics_v2 import BASE,decode,encode
from pet_graphics_font import glyphs
import json

PET_REGION=(0x6317B8,0x631CB8)                 # tiles 0x80+0xA0 .. ; contains both plugged-in buttons
PET_UNITS=[dict(id='pet.obj.subchip',source='サブチップ',translation='서브칩',tiles=(292,300),advance=8),
           dict(id='pet.obj.keyitem',source='キーアイテム',translation='키 아이템',tiles=(324,316),advance=8)]


def footer(prev):
    bank=bytearray(prev[FOOTER:FOOTER+FOOTER_SIZE]);loc=locations()
    for sx in (52,132,180):
        for x in range(8):
            for y in range(8):
                a,s=loc[(sx+x,113+y)];bank[a]&=~(15<<s)
    return bytes(bank)


def pet(source,prev):
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    g=glyphs(asset,extra_characters=''.join(u['translation'] for u in PET_UNITS))
    span=0x1A00;block=bytearray(prev[BASE:BASE+span])
    if source[PET_REGION[0]:PET_REGION[1]]!=prev[PET_REGION[0]:PET_REGION[1]]:raise ValueError('plugged-in PET buttons already modified')
    allowed=set()
    for u in PET_UNITS:
        left,right=u['tiles'];original=decode(bytes(block),left,right);pixels=[list(r) for r in original]
        for y in range(1,9):
            for x in range(1,64):
                if pixels[y][x] not in (1,4):raise ValueError('PET clean background role '+u['id'])
                pixels[y][x]=1;tile=(left,right)[x//32]+y//8*4+(x%32)//8;allowed.add((tile-0x80)*32+(y%8)*4+(x%8)//2)
        pen=0;points=[]
        for ch in u['translation']:
            gl=g[ch]
            for y,bits in enumerate(gl['bits']):
                for x in range(gl['width']):
                    if bits&(1<<(8*((gl['width']+7)//8)-1-x)):points.append((pen+gl['xoff']+x,gl['top']+y))
            pen+=3 if ch==' ' else u['advance']
        width=max(x for x,_ in points)+1;x0=max(1,(64-width)//2)
        for x,y in points:pixels[y+1][x+x0]=4
        for y in range(16):
            for x in range(64):
                if not(1<=x<64 and 1<=y<9) and original[y][x]!=pixels[y][x]:raise ValueError('PET protected pixel')
        encode(block,pixels,left,right)
    out=bytes(block[PET_REGION[0]-BASE:PET_REGION[1]-BASE])
    old=prev[PET_REGION[0]:PET_REGION[1]]
    if any(a!=b and (PET_REGION[0]-BASE+i) not in allowed for i,(a,b) in enumerate(zip(old,out))):raise ValueError('PET write outside label rows')
    return out


# PET sub-screen title strips: 8 raw 4bpp OBJ tiles (64x8, ink 15 on 0) each, shown as two 32x8 sprites.
HEADER_BASE=0x632FA4
HEADERS=[('データライブラリ','데이터라이브러리'),('そうび',None),('Eメール','메일'),('つうしん','통신'),('セーブ',None),('キーアイテム','키 아이템'),('サブチップ','서브칩')]
EQUIP_RESIDUE=range(44,64)    # the 장비 strip (folder_labels.title) kept び's dakuten at x=45


def strip_rows(b):return [[(b[(x//8)*32+y*4+(x%8)//2]>>(4*(x&1)))&15 for x in range(64)] for y in range(8)]


def strip_bytes(rows):
    out=bytearray(256)
    for y in range(8):
        for x in range(64):out[(x//8)*32+y*4+(x%8)//2]|=rows[y][x]<<(4*(x&1))
    return bytes(out)


def headers(source,prev):
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    g=glyphs(asset,extra_characters=''.join(t for _,t in HEADERS if t))
    out=bytearray(prev[HEADER_BASE:HEADER_BASE+256*len(HEADERS)])
    for i,(ja,ko) in enumerate(HEADERS):
        o=HEADER_BASE+256*i;old=strip_rows(prev[o:o+256])
        if strip_bytes(old)!=prev[o:o+256]:raise ValueError('header roundtrip '+ja)
        if ko is None:
            if ja=='そうび':
                new=[[0 if x in EQUIP_RESIDUE else v for x,v in enumerate(r)] for r in old]
                if not any(old[y][x] for y in range(8) for x in EQUIP_RESIDUE):raise ValueError('equip residue gone')
                out[256*i:256*i+256]=strip_bytes(new)
            continue
        if prev[o:o+256]!=source[o:o+256]:raise ValueError('header already modified '+ja)
        pen=0;points=[]
        for ch in ko:
            gl=g[ch]
            for y,bits in enumerate(gl['bits']):
                for x in range(gl['width']):
                    if bits&(1<<(8*((gl['width']+7)//8)-1-x)):points.append((pen+gl['xoff']+x,gl['top']+y))
            pen+=3 if ch==' ' else 8
        width=max(x for x,_ in points)+1;x0=(64-width)//2
        new=[[0]*64 for _ in range(8)]
        for x,y in points:
            if not(0<=x+x0<64 and 0<=y<8):raise ValueError('header glyph overflow '+ko)
            new[y][x+x0]=15
        out[256*i:256*i+256]=strip_bytes(new)
    return bytes(out)


# Battle result windows RESULT / WINNER / LOSER (code 0x226FC/0x22734): raw 4bpp tile bank per window copied to
# 0x06008020 (tile 1..), raw 24x17 map, palette 9. Labels are two-row bands (fill tiles at column 13); dakuten
# stick into the bottom pixel row of the border rows above (ink 13 on 3). Digits are written into rows 3/6 from
# column 13 at runtime, so the redraw stays in columns 3..12 / 3..17.
RESULT_REGION=(0x7704A0,0x7734B0)
RESULT_WINDOWS=[(0x7704A0,0xD00,0x772B20),(0x7711A0,0xD00,0x772E50),(0x771EA0,0xC80,0x773180)]
RESULT_LABELS=[dict(source='デリートタイム',text='딜리트 타임',row=3,first=3,last=12),dict(source='バスティングレベル',text='버스팅 레벨',row=6,first=3,last=17)]
RESULT_FONT='external/fonts/Galmuri11-Condensed-v2.40.4.bdf'   # 8px advance: regular Galmuri11 needs 36 tiles, pools are 29..30
INK,SHADOW,BG=13,14,3


def bdf(path,text):
    out={}
    for b in (ROOT/path).read_text(encoding='utf-8').split('STARTCHAR ')[1:]:
        lines=b.splitlines();ch=chr(int(next(l.split()[1] for l in lines if l.startswith('ENCODING '))))
        if ch not in text:continue
        w,h,xo,yo=map(int,next(l for l in lines if l.startswith('BBX ')).split()[1:]);adv=int(next(l for l in lines if l.startswith('DWIDTH ')).split()[1])
        s=lines.index('BITMAP')+1;bits=[int(l,16) for l in lines[s:s+h]]
        out[ch]=dict(adv=adv,ink={(x+xo,y+(11-h-yo)) for y,r in enumerate(bits) for x in range(w) if r&(1<<(((w+7)//8)*8-1-x))})
    if set(out)!=set(text):raise ValueError('result font glyph missing')
    return out


def result_windows(source,prev):
    lo,hi=RESULT_REGION
    if prev[lo:hi]!=source[lo:hi]:raise ValueError('result windows already modified')
    font=bdf(RESULT_FONT,''.join(l['text'] for l in RESULT_LABELS));out=bytearray(prev[lo:hi]);report=[]
    for tb,size,mo in RESULT_WINDOWS:
        tiles=bytearray(prev[tb:tb+size]);mp=bytearray(prev[mo:mo+816]);n=size//32
        def ent(r,c):return int.from_bytes(mp[(r*24+c)*2:(r*24+c)*2+2],'little')
        def tpx(t):return [[(tiles[(t-1)*32+y*4+x//2]>>4) if x&1 else tiles[(t-1)*32+y*4+x//2]&15 for x in range(8)] for y in range(8)]
        if any(ent(l['row']+d,c)&0xC00 for l in RESULT_LABELS for d in (-1,0,1) for c in range(l['first'],14)):raise ValueError('flipped result label cell')
        edit={}
        for l in RESULT_LABELS:
            fills=[ent(l['row']+d,13)&1023 for d in (0,1)]
            for d in (0,1):
                if any(ent(l['row']+d,c)&1023!=fills[d] for c in range(l['last']+1,14)):raise ValueError('result label right edge')
            width=(l['last']-l['first']+1)*8;img=[[tpx(fills[y//8])[y%8][x%8] for x in range(width)] for y in range(16)]
            pen=1;ink=set()
            for ch in l['text']:
                g=font[ch];ink|={(x+pen,y+1) for x,y in g['ink']};pen+=g['adv']
            if max(x for x,_ in ink)+2>width or max(y for _,y in ink)+2>13:raise ValueError('result label fit '+l['text'])
            for x,y in ink:
                if (x+1,y+1) not in ink:img[y+1][x+1]=SHADOW
            for x,y in ink:img[y][x]=INK
            for d in (0,1):
                for k in range(l['last']-l['first']+1):edit[(l['row']+d,l['first']+k)]=[row[k*8:k*8+8] for row in img[d*8:d*8+8]]
            for c in range(l['first'],l['last']+1):   # dakuten in the border row above
                p=tpx(ent(l['row']-1,c)&1023)
                if INK in p[7]:edit[(l['row']-1,c)]=p[:7]+[[BG if v==INK else v for v in p[7]]]
        used={}
        for r in range(17):
            for c in range(24):used.setdefault(ent(r,c)&1023,set()).add((r,c))
        pool=sorted(t for t,cells in used.items() if t and cells<=set(edit))
        keep={tuple(map(tuple,tpx(t))):t for t in range(1,n+1) if t not in pool}
        assigned={};free=list(pool)
        for (r,c),cell in sorted(edit.items()):
            key=tuple(map(tuple,cell))
            if key in keep:t=keep[key]
            elif key in assigned:t=assigned[key]
            else:
                if not free:raise ValueError('result tile pool exhausted')
                t=free.pop(0);assigned[key]=t
                for y in range(8):
                    for x in range(0,8,2):tiles[(t-1)*32+y*4+x//2]=cell[y][x]|cell[y][x+1]<<4
            e=ent(r,c);mp[(r*24+c)*2:(r*24+c)*2+2]=((e&~1023)|t).to_bytes(2,'little')
        for t in free:tiles[(t-1)*32:t*32]=bytes(32)
        out[tb-lo:tb-lo+size]=tiles;out[mo-lo:mo-lo+816]=mp
        report.append(dict(window=hex(mo),pool=len(pool),new_tiles=len(assigned)))
    return bytes(out),report


# Profile-topic speech bubbles (sprite file at 0x506C1C, 19 frames; frame records [tileset, palette, minianim,
# objects, 0x00800008] from 0x506C68; objects [tile, x, y, size, shape], 0xFF end). Every frame has its own
# tileset, each tile used once. Text is palette index 7 on bubble index 3; words follow the profile menu
# 7CC6A0:75..92 (こじん is not in that list).
BUBBLE_FILE,BUBBLE_FRAMES,BUBBLE_COUNT=0x506C1C,0x506C68,19
BUBBLE_REGION=(0x506DE4,0x50A610)
# Interiors are 38..46 px; three menu words are shortened here only (좋아하는 사람, TV 프로그램 -> 방송 as in dialogue, 갖고 싶은 것).
BUBBLE_WORDS=['유치원','형·오빠','남동생','누나·언니','여동생','친구','좋아하는 음식','취미','꿈','좋아하는 이','존경하는 사람','불편한 사람','TV 방송','잘하는 과목','어려운 과목','원하는 것','개인','학교','회사']
BUBBLE_SOURCE=['ようちえん','おにいさん','おとうと','おねえさん','いもうと','ともだち','すきなたべもの','しゅみ','ゆめ','すきな人','そんけいする人','にがてな人','TVばんぐみ','とくいかもく','にがてかもく','ほしいもの','こじん','がっこう','かいしゃ']
OBJ_DIM={(0,0):(8,8),(1,0):(16,16),(2,0):(32,32),(0,1):(16,8),(1,1):(32,8),(2,1):(32,16),(0,2):(8,16),(1,2):(8,32),(2,2):(16,32)}
B_TEXT,B_FILL,B_SHADES=7,3,(4,5,7)


def bubbles(source,prev):
    lo,hi=BUBBLE_REGION
    if prev[lo:hi]!=source[lo:hi]:raise ValueError('bubbles already modified')
    def u32(a):return int.from_bytes(prev[a:a+4],'little')
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    g=glyphs(asset,extra_characters=''.join(BUBBLE_WORDS).replace(' ',''))
    out=bytearray(prev[lo:hi]);report=[]
    for k in range(BUBBLE_COUNT):
        t,p,m,o,f=(u32(BUBBLE_FRAMES+20*k+i) for i in range(0,20,4))
        if f!=0x00800008 or p!=0x39F4:raise ValueError('bubble frame record %d'%k)
        tb=BUBBLE_FILE+t+4;size=u32(BUBBLE_FILE+t);a=BUBBLE_FILE+o+u32(BUBBLE_FILE+o);where={};seen=set()
        if not(lo<=tb and tb+size<=hi):raise ValueError('bubble tileset bounds')
        while prev[a]!=0xFF:
            ti,x,y,sz,sh=prev[a],prev[a+1]-256*(prev[a+1]>127),prev[a+2]-256*(prev[a+2]>127),prev[a+3],prev[a+4];a+=5
            w,h=OBJ_DIM[(sz,sh)]
            for ty in range(h//8):
                for tx in range(w//8):
                    tt=ti+ty*(w//8)+tx
                    if tt in seen or (tt+1)*32>size:raise ValueError('bubble tile reuse/bounds')
                    seen.add(tt)
                    for yy in range(8):
                        for xx in range(8):where[(x+tx*8+xx,y+ty*8+yy)]=(tb+tt*32+yy*4+xx//2,4*(xx&1))
        def get(q):b,s=where[q];return (out[b-lo]>>s)&15
        def put(q,v):b,s=where[q];out[b-lo]=(out[b-lo]&~(15<<s))|(v<<s)
        old=[q for q in where if get(q)==B_TEXT]
        if not old:raise ValueError('bubble without text %d'%k)
        x0,x1=min(x for x,_ in old),max(x for x,_ in old);y0,y1=min(y for _,y in old),max(y for _,y in old)
        for q in where:   # text plus its anti-alias shades 4/5 inside the text box
            if x0-1<=q[0]<=x1+1 and y0-1<=q[1]<=y1+1 and get(q) in B_SHADES:put(q,B_FILL)
        def inside(q):return all(z in where and get(z)==B_FILL for z in (q,(q[0]-1,q[1]),(q[0]+1,q[1]),(q[0],q[1]-1),(q[0],q[1]+1)))
        cols=[x for x in range(x0-24,x1+25) if all(inside((x,y)) for y in range(y0,y0+8))]
        x0,x1=min(cols),max(cols)   # centre on the clean interior, not on the old word
        word=BUBBLE_WORDS[k];done=None
        for adv in (8,7):
            pts=[];pen=0
            for ch in word:
                if ch==' ':pen+=3;continue
                gl=g[ch]
                for yy,bits in enumerate(gl['bits']):
                    for xx in range(gl['width']):
                        if bits&(1<<(8*((gl['width']+7)//8)-1-xx)):pts.append((pen+gl['xoff']+xx,gl['top']+yy))
                pen+=adv if '가'<=ch<='힣' else gl['xoff']+gl['width']+1   # narrow Latin/middle dot
            w=max(x for x,_ in pts)+1;top=min(y for _,y in pts);ox=(x0+x1+1-w)//2;oy=y0-top
            q=[(x+ox,y+oy) for x,y in pts]
            if all(inside(z) for z in q):done=(adv,q);break
        if done is None:raise ValueError('bubble word does not fit: '+word)
        for z in done[1]:put(z,B_TEXT)
        report.append(dict(frame=k,source=BUBBLE_SOURCE[k],translation=word,advance=done[0]))
    return bytes(out),report


# Field HUD clock font (raw OBJ tiles, tile 800 = 0x621458, 1D mapping): 月 / 日 are 8x16 cells (tiles 826 / 828,
# blue 0xC in a black 0xB box); weekdays are a 16x16 '(' + kanji sprite followed by an 8x16 ')' sprite, 6 tiles each
# from tile 834 (white 8 in a black box at x 7..16). Galmuri7 glyphs (월/일 6 wide, weekdays <=7) redrawn the same way.
CLOCK_TILE0=0x621458-800*32
CLOCK_REGION=(CLOCK_TILE0+826*32,CLOCK_TILE0+876*32)
CLOCK_UNITS=[('月','월',826,'cell'),('日','일',828,'cell')]+[(j,k,834+6*d,'weekday') for d,(j,k) in enumerate(zip('日月火水木金土','일월화수목금토'))]


def clock(source,prev):
    lo,hi=CLOCK_REGION
    if prev[lo:hi]!=source[lo:hi]:raise ValueError('clock font already modified')
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    g=glyphs(asset,extra_characters='월일화수목금토');out=bytearray(prev[lo:hi])
    def at(t,kind,x,y):
        if kind=='cell':tt=t+y//8
        else:tt=t+(y//8)*2+x//8 if x<16 else t+4+y//8
        return CLOCK_TILE0+tt*32+(y%8)*4+(x%8)//2-lo,4*(x&1)
    def put(t,kind,x,y,v):b,s=at(t,kind,x,y);out[b]=(out[b]&~(15<<s))|(v<<s)
    def get(t,kind,x,y):b,s=at(t,kind,x,y);return (out[b]>>s)&15
    for ja,ko,t,kind in CLOCK_UNITS:
        xa,xb,ink=(0,8,0xC) if kind=='cell' else (7,17,8)
        for y in range(16):
            for x in range(xa,xb):
                if kind=='weekday' and get(t,kind,x,y)==0xC:raise ValueError('clock bracket inside glyph area')
                put(t,kind,x,y,0)
        gl=g[ko];w=gl['xoff']+gl['width'];h=len(gl['bits'])
        x0=xa+1 if kind=='cell' else 8+(7-w)//2;y0=12-h
        pts={(x0+gl['xoff']+x,y0+y) for y,bits in enumerate(gl['bits']) for x in range(gl['width']) if bits&(1<<(8*((gl['width']+7)//8)-1-x))}
        bx0,bx1=min(x for x,_ in pts)-1,max(x for x,_ in pts)+1
        if bx0<xa or bx1>=xb:raise ValueError('clock glyph width '+ko)
        for y in range(y0-1,y0+h+1):
            for x in range(bx0,bx1+1):put(t,kind,x,y,0xB)
        for x,y in pts:put(t,kind,x,y,ink)
    return bytes(out)


def patches(source,prev):
    """[(offset, final_bytes, reason)] relative to the predecessor ROM image."""
    return [(FOOTER,footer(prev),'date-input footer: clear leftover first kana cells'),
            (HEADER_BASE,headers(source,prev),'PET sub-screen title strips 데이터라이브러리/메일/통신/키 아이템/서브칩, 장비 residue'),
            (PET_REGION[0],pet(source,prev),'plugged-in PET menu buttons 서브칩/키 아이템'),
            (RESULT_REGION[0],result_windows(source,prev)[0],'battle result windows 딜리트 타임/버스팅 레벨'),
            (BUBBLE_REGION[0],bubbles(source,prev)[0],'profile-topic speech bubbles (19 words)'),
            (CLOCK_REGION[0],clock(source,prev),'field clock 월/일 and weekdays')]
