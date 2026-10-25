"""Exact-ROM normal pre-jack-in pages and separate upbeat read-alias evidence."""
import struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from archive_scripts import script_spans
STEM='exe45_ko_development_roll_jackin_v1'
PREFIX='roll-jackin-v1-'

def main():
    m,rom,expected,streams,checks=static(STEM,'660CA8');ar=next(a for a in m['archives'] if a['archive']=='660CA8');pool=0x08000000+ar['rom_offset'];pages=[];settling=[];seen=set();observed={False:set(),True:set()};receipts={}
    for name,diagnostic,wanted in [('normal',False,{'660CA8:1:0','660CA8:2:0','660CA8:2:1'}),('upbeat-diagnostic',True,{'660CA8:3:0','660CA8:3:1'})]:
        path=ROOT/'poc/runtime'/(PREFIX+name);receipt=verify_route(path,m['output_sha256'],seen);receipts[name]=receipt
        if receipt['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('jack-in emulator identity')
        if diagnostic:
            env=read(path/'upbeat_environment.json')
            if not env['passed'] or env['rom_sha256']!=m['output_sha256'] or env['aliases']!=1 or env['context']!=0x0200FA20:raise ValueError('upbeat diagnostic identity')
            for field,tool in [('tool_sha256','capture_roll_jackin_upbeat.py'),('observer_sha256','capture_roll_jackin.py'),('probe_sha256','capture_roll_pet.py')]:
                if env[field]!=sha((ROOT/'tools'/tool).read_bytes()):raise ValueError('upbeat observer drift')
            if receipt.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in receipt['artifacts']:raise ValueError('upbeat quarantine')
        for step in receipt['capture_steps']:
            cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool:continue
            state=read(path/(cp+'_roll_pet.json'))
            for u in wanted:
                script=int(u.split(':')[1]);native_script=2 if diagnostic else script
                if ram[0xFA21]!=native_script or not min(streams[u])<=cursor<=max(streams[u])+5:continue
                last={d['stream']:d for d in state['draws'] if d['stream'] in streams[u]}
                if set(last)!=set(streams[u]):continue
                draws=[last[s] for s in streams[u]]
                if any(d['context']!=0x0200FA20 for d in draws):raise ValueError('jack-in native draw context')
                counts=Counter(expected[d['stream']]['index'] for d in draws);reads={r['index']:r['reads'] for r in state['font_reads']}
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('jack-in font CPU consumption')
                try:proof=pixels(path,step,draws,expected,rom,m)
                except ValueError as e:
                    # Never credit an in-flight screenshot as a pixel pass.
                    # Require a later same-page, identical-glyph-trace snapshot
                    # which passes the unchanged strict pixel validator. Every
                    # changing text pixel must be inside the final glyph only.
                    later=step+1;later_cp=f'step_{later:03}'
                    if str(e)!='PET visible role colors disagree' or later not in receipt['capture_steps']:raise ValueError(f'{name}/{step}/{u}: {e}') from e
                    ls=read(path/(later_cp+'_roll_pet.json'));lr=(path/(later_cp+'_gbaExtWorkRam.bin')).read_bytes()
                    if state['draws']!=ls['draws'] or lr[0xFA21]!=native_script or struct.unpack_from('<I',lr,0xFA4C)[0]!=cursor:raise ValueError('unexplained unsettled glyph state') from e
                    pixels(path,later,draws,expected,rom,m)
                    a=Image.open(path/(cp+'.png')).convert('RGB');b=Image.open(path/(later_cp+'.png')).convert('RGB');diff=[(x,y) for y in range(110,150) for x in range(92,234) if a.getpixel((x,y))!=b.getpixel((x,y))]
                    last=draws[-1];row,off=divmod(last['offset'],10752);x=92+off//4;y=110+row*14;width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+last['glyph_index']*4)[0]
                    if not diff or any(not(x<=px<x+width and y<=py<y+12) for px,py in diff):raise ValueError('unexplained text pixel changes while settling') from e
                    settling.append({'route':name,'step':step,'unit':u,'credited_as_complete_page':False,'later_pass_step':later,'same_draw_trace':True,'changing_pixels':len(diff),'bounds':[min(px for px,py in diff),min(py for px,py in diff),max(px for px,py in diff),max(py for px,py in diff)],'last_draw':last,'capture_frame':read(path/(cp+'.json'))['frame'],'later_frame':read(path/(later_cp+'.json'))['frame'],'failure':str(e)})
                    continue
                im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
                for d in draws:
                    row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;i=expected[d['stream']]['index'];w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0];rects.append((x,y,x+w,y+12))
                vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(p)!=bg for p in vacant):raise ValueError(f'jack-in stale pixels:{name}/{step}/{u}')
                pages.append({'route':name,'diagnostic':diagnostic,'unit':u,'step':step,'frame':read(path/(cp+'.json'))['frame'],'last_glyph_frame':max(d['frame'] for d in draws),'vacant_text_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});observed[diagnostic].add(u)
        if observed[diagnostic]!=wanted:raise ValueError(f'jack-in coverage:{name}:{observed[diagnostic]}')
    normal_path=ROOT/'poc/runtime'/(PREFIX+'normal');calls=read(normal_path/'step_021_roll_pet.json')['calls']
    if [c['script'] for c in calls]!=[2,1] or any(c['root']!=pool or c['lr']!=0x08037F27 for c in calls):raise ValueError('normal caller/order')
    full=next(p for p in pages if p['unit']=='660CA8:1:0');after=read(normal_path/'step_021_roll_pet.json')
    if calls!=read(normal_path/f"step_{full['step']:03}_roll_pet.json")['calls'] or after['draws']!=read(normal_path/f"step_{full['step']:03}_roll_pet.json")['draws']:raise ValueError('jack-in draw lifetime after exit')
    # While native wait30 is pending, cursor remains at that command; then
    # flagClear3603/3651 advances it. Use input/frame samples only, no writes.
    payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];s1=script_spans(payload,5)[1];wait_end=max(streams['660CA8:1:0'])+1
    if rom[wait_end-0x08000000:wait_end-0x08000000+4]!=bytes.fromhex('ed001e00'):raise ValueError('native wait30 compiled arguments')
    waits=[];released=[]
    for step in receipts['normal']['capture_steps']:
        ram=(normal_path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0];frame=read(normal_path/f'step_{step:03}.json')['frame']
        if ram[0xFA21]==1 and cursor==wait_end:waits.append(frame)
        elif ram[0xFA21]==1 and cursor>wait_end:released.append(frame)
    if not waits or not released or not(max(waits)<min(released)):raise ValueError('native wait lifecycle sample')
    out=ROOT/'analysis/roll_jackin_v1';out.mkdir(parents=True,exist_ok=True);selected=[next(p for p in pages if p['unit']==u) for u in ['660CA8:2:0','660CA8:2:1','660CA8:1:0','660CA8:3:0','660CA8:3:1']];sheet=Image.new('RGB',(720,320))
    for i,p in enumerate(selected):sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+p['route'])/f"step_{p['step']:03}.png"),(i%3*240,i//3*160))
    sheet.paste(Image.open(normal_path/'step_021.png'),(480,160));sheet.save(out/'jackin_pages.png')
    r={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'pages':pages,'normal_runtime_units':sorted(observed[False]),'diagnostic_renderer_units':sorted(observed[True]),'native_entry_order':calls,'draws_stopped_after_transmission':True,'native_wait30_source_controls_preserved':ar['protected_controls_unchanged'],'wait_cursor_samples':waits,'post_wait_cursor_samples':released,'internet_screen_sha256':sha((normal_path/'step_021.png').read_bytes()),'limits':['Upbeat script3 uses a single native table-offset read alias2->3, not normal mood-selection evidence. Diagnostic state quarantined.','Prior reward/hint diagnostics belong to prior ROMs and do not transfer automatically.','Human wording/visual review, full-game/hardware/audio/release QA pending.']}
    r['in_flight_snapshots_not_credited']=settling
    (out/'jackin_runtime.json').write_text(__import__('json').dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'jackin_runtime.json');return r

if __name__=='__main__':main()
