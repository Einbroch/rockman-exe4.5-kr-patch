"""Normal confirmation page, exact choice geometry, and Yes/No/B behavior."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_calendar_prompts import main as questions
from run_gutsman_calendar_confirmation import STEM,PREFIX,OUTDIR
ASSET='gutsman_calendar_confirmation_ko.json'
def checked_route(name,parent,m,pool):
    p=ROOT/'poc/runtime'/(PREFIX+name);r=verify_route(p,m['output_sha256'],set());env=read(p/'calendar_prompts_environment.json')
    if r['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+parent)/'result.json') or r.get('normal_play_checkpoint_eligible') is False or not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['pool']!=pool:raise ValueError('confirmation normal ancestry')
    for f,k in [('capture_gutsman_calendar_prompts.py','self_sha256'),('capture_roll_pet.py','pet_probe_sha256'),('capture_fixedcell_probe.py','fixed_probe_sha256')]:
        if sha((ROOT/'tools'/f).read_bytes())!=env[k]:raise ValueError('confirmation observer drift')
    if any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('confirmation intervention')
    return p,r
def main(home=False,register=False,anniversary=False,anniversary_confirmation=False):
    baseline=questions(stem=STEM,prefix=PREFIX,outdir=OUTDIR,confirmation=not home and not register and not anniversary,home=home and not register and not anniversary,register=register and not anniversary,anniversary=anniversary,anniversary_confirmation=anniversary_confirmation)
    asset='gutsman_calendar_anniversary_confirmation_ko.json' if anniversary_confirmation else 'gutsman_calendar_anniversary_ko.json' if anniversary else 'gutsman_calendar_register_ko.json' if register else 'gutsman_calendar_home_ko.json' if home else ASSET
    m,rom,e,streams,checks=static(STEM,'665698');pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='665698');units={u['id']:u for u in read(ROOT/'translations'/asset)['units']};p,_=checked_route('confirmation','time-stable',m,pool);step=5;cp=f'step_{step:03}'
    ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));keys=[f'665698:24:{i}' for i in range(3)];selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
    if ram[0xFA21]!=24 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or set(last)!=set(selected):raise ValueError('confirmation script/full literals')
    draws=[last[s] for s in selected]
    for key in keys:
        offsets=[last[s]['offset'] for s in streams[key]];row,start=divmod(offsets[0],10752);advance=start//4;cursor=iter(streams[key])
        for ch in units[key]['translation']:
            if ch=='\n':row+=1;advance=0;continue
            s=next(cursor)
            if last[s]['context']!=0x0200FA20 or last[s]['offset']!=row*10752+advance*4:raise ValueError('confirmation exact geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
    counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('confirmation CPU font supply')
    proof=pixels(p,step,draws,e,rom,m,origin=(52,110),cursor_screen_background=True,cursor_indices=(2,))
    source=ROOT/'poc/runtime/gutsman-calendar-confirmation-baseline-v1-meal';sr=verify_route(source,'e8ab0e4a8381d904d92e155a6852369c70532449f6fd74386831607fd4f0e4d7',set());senv=read(source/'calendar_prompts_environment.json')
    if sr['state_origin']!=str(ROOT/'poc/runtime/gutsman-calendar-content-v1-time/result.json') or sr.get('normal_play_checkpoint_eligible') is False or not senv['observer_only'] or senv['pool']!=0x08807E1C:raise ValueError('source confirmation reference')
    current_o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();source_o=(source/'step_005_gbaSpriteRam.bin').read_bytes();cur=struct.unpack_from('<HHH',current_o,16);old=struct.unpack_from('<HHH',source_o,16)
    if cur!=old or (cur[0]&255,cur[1]&511,cur[2]&1023,cur[2]>>12)!=(136,85,1020,14):raise ValueError('default Yes cursor geometry')
    phases=ROOT/'poc/runtime/gutsman-calendar-confirmation-baseline-v1-phases';pr=verify_route(phases,'e8ab0e4a8381d904d92e155a6852369c70532449f6fd74386831607fd4f0e4d7',set());penv=read(phases/'calendar_prompts_environment.json');boxes=[(5,107,50,151),(1,104,238,107),(1,151,238,155)];im=Image.open(p/(cp+'.png')).convert('RGB');matches=[]
    if pr['state_origin']!=str(source/'result.json') or pr.get('normal_play_checkpoint_eligible') is False or not penv['observer_only'] or len(pr['capture_steps'])!=90:raise ValueError('confirmation phase population')
    for s in pr['capture_steps']:
        name=f'step_{s:03}';rr=(phases/(name+'_gbaExtWorkRam.bin')).read_bytes();ref=Image.open(phases/(name+'.png')).convert('RGB')
        if rr[0xFA21]!=24 or struct.unpack_from('<I',rr,0xFA50)[0]!=penv['pool']:raise ValueError('confirmation phase script/root')
        if all(im.crop(b).tobytes()==ref.crop(b).tobytes() for b in boxes):matches.append(phases/(name+'.png'))
    if not matches:raise ValueError('no exact native confirmation portrait/border phase')
    bg=im.getpixel((233,110));rects=[]
    for d in draws:
        row,off=divmod(d['offset'],10752);x=52+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
    rects.append((85,136,101,152));vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
    if any(im.getpixel(xy)!=bg for xy in vacant):raise ValueError('confirmation stale pixels')
    no,_=checked_route('no-focus','confirmation',m,pool);nram=(no/'step_002_gbaExtWorkRam.bin').read_bytes();no_o=(no/'step_002_gbaSpriteRam.bin').read_bytes();ncur=struct.unpack_from('<HHH',no_o,16)
    if nram[0xFA21]!=24 or struct.unpack_from('<I',nram,0xFA50)[0]!=pool or (ncur[0]&255,ncur[1]&511,ncur[2]&1023,ncur[2]>>12)!=(136,121,1020,14):raise ValueError('No focus cursor geometry')
    pre=ram[0x1310:0x1330];branches={}
    for name,parent in [('no-accept','no-focus'),('b-cancel','confirmation'),('yes-accept','confirmation')]:
        q,_=checked_route(name,parent,m,pool);qram=(q/'step_002_gbaExtWorkRam.bin').read_bytes();branches[name]={'script':qram[0xFA21],'record':qram[0x1310:0x1330].hex(),'screenshot_sha256':sha((q/'step_002.png').read_bytes())}
        if struct.unpack_from('<I',qram,0xFA50)[0]!=pool:raise ValueError('confirmation result root')
    if any(branches[x]['script']!=22 or bytes.fromhex(branches[x]['record'])!=pre for x in ['no-accept','b-cancel']):raise ValueError('No/B must return without commit')
    expected=bytes.fromhex('03000001010602000002f9fcdd16f9fcac14e500000000000000000000000000')
    if branches['yes-accept']['script']!=0 or bytes.fromhex(branches['yes-accept']['record'])!=expected:raise ValueError('default Yes commit record')
    page=dict(route=p.name,step=step,units=keys,vacant_pixels_cleared=len(vacant),screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),reference_screenshot=str(matches[0].relative_to(ROOT)),reference_screenshot_sha256=sha(matches[0].read_bytes()),default_yes_cursor_xy=[85,136],no_cursor_xy=[121,136],choice_row_advance_pixels=104,**proof)
    out=ROOT/'analysis'/OUTDIR;sheet=Image.new('RGB',(720,320));shots=[(p,5),(no,2),(ROOT/'poc/runtime'/(PREFIX+'no-accept'),2),(ROOT/'poc/runtime'/(PREFIX+'b-cancel'),2),(ROOT/'poc/runtime'/(PREFIX+'yes-accept'),2)]
    for i,(q,s) in enumerate(shots):sheet.paste(Image.open(q/f'step_{s:03}.png'),(i%3*240,i//3*160))
    sheet.save(out/'confirmation_choices.png');baseline.update(confirmation_page=page,choice_behavior=branches,normal_meal_record_committed=True,no_and_b_leave_record_unchanged=True,limits=baseline['limits']+['Confirmation24/meal preset/default Yes commit and alternate No/B return only. Other content/name types, persistent save/reload and RTC dispatch remain unverified.'])
    (out/'runtime.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf8');print('GutsMan confirmation page + Yes/No/B normal branches: PASS');return baseline
if __name__=='__main__':main()
