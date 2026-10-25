"""Selected variable-free schedule runtime evidence; dynamic listings remain open."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from report_roll_pet_license import literal_end
from run_roll_schedule import STEM,PREFIX,OUTDIR

def main():
    m,rom,e,streams,checks=static(STEM,'661754');ar=next(a for a in m['archives'] if a['archive']=='661754');pool=0x08000000+ar['rom_offset'];units={u['id']:u for u in read(ROOT/'translations/roll_schedule_ko.json')['units']};covered=set();pages=[]
    oldm=read(ROOT/'poc/output/exe45_ko_development_roll_competition_v2.json');old=(ROOT/'poc/output/exe45_ko_development_roll_competition_v2.gba').read_bytes()
    if sha(old)!=oldm['output_sha256']:raise ValueError('previous ROM identity')
    for previous in oldm['archives']:
        current=next(a for a in m['archives'] if a['archive']==previous['archive'])
        if current['compiled_sha256']!=previous['compiled_sha256'] or current['translated_units']!=previous['translated_units'] or rom[current['rom_offset']:current['rom_offset']+current['compiled_bytes']]!=old[previous['rom_offset']:previous['rom_offset']+previous['compiled_bytes']]:raise ValueError('previous payload changed')
    if len(m['archives'])!=18 or m['translated_units']!=1070:raise ValueError('selected denominator')
    for script in [1,3,10,12]:
        path=ROOT/'poc/runtime'/(PREFIX+f'script{script}');r=verify_route(path,m['output_sha256'],set());env=read(path/'schedule_environment.json')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+'roll-intro')/'result.json'):raise ValueError('diagnostic identity/parent/quarantine')
        for file,key in [('capture_roll_schedule.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer drift')
        for step,literal in ([(2,0),(4,1)] if script==10 else [(2,0)]):
            key=f'661754:{script}:{literal}';selected=streams[key];cp=f'step_{step:03}';state=read(path/(cp+'_roll_pet.json'));ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
            if set(last)!=set(selected) or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or state['calls']!=[{'frame':8,'root':pool,'script':0,'lr':0x08037F27}]:raise ValueError('literal consumer coverage')
            row=0;advance=0;cursor=iter(selected)
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;advance=0;continue
                stream=next(cursor)
                if last[stream]['offset']!=row*10752+advance*4 or last[stream]['context']!=0x0200FA20:raise ValueError('exact geometry')
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
            end=literal_end(rom,selected,e)
            if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('source keyWait/clearMsg boundary')
            draws=[last[s] for s in selected];counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU font consumption')
            proof=pixels(path,step,draws,e,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
            for d in draws:
                row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
            vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
            if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('stale text pixels')
            pages.append({'script':script,'step':step,'unit':key,'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});covered.add(key)
        if script!=1:
            step=6 if script==10 else 4;ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            if struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('dialogue exit not reached')
    if covered!=set(units):raise ValueError('finite scope incomplete')
    from bench_dialogue_chip_name import main as bench
    b=bench(STEM,OUTDIR);result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'previous_17_payloads_identical':True,'normal_runtime_units':[],'diagnostic_renderer_units':sorted(covered),'pages':pages,'name_selector_cpu_vectors':b['vectors'],'limits':['Four read-alias paths, not native reminder reachability or registered-event/time progression.','Script1 stops before event-name lookup; script10 no-event branch only.','Source script2/11 event name, AMPM and time insertion retained, partly Japanese and not runtime verified here.','No Hangul user input, save, RTC, audio, hardware, full-game or human wording approval.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'schedule_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    sheet=Image.new('RGB',(1200,160))
    for i,p in enumerate(pages):sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+f"script{p['script']}")/f"step_{p['step']:03}.png"),(i*240,0))
    sheet.save(out/'schedule_pages.png');print('schedule QA',True,len(covered),len(pages));return result

if __name__=='__main__':main()
