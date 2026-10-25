"""Finite alarm prose font/geometry/pixel proof with explicit diagnostic limits."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from report_roll_pet_license import literal_end
from run_roll_schedule_alarm import STEM,PREFIX,OUTDIR

def main():
    m,rom,e,streams,checks=static(STEM,'660D90');ar=next(a for a in m['archives'] if a['archive']=='660D90');pool=0x08000000+ar['rom_offset'];units={u['id']:u for u in read(ROOT/'translations/roll_schedule_alarm_ko.json')['units']};pages=[]
    oldm=read(ROOT/'poc/output/exe45_ko_development_roll_schedule_time_v1.json');old=(ROOT/'poc/output/exe45_ko_development_roll_schedule_time_v1.gba').read_bytes()
    if sha(old)!=oldm['output_sha256']:raise ValueError('previous ROM identity')
    for before in oldm['archives']:
        now=next(a for a in m['archives'] if a['archive']==before['archive'])
        if now['compiled_sha256']!=before['compiled_sha256'] or now['translated_units']!=before['translated_units'] or rom[now['rom_offset']:now['rom_offset']+now['compiled_bytes']]!=old[before['rom_offset']:before['rom_offset']+before['compiled_bytes']]:raise ValueError('previous payload drift')
    if len(m['archives'])!=19 or m['translated_units']!=1074 or m['pet_menu_graphics']['final_block_sha256']!=oldm['pet_menu_graphics']['final_block_sha256']:raise ValueError('denominator/graphics')
    for script in [3,4,6]:
        path=ROOT/'poc/runtime'/(PREFIX+f'script{script}');r=verify_route(path,m['output_sha256'],set());env=read(path/'alarm_environment.json')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+'roll-intro')/'result.json'):raise ValueError('diagnostic identity/quarantine')
        for file,key in [('capture_roll_schedule_alarm.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer drift')
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        for g in env['native_guards']:
            if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('native guard drift')
        key=f'660D90:{script}:0';selected=streams[key]
        for step in [2,3]:
            cp=f'step_{step:03}';s=read(path/(cp+'_roll_pet.json'));ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();last={d['stream']:d for d in s['draws'] if d['stream'] in selected}
            if set(last)!=set(selected) or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or s['calls']!=[{'frame':8,'root':pool,'script':0,'lr':0x08037F27}]:raise ValueError('literal coverage/native caller')
            row=0;advance=0;cursor=iter(selected)
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;advance=0;continue
                stream=next(cursor)
                if last[stream]['offset']!=row*10752+advance*4 or last[stream]['context']!=0x0200FA20:raise ValueError('geometry')
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
            end=literal_end(rom,selected,e)
            if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('keyWait/clear boundary')
            draws=[last[s] for s in selected];counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in s['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('font CPU reads')
            proof=pixels(path,step,draws,e,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
            for d in draws:
                row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
            vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
            if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('stale text pixels')
            pages.append({'script':script,'step':step,'unit':key,'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof})
    covered=sorted({p['unit'] for p in pages})
    if set(covered)!=set(units):raise ValueError('finite scope')
    from bench_dialogue_chip_name import main as bench
    b=bench(STEM,OUTDIR)
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'previous_18_payloads_identical':True,'normal_runtime_units':[],'diagnostic_renderer_units':covered,'pages':pages,'name_selector_cpu_vectors':b['vectors'],'limits':['Three read-alias PET entries; not naturally triggered RTC alarms or event progression.','Script6 stops at keyWait before dynamic event dispatch.','Basic event names/menu, alternate mugshot alarm23/24/26 and other event classes still untranslated.','Hangul input, save, RTC consistency, audio, hardware, full game and human wording review pending.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'alarm_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(720,160))
    for i,script in enumerate([3,4,6]):sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+f'script{script}')/'step_003.png'),(i*240,0))
    sheet.save(out/'alarm_pages.png');print('alarm QA',True,len(covered),len(pages));return result

def regressions():
    import report_roll_pet_talk as talk
    from report_roll_intro import main as intro
    from report_roll_pet import main as pet
    from report_attack_caption_runtime import main as caption
    previous=talk.STEM,talk.PREFIX,talk.OUTDIR
    try:talk.STEM=STEM;talk.PREFIX=PREFIX;talk.OUTDIR=OUTDIR;reports=[talk.talk_report()]
    finally:talk.STEM,talk.PREFIX,talk.OUTDIR=previous
    reports.extend([intro(STEM,PREFIX+'roll-',OUTDIR+'/greeting_regression'),pet(STEM,PREFIX,OUTDIR+'/pet_regression'),caption(STEM,PREFIX+'roll-',OUTDIR+'/roll_caption',roll=True)])
    m=read(ROOT/f'poc/output/{STEM}.json')
    if len(reports)!=4 or not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==m['output_sha256'] for r in reports):raise ValueError('normal regression identities')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True)
    (out/'normal_regressions.json').write_text(json.dumps({'passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'normal_reports':4,'diagnostic_reports':0,'limits':['Focused greeting/PET/default-talk/attack-caption paths, not whole-game coverage.']},indent=2),encoding='utf-8')
    return reports

if __name__=='__main__':main();regressions()
