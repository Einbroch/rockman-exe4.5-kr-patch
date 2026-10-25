"""Dynamic month/day calendar-home prompt after normal Yes commit."""
import json,struct
from collections import Counter
from PIL import Image
import report_gutsman_calendar_confirmation as base
from report_roll_pet import ROOT,read,sha,static,pixels
from run_gutsman_calendar_home import STEM,PREFIX,OUTDIR
ASSET='gutsman_calendar_home_ko.json'
def main(register=False,anniversary=False,anniversary_confirmation=False):
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR
    result=base.main(home=not register and not anniversary,register=register and not anniversary,anniversary=anniversary,anniversary_confirmation=anniversary_confirmation)
    asset='gutsman_calendar_anniversary_confirmation_ko.json' if anniversary_confirmation else 'gutsman_calendar_anniversary_ko.json' if anniversary else 'gutsman_calendar_register_ko.json' if register else ASSET
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='665698');p,r=base.checked_route('yes-accept','confirmation',m,pool);cp='step_002';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));keys=[f'665698:0:{i}' for i in range(3)];selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
    if ram[0xFA21]!=0 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or set(last)!=set(selected):raise ValueError('calendar home script/full literals')
    units={u['id']:u for u in read(ROOT/'translations'/asset)['units']};draws=[last[s] for s in selected]
    for key in keys:
        offsets=[last[s]['offset'] for s in streams[key]];row,start=divmod(offsets[0],10752);advance=start//4;cursor=iter(streams[key])
        for ch in units[key]['translation']:
            if ch=='\n':row+=1;advance=0;continue
            s=next(cursor);d=last[s]
            if d['context']!=0x0200FA20 or d['offset']!=row*10752+advance*4:raise ValueError('calendar home exact geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0]
    if last[streams[keys[0]][0]]['offset']!=0:raise ValueError('calendar home first literal anchor')
    counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('calendar home CPU font supply')
    proof=pixels(p,2,draws,e,rom,m,origin=(52,110),cursor_indices=())
    im=Image.open(p/(cp+'.png')).convert('RGB');old=Image.open(ROOT/'poc/runtime/gutsman-calendar-confirmation-v1-yes-accept/step_002.png').convert('RGB')
    for box in [(1,104,238,107),(1,151,238,155)]:
        if im.crop(box).tobytes()!=old.crop(box).tobytes():raise ValueError('calendar home window border drift')
    page=dict(route=p.name,step=2,units=keys,screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),dynamic_month_day_controls_preserved=True,record=ram[0x1310:0x1330].hex(),**proof)
    if page['record']!='03000001010602000002f9fcdd16f9fcac14e500000000000000000000000000':raise ValueError('calendar home committed record drift')
    result.update(calendar_home_page=page,new_literal_units=5 if anniversary_confirmation else 2 if anniversary else 4 if register else 3,selected_text_units=2304 if anniversary_confirmation else 2299 if anniversary else 2297 if register else 2293,limits=result['limits']+['Calendar home0 verified for current 1월 1일 after meal preset commit only; other dates, conflicting schedules, editing/deletion, persistence and RTC dispatch remain unverified.'])
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);Image.open(p/(cp+'.png')).save(out/'calendar_home.png');(out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Dynamic calendar home prompt after normal Yes commit: PASS');return result
if __name__=='__main__':main()
