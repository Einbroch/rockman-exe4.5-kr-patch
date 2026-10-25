"""Pinned64x8 same-slot save title using the existing licensed pixel font."""
import json
from build_visibility_poc import ROOT,sha
from pet_graphics_font import SOURCE_SHA,glyphs
BASE=0x6333A4
DIGEST='f4807ae7a8c34336901a3715b2042505b7f817a953b30f89be3cc8626e9cf7a1'

def decode(block):
    if len(block)!=256:raise ValueError('title tile extent')
    return [[(block[x//8*32+y*4+x%8//2]>>(4*(x%2)))&15 for x in range(64)] for y in range(8)]

def encode(rows):
    if len(rows)!=8 or any(len(r)!=64 for r in rows):raise ValueError('title canvas')
    block=bytearray(256)
    for y,row in enumerate(rows):
        for x,role in enumerate(row):
            if role not in (0,15):raise ValueError('title palette role')
            block[x//8*32+y*4+x%8//2]|=role<<(4*(x%2))
    return bytes(block)

def construct(source,asset):
    if sha(source)!=SOURCE_SHA or asset['source_sha256']!=SOURCE_SHA or asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False:raise ValueError('source/policy')
    if (asset['source_offset'],asset['bytes'],asset['source_block_sha256'])!=(BASE,256,DIGEST) or (asset['source'],asset['translation'],asset['state'])!=('セーブ','저장','needs_review') or asset['canvas']!=[64,8] or asset['edit_rect']!=[21,0,23,8] or asset['roles']!={'background':0,'ink':15}:raise ValueError('title scope')
    old=source[BASE:BASE+256]
    if sha(old)!=DIGEST:raise ValueError('source title')
    rows=decode(old)
    if encode(rows)!=old or any(value and not 21<=x<44 for row in rows for x,value in enumerate(row)):raise ValueError('source text/background boundary')
    font_path=ROOT/asset['font_asset'];font=json.loads(font_path.read_text(encoding='utf-8'));g=glyphs(font);new=[r.copy() for r in rows]
    for row in new:row[21:44]=[0]*23
    for i,ch in enumerate('저장'):
        gl=g[ch]
        for y,bits in enumerate(gl['bits']):
            for x in range(gl['width']):
                if bits&(1<<(7-x)):
                    px=24+i*8+gl['xoff']+x;py=gl['top']+y
                    if not(21<=px<44 and 0<=py<8):raise ValueError('title glyph overflow')
                    new[py][px]=15
    if any(new[y][x]!=rows[y][x] for y in range(8) for x in range(64) if not 21<=x<44):raise ValueError('protected title pixels')
    block=encode(new)
    if decode(block)!=new:raise ValueError('modified title roundtrip')
    return block,dict(asset,final_block_sha256=sha(block),font_asset_sha256=sha(font_path.read_bytes()),unchanged_roundtrip=True,protected_pixels_equal=True,translated_graphic_labels=1,runtime='pending normal same-ROM save loader')
