"""Native mail arrival evidence; no event alias or observer writes."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_roll_pet_license import nickname_proof,literal_end
from archive_scripts import script_spans
from run_roll_mail_alert import STEM,PREFIX,OUTDIR,ACTIONS

def arrival_report():
    m,rom,e,streams,checks=static(STEM,'661060');ar=next(a for a in m['archives'] if a['archive']=='661060');pool=0x08000000+ar['rom_offset']
    path=ROOT/'poc/runtime'/(PREFIX+'arrival');r=verify_route(path,m['output_sha256'],set());env=read(path/'mail_environment.json')
    if r.get('normal_play_checkpoint_eligible') is False or r['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+'weekday-select-roll')/'result.json') or r['actions']!=ACTIONS or r['capture_steps']!=list(range(1,11)):raise ValueError('native mail route provenance')
    if not env['observer_only'] or env['rom_sha256']!=m['output_sha256'] or env['pool']!=pool or env['size']!=ar['compiled_bytes']:raise ValueError('mail observer identity')
    for file,field in [('capture_roll_mail_alert.py','tool_sha256'),('capture_roll_pet.py','probe_sha256'),('capture_roll_return.py','nickname_probe_sha256')]:
        if sha((ROOT/'tools'/file).read_bytes())!=env[field]:raise ValueError('mail observer drift')
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();before=script_spans(source[0x661060:0x661060+1351],255)[1]
    payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];span=script_spans(payload,255)[1];start=pool+struct.unpack_from('<H',payload,2)[0];initial_at=before.index(b'\x83\x83')
    # Entire prefix through the preserved nickname command precedes literal1.
    prefix_end=min(streams['661060:1:1'])-start
    if span[:prefix_end]!=before[:prefix_end] or span[initial_at:initial_at+2]!=b'\x83\x83':raise ValueError('native alert sound/wait/nickname prefix changed')
    initial=[start+initial_at,start+initial_at+1]
    for k in initial:e[k]={'ch':'!','index':131,'record':source[0x608758+131*96:0x608758+132*96],'id':'661060:1:0-preserved'}
    source_calls=read(ROOT/'poc/runtime/roll-mail-alert-source-v1-arrival/step_008_roll_pet.json')['calls']
    expected_calls=[dict(c,root=pool) for c in source_calls]
    if len(expected_calls)!=1 or expected_calls[0]['script']!=1:raise ValueError('original native mail entry')
    pages=[];selected=streams['661060:1:1'];units=read(ROOT/'translations/roll_mail_alert_ko.json')['units'];text=units[0]['translation']
    for step in [5,6,7,8]:
        cp=f'step_{step:03}';s=read(path/(cp+'_roll_pet.json'));ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes()
        if s['calls']!=expected_calls or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=1:raise ValueError('native mail caller/root/script')
        keys=initial if step<7 else selected;last={d['stream']:d for d in s['draws'] if d['stream'] in keys}
        if set(last)!=set(keys):raise ValueError('mail complete glyph stream')
        ordered=[];nickname='';width=0;expected=e
        if step>=7:
            ordered,width,nickname,expected=nickname_proof(path,cp,ram,rom,m,e);row=0;advance=width;cursor=iter(selected)
            for ch in text:
                if ch=='\n':row+=1;advance=0;continue
                key=next(cursor)
                if last[key]['offset']!=row*10752+advance*4:raise ValueError('mail nickname/body line geometry')
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[key]['index']*4)[0]
            end=literal_end(rom,selected,e)
            if rom[end-0x08000000:end-0x08000000+5]!=bytes.fromhex('e600f1edff') or struct.unpack_from('<I',ram,0xFA4C)[0]!=end:raise ValueError('mail native key wait boundary')
        elif [last[k]['offset'] for k in initial]!=[0,44] or read(path/(cp+'_talk_ram.json'))['draws']:raise ValueError('initial alert geometry')
        draws=[last[k] for k in keys]+ordered;counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in s['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('mail native CPU font read coverage')
        proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('mail stale text pixels')
        pages.append({'step':step,'nickname':nickname,'nickname_width':width,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),'vacant_text_pixels_cleared':len(vacant),**proof})
    for step in [9,10]:
        ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('mail key dismissal did not exit alert')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'normal_runtime_units':['661060:1:1'],'runtime_open_units':[u['id'] for u in units[1:]],'diagnostic_renderer_units':[],'native_calls':expected_calls,'preserved_initial_alert_literals':14,'sound_wait_nickname_prefix_identical':True,'pages':pages,'limits':['Only script1 natural event entry verified; other13 native branches pending.','Audio disabled during capture; retained sound commands do not prove audible output.','Native nickname display only, no Hangul input/save/RTC/full-game/wording approval.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'mail_arrival_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def main():
    import report_roll_pet_weekday as weekday
    previous=weekday.STEM,weekday.PREFIX,weekday.OUTDIR
    try:weekday.STEM=STEM;weekday.PREFIX=PREFIX;weekday.OUTDIR=OUTDIR;reports=weekday.main()
    finally:weekday.STEM,weekday.PREFIX,weekday.OUTDIR=previous
    reports.append(arrival_report());out=ROOT/'analysis'/OUTDIR;summary=read(out/'cumulative_runtime.json');summary.update(reports_total=28,normal_reports=5,new_units=14,mail_arrival_normal_passed=True,new_runtime_open_units=reports[-1]['runtime_open_units']);(out/'cumulative_runtime.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
