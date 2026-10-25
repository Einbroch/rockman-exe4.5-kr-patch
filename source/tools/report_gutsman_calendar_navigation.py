"""Exact-ROM normal PET/save regression and finite calendar6/7 verification."""
import json,struct
from pathlib import Path
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route,pixels
from report_gutsman_alarm_followup import main as retained_report
from report_gutsman_calendar_register import exact_page
import report_gutsman_calendar_confirmation as confirmation
from run_gutsman_calendar_navigation import STEM,PREFIX,OUTDIR
from gutsman_calendar_navigation import CHILD,validate
def main(management=False,schedule_delete=False,frequency_names=False):
    if frequency_names and not schedule_delete:raise ValueError('frequency regression requires retained schedule-delete scope')
    result=retained_report(stem=STEM,prefix=PREFIX,expected_counts=(2345 if frequency_names else 2340 if schedule_delete else 2331 if management else 2308,58,674),oldstem='exe45_ko_development_gutsman_calendar_schedule_delete_v1' if frequency_names else 'exe45_ko_development_gutsman_calendar_management_v1' if schedule_delete else 'exe45_ko_development_gutsman_calendar_navigation_v1' if management else 'exe45_ko_development_gutsman_calendar_anniversary_confirmation_v1',outdir=OUTDIR+'/regression',inventory_outdir='full_scope_'+OUTDIR,new_literal_units=5 if frequency_names else 9 if schedule_delete else 23 if management else 4,meal=True,unit_asset='gutsman_alarm_meal_ko.json',changed_archives=('6368E8',) if frequency_names else ('665698',))
    child,check=CHILD,validate
    if management:
        from gutsman_calendar_management import CHILD as child,validate as check
    if schedule_delete:
        from gutsman_calendar_schedule_delete import CHILD as child,validate as check
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='665698');asset=read(ROOT/child);check(asset);units={u['id']:u for u in asset['units']}
    confirmation.PREFIX=PREFIX;rt=ROOT/'poc/runtime'
    parents={'anniversary-cancel':'register-anniversary-accept','return-menu-first':'anniversary-cancel','return-menu-schedule':'return-menu-first','return-menu-anniversary':'anniversary-cancel','return-menu-cancel':'anniversary-cancel','query-date':'self-yes-accept','query-cancel':'query-date','self-query':'self-yes-accept','school-query':'school-yes-accept'}
    paths={k:confirmation.checked_route(k,v,m,pool)[0] for k,v in parents.items()}
    pages=[exact_page(paths['anniversary-cancel'],2,7,[f'665698:7:{i}' for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(16,)),exact_page(paths['query-date'],3,6,['665698:6:0'],m,rom,e,streams,pool,units)]
    # Native focus changes do not redraw text: prove its residency instead of
    # pretending a new CPU font-read occurred in this checkpoint segment.
    focus=paths['return-menu-first'];ram=(focus/'step_002_gbaExtWorkRam.bin').read_bytes();obs=read(focus/'step_002_roll_pet.json')
    if ram[0xFA21]!=7 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or obs['draws']:raise ValueError('focus must retain script7 without redraw')
    selected={s for i in range(3) for s in streams[f'665698:7:{i}']};parent_obs=read(paths['anniversary-cancel']/'step_002_roll_pet.json');last={d['stream']:d for d in parent_obs['draws'] if d['stream'] in selected}
    if set(last)!=selected:raise ValueError('focus parent complete draw population')
    proof=pixels(focus,2,list(last.values()),e,rom,m,origin=(52,110),cursor_screen_background=True,cursor_indices=(16,))
    pages.append(dict(route=focus.name,step=2,units=[f'665698:7:{i}' for i in range(3)],no_redraw=True,font_supply='parent CPU reads; current retained VRAM and pixels',screenshot_sha256=sha((focus/'step_002.png').read_bytes()),**proof))
    for name,y in [('anniversary-cancel',136),('return-menu-first',122)]:
        o=(paths[name]/'step_002_gbaSpriteRam.bin').read_bytes();a,b,c=struct.unpack_from('<HHH',o,16*8)
        if (a&255,b&511,c&1023,c>>12)!=(y,89,1020,14):raise ValueError('calendar return choice cursor')
    expected={'return-menu-schedule':20,'return-menu-anniversary':31,'return-menu-cancel':1,'query-cancel':0}
    branches={}
    for name,script in expected.items():
        ram=(paths[name]/'step_002_gbaExtWorkRam.bin').read_bytes()
        if ram[0xFA21]!=script or struct.unpack_from('<I',ram,0xFA50)[0]!=pool:raise ValueError(f'calendar branch script/root: {name}: {ram[0xFA21]}')
        parent_ram=sorted((rt/(PREFIX+parents[name])).glob('step_*_gbaExtWorkRam.bin'))[-1].read_bytes()
        if ram[0x1310:0x1330]!=parent_ram[0x1310:0x1330]:raise ValueError('calendar navigation changed record')
        branches[name]=dict(script=script,record_unchanged=True)
    # Retained confirmation and dynamic Korean-name redisplay on this exact ROM.
    import report_gutsman_calendar_anniversary_confirmation as ann
    name_checks={}
    for kind in ['self','school']:
        p=rt/(PREFIX+'anniversary-'+kind+'-accept');confirmation.checked_route('anniversary-'+kind+'-accept','register-anniversary-accept' if kind=='self' else 'anniversary-second',m,pool)
        pages.append(exact_page(p,2,33,[f'665698:33:{i}' for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(30,)))
        word='생일' if kind=='self' else '개교기념일'
        name_checks[kind]=dict(confirmation=ann.fixed_name(p,2,word,rom,m),query=ann.query_name(paths[kind+'-query'],word,rom,m))
    sheet=Image.new('RGB',(720,320));shots=[(paths['anniversary-cancel'],2),(paths['return-menu-first'],2),(paths['query-date'],3),(paths['return-menu-schedule'],2),(paths['return-menu-anniversary'],2),(paths['query-cancel'],2)]
    for i,(p,s) in enumerate(shots):sheet.paste(Image.open(p/f'step_{s:03}.png'),(i%3*240,i//3*160))
    out=ROOT/'analysis'/OUTDIR;sheet.save(out/'calendar_navigation.png')
    result.update(calendar_static=checks,calendar_pages=pages,calendar_navigation_branches=branches,anniversary_name_regressions=name_checks,calendar_runtime_observed_navigation_units=[f'665698:7:{i}' for i in range(3)]+['665698:6:0'],limits=result['limits']+['Holiday130 remains Japanese. Earlier full calendar confirmation report is not automatically transferred to this ROM. Anniversary persistent native reload and arbitrary Hangul input remain unverified.'])
    if not management:result['calendar_runtime_observed_new_units']=result['calendar_runtime_observed_navigation_units']
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Calendar navigation4 / choices and B / retained confirmation: PASS');return result
if __name__=='__main__':main()
