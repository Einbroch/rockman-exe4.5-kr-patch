"""Normal calendar menu source->parser->1536-byte OBJ->pixel proof."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,verify_route
from fixedcell_font import bdf_cells,unpack_pixels
from archive_scripts import verify_untouched_scripts,script_spans
from korean_codec import encode_character
from calendar_menu_model import validate
from run_calendar_menu import STEM,PREFIX,OUTDIR
RTC_STEM=None

def main():
    m=read(ROOT/f'poc/output/{STEM}.json');rom=(ROOT/f'poc/output/{STEM}.gba').read_bytes();source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();asset=read(ROOT/'translations/calendar_menu_ko.json');boundary=validate(asset['units'])
    if sha(rom)!=m['output_sha256'] or sha(source)!=asset['source_sha256'] or sha((ROOT/f'poc/output/{STEM}_repro.gba').read_bytes())!=m['output_sha256']:raise ValueError('ROM identity')
    ar=next(a for a in m['archives'] if a['archive']=='6368E8');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    manifest=next(a for a in m['translation_assets'] if a['archive']=='6368E8')
    if sha((ROOT/manifest['path']).read_bytes())!=manifest['sha256'] or sha(payload)!=ar['compiled_sha256'] or sha(source[0x6368E8:0x6368E8+2337])!=asset['source_archive_sha256'] or rom[0x6368E8:0x6368E8+2337]!=source[0x6368E8:0x6368E8+2337]:raise ValueError('asset/source/payload')
    pointers=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6368E8']['pointers']
    if ar['pointers']!=pointers or len(pointers)!=15 or any(struct.unpack_from('<I',rom,p)[0]!=pool for p in pointers):raise ValueError('15 relocation roots')
    types=ar['translated_units']==2
    if types:
        from calendar_types_model import validate as types_validate
        selected=read(ROOT/'translations/calendar_types_ko.json');types_validate(selected['units'])
        if (ROOT/manifest['path']).resolve()!=(ROOT/'translations/calendar_types_ko.json').resolve():raise ValueError('type variant asset')
    untouched=verify_untouched_scripts(source[0x6368E8:0x6368E8+2337],payload,255,{0,60} if types else {0})
    if len(untouched)!=254-types or ar['translated_units']!=1+types or not all(ar[k] for k in ['protected_controls_unchanged','binary_roundtrip','semantic_roundtrip']):raise ValueError('scope/roundtrip')
    oldm=read(ROOT/'poc/output/exe45_ko_development_roll_schedule_alarm_v1.json');old=(ROOT/'poc/output/exe45_ko_development_roll_schedule_alarm_v1.gba').read_bytes()
    extra=next((a['translated_units'] for a in m['archives'] if a['archive']=='65F11C'),0)
    if sha(old)!=oldm['output_sha256'] or len(m['archives'])!=20+bool(extra) or m['translated_units']!=1075+extra+types:raise ValueError('baseline/denominator')
    for before in oldm['archives']:
        now=next(a for a in m['archives'] if a['archive']==before['archive'])
        if now['compiled_sha256']!=before['compiled_sha256'] or now['translated_units']!=before['translated_units'] or rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]!=old[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]:raise ValueError('previous19 payload drift')
    if m['pet_menu_graphics']['final_block_sha256']!=oldm['pet_menu_graphics']['final_block_sha256']:raise ValueError('previous graphics drift')
    profile=read(ROOT/'tools/specs/exe45_fixedcell_visibility_v1.json');font=ROOT/profile['font']['path']
    if sha(font.read_bytes())!=profile['font']['sha256']:raise ValueError('BDF identity')
    text=asset['units'][0]['translation'];cells=bdf_cells(font,{c for c in text if c!=' '},profile['raster']);font_at=m['fixedcell_extension']['font_offset']
    encoded=[];records=[];cursor=pool+struct.unpack_from('<H',payload,0)[0]
    for ch in text:
        data=bytes([0]) if ch==' ' else encode_character(ch);index=0 if ch==' ' else ord(ch)-0xAC00;provider=0x08601738 if ch==' ' else 0x08000000+font_at;record=source[0x601738:0x601738+64] if ch==' ' else cells[ch]
        if rom[provider-0x08000000+index*64:provider-0x08000000+(index+1)*64]!=record:raise ValueError('big Hangul/source space supply')
        encoded.append((cursor,index,provider));records.append(record);cursor+=len(data)
    if script_spans(payload,255)[0]!=b''.join(bytes([0]) if c==' ' else encode_character(c) for c in text)+b'\xe5':raise ValueError('menu encoding/terminator')
    path=ROOT/'poc/runtime'/(PREFIX+'calendar');r=verify_route(path,m['output_sha256'],set());env=read(path/'probe_environment.json')
    changed_files=sorted(k for k in set(env['files_before'])|set(env['files_after']) if env['files_before'].get(k)!=env['files_after'].get(k))
    if r.get('normal_play_checkpoint_eligible') is False or env['probe_sha256']!=sha((ROOT/'tools/capture_fixedcell_probe.py').read_bytes()) or set(changed_files)-{(RTC_STEM or STEM)+'.rtc'}:raise ValueError('observer/save isolation')
    source_path=ROOT/'poc/runtime/calendar-fixed-source-v1';verify_route(source_path,oldm['output_sha256'],set());reference=read(source_path/'step_002_fixedcells.json')['calls'][0];pages=[]
    for step in [2,3]:
        cp=f'step_{step:03}';calls=read(path/(cp+'_fixedcells.json'))['calls'];selected=[c for c in calls if c['stream']==encoded[0][0]]
        if len(selected)!=1:raise ValueError('normal menu caller population')
        call=selected[0]
        if not call['complete'] or call['bytes']!=1536 or len(call['glyphs'])!=24 or call['tint']!=0 or call['caller_lr']!=0x080554BA or call['copy_source']!=call['stage'] or call['copy_target']!=call['target']:raise ValueError('parser/copy boundary')
        for key in ['stage','target','width','height','font','tint','bytes','caller_lr']:
            if call[key]!=reference[key]:raise ValueError('native menu ABI/extent')
        for i,(g,(stream,index,provider)) in enumerate(zip(call['glyphs'],encoded)):
            if (g['stream'],g['index'],g['font'],g['destination'])!=(stream,index,provider,call['stage']+i*64):raise ValueError('decoded menu cell identity')
        staged=(path/f"fixed_{call['id']:04d}_stage.bin").read_bytes();v=(path/(cp+'_gbaVideoRam.bin')).read_bytes();target=call['target']-0x06000000
        if staged!=b''.join(records) or v[target:target+1536]!=staged:raise ValueError('font->stage->VRAM')
        im=Image.open(path/(cp+'.png')).convert('RGB');o=(path/(cp+'_gbaSpriteRam.bin')).read_bytes();old_o=(source_path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();pal=(path/(cp+'_gbaPaletteRam.bin')).read_bytes();proof=[]
        for i,ch in enumerate(text):
            if ch==' ':continue
            tile=(target-0x10000)//32+i*2
            matches=[j for j in range(128) if struct.unpack_from('<H',o,j*8+4)[0]&1023==tile]
            if len(matches)!=1:raise ValueError('unique menu OBJ tile consumer')
            j=matches[0];a,b,k=struct.unpack_from('<HHH',o,j*8)
            if o[j*8:j*8+6]!=old_o[j*8:j*8+6] or a&0x2300 or a>>14!=2 or b>>14!=0:raise ValueError('source menu OAM geometry/palette')
            x=b&511;y=a&255
            # Source/candidate screen role equality avoids guessing Mesen's
            # 5-bit color conversion LUT, while the palette must stay native.
            old_im=Image.open(source_path/f'step_{step:03}.png').convert('RGB');observed={}
            for yy,row in enumerate(unpack_pixels(records[i])):
                for xx,role in enumerate(row):
                    if role:observed.setdefault(role,set()).add(im.getpixel((x+xx,y+yy)))
            if any(len(observed.get(role,set()))!=1 for role in [1,2]) or observed[1]==observed[2]:raise ValueError('menu ink/shadow roles')
            native=reference['glyphs'][i];native_at=native['font']-0x08000000+native['index']*64;native_record=old[native_at:native_at+64];native_colors={}
            for yy,row in enumerate(unpack_pixels(native_record)):
                for xx,role in enumerate(row):
                    if role:native_colors.setdefault(role,set()).add(old_im.getpixel((x+xx,y+yy)))
            if observed!=native_colors:raise ValueError('source/candidate palette role colors')
            # Compare current palette to immutable source-reference palette;
            # menu palette stays native while font pixels change.
            old_pal=(source_path/f'step_{step:03}_gbaPaletteRam.bin').read_bytes()
            if pal[0x200+(k>>12)*32:0x200+(k>>12)*32+32]!=old_pal[0x200+(k>>12)*32:0x200+(k>>12)*32+32]:raise ValueError('menu palette drift')
            for yy,row in enumerate(unpack_pixels(records[i])):
                for xx,role in enumerate(row):
                    color=im.getpixel((x+xx,y+yy))
                    if role and color!=next(iter(observed[role])):raise ValueError('screenshot glyph mask')
                    if not role and color in set().union(*observed.values()):raise ValueError('stale source ink/shadow')
            proof.append({'character':ch,'cell':i,'sprite':j,'xy':[x,y],'pixels':128,'record_sha256':sha(records[i]),'native_geometry_palette_preserved':True})
        pages.append({'step':step,'source_stage_vram_bytes':1536,'decoded_cells':24,'translated_cell_pixels':proof,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes())})
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'normal_runtime_units':['6368E8:0:0'],'diagnostic_runtime_units':[],'new_units':1,'translated_operation_labels':3,'boundary':boundary,'protected_scripts':254-types,'previous19_payloads_identical':True,'root_pointers_verified':15,'pages':pages,'isolated_environment_changes':changed_files,'limits':['Operation-menu proof only; type-menu variant needs its own report. Native basic names/input remain Japanese.','Isolated emulator RTC sidecar updated normally; no persistent save/reload or RTC correctness claim.','No Hangul input, RTC alarm/hardware/audio/full-game or human approval.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'calendar_menu_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('normal calendar menu QA',True);return result

def regressions():
    import report_roll_schedule_alarm as base
    import report_roll_schedule_time as time
    for mod in [base,time]:mod.STEM=STEM;mod.PREFIX=PREFIX;mod.OUTDIR=OUTDIR
    base.regressions();time.main()

if __name__=='__main__':main();regressions()
