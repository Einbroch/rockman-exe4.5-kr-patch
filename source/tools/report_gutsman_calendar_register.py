"""Normal calendar registration date prompt, vertical choices, and branches."""
import json,struct
from collections import Counter
from PIL import Image
import report_gutsman_calendar_home as prior
import report_gutsman_calendar_confirmation as confirmation
from report_roll_pet import ROOT,read,sha,static,pixels
from run_gutsman_calendar_register import STEM,PREFIX,OUTDIR
ASSET='gutsman_calendar_register_ko.json'
def exact_page(p,step,script,keys,m,rom,e,streams,pool,units,cursor_indices=()):
    cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
    if ram[0xFA21]!=script or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or set(last)!=set(selected):raise ValueError('register page script/full literals')
    draws=[last[s] for s in selected]
    for key in keys:
        offsets=[last[s]['offset'] for s in streams[key]];row,start=divmod(offsets[0],10752);advance=start//4;cursor=iter(streams[key])
        for ch in units[key]['translation']:
            if ch=='\n':row+=1;advance=0;continue
            s=next(cursor);d=last[s]
            if d['context']!=0x0200FA20 or d['offset']!=row*10752+advance*4:raise ValueError('register exact geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0]
    counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('register CPU font supply')
    return dict(route=p.name,step=step,units=keys,screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),**pixels(p,step,draws,e,rom,m,origin=(52,110),cursor_screen_background=bool(cursor_indices),cursor_indices=cursor_indices))
def main(anniversary=False,anniversary_confirmation=False):
    prior.STEM=STEM;prior.PREFIX=PREFIX;prior.OUTDIR=OUTDIR
    result=prior.main(register=not anniversary,anniversary=anniversary,anniversary_confirmation=anniversary_confirmation)
    asset='gutsman_calendar_anniversary_confirmation_ko.json' if anniversary_confirmation else 'gutsman_calendar_anniversary_ko.json' if anniversary else ASSET
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='665698');units={u['id']:u for u in read(ROOT/'translations'/asset)['units']};rt=ROOT/'poc/runtime'
    calendar,_=confirmation.checked_route('calendar','select-gutsman',m,pool);date_page=exact_page(calendar,4,1,['665698:1:0'],m,rom,e,streams,pool,units);menu_page=exact_page(calendar,5,2,[f'665698:2:{i}' for i in range(3)],m,rom,e,streams,pool,units,cursor_indices=(16,))
    routes={}
    for name,parent,script in [('register-menu','select-gutsman',2),('register-menu-second','register-menu',2),('register-menu-cancel','register-menu',1),('register-schedule-accept','register-menu',20),('register-anniversary-accept','register-menu-second',31)]:
        p,_=confirmation.checked_route(name,parent,m,pool);ram=(p/'step_002_gbaExtWorkRam.bin').read_bytes() if name!='register-menu' else (p/'step_005_gbaExtWorkRam.bin').read_bytes();step=2 if name!='register-menu' else 5
        if ram[0xFA21]!=script or struct.unpack_from('<I',ram,0xFA50)[0]!=pool:raise ValueError('register branch script/root')
        routes[name]=dict(script=script,record=ram[0x1310:0x1330].hex(),screenshot_sha256=sha((p/f'step_{step:03}.png').read_bytes()))
    expected_record='0000000101060000000000000000000000000000000000000000000000000000'
    if any(x['record']!=expected_record for x in routes.values()):raise ValueError('register navigation changed schedule record')
    for name,xy in [('register-menu',(122,89)),('register-menu-second',(136,89))]:
        p=rt/(PREFIX+name);step=5 if name=='register-menu' else 2;o=(p/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();cur=struct.unpack_from('<HHH',o,16*8)
        if (cur[0]&255,cur[1]&511,cur[2]&1023,cur[2]>>12)!=(xy[0],xy[1],1020,14):raise ValueError('register vertical cursor geometry')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,320));shots=[(calendar,4),(calendar,5),(rt/(PREFIX+'register-menu-second'),2),(rt/(PREFIX+'register-menu-cancel'),2),(rt/(PREFIX+'register-schedule-accept'),2),(rt/(PREFIX+'register-anniversary-accept'),2)]
    for i,(p,s) in enumerate(shots):sheet.paste(Image.open(p/f'step_{s:03}.png'),(i%3*240,i//3*160))
    limit='Register date1/type2 verified on 1월1일: default 일정, 기념일 focus, B return, both accepts.' if anniversary else 'Register date1/type2 verified on 1월1일: default 일정, 기념일 focus, B return, both accepts. Anniversary script31 and its three TV labels remain Japanese and are the next scope.'
    sheet.save(out/'calendar_register.png');result.update(registration_date_page=date_page,registration_menu_page=menu_page,registration_branches=routes,new_literal_units=5 if anniversary_confirmation else 2 if anniversary else 4,selected_text_units=2304 if anniversary_confirmation else 2299 if anniversary else 2297,limits=result['limits']+[limit])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Calendar registration date/type + focus/B/two accept branches: PASS');return result
if __name__=='__main__':main()
