"""Exact integrated artifact, normal selector/runtime and finite glyph QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,require_hash,bdf_glyphs,pixels,verify_route
from report_gutsman_pet import main as regression
from keyitem_empty import resolved
from keyitem_rom_data import verify_final
from korean_codec import encode_character

STEM='exe45_ko_development_keyitem_full_rom_v1';PREFIX='keyitem-full-rom-v1-'

def static():
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);s=source.read_bytes();k=m['keyitem_rom'];verify_final(s,rom,k)
    old=ROOT/'poc/output/exe45_ko_development_possessions_statistics_v1.gba';om=read(old.with_suffix('.json'));require_hash(old,om['output_sha256']);previous=old.read_bytes()
    diffs=[i for i,(a,b)in enumerate(zip(previous,rom))if a!=b]
    if not diffs or any(not 0x4FB4C<=i<0x4FB58 for i in diffs)or len(rom)<=len(previous):raise ValueError('only new entry/append versus latest product')
    rebuilt=bytearray(s);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];b=bytes.fromhex(w['final_hex'])
        if len(b)!=n or s[at:at+n]!=bytes.fromhex(w['expected_hex'])or occupied.intersection(range(at,at+n)):raise ValueError('final ledger')
        occupied.update(range(at,at+n));rebuilt[at:at+n]=b
    if bytes(rebuilt)!=rom[:len(s)]or rom[:192]!=s[:192]or len(rom)!=len(s)+m['append_bytes']or sha(rom[len(s):])!=m['append_sha256']:raise ValueError('source/append/header audit')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    asset=read(ROOT/'translations/keyitem_full_rom_ko.json');units=asset['units'];root=0x08000000+k['rom_offset'];payload=rom[k['rom_offset']:k['rom_offset']+k['rom_bytes']];spans=resolved(payload)
    table=ROOT/'external/textpet-plugins/exe45-utf8.tbl'
    codes={v:bytes.fromhex(a)for line in table.read_text(encoding='utf-8-sig').splitlines()if '='in line for a,v in [line.split('=',1)]if len(v)==1}
    glyphs=bdf_glyphs(ROOT/m['font']['path'],{c for u in units for c in u['translation']if '\uac00'<=c<='\ud7a3'})
    expected={};streams={};geometry={};all_rows=[]
    for script in sorted({int(u['id'].split(':')[1])for u in units}):
        row=advance=0
        for unit in [u for u in units if int(u['id'].split(':')[1])==script]:
            text=unit['translation'];body=b''.join(b'\xe8'if c=='\n'else encode_character(c)if '\uac00'<=c<='\ud7a3'else codes[c]for c in text)
            off=spans[script].find(body)
            if off<0:raise ValueError('finite selected bytes missing')
            cursor=root+struct.unpack_from('<H',payload,script*2)[0]+off;streams[unit['id']]=[]
            # Quantity suffix begins after up to three digits; its exact
            # dynamic geometry is checked from runtime, not guessed here.
            for ch in text:
                if ch=='\n':row+=1;advance=0;cursor+=1;continue
                hangul='\uac00'<=ch<='\ud7a3';idx=ord(ch)-0xAC00+m['extension']['legacy_index_view']if hangul else codes[ch][0]
                at=m['extension']['normal_font_offset']+idx*96;record=rom[at:at+96]
                if hangul and record!=glyphs[ch]:raise ValueError('full39 Hangul glyph record')
                if not hangul and record!=s[0x608758+idx*96:0x608758+(idx+1)*96]:raise ValueError('full39 legacy glyph')
                expected[cursor]=dict(ch=ch,index=idx,record=record,id=unit['id'],script=script)
                streams[unit['id']].append(cursor);geometry[cursor]=(row,advance)
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+idx*4)[0];cursor+=4 if hangul else len(codes[ch])
            all_rows.append(dict(id=unit['id'],static_ending_row=row,static_ending_advance_px=advance))
    return m,rom,expected,streams,geometry,dict(passed=True,rom_sha256=m['output_sha256'],selected_literal_units=len(units),all_finite_glyph_records_verified=True,source_unchanged=True,header_and_append_verified=True,write_ledger_verified=True,prior_product_only_entry_and_append_changed=True,source_extent_changed_bytes=len(diffs),static_rows=all_rows)

def main():
    m,rom,e,streams,geometry,proof=static();out=ROOT/'analysis/keyitem_full_rom_v1';out.mkdir(exist_ok=True)
    (out/'static.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    regression(stem=STEM,prefix=PREFIX,expected_counts=(2388,59,673),oldstem='exe45_ko_development_possessions_statistics_v1',outdir='keyitem_full_rom_v1',inventory_outdir='full_scope_keyitem_full_rom_v1',added_literal_units=38)
    rt=ROOT/'poc/runtime';root=0x08000000+m['keyitem_rom']['rom_offset'];pages=[];seen=set();routes={}
    from run_keyitem_empty import ROUTES
    for name,parent,_ in ROUTES:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen);routes[name]=r
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json')or any(x in (p/'segment.lua').read_text()for x in ['emu.write','setState','matrixCases']):raise ValueError('normal ancestry/intervention')
    wanted={s for s,g in e.items()if g['script']==32}
    for name,step in [('empty',2),('empty-reenter',2)]:
        p=rt/(PREFIX+name);cp=f'step_{step:03d}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'))
        if ram[0xFA21]!=32 or struct.unpack_from('<I',ram,0xFA50)[0]!=root:raise ValueError('actual selector root/script')
        last={d['stream']:d for d in obs['draws']if d['stream']in wanted}
        if set(last)!=wanted:raise ValueError('normal full Korean glyph consumption')
        draws=[last[s]for s in sorted(wanted)]
        if any(divmod(d['offset']//4,2688)!=(geometry[d['stream']][0],geometry[d['stream']][1])for d in draws):raise ValueError('normal line geometry')
        counts=Counter(d['glyph_index']for d in draws);reads={x['index']:x['reads']for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('normal CPU font reads')
        pages.append(dict(route=name,step=step,**pixels(p,step,draws,e,rom,m,origin=(52,110),cursor_indices=())))
    held=rt/(PREFIX+'empty-hold');holdram=(held/'step_001_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',holdram,0xFA50)[0]!=root:raise ValueError('hold root lifetime')
    # Hold has no new glyph draws. Reuse entry geometry solely to verify
    # font OBJ residency/pixels; other VRAM includes native animated graphics.
    entry=rt/(PREFIX+'empty')
    hold_draws={d['stream']:d for d in read(entry/'step_002_roll_pet.json')['draws']if d['stream']in wanted}
    holdproof=pixels(held,1,[hold_draws[s]for s in sorted(wanted)],e,rom,m,origin=(52,110),cursor_indices=())
    close=(rt/(PREFIX+'empty-close')/'step_002_gbaExtWorkRam.bin').read_bytes()
    if close[0xFA21]!=10:raise ValueError('normal B return')
    result=dict(passed=True,rom_sha256=m['output_sha256'],normal_pages=pages,hold_residency=dict(no_new_draw_expected=True,font_OBJ_VRAM_pixels_verified=True,whole_VRAM_not_required_constant=True,**holdproof),normal_B_return_script=10,
        scope='Normal empty-item32: original LZ/RAM gate to raw-ROM clone, CPU/font/VRAM/pixels/hold/B/reentry. Other descriptions require matrix diagnostic/normal acquisition evidence.',release_eligible=False)
    (out/'selector_runtime.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    sheet=Image.new('RGB',(720,160))
    for i,(name,step)in enumerate([('empty',2),('empty-close',2),('empty-reenter',2)]):sheet.paste(Image.open(rt/(PREFIX+name)/f'step_{step:03d}.png'),(240*i,0))
    sheet.save(out/'selector_normal.png');print('Full-ROM normal selector/runtime PASS')
if __name__=='__main__':main()
