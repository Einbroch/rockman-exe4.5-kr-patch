"""Same-slot five frequency OBJ labels using the established unscaled BDF font."""
import json,re,struct
from build_visibility_poc import ROOT,sha
from pet_graphics_font import SOURCE_SHA,glyphs
from verify_tpi_index import lz77_decompress
from lz10_greedy import encode as compress

BASE=0x63673C
STORED=428
WORDS=['1회만','매일','매주','매월','매년']
REFS=[0x327E0,0x32D44,0x33080,0x343E8]

def decode(data):
    if len(data)!=256:raise ValueError('frequency tile size')
    return [[(data[(y//8*4+x//8)*32+y%8*4+x%8//2]>>(4*(x%2)))&15 for x in range(32)] for y in range(16)]

def encode(rows):
    out=bytearray(256)
    if len(rows)!=16 or any(len(r)!=32 for r in rows):raise ValueError('canvas')
    for y,row in enumerate(rows):
        for x,v in enumerate(row):
            if not 0<=v<16:raise ValueError('role')
            out[(y//8*4+x//8)*32+y%8*4+x%8//2]|=v<<(4*(x%2))
    return bytes(out)

def construct(source,asset):
    if sha(source)!=SOURCE_SHA or asset['source_sha256']!=SOURCE_SHA or asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False:raise ValueError('source/policy')
    if (asset['source_offset'],asset['stored_bytes'])!=(BASE,STORED) or sha(source[BASE:BASE+STORED])!=asset['source_stored_sha256']:raise ValueError('slot')
    if [u['translation'] for u in asset['units']]!=WORDS or [u['source'] for u in asset['units']]!=['1回のみ','毎日','毎週','毎月','毎年'] or any(u['state']!='needs_review' for u in asset['units']):raise ValueError('wording')
    if asset['edit_rect']!=[0,4,32,11] or asset['palette_roles']!={'background':0,'ink':3,'shadow':9}:raise ValueError('pixel boundary')
    refs=[m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+BASE)),source)]
    if refs!=REFS:raise ValueError('reference population')
    payload,used=lz77_decompress(source,BASE)
    if len(payload)!=1284 or used!=425 or payload[:4]!=bytes.fromhex('00040500'):raise ValueError('compressed/header contract')
    font_path=ROOT/asset['font_asset'];font=json.loads(font_path.read_text(encoding='utf-8'));g=glyphs(font,''.join(WORDS));new=bytearray(payload);records=[]
    for i,u in enumerate(asset['units']):
        block=payload[4+i*256:4+(i+1)*256];old=decode(block)
        if encode(old)!=block:raise ValueError('unchanged tile roundtrip')
        if any(v not in (0,3,9) or (v!=0 and not 4<=y<15) for y,row in enumerate(old) for v in row):raise ValueError('source text/background')
        rows=[list(r) for r in old]
        for y in range(4,15):rows[y]=[0]*32
        points=[];pen=0
        for ch in u['translation']:
            glyph=g[ch]
            for y,bits in enumerate(glyph['bits']):
                for x in range(glyph['width']):
                    if bits&(1<<(7-x)):points.append((pen+glyph['xoff']+x,6+glyph['top']+y))
            pen+=8
        width=max(x for x,y in points)+1;x0=(32-width)//2
        for x,y in points:
            if not(0<=x+x0<31 and 4<=y<14):raise ValueError('glyph/shadow overflow')
            rows[y+1][x+x0+1]=9
        for x,y in points:rows[y][x+x0]=3
        if any(rows[y][x]!=old[y][x] for y in range(16) for x in range(32) if not 4<=y<15):raise ValueError('protected pixel')
        new[4+i*256:4+(i+1)*256]=encode(rows)
        records.append(dict(u,tile_offset=i*8,ink_width=width,x0=x0,final_pixels_sha256=sha(bytes(v for r in rows for v in r))))
    stored=compress(bytes(new),output_limit=1284,stored_limit=STORED)
    padded=stored+bytes(STORED-len(stored))
    if lz77_decompress(padded,0)[0]!=bytes(new):raise ValueError('roundtrip')
    return padded,bytes(new),{'source_offset':BASE,'stored_bytes':STORED,'compressed_bytes':len(stored),'source_stored_sha256':sha(source[BASE:BASE+STORED]),'final_stored_sha256':sha(padded),'source_payload_sha256':sha(payload),'final_payload_sha256':sha(new),'units':records,'font_asset_sha256':sha(font_path.read_bytes()),'literal_references':refs,'translated_graphic_labels':5,'unchanged_roundtrip':True,'protected_pixels_equal':True,'header_unchanged':True,'runtime':'pending native reload/VRAM/OAM/screen','review':'needs_review','release_eligible':False}

if __name__=='__main__':
    source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
    _,_,record=construct(source,json.loads((ROOT/'translations/calendar_frequency_graphics_ko.json').read_text(encoding='utf-8')))
    print(json.dumps(record,ensure_ascii=False,indent=2))
