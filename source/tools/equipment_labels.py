"""Pinned common equipment fixed-text roots; no Navi-specific dialogue writes."""
from build_visibility_poc import sha
from folder_labels import validate_header_path,HEADER_SCOPE
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans

ROOTS=[0xD37FC,0xD387C]
HEADER_WIDTH=0xD382C
SCOPE=dict(HEADER_SCOPE,literal_scripts=[1,2,3,4],max_line_advance=80,
 literal_profiles=[{'scripts':[1],'consumer':'fixed-cell-big','literal_language':'mmbn45s','max_literal_rows':1,'max_line_advance':64},
 {'scripts':[3,4],'consumer':'fixed-cell-big','literal_language':'mmbn45s','max_literal_rows':1,'max_line_advance':72}])

def validate(source):
    native=validate_header_path(source)
    if source[HEADER_WIDTH:HEADER_WIDTH+3]!=bytes([10,3,3]):raise ValueError('equipment slot widths')
    if source[0xD382F:0xD3832]!=bytes([2,38,39]) or sha(source[0xD389C:0xD3958])!='a2564bfe5e270161dd63f28306531bd37790c170d88f15ef5de7ea4ef6cbfdd3':raise ValueError('equipment selection tables')
    selectors=[]
    for i in range(23):
        pointer=int.from_bytes(source[0xD38A0+i*4:0xD38A4+i*4],'little')-0x08000000
        if pointer!=0xD38FC+i*4:raise ValueError('Navi weapon selector root')
        values=list(source[pointer:pointer+4])
        if any(v>=60 for v in values):raise ValueError('weapon selector outside common text')
        selectors.append({'navi':i,'offset':pointer,'scripts':values})
    expected=None
    for pool in native['identical_native_header_sources']:
        scripts=script_spans(lz77_decompress(source,pool['pool'])[0],76)[:60]
        if expected is None:expected=scripts
        if scripts!=expected:raise ValueError('Navi common equipment population drift')
    ranges=[(0xD37D4,0xD37FA,'f253a58db7987a83485581a31cc7a6212026b8e2229c22693a80ae0c2c7dccee'),
      (0xD3834,0xD387C,'67a59735006b97ffa310c4f4fd726a26c049ded3a18864bb761d593ec4e7cb79')]
    for start,end,digest in ranges:
        if sha(source[start:end])!=digest:raise ValueError('equipment native function drift')
    refs=[]
    for literal,reader in zip(ROOTS,[0xD37D8,0xD385E]):
        if source[literal:literal+4]!=bytes.fromhex('7cba0202'):raise ValueError('equipment root literal drift')
        found=[]
        for at in range(0xD3000,0xD4000,2):
            h=int.from_bytes(source[at:at+2],'little')
            if h&0xF800==0x4800 and ((at+4)&~3)+(h&255)*4==literal:found.append(at)
        if found!=[reader]:raise ValueError('equipment literal references')
        refs.append({'literal':literal,'readers':found})
    return {'common_scripts':list(range(60)),'native_navi_pools':23,'roots':refs,
      'weapon_selector_records':selectors,'selection_table_sha256':sha(source[0xD389C:0xD3958]),
      'functions':[{'start':a,'end':b,'sha256':c} for a,b,c in ranges],
      'header_clear':{'width_byte':HEADER_WIDTH,'original_width':10,'target_width':12,'original_literal_cells':12,'native_text_objects':12,'policy':'Clear full original12-cell title OBJ region, including two stale trailing objects; weapon widths3/3 unchanged'},
      'policy':'Only fixed equipment roots and title clear width change; instructions, weapon index tables, numeric script63, all original Navi loaders/dialogue roots and RAM preserved'}
