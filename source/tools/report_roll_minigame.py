"""Keep normal-play and quarantined minigame-renderer evidence separate."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
STEM='exe45_ko_development_roll_minigame_v1'
PREFIX='roll-minigame-v1-'

def main():
    m,rom,expected,streams,checks=static(STEM,'65FF3C');pages=[];seen=set();observed=set()
    root=0x08000000+next(a for a in m['archives'] if a['archive']=='65FF3C')['rom_offset']
    for script in (50,60):
        path=ROOT/'poc/runtime'/f'{PREFIX}diagnostic-v2-{script}';receipt=verify_route(path,m['output_sha256'],seen)
        env=read(path/'mini_alias_environment.json')
        if receipt.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in receipt['artifacts']:raise ValueError('diagnostic checkpoint quarantine')
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['displayed_entry']!=script or env['reads']!=1:raise ValueError('diagnostic alias identity')
        if env['tool_sha256']!=sha((ROOT/'tools/capture_roll_minigame_samples.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()):raise ValueError('diagnostic observer identity')
        require={u for u in streams if int(u.split(':')[1])==script};route_observed=set()
        for step in receipt['capture_steps']:
            cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=root:continue
            state=read(path/(cp+'_roll_pet.json'));alias=read(path/(cp+'_mini_alias.json'))
            if alias['reads']!=1:continue
            for unit in require:
                if not min(streams[unit])<=cursor<=max(streams[unit])+5:continue
                last={d['stream']:d for d in state['draws'] if d['stream'] in streams[unit]}
                if set(last)!=set(streams[unit]):continue
                draws=[last[s] for s in streams[unit]];counts=Counter(expected[d['stream']]['index'] for d in draws);reads={r['index']:r['reads'] for r in state['font_reads']}
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('diagnostic font reads')
                proof=pixels(path,step,draws,expected,rom,m)
                im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
                for d in draws:
                    row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;i=expected[d['stream']]['index'];w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0];rects.append((x,y,x+w,y+12))
                vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('diagnostic stale page pixels')
                pages.append({'route':path.name,'step':step,'unit':unit,'context_script_byte':ram[0xFA21],'alias':alias,'vacant_text_pixels_cleared':len(vacant),**proof,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes())});route_observed.add(unit)
        if not require<=route_observed:raise ValueError(f'diagnostic failure pages absent: {sorted(require-route_observed)}')
        observed|=route_observed
    normal=read(ROOT/'analysis/roll_minigame_v1/runtime.json');normal_observed=set(normal['runtime_observed_units'])
    if normal['rom_sha256']!=m['output_sha256'] or not normal['passed'] or normal_observed&observed:raise ValueError('normal/diagnostic separation')
    selected=[next(p for p in pages if p['unit']==u) for u in sorted(observed)];sheet=Image.new('RGB',(480,160*((len(selected)+1)//2)))
    for i,p in enumerate(selected):sheet.paste(Image.open(ROOT/'poc/runtime'/p['route']/f"step_{p['step']:03}.png"),(i%2*240,i//2*160))
    out=ROOT/'analysis/roll_minigame_v1';sheet.save(out/'diagnostic_minigame_pages.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'normal_runtime_observed_units':sorted(normal_observed),'diagnostic_renderer_observed_units':sorted(observed),'static_only_units':sorted(set(streams)-normal_observed-observed),'pages':pages,'limits':['No minigame was played or completed; record/branch handler executes from native table-offset alias, not a normal outcome. Diagnostic states are quarantined.','Success51/61 and all unlisted pages remain static only; actual gameplay, rewards and recording correctness remain unverified.','Hint23 and fourteen dynamic reward literals remain Japanese; human wording/visual approval and release QA pending.']}
    (out/'minigame_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'minigame_runtime.json');return result

if __name__=='__main__':main()
