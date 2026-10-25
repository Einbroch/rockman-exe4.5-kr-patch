"""Exact-ROM normal return, native RAM nickname and diagnostic defeat pixel QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
STEM='exe45_ko_development_roll_return_v1'
PREFIX='roll-return-v1-'

def main(outdir='roll_return_v1'):
    m,rom,expected,streams,checks=static(STEM,'65FEC0');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='65FEC0')['rom_offset'];pages=[];seen=set();observed={False:set(),True:set()};calls_by_route={}
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    for name,diagnostic in [('normal',False),('defeat-diagnostic',True)]:
        path=ROOT/'poc/runtime'/(PREFIX+name);r=verify_route(path,m['output_sha256'],seen)
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('return emulator identity')
        if diagnostic:
            env=read(path/'defeat_environment.json')
            if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['aliases']!=1:raise ValueError('defeat alias identity')
            for field,tool in [('tool_sha256','capture_roll_return_defeat.py'),('observer_sha256','capture_roll_return.py'),('probe_sha256','capture_roll_pet.py')]:
                if env[field]!=sha((ROOT/'tools'/tool).read_bytes()):raise ValueError('defeat tool drift')
            if r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('defeat quarantine')
        wanted={f'65FEC0:{2 if diagnostic else 1}:{n}' for n in range(2)}
        for step in r['capture_steps']:
            cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0];state=read(path/(cp+'_roll_pet.json'));calls_by_route[name]=state['calls']
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=1:continue
            for unit in wanted:
                if not min(streams[unit])<=cursor<=max(streams[unit])+5:continue
                last={d['stream']:d for d in state['draws'] if d['stream'] in streams[unit]}
                if set(last)!=set(streams[unit]):continue
                draws=[last[s] for s in streams[unit]];e=dict(expected);nickname=None
                if unit=='65FEC0:1:1':
                    nd=read(path/(cp+'_return_ram.json'))['draws']
                    if not nd:raise ValueError('missing native RAM nickname')
                    first=min(d['stream'] for d in nd);lastn={d['stream']:d for d in nd};ordered=[lastn[s] for s in sorted(lastn)];nickname=''
                    if list(sorted(lastn))!=list(range(first,first+len(ordered))) or ram[first-0x02000000+len(ordered)]!=0xE5:raise ValueError('nickname native byte stream/terminator')
                    offset=0
                    for d in ordered:
                        index=ram[d['stream']-0x02000000]
                        if index!=d['glyph_index'] or index not in codes or d['offset']!=offset or d['context']!=0x0200FA20:raise ValueError('nickname decoding/advance')
                        record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset']
                        if rom[font+index*96:font+(index+1)*96]!=record:raise ValueError('nickname source font changed')
                        e[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
                    if draws[0]['offset']!=offset:raise ValueError('nickname comma position')
                    draws=ordered+draws
                counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('return CPU font read coverage')
                proof=pixels(path,step,draws,e,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
                for d in draws:
                    row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
                vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(p)!=bg for p in vacant):raise ValueError(f'return stale pixels {name}/{step}/{unit}')
                pages.append({'route':name,'diagnostic':diagnostic,'unit':unit,'step':step,'nickname':nickname,'vacant_text_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});observed[diagnostic].add(unit)
        if observed[diagnostic]!=wanted:raise ValueError(f'return coverage {name}: {observed[diagnostic]}')
        if len(calls_by_route[name])!=1 or calls_by_route[name][0]['script']!=1 or calls_by_route[name][0]['root']!=pool or calls_by_route[name][0]['lr']!=0x08037F27:raise ValueError('return native entry')
    normal_path=ROOT/'poc/runtime'/(PREFIX+'normal');final_ram=(normal_path/'step_009_gbaExtWorkRam.bin').read_bytes();exit_pool=struct.unpack_from('<I',final_ram,0xFA50)[0]
    if exit_pool==pool or read(normal_path/'step_007_roll_pet.json')['draws']!=read(normal_path/'step_009_roll_pet.json')['draws'] or read(normal_path/'step_007_return_ram.json')['draws']!=read(normal_path/'step_009_return_ram.json')['draws']:raise ValueError('return draw lifetime after next dialogue')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,320))
    for i,unit in enumerate(['65FEC0:1:0','65FEC0:1:1','65FEC0:2:0','65FEC0:2:1']):
        p=next(p for p in pages if p['unit']==unit);sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+p['route'])/f"step_{p['step']:03}.png"),(i%2*240,i//2*160))
    sheet.save(out/'return_pages.png');result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'normal_runtime_units':sorted(observed[False]),'diagnostic_renderer_units':sorted(observed[True]),'native_entry_calls':calls_by_route,'pages':pages,'limits':['Defeat pages use quarantined table read alias1->2, not an actual battle loss.','Native nickname tested for observed default ああくん only; comma line remains unchanged for other names.','Human wording/visual, whole-game/hardware/audio/release approval pending.']}
    result.update(normal_exit_pool=exit_pool,return_draws_stopped_after_exit=True)
    (out/'return_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'return_runtime.json');return result

if __name__=='__main__':main()
