"""Finite normal five-script calendar dialogue and choice pixel evidence."""
import json,struct
from collections import Counter
from PIL import Image
from archive_scripts import script_spans
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from run_roll_calendar_dialogue import STEM,PREFIX,OUTDIR
ASSET='roll_calendar_dialogue_ko.json'
UNIT_COUNT=9
SAMPLES=[('calendar',4,1),('calendar',5,2),('calendar',6,20),('time',5,21),('meal',5,24)]

def main():
    m,rom,e,streams,checks=static(STEM,'65F11C');ar=next(a for a in m['archives'] if a['archive']=='65F11C');pool=0x08000000+ar['rom_offset'];units={u['id']:u for u in read(ROOT/'translations'/ASSET)['units']};oldm=read(ROOT/'poc/output/exe45_ko_development_calendar_menu_v1.json');old=(ROOT/'poc/output/exe45_ko_development_calendar_menu_v1.gba').read_bytes()
    types=next(a for a in m['archives'] if a['archive']=='6368E8')['translated_units']==2
    if sha(old)!=oldm['output_sha256'] or len(m['archives'])!=21 or m['translated_units']!=1075+UNIT_COUNT+types:raise ValueError('baseline/denominator')
    for before in oldm['archives']:
        now=next(a for a in m['archives'] if a['archive']==before['archive'])
        if types and before['archive']=='6368E8':
            asset=next(a for a in m['translation_assets'] if a['archive']=='6368E8')
            if (ROOT/asset['path']).resolve()!=(ROOT/'translations/calendar_types_ko.json').resolve() or sha((ROOT/asset['path']).read_bytes())!=asset['sha256']:raise ValueError('registered type variant identity')
            if script_spans(rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']],255)[0]!=script_spans(old[before['rom_offset']:before['rom_offset']+before['compiled_bytes']],255)[0]:raise ValueError('operation menu script drift')
            continue
        if now['compiled_sha256']!=before['compiled_sha256'] or now['translated_units']!=before['translated_units'] or rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]!=old[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]:raise ValueError('previous20 payload drift')
    covered=set();pages=[]
    samples=SAMPLES
    for route,step,script in samples:
        path=ROOT/'poc/runtime'/(PREFIX+route);r=verify_route(path,m['output_sha256'],set());env=read(path/'calendar_dialogue_environment.json')
        if env['rom_sha256']!=m['output_sha256'] or not env['observer_only'] or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('normal observer identity')
        for name,key in [('capture_roll_calendar_dialogue.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256'),('capture_fixedcell_probe.py','fixed_probe_sha256')]:
            if sha((ROOT/'tools'/name).read_bytes())!=env[key]:raise ValueError('observer drift')
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();state=read(path/(cp+'_roll_pet.json'));keys=[k for k in units if int(k.split(':')[1])==script];selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
        if ram[0xFA21]!=script or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or set(last)!=set(selected):raise ValueError('active normal script/full selected streams')
        draws=[last[s] for s in selected]
        if any(d['context']!=0x0200FA20 for d in draws):raise ValueError('normal dialogue context')
        for key in keys:
            offsets=[d['offset'] for d in draws if d['stream'] in streams[key]]
            # The source commands define newline and selection-row placement.
            # The first glyph offset is native-command-derived at runtime;
            # subsequent offsets must match exact translated advances.
            row,start=divmod(offsets[0],10752);advance=start//4;cursor=iter(streams[key])
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;advance=0;continue
                s=next(cursor)
                if last[s]['offset']!=row*10752+advance*4:raise ValueError('within-literal exact geometry')
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
        counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU font supply')
        indices=(16,) if script==2 else (3,) if script==24 else ()
        source_o=(ROOT/'poc/runtime'/('calendar-menu-v1-'+route)/(cp+'_gbaSpriteRam.bin')).read_bytes() if indices else b'';current_o=(path/(cp+'_gbaSpriteRam.bin')).read_bytes()
        for i in indices:
            a,b,k=struct.unpack_from('<HHH',current_o,i*8);old_a,old_b,old_k=struct.unpack_from('<HHH',source_o,i*8)
            if (a,b,k)!=(old_a,old_b,old_k):raise ValueError('native default cursor position/geometry')
        proof=pixels(path,step,draws,e,rom,m,origin=(52,110),cursor_screen_background=True,cursor_indices=indices)
        im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=52+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        # Choice cursor is an independent native OBJ; verify all other unused
        # text pixels clear, without treating cursor pixels as leftover prose.
        o=(path/(cp+'_gbaSpriteRam.bin')).read_bytes();cursors=[]
        for i in range(128):
            a,b,k=struct.unpack_from('<HHH',o,i*8)
            if not a&0x2300 and k&1023==1020:cursors.append((b&511,a&255,(b&511)+16,(a&255)+16))
        vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects+cursors)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('stale text pixels')
        pages.append({'route':route,'step':step,'script':script,'units':keys,'first_offsets':{k:last[streams[k][0]]['offset'] for k in keys},'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});covered.update(keys)
    if covered!=set(units):raise ValueError('finite normal scope incomplete')
    result={'passed':True,'release_eligible':False,'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],'new_units':UNIT_COUNT,'previous20_payloads_identical':not types,'previous19_payloads_identical':True,'operation_menu_script_unchanged':True,'static':checks,'normal_runtime_units':sorted(covered),'diagnostic_runtime_units':[],'pages':pages,'limits':['Same-session AM2:00 one-time meal registration only; default Yes completes, alternate No/cancel behavior pending independent route.','Date-number intro, basic names, other calendar dialogues and user input remain untranslated.','No persistent save/reload, RTC alarm, hardware/audio/full-game or human approval.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'calendar_dialogue_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');sheet=Image.new('RGB',(240*len(pages),160))
    for i,p in enumerate(pages):sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+p['route'])/f"step_{p['step']:03}.png"),(i*240,0))
    sheet.save(out/'calendar_dialogue_pages.png');print('normal calendar dialogue QA',True,len(covered));return result

def regressions():
    import report_calendar_menu as menu
    menu.STEM=STEM;menu.PREFIX=PREFIX;menu.OUTDIR=OUTDIR;menu.main();menu.regressions()
if __name__=='__main__':main();regressions()
