"""Exact heading33 product/write audit and native mono BG scanout evidence."""
import json,struct
from PIL import Image,ImageDraw
from report_roll_pet import ROOT,read,sha,require_hash
from archive_scripts import script_spans
from fixedcell_font import bdf_cells,unpack_pixels
from report_fixedcell_runtime import verify_route
from input_heading import validate,CHILD,ADDED
from run_input_heading import STEM,PREFIX
from keyitem_rom_data import verify_final

def main():
    out=ROOT/'analysis/input_heading_v1';out.mkdir(exist_ok=True)
    m=read(ROOT/f'poc/output/{STEM}.json');rp=ROOT/f'poc/output/{STEM}.gba';require_hash(rp,m['output_sha256']);require_hash(ROOT/f'poc/output/{STEM}_repro.gba',m['output_sha256']);rom=rp.read_bytes()
    srcp=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(srcp,m['source_sha256']);src=srcp.read_bytes();rebuilt=bytearray(src);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];value=bytes.fromhex(w['final_hex'])
        if len(value)!=n or src[at:at+n]!=bytes.fromhex(w['expected_hex']) or occupied.intersection(range(at,at+n)):raise ValueError('write ledger')
        occupied.update(range(at,at+n));rebuilt[at:at+n]=value
    if rebuilt!=rom[:len(src)] or rom[:192]!=src[:192] or len(rom)!=len(src)+m['append_bytes'] or sha(rom[len(src):])!=m['append_sha256']:raise ValueError('source/header/ledger/append')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    asset=read(ROOT/CHILD);validate(asset)
    oldm=read(ROOT/'poc/output/exe45_ko_development_input_confirmation_v1_r3.json');oldp=ROOT/'poc/output/exe45_ko_development_input_confirmation_v1_r3.gba';require_hash(oldp,oldm['output_sha256']);old=oldp.read_bytes()
    prior={a['archive']:a for a in oldm['archives']};current={a['archive']:a for a in m['archives']}
    if set(prior)!=set(current) or m['translated_units']!=oldm['translated_units']+1:raise ValueError('selected population')
    common=current['6368E8'];previous=prior['6368E8'];payload=rom[common['rom_offset']:common['rom_offset']+common['compiled_bytes']];sp=script_spans(payload,255);osp=script_spans(old[previous['rom_offset']:previous['rom_offset']+previous['compiled_bytes']],255)
    if any(sp[i]!=osp[i] for i in range(255) if i!=33) or not all(common[k] for k in ['binary_roundtrip','semantic_roundtrip','protected_controls_unchanged']):raise ValueError('254 unchanged scripts/roundtrip')
    root=0x08000000+common['rom_offset'];stream=root+struct.unpack_from('<H',payload,33*2)[0]
    if len(common['pointers'])!=15 or any(struct.unpack_from('<I',rom,p)[0]!=root for p in common['pointers']):raise ValueError('15 common roots')
    for name,a in prior.items():
        b=current[name]
        if name!='6368E8' and old[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']]:raise ValueError('other payload '+name)
    if rom[0x6368e8:0x6368e8+2337]!=src[0x6368e8:0x6368e8+2337]:raise ValueError('source archive')
    for key in ['normal_font_offset','advance_offset']:
        n=(m['extension']['legacy_index_view']+11172+m['extension']['extra_glyph_count'])*(96 if key=='normal_font_offset' else 4)
        a=oldm['extension'][key];b=m['extension'][key]
        if old[a:a+n]!=rom[b:b+n]:raise ValueError('normal supply drift')
    for a,b in [(oldm['fixedcell_extension']['font_offset'],m['fixedcell_extension']['font_offset']),(oldm['fixedcell_extension']['mono_provider']['font_offset'],m['fixedcell_extension']['mono_provider']['font_offset'])]:
        if old[a:a+11172*64]!=rom[b:b+11172*64]:raise ValueError('fixed bank drift')
    for key in ['calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics']:
        a,b=oldm[key],m[key];at=b['source_offset'];n=b.get('stored_bytes',b.get('bytes'))
        if a!=b or old[at:at+n]!=rom[at:at+n]:raise ValueError('graphics drift')
    verify_final(src,rom,m['keyitem_rom']);a,b=oldm['keyitem_rom'],m['keyitem_rom']
    if old[a['rom_offset']:a['rom_offset']+a['rom_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['rom_bytes']]:raise ValueError('keyitem39')
    rt=ROOT/'poc/runtime';seen=set();routes={}
    for name in ['header','typed','confirmation','no','yes']:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen)
        if any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('intervention')
        routes[name]=dict(result_sha256=sha((p/'result.json').read_bytes()),actions=r['actions'])
    p=rt/(PREFIX+'header');calls=read(p/'step_004_fixedcells.json')['calls'];h=[c for c in calls if c['stream']==stream]
    if len(h)!=1:raise ValueError('heading stream');
    h=h[0]
    if (h['width'],h['height'],h['font'],h['stage'],h['target'],h['bytes'],h['tint'])!=(2,10,0x08619ef8,0x0201c800,0x0600b800,1280,0) or not h['complete']:raise ValueError('native header geometry')
    mono=m['fixedcell_extension']['mono_provider'];wanted={c for c in ADDED['translation'] if '\uac00'<=c<='\ud7a3'};cells=bdf_cells(ROOT/mono['font']['path'],wanted,mono['raster'])
    table={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    expected=[];providers=[]
    for ch in ADDED['translation'].ljust(20):
        if ch in cells:index=ord(ch)-0xac00;font=0x08000000+mono['font_offset'];cell=cells[ch]
        else:
            code=table[ch]
            if len(code)!=1:raise ValueError('legacy single-byte punctuation')
            index=code[0];font=0x08619ef8;cell=src[0x619ef8+index*64:0x619ef8+(index+1)*64]
        expected.append(cell);providers.append((font,index))
    stage=(p/f"fixed_{h['id']:04}_stage.bin").read_bytes();video=(p/'step_004_gbaVideoRam.bin').read_bytes()
    if stage!=b''.join(expected) or [(g['font'],g['index']) for g in h['glyphs']]!=providers or video[0xb800:0xbd00]!=stage:raise ValueError('font->stage->VRAM')
    native=rt/'input-entry-v1-header-source';verify_route(native,oldm['output_sha256'],set());oldh=read(native/'step_004_fixedcells.json')['calls'][0];oldstage=(native/f"fixed_{oldh['id']:04}_stage.bin").read_bytes();oldvideo=(native/'step_004_gbaVideoRam.bin').read_bytes()
    if oldvideo[0xb800:0xbd00]!=oldstage:raise ValueError('native resident header')
    before=Image.open(native/'step_004.png').convert('RGB');shot=Image.open(p/'step_004.png').convert('RGB');rolecolors={}
    palette=(p/'step_004_gbaPaletteRam.bin').read_bytes();oldpalette=(native/'step_004_gbaPaletteRam.bin').read_bytes()
    for j in range(10):
        for y,row in enumerate(unpack_pixels(oldstage[j*64:(j+1)*64])):
            for x,role in enumerate(row):
                color=before.getpixel((24+j*8+x,32+y));raw=struct.unpack_from('<H',oldpalette,0x140+role*2)[0]
                if role in rolecolors and rolecolors[role]!=(color,raw):raise ValueError('source role colors')
                rolecolors[role]=(color,raw)
    io=(p/'step_004_display_io.bin').read_bytes();ctrl=struct.unpack_from('<H',io,12)[0]
    if ctrl!=0x1e4a:raise ValueError('BG2 header tile geometry')
    for j in range(10):
        entries=[struct.unpack_from('<H',video,0xf000+(4+dy)*64+(3+j)*2)[0] for dy in [0,1]]
        if entries!=[0xa1c0+j*2,0xa1c1+j*2]:raise ValueError('header tile map')
        for y,row in enumerate(unpack_pixels(expected[j])):
            for x,role in enumerate(row):
                color,raw=rolecolors[role]
                if struct.unpack_from('<H',palette,0x140+role*2)[0]!=raw or shot.getpixel((24+j*8+x,32+y))!=color:raise ValueError('header scanout pixels')
    def ram(name,step):return (rt/(PREFIX+name)/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
    typed=ram('typed',8);deleted=ram('typed',4);no=ram('no',4);yes=ram('yes',3)
    if deleted[0xfc80:0xfc85]!=bytes.fromhex('98989898e5') or typed[0xfc80:0xfc85]!=bytes.fromhex('9b989898e5') or no[0xfc80:0xfc90]!=typed[0xfc80:0xfc90] or no[0x10a6:0x10ad]!=typed[0x10a6:0x10ad] or yes[0x10a6:0x10ad].hex()!='019be57ee50000' or yes[0xfa21]!=93:raise ValueError('edit/delete/No/Yes regression')
    noimage=Image.open(rt/(PREFIX+'no')/'step_004.png').convert('RGB')
    if noimage.crop((24,32,104,48)).tobytes()!=shot.crop((24,32,104,48)).tobytes():raise ValueError('header No return residency')
    cpu=read(ROOT/'analysis/input_heading_v1_cpu.json')
    if cpu['rom_sha256']!=m['output_sha256'] or cpu['vectors']!=22390:raise ValueError('CPU binding')
    sheet=Image.new('RGB',(720,188),'white');d=ImageDraw.Draw(sheet)
    for i,(path,label) in enumerate([(native/'step_004.png','source heading'),(p/'step_004.png','Korean native heading33'),(rt/(PREFIX+'no')/'step_004.png','No: title and input retained')]):d.text((i*240+4,3),label,fill='black');sheet.paste(Image.open(path).convert('RGB'),(i*240,24))
    sheet.save(out/'heading_pages.png')
    report=dict(passed=True,release_eligible=False,rom_sha256=m['output_sha256'],selected_literals=m['translated_units'],added_literals=1,parent16_and_other254_scripts_preserved=True,other59_payloads_preserved=True,source_header_ledger_append_verified=True,all15_common_roots_verified=True,normal_big_mono_fonts_graphics_keyitem39_preserved=True,header_stream=stream,header_geometry=dict(stage=h['stage'],target=h['target'],bytes=1280,visible_cells=10,origin=[24,32]),glyphs20=providers,stage_sha256=sha(stage),pixel_count=1280,exact_BG2_palette_pixels=True,edit_delete_No_Yes_regressions=True,routes=routes,cpu_sha256=sha((ROOT/'analysis/input_heading_v1_cpu.json').read_bytes()),pages_sha256=sha((out/'heading_pages.png').read_bytes()),tool_sha256=sha(__import__('pathlib').Path(__file__).read_bytes()),limits=['Only heading33 translated; other keyboard labels/input headers remain Japanese.','Native Japanese editing/commit regression only, not Hangul input/record/save support.','Own-ROM baseline native save/cold continue predates entered answer; no transfer of old-ROM input persistence claim.','Other heading consumers, whole-game translation, images, shop/RTC and human review/release remain pending.'])
    (out/'runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('PASS header33 mono BG2 1280pixels, product preservation and edit/confirm regressions')
if __name__=='__main__':main()
