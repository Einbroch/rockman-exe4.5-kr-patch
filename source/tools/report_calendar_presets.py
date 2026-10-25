"""Bounded default names: relocated data -> native copy -> mono display -> record -> query."""
import json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from report_roll_pet import read,pixels
from report_fixedcell_runtime import verify_route
from archive_scripts import script_spans,verify_untouched_scripts
from fixedcell_font import bdf_cells,unpack_pixels
from calendar_presets import validate,NAMES,SITE,END,EXPECTED
from korean_codec import encode_hangul
from run_calendar_presets import STEM,PREFIX

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read(ROOT/'project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    asset=read(ROOT/'translations/calendar_presets_ko.json');boundary=validate(asset['units']);ar=next(a for a in m['archives'] if a['archive']=='6368E8');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];pool=0x08000000+ar['rom_offset'];native=source[0x6368E8:0x6368E8+2337]
    manifest=next(a for a in m['translation_assets'] if a.get('archive')=='6368E8')
    if sha((ROOT/manifest['path']).read_bytes())!=manifest['sha256'] or (ROOT/manifest['path']).resolve()!=(ROOT/'translations/calendar_presets_ko.json').resolve() or sha(payload)!=ar['compiled_sha256'] or rom[0x6368E8:0x6368E8+2337]!=native:raise ValueError('preset source/asset/payload')
    if len(verify_untouched_scripts(native,payload,255,{0,60,62,63}))!=251 or ar['translated_units']!=4 or m['translated_units']!=1092 or len(m['archives'])!=21 or not all(ar[k] for k in ['protected_controls_unchanged','binary_roundtrip','semantic_roundtrip']):raise ValueError('preset denominator/protected scripts')
    for root in ar['pointers']:
        if struct.unpack_from('<I',rom,root)[0]!=pool:raise ValueError('preset archive references')
    previous=ROOT/'poc/output/exe45_ko_development_calendar_frequency_v1.gba';require_hash(previous,'43f7305a20ccc4acfff75815e9cde450fb22642a9c2012bd7d08ac97cd7da6ac');prev=previous.read_bytes();pm=read(previous.with_suffix('.json'))
    for before in pm['archives']:
        if before['archive']=='6368E8':continue
        now=next(a for a in m['archives'] if a['archive']==before['archive'])
        if rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]!=prev[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]:raise ValueError('other20 payload changed')
    oldar=next(a for a in pm['archives'] if a['archive']=='6368E8');ps=script_spans(payload,255);oldps=script_spans(prev[oldar['rom_offset']:oldar['rom_offset']+oldar['compiled_bytes']],255)
    if any(ps[i]!=oldps[i] for i in range(255) if i not in (62,63)):raise ValueError('prior253 scripts changed')
    if rom[0x63673C:0x6368E8]!=prev[0x63673C:0x6368E8] or source[SITE:END]!=EXPECTED:raise ValueError('frequency/source code')
    mono=m['fixedcell_extension']['mono_provider'];font=m['extension'];wanted=set('식사학원');fixedglyphs=bdf_cells(ROOT/mono['font']['path'],wanted,mono['raster'])
    normalglyphs=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],wanted)
    pages=[];sheet=Image.new('RGB',(480,320))
    for row,(kind,script,word,confirm,commit) in enumerate([('meal',62,'식사',5,7),('school',63,'학원',7,9)]):
        body=encode_hangul(word)+b'\xe5'
        if ps[script]!=body:raise ValueError('name bytes/terminator')
        p=ROOT/'poc/runtime'/(PREFIX+kind+'-register');verify_route(p,m['output_sha256'],set());env=read(p/'preset_path_environment.json')
        if not env['observer_only'] or env['self_sha256']!=sha((ROOT/'tools/capture_calendar_presets.py').read_bytes()) or env['fixed_probe_sha256']!=sha((ROOT/'tools/capture_fixedcell_probe.py').read_bytes()):raise ValueError('preset observer drift')
        cp=f'step_{confirm:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(p/(cp+'_preset_path.json'));calls=read(p/(cp+'_fixedcells.json'))['calls'];count=[c for c in trace['calls'] if c['pc']==0x08000000+END]
        start=pool+struct.unpack_from('<H',payload,script*2)[0];copy=[c for c in trace['calls'] if c['pc']==0x08032AC6 and c['registers'][0]==start and c['registers'][1]==0x02026080]
        if len(copy)!=1 or not count or count[-1]['registers'][1:4]!=[8,2,0x02026080] or ram[0x26080:0x26080+9]!=body:raise ValueError('ROM lookup/copy/length/RAM')
        found=[c for c in calls if c['target']==0x06014000 and c['bytes']==640 and len(c['glyphs'])==10]
        if len(found)!=1:raise ValueError('native name/clear fixed cells')
        call=found[0];records=[]
        for i,g in enumerate(call['glyphs']):
            at=g['font']-0x08000000+g['index']*64;record=rom[at:at+64];records.append(record)
            if i<2 and (g['font']!=0x08000000+mono['font_offset'] or g['index']!=ord(word[i])-0xAC00 or record!=fixedglyphs[word[i]]):raise ValueError('mono default glyph provider')
            if i>=2 and (g['index']!=0 or record!=source[0x619EF8:0x619EF8+64]):raise ValueError('native blank clear')
        stage=(p/f"fixed_{call['id']:04}_stage.bin").read_bytes();v=(p/(cp+'_gbaVideoRam.bin')).read_bytes()
        if stage!=b''.join(records) or v[0x14000:0x14280]!=stage:raise ValueError('fixed font/stage/VRAM')
        o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(p/(cp+'.png')).convert('RGB');visible=[]
        for j in range(128):
            a,b,k=struct.unpack_from('<HHH',o,j*8)
            if a&0x2300 or not 512<=k&1023<532:continue
            i=((k&1023)-512)//2
            if (k&1023)%2 or a>>14!=2 or b>>14!=0:raise ValueError('name OBJ cell')
            colors={}
            for yy,r in enumerate(unpack_pixels(records[i])):
                for xx,role in enumerate(r):colors.setdefault(role,set()).add(im.getpixel(((b&511)+xx,(a&255)+yy)))
            if any(len(c)!=1 for c in colors.values()) or (i<2 and len(colors)!=3):raise ValueError('name/blank screen mask')
            visible.append(i)
        if not set(range(2))<=set(visible):raise ValueError('both name glyphs visible')
        committed=(p/f'step_{commit:03}_gbaExtWorkRam.bin').read_bytes()
        rec=committed[0x1310:0x1330]
        header=bytes.fromhex('030000010106020000')+bytes([2 if kind=='meal' else 3])
        if rec[:10]!=header or rec[10:19]!=body or rec[19:]!=bytes(13):raise ValueError('committed32-byte record')
        q=ROOT/'poc/runtime'/(PREFIX+kind+'-query');verify_route(q,m['output_sha256'],set());qcp='step_005';qr=(q/(qcp+'_gbaExtWorkRam.bin')).read_bytes();draws=read(q/(qcp+'_preset_path.json'))['draws'];last={d['stream']:d for d in draws};addresses=[0x02010C40,0x02010C44];expected={}
        if qr[0x1310:0x1330]!=rec or qr[0x10C40:0x10C49]!=body or set(last)!=set(addresses):raise ValueError('same-session record/query buffer/glyphs')
        for ch,addr in zip(word,addresses):
            index=font['legacy_index_view']+ord(ch)-0xAC00;record=rom[font['normal_font_offset']+index*96:font['normal_font_offset']+(index+1)*96]
            if record!=normalglyphs[ch] or last[addr]['glyph_index']!=index:raise ValueError('normal name font provider')
            expected[addr]={'ch':ch,'index':index,'record':record,'id':'preset-query'}
        if [last[a]['offset'] for a in addresses]!=[10796,10844]:raise ValueError('query name exact positions')
        proof=pixels(q,5,[last[a] for a in addresses],expected,rom,m,cursor_indices=())
        sheet.paste(im,(row*240,0));sheet.paste(Image.open(q/(qcp+'.png')),(row*240,160));pages.append({'name':word,'normal_fixed_confirmation':confirm,'normal_commit':commit,'raw_name_bytes':body.hex(),'canonical_record':rec.hex(),'fixed_ten_cell_clear':True,'query_name_pixels':proof,'same_session_only':True})
    out=ROOT/'analysis/calendar_presets_poc_v1';out.mkdir(parents=True,exist_ok=True);sheet.save(out/'preset_pages.png')
    result={'passed':True,'policy':'functional-poc; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'source_sha256':sha(source),'translated_units':1092,'added_default_names':2,'boundary':boundary,'previous20_archive_payloads_identical':True,'previous253_scripts_identical_except62_63':True,'frequency_graphics_unchanged':True,'pages':pages,'tool_sha256':sha(Path(__file__).read_bytes()),'limits':['Default meal/school confirmation, commit and same-session query only.','Native keyboard/editing and save/power-cycle/fresh-process reload/Hangul input/other names remain unresolved.','No full-game, hardware, RTC/alarm/audio or human release approval.']}
    (out/'preset_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('normal two preset names QA: PASS');return result

if __name__=='__main__':main()
