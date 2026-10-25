"""Six NumberMan alert literals: guarded runtime receipt, wait, font and OBJ pixels."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from archive_scripts import script_spans
from korean_codec import encode_character,EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from report_roll_pet import pixels

def read(p):return json.loads(p.read_text(encoding='utf8'))

def main():
    rp=ROOT/'poc/output/exe45_ko_development_pending500_004_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read(ROOT/'project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    ar=next(x for x in m['archives'] if x['archive']=='68BAAC');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    require_hash(ROOT/'poc/output/exe45_ko_development_pending500_004_v1_repro.gba',m['output_sha256'])
    asset=read(ROOT/'analysis/pending_insertion_500_004_rom/68BAAC_selected_asset.json');units=asset['units'];spans=script_spans(payload,5)
    wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'};ef=m['extension'];bias=ef['legacy_index_view'];font=ef['normal_font_offset']
    glyphs=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],wanted)
    extra={c for u in units for c in u['translation'] if c in EXTRA_CHARACTER_INDICES}
    glyphs.update(bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    supplied=wanted|extra
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    expected={};streams={};ends={}
    for u in units:
        script=int(u['id'].split(':')[1]);text=u['translation'];encoded=b''.join(b'\xe8' if c=='\n' else encode_character(c) if c in supplied else codes[c] for c in text)
        if spans[script].count(encoded)!=1:raise ValueError('Literal encoding identity')
        cursor=pool+struct.unpack_from('<H',payload,script*2)[0]+spans[script].index(encoded);ordered=[]
        for ch in text:
            if ch=='\n':cursor+=1;continue
            data=encode_character(ch) if ch in supplied else codes[ch];index=ord(ch)-0xAC00+bias if ch in wanted else EXTRA_CHARACTER_INDICES[ch]+bias if ch in extra else data[0]
            record=rom[font+index*96:font+(index+1)*96];reference=glyphs[ch] if ch in supplied else source[0x608758+index*96:0x608758+(index+1)*96]
            if record!=reference:raise ValueError('ROM font supply')
            expected[cursor]=dict(ch=ch,index=index,record=record,id=u['id']);ordered.append(cursor);cursor+=len(data)
        streams[u['id']]=ordered;ends[u['id']]=cursor
        if rom[cursor-0x08000000:cursor-0x08000000+2]!=bytes.fromhex('e600'):raise ValueError('Native wait byte anchor')
    pages=[];covered=set();sheet=Image.new('RGB',(720,320))
    for script in (1,2):
        folder=ROOT/f'poc/runtime/pending500-004-v1-number-alert{script}';receipt=read(folder/'result.json');d=receipt['alert_diagnostic']
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is not False or d['native_navi']!=8 or d['root_aliases']!=d['entry_aliases']!=1:raise ValueError('Runtime alias binding')
        if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Diagnostic quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        for ordinal,step in enumerate((2,4,6)):
            key=f'68BAAC:{script}:{ordinal}';state=read(folder/f'step_{step:03}_roll_pet.json');ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
            if (ptr,root)!=(ends[key],pool):raise ValueError('Exact current wait/root')
            last={x['stream']:x for x in state['draws'] if x['stream'] in streams[key]}
            if set(last)!=set(streams[key]):raise ValueError('Literal draw coverage')
            draws=[last[s] for s in streams[key]];counts=Counter(x['glyph_index'] for x in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Font CPU consumption')
            proof=pixels(folder,step,draws,expected,rom,m);im=Image.open(folder/f'step_{step:03}.png').convert('RGB');bg=im.getpixel((233,110));rects=[]
            for x in draws:
                row,off=divmod(x['offset'],10752);left=92+off//4;top=110+row*14;width=struct.unpack_from('<I',rom,ef['advance_offset']+x['glyph_index']*4)[0]
                rects.append((left,top,left+width,top+12))
            vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
            if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('Stale text pixels between pages')
            sheet.paste(im,(ordinal*240,(script-1)*160));covered.add(key)
            pages.append(dict(id=key,step=step,exact_keywait=True,vacant_pixels_cleared=len(vacant),screenshot_sha256=sha((folder/f'step_{step:03}.png').read_bytes()),**proof))
    if covered!={u['id'] for u in units}:raise ValueError('Selected six-literal scope')
    out=ROOT/'analysis/pending_insertion_500_004_rom';sheet.save(out/'number_alerts_v1.png')
    report=dict(passed=True,rom_sha256=sha(rom),diagnostic_rendered_ids=sorted(covered),pages=pages,native_numberman_portrait_context_retained=True,
        contact_sheet_sha256=sha((out/'number_alerts_v1.png').read_bytes()),normal_scene_selection_verified=False,release_eligible=False,
        limits=['Pointer/table read aliases from actual NumberMan normal state, display evidence only; not natural tournament/date selection/progression/save.','Only six of500 newly inserted literals runtime-observed; remaining complete-script raw consumer members static-verified.'])
    (out/'alert_runtime_v1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS six NumberMan alert waits/font/OBJ pixels and page clearing')

if __name__=='__main__':main()
