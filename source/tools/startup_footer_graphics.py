"""Same-size native OBJ footer labels; no sprite metadata or input changes."""
import re
from build_visibility_poc import ROOT,sha,require_hash

OFFSET=0x539E54
SIZE=1120
SOURCE_SHA='d72010dbe85c194431e93d21670f4edd11dba15f7759d2c1a10e426415cb44e1'
FONT_SHA='2a6fd090ac6d24f7392d6cc49db02ce54b9d1c01048bf8c97cbcdbc5a885cb15'
# Native one-dimensional OBJ tile order, observed in normal date-input OAM.
SPRITES=[(36,105,16,0),(36,121,8,4),(52,113,8,5),(60,113,8,6),(68,105,16,7),(84,113,8,11),(92,105,16,12),(116,105,16,16),(132,113,8,20),(140,105,16,21),(156,113,8,25),(164,105,16,26),(180,113,8,30),(188,105,16,31)]
RECTS=[(60,105,52,16),(140,105,24,16),(188,105,16,16)]

def locations():
    result={}
    for sx,sy,width,base in SPRITES:
        for y in range(width):
            for x in range(width):
                at=(base+(y//8)*(width//8)+x//8)*32+(y%8)*4+(x%8)//2
                if (sx+x,sy+y) in result:raise ValueError('overlapping native footer sprites')
                result[sx+x,sy+y]=(at,4*(x%2))
    if len(result)!=35*64:raise ValueError('footer tile population')
    return result

def construct(source,asset):
    bank=source[OFFSET:OFFSET+SIZE]
    if sha(bank)!=SOURCE_SHA:raise ValueError('footer immutable tile bank')
    if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False or asset['font_sha256']!=FONT_SHA:raise ValueError('footer input policy')
    lines=[u['translation'] for u in asset['units']]
    if lines!=['늘림·줄임','다음','뒤로']:raise ValueError('footer selected wording')
    font=ROOT/asset['font'];require_hash(font,FONT_SHA)
    selected=set(''.join(lines));glyphs={}
    for block in font.read_text(encoding='utf8').split('STARTCHAR ')[1:]:
        code=int(re.search(r'^ENCODING (\d+)',block,re.M)[1]);ch=chr(code)
        if ch not in selected:continue
        width,height,dx,dy=map(int,re.search(r'^BBX (.*)',block,re.M)[1].split())
        advance=int(re.search(r'^DWIDTH (\d+)',block,re.M)[1])
        rows=[int(s,16) for s in block.split('BITMAP\n')[1].split('ENDCHAR')[0].strip().splitlines()]
        if len(rows)!=height or width>8 or height>8 or dx<0 or dy<0:raise ValueError('footer glyph native cell bounds')
        glyphs[ch]=(width,height,dx,dy,advance,rows)
    if set(glyphs)!=selected:raise ValueError('missing footer glyph')
    loc=locations();pixels={p:(bank[a]>>s)&15 for p,(a,s) in loc.items()};target=dict(pixels)
    editable={p for p in pixels if any(x<=p[0]<x+w and y<=p[1]<y+h for x,y,w,h in RECTS)}
    for p in editable:target[p]=0
    for line,(x,y,w,h) in zip(lines,RECTS):
        advance=sum(glyphs[ch][4] for ch in line)
        if advance>w:raise ValueError('footer line overflow')
        pen=x+(w-advance)//2
        for ch in line:
            gw,gh,dx,dy,step,rows=glyphs[ch]
            for gy,row in enumerate(rows):
                for gx in range(gw):
                    if row&(1<<(7-gx)):
                        p=(pen+dx+gx,113+7-gh-dy+gy)
                        if p not in editable:raise ValueError('footer glyph outside edit mask')
                        target[p]=9 # Existing dark footer-text palette index; icons untouched.
            pen+=step
    out=bytearray(bank)
    for p,(a,s) in loc.items():out[a]=(out[a]&~(15<<s))|(target[p]<<s)
    if any(target[p]!=pixels[p] for p in pixels if p not in editable):raise ValueError('footer protected pixels changed')
    if any(((out[a]>>s)&15)!=target[p] for p,(a,s) in loc.items()):raise ValueError('footer native tile roundtrip')
    return bytes(out),dict(source_offset=OFFSET,bytes=SIZE,source_sha256=SOURCE_SHA,target_sha256=sha(out),editable_rects=RECTS,protected_pixels_identical=True,native_sprite_metadata_unchanged=True,native_palette_unchanged=True,observed_native_vram_offset=0x15200,runtime_verified=False)
