"""Two native calendar prompts plus cumulative own-ROM regressions."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_alarm_followup import main as regressions
from run_gutsman_calendar_prompts import STEM,PREFIX,OUTDIR
def main(stem=STEM,prefix=PREFIX,outdir=OUTDIR,content=False,confirmation=False,home=False,register=False,anniversary=False,anniversary_confirmation=False):
    STEM,PREFIX,OUTDIR=stem,prefix,outdir
    has_content=content or confirmation or home or register or anniversary or anniversary_confirmation;selected_count=2304 if anniversary_confirmation else 2299 if anniversary else 2297 if register else 2293 if home else 2290 if confirmation else 2287 if content else 2285
    oldstem='exe45_ko_development_gutsman_calendar_anniversary_v1' if anniversary_confirmation else 'exe45_ko_development_gutsman_calendar_register_v1' if anniversary else 'exe45_ko_development_gutsman_calendar_home_v1' if register else 'exe45_ko_development_gutsman_calendar_confirmation_v1' if home else 'exe45_ko_development_gutsman_calendar_content_v1' if confirmation else 'exe45_ko_development_gutsman_calendar_prompts_v1' if content else 'exe45_ko_development_gutsman_alarm_meal_v1'
    changed=('6368E8','665698') if anniversary or anniversary_confirmation else ('665698',) if has_content else ()
    baseline=regressions(stem=STEM,prefix=PREFIX,outdir=OUTDIR+'/regression',expected_counts=(selected_count,58,674),oldstem=oldstem,unit_asset='gutsman_alarm_meal_ko.json',inventory_outdir='full_scope_'+OUTDIR,new_literal_units=0,meal=True,changed_archives=changed)
    asset='gutsman_calendar_anniversary_confirmation_ko.json' if anniversary_confirmation else 'gutsman_calendar_anniversary_ko.json' if anniversary else 'gutsman_calendar_register_ko.json' if register else 'gutsman_calendar_home_ko.json' if home else 'gutsman_calendar_confirmation_ko.json' if confirmation else 'gutsman_calendar_content_ko.json' if content else 'gutsman_calendar_prompts_ko.json'
    m,rom,e,streams,checks=static(STEM,'665698');ar=next(a for a in m['archives'] if a['archive']=='665698');pool=0x08000000+ar['rom_offset'];units={u['id']:u for u in read(ROOT/'translations'/asset)['units']};pages=[];rt=ROOT/'poc/runtime'
    samples=[('calendar','select-gutsman',6,20),('time','calendar',5,21)]
    if has_content:samples += [('time-stable','calendar',6,22),('person-input','person-stable',2,23)]
    for route,parent,step,script in samples:
        p=rt/(PREFIX+route);r=verify_route(p,m['output_sha256'],set());env=read(p/'calendar_prompts_environment.json')
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json') or r.get('normal_play_checkpoint_eligible') is False or not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['pool']!=pool:raise ValueError('normal calendar ancestry')
        for f,k in [('capture_gutsman_calendar_prompts.py','self_sha256'),('capture_roll_pet.py','pet_probe_sha256'),('capture_fixedcell_probe.py','fixed_probe_sha256')]:
            if sha((ROOT/'tools'/f).read_bytes())!=env[k]:raise ValueError('calendar observer drift')
        if any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('calendar intervention')
        cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));key=f'665698:{script}:0';addresses=streams[key];last={d['stream']:d for d in obs['draws'] if d['stream'] in addresses}
        if ram[0xFA21]!=script or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or set(last)!=set(addresses):raise ValueError('native calendar script/full literal')
        draws=[last[a] for a in addresses];advance=0
        for d in draws:
            if d['context']!=0x0200FA20 or d['offset']!=advance*4:raise ValueError('calendar exact row geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
        if advance>183:raise ValueError('calendar capacity')
        counts=Counter(d['glyph_index'] for d in draws);fontreads={v['index']:v['reads'] for v in obs['font_reads']}
        if any(fontreads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('calendar CPU font supply')
        proof=pixels(p,step,draws,e,rom,m,origin=(52,110),cursor_indices=())
        im=Image.open(p/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not (52<=x<52+advance and 110<=y<122) and not (x>=224 and y>=138)]
        if any(im.getpixel(xy)!=bg for xy in vacant):raise ValueError('calendar stale pixels')
        # Reuse the same native mugshot/window for each question, not another Navi.
        oldroute='calendar' if script==20 else 'time';oldstep=6 if script==20 else step
        oldpath=rt/f'gutsman-event-buffer-native-v1-{oldroute}'/f'step_{oldstep:03}.png'
        if script==22:oldpath=rt/'gutsman-calendar-prompts-v1-time/step_006.png'
        if script==23:
            oldpath=rt/'gutsman-calendar-content-baseline-v1-person-input/step_002.png'
            oldsha='68a8d4d0c13d39cc6e80c0bbd3e367d6469062e042363dad2b59461573a56cee';rr=verify_route(oldpath.parent,oldsha,set());renv=read(oldpath.parent/'calendar_prompts_environment.json')
            if rr['state_origin']!=str(rt/'gutsman-calendar-content-baseline-v1-person/result.json') or rr.get('normal_play_checkpoint_eligible') is False or not renv['observer_only'] or renv['rom_sha256']!=oldsha:raise ValueError('native person reference ancestry')
            rram=(oldpath.parent/'step_002_gbaExtWorkRam.bin').read_bytes()
            if rram[0xFA21]!=23 or struct.unpack_from('<I',rram,0xFA50)[0]!=renv['pool']:raise ValueError('native person reference script')
        boxes=[(5,107,50,151),(1,104,238,107),(1,151,238,155)]
        if has_content and script in (20,22):
            name='calendar-phases' if script==20 else 'tv-phases';reference=rt/('gutsman-calendar-content-baseline-v1-'+name)
            oldsha='68a8d4d0c13d39cc6e80c0bbd3e367d6469062e042363dad2b59461573a56cee'
            oldm=read(ROOT/'poc/output/exe45_ko_development_gutsman_calendar_prompts_v1.json')
            if oldm['output_sha256']!=oldsha or sha((ROOT/'poc/output/exe45_ko_development_gutsman_calendar_prompts_v1.gba').read_bytes())!=oldsha:raise ValueError('phase baseline ROM identity')
            rr=verify_route(reference,oldsha,set());renv=read(reference/'calendar_prompts_environment.json');oldpool=0x08000000+next(a['rom_offset'] for a in oldm['archives'] if a['archive']=='665698')
            parent_name='calendar' if script==20 else 'time'
            if rr['state_origin']!=str(rt/('gutsman-calendar-prompts-v1-'+parent_name)/'result.json') or rr.get('normal_play_checkpoint_eligible') is False or not renv['observer_only'] or renv['rom_sha256']!=oldsha or renv['pool']!=oldpool or len(rr['capture_steps'])!=90:raise ValueError('native phase ancestry/population')
            for f,k in [('capture_gutsman_calendar_prompts.py','self_sha256'),('capture_roll_pet.py','pet_probe_sha256'),('capture_fixedcell_probe.py','fixed_probe_sha256')]:
                if sha((ROOT/'tools'/f).read_bytes())!=renv[k]:raise ValueError('phase observer drift')
            if any(x in (reference/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('phase intervention')
            matches=[]
            for s in rr['capture_steps']:
                name=f'step_{s:03}';rram=(reference/(name+'_gbaExtWorkRam.bin')).read_bytes();ref=Image.open(reference/(name+'.png')).convert('RGB')
                if rram[0xFA21]!=script or struct.unpack_from('<I',rram,0xFA50)[0]!=oldpool:raise ValueError('phase native script/root')
                if all(im.crop(box).tobytes()==ref.crop(box).tobytes() for box in boxes):matches.append(reference/(name+'.png'))
            if not matches:raise ValueError('no exact native portrait/border phase')
            oldpath=matches[0]
        old=Image.open(oldpath).convert('RGB')
        for box in boxes:
            if im.crop(box).tobytes()!=old.crop(box).tobytes():raise ValueError('GutsMan portrait/window drift')
        pages.append(dict(route=p.name,step=step,unit=key,width=advance,vacant_pixels_cleared=len(vacant),screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),reference_screenshot=str(oldpath.relative_to(ROOT)),reference_screenshot_sha256=sha(oldpath.read_bytes()),gutsman_mugshot_and_border_identical=True,**proof))
    question_keys={k for k in units if 20<=int(k.split(':')[1])<24}
    if {p['unit'] for p in pages}!=question_keys:raise ValueError('calendar finite question scope')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,160*((len(question_keys)+1)//2)))
    for i,key in enumerate(sorted(question_keys,key=lambda k:int(k.split(':')[1]))):
        p=next(p for p in pages if p['unit']==key);sheet.paste(Image.open(rt/p['route']/f"step_{p['step']:03}.png"),((i%2)*240,(i//2)*160))
    limits=['Four native input questions proved by this component; other translated calendar pages are covered by downstream reports. Friend selection reaches person question23; entered person names, deletion and persistent schedules remain open.' if content else 'Time/type two normal input prompts only; date/choice/confirmation/content/name/delete and69 other literals remain original.','Baseline normal meal registration/query is from previous meal ROM, not evidence of new ROM registration commit or RTC alarm. Event alias initialization cause remains unresolved.','Whole ROM/images/Hangul name editing/persistence/old-save compatibility/prior wait-arrow53pixel and human wording review unresolved.']
    if has_content:limits.append('Initial TV capture time6 corner(1,105) differed by1pixel and remains transition-scope unresolved. Content page evidence is normal time-stable6 after90 additional idle frames; no tolerance/ROI/state mutation. Calendar blink frame and stable TV entire three ROIs require exact observed prior native animation phase, not arbitrary masks or another Navi.')
    sheet.save(out/'calendar_prompts.png');result=dict(passed=True,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',rom_sha256=m['output_sha256'],new_literal_units=5 if anniversary_confirmation else 2 if anniversary else 4 if register else 3 if confirmation or home else 2,selected_text_units=selected_count,static=checks,normal_calendar_pages=pages,regression=baseline,limits=limits)
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(f'{len(pages)} native GutsMan calendar questions + cumulative regression: PASS');return result
if __name__=='__main__':main()
