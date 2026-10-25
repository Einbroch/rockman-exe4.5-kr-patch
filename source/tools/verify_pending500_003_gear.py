"""Normal GutsMan guides: native selection, clone/font consumption and OBJ pixels."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from archive_scripts import script_spans
from korean_codec import encode_character
from verify_tpi_index import lz77_decompress

def read(p):return json.loads(p.read_text(encoding='utf8'))

def main():
    rp=ROOT/'poc/output/exe45_ko_development_pending500_003_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read(ROOT/'project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    ar=next(x for x in m['keyitem_rom']['equipment_archives'] if x['archive']=='6E1554')
    pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    if sha(payload)!=ar['compiled_sha256']:raise ValueError('Gear clone identity')
    asset=read(ROOT/'translations/batch500_001_equipment_guts_draft_ko.json')
    units=[u for u in asset['units'] if int(u['id'].split(':')[1]) in (60,61,62)]
    ef=m['extension'];font=ef['normal_font_offset'];bias=ef['legacy_index_view']
    wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'}
    glyphs=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],wanted)
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    spans=script_spans(payload,76);expected={};streams={}
    for u in units:
        script=int(u['id'].split(':')[1]);text=u['translation']
        encoded=b''.join(b'\xe8' if c=='\n' else encode_character(c) if c in wanted else codes[c] for c in text)
        if spans[script].count(encoded)!=1:raise ValueError('Literal encoding')
        cursor=pool+struct.unpack_from('<H',payload,script*2)[0]+spans[script].index(encoded);ordered=[]
        for ch in text:
            if ch=='\n':cursor+=1;continue
            data=encode_character(ch) if ch in wanted else codes[ch];index=ord(ch)-0xAC00+bias if ch in wanted else data[0]
            record=rom[font+index*96:font+(index+1)*96]
            reference=glyphs[ch] if ch in wanted else source[0x608758+index*96:0x608758+(index+1)*96]
            if record!=reference:raise ValueError('Font supply')
            expected[cursor]=dict(ch=ch,index=index,record=record);ordered.append(cursor);cursor+=len(data)
        streams[script]=ordered
    p=ROOT/'poc/runtime/pending500-003-v2-guts-equipment-r2';receipt=read(p/'result.json')
    if not receipt['complete'] or receipt['rom_sha256']!=sha(rom):raise ValueError('Runtime binding')
    for name,digest in receipt['artifacts'].items():require_hash(p/name,digest)
    states={s:read(p/f'step_{s:03}_guides.json') for s in (7,9,11,12,15)};final=states[15]
    if len(final['entries'])!=4 or len(final['calls'])!=4 or len(final['returns'])!=4:raise ValueError('Guide ABI count')
    if [(x['root'],x['script_offset']) for x in final['lookups']]!=[(pool,s*2) for s in (60,61,62,60)]:raise ValueError('Actual native lookup selection')
    for e,c,r in zip(final['entries'],final['calls'],final['returns']):
        before=e['regs'];call=c['regs'];ret=r['regs']
        if e['navi']!=2 or call[0]!=0x0202BA7C or call[1]!=before[0]+60 or call[2:12]!=before[2:12] or call[13]!=before[13]-4 or c['saved_lr']!=before[14]:raise ValueError('Native guide caller ABI')
        if ret[4:12]!=before[4:12] or ret[13]!=before[13]-4 or r['saved_lr']!=before[14]:raise ValueError('Native guide return ABI')
    native=lz77_decompress(source,0x6E1554)[0];pages=[]
    for step,script in ((7,60),(9,61),(11,62),(15,60)):
        state=states[step];frame=state['entries'][-1]['frame'];draws=[d for d in state['draws'] if d['frame']>=frame and d['stream'] in streams[script]]
        if [d['stream'] for d in draws]!=streams[script]:raise ValueError('Draw coverage/order')
        counts=Counter(expected[d['stream']]['index'] for d in draws);reads={d['index']:d['reads'] for d in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Normal font CPU reads')
        ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0x2BA7C:0x2BA7C+len(native)]!=native:raise ValueError('Native loaded RAM changed')
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool:raise ValueError('Native context root')
        im=Image.open(p/f'step_{step:03}.png').convert('RGB');v=(p/f'step_{step:03}_gbaVideoRam.bin').read_bytes();o=(p/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();objects=[]
        for i in range(128):
            a,b,k=struct.unpack_from('<HHH',o,i*8)
            if not a&0x2300 and a>>14==1 and b>>14==2 and k>>12==14 and a&255 in (110,126):objects.append((i,b&511,a&255,k&1023))
        colors={1:set(),2:set(),3:set()};cells=[]
        for d in draws:
            g=expected[d['stream']]
            if d['glyph_index']!=g['index'] or d['color']!=0 or d['offset']%4:raise ValueError('Glyph index/color')
            row,off=divmod(d['offset'],10752);x0=92+off//4;y0=110+row*14;width=12 if g['ch'] in wanted else struct.unpack_from('<I',rom,ef['advance_offset']+g['index']*4)[0]
            if row not in (0,1) or x0+width>236 or y0+12>138:raise ValueError('Guide geometry')
            for yy in range(12):
                for xx in range(width):
                    role=(g['record'][yy*8+xx//2]>>(4*(xx%2)))&15;x=x0+xx;y=y0+yy
                    matches=[obj for obj in objects if obj[1]<=x<obj[1]+32 and obj[2]<=y<obj[2]+16]
                    if len(matches)!=1:raise ValueError('OBJ residency')
                    idx,ox,oy,tile=matches[0];lx=x-ox;ly=y-oy;at=0x10000+tile*32+(ly//8*4+lx//8)*32+(ly%8)*4+lx%8//2
                    if (v[at]>>(4*(lx%2)))&15!=role:raise ValueError('Font to VRAM pixel mismatch')
                    colors[role].add(im.getpixel((x,y)))
            cells.append(dict(character=g['ch'],stream=d['stream'],index=g['index'],xy=[x0,y0],font_vram_pixels_match=True))
        if any(len(x)!=1 for x in colors.values()) or len({next(iter(x)) for x in colors.values()})!=3:raise ValueError('Screenshot role colors')
        pages.append(dict(step=step,script=script,cells=cells,native_ram_preserved=True,font_cpu_reads_verified=True,all_glyph_pixels_match=True))
    if any(states[11][k]!=states[12][k] for k in ('entries','calls','returns','draws','lookups')):raise ValueError('Guide continues after exit')
    if struct.unpack_from('<I',(p/'step_012_gbaExtWorkRam.bin').read_bytes(),0xFA50)[0]==pool:raise ValueError('Guide root persists after exit')
    out=ROOT/'analysis/pending_insertion_500_003_rom';sheet=Image.new('RGB',(720,160))
    for i,s in enumerate((7,9,11)):sheet.paste(Image.open(p/f'step_{s:03}.png'),(i*240,0))
    sheet.save(out/'guts_guides_v1.png')
    report=dict(passed=True,rom_sha256=sha(rom),normal_navi=2,normal_controller_only=True,pages=pages,
        actual_clone_lookup_verified=True,native_caller_return_abi_verified=True,exit_reentry_verified=True,
        contact_sheet_sha256=sha((out/'guts_guides_v1.png').read_bytes()),release_eligible=False,
        limits=['Only GutsMan guide60/61/62 normal routes verified. Error70..75, FireMan and ProtoMan not gameplay-tested here. Full500 natural progression/reward/save not verified.'])
    (out/'guts_runtime_v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS GutsMan normal guides60/61/62, native clone/font/OBJ pixels, exit and reentry')

if __name__=='__main__':main()
