"""NumberMan transmission slogan: native lookup/font/pixels/wait lifecycle."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,static,sha,verify_route
from report_numberman_training_intro import page,ram

STEM='exe45_ko_development_numberman_jackin_v1'
PREFIX='numberman-jackin-v1-'

def glyph_vram(path,step,draw,index,rom,m):
    o=(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();v=(path/f'step_{step:03}_gbaVideoRam.bin').read_bytes();objects=[]
    sizes=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]]
    for i in range(128):
        a,b,k=struct.unpack_from('<HHH',o,i*8)
        if not a&0x2300 and a>>14<3 and k>>12==14 and k&1023!=1020:
            w,h=sizes[a>>14][b>>14];objects.append((b&511,a&255,k&1023,w,h))
    row,off=divmod(draw['offset'],10752);x0=92+off//4;y0=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0];result={}
    for y in range(y0,y0+12):
        for x in range(x0,x0+width):
            matches=[q for q in objects if q[0]<=x<q[0]+q[3] and q[1]<=y<q[1]+q[4]]
            if len(matches)!=1:raise ValueError('in-flight unique glyph residency')
            ox,oy,tile,w,h=matches[0];lx=x-ox;ly=y-oy;at=0x10000+tile*32+(ly//8*(w//8)+lx//8)*32+(ly%8)*4+lx%8//2
            result[x,y]=(v[at]>>(4*(lx%2)))&15
    return result

def main():
    m,rom,e,streams,checks=static(STEM,'687E3C');key='687E3C:1:0'
    if m['translated_units']!=1213 or len(m['archives'])!=25:raise ValueError('scope denominator')
    old=ROOT/'poc/output/exe45_ko_development_numberman_training_intro_v1.gba';pm=read(old.with_suffix('.json'));pr=old.read_bytes()
    if sha(pr)!=pm['output_sha256']:raise ValueError('previous identity')
    for a in pm['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['compiled_sha256']!=n['compiled_sha256'] or pr[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('previous24 payload drift')
    if rom[0x6333A4:0x6334A4]!=pr[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    rt=ROOT/'poc/runtime';seen=set();chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','warning','transmission']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
    wm,_,we,ws,wc=static(STEM,'687910');war=next(x for x in m['archives'] if x['archive']=='687910');wp=0x08000000+war['rom_offset'];warning=rt/(PREFIX+'warning')
    prior_warning=page(warning,13,['687910:21:0'],m,rom,we,ws,wp)
    ar=next(x for x in m['archives'] if x['archive']=='687E3C');pool=0x08000000+ar['rom_offset'];wait_end=max(streams[key])+1
    if rom[wait_end-0x08000000:wait_end-0x08000000+4]!=bytes.fromhex('ed001e00'):raise ValueError('compiled source wait30 boundary')
    p=rt/(PREFIX+'transmission');receipt=read(p/'result.json');waits=[];released=[];pages=[];in_flight=[]
    for step in receipt['capture_steps']:
        r=ram(p,step);cursor=struct.unpack_from('<I',r,0xFA4C)[0];frame=read(p/f'step_{step:03}.json')['frame']
        if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=1:continue
        if cursor==wait_end:
            waits.append({'step':step,'frame':frame})
            obs=read(p/f'step_{step:03}_roll_pet.json');last={d['stream'] for d in obs['draws']}
            if not set(streams[key])<=last:continue
            try:proof=page(p,step,[key],m,rom,e,streams,pool)
            except ValueError as ex:
                if str(ex) not in ['PET visible role colors disagree','PET ROM glyph -> OBJ VRAM pixel']:raise
                in_flight.append({'step':step,'frame':frame,'failure':str(ex),'credited':False});continue
            pages.append({**proof,'frame':frame})
        elif cursor>wait_end:released.append({'step':step,'frame':frame})
    if not pages or not waits or not released:raise ValueError('missing complete slogan or wait lifecycle')
    # A transient snapshot is never a pixel pass. Explain each failure against
    # a later strict pass with exactly the same parser/glyph trace; reject any
    # difference outside the source-preserved terminal !! pair. VRAM changes
    # must be confined to the final glyph; screenshots may still contain the
    # preceding ! from the earlier rendered frame. Neither is credited.
    for pending in in_flight:
        early=read(p/f"step_{pending['step']:03}_roll_pet.json");settled=next((q for q in pages if q['step']>pending['step'] and read(p/f"step_{q['step']:03}_roll_pet.json")==early),None)
        if settled is None:raise ValueError('no identical-trace settled snapshot')
        draws=[d for d in early['draws'] if d['stream'] in streams[key]];last=draws[-1];region=set(glyph_vram(p,settled['step'],last,e[last['stream']]['index'],rom,m));screen_region=set();vdelta=set()
        if ''.join(e[d['stream']]['ch'] for d in draws[-2:])!='!!':raise ValueError('source terminal pair identity')
        for d in draws[-2:]:screen_region.update(glyph_vram(p,settled['step'],d,e[d['stream']]['index'],rom,m))
        for d in draws:
            before=glyph_vram(p,pending['step'],d,e[d['stream']]['index'],rom,m);after=glyph_vram(p,settled['step'],d,e[d['stream']]['index'],rom,m)
            vdelta.update(xy for xy in before if before[xy]!=after[xy])
        a=Image.open(p/f"step_{pending['step']:03}.png").convert('RGB');b=Image.open(p/f"step_{settled['step']:03}.png").convert('RGB');sdelta={(x,y) for y in range(110,150) for x in range(92,234) if a.getpixel((x,y))!=b.getpixel((x,y))}
        if not(vdelta or sdelta) or not vdelta<=region or not sdelta<=screen_region:raise ValueError('unexplained in-flight text differences')
        pending.update(later_strict_pass_step=settled['step'],same_observer_trace=True,vram_changed_pixels=len(vdelta),screen_changed_pixels=len(sdelta),vram_changes_confined_to_final_glyph=True,screen_changes_confined_to_terminal_pair=True,terminal_draws=draws[-2:])
    firstwait=min(x['frame'] for x in waits);firstrelease=min(x['frame'] for x in released)
    # Frame callbacks sample the native parser around its wait decrement;
    # retain the measured interval rather than infer exact hardware timing.
    if not 30<=firstrelease-firstwait<=31:raise ValueError('native wait30 sampled interval')
    selected=pages[0];obs=read(p/f"step_{selected['step']:03}_roll_pet.json");end=read(p/f"step_{receipt['capture_steps'][-1]:03}_roll_pet.json")
    if len(end['calls'])!=1 or end['calls'][0]['root']!=pool or end['calls'][0]['script']!=1 or obs['calls']!=end['calls'] or obs['draws']!=end['draws']:raise ValueError('native entry/draw lifetime')
    dest=ROOT/'analysis/numberman_jackin_v1';dest.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,(path,step) in enumerate([(warning,13),(p,selected['step']),(p,receipt['capture_steps'][-1])]):sheet.paste(Image.open(path/f'step_{step:03}.png'),(i*240,0))
    sheet.save(dest/'jackin_pages.png');Image.open(p/f"step_{selected['step']:03}.png").save(dest/'transmission.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':1,'selected_text_units':1213,'static':checks,'previous24_payloads_identical':True,'prior_warning_current_rom':prior_warning,'pages':pages,'in_flight_not_credited':in_flight,'native_entry':end['calls'],'wait_cursor_samples':waits,'released_cursor_samples':released,'sampled_wait_interval_frames':firstrelease-firstwait,'draws_stopped_after_slogan':True,'tool_sha256':sha((ROOT/'tools/report_numberman_jackin.py').read_bytes()),'limits':['One3-row transmission unit, not full-game completion.','Post-slogan snapshot is direct observed transition evidence, not all network gameplay/reentry/return/battle proof.','No current save execution, Hangul input, persistence reload/old-save compatibility, RTC/audio/hardware or human release approval.']}
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan slogan/font/pixels/clearing/native wait: PASS');return result

if __name__=='__main__':main()
