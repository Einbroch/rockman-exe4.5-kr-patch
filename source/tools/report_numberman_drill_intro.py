"""Exact-ROM bottom drill intro/lecture glyph, choice and clearing checks."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route

STEM='exe45_ko_development_numberman_drill_intro_v1'
PREFIX='numberman-drill-intro-v1-'

def page(path,step,keys,m,rom,e,streams,pool):
    r=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();script=int(keys[0].split(':')[1]);cursor=struct.unpack_from('<I',r,0xFA4C)[0]
    if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=script:raise ValueError('drill active root/script')
    wanted={s for k in keys for s in streams[k]}
    if not min(wanted)<=cursor<=max(wanted)+20:raise ValueError('drill current cursor')
    obs=read(path/f'step_{step:03}_roll_pet.json');entry=max((c['frame'] for c in obs['calls']),default=0)
    last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted and d['frame']>=entry}
    if set(last)!=wanted:raise ValueError('drill complete current glyphs')
    draws=[last[s] for k in keys for s in streams[k]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('drill full font reads')
    proof=pixels(path,step,draws,e,rom,m,origin=(52,110),cursor_screen_background=True)
    im=Image.open(path/f'step_{step:03}.png').convert('RGB');occupied=set()
    for d in draws:
        row,off=divmod(d['offset'],10752);x0=52+off//4;y0=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
        occupied.update((x,y) for y in range(y0,y0+12) for x in range(x0,x0+w))
    o=(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0);cursor_rect=set()
    if k&1023==1020 and k>>12==14:cursor_rect={(x,y) for y in range(a&255,(a&255)+16) for x in range(b&511,(b&511)+16)}
    blank={(x,y) for y in range(110,150) for x in range(52,228) if (x,y) not in occupied|cursor_rect}
    if {im.getpixel(xy) for xy in blank}!={im.getpixel((225,112))}:raise ValueError('drill vacant page pixels')
    return {'route':path.name,'step':step,'units':keys,'cursor':cursor,'vacant_pixels_cleared':len(blank),'screenshot_sha256':sha((path/f'step_{step:03}.png').read_bytes()),**proof}

def main():
    m,rom,e,streams,checks=static(STEM,'715064');rt=ROOT/'poc/runtime';seen=set()
    if m['translated_units']!=1233 or len(m['archives'])!=26:raise ValueError('drill denominator')
    old=ROOT/'poc/output/exe45_ko_development_numberman_jackin_v1.gba';pm=read(old.with_suffix('.json'));pr=old.read_bytes()
    if sha(pr)!=pm['output_sha256']:raise ValueError('previous identity')
    for a in pm['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['compiled_sha256']!=n['compiled_sha256'] or pr[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('previous25 payload drift')
    if rom[0x6333A4:0x6334A4]!=pr[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','drill','lecture']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold chain')
    ar=next(x for x in m['archives'] if x['archive']=='715064');pool=0x08000000+ar['rom_offset']
    for p in [0xDD394,0xDD894]:
        if struct.unpack_from('<I',rom,p)[0]!=pool:raise ValueError('both drill roots relocated')
    drill=rt/(PREFIX+'drill');lecture=rt/(PREFIX+'lecture')
    pages=[page(drill,step,[f'715064:0:{i}'],m,rom,e,streams,pool) for i,step in enumerate([12,13,14])]
    pages.extend(page(drill,step,['715064:0:3','715064:0:4'],m,rom,e,streams,pool) for step in [15,16])
    pages.extend(page(lecture,step,[f'715064:1:{i}'],m,rom,e,streams,pool) for i,step in enumerate(range(1,14)))
    pages.extend(page(lecture,step,['715064:1:13','715064:1:14'],m,rom,e,streams,pool) for step in [14,15])
    for path,step,y,x in [(drill,15,108,47),(drill,16,122,47),(lecture,14,108,36),(lecture,15,122,36)]:
        a,b,k=struct.unpack_from('<HHH',(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes(),0)
        if (a&255,b&511,k&1023,k>>12)!=(y,x,1020,14):raise ValueError('drill vertical choice focus')
    # select's internal script jump does not call the external root-entry
    # routine0804F7B6. Require parent script0 selection, current script1/root
    # and its full new glyph stream instead of inventing an external call.
    parent=(drill/'step_016_gbaExtWorkRam.bin').read_bytes();child=(lecture/'step_001_gbaExtWorkRam.bin').read_bytes()
    if parent[0xFA21]!=0 or child[0xFA21]!=1 or any(struct.unpack_from('<I',r,0xFA50)[0]!=pool for r in [parent,child]):raise ValueError('native internal lecture choice branch')
    _,_,pe,ps,_=static(STEM,'6873F4');intro=rt/(PREFIX+'intro');pet_pages=[]
    petpool=0x08000000+next(a for a in m['archives'] if a['archive']=='6873F4')['rom_offset']
    for step in read(intro/'result.json')['capture_steps']:
        r=(intro/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();script=r[0xFA21]
        if struct.unpack_from('<I',r,0xFA50)[0]!=petpool or script not in [1,2]:continue
        keys=[k for k in ps if int(k.split(':')[1])==script];wanted={s for k in keys for s in ps[k]}
        obs=read(intro/f'step_{step:03}_roll_pet.json');last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
        if set(last)!=wanted:continue
        pet_pages.append({'step':step,'script':script,**pixels(intro,step,[last[s] for k in keys for s in ps[k]],pe,rom,m,cursor_screen_background=True)})
    if not any(p['script']==2 for p in pet_pages):raise ValueError('current PET prompt regression')
    dest=ROOT/'analysis/numberman_drill_intro_v1';dest.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,1120))
    for i,p in enumerate(pages):sheet.paste(Image.open(rt/p['route']/f"step_{p['step']:03}.png"),(i%3*240,i//3*160))
    sheet.save(dest/'drill_pages.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':20,'selected_text_units':1233,'static':checks,'previous25_payloads_identical':True,'both_roots_relocated':True,'pages':pages,'runtime_observed_units':sorted({k for p in pages for k in p['units']}),'limits':['Academic-exam variant15, small timed bubbles2..12/14, level selection13 and results/rewards remain source Japanese.','Lecture final options preserve all-targets-continue; no full minigame completion or repeat-lecture behavior claim.','Hangul name entry/committed record/redisplay, persistence reload and old-save compatibility unresolved.','No full-game/RTC/audio/hardware or human wording/release approval.']}
    result.update(native_internal_lecture_branch=True,current_pet_regression=pet_pages,observer_limit='External root entry hook does not observe select internal jumps. Initial report rejected for that unsupported expectation; full glyph/pixel checks had passed. Parent0 choice -> child1 root/stream checks used.')
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan drill intro/lecture: PASS');return result

if __name__=='__main__':main()
