"""Graphic-label fixes after stage 066 (graphics_fix_v1 is frozen with the 066 build).

* PET top-bar weekday boxes "(日)".."(土)" (raw strips 0x632DA4/0x632EA4, also the schedule screen date): the
  kanji between the bracket strokes is redrawn with the Galmuri7 일..토 glyphs.
Pending: calendar weekday header (tileset 0x63756C, 95 tiles all in use + raw 30-wide map 0x63818C; tiles 8 and 9
are shared by two weekdays, so it needs two more tiles and a changed load size).
"""
from build_visibility_poc import ROOT
from pet_graphics_font import glyphs
from graphics_fix_v1 import strip_rows,strip_bytes
import json

# PET top-bar weekday boxes "(日)" (same raw strip format as the title strips, ink 15): 0x632DA4 x16/32/48 =
# 日月火, 0x632EA4 x0/16/32/48 = 水木金土. Only the columns between the two bracket strokes are redrawn.
WEEKDAY_REGION=(0x632DA4,0x632FA4)
WEEKDAY_BOXES=[(0x632DA4,16,'日','일'),(0x632DA4,32,'月','월'),(0x632DA4,48,'火','화'),(0x632EA4,0,'水','수'),(0x632EA4,16,'木','목'),(0x632EA4,32,'金','금'),(0x632EA4,48,'土','토')]


def weekdays(source,prev):
    lo,hi=WEEKDAY_REGION
    if prev[lo:hi]!=source[lo:hi]:raise ValueError('PET weekday strips already modified')
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    g=glyphs(asset,extra_characters='일월화수목금토');out=bytearray(prev[lo:hi]);strips={}
    for base,bx,ja,ko in WEEKDAY_BOXES:
        rows=strips.setdefault(base,strip_rows(out[base-lo:base-lo+256]))
        cols=[x for x in range(bx,bx+16) if any(rows[y][x] for y in range(2,7))]
        left,right=min(cols)+2,max(cols)-2               # 1-px bracket stroke whose curl reaches one more column
        if any(rows[y][left-2]==0 or rows[y][right+2]==0 for y in range(2,7)):raise ValueError('weekday bracket shape '+ja)
        for y in range(8):
            for x in range(left,right+1):rows[y][x]=0
        gl=g[ko];w=gl['xoff']+gl['width'];x0=left+(right-left+1-w)//2;y0=8-len(gl['bits'])
        if x0<left or x0+w-1>right:raise ValueError('weekday glyph width '+ko)
        for y,bits in enumerate(gl['bits']):
            for x in range(gl['width']):
                if bits&(1<<(8*((gl['width']+7)//8)-1-x)):rows[y0+y][x0+gl['xoff']+x]=15
    for base,rows in strips.items():out[base-lo:base-lo+256]=strip_bytes(rows)
    return bytes(out)


def patches(source,prev):
    """[(offset, final_bytes, reason)] relative to the predecessor ROM image."""
    return [(WEEKDAY_REGION[0],weekdays(source,prev),'PET top-bar weekday boxes')]
