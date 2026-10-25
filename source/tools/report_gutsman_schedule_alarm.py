"""Strict alarm renderer evidence, separate from natural alarm reachability."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_roll_pet_license import literal_end
from report_gutsman_pet import main as pet_regression
from run_gutsman_schedule_alarm import STEM,PREFIX,OUTDIR

def alarm_pages(path,script,requested,m,rom,e,streams,pool,exit_step=None,unit_asset='gutsman_schedule_alarm_ko.json',only_keys=None):
    receipt=read(path/'result.json');out=[]
    units={u['id']:u for u in read(ROOT/'translations'/unit_asset)['units']}
    if set(units)!=set(streams):raise ValueError('page asset/stream population mismatch')
    if only_keys is not None and (not only_keys or len(set(only_keys))!=len(only_keys) or not set(only_keys)<=set(streams) or any(int(k.split(':')[1])!=script for k in only_keys)):raise ValueError('invalid explicit page selection')
    for key in [k for k in streams if int(k.split(':')[1])==script and (only_keys is None or k in only_keys)]:
        found=None
        for step in receipt['capture_steps']:
            ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=requested or not min(streams[key])<=cursor<=max(streams[key])+5:continue
            obs=read(path/f'step_{step:03}_roll_pet.json');entry=max((c['frame'] for c in obs['calls']),default=0)
            last={d['stream']:d for d in obs['draws'] if d['stream'] in streams[key] and d['frame']>=entry}
            if set(last)!=set(streams[key]):continue
            draws=[last[s] for s in streams[key]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('return font CPU reads')
            end=literal_end(rom,streams[key],e)
            if cursor!=end or rom[end-0x08000000:end-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('alarm keyWait/clear boundary')
            row=0;advance=0;it=iter(draws)
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;advance=0;continue
                d=next(it)
                if d['offset']!=row*10752+advance*4 or d['context']!=0x0200FA20:raise ValueError('alarm literal geometry')
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
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
    return out

def main():
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2244,55,677),oldstem='exe45_ko_development_gutsman_schedule_v1',outdir=OUTDIR+'/pet_regression',inventory_outdir='full_scope_gutsman_schedule_alarm_v1',added_literal_units=0)
    m,rom,e,s,c=static(STEM,'66651C');pool=0x8000000+next(a for a in m['archives'] if a['archive']=='66651C')['rom_offset'];rt=ROOT/'poc/runtime';q=[]
    for script in [4,6]:
        p=rt/(PREFIX+f'script{script}');r=verify_route(p,m['output_sha256'],set());env=read(p/'alarm_environment.json')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['root_aliases']!=1 or env['entry_aliases']!=1 or env['script']!=script or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is not False or (p/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json'):raise ValueError('quarantine/own parent')
        for file,key in [('capture_gutsman_schedule_alarm.py','tool_sha256'),('capture_roll_pet.py','pet_probe_sha256')]:
            if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('observer drift')
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        for g in env['native_guards']:
            if sha(source[g['start']:g['end']])!=g['sha256'] or source[g['start']:g['end']]!=rom[g['start']:g['end']]:raise ValueError('native guard drift')
        found=alarm_pages(p,script,0,m,rom,e,s,pool)
        for page in found:
            obs=read(p/f"step_{page['step']:03}_roll_pet.json")
            if len(obs['calls'])!=1 or obs['calls'][0]['root']!=pool or obs['calls'][0]['script']!=0 or obs['calls'][0]['lr']!=0x08037F27:raise ValueError('virtual entry caller')
        q.extend(found)
    if {x['unit'] for x in q}!=set(s):raise ValueError('all3 renderer pages')
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,x in enumerate(q):sheet.paste(Image.open(rt/x['route']/f"step_{x['step']:03}.png"),(i*240,0))
    sheet.save(out/'diagnostic_alarm_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=3,selected_text_units=2244,static=c,previous54_payloads_identical=True,pet_regression=baseline,normal_runtime_new_units=[],diagnostic_renderer_pages=q,remaining_catalog=baseline['remaining_catalog'],limits=['PET school4 two pages and additional-event6 only; diagnostic read aliases not native RTC/event reachability. Script6 stops at keyWait before dispatch.','18 other source literals/26 unselected spans including mugshot24/26 and dynamic names remain Japanese. No original source code, event flags, RTC, input or save writes by observer.','Normal NumberMan save/cold continue/3pages,Guts intro2/PET8scenes22units are fresh exact-ROM regressions. Other previous content not rerun.','Whole text/images/inline/fixed population and Hangul name editing/committed records/all redisplays/persistence/old-save compatibility remain open. Prior wait-arrow53pixel issue open; human wording review pending.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts PET alarm3 diagnostic pages and native PET/save regressions PASS');return result
if __name__=='__main__':main()
