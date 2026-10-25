"""Exact-ROM decompression, independent script lookup and Korean OBJ pixel QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,pixels,verify_route
from build_visibility_poc import require_hash,bdf_glyphs
from verify_tpi_index import lz77_decompress
from korean_codec import encode_character
from keyitem_empty import resolved,compact,validate_source
from run_keyitem_empty import STEM,PREFIX,ROUTES
from report_gutsman_pet import main as regression

OUTDIR='keyitem_empty_v1'
RAWDIR='poc/build_keyitem_empty_v1'
def main(statistics=False):
    result=regression(stem=STEM,prefix=PREFIX,expected_counts=(2350 if statistics else 2349,59,673),
        oldstem='exe45_ko_development_keyitem_empty_v1' if statistics else 'exe45_ko_development_gutsman_calendar_inventory_v1',outdir=OUTDIR,
        inventory_outdir='full_scope_possessions_statistics_v1' if statistics else 'full_scope_keyitem_empty_v1',added_literal_units=1,
        changed_archives=('6368E8',) if statistics else ())
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));rom=rp.read_bytes()
    ar=next(a for a in m['archives']if a['archive']=='709408')
    payload,_=lz77_decompress(rom,ar['rom_offset']);require_hash(rp,m['output_sha256'])
    if len(payload)!=1273 or sha(payload)!=ar['compiled_sha256']:
        raise ValueError('keyitem product payload identity')
    source_rom=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
    source,_=lz77_decompress(source_rom,0x709408);validate_source(source_rom,source)
    raw=(ROOT/RAWDIR/'709408/compiled/709408.msg').read_bytes()
    expected_payload,proof=compact(source,raw)
    if payload!=expected_payload:raise ValueError('keyitem final storage plan')
    root=0x08000000+ar['rom_offset']
    if any(struct.unpack_from('<I',rom,p)[0]!=root for p in [0x34a2c,0x4c5e8]):
        raise ValueError('keyitem two roots not installed atomically')
    text=read(ROOT/'translations/keyitem_empty_ko.json')['units'][0]['translation']
    codes={v:bytes.fromhex(k)for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()if '='in line for k,v in [line.split('=',1)]if len(v)==1}
    body=b''.join(b'\xe8'if c=='\n'else encode_character(c)if '\uac00'<=c<='\ud7a3'else codes[c]for c in text)
    if resolved(payload)[32]!=bytes.fromhex('fc06e702f00000')+body+bytes.fromhex('edff0000'):
        raise ValueError('keyitem exact script/control bytes')
    font=m['extension']['normal_font_offset'];bias=m['extension']['legacy_index_view']
    glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],{c for c in text if '\uac00'<=c<='\ud7a3'})
    cursor=0x02020800+struct.unpack_from('<H',payload,64)[0]+7;expected={};geometry={};row=advance=0
    for ch in text:
        if ch=='\n':cursor+=1;row+=1;advance=0;continue
        hangul='\uac00'<=ch<='\ud7a3';index=ord(ch)-0xAC00+bias if hangul else codes[ch][0]
        record=rom[font+index*96:font+(index+1)*96]
        if hangul and record!=glyphs[ch]:raise ValueError('keyitem Korean font supply')
        if not hangul and record!=source_rom[0x608758+index*96:0x608758+(index+1)*96]:raise ValueError('keyitem native numeral/punctuation font')
        expected[cursor]=dict(ch=ch,index=index,record=record,id='709408:32:0',script=32)
        geometry[cursor]=row*10752+advance*4
        advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
        cursor+=4 if hangul else len(codes[ch])
    rt=ROOT/'poc/runtime';paths={};seen=set();routes={}
    for name,parent,_ in ROUTES:
        p=rt/(PREFIX+name);receipt=verify_route(p,m['output_sha256'],seen)
        if receipt['state_origin']!=str(rt/(PREFIX+parent)/'result.json'):raise ValueError('keyitem normal ancestry')
        if any(x in (p/'segment.lua').read_text(encoding='utf8')for x in ['emu.write','setState','AliasReads']):raise ValueError('keyitem observer intervention')
        if read(p/'keyitem_environment.json')['self_sha256']!=sha((ROOT/'tools/capture_keyitem_empty.py').read_bytes()):raise ValueError('keyitem observer provenance')
        paths[name]=p;routes[name]=receipt
    pages=[]
    for name in ['empty','empty-reenter']:
        p=paths[name];step=2;cp='step_002';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));key=read(p/(cp+'_keyitem.json'))
        if ram[0x20800:0x20800+len(payload)]!=payload or ram[0xFA21]!=32 or struct.unpack_from('<I',ram,0xFA50)[0]!=0x02020800:
            raise ValueError('keyitem native RAM/root/script')
        if not any(c['root']==0x02020800 and c['script']==32 for c in key['lookups']):raise ValueError('keyitem independent lookup not observed')
        last={d['stream']:d for d in obs['draws']if d['stream']in expected}
        if set(last)!=set(expected):raise ValueError('keyitem full glyph population')
        draws=[last[s]for s in expected]
        if any(d['offset']!=geometry[d['stream']]or d['context']!=0x0200FA20 for d in draws):raise ValueError('keyitem line geometry')
        counts=Counter(d['glyph_index']for d in draws);reads={x['index']:x['reads']for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('keyitem CPU font reads')
        page=pixels(p,step,draws,expected,rom,m,origin=(52,110),cursor_indices=())
        pages.append(dict(route=name,step=step,screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),**page))
    load=read(paths['empty']/'step_002_keyitem.json')['loads']
    if len(load)!=1 or (load[0]['root'],load[0]['destination'],load[0]['lr'])!=(root,0x02020800,0x080349f1):raise ValueError('keyitem relocated compressed native load')
    held=(paths['empty-hold']/'step_001_gbaExtWorkRam.bin').read_bytes()
    if held[0x20800:0x20800+len(payload)]!=payload:raise ValueError('keyitem hold residency')
    close=(paths['empty-close']/'step_002_gbaExtWorkRam.bin').read_bytes()
    if close[0xFA21]!=10:raise ValueError('keyitem close destination')
    baseline=(rt/'gutsman-calendar-inventory-v1-inventory'/'step_002_gbaExtWorkRam.bin').read_bytes()
    for p in paths.values():
        steps=routes[p.name.removeprefix(PREFIX)]['capture_steps']
        ram=(p/f'step_{steps[-1]:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0x10AC0:0x10AC5]!=baseline[0x10AC0:0x10AC5]or ram[0x1310:0x1330]!=baseline[0x1310:0x1330]:raise ValueError('keyitem nickname/schedule isolation')
    out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(720,160))
    for i,name in enumerate(['empty','empty-close','empty-reenter']):sheet.paste(Image.open(paths[name]/'step_002.png'),(i*240,0))
    sheet.save(out/'empty_item.png')
    result.update(keyitem_native_storage=proof,keyitem_two_roots_installed=True,keyitem_pages=pages,
        keyitem_load=load,keyitem_hold_residency=True,keyitem_close_script=10,
        limits=result['limits']+['Only UI02020800 load/use/hold/close/reentry observed; other02031000 consumer has source-bounded storage but no runtime trial here.',
            'Other38 key-item literals remain untranslated in ROM; full draft2477 bytes still needs a separate capacity design.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Keyitem empty: native LZ/RAM/lookup/font/OBJ pixels/hold/B/reentry PASS')
    return result

if __name__=='__main__':main()
