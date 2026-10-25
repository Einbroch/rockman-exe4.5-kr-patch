"""Native registered 02:00 AM meal -> RAM -> mixed-script normal dialogue pixels."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from archive_scripts import script_spans
from run_roll_schedule_time import STEM,PREFIX,OUTDIR
def main():
    m,rom,e,streams,checks=static(STEM,'661754');ar=next(a for a in m['archives'] if a['archive']=='661754');pool=0x08000000+ar['rom_offset'];source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];span=script_spans(payload,14)[11];start=pool+struct.unpack_from('<H',payload,22)[0];expected=dict(e)
    anchors=[(bytes.fromhex('f90382017c'),4,124),(bytes.fromhex('f903c20100'),4,0),(bytes.fromhex('fc032d0092f90c4393e600'),4,146),(bytes.fromhex('fc032d0092f90c4393e600'),8,147)];native_streams=[]
    for marker,off,index in anchors:
        if span.count(marker)!=1:raise ValueError('native time/event quote command boundary')
        cursor=start+span.index(marker)+off;native_streams.append(cursor);expected[cursor]={'ch':'native punctuation','index':index,'record':source[0x608758+index*96:0x608758+(index+1)*96],'id':'protected-clock/name-punctuation'}
    oldm=read(ROOT/'poc/output/exe45_ko_development_roll_schedule_v1.json');old=(ROOT/'poc/output/exe45_ko_development_roll_schedule_v1.gba').read_bytes()
    if sha(old)!=oldm['output_sha256']:raise ValueError('prior baseline')
    for a in oldm['archives']:
        if a['archive']=='661754':continue
        b=next(b for b in m['archives'] if b['archive']==a['archive'])
        if rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']]!=old[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]:raise ValueError('prior17 payload drift')
    for stage in ['calendar','time','meal','list']:
        verify_route(ROOT/'poc/runtime'/(PREFIX+stage),m['output_sha256'],set())
    path=ROOT/'poc/runtime'/(PREFIX+'list');r=read(path/'result.json');env=read(path/'native_schedule_environment.json')
    if not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['pool']!=pool or r.get('normal_play_checkpoint_eligible') is False or (path/'diagnostic_checkpoint.mss').exists():raise ValueError('native query quarantine/identity')
    for file,key in [('capture_roll_schedule_native.py','tool_sha256'),('capture_roll_pet.py','probe_sha256')]:
        if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('native observer drift')
    pages=[]
    for step in [5,6]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();state=read(path/(cp+'_roll_pet.json'));dynamic=read(path/(cp+'_schedule_ram.json'))['draws'];selected=streams['661754:11:2'];want_streams=selected+native_streams;last={d['stream']:d for d in state['draws'] if d['stream'] in want_streams}
        if set(last)!=set(want_streams) or len(state['calls'])!=1 or state['calls'][0]['root']!=pool or state['calls'][0]['script']!=10 or state['calls'][0]['lr']!=0x08037F27 or ram[0xFA21]!=11:raise ValueError('native L10 -> lookup branch11')
        indices=[0,3,1,1,94,106,207,180,202];offsets=[0,32,120,164,240,284,10796,10840,10884];addresses=[0x02010AC0,0x02010AC1,0x02010B40,0x02010B41,0x02010BC0,0x02010BC1,0x02010C40,0x02010C41,0x02010C42]
        if len(dynamic)!=9:raise ValueError('native hour/minute/AM/name glyph population')
        current=dict(expected)
        for d,index,off,address in zip(dynamic,indices,offsets,addresses):
            record=source[0x608758+index*96:0x608758+(index+1)*96]
            if d['stream']!=address or d['byte']!=index or d['glyph_index']!=index or d['offset']!=off or d['context']!=0x0200FA20 or ram[address-0x02000000]!=index or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record:raise ValueError('native buffer residency/font/position')
            current[address]={'ch':'native clock/event','index':index,'record':record,'id':'native-buffer'}
        for address,size in [(0x02010AC0,2),(0x02010B40,2),(0x02010BC0,2),(0x02010C40,3)]:
            if ram[address-0x02000000+size]!=0xE5:raise ValueError('native buffer terminator')
        if [last[s]['offset'] for s in selected]!=[328,376]:raise ValueError('부터 after native 82px prefix')
        end=start+span.index(bytes.fromhex('fc032d0092f90c4393e600'))+9
        if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('native event page keyWait')
        draws=[last[s] for s in want_streams]+dynamic;counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU font read coverage')
        proof=pixels(path,step,draws,current,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('native time suffix stale pixels')
        pages.append({'step':step,'first_row_width':106,'event_name_width_with_quotes':55,'native_buffer_bytes':[2,2,2,3],'vacant_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof})
    # New-ROM native greeting, schedule intro, and list ending remain bound to
    # their literal streams; complete-page font/pixels checked independently.
    other=[]
    for step,key in [(3,'661754:10:0'),(7,'661754:12:0')]:
        state=read(path/f'step_{step:03}_roll_pet.json');last={d['stream']:d for d in state['draws'] if d['stream'] in streams[key]}
        if set(last)!=set(streams[key]):raise ValueError('normal surrounding page coverage')
        other.append({'step':step,'unit':key,**pixels(path,step,list(last.values()),e,rom,m)})
    ram=(path/'step_009_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('normal list exit')
    from bench_dialogue_chip_name import main as bench
    b=bench(STEM,OUTDIR);out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True)
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'normal_runtime_units':['661754:10:0','661754:11:2','661754:12:0'],'new_wording_count':1,'previous17_payloads_identical':True,'pages':pages,'surrounding_pages':other,'name_selector_cpu_vectors':b['vectors'],'limits':['Native same-session calendar02:00 AM one-time meal only; no persistent save/RTC claim.','Source ごはん event name remains Japanese; other AMPM/times/names/multi-event loops pending.','No Hangul input, audio, hardware, full-game or human wording/release approval.']}
    (out/'time_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('native schedule time QA',True);return result
if __name__=='__main__':main()
