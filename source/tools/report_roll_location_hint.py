"""Exact-ROM diagnostic hint23 page and native clearing evidence."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
import capture_roll_location_hint as observer
import capture_roll_pet

STEM='exe45_ko_development_roll_location_v3'
PREFIX='roll-location-v3-'

def main():
    m,rom,expected,streams,checks=static(STEM,'65FF3C');path=ROOT/'poc/runtime'/(PREFIX+'hint23-diagnostic')
    receipt=verify_route(path,m['output_sha256'],set());env=read(path/'hint_environment.json')
    if receipt.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or not (path/'diagnostic_checkpoint.mss').exists():raise ValueError('hint state quarantine')
    if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['tool_sha256']!=sha(PathBytes(observer.__file__)) or env['observer_sha256']!=sha(PathBytes(capture_roll_pet.__file__)):raise ValueError('hint environment')
    unit='65FF3C:23:0';pages=[]
    for step in receipt['capture_steps']:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes()
        if ram[0xFA21]!=23:continue
        ar=next(a for a in m['archives'] if a['archive']=='65FF3C')
        if struct.unpack_from('<I',ram,0xFA50)[0]!=0x08000000+ar['rom_offset']:raise ValueError('hint root')
        cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
        if not min(streams[unit])<=cursor<=max(streams[unit])+5:continue
        state=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in state['draws'] if d['stream'] in streams[unit]}
        if set(last)!=set(streams[unit]):continue
        draws=[last[s] for s in streams[unit]];counts=Counter(expected[d['stream']]['index'] for d in draws);reads={r['index']:r['reads'] for r in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('hint CPU font reads')
        p=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;i=expected[d['stream']]['index'];w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(x)!=bg for x in vacant):raise ValueError('hint stale pixels')
        p.update(step=step,unit=unit,vacant_text_pixels_cleared=len(vacant),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()));pages.append(p)
    if not pages:raise ValueError('no complete hint23 page')
    out=ROOT/'analysis/roll_location_v3';out.mkdir(parents=True,exist_ok=True)
    # Prove the preceding native lucky-item page, not only a screenshot label.
    previous=(path/'step_006_gbaExtWorkRam.bin').read_bytes();previous_unit='65FF3C:10:4'
    previous_cursor=struct.unpack_from('<I',previous,0xFA4C)[0]
    if previous[0xFA21]!=10 or not min(streams[previous_unit])<=previous_cursor<=max(streams[previous_unit])+5:raise ValueError('hint predecessor cursor')
    previous_draws={d['stream']:d for d in read(path/'step_006_roll_pet.json')['draws'] if d['stream'] in streams[previous_unit]}
    if set(previous_draws)!=set(streams[previous_unit]):raise ValueError('hint predecessor glyph coverage')
    predecessor=pixels(path,6,list(previous_draws.values()),expected,rom,m)
    sheet=Image.new('RGB',(480,160));sheet.paste(Image.open(path/'step_006.png'),(0,0));sheet.paste(Image.open(path/f"step_{pages[0]['step']:03}.png"),(240,0));sheet.save(out/'hint_transition.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'diagnostic_units':[unit],'predecessor':{'unit':previous_unit,'step':6,**predecessor},'pages':pages,'native_clear':env,'limits':['Native EE33 read alias20->23, not real item-location selection/acquisition.','Human wording/visual review and whole-game QA pending.']}
    (out/'hint_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'hint_runtime.json');return result

def PathBytes(path):
    from pathlib import Path
    return Path(path).read_bytes()

if __name__=='__main__':main()
