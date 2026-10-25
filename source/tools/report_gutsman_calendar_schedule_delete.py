"""Exact-ROM schedule deletion, retained management and static conflict evidence."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,static
from report_gutsman_calendar_register import exact_page
import report_gutsman_calendar_confirmation as ancestry
import report_gutsman_calendar_management as retained
from gutsman_calendar_schedule_delete import CHILD,validate
from run_gutsman_calendar_schedule_delete import STEM,PREFIX,OUTDIR,ROUTES
def main(frequency_names=False):
    retained.STEM=STEM;retained.PREFIX=PREFIX;retained.OUTDIR=OUTDIR
    result=retained.main(schedule_delete=True,frequency_names=frequency_names)
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset']for a in m['archives']if a['archive']=='665698')
    asset=read(ROOT/CHILD);validate(asset);units={u['id']:u for u in asset['units']};ancestry.PREFIX=PREFIX;paths={}
    for name,parent,_ in ROUTES:
        p,r=ancestry.checked_route(name,parent,m,pool);env=read(p/'calendar_prompts_environment.json')
        if env.get('management_observer_sha256')!=sha((ROOT/'tools/capture_gutsman_calendar_management.py').read_bytes()) or env.get('additional_stream_range')!=[0x02000000,0x02040000]:raise ValueError('schedule observer identity')
        paths[name]=p
    first=paths['schedule-delete-first'];ram=(first/'step_002_gbaExtWorkRam.bin').read_bytes();script=ram[0xFA21]
    if script not in (50,51):raise ValueError('normal schedule deletion did not reach50/51')
    tail=5 if script==50 else 6
    pages=[exact_page(first,2,script,[f'665698:{script}:{tail}'],m,rom,e,streams,pool,units),exact_page(paths['schedule-delete-confirm'],2,script,[f'665698:{script}:{i}'for i in range(tail+1,tail+4)],m,rom,e,streams,pool,units,cursor_indices=(1,))]
    name=retained.ram_name(first,2,'식사',m,rom)
    for route,x in [('schedule-delete-confirm',85),('schedule-delete-no-focus',121)]:
        o=(paths[route]/'step_002_gbaSpriteRam.bin').read_bytes();a,b,c=struct.unpack_from('<HHH',o,8)
        if (a&255,b&511,c&1023,c>>12,a>>14,b>>14)!=(136,x,1020,14,0,1):raise ValueError('schedule choice cursor contract')
    confirm=paths['schedule-delete-confirm'];im=Image.open(confirm/'step_002.png').convert('RGB');bg=im.getpixel((233,124))
    if any(im.getpixel((x,y))!=bg for y in range(124,136) for x in range(52,234)):raise ValueError('schedule deletion name row clearing')
    pre=(confirm/'step_002_gbaExtWorkRam.bin').read_bytes()[0x1310:0x1330];expected=bytes.fromhex('03000001010602000002f9fcdd16f9fcac14e500000000000000000000000000')
    if pre!=expected:raise ValueError('schedule isolated meal identity')
    branches={}
    for route in ['schedule-delete-no-accept','schedule-delete-b-cancel','schedule-delete-yes-accept']:
        p=paths[route];record=(p/'step_002_gbaExtWorkRam.bin').read_bytes()[0x1310:0x1330]
        if record!=(bytes(32)if route.endswith('yes-accept')else pre):raise ValueError('schedule deletion/cancel exact record')
        branches[route]=dict(record=record.hex(),record_changed=record!=pre,screenshot_sha256=sha((p/'step_002.png').read_bytes()))
    observed={f'665698:{script}:{i}'for i in range(tail,tail+4)};new={u['id']for u in asset['units'][45:]};out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(720,320))
    for i,route in enumerate(['schedule-delete-list','schedule-delete-first','schedule-delete-confirm','schedule-delete-no-focus','schedule-delete-no-accept','schedule-delete-yes-accept']):sheet.paste(Image.open(paths[route]/'step_002.png'),(i%3*240,i//3*160))
    sheet.save(out/'schedule_delete.png')
    result.update(passed=True,schedule_delete_static=checks,schedule_delete_pages=pages,schedule_delete_dynamic_name=name,schedule_delete_branches=branches,schedule_delete_added_literal_units=9,schedule_delete_runtime_observed_units=sorted(observed),schedule_delete_static_only_units=sorted(new-observed),limits=result['limits']+['One isolated meal deletion branch only. Other date/frequency branch and conflict25 remain static-only unless separately observed. Native persistent schedule save/reload, old saves, arbitrary Hangul input and complete population remain unverified.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Schedule9 static / native deletion4 and meal name / Yes No B: PASS');return result
if __name__=='__main__':main()
