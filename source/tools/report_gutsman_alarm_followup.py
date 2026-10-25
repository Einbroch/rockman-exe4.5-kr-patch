"""Second-page pixel proof; source event pages remain protected, not translated."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_gutsman_pet import main as pet_regression
from report_gutsman_schedule_alarm import alarm_pages
from report_gutsman_chipquest import chip_pages
from bench_dialogue_chip_name import main as bench
from archive_scripts import script_spans
from gutsman_alarm_followup import validate_parent,CHILD
from run_gutsman_alarm_followup import STEM,PREFIX,OUTDIR
def main(stem=STEM,prefix=PREFIX,outdir=OUTDIR,expected_counts=(2282,57,675),oldstem='exe45_ko_development_gutsman_chipquest_v1',unit_asset='gutsman_alarm_followup_ko.json',inventory_outdir='full_scope_gutsman_alarm_followup_v1',new_literal_units=2,meal=False,changed_archives=('66651C',)):
    STEM,PREFIX,OUTDIR=stem,prefix,outdir
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=expected_counts,oldstem=oldstem,outdir=OUTDIR+'/pet_regression',inventory_outdir=inventory_outdir,added_literal_units=0,changed_archives=changed_archives)
    if meal:
        from gutsman_alarm_meal import validate_parent as meal_parent
        meal_parent(read(ROOT/'translations'/unit_asset))
    else:validate_parent(read(ROOT/CHILD))
    m,rom,e,s,c=static(STEM,'66651C');ar=next(a for a in m['archives'] if a['archive']=='66651C');pool=0x08000000+ar['rom_offset'];rt=ROOT/'poc/runtime';q=[];meal_pages=[]
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();native=script_spans(source[0x66651c:0x66651c+771],28);compiled=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],28)
    for script in [1,2]:
        boundary=bytes.fromhex('e600f1');end=native[script].index(boundary)+3
        if compiled[script][:end]!=native[script][:end]:raise ValueError('original event first-page prefix changed')
    for script in [1,2,4,6]:
        p=rt/(PREFIX+f'script{script}');r=verify_route(p,m['output_sha256'],set());env=read(p/'alarm_environment.json')
        if not env['passed'] or not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json'):raise ValueError('alarm quarantine/own parent')
        if env['talk_root']!=struct.unpack_from('<I',rom,0x38148)[0]:raise ValueError('actual own Guts talk root')
        for file,key in [('capture_gutsman_alarm_followup.py','wrapper_sha256'),('capture_gutsman_schedule_alarm.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer identity drift')
        segment=(p/'segment.lua').read_text(encoding='utf8')
        if any(v in segment for v in ['emu.write','setState']):raise ValueError('alarm observer write')
        for g in env['native_guards']:
            if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('native consumer drift')
        found=alarm_pages(p,script,0,m,rom,e,s,pool,unit_asset=unit_asset)
        for page in found:
            calls=read(p/f"step_{page['step']:03}_roll_pet.json")['calls']
            if len(calls)!=1 or calls[0]['root']!=pool or calls[0]['script']!=0 or calls[0]['lr']!=0x08037F27:raise ValueError('exact alias caller')
        q.extend(found)
    if meal:
        from report_gutsman_talk_name import name_page
        p=rt/(PREFIX+'script3');r=verify_route(p,m['output_sha256'],set());env=read(p/'alarm_environment.json')
        if not env['passed'] or not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=3 or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json'):raise ValueError('meal quarantine/own parent')
        for f,k in [('capture_gutsman_alarm_names.py','wrapper_sha256'),('capture_gutsman_schedule_alarm.py','tool_sha256'),('capture_roll_return.py','ram_probe_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/f).read_bytes())!=env[k]:raise ValueError('meal observer identity')
        for g in [*env['native_guards'],env['parser_guard']]:
            if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('meal consumer guard')
        if any(v in (p/'segment.lua').read_text(encoding='utf8') for v in ['emu.write','setState']):raise ValueError('meal observer write')
        for step in [2,3]:
            page=name_page(p,step,'66651C:3:0',0,m,rom,e,s,pool,unit_asset=unit_asset)
            ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();reads=read(p/f'step_{step:03}_variable_reads.json')['reads'];draws=read(p/f'step_{step:03}_return_ram.json')['draws'];start=min(d['stream'] for d in draws);end=start+len(draws)
            if not reads or any(x['context']!=0x0200FA20 or not start<=x['stream']<=end or x['byte']!=ram[x['stream']-0x02000000] for x in reads) or {x['stream'] for x in reads}!=set(range(start,end+1)) or reads[-1]['stream']!=end or reads[-1]['byte']!=0xE5:raise ValueError('meal actual parser RAM boundary/terminator')
            calls=read(p/f'step_{step:03}_roll_pet.json')['calls']
            if calls!=[dict(frame=8,root=pool,script=0,lr=0x08037F27)]:raise ValueError('meal exact alias caller')
            page.update(native_parser_reads_match_RAM=True,first_row_with_comma=page['nickname_width']+11);meal_pages.append(page)
        q.append(meal_pages[0])
    if {x['unit'] for x in q}!=set(s):raise ValueError('all selected pages')
    _,_,ge,gs,gc=static(STEM,'66A844');gp=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='66A844');p=rt/(PREFIX+'chip13');r=verify_route(p,m['output_sha256'],set());env=read(p/'talk_environment.json')
    if not env['passed'] or not env['observer_only'] or env['entry_aliases']!=1 or env['script']!=13 or env['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is not False or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json') or (p/'checkpoint.mss').exists():raise ValueError('chip diagnostic quarantine')
    for f,k in [('capture_gutsman_chipquest.py','chip_wrapper_sha256'),('capture_gutsman_pet_talk_diagnostic.py','tool_sha256'),('capture_gutsman_pet_talk.py','observer_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
        if sha((ROOT/'tools'/f).read_bytes())!=env[k]:raise ValueError('chip observer drift')
    chip=chip_pages(p,'66A844',m,rom,ge,gs,gp);b=bench(STEM,OUTDIR)
    if b['vectors']!=64:raise ValueError('selector regression population')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(len(q)*240,160))
    for i,x in enumerate(q):sheet.paste(Image.open(rt/x['route']/f"step_{x['step']:03}.png"),(i*240,0))
    sheet.save(out/'alarm_pages.png')
    limits=['TV/promise second pages plus prior school/lead-in renderer evidence only; read aliases bypass native alarm route. No registered-event/name/RTC progression or acquisition proved. First pages remain Japanese; separate baseline event-name alias produced32 repeated bytes, not a valid registered event sample.','Guts chip name rerun after relocation; Roll guard synthetic CPU evidence only on this new ROM, not new Roll screen evidence.',f'{15 if meal else 16} remaining source literals including event/name prefixes and alternate mugshot consumers preserved. Whole ROM/images/inline/fixed/name persistence/old-save compatibility/prior wait-arrow53pixel remain unresolved; wording human review pending.']
    if meal:limits.append('Meal source-native captured nickname plus literal checked twice. Not arbitrary/Hangul name persistence or native reminder timing/registration proof; stops at keyWait before event dispatch.')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],new_literal_units=new_literal_units,selected_text_units=expected_counts[0],static=c,pet_regression=baseline,diagnostic_renderer_pages=q,meal_pages=meal_pages,guts_chip_regression=chip,synthetic_selector_vectors=b['vectors'],original_event_first_pages_identical=True,remaining_catalog=baseline['remaining_catalog'],limits=limits)
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(f'Alarm{len(q)} selected renderer pages; new{new_literal_units} + Guts chip/save/PET regressions PASS');return result
if __name__=='__main__':main()
