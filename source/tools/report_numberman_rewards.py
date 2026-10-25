"""Bonus pages including native decimal RAM stream -> OBJ -> screen."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from numberman_reward_model import model
STEM='exe45_ko_development_numberman_training_rewards_v2'
PREFIX='numberman-training-rewards-v1-'

def main(stem=STEM,route_prefix=PREFIX,outdir='numberman_training_rewards_v1'):
    m,rom,expected,streams,checks=static(stem,'687910');source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();proof=model(source)
    ar=next(a for a in m['archives'] if a['archive']=='687910');pool=0x08000000+ar['rom_offset'];pages=[];observed=set();seen=set()
    for script in (16,18,52,53):
        path=ROOT/'poc/runtime'/f'{route_prefix}diagnostic-r2-{script}';receipt=verify_route(path,m['output_sha256'],seen);env=read(path/'reward_environment.json')
        amount=max(proof['zenny_values'] if script in (16,52) else proof['bugfrag_values']);keys={u for u in streams if int(u.split(':')[1])==script}
        if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['script']!=script or env['amount']!=amount:raise ValueError('bonus alias identity')
        if env['tool_sha256']!=sha((ROOT/'tools/capture_numberman_reward_samples.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()):raise ValueError('bonus observer identity')
        if receipt.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in receipt['artifacts']:raise ValueError('bonus state quarantine')
        groups=([[f'687910:{script}:0']] if script==16 else [[f'687910:18:0',f'687910:18:1']] if script==18 else [[f'687910:{script}:0'],[f'687910:{script}:1'],[f'687910:{script}:2']+([f'687910:{script}:3'] if script==53 else [])]);route_seen=set()
        for step in receipt['capture_steps']:
            cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script:continue
            state=read(path/(cp+'_roll_pet.json'));reward=read(path/(cp+'_reward.json'))
            for group in groups:
                endkey=group[-1]
                if not min(streams[endkey])<=cursor<=max(streams[endkey])+5:continue
                wanted={s for u in group for s in streams[u]};last={d['stream']:d for d in state['draws'] if d['stream'] in wanted}
                if set(last)!=wanted:continue
                draws=[last[s] for s in sorted(wanted)];numeric=None
                if group==groups[-1]:
                    if len(reward['formatters'])!=1:raise ValueError('one native decimal template expected')
                    f=reward['formatters'][0];start=f['buffer'];digits=str(amount);offset=start-0x02000000
                    if f['value']!=amount or f['flags']!=(0x80 if script in (18,53) else 0) or not 0<=offset<=len(ram)-len(digits)-1:raise ValueError('decimal value/format/context')
                    if ram[offset:offset+len(digits)+1]!=bytes(int(d)+1 for d in digits)+b'\xe5':raise ValueError('native decimal RAM codes/terminator')
                    if struct.unpack_from('<I',ram,0xFA74)[0]!=amount:raise ValueError('buffer3 amount mismatch')
                    nd={d['stream']:d for d in reward['digit_draws'] if start<=d['stream']<start+len(digits)}
                    if set(nd)!=set(range(start,start+len(digits))):raise ValueError('decimal character coverage')
                    prefix=sum(next(x['line_advance_pixels'][0] for x in ar['layout'] if x['id']==group[0]) for _ in [0]) if script in (18,53) else 0
                    for i,ch in enumerate(digits):
                        d=nd[start+i];index=int(ch)+1;record=rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]
                        if record!=source[0x608758+index*96:0x608758+(index+1)*96] or d['offset']!=(prefix+i*11)*4 or d['context']!=0x0200FA20:raise ValueError('native decimal glyph/advance')
                        expected[start+i]={'ch':ch,'index':index,'record':record,'id':group[-1]+':native-number','script':script}
                        draws.append(d)
                    numeric={'value':amount,'formatter':f,'native_ram_codes_verified':True,'digit_count':len(digits),'composed_line_advance':next(x['reward_composed_line']['composed_line_advance'] for x in ar['layout'] if x['id']==group[-1])}
                counts=Counter(expected[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('bonus full font reads')
                check=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
                for d in draws:
                    row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;i=expected[d['stream']]['index'];w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0];rects.append((x,y,x+w,y+12))
                vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('bonus vacant pixels/stale page')
                pages.append({'route':path.name,'step':step,'units':group,'numeric':numeric,'vacant_text_pixels_cleared':len(vacant),**check,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes())});route_seen.update(group)
        if route_seen!=keys:raise ValueError(f'bonus page coverage missing {keys-route_seen}')
        observed|=route_seen
    normal=read(ROOT/'analysis'/outdir/'runtime.json');normal_seen=set(normal['runtime_observed_new_units'])
    if normal['rom_sha256']!=m['output_sha256'] or not normal['passed'] or normal_seen&observed:raise ValueError('bonus vs normal coverage')
    unique=[next(p for p in pages if p['numeric'] is not None and int(p['units'][0].split(':')[1])==s) for s in (16,18,52,53)]
    out=ROOT/'analysis'/outdir;sheet=Image.new('RGB',(480,320))
    for i,p in enumerate(unique):sheet.paste(Image.open(ROOT/'poc/runtime'/p['route']/f"step_{p['step']:03}.png"),(i%2*240,i//2*160))
    sheet.save(out/'diagnostic_reward_pages.png')
    added={'687910:16:0','687910:18:0','687910:18:1','687910:52:2','687910:53:2','687910:53:3'}
    if not added<=observed:raise ValueError('six new diagnostic readout coverage')
    r={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'bonus_variable_model':ar['reward_variable_proof'],'normal_runtime_observed_new_units':sorted(normal_seen),'diagnostic_renderer_observed_units':sorted(observed),'new_readout_diagnostic_units':sorted(added),'static_only_units':sorted(set(streams)-normal_seen-observed),'pages':pages,'limits':['Native table maxima800/5 renderer diagnostics only, not normal minigame completion/recording/awards or inventory proof. Diagnostic states quarantined.','Two failure literals normal verified; six new amount literals diagnostic verified. Other prose proof limited to observed diagnostic pages.','Human wording/visual review, Hangul name entry/committed record/redisplay/persistence/old saves, full-game/hardware/audio/release QA pending.']}
    (out/'reward_runtime.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'reward_runtime.json');return r

if __name__=='__main__':main()
