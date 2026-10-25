"""Full42-literal static scope plus own-normal and quarantined options proof."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from archive_scripts import script_spans
from report_numberman_drill_intro import page as normal_page

STEM='exe45_ko_development_numberman_drill_options_v3'
PREFIX='numberman-drill-options-v3-'

def page(path,step,keys,origin,m,rom,e,streams,pool):
    ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0];wanted={s for k in keys for s in streams[k]}
    # Diagnostic native init stored requested0 before the offset alias. It
    # does not relabel0 as13/15; exact target stream and alias prove scope.
    if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=0 or not min(wanted)<=cursor<=max(wanted)+20:raise ValueError('options diagnostic context/current stream')
    # Fresh probe starts with the parent on687910, before715064 init. The
    # guarded native4FB76 read alias is positive entry evidence even when
    # the unrelated external4F7B6 observer recorded no call. No prior-job
    # draw arrays are imported; only this entry's target stream is counted.
    obs=read(path/f'step_{step:03}_roll_pet.json');entry=max((c['frame'] for c in obs['calls']),default=0);last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted and d['frame']>=entry}
    if set(last)!=wanted:raise ValueError('options full current glyphs')
    draws=[last[s] for k in keys for s in streams[k]];counts=Counter(e[d['stream']]['index'] for d in draws);reads={r['index']:r['reads'] for r in obs['font_reads']}
    if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('options full font CPU reads')
    proof=pixels(path,step,draws,e,rom,m,origin=origin,cursor_screen_background=True);im=Image.open(path/f'step_{step:03}.png').convert('RGB');occupied=set()
    for d in draws:
        row,off=divmod(d['offset'],10752);x=origin[0]+off//4;y=origin[1]+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[d['stream']]['index']*4)[0]
        occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
    a,b,k=struct.unpack_from('<HHH',(path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes(),0);focus=None;cr=set()
    arrow=None
    if k&1023==1016 and k>>12==14:
        native={'level':((32,110),(205,134)),'exam':((52,110),(225,141))}
        kind='level' if keys[0].startswith('715064:13:') else 'exam'
        source=ROOT/('poc/runtime/numberman-drill-options-source-v1-'+kind)
        source_oam=struct.unpack_from('<HHH',(source/'step_001_gbaSpriteRam.bin').read_bytes(),0)
        if origin!=native[kind][0] or (a,b,k)!=source_oam or (b&511,a&255)!=native[kind][1]:raise ValueError('unknown wait arrow placement')
        v=(path/f'step_{step:03}_gbaVideoRam.bin').read_bytes();pal=(path/f'step_{step:03}_gbaPaletteRam.bin').read_bytes()
        # Source-exam pages show two native wait-arrow tile phases. Match
        # exact OAM, tile bytes and palette to an observed source phase;
        # do not accept unknown graphics or infer screen identity from RAM.
        phase=None
        for sn in ([1] if kind=='level' else [1,2,3]):
            sv=(source/f'step_{sn:03}_gbaVideoRam.bin').read_bytes();sp=(source/f'step_{sn:03}_gbaPaletteRam.bin').read_bytes()
            so=struct.unpack_from('<HHH',(source/f'step_{sn:03}_gbaSpriteRam.bin').read_bytes(),0)
            if (a,b,k)==so and v[0x17F00:0x18000]==sv[0x17F00:0x18000] and pal[0x3C0:0x3E0]==sp[0x3C0:0x3E0]:
                phase=sn;break
        if phase is None:raise ValueError('native wait arrow asset changed')
        ax,ay=native[kind][1]
        cr={(x,y) for y in range(ay,min(160,ay+16)) for x in range(ax,min(240,ax+16))}
        if occupied&cr:raise ValueError('translated glyph footprint reaches native wait arrow')
        si=Image.open(source/f'step_{phase:03}.png').convert('RGB');difference=sum(si.getpixel(xy)!=im.getpixel(xy) for xy in cr)
        arrow={'oam_vram_palette_identical_to_source':True,'source_phase_step':phase,'source_comparison_screen_difference_pixels':difference,'scope':'native control graphic excluded from vacant-text region; any screenshot difference not diagnosed or waived'}
    if k&1023==1020 and k>>12==14:
        focus=[b&511,a&255];cr={(x,y) for y in range(a&255,(a&255)+16) for x in range(b&511,(b&511)+16)}
    vacant={(x,y) for y in range(110,150) for x in range(origin[0],228) if (x,y) not in occupied|cr}
    if {im.getpixel(xy) for xy in vacant}!={im.getpixel((225,112))}:raise ValueError('options vacant page clearing')
    return {'route':path.name,'step':step,'units':keys,'focus_xy':focus,'native_wait_arrow':arrow,'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/f'step_{step:03}.png').read_bytes()),**proof}

def main():
    m,rom,e,streams,checks=static(STEM,'715064');rt=ROOT/'poc/runtime';seen=set()
    if m['translated_units']!=1278 or len(m['archives'])!=26 or len(streams)!=42:raise ValueError('options denominator')
    old=ROOT/'poc/output/exe45_ko_development_numberman_training_rewards_v2.gba';om=read(old.with_suffix('.json'));previous=old.read_bytes()
    if sha(previous)!=om['output_sha256']:raise ValueError('prior ROM identity')
    for a in om['archives']:
        n=next(x for x in m['archives'] if x['archive']==a['archive'])
        if a['archive']=='715064':continue
        if a['compiled_sha256']!=n['compiled_sha256'] or previous[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[n['rom_offset']:n['rom_offset']+n['compiled_bytes']]:raise ValueError('prior25 payload drift')
    ar=next(x for x in m['archives'] if x['archive']=='715064');oa=next(x for x in om['archives'] if x['archive']=='715064');pool=0x08000000+ar['rom_offset']
    before=script_spans(previous[oa['rom_offset']:oa['rom_offset']+oa['compiled_bytes']],16);after=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],16)
    if any(before[i]!=after[i] for i in list(range(13))+[14]):raise ValueError('retained32 units drift')
    if rom[0x6333A4:0x6334A4]!=previous[0x6333A4:0x6334A4]:raise ValueError('save title drift')
    if any(struct.unpack_from('<I',rom,p)[0]!=pool for p in [0xDD394,0xDD894]):raise ValueError('both drill roots')
    chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','pre','normal']
    for i,name in enumerate(chain):
        r=verify_route(rt/(PREFIX+name),m['output_sha256'],seen)
        if (not i and r['state_origin'] is not None) or (i and r['state_origin']!=str(rt/(PREFIX+chain[i-1])/'result.json')):raise ValueError('own cold ancestry')
    normal=rt/(PREFIX+'normal');regression=[normal_page(normal,s,[f'715064:0:{i}'],m,rom,e,streams,pool) for i,s in enumerate([1,2,3])]
    parent=(rt/(PREFIX+'pre')/'step_010_gbaExtWorkRam.bin').read_bytes()
    training_pool=0x08000000+next(x for x in m['archives'] if x['archive']=='687910')['rom_offset']
    if struct.unpack_from('<I',parent,0xFA50)[0]!=training_pool or parent[0xFA21]!=20:raise ValueError('diagnostic parent must precede drill init')
    regression.extend(normal_page(normal,s,['715064:0:3','715064:0:4'],m,rom,e,streams,pool) for s in [4,6,8])
    pages=[]
    verify_route(rt/'numberman-drill-options-source-v1-level',om['output_sha256'],set())
    verify_route(rt/'numberman-drill-options-source-v1-exam',om['output_sha256'],set())
    for name,script in [('level',13),('exam',15)]:
        path=rt/(PREFIX+'diagnostic-'+name);r=verify_route(path,m['output_sha256'],seen);env=read(path/'options_environment.json')
        if not env['passed'] or env['target_script']!=script or env['read_aliases']!=1 or env['rom_sha256']!=m['output_sha256'] or r['state_origin']!=str(rt/(PREFIX+'pre')/'result.json'):raise ValueError('options alias identity/parent')
        if env['tool_sha256']!=sha((ROOT/'tools/capture_numberman_drill_options.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_numberman_drill.py').read_bytes()):raise ValueError('options observer identity')
        if r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('options quarantine')
        if script==13:
            pages.append(page(path,1,['715064:13:0'],(32,110),m,rom,e,streams,pool))
            choices=[page(path,s,[f'715064:13:{i}' for i in range(1,5)],(32,110),m,rom,e,streams,pool) for s in [2,3,5,7,9]]
            # Space(1) consumes8px; cursor anchored13px left of label.
            width=next(x['line_advance_pixels'][0] for x in ar['layout'] if x['id']=='715064:13:1')
            # The animated cursor shifts horizontally over a three-pixel
            # interval; validate column anchor, not one animation phase.
            expected=[[27,108],[35+width,108],[35+width,122],[27,122],[27,108]]
        else:
            pages.extend(page(path,s,[f'715064:15:{i}'],(52,110),m,rom,e,streams,pool) for i,s in enumerate([1,2,3]))
            choices=[page(path,s,['715064:15:3','715064:15:4'],(52,110),m,rom,e,streams,pool) for s in [4,6,8]]
            expected=[[58,108],[58,122],[58,108]]
        if any(p['focus_xy'][1]!=xy[1] or not xy[0]-3<=p['focus_xy'][0]<=xy[0] for p,xy in zip(choices,expected)):raise ValueError('options focus graph')
        pages.extend(choices)
    observed={k for p in pages for k in p['units']};added=set(streams)-{u['id'] for u in read(ROOT/'translations/numberman_drill_bubbles_ko.json')['units']}
    if observed!=added or len(added)!=10:raise ValueError('all10 options diagnostic coverage')
    dest=ROOT/'analysis/numberman_drill_options_v3';dest.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,640))
    for i,p in enumerate(pages):sheet.paste(Image.open(rt/p['route']/f"step_{p['step']:03}.png"),(i%3*240,i//3*160))
    sheet.save(dest/'diagnostic_options_pages.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'added_units':10,'selected_text_units':1278,'static':checks,'retained25_payloads_identical':True,'retained32_unit_script_bytes_identical':True,'pages':pages,'normal_intro_regression':regression,'diagnostic_renderer_units':sorted(observed),'normal_play_new_units':[],'limits':['All10 new units are renderer-only diagnostics; actual flags5505/5506 acquisition, level invocation and selection gameplay effect unverified.','Active requested script label0 retained by init-table alias; exact stream and font/pixels prove only target renderer. Diagnostic states quarantined.','Existing timed bubble5 open paths/effect legibility and unvisited results remain unresolved; no imported full runtime claim.','Hangul name input/committed record/all redisplay/persistence/old saves, human wording approval, full-game/RTC/audio/hardware/release incomplete.']}
    result['limits'].append('Level/exam native wait-arrow raw OAM/VRAM/palette identity preserved, but source/candidate screenshot differences remain undiagnosed; graphic regions are not credited as blank text or as pixel-identical. Source-exam placement225,141 extends past screen edge and is preserved, not redesigned.')
    (dest/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('NumberMan options renderer and ordinary regression: PASS');return result

if __name__=='__main__':main()
