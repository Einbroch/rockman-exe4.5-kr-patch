"""Four fixed-cell save headings: source lookup, font, clear, BG and pixels."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha
from report_fixedcell_runtime import verify_route
from build_visibility_poc import require_hash
from tpl_literals import resolve_units
from archive_scripts import script_spans,verify_untouched_scripts
from fixedcell_font import bdf_cells,unpack_pixels
from korean_codec import encode_hangul

STEM='exe45_ko_development_save_labels_poc_v1'
PREFIX='save-labels-poc-v1-'

def main(surface=False):
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);require_hash(ROOT/f'poc/output/{STEM}_repro.gba',m['output_sha256']);rom=rp.read_bytes()
    cfg=read(ROOT/'project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/cfg['source_profile']['filename'],m['source_sha256'])
    asset=read(ROOT/('translations/rockman_roll_save_surface_ko.json' if surface else 'translations/rockman_roll_save_labels_ko.json'));units=resolve_units(asset);ar=next(a for a in m['archives'] if a['archive']=='6DA21C');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    pinned=next(a for a in m['translation_assets'] if a['archive']=='6DA21C');require_hash(ROOT/pinned['path'],pinned['sha256'])
    prior_units=resolve_units(read(ROOT/('translations/rockman_roll_save_labels_ko.json' if surface else 'translations/rockman_roll_save_ko.json')))
    if units[:len(prior_units)]!=prior_units or len(units)!=(37 if surface else 36) or m['translated_units']!=(1113 if surface else 1112) or len(m['archives'])!=21 or sha(payload)!=ar['compiled_sha256']:raise ValueError('asset/denominator/payload')
    native=source[0x6DA21C:0x6DA21C+9008];chosen=set(range(5))|set(range(10,14))|set(range(20,25))|({16} if surface else set());protected=verify_untouched_scripts(native,payload,120,chosen)
    if len(protected)!=(105 if surface else 106) or rom[0x6DA21C:0x6DA21C+9008]!=native or not all(ar[k] for k in ['protected_controls_unchanged','binary_roundtrip','semantic_roundtrip']):raise ValueError('protected source/slots/controls')
    for root in ar['pointers']:
        if struct.unpack_from('<I',rom,root)[0]!=pool:raise ValueError('save roots')
    previous=ROOT/('poc/output/exe45_ko_development_save_labels_poc_v1.gba' if surface else 'poc/output/exe45_ko_development_roll_save_poc_v1.gba');pm=read(previous.with_suffix('.json'));require_hash(previous,pm['output_sha256']);pr=previous.read_bytes();old=next(a for a in pm['archives'] if a['archive']=='6DA21C');os=script_spans(pr[old['rom_offset']:old['rom_offset']+old['compiled_bytes']],120);ns=script_spans(payload,120)
    if any(os[i]!=ns[i] for i in range(120) if i not in ({16} if surface else set(range(10,14)))):raise ValueError('previous protected save slots')
    for before in pm['archives']:
        if before['archive']=='6DA21C':continue
        now=next(a for a in m['archives'] if a['archive']==before['archive'])
        if before['compiled_sha256']!=now['compiled_sha256'] or pr[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]!=rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]:raise ValueError('previous20 payloads')
    rt=ROOT/'poc/runtime';p=rt/(PREFIX+'save-labels');verify_route(p,m['output_sha256'],set());env=read(p/'probe_environment.json');require_hash(ROOT/'tools/capture_fixedcell_probe.py',env['probe_sha256'])
    chain=['cold-part1','date','profile','navi-menu','select-roll','intro']
    for i,name in enumerate(chain):
        r=read(rt/(PREFIX+name)/'result.json')
        if (i==0 and r['state_origin'] is not None) or (i and Path(r['state_origin']).resolve()!=(rt/(PREFIX+chain[i-1])/'result.json').resolve()):raise ValueError('own cold chain')
    if Path(read(p/'result.json')['state_origin']).resolve()!=(rt/(PREFIX+'intro')/'result.json').resolve():raise ValueError('pre-load own-ROM origin')
    cp='step_011';calls=read(p/(cp+'_fixedcells.json'))['calls'];v=(p/(cp+'_gbaVideoRam.bin')).read_bytes();io=(p/(cp+'_display_io.bin')).read_bytes();state=read(p/(cp+'_state.json'))['state'];im=Image.open(p/(cp+'.png')).convert('RGB');fc=m['fixedcell_extension'];glyphs=bdf_cells(ROOT/fc['font']['path'],set('시간칩컵크레딧'),fc['raster']);pages=[]
    bg=struct.unpack_from('<H',io,8)[0];cb=((bg>>2)&3)*0x4000;sb=((bg>>8)&31)*0x800
    if bg&0xC080 or cb!=0x8000 or any(state[f'ppu.bgLayers[0].scroll{axis}'] for axis in ('X','Y')):raise ValueError('save BG format/scroll')
    for row,u in enumerate(units[32:36]):
        script=10+row;body=encode_hangul(u['translation'])+b'\xe5'
        if ns[script]!=body:raise ValueError('fixed label exact encoded script')
        stream=pool+struct.unpack_from('<H',payload,script*2)[0];target=0x06008400+row*512;matches=[c for c in calls if c['stream']==stream and c['target']==target]
        if len(matches)!=1:raise ValueError('native lookup/transfer')
        c=matches[0]
        if c['width']!=6 or c['height']!=1 or c['bytes']!=384 or len(c['glyphs'])!=6 or c['tint']!=0 or not c['complete'] or c['copy_target']!=target:raise ValueError('six-cell clear/transfer')
        records=[];pixels_checked=0
        for i,g in enumerate(c['glyphs']):
            offset=g['font']-0x08000000+g['index']*64;record=rom[offset:offset+64];records.append(record)
            if i<len(u['translation']):
                ch=u['translation'][i]
                if g['font']!=0x08000000+fc['font_offset'] or g['index']!=ord(ch)-0xAC00 or record!=glyphs[ch]:raise ValueError('BDF/glyph provider')
            elif g['index']!=0 or g['font']!=0x08601738 or record!=source[0x601738:0x601778]:raise ValueError('native blank clear')
            x=13+i;y=3+row*2;entries=[struct.unpack_from('<H',v,sb+(y+dy)*64+x*2)[0] for dy in (0,1)]
            if any(a&0xC00 or a>>12!=9 for a in entries):raise ValueError('save BG palette/flip')
            rendered=b''.join(v[cb+(a&1023)*32:cb+(a&1023)*32+32] for a in entries)
            if rendered!=record:raise ValueError('BG top/bottom consumption')
            pix=unpack_pixels(record)
            if i<len(u['translation']):
                colors=[]
                for role in (1,2):
                    wanted={(xx,yy) for yy,r in enumerate(pix) for xx,value in enumerate(r) if value==role}
                    actual_colors={im.getpixel((x*8+xx,y*8+yy)) for xx,yy in wanted}
                    if len(actual_colors)!=1:raise ValueError('visible ink/shadow role')
                    color=next(iter(actual_colors));actual={(xx,yy) for yy in range(16) for xx in range(8) if im.getpixel((x*8+xx,y*8+yy))==color}
                    if actual!=wanted:raise ValueError('visible glyph mask')
                    colors.append(color);pixels_checked+=len(wanted)
                if colors[0]==colors[1]:raise ValueError('ink/shadow contrast')
        stage=(p/f"fixed_{c['id']:04}_stage.bin").read_bytes()
        if stage!=b''.join(records) or v[target-0x06000000:target-0x06000000+384]!=stage:raise ValueError('font/stage/VRAM')
        pages.append({'script':script,'source':u['source'],'translation':u['translation'],'stream':stream,'target':target,'cells':6,'translated_cells':len(u['translation']),'native_blank_cells':6-len(u['translation']),'bg':0,'palette_bank':9,'ink_shadow_pixels':pixels_checked,'glyph_provider_stage_bg_screen_match':True})
    for name,before in env['files_before'].items():
        if name.endswith('.sav') and env['files_after'].get(name)!=before:raise ValueError('non-save label route modified save')
    commit=rt/(PREFIX+'save-commit');verify_route(commit,m['output_sha256'],set());ce=read(commit/'save_environment.json');sav=STEM+'.sav';rtc=STEM+'.rtc'
    if Path(read(commit/'result.json')['state_origin']).resolve()!=(p/'result.json').resolve() or ce['build_sha256']!=m['output_sha256'] or not ce['observer_only']:raise ValueError('native save own-ROM ancestry')
    before=ce['files_before'][sav];after=ce['files_after'][sav]
    if before!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or after['bytes']!=65536 or after==before or sha((commit/'persistent_files_after'/sav).read_bytes())!=after['sha256']:raise ValueError('native save disk edge')
    ram=(commit/'step_007_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=23:raise ValueError('native save success branch')
    for name in set(ce['files_before'])|set(ce['files_after']):
        if name not in (sav,rtc) and ce['files_before'].get(name)!=ce['files_after'].get(name):raise ValueError('unrelated saves changed')
    out=ROOT/('analysis/save_surface_poc_v1' if surface else 'analysis/save_labels_poc_v1');out.mkdir(parents=True,exist_ok=True);im.save(out/'save_labels.png');result={'passed':True,'policy':'functional-poc; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':1 if surface else 4,'selected_text_units':m['translated_units'],'protected_slots':len(protected),'previous_unchanged_save_slots':119 if surface else 116,'previous20_payloads_identical':True,'source_probe_route':'poc/runtime/save-labels-source-v1','source_native_font':'08601738','pages':pages,'tool_sha256':sha(Path(__file__).read_bytes()),'limits':['Four labels are rendered text, not four translated graphic assets.','Title and cup unit proof is separate save_surface report.' if surface else 'Top save title graphic and numeric-unit コ remain untranslated; numeric buffers preserved.','Shared common labels may serve other Navi saves; only normal Roll save entry is executed here.','No full-game, Hangul input/editing, old-save compatibility, RTC/audio/hardware or human release approval.']}
    result['native_save_regression']={'before':before,'after':after,'success_script':23,'screenshot_sha256':sha((commit/'step_007.png').read_bytes()),'scope':'Actual disk save and success transition, not persistence/reload or full-game/save compatibility.'}
    (out/'labels_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('four fixed save labels font/BG/pixels and native save: PASS');return result

if __name__=='__main__':main()
