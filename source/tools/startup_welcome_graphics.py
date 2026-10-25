"""Font-derived native tiles for the initial PET welcome. No bitmap repainting."""
import re,struct
from build_visibility_poc import ROOT,sha,bdf_glyphs,require_hash,FONT_SHA256
from verify_tpi_index import lz77_decompress
from lz10_optimal import encode

BANK=(0x63466C,1310,'c92f12e2199b1d58cfbed4fe9d0399199a20a2b4e7d7d031f70c6e2a1d010ee7')
MAP=(0x634BB8,463,'bc2c2bb1a983384d21895b88c2f42507a983eb3a23a1c9b6f8c1691368c99006')
def pixels(bank,mapping):
    rows=[[0]*240 for _ in range(160)]
    for i,e in enumerate(struct.unpack('<600H',mapping[4:])):
        t=e&1023
        for y in range(8):
            for x in range(8):
                px=7-x if e&0x400 else x;py=7-y if e&0x800 else y
                rows[(i//30)*8+y][(i%30)*8+x]=(bank[4+t*32+py*4+px//2]>>(4*(px%2)))&15
    return rows

def construct(source,asset,appended):
    if asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['release_eligible'] is not False or asset['font_sha256']!=FONT_SHA256:raise ValueError('welcome policy/font')
    if asset['translation_lines']!=['PET을 구매해 주셔서','진심으로 감사드립니다.','사용자 이름을','입력해 주세요.']:raise ValueError('welcome selected wording')
    decoded=[]
    for at,n,h in [BANK,MAP]:
        if sha(source[at:at+n])!=h:raise ValueError('welcome source slot')
        p,c=lz77_decompress(source,at)
        if c!=n:raise ValueError('welcome compressed extent')
        decoded.append(p)
    bank,mapping=decoded
    if len(bank)!=4868 or len(mapping)!=1204:raise ValueError('welcome payload sizes')
    for at,refs in [(BANK[0],[0x3A0B4]),(MAP[0],[0x3A0BC])]:
        if [m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+at)),source)]!=refs:raise ValueError('welcome reference population')
    original=pixels(bank,mapping);target=[row[:] for row in original]
    # Original text occupies seven tile rows; every outside pixel is protected.
    for y in range(56,112):target[y][24:224]=[0]*200
    require_hash(ROOT/asset['font'],FONT_SHA256)
    glyphs=bdf_glyphs(ROOT/asset['font'],set(''.join(asset['translation_lines']).replace(' ','')))
    for n,line in enumerate(asset['translation_lines']):
        advance=sum(6 if ch==' ' else 11 for ch in line);pen=24+(192-advance)//2
        for ch in line:
            if ch==' ':pen+=6;continue
            g=glyphs[ch]
            for role,new in [(2,2),(3,1)]:
                for y in range(12):
                    for x in range(16):
                        if (g[y*8+x//2]>>(4*(x%2)))&15==role:
                            px,py=pen+x,58+n*13+y
                            if not (24<=px<216 and 56<=py<112):raise ValueError('welcome glyph extent')
                            if new==1 or target[py][px]==0:target[py][px]=new
            pen+=11
    entries=list(struct.unpack('<600H',mapping[4:]));tiles=[bank[4:36]];indices={tiles[0]:0}
    for ty in range(7,14):
        for tx in range(3,28):
            tile=bytearray(32)
            for y in range(8):
                for x in range(8):tile[y*4+x//2]|=target[ty*8+y][tx*8+x]<<(4*(x%2))
            b=bytes(tile)
            if b not in indices:indices[b]=len(tiles);tiles.append(b)
            entries[ty*30+tx]=(entries[ty*30+tx]&0xF000)|indices[b]
    if len(tiles)>152:raise ValueError('welcome tile capacity')
    oldtiles=tiles;tiles=[oldtiles[0]]+sorted(oldtiles[1:]);remap={i:tiles.index(t) for i,t in enumerate(oldtiles)}
    for ty in range(7,14):
        for tx in range(3,28):
            i=ty*30+tx;entries[i]=(entries[i]&0xF000)|remap[entries[i]&1023]
    newbank=bank[:4]+b''.join(tiles)+bytes((152-len(tiles))*32)
    newmap=mapping[:4]+struct.pack('<600H',*entries)
    if pixels(newbank,newmap)!=target:raise ValueError('welcome protected pixel roundtrip')
    patches=[];records=[];out=bytearray(appended)
    for (at,n,h),p,reference in zip([BANK,MAP],[newbank,newmap],[0x3A0B4,0x3A0BC]):
        compressed=encode(p,stored_limit=len(p)*2)
        if lz77_decompress(compressed,0)[0]!=p:raise ValueError('welcome independent decode')
        out.extend(b'\xff'*(-len(out)%4));target_at=len(source)+len(out);out.extend(compressed)
        patches.append((reference,(0x08000000+target_at).to_bytes(4,'little'),'initial PET welcome native graphics reference'))
        records.append(dict(source_offset=at,source_stored_bytes=n,offset=target_at,reference=reference,stored_bytes=len(compressed),payload_bytes=len(p),source_sha256=h,target_sha256=sha(compressed),payload_sha256=sha(p)))
    return bytes(out),patches,dict(id=asset['id'],records=records,editable_rect=[24,56,200,56],protected_pixels_identical=True,tiles_used=len(tiles),tile_capacity=152,loader_and_palette_unchanged=True,source_graphics_unchanged=True,runtime_verified=False)
