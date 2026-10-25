"""Pinned compressed equipment caption; native typography and framing preserved."""
import json,re,struct
from build_visibility_poc import ROOT,sha
from pet_graphics_font import SOURCE_SHA,glyphs
from verify_tpi_index import lz77_decompress
from lz10_greedy import encode as compress

BASE=0x512FA0;STORED=516;SIZE=1156;TILES=36;BYTES=768
SOURCE_STORED_SHA='34e7af43c90dd7c80ea176df7bfcb83557673741380328d0853ab481daa46bff'

def decode(block):
    if len(block)!=BYTES:raise ValueError('caption tile extent')
    return [[(block[(x//32*8+y//8*4+x%32//8)*32+y%8*4+x%8//2]>>(4*(x%2)))&15 for x in range(96)] for y in range(16)]

def encode(rows):
    if len(rows)!=16 or any(len(r)!=96 for r in rows):raise ValueError('caption dimensions')
    block=bytearray(BYTES)
    for y,row in enumerate(rows):
        for x,role in enumerate(row):
            if type(role)!=int or not 0<=role<=15:raise ValueError('caption palette index')
            block[(x//32*8+y//8*4+x%32//8)*32+y%8*4+x%8//2]|=role<<(4*(x%2))
    return bytes(block)

def construct(source,asset):
    if sha(source)!=SOURCE_SHA or asset['source_sha256']!=SOURCE_SHA or asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False:raise ValueError('caption source/policy')
    fields={'source_offset':BASE,'stored_bytes':STORED,'decompressed_bytes':SIZE,'tile_payload_offset':TILES,'caption_bytes':BYTES,'canvas':[96,16],'edit_rect':[7,4,60,11],'glyph_origin':[8,5],'advance':8,'space_advance':3,'source':'バスター攻撃力','translation':'버스터 공격력','source_stored_sha256':SOURCE_STORED_SHA,'palette_roles':{'background':14,'ink':15,'shadow':13,'bottom_border':12}}
    if any(asset[k]!=v for k,v in fields.items()):raise ValueError('caption adopted source/typography boundary')
    if sha(source[BASE:BASE+STORED])!=SOURCE_STORED_SHA or source[0x3C414:0x3C422]!=bytes.fromhex('00b503480649094aecf7a2fe00bd') or source[0x3C42C:0x3C430]!=struct.pack('<I',0x08000000+BASE):raise ValueError('caption native loader contract')
    refs=[m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+BASE)),source)]
    if refs!=[0x3C42C]:raise ValueError('caption source reference audit')
    payload,used=lz77_decompress(source,BASE)
    if len(payload)!=SIZE or used!=STORED:raise ValueError('caption original compressed boundary')
    old=decode(payload[TILES:TILES+BYTES])
    if encode(old)!=payload[TILES:TILES+BYTES]:raise ValueError('caption unchanged tile roundtrip')
    clean=[list(row) for row in old]
    for y,row in enumerate(old):
        for x,role in enumerate(row):
            if role in [13,15] and not(7<=x<67 and 4<=y<15):raise ValueError('source glyph outside edit scope')
    for y in range(4,15):
        for x in range(7,67):
            bg=12 if y==14 else 14
            if old[y][x] not in [bg,13,15]:raise ValueError('caption clean background role')
            clean[y][x]=bg
    font_asset=json.loads((ROOT/asset['font_asset']).read_text(encoding='utf-8'));g=glyphs(font_asset,asset['translation'].replace(' ',''));new=[list(row) for row in clean];pen=8;points=[]
    for ch in asset['translation']:
        if ch==' ':pen+=3;continue
        glyph=g[ch]
        for y,bits in enumerate(glyph['bits']):
            for x in range(glyph['width']):
                if bits&(1<<(7-x)):points.append((pen+glyph['xoff']+x,5+glyph['top']+y))
        pen+=8
    for x,y in points:
        if not(7<=x<66 and 4<=y<14):raise ValueError('caption glyph/shadow overflow')
        new[y+1][x+1]=13
    for x,y in points:new[y][x]=15
    for y in range(16):
        for x in range(96):
            if not(7<=x<67 and 4<=y<15) and new[y][x]!=old[y][x]:raise ValueError('caption protected pixels')
    final=payload[:TILES]+encode(new)+payload[TILES+BYTES:]
    stored=compress(final,output_limit=SIZE,stored_limit=STORED);padded=stored+b'\0'*(STORED-len(stored))
    if lz77_decompress(padded,0)[0]!=final:raise ValueError('caption final source slot roundtrip')
    record={'id':asset['id'],'source':asset['source'],'translation':asset['translation'],'source_offset':BASE,'stored_bytes':STORED,'source_stored_sha256':SOURCE_STORED_SHA,'compressed_bytes':len(stored),'final_stored_sha256':sha(padded),'source_payload_sha256':sha(payload),'final_payload_sha256':sha(final),'decompressed_bytes':SIZE,'tile_payload_offset':TILES,'caption_bytes':BYTES,'edit_rect':asset['edit_rect'],'source_caption_sha256':sha(payload[TILES:TILES+BYTES]),'final_caption_sha256':sha(final[TILES:TILES+BYTES]),'clean_background_sha256':sha(encode(clean)),'font':font_asset['font'],'protected_pixels_equal':True,'protected_payload_bytes_equal':True,'unchanged_roundtrip':True,'native_literal_references':refs,'native_loader_unchanged':True,'palette_roles':asset['palette_roles'],'glyphs_unscaled':True,'translated_graphic_labels':1,'runtime':'pending exact-ROM native decompression/RAM/VRAM/OBJ/pixels','review':'needs_review','release_eligible':False}
    return padded,final,record

if __name__=='__main__':
    source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes();asset=json.loads((ROOT/'translations/equipment_attack_caption_ko.json').read_text(encoding='utf-8'));_,_,r=construct(source,asset);print(json.dumps(r,ensure_ascii=False,indent=2))
