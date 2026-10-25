"""Results prose: exact-ROM failure route and protected native nickname prefix."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from report_numberman_training_intro import page as invitation_page
from archive_scripts import script_spans

STEM='exe45_ko_development_numberman_training_rewards_v2'
PREFIX='numberman-training-rewards-v1-'
SOURCE_STEM='exe45_ko_development_numberman_drill_bubbles_v1'

def page(path,step,key,m,rom,e,streams,pool,nickname_source=None):
    r=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();script=int(key.split(':')[1]);cursor=struct.unpack_from('<I',r,0xFA4C)[0];wanted=set(streams[key])
    if struct.unpack_from('<I',r,0xFA50)[0]!=pool or r[0xFA21]!=script or not min(wanted)<=cursor<=max(wanted)+16:raise ValueError('results active root/script/cursor')
    obs=read(path/f'step_{step:03}_roll_pet.json');entry=max((c['frame'] for c in obs['calls']),default=0)
    last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted and d['frame']>=entry}
    if set(last)!=wanted:raise ValueError('results complete current glyph stream')
    draws=[last[s] for s in streams[key]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('results font CPU reads')
    proof=pixels(path,step,draws,e,rom,m);occupied=set();im=Image.open(path/f'step_{step:03}.png').convert('RGB');prefix_proof=None
    for d in draws:
        row,off=divmod(d['offset'],10752);x=92+off//4;y=110+14*row;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
        occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
    if nickname_source:
        comma=draws[0]
        if e[comma['stream']]['ch']!='、' or comma['offset']>=10752 or comma['offset']%4:raise ValueError('nickname first-line comma anchor')
        end=92+comma['offset']//4
        if not 92<end<=214:raise ValueError('nickname observed prefix extent')
        native=Image.open(nickname_source/'step_001.png').convert('RGB');area={(x,y) for y in range(110,122) for x in range(92,end)}
        if any(im.getpixel(xy)!=native.getpixel(xy) for xy in area):raise ValueError('native nickname prefix differs from observed source scene')
        occupied|=area;prefix_proof={'observed_prefix_pixels_identical_to_source':len(area),'first_comma_x':end,'scope':'this observed native Japanese nickname only; not Hangul-name input or all user names'}
    blank={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied and not(x>=220 and y>=140)}
    if {im.getpixel(xy) for xy in blank}!={im.getpixel((231,112))}:raise ValueError('results vacant page clearing')
    return {'route':path.name,'step':step,'units':[key],'screenshot_sha256':sha((path/f'step_{step:03}.png').read_bytes()),'vacant_pixels_cleared':len(blank),'native_nickname_prefix':prefix_proof,**proof}

def main():
    m,rom,e,streams,checks=static(STEM,'687910');rt=ROOT/'poc/runtime';seen=set()
    if m['translated_units']!=1268 or len(m['archives'])!=26:raise ValueError('results denominator')
    old=ROOT/f'poc/output/{SOURCE_STEM}.gba';om=read(old.with_suffix('.json'));oldrom=old.read_bytes()
    if sha(oldrom)!=om['output_sha256']:raise ValueError('prior identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['archive']=='687910':continue
        if a['compiled_sha256']!=n['compiled_sha256'] or oldrom[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('prior25 archive drift')
    if rom[0x6333A4:0x6334A4]!=oldrom[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    ar=next(a for a in m['archives'] if a['archive']=='687910');oa=next(a for a in om['archives'] if a['archive']=='687910');pool=0x08000000+ar['rom_offset']
    if struct.unpack_from('<I',rom,0x38284)[0]!=pool:raise ValueError('results root')
    before=script_spans(oldrom[oa['rom_offset']:oa['rom_offset']+oa['compiled_bytes']],65);after=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],65)
    if any(before[i]!=after[i] for i in [10,11,20,21]):raise ValueError('retained invitation bytes')
    chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','drill','game','results']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
    source=rt/'numberman-training-results-source-v1';sr=verify_route(source,om['output_sha256'],set())
    if (source/'step_001_roll_pet.json').exists():
        ram=(source/'step_001_gbaExtWorkRam.bin').read_bytes()
        if ram[0xFA21]!=13:raise ValueError('source poor-result script')
    results=rt/(PREFIX+'results');pages=[page(results,1,'687910:13:0',m,rom,e,streams,pool,source),page(results,2,'687910:13:1',m,rom,e,streams,pool)]
    regression=[invitation_page(rt/(PREFIX+'drill'),step,[f'687910:20:{i}'],m,rom,e,streams,pool) for i,step in enumerate([5,6,7,8,9])]
    regression.append(invitation_page(rt/(PREFIX+'drill'),10,['687910:20:5','687910:20:6'],m,rom,e,streams,pool))
    ram=(results/'step_003_gbaExtWorkRam.bin').read_bytes();petpool=0x08000000+next(a for a in m['archives'] if a['archive']=='6873F4')['rom_offset']
    if struct.unpack_from('<I',ram,0xFA50)[0]!=petpool or ram[0xFA21]!=1:raise ValueError('normal result return PET')
    obs=read(results/'step_001_roll_pet.json')
    if not any(c['root']==pool and c['script']==12 for c in obs['calls']):raise ValueError('native result dispatcher12')
    added=set(streams)-{u['id'] for u in read(ROOT/'translations/numberman_training_intro_ko.json')['units']};observed={k for p in pages for k in p['units']}
    dest=ROOT/'analysis/numberman_training_rewards_v1';dest.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,step in enumerate([1,2,3]):sheet.paste(Image.open(results/f'step_{step:03}.png'),(240*i,0))
    sheet.save(dest/'results_pages.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':23,'selected_text_units':1268,'static':checks,'retained25_payloads_identical':True,'retained_invitation_scripts_identical':True,'pages':pages,'current_invitation_regression':regression,'runtime_observed_new_units':sorted(observed),'runtime_open_new_units':sorted(added-observed),'native_dispatcher12_to_poor13_then_pet':True,'limits':['Positive/reward/record-result prose15 and six readouts not normal-play verified; no success/reward quantity or inventory proof.','Six dynamic readout units are translated; separate diagnostic-renderer proof required.','Existing drill small-bubble five open paths/explosion legibility still unresolved; no new claim.','Only observed native nickname prefix compared; Hangul name input/committed record/redisplay and persistence/old saves unresolved.','No full game/RTC/audio/hardware/human wording approval/release.']}
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan result failure/pages/PET: PASS');return result

if __name__=='__main__':main()
