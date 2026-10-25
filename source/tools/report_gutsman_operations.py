"""Three finite archives plus genuine timed Jack-In; preserve transient evidence."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,verify_route
from report_gutsman_pet import main as pet_regression
from report_numberman_training_intro import page,ram
from report_numberman_jackin import glyph_vram
from run_gutsman_operations import STEM,PREFIX

def main():
    out=ROOT/'analysis/gutsman_operations_v1'
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2219,52,680),oldstem='exe45_ko_development_gutsman_pet_v1',outdir='gutsman_operations_v1/pet_regression',inventory_outdir='full_scope_gutsman_operations_v1',added_literal_units=0)
    checks={};bindings=[]
    for archive,root in [('6663B8',0x38118),('6664D0',0x38120),('666820',0x38128)]:
        m,rom,e,s,c=static(STEM,archive);checks[archive]=c;ar=next(x for x in m['archives'] if x['archive']==archive);pool=0x8000000+ar['rom_offset']
        if struct.unpack_from('<I',rom,root)[0]!=pool:raise ValueError('operations native binding')
        bindings.append(dict(archive=archive,root_offset=root,rom_pointer=pool))
    if sum(x['new_units'] for x in checks.values())!=31:raise ValueError('operations population')
    m,rom,e,s,_=static(STEM,'6664D0');pool=0x8000000+next(x for x in m['archives'] if x['archive']=='6664D0')['rom_offset'];key='6664D0:1:0';wait_end=max(s[key])+1
    if rom[wait_end-0x8000000:wait_end-0x8000000+4]!=bytes.fromhex('ed001e00'):raise ValueError('source wait30 boundary')
    rt=ROOT/'poc/runtime';seen=set()
    for name,parent in [('jackin-prompt-r2','select-gutsman'),('transmission-r2','jackin-prompt-r2')]:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen)
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json') or r.get('normal_play_checkpoint_eligible') is False or any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('native Jack-In ancestry/intervention')
    prompt=rt/(PREFIX+'jackin-prompt-r2');pr=ram(prompt,4);petpool=0x8000000+next(x for x in m['archives'] if x['archive']=='665F3C')['rom_offset']
    if pr[0xFA21]!=3 or struct.unpack_from('<I',pr,0xFA50)[0]!=petpool:raise ValueError('native PET3 Jack-In question not observed')
    p=rt/(PREFIX+'transmission-r2');receipt=read(p/'result.json');waits=[];released=[];settled=[];transients=[]
    for step in receipt['capture_steps']:
        r=ram(p,step);cursor=struct.unpack_from('<I',r,0xFA4C)[0];frame=read(p/f'step_{step:03}.json')['frame']
        if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=1:continue
        if cursor==wait_end:
            waits.append(dict(step=step,frame=frame));obs=read(p/f'step_{step:03}_roll_pet.json')
            if not set(s[key])<={d['stream'] for d in obs['draws']}:continue
            try:proof=page(p,step,[key],m,rom,e,s,pool)
            except ValueError as ex:
                if str(ex) not in ['PET visible role colors disagree','PET ROM glyph -> OBJ VRAM pixel']:raise
                transients.append(dict(step=step,frame=frame,failure=str(ex),credited=False));continue
            settled.append(dict(**proof,frame=frame))
        elif cursor>wait_end:released.append(dict(step=step,frame=frame))
    if not settled or not waits or not released:raise ValueError('normal slogan/wait lifecycle not observed')
    for q in transients:
        early=read(p/f"step_{q['step']:03}_roll_pet.json");later=next((x for x in settled if x['step']>q['step'] and read(p/f"step_{x['step']:03}_roll_pet.json")==early),None)
        if later is None:raise ValueError('no identical-trace strict settled snapshot')
        draws=[d for d in early['draws'] if d['stream'] in s[key]]
        if ''.join(e[d['stream']]['ch'] for d in draws[-2:])!='!!':raise ValueError('source terminal pair')
        last=draws[-1];region=set(glyph_vram(p,later['step'],last,e[last['stream']]['index'],rom,m));screen_region=set();delta=set()
        for d in draws[-2:]:screen_region.update(glyph_vram(p,later['step'],d,e[d['stream']]['index'],rom,m))
        for d in draws:
            a=glyph_vram(p,q['step'],d,e[d['stream']]['index'],rom,m);b=glyph_vram(p,later['step'],d,e[d['stream']]['index'],rom,m);delta.update(xy for xy in a if a[xy]!=b[xy])
        a=Image.open(p/f"step_{q['step']:03}.png").convert('RGB');b=Image.open(p/f"step_{later['step']:03}.png").convert('RGB');sd={(x,y) for y in range(110,150) for x in range(92,234) if a.getpixel((x,y))!=b.getpixel((x,y))}
        if not(delta or sd) or not delta<=region or not sd<=screen_region:raise ValueError('unexplained in-flight differences')
        q.update(later_strict_pass_step=later['step'],same_observer_trace=True,vram_changed_pixels=len(delta),screen_changed_pixels=len(sd),vram_changes_confined_to_final_glyph=True,screen_changes_confined_to_terminal_pair=True)
    interval=min(q['frame'] for q in released)-min(q['frame'] for q in waits)
    if not 30<=interval<=31:raise ValueError('sampled native wait30 interval')
    selected=settled[0];obs=read(p/f"step_{selected['step']:03}_roll_pet.json");end=read(p/f"step_{receipt['capture_steps'][-1]:03}_roll_pet.json")
    if len(end['calls'])!=1 or end['calls'][0]['root']!=pool or end['calls'][0]['script']!=1 or obs['calls']!=end['calls'] or obs['draws']!=end['draws']:raise ValueError('slogan entry/draw lifetime')
    out.mkdir(parents=True,exist_ok=True);Image.open(p/f"step_{selected['step']:03}.png").save(out/'normal_transmission.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=31,new_translated_prose=17,source_identical_exclamations=14,selected_text_units=2219,archives_static=checks,native_operations_bindings=bindings,pet_regression=baseline,normal_transmission_pages=settled,in_flight_not_credited=transients,native_entry=end['calls'],wait_cursor_samples=waits,released_cursor_samples=released,sampled_wait_interval_frames=interval,draws_stopped_after_slogan=True,remaining_catalog=baseline['remaining_catalog'],limits=['One native timed GutsMan slogan. Return2 and mail28 literals static-only; no return success/defeat/mail delivery flags/tournament event/name consumer runtime proof.','PET eight scenes22units/Guts intro2/NumberMan3/native NumberMan save/cold continue regression only. No live communications or GutsMan save proved.','Complete Hangul name editing/committed records/redisplay/persistence/old-save compatibility,whole text/images/inline/fixed populations and previous native wait-arrow53pixel difference remain unresolved. Wording/voice human review pending; no release.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Operations31 static / native Guts Jack-In wait30 / PET regression: PASS');return result

if __name__=='__main__':main()
