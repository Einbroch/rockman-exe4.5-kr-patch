"""Source-pinned equipment title typography and isolated folder-header data root."""
from build_visibility_poc import ROOT,sha
from pet_graphics_font import SOURCE_SHA,glyphs
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans

TITLE_BASE=0x6330A4
TITLE_SHA='f082c9872534fc5b27444b891f20d550fe3aaa27a42b53c3ba549059c0089698'
HEADER_ROOT=0x3E474
HEADER_CODE_SHA='2872d08dc3844238930abb897eb3a3149d60cde27698e2e0e30089ce446dec74'
HEADER_SCOPE={'source_bytes':634,'pointers':[0x3C5E8],'compressed':True,'consumer':'fixed-cell-big',
 'max_literal_rows':1,'max_line_advance':64,'complete_literal_scope':False,'literal_scripts':[1],
 'literal_language':'mmbn45s','script_count':76}

def validate_header_path(source):
    if sha(source)!=SOURCE_SHA or sha(source[0x3E45C:0x3E474])!=HEADER_CODE_SHA or source[HEADER_ROOT:HEADER_ROOT+4]!=bytes.fromhex('7cba0202'):raise ValueError('folder header native path drift')
    # This isolated renderer has a constant script1. Every native Navi pool's
    # script1 is byte-identical, so direct ROM supply does not change Navi words.
    expected=None;roots=[]
    for at in range(0x3C5BC,0x3C618,4):
        address=int.from_bytes(source[at:at+4],'little')-0x08000000
        payload,_=lz77_decompress(source,address);s=script_spans(payload,76)[1]
        if expected is None:expected=s
        if s!=expected:raise ValueError('Navi-dependent header differs')
        roots.append({'pointer':at,'pool':address,'script1_sha256':sha(s)})
    # Validate the only Thumb PC-relative LDR consumers of this literal over
    # the surrounding native code/data extent, rather than moving RAM storage.
    refs=[]
    for at in range(0x3E000,0x3F000,2):
        half=int.from_bytes(source[at:at+2],'little')
        if half&0xF800==0x4800 and ((at+4)&~3)+(half&255)*4==HEADER_ROOT:refs.append(at)
    if refs!=[0x3E460]:raise ValueError('isolated folder header literal references')
    return {'constant_script':1,'native_function':0x0803E45C,'native_root':0x0202BA7C,
        'literal_read_sites':refs,'identical_native_header_sources':roots,'source_code_sha256':HEADER_CODE_SHA,
        'policy':'Only isolated 8x1 header function data-root changes; source compressed pointer, load and all other RAM consumers remain unchanged'}

def title(source,font_asset):
    if sha(source)!=SOURCE_SHA:raise ValueError('equipment title source')
    old=source[TITLE_BASE:TITLE_BASE+256]
    if sha(old)!=TITLE_SHA:raise ValueError('equipment title block')
    rows=[[(old[x//8*32+y*4+(x%8)//2]>>(4*(x%2)))&15 for x in range(64)] for y in range(8)]
    output=[list(r) for r in rows]
    for y in range(8):
        for x in range(22,45):
            if rows[y][x] not in (0,15):raise ValueError('equipment title role')
            output[y][x]=0
    g=glyphs(font_asset);pen=24
    for ch in '장비':
        glyph=g[ch]
        for y,bits in enumerate(glyph['bits']):
            for x in range(glyph['width']):
                if bits&(1<<(7-x)):output[glyph['top']+y][pen+x]=15
        pen+=8
    target=bytearray(old)
    for y,row in enumerate(output):
        for x,role in enumerate(row):
            if not 22<=x<45 and role!=rows[y][x]:raise ValueError('title protected pixel')
            at=x//8*32+y*4+(x%8)//2;shift=(x%2)*4
            target[at]=(target[at]&~(15<<shift))|(role<<shift)
    roundtrip=bytearray(256)
    for y,row in enumerate(rows):
        for x,role in enumerate(row):roundtrip[x//8*32+y*4+x%8//2]|=role<<(4*(x%2))
    if roundtrip!=old:raise ValueError('title unchanged roundtrip')
    return bytes(target),{'id':'equipment.obj.title','source':'そうび','translation':'장비','source_offset':TITLE_BASE,'bytes':256,
        'source_block_sha256':TITLE_SHA,'final_block_sha256':sha(target),'edit_rect':[22,0,23,8],
        'roles':[0,15],'protected_pixels_equal':True,'unchanged_roundtrip':True,'font':font_asset['font'],
        'runtime':'pending exact-ROM','review':'needs_review','release_eligible':False}
