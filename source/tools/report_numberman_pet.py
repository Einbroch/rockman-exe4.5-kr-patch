"""Finite NumberMan PET translation and exact-ROM normal-menu runtime QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route

STEM='exe45_ko_development_numberman_pet_v1'
PREFIX='numberman-pet-v1-'

def main():
    m,rom,e,streams,checks=static(STEM,'6873F4')
    if m['translated_units']!=1196 or len(m['archives'])!=23:raise ValueError('selected scope')
    previous=ROOT/'poc/output/exe45_ko_development_numberman_intro_v1.gba';pm=read(previous.with_suffix('.json'));pr=previous.read_bytes()
    if sha(pr)!=pm['output_sha256']:raise ValueError('previous identity')
    for a in pm['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['compiled_sha256']!=n['compiled_sha256'] or pr[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('previous22 payload drift')
    if rom[0x6333A4:0x6334A4]!=pr[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    rt=ROOT/'poc/runtime';chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','prompt-seed','prompts'];seen=set();receipts={}
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen);receipts[name]=r
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
    ar=next(x for x in m['archives'] if x['archive']=='6873F4');pool=0x08000000+ar['rom_offset'];pages=[];observed=set()
    for name in ['intro','prompt-seed','prompts']:
        p=rt/(PREFIX+name)
        for step in receipts[name]['capture_steps']:
            cp=f'step_{step:03}';ram=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes()
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool:continue
            script=ram[0xFA21];keys=[k for k in streams if int(k.split(':')[1])==script]
            if not keys:continue
            obs=read(p/(cp+'_roll_pet.json'));calls=obs['calls']
            if not calls:continue
            entry=max(c['frame'] for c in calls);wanted={s for k in keys for s in streams[k]};last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted and d['frame']>=entry}
            if set(last)!=wanted:continue
            draws=[last[s] for k in keys for s in streams[k]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('actual glyph CPU reads')
            proof=pixels(p,step,draws,e,rom,m,cursor_screen_background=True)
            # The nickname belongs to the preserved native consumer, not this
            # literal stream. Restrict idle clearing to row0; prompt prose to
            # rows0/1, excluding the independently checked option cursor row.
            im=Image.open(p/(cp+'.png')).convert('RGB');occupied=set()
            for d in draws:
                row,off=divmod(d['offset'],10752);x0=92+off//4;y0=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
                occupied.update((x,y) for y in range(y0,y0+12) for x in range(x0,x0+width))
            end=122 if script==1 else 136
            blank={(x,y) for y in range(110,end) for x in range(92,234) if (x,y) not in occupied}
            if {im.getpixel(xy) for xy in blank}!={im.getpixel((231,112))}:raise ValueError('vacant prose region not cleared')
            observed.update(keys);pages.append({'route':p.name,'step':step,'script':script,'units':keys,'vacant_pixels_cleared':len(blank),'screenshot_sha256':sha((p/(cp+'.png')).read_bytes()),**proof})
    expectation={1:(2,108),2:(2,144),3:(1,220),4:(2,108),5:(1,220)}
    for script,base in zip(range(3,9),range(6,30,4)):expectation.update({base:(1,220),base+1:(script,108),base+2:(script,144),base+3:(1,220)})
    behavior=[];p=rt/(PREFIX+'prompts')
    for step,(script,cursor_x) in expectation.items():
        ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();o=(p/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0)
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or b&511!=cursor_x:raise ValueError(f'PET focus/cancel/return transition:{step}:{ram[0xFA21]}:{b&511}')
        if script!=1 and (a&255!=136 or k&1023!=1020 or k>>12!=14):raise ValueError('PET normal option cursor')
        behavior.append({'step':step,'script':script,'cursor_x':cursor_x,'same_relocated_root':True})
    for script in range(1,9):
        if not any(p['script']==script for p in pages):raise ValueError(f'missing complete PET page:{script}')
    enter=rt/(PREFIX+'save-enter');commit=rt/(PREFIX+'save-commit')
    for path,parent in [(enter,'intro'),(commit,'save-enter')]:
        r=verify_route(path,m['output_sha256'],seen)
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json'):raise ValueError('save path ancestry')
    savear=next(x for x in m['archives'] if x['archive']=='6DA21C');savepool=0x08000000+savear['rom_offset']
    q=(enter/'step_010_gbaExtWorkRam.bin').read_bytes();after=(enter/'step_011_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',q,0xFA50)[0]!=pool or q[0xFA21]!=8 or struct.unpack_from('<I',after,0xFA50)[0]!=savepool or after[0xFA21]!=55:raise ValueError('accepted save-screen navigation')
    env=read(commit/'save_environment.json');sav=STEM+'.sav';rtc=STEM+'.rtc';before=env['files_before'][sav];after=env['files_after'][sav]
    if not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or before!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or after['bytes']!=65536 or before==after or sha((commit/'persistent_files_after'/sav).read_bytes())!=after['sha256']:raise ValueError('native disk save')
    for name in set(env['files_before'])|set(env['files_after']):
        if name not in(sav,rtc) and env['files_before'].get(name)!=env['files_after'].get(name):raise ValueError('unrelated save changed')
    ram=(commit/'step_013_gbaExtWorkRam.bin').read_bytes()
    if ram[0xFA21]!=58 or struct.unpack_from('<I',ram,0xFA50)[0]!=savepool:raise ValueError('native success58')
    out=ROOT/'analysis/numberman_pet_v1';out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(960,320))
    for i,script in enumerate(range(1,9)):
        page=next(p for p in pages if p['script']==script);sheet.paste(Image.open(rt/page['route']/f"step_{page['step']:03}.png"),(i%4*240,i//4*160))
    sheet.save(out/'pet_prompts.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':44,'selected_text_units':1196,'static':checks,'previous22_payloads_identical':True,'pages':pages,'choice_behavior':behavior,'runtime_observed_units':sorted(observed),'runtime_open_units':sorted(set(streams)-observed),'limits':['Duplicate reentry/save-now and interruption remain runtime-open unless listed; source controls and finite font/layout validated for all44 units.','No live communication, Hangul name input, persistence reload/old-save compatibility, RTC/audio/hardware/full-game/human release approval.']}
    result.update(accepted_save_screen_navigation=True,native_save_before=before,native_save_after=after,native_save_success_script=58,tool_sha256=sha((ROOT/'tools/report_numberman_pet.py').read_bytes()))
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan PET static/pages/focus/cancel/clearing: PASS');return result

if __name__=='__main__':main()
