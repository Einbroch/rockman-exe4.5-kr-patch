"""NumberMan training invitations: finite static scope and native choice paths."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route

STEM='exe45_ko_development_numberman_training_intro_v1'
PREFIX='numberman-training-intro-v1-'

def ram(path,step):return (path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()

def page(path,step,keys,m,rom,e,streams,pool):
    r=ram(path,step);script=int(keys[0].split(':')[1]);cursor=struct.unpack_from('<I',r,0xFA4C)[0]
    if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=script:raise ValueError('active page script/root')
    wanted={s for k in keys for s in streams[k]}
    if not min(wanted)<=cursor<=max(wanted)+16:raise ValueError('current page cursor')
    obs=read(path/f'step_{step:03}_roll_pet.json');entry=max((c['frame'] for c in obs['calls']),default=0)
    last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted and d['frame']>=entry}
    if set(last)!=wanted:raise ValueError('complete current glyph stream')
    draws=[last[s] for k in keys for s in streams[k]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('actual font CPU reads')
    proof=pixels(path,step,draws,e,rom,m,cursor_screen_background=True)
    im=Image.open(path/f'step_{step:03}.png').convert('RGB');occupied=set()
    for d in draws:
        row,off=divmod(d['offset'],10752);x0=92+off//4;y0=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
        occupied.update((x,y) for y in range(y0,y0+12) for x in range(x0,x0+width))
    o=(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0)
    cursor_rect=set()
    if k&1023==1020 and k>>12==14:
        cursor_rect={(x,y) for y in range(a&255,(a&255)+16) for x in range(b&511,(b&511)+16)}
    blank={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied|cursor_rect and not(x>=220 and y>=140)}
    if {im.getpixel(xy) for xy in blank}!={im.getpixel((231,112))}:raise ValueError('page/choice vacant region clear')
    return {'route':path.name,'step':step,'units':keys,'cursor':cursor,'vacant_pixels_cleared':len(blank),'screenshot_sha256':sha((path/f'step_{step:03}.png').read_bytes()),**proof}

def main():
    m,rom,e,streams,checks=static(STEM,'687910')
    if m['translated_units']!=1212 or len(m['archives'])!=24:raise ValueError('scope denominator')
    old=ROOT/'poc/output/exe45_ko_development_numberman_pet_v1.gba';pm=read(old.with_suffix('.json'));pr=old.read_bytes()
    if sha(pr)!=pm['output_sha256']:raise ValueError('previous identity')
    for a in pm['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['compiled_sha256']!=n['compiled_sha256'] or pr[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('previous23 payload drift')
    if rom[0x6333A4:0x6334A4]!=pr[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','entry']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
    for name in ['decline-full','accept']:
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        parent='intro' if name=='decline-full' else 'entry'
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json'):raise ValueError('own choice ancestry')
    ar=next(x for x in m['archives'] if x['archive']=='687910');pool=0x08000000+ar['rom_offset'];entry=rt/(PREFIX+'entry');decline=rt/(PREFIX+'decline-full');accept=rt/(PREFIX+'accept')
    pages=[page(entry,step,[f'687910:20:{i}'],m,rom,e,streams,pool) for i,step in enumerate([5,6,7,8,9])]
    choicekeys=['687910:20:5','687910:20:6'];pages.append(page(entry,10,choicekeys,m,rom,e,streams,pool));pages.append(page(decline,11,choicekeys,m,rom,e,streams,pool));pages.append(page(decline,13,['687910:21:0'],m,rom,e,streams,pool))
    obs=read(entry/'step_010_roll_pet.json')
    if not any(c['root']==pool and c['script']==20 for c in obs['calls']):raise ValueError('native script20 entry')
    for path,step,x in [(entry,10,108),(decline,11,144)]:
        o=(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0)
        if (a&255,b&511,k&1023,k>>12)!=(108,x,1020,14):raise ValueError('standalone choice cursor')
    out=ram(decline,15);pet=next(x for x in m['archives'] if x['archive']=='6873F4');petpool=0x08000000+pet['rom_offset']
    if struct.unpack_from('<I',out,0xFA50)[0]!=0x08687E3C or out[0xFA21]!=1:raise ValueError('decline training continues Jack-In')
    for step in [2,3]:
        r=ram(accept,step)
        if struct.unpack_from('<I',r,0xFA50)[0]!=0x08715064:raise ValueError('native accepted minigame entry')
    # Previous PET stream remains intact and executes on this exact cumulative
    # ROM; do not transfer the old ROM's runtime claims via payload equality.
    pm2,_,pe,ps,pc=static(STEM,'6873F4');intro=rt/(PREFIX+'intro');pet_pages=[]
    for step in read(intro/'result.json')['capture_steps']:
        r=ram(intro,step)
        if struct.unpack_from('<I',r,0xFA50)[0]!=petpool:continue
        script=r[0xFA21];keys=[k for k in ps if int(k.split(':')[1])==script]
        if script not in [1,2] or not keys:continue
        obs=read(intro/f'step_{step:03}_roll_pet.json');wanted={s for k in keys for s in ps[k]};last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
        if set(last)!=wanted:continue
        pet_pages.append({'step':step,'script':script,**pixels(intro,step,[last[s] for k in keys for s in ps[k]],pe,rom,m,cursor_screen_background=True)})
    if not any(p['script']==2 for p in pet_pages):raise ValueError('current PET normal prompt regression')
    dest=ROOT/'analysis/numberman_training_intro_v1';dest.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,640))
    for i,p in enumerate(pages):sheet.paste(Image.open(rt/p['route']/f"step_{p['step']:03}.png"),(i%2*240,i//2*160))
    sheet.save(dest/'training_pages.png');observed={k for p in pages for k in p['units']}
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':16,'selected_text_units':1212,'static':checks,'previous23_payloads_identical':True,'pages':pages,'runtime_observed_units':sorted(observed),'runtime_open_units':sorted(set(streams)-observed),'standalone_yes_no_focus':True,'decline_script21_then_native_jackin_root':'0x08687E3C','accepted_native_minigame_root':'0x08715064','current_pet_regression':pet_pages,'tool_sha256':sha((ROOT/'tools/report_numberman_training_intro.py').read_bytes()),'limits':['General invitation10/decline11 (8units) static only; actual source path reached20/21.','Training decline continues existing Jack-In; its687E3C slogan remains Japanese.','Minigame entry only, not minigame text/graphics/results/rewards or completed gameplay.','No Hangul name input, persistence reload/old-save compatibility, RTC/audio/hardware/full-game/human release approval.']}
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan training pages/choices/decline-to-Jack-In/accept/current PET: PASS');return result

if __name__=='__main__':main()
