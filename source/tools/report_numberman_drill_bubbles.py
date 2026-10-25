"""Finite small-bubble pixel proof; unvisited scripts remain runtime-open."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from report_numberman_drill_intro import page as intro_page
from archive_scripts import script_spans

STEM='exe45_ko_development_numberman_drill_bubbles_v1'
PREFIX='numberman-drill-bubbles-v1-'

def bubble(path,step,key,m,rom,e,streams,pool):
    r=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();script=int(key.split(':')[1]);wanted=set(streams[key])
    if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=script:raise ValueError('bubble active root/script')
    cursor=struct.unpack_from('<I',r,0xFA4C)[0]
    if not min(wanted)<=cursor<=max(wanted)+20:raise ValueError('bubble active cursor')
    obs=read(path/f'step_{step:03}_roll_pet.json');last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
    if set(last)!=wanted:raise ValueError('bubble incomplete stream')
    draws=[last[s] for s in streams[key]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('bubble font read coverage')
    proof=pixels(path,step,draws,e,rom,m,origin=(10,18));occupied=set()
    for d in draws:
        row,off=divmod(d['offset'],10752);x0=10+off//4;y0=18+14*row;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
        if row>2 or x0+w>70 or y0+12>58:raise ValueError('bubble adopted bounds')
        occupied.update((x,y) for y in range(y0,y0+12) for x in range(x0,x0+w))
    im=Image.open(path/f'step_{step:03}.png').convert('RGB');blank={(x,y) for y in range(18,58) for x in range(10,70)}-occupied
    if {im.getpixel(p) for p in blank}!={im.getpixel((71,19))}:raise ValueError('bubble clearing')
    return {'route':path.name,'step':step,'units':[key],'cursor':cursor,'vacant_pixels_cleared':len(blank),'screenshot_sha256':sha((path/f'step_{step:03}.png').read_bytes()),**proof}

def main():
    m,rom,e,streams,checks=static(STEM,'715064');rt=ROOT/'poc/runtime';seen=set();pages=[];incomplete=[]
    if m['translated_units']!=1245 or len(m['archives'])!=26:raise ValueError('bubble denominator')
    old=ROOT/'poc/output/exe45_ko_development_numberman_drill_intro_v1.gba';om=read(old.with_suffix('.json'));previous=old.read_bytes()
    if sha(previous)!=om['output_sha256']:raise ValueError('old identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['archive']=='715064':continue
        if a['compiled_sha256']!=n['compiled_sha256'] or previous[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('retained25 payloads')
    if rom[0x6333A4:0x6334A4]!=previous[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','drill','game']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
    ar=next(a for a in m['archives'] if a['archive']=='715064');pool=0x08000000+ar['rom_offset']
    oa=next(a for a in om['archives'] if a['archive']=='715064')
    oldspans=script_spans(previous[oa['rom_offset']:oa['rom_offset']+oa['compiled_bytes']],16)
    newspans=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],16)
    if any(oldspans[i]!=newspans[i] for i in [0,1]):raise ValueError('retained intro/lecture binary drift')
    for pointer in [0xDD394,0xDD894]:
        if struct.unpack_from('<I',rom,pointer)[0]!=pool:raise ValueError('both roots')
    drill=rt/(PREFIX+'drill')
    pages.extend(intro_page(drill,step,[f'715064:0:{i}'],m,rom,e,streams,pool) for i,step in enumerate([12,13,14]))
    pages.extend(intro_page(drill,step,['715064:0:3','715064:0:4'],m,rom,e,streams,pool) for step in [15,16])
    small={k for k in streams if int(k.split(':')[1]) in list(range(2,13))+[14]}
    paths=[rt/(PREFIX+'game')]
    # Additional normal-controller descendants are optional; each receipt is
    # checked recursively against this ROM, never another candidate's state.
    paths.extend(p for p in sorted(rt.glob(PREFIX+'game-*')) if (p/'result.json').exists())
    for path in paths:
        r=verify_route(path,m['output_sha256'],seen)
        for step in r['capture_steps']:
            ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();key=f'715064:{ram[0xFA21]}:0'
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or key not in small:continue
            obs=read(path/f'step_{step:03}_roll_pet.json');wanted=set(streams[key]);last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
            if set(last)!=wanted:incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'still typing or no new load in this observer'});continue
            first=last[streams[key][0]]['frame']
            if any(d['frame']<first for d in last.values()):
                incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'repeat instance is still typing; earlier same-script glyphs not credited'});continue
            snapshot=read(path/f'step_{step:03}_state.json');snapshot_frame=snapshot['frame']
            # This report deliberately credits settled visible snapshots only.
            # New CPU draw != completed VRAM/display transfer. Keep every
            # First observations showed samples at draw+1 and draw+4 still
            # in flight, followed by strict matching frames. Adopt >=6-frame
            # settling for credit; this is not a hardware latency bound.
            if snapshot_frame-max(d['frame'] for d in last.values())<=5:
                incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'within5frames of last CPU glyph draw; transfer/display settlement not credited'});continue
            if snapshot['state']['ppu.blendMainControl']!=0:
                incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'native PPU blend/effect mode outside normal unflashed text proof','blendMainControl':snapshot['state']['ppu.blendMainControl'],'brightness':snapshot['state']['ppu.brightness']});continue
            # A completed parser stream can survive after the timed window is
            # closed. Residency is a separate prerequisite, not a pixel waiver.
            o=(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();resident=False
            for i in range(128):
                a,b,k=struct.unpack_from('<HHH',o,i*8)
                if not a&0x2300 and k>>12==14 and k&1023!=1020 and (a&255)==18 and (b&511)<=10:resident=True
            if not resident:incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'completed parser remains but small text OBJ window no longer resident'});continue
            im=Image.open(path/f'step_{step:03}.png').convert('RGB')
            if im.getpixel((71,19))!=(248,236,212):
                incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'outside normal unflashed bubble background scope; native explosion/fade transition not credited'});continue
            if len({im.getpixel((x,y)) for y in range(18,58) for x in range(10,70)})==1:
                incomplete.append({'route':path.name,'step':step,'unit':key,'reason':'uniform explosion/transition region, no visible text claim'});continue
            pages.append(bubble(path,step,key,m,rom,e,streams,pool))
    observed={k for p in pages for k in p['units']}&small
    if not {'715064:12:0','715064:5:0'}<=observed:raise ValueError('initial/wrong-answer bubble coverage')
    dest=ROOT/'analysis/numberman_drill_bubbles_v1';dest.mkdir(parents=True,exist_ok=True)
    # One complete frame per observed small script, plus retained intro pages.
    chosen=pages[:5]+[next(p for p in pages if key in p['units']) for key in sorted(observed)]
    sheet=Image.new('RGB',(720,160*((len(chosen)+2)//3)))
    for i,p in enumerate(chosen):sheet.paste(Image.open(rt/p['route']/f"step_{p['step']:03}.png"),(i%3*240,i//3*160))
    sheet.save(dest/'bubble_pages.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':12,'selected_text_units':1245,'static':checks,'retained25_payloads_identical':True,'both_roots_relocated':True,'pages':pages,'incomplete_not_credited':incomplete,'runtime_observed_new_units':sorted(observed),'runtime_open_new_units':sorted(small-observed),'limits':['Only observed small scripts and retained intro0 get runtime credit; lecture1 wording/control/font preservation static, not new full lecture traversal.','Level13/exam15/results/rewards remain Japanese. No full gameplay success/reward or exact hardware timing claim.','Hangul user-name input/committed record/redisplay and persistence/old saves unresolved.','Human wording approval/full game/audio/RTC/hardware/release incomplete.']}
    result['retained_intro_lecture_script_bytes_identical']=True
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan bubbles: PASS',sorted(observed),'open',sorted(small-observed));return result

if __name__=='__main__':main()
