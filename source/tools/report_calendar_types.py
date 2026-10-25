"""Normal whole27-cell type pool -> native OBJ segments -> pixels/scroll."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,verify_route
from archive_scripts import script_spans,verify_untouched_scripts
from calendar_types_model import validate
from fixedcell_font import bdf_cells,unpack_pixels
from korean_codec import encode_character
from run_calendar_types import STEM as CAPTURE_STEM,PREFIX,OUTDIR
STEM='exe45_ko_development_calendar_types_v2'
TOTAL_UNITS=1087

def main():
    m=read(ROOT/f'poc/output/{STEM}.json');rom=(ROOT/f'poc/output/{STEM}.gba').read_bytes();source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();asset=read(ROOT/'translations/calendar_types_ko.json');boundary=validate(asset['units'])
    if sha(rom)!=m['output_sha256'] or sha((ROOT/f'poc/output/{STEM}_repro.gba').read_bytes())!=m['output_sha256'] or sha(source)!=asset['source_sha256']:raise ValueError('source/repro identity')
    capture_rom=ROOT/f'poc/output/{CAPTURE_STEM}.gba'
    if capture_rom.read_bytes()!=rom:raise ValueError('normal capture artifact byte identity')
    from build_development_patch import selected_scope,literal_scope
    adopted=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6368E8'],asset)
    if literal_scope(adopted,'6368E8:60:0')['consumer']!='fixed-cell-mono':raise ValueError('native mono adopted scope')
    ar=next(a for a in m['archives'] if a['archive']=='6368E8');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];pool=0x8000000+ar['rom_offset'];native=source[0x6368E8:0x6368E8+2337]
    manifest=next(a for a in m['translation_assets'] if a['archive']=='6368E8')
    if (ROOT/manifest['path']).resolve()!=(ROOT/'translations/calendar_types_ko.json').resolve() or sha((ROOT/manifest['path']).read_bytes())!=manifest['sha256'] or sha(payload)!=ar['compiled_sha256'] or sha(native)!=asset['source_archive_sha256'] or rom[0x6368E8:0x6368E8+2337]!=native:raise ValueError('protected source/asset/payload')
    if len(verify_untouched_scripts(native,payload,255,{0,60}))!=253 or ar['translated_units']!=2 or m['translated_units']!=TOTAL_UNITS or len(m['archives'])!=21 or not all(ar[k] for k in ['protected_controls_unchanged','binary_roundtrip','semantic_roundtrip']):raise ValueError('scope/roundtrip')
    pointers=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6368E8']['pointers']
    if len(pointers)!=15 or ar['pointers']!=pointers or any(struct.unpack_from('<I',rom,p)[0]!=pool for p in pointers):raise ValueError('15roots')
    oldm=read(ROOT/'poc/output/exe45_ko_development_roll_calendar_content_v1.json');old=(ROOT/'poc/output/exe45_ko_development_roll_calendar_content_v1.gba').read_bytes()
    if sha(old)!=oldm['output_sha256']:raise ValueError('old identity')
    date_intro=next(a for a in m['archives'] if a['archive']=='65F11C')['translated_units']==14
    for a in oldm['archives']:
        now=next(x for x in m['archives'] if x['archive']==a['archive'])
        before=old[a['rom_offset']:a['rom_offset']+a['compiled_bytes']];after=rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]
        if a['archive']=='6368E8':
            if len(verify_untouched_scripts(before,after,255,{60}))!=254:raise ValueError('prior254 scripts')
        elif date_intro and a['archive']=='65F11C':
            entry=next(x for x in m['translation_assets'] if x['archive']=='65F11C')
            if (ROOT/entry['path']).resolve()!=(ROOT/'translations/roll_calendar_date_ko.json').resolve() or sha((ROOT/entry['path']).read_bytes())!=entry['sha256'] or len(verify_untouched_scripts(before,after,255,{0}))!=254:raise ValueError('registered date extension/prior254 scripts')
        elif before!=after or a['compiled_sha256']!=now['compiled_sha256']:raise ValueError('previous20 other payloads')
    if m['pet_menu_graphics']['final_block_sha256']!=oldm['pet_menu_graphics']['final_block_sha256']:raise ValueError('graphics drift')
    profile=read(ROOT/'tools/specs/exe45_fixedcell_visibility_v1.json');font=ROOT/profile['font']['path']
    if sha(font.read_bytes())!=profile['font']['sha256']:raise ValueError('BDF identity')
    mono=m['fixedcell_extension']['mono_provider'];ms=read(ROOT/'tools/specs/exe45_fixedcell_mono_v1.json')
    if sha((ROOT/mono['spec_path']).read_bytes())!=mono['spec_sha256'] or mono['native_font']!=ms['native_font'] or mono['roles']!=ms['roles'] or sha(source[ms['native_font']['offset']:ms['native_font']['offset']+ms['native_font']['bytes']])!=ms['native_font']['sha256']:raise ValueError('mono source/spec')
    text=asset['units'][1]['translation'];cells=bdf_cells(font,{c for c in text if '\uac00'<=c<='\ud7a3'},mono['raster']);codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1};records=[];decoded=[];cursor=pool+struct.unpack_from('<H',payload,120)[0];encoded=b''
    for ch in text:
        hangul='\uac00'<=ch<='\ud7a3';data=encode_character(ch) if hangul else codes[ch];index=ord(ch)-0xAC00 if hangul else data[0];provider=0x8000000+mono['font_offset'] if hangul else 0x08619EF8;record=cells[ch] if hangul else source[0x619EF8+index*64:0x619EF8+(index+1)*64]
        if rom[provider-0x8000000+index*64:provider-0x8000000+(index+1)*64]!=record:raise ValueError('provider')
        decoded.append((cursor,index,provider));records.append(record);encoded+=data;cursor+=len(data)
    if script_spans(payload,255)[60]!=encoded+b'\xe5':raise ValueError('encoded selector/terminator')
    p=ROOT/'poc/runtime'/(PREFIX+'time');cp='step_006';verify_route(p,m['output_sha256'],set());calls=read(p/(cp+'_fixedcells.json'))['calls'];selected=[c for c in calls if c['stream']==decoded[0][0]]
    if len(selected)!=1:raise ValueError('normal whole-pool call')
    c=selected[0];refp=ROOT/'poc/runtime/roll-calendar-content-v1-time';verify_route(refp,oldm['output_sha256'],set());ref=read(refp/(cp+'_fixedcells.json'))['calls'][0]
    for k in ['stage','target','width','height','font','tint','bytes','caller_lr']:
        if c[k]!=ref[k]:raise ValueError('native call ABI')
    if not c['complete'] or c['bytes']!=1728 or len(c['glyphs'])!=27 or c['caller_lr']!=0x80554BA or ref['font']!=0x08619EF8:raise ValueError('27cell extent/native source font')
    for i,(g,triple) in enumerate(zip(c['glyphs'],decoded)):
        if (g['stream'],g['index'],g['font'],g['destination'])!=(*triple,c['stage']+i*64):raise ValueError('decoded cell identity')
    staged=(p/f"fixed_{c['id']:04d}_stage.bin").read_bytes()
    if staged!=b''.join(records):raise ValueError('ROMfont->staging')
    coverage=set();pages=[];tile=(c['target']-0x6010000)//32
    samples=[(p,6,refp,6)]+[(ROOT/'poc/runtime'/(PREFIX+'types-scroll'),i,ROOT/'poc/runtime/calendar-types-source-v1',i) for i in (2,4,6,8)]
    for path,step,source_path,source_step in samples:
        verify_route(path,m['output_sha256'],set());verify_route(source_path,oldm['output_sha256'],set());cp=f'step_{step:03}';scp=f'step_{source_step:03}';env=read(path/'probe_environment.json')
        if env['probe_sha256']!=sha((ROOT/'tools/capture_fixedcell_probe.py').read_bytes()):raise ValueError('observer identity')
        changed={k for k in set(env['files_before'])|set(env['files_after']) if env['files_before'].get(k)!=env['files_after'].get(k)}
        if changed-{CAPTURE_STEM+'.rtc'}:raise ValueError('save isolation')
        v=(path/(cp+'_gbaVideoRam.bin')).read_bytes();o=(path/(cp+'_gbaSpriteRam.bin')).read_bytes();so=(source_path/(scp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(path/(cp+'.png')).convert('RGB');sim=Image.open(source_path/(scp+'.png')).convert('RGB');pal=(path/(cp+'_gbaPaletteRam.bin')).read_bytes();spal=(source_path/(scp+'_gbaPaletteRam.bin')).read_bytes();visible=[]
        if v[c['target']-0x6000000:c['target']-0x6000000+1728]!=staged:raise ValueError('staging->VRAM residency')
        # Native scroll-up arrow sprite0 can cover the first row of cell10.
        # Keep glyph VRAM proof intact; only its opaque pixels use overlay proof.
        overlay=set();aa0,bb0,kk0=struct.unpack_from('<HHH',o,0);sv=(source_path/(scp+'_gbaVideoRam.bin')).read_bytes()
        if not aa0&0x2300 and (aa0,bb0,kk0)==(0x11,0x38,0xC6D1):
            if o[:6]!=so[:6]:raise ValueError('native scroll arrow OAM')
            at=0x10000+(kk0&1023)*32;bank=0x200+(kk0>>12)*32
            if v[at:at+32]!=sv[at:at+32] or pal[bank:bank+32]!=spal[bank:bank+32]:raise ValueError('native scroll arrow residency/palette')
            arrow_colors={}
            for yy in range(8):
                for xx in range(8):
                    role=(v[at+yy*4+xx//2]>>(4*(xx%2)))&15
                    if role:
                        xy=((bb0&511)+xx,(aa0&255)+yy)
                        arrow_colors.setdefault(role,set()).add(im.getpixel(xy))
                        overlay.add(xy)
            if any(len(colors)!=1 for colors in arrow_colors.values()):raise ValueError('current arrow shape/color consistency')
        for j in range(128):
            aa,bb,kk=struct.unpack_from('<HHH',o,j*8)
            if aa&0x2300 or not tile<=kk&1023<tile+54:continue
            i=((kk&1023)-tile)//2
            if ((kk&1023)-tile)%2 or o[j*8:j*8+6]!=so[j*8:j*8+6] or aa>>14!=2 or bb>>14!=0:raise ValueError('native segment OAM geometry')
            x=bb&511;y=aa&255;sg=ref['glyphs'][i];sr=old[sg['font']-0x8000000+sg['index']*64:sg['font']-0x8000000+(sg['index']+1)*64];colors={}
            for yy,row in enumerate(unpack_pixels(sr)):
                for xx,role in enumerate(row):
                    if (x+xx,y+yy) not in overlay:colors.setdefault(role,set()).add(sim.getpixel((x+xx,y+yy)))
            if any(len(colors.get(role,set()))!=1 for role in (1,3,4)):raise ValueError('source mono palette role colors')
            for yy,row in enumerate(unpack_pixels(records[i])):
                for xx,role in enumerate(row):
                    if (x+xx,y+yy) in overlay:continue
                    if im.getpixel((x+xx,y+yy))!=next(iter(colors[role])):raise ValueError('type screen font/no stale source pixels')
            bank=0x200+(kk>>12)*32
            if pal[bank:bank+32]!=spal[bank:bank+32]:raise ValueError('native palette')
            coverage.add(i);visible.append({'cell':i,'character':text[i],'xy':[x,y],'sprite':j,'pixels':128})
        pages.append({'step':step,'route':path.name,'visible_cells':visible,'native_arrow_opaque_pixels':len(overlay),'arrow_proof':'Source OAM/VRAM/palette identity and current opaque shape/color consistency; source screenshot RGB equality not claimed. Underlying glyph pixels proved by exact full VRAM.','screenshot_sha256':sha((path/(cp+'.png')).read_bytes())})
    if not set(range(22))<=coverage:raise ValueError('all5 visible labels not covered')
    result={'passed':True,'release_eligible':False,'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],'new_units':1,'translated_visible_labels':5,'boundary':boundary,'protected_scripts':253,'previous20_other_payloads_identical':True,'previous254_scripts_identical_except60':True,'root_pointers_verified':15,'normal_runtime_units':['6368E8:60:0'],'diagnostic_runtime_units':[],'pages':pages,'limits':['Selector labels only; raw basic names, input/confirmation/query/persistence remain native Japanese.','Sixth ????? supplied unchanged but not selectable/visible in this route.','No Hangul input, persistent save/reload, RTC alarm, hardware/audio/full-game or human approval.']}
    result['runtime_artifact']=CAPTURE_STEM;result['verified_artifact']=STEM;result['runtime_and_verified_rom_bytes_identical']=True;result['normal_native_font']='08619EF8 mono; native roles1/3/4; existing F9FC mono bank'
    result['previous20_other_payloads_identical']=not date_intro;result['previous19_other_payloads_identical']=True;result['calendar_date_intro_extension']=date_intro
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'types_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');sheet=Image.new('RGB',(480,160));sheet.paste(Image.open(p/'step_006.png'),(0,0));sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+'types-scroll')/'step_008.png'),(240,0));sheet.save(out/'types_pages.png');print('normal calendar types QA',True);return result

def regressions():
    import report_calendar_menu as menu
    menu.RTC_STEM=CAPTURE_STEM
    import report_roll_calendar_content as content
    content.UNIT_COUNT=next(a for a in read(ROOT/f'poc/output/{STEM}.json')['archives'] if a['archive']=='65F11C')['translated_units']
    content.STEM=STEM;content.PREFIX=PREFIX;content.OUTDIR=OUTDIR;content.main()
if __name__=='__main__':main();regressions()
