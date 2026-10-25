"""Normal native month/day insertion between three Korean date literals."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,sha,pixels,verify_route
from run_calendar_date import STEM,PREFIX,OUTDIR
def main():
    old=read(ROOT/'translations/roll_calendar_content_ko.json');a=read(ROOT/'translations/roll_calendar_date_ko.json');units={u['id']:u for u in a['units']}
    if len(units)!=14 or any(units[u['id']]!=u for u in old['units']) or set(units)-{u['id'] for u in old['units']}!={'65F11C:0:0','65F11C:0:1','65F11C:0:2'}:raise ValueError('prior11 identity/date scope')
    m,rom,e,streams,checks=static(STEM,'65F11C');ar=next(x for x in m['archives'] if x['archive']=='65F11C');pool=0x8000000+ar['rom_offset'];source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();path=ROOT/'poc/runtime'/(PREFIX+'date-font2');verify_route(path,m['output_sha256'],set());env=read(path/'date_environment.json');base=read(path/'calendar_dialogue_environment.json')
    if not env['observer_only'] or env['pool']!=pool or env['rom_sha256']!=m['output_sha256'] or not base['observer_only']:raise ValueError('date observer identity')
    for name,want in [('capture_calendar_date.py',env['self_sha256']),('capture_roll_calendar_dialogue.py',env['base_probe_sha256']),('capture_roll_pet.py',base['pet_probe_sha256']),('capture_fixedcell_probe.py',base['fixed_probe_sha256'])]:
        if sha((ROOT/'tools'/name).read_bytes())!=want:raise ValueError('observer drift')
    advance=lambda i:struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0]
    keys=[f'65F11C:0:{i}' for i in range(3)];selected=[s for k in keys for s in streams[k]];pages=[]
    for step in (2,3):
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();state=read(path/(cp+'_roll_pet.json'));dynamic=read(path/(cp+'_date_ram.json'))['draws'];last={d['stream']:d for d in state['draws'] if d['stream'] in selected};expected=dict(e)
        if ram[0xFA21]!=0 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or set(last)!=set(selected) or len(dynamic)!=4:raise ValueError('normal date script/full literals/native digits')
        prefix=sum(advance(e[s]['index']) for s in streams[keys[0]]);month_end=prefix+advance(0)+advance(2);day_start=month_end+advance(e[streams[keys[1]][0]]['index']);end=day_start+advance(0)+advance(2);offsets=[prefix*4,(prefix+advance(0))*4,day_start*4,(day_start+advance(0))*4]
        addresses=[0x02010AC0,0x02010AC1,0x02010B40,0x02010B41]
        for d,index,off,address in zip(dynamic,[0,2,0,2],offsets,addresses):
            record=source[0x608758+index*96:0x608758+(index+1)*96]
            if d['stream']!=address or d['byte']!=index or d['glyph_index']!=index or d['offset']!=off or d['context']!=0x0200FA20 or ram[address-0x02000000]!=index or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record:raise ValueError('native Jan1 date insertion/position/font')
            expected[address]={'ch':'native date digit/space','index':index,'record':record,'id':'native-date-buffer'}
        if any(ram[address-0x02000000+2]!=0xE5 for address in (0x02010AC0,0x02010B40)):raise ValueError('native date buffer terminator')
        for key,start in zip(keys,[0,month_end,end]):
            row=0;x=start;cursor=iter(streams[key])
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;x=0;continue
                s=next(cursor)
                if last[s]['offset']!=row*10752+x*4:raise ValueError('date literal exact geometry')
                x+=advance(e[s]['index'])
        draws=[last[s] for s in selected]+dynamic;counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU font supply')
        proof=pixels(path,step,draws,expected,rom,m,origin=(52,110),cursor_indices=());im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=52+off//4;y=110+row*14;rects.append((x,y,x+advance(d['glyph_index']),y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('date stale pixels')
        pages.append({'step':step,'native_date':'Jan1 only','native_digit_draws':dynamic,'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof})
    result={'passed':True,'release_eligible':False,'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],'added_units':3,'normal_runtime_units':keys,'diagnostic_runtime_units':[],'prior11_units_unchanged':True,'static':checks,'pages':pages,'limits':['Normal Jan1 opening only; two-digit months/days, rollover and RTC correctness not claimed.','Frequency selector source scripts119..123 did not show observed reads in separate source probes; no frequency translation claim.','Basic names/input/save/reload/full-game/hardware/audio/human approval remain open.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'date_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('normal calendar date QA',True);return result
def regressions():
    import report_calendar_types as types
    types.STEM=STEM;types.CAPTURE_STEM=STEM;types.PREFIX=PREFIX;types.OUTDIR=OUTDIR;types.TOTAL_UNITS=1090;types.main();types.regressions()
if __name__=='__main__':main();regressions()
