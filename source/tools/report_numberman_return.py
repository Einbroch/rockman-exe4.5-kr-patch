"""Five quarantined return pages and seven normal introduction regressions."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from archive_scripts import script_spans

STEM='exe45_ko_development_numberman_return_v1'
PREFIX='numberman-return-v1-'

def pages(path,script,requested,m,rom,e,streams,pool,exit_step=None):
    receipt=read(path/'result.json');out=[]
    for key in [k for k in streams if int(k.split(':')[1])==script]:
        found=None
        for step in receipt['capture_steps']:
            ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=requested or not min(streams[key])<=cursor<=max(streams[key])+5:continue
            obs=read(path/f'step_{step:03}_roll_pet.json');entry=max((c['frame'] for c in obs['calls']),default=0)
            last={d['stream']:d for d in obs['draws'] if d['stream'] in streams[key] and d['frame']>=entry}
            if set(last)!=set(streams[key]):continue
            draws=[last[s] for s in streams[key]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('return font CPU reads')
            proof=pixels(path,step,draws,e,rom,m)
            im=Image.open(path/f'step_{step:03}.png').convert('RGB');occupied=set()
            for d in draws:
                row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
                occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
            a,b,k=struct.unpack_from('<HHH',(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes(),0);arrow=set()
            if k&1023==1016 and k>>12==14:
                if (a,b)!=(141,16609):raise ValueError('return unknown native arrow')
                arrow={(x,y) for y in range(141,157) for x in range(225,240)}
            if occupied&arrow:raise ValueError('glyph footprint reaches native arrow')
            baseline=Image.open(ROOT/'poc/runtime/numberman-intro-v1-select-numberman-full/step_008.png').convert('RGB')
            frame={(x,y) for y in range(110,140) for x in [234,235]}
            if any(im.getpixel(xy)!=baseline.getpixel(xy) for xy in frame):raise ValueError('native right box border changed')
            blank={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied|arrow}
            bad=[(xy,im.getpixel(xy)) for xy in sorted(blank) if im.getpixel(xy)!=im.getpixel((231,112))]
            if bad:raise ValueError(f'return vacant page clearing:{path.name}/{step}/{key}/{bad[:6]}')
            found=dict(unit=key,step=step,route=path.name,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/f'step_{step:03}.png').read_bytes()),**proof);break
        if found is None:raise ValueError('unobserved complete page '+key)
        out.append(found)
    if any(b['step']<=a['step'] for a,b in zip(out,out[1:])):raise ValueError('ordered pages')
    end=out[-1]['step'];exit_step=end+1 if exit_step is None else exit_step
    if exit_step not in receipt['capture_steps'] or exit_step<=end:raise ValueError('recorded exit snapshot required')
    before=read(path/f'step_{end:03}_roll_pet.json');after=read(path/f'step_{exit_step:03}_roll_pet.json');ram=(path/f'step_{exit_step:03}_gbaExtWorkRam.bin').read_bytes()
    if before['calls']!=after['calls'] or before['draws']!=after['draws'] or struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('entry exit lifetime')
    return out

def main():
    m,rom,e,s,checks=static(STEM,'6872B8');rt=ROOT/'poc/runtime';seen=set()
    verify_route(rt/'numberman-intro-v1-select-numberman-full',read(ROOT/'poc/output/exe45_ko_development_numberman_intro_v1.json')['output_sha256'],set())
    if m['translated_units']!=1283 or len(m['archives'])!=26 or len(s)!=12:raise ValueError('return denominator')
    old=ROOT/'poc/output/exe45_ko_development_numberman_drill_options_v3.gba';om=read(old.with_suffix('.json'));previous=old.read_bytes()
    if sha(previous)!=om['output_sha256']:raise ValueError('old identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['archive']=='6872B8':continue
        if a['compiled_sha256']!=n['compiled_sha256'] or previous[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('retained25 payload drift')
    ar=next(x for x in m['archives'] if x['archive']=='6872B8');oa=next(x for x in om['archives'] if x['archive']=='6872B8');pool=0x08000000+ar['rom_offset']
    if script_spans(previous[oa['rom_offset']:oa['rom_offset']+oa['compiled_bytes']],4)[1]!=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],4)[1]:raise ValueError('seven first-meeting bytes drift')
    if rom[0x6333A4:0x6334A4]!=previous[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    chain=['cold-part1','date','profile','navi-menu','select-numberman','intro']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
    parent=rt/(PREFIX+'navi-menu');ram=(parent/'final_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('parent must precede introduction load')
    for name in ['normal-full','diagnostic-return']:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen)
        if r['state_origin']!=str(parent/'result.json'):raise ValueError('fresh parent mismatch')
    p=rt/(PREFIX+'diagnostic-return');r=read(p/'result.json');env=read(p/'return_environment.json')
    if not env['passed'] or env['read_aliases']!=1 or env['requested_script']!=1 or env['target_script']!=2 or env['rom_sha256']!=m['output_sha256'] or env['tool_sha256']!=sha((ROOT/'tools/capture_numberman_return.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()) or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('return alias identity/quarantine')
    normal=pages(rt/(PREFIX+'normal-full'),1,1,m,rom,e,s,pool);diagnostic=pages(p,2,1,m,rom,e,s,pool)
    if len(normal)!=7 or len(diagnostic)!=5:raise ValueError('all12 complete pages')
    # Native save/continue route was tried separately. It reached a seasonal
    # greeting, not a verified script2 page. Preserve that negative scope.
    for name,parent_name in [('save-enter','intro'),('save-commit','save-enter')]:
        sr=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if sr['state_origin']!=str(rt/(PREFIX+parent_name)/'result.json'):raise ValueError('native save parent')
    commit=rt/(PREFIX+'save-commit');ce=read(commit/'save_environment.json');sav=STEM+'.sav';rtc=STEM+'.rtc';before=ce['files_before'][sav];saved=ce['files_after'][sav]
    if not ce['observer_only'] or before!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or saved['bytes']!=65536 or before==saved or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256']:raise ValueError('native disk save')
    sr=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x08000000+next(a for a in m['archives'] if a['archive']=='6DA21C')['rom_offset']
    if sr[0xFA21]!=58 or struct.unpack_from('<I',sr,0xFA50)[0]!=savepool:raise ValueError('save success58')
    reload_names=['normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return']
    for i,name in enumerate(reload_names):
        rp=rt/(PREFIX+name);rr=verify_route(rp,m['output_sha256'],seen);env=read(rp/'reload_environment.json')
        if rr['state_origin']!=(None if not i else str(rt/(PREFIX+reload_names[i-1])/'result.json')):raise ValueError('cold native reload ancestry')
        if not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['tool_sha256']!=sha((ROOT/'tools/capture_numberman_return_reload.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()) or env['save_directory']!=ce['save_directory'] or env['files_before'][sav]!=saved or env['files_after'][sav]!=saved:raise ValueError('native saved-file reload identity')
        for fn in set(env['files_before'])|set(env['files_after']):
            if fn not in (sav,rtc) and env['files_before'].get(fn)!=env['files_after'].get(fn):raise ValueError('unrelated test save changed')
    native_reload=dict(cold_boot_without_checkpoint=True,native_save_before=before,native_save_after=saved,save_success_script=58,all_reload_segments_preserved_save=True,return_script2_verified=False,observed='Navi reselection followed seasonal New Year greeting68BBB4/script1 then PET; no complete target2 page observed. This is not an unreachable-code claim.')
    dest=ROOT/'analysis/numberman_return_v1';dest.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,480))
    for i,q in enumerate(diagnostic):sheet.paste(Image.open(p/f"step_{q['step']:03}.png"),(i%2*240,i//2*160))
    sheet.save(dest/'return_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_units=5,selected_text_units=1283,static=checks,retained25_payloads_identical=True,retained7_intro_bytes_identical=True,normal_intro_pages=normal,diagnostic_return_pages=diagnostic,normal_play_new_units=[],limits=['Return5 renderer-only; normal Navi reselection caller/flag prerequisites unverified.','Native wait-arrow graphics excluded from blank text; prior53screen-pixel differences unresolved, not graphic QA passed.','Hangul name input/committed records/redisplay/persistence/old saves; full-game/RTC/audio/hardware/release incomplete.','4649 adaptation approved by user only for this greeting; other wording/presentation approval pending.'])
    result['native_reload_attempt']=native_reload
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Return5 diagnostics / intro7 normal regression: PASS')
    return result

if __name__=='__main__':main()
