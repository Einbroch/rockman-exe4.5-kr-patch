"""Runtime display evidence for communication options and AquaMan three pages."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from archive_scripts import script_spans
from korean_codec import encode_character,EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from report_roll_pet import pixels

def read(p):return json.loads(p.read_text(encoding='utf8'))

def model(rom,m,cfg,archive,script,count,asset_folder='analysis/pending_insertion_500_005_rom',record=None,asset=None):
    ar=record if record is not None else next(x for x in m['archives'] if x['archive']==archive);pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    asset=asset if asset is not None else read(ROOT/asset_folder/f'{archive}_selected_asset.json');units=[u for u in asset['units'] if int(u['id'].split(':')[1])==script]
    wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'};extra={c for u in units for c in u['translation'] if c in EXTRA_CHARACTER_INDICES};supplied=wanted|extra
    ef=m['extension'];bias=ef['legacy_index_view'];font=ef['normal_font_offset'];sp=ROOT/cfg['source_profile']['filename'];source=sp.read_bytes()
    glyphs=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],wanted)
    glyphs.update(bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    span=script_spans(payload,count)[script];expected={};streams={};ends={}
    for u in units:
        encoded=b''.join(b'\xe8' if c=='\n' else encode_character(c) if c in supplied else codes[c] for c in u['translation'])
        if span.count(encoded)!=1:raise ValueError('Selected literal boundary uniqueness')
        cursor=pool+struct.unpack_from('<H',payload,script*2)[0]+span.index(encoded);ordered=[]
        for c in u['translation']:
            if c=='\n':cursor+=1;continue
            data=encode_character(c) if c in supplied else codes[c];index=ord(c)-0xAC00+bias if c in wanted else EXTRA_CHARACTER_INDICES[c]+bias if c in extra else data[0]
            record=rom[font+index*96:font+(index+1)*96];reference=glyphs[c] if c in supplied else source[0x608758+index*96:0x608758+(index+1)*96]
            if record!=reference:raise ValueError('Actual font supply')
            expected[cursor]=dict(ch=c,index=index,record=record,id=u['id']);ordered.append(cursor);cursor+=len(data)
        streams[u['id']]=ordered;ends[u['id']]=cursor
    return pool,units,expected,streams,ends

def main():
    rp=ROOT/'poc/output/exe45_ko_development_pending500_005_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read(ROOT/'project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    require_hash(ROOT/'poc/output/exe45_ko_development_pending500_005_v1_repro.gba',sha(rom));pages=[];images=[];covered=set()
    for case,archive,script,count,steps in [('communication','776650',0,138,(2,4,6)),('aqua','776198',6,20,(2,4,6))]:
        pool,units,expected,streams,ends=model(rom,m,cfg,archive,script,count);folder=ROOT/f'poc/runtime/pending500-005-v1-display-{case}';receipt=read(folder/'result.json');d=receipt['display_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is not False or d['roots']!=d['entries']!=1 or d['navi']!=0:raise ValueError('Diagnostic binding')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        for ordinal,step in enumerate(steps):
            selected=units if case=='communication' else [units[ordinal]];keys=[u['id'] for u in selected];selected_streams=[s for key in keys for s in streams[key]]
            state=read(folder/f'step_{step:03}_roll_pet.json');ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if root!=pool:raise ValueError('Native current root')
            last={x['stream']:x for x in state['draws'] if x['stream'] in selected_streams}
            if set(last)!=set(selected_streams):raise ValueError('Current page glyph coverage')
            draws=[last[s] for s in selected_streams];reads={x['index']:x['reads'] for x in state['font_reads']};counts=Counter(x['glyph_index'] for x in draws)
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Font CPU reads')
            # Context+18/+19 supply native52/110 text origin after initialization.
            if tuple(ram[0xFA38:0xFA3A])!=(52,110):raise ValueError('Native text origin')
            proof=pixels(folder,step,draws,expected,rom,m,origin=(52,110),cursor_screen_background=True)
            if case=='aqua':
                if ptr!=ends[keys[0]] or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Exact AquaMan keyWait')
                im=Image.open(folder/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((233,110));rects=[]
                for x in draws:
                    row,off=divmod(x['offset'],10752);left=52+off//4;top=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+x['glyph_index']*4)[0]
                    rects.append((left,top,left+width,top+12))
                vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('AquaMan page clearing')
            else:
                if ptr!=ends[keys[-1]] or rom[ptr-0x08000000:ptr-0x08000000+6]!=bytes.fromhex('ec06800102ff'):raise ValueError('Exact native select boundary')
                o=(folder/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0)
                if a&0x2300 or k&1023!=1020 or (b&511,a&255)!=(44,136 if step==4 else 122):raise ValueError('Native option cursor up/down/reentry')
            covered.update(keys);images.append(Image.open(folder/f'step_{step:03}.png'));pages.append(dict(case=case,step=step,ids=keys,current_pointer=ptr,exact_native_wait_or_select_verified=True,**proof))
    out=ROOT/'analysis/pending_insertion_500_005_rom';sheet=Image.new('RGB',(720,320))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    sheet.save(out/'display_pages_v1.png')
    result=dict(passed=True,rom_sha256=sha(rom),diagnostic_rendered_ids=sorted(covered),pages=pages,contact_sheet_sha256=sha((out/'display_pages_v1.png').read_bytes()),
        normal_scene_selection_verified=False,release_eligible=False,limits=['Six newly inserted literals in pointer/table read-alias display diagnostics, not native battle/communication failure, chip integration/HP reward, acquisition or save.','Actual controller confirm/outcome for communication choices not tested; cursor navigation/display only.'])
    (out/'display_runtime_v1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS six new display literals, font/OBJ pixels and AquaMan waits')

if __name__=='__main__':main()
