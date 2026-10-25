"""Deterministic approved pixel-font typography, preserving native OBJ framing."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from prepare_pet_graphics_v2 import BASE,TILES,decode,encode

SOURCE_SHA='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'
BLOCK_SHA='915d5ef52fa9ca70e1149a196187e60423a1dd30419376fde45c1eef8e193389'
WORDS=['토너먼트','플러그인','장비','데이터 라이브러리','메일','통신','저장']

def glyphs(asset,extra_characters=''):
    font=asset['font']
    require_hash(ROOT/font['path'],font['sha256']);require_hash(ROOT/font['license'],font['license_sha256'])
    wanted=set(''.join(WORDS)+'동'+extra_characters);out={}
    for b in (ROOT/font['path']).read_text().split('STARTCHAR ')[1:]:
        lines=b.splitlines();cp=int(next(l.split()[1] for l in lines if l.startswith('ENCODING ')));ch=chr(cp)
        if ch not in wanted:continue
        w,h,xoff,yoff=map(int,next(l for l in lines if l.startswith('BBX ')).split()[1:]);start=lines.index('BITMAP')+1
        bits=[int(l,16) for l in lines[start:start+h]];top=8-h-yoff
        if w>7 or h>8 or xoff<0 or top<0 or top+h>8:raise ValueError('small glyph does not fit:'+ch)
        out[ch]={'width':w,'height':h,'xoff':xoff,'top':top,'bits':bits}
    if set(out)!=wanted:raise ValueError('small font glyph missing')
    if out['통']['bits']!=[0x7C,0x78,0x7C,0x10,0xFE,0x44,0x38] or out['통']==out['동']:raise ValueError('Tong/Dong glyph distinction')
    override=asset.get('glyph_overrides',{})
    if set(override)!={'통'} or any(override['통'].get(k)!=v for k,v in {'width':7,'height':8,'top':0,'bits':[124,120,64,124,16,254,68,56]}.items()):raise ValueError('adopted project Tong profile')
    out['통']=dict(out['통'],width=7,height=8,top=0,bits=override['통']['bits'])
    return out

def construct(source,asset):
    if sha(source)!=SOURCE_SHA or asset['source_sha256']!=SOURCE_SHA or asset['policy']!='development-draft; NON-DISTRIBUTION':raise ValueError('PET asset source/policy')
    if (asset['source_offset'],asset['bytes'],asset['source_block_sha256'])!=(BASE,0x1200,BLOCK_SHA):raise ValueError('PET graphics boundary')
    block=source[BASE:BASE+0x1200]
    if sha(block)!=BLOCK_SHA:raise ValueError('PET source block mismatch')
    if len(asset['units'])!=7 or [u['translation'] for u in asset['units']]!=WORDS or [tuple(u['tiles']) for u in asset['units']]!=TILES:raise ValueError('PET label identity/wording')
    g=glyphs(asset);target=bytearray(block);records=[];allowed=set()
    for row,u in enumerate(asset['units']):
        left,right=u['tiles'];advance=u['advance']
        if advance!=(7 if row==3 else 8):raise ValueError('PET adopted glyph spacing')
        original=decode(block,left,right);pixels=[list(r) for r in original];rt=bytearray(block);encode(rt,original,left,right)
        if rt!=block:raise ValueError('PET unchanged roundtrip')
        for y in range(1,9):
            for x in range(1,64):
                if pixels[y][x] not in (1,4):raise ValueError('PET clean background role')
                pixels[y][x]=1
                tile=(left,right)[x//32]+y//8*4+(x%32)//8
                allowed.add((tile-0x80)*32+(y%8)*4+(x%8)//2)
        pen=0;points=[];chars=[]
        for ch in u['translation']:
            glyph=g[ch];chars.append({'character':ch,'pen':pen,'glyph_sha256':sha(bytes(glyph['bits']))})
            for y,bits in enumerate(glyph['bits']):
                for x in range(glyph['width']):
                    if bits&(1<<(8*((glyph['width']+7)//8)-1-x)):points.append((pen+glyph['xoff']+x,glyph['top']+y))
            pen+=3 if ch==' ' else advance
        width=max(x for x,y in points)+1
        if width>63:raise ValueError('PET lettering overflow')
        x0=max(1,(64-width)//2)
        for x,y in points:pixels[y+1][x+x0]=4
        for y in range(16):
            for x in range(64):
                if not(1<=x<64 and 1<=y<9) and original[y][x]!=pixels[y][x]:raise ValueError('PET protected pixel')
        encode(target,pixels,left,right)
        records.append(dict(u,ink_width=width,x0=x0,glyphs=chars,pixel_sha256=sha(bytes(c for r in pixels for c in r))))
    if any(a!=b and i not in allowed for i,(a,b) in enumerate(zip(block,target))):raise ValueError('PET outside tile write')
    record={'source_offset':BASE,'bytes':len(block),'source_block_sha256':BLOCK_SHA,'final_block_sha256':sha(target),
        'font':asset['font'],'glyph_overrides':asset['glyph_overrides'],'units':records,'unchanged_roundtrip':True,'protected_pixels_equal':True,
        'palette_roles':[1,4],'glyphs_unscaled':True,'translated_graphic_labels':7,'runtime':'pending exact-ROM cold-chain',
        'review':'needs_review','release_eligible':False}
    return bytes(target),record

def main():
    import struct
    from PIL import Image
    asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];target,record=construct(source.read_bytes(),asset)
    out=ROOT/'analysis/pet_font_v2'
    if out.exists():raise ValueError('fresh preview directory required')
    out.mkdir();palette=(ROOT/'poc/runtime/roll-tactics-v1-cold-part2/step_040_gbaPaletteRam.bin').read_bytes();img=Image.new('RGBA',(64,112))
    for row,(left,right) in enumerate(TILES):
        pixels=decode(target,left,right)
        for y,r in enumerate(pixels):
            for x,role in enumerate(r):
                raw=struct.unpack_from('<H',palette,0x200+9*32+role*2)[0]
                img.putpixel((x,row*16+y),tuple(((raw>>s)&31)*255//31 for s in (0,5,10))+(255 if role else 0,))
    img.save(out/'labels_native.png');img.resize((512,896),Image.Resampling.NEAREST).save(out/'labels_8x.png')
    (out/'prepared.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
