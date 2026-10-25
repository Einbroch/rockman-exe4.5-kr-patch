"""Native chip insertion proof, one renderer diagnostic and focused normals."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_roll_pet_license import literal_end
from archive_scripts import script_spans
from run_roll_chipquest import STEM,PREFIX,OUTDIR

def chip_report():
    m,rom,e,streams,checks=static(STEM,'664E28');ar=next(a for a in m['archives'] if a['archive']=='664E28');pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    path=ROOT/'poc/runtime'/(PREFIX+'script13');r=verify_route(path,m['output_sha256'],set());env=read(path/'license_environment.json');old=read(ROOT/'poc/output/exe45_ko_development_roll_mail_alert_v1.json');oldrom=(ROOT/'poc/output/exe45_ko_development_roll_mail_alert_v1.gba').read_bytes();oldar=next(a for a in old['archives'] if a['archive']=='664E28');oldspans=script_spans(oldrom[oldar['rom_offset']:oldar['rom_offset']+oldar['compiled_bytes']],255);newspans=script_spans(payload,255)
    if any(oldspans[i]!=newspans[i] for i in range(255) if i!=13):raise ValueError('prior PET script bytes drift')
    byarchive={a['archive']:a for a in m['archives']}
    if any(byarchive[a['archive']]['compiled_sha256']!=a['compiled_sha256'] for a in old['archives'] if a['archive']!='664E28') or m['pet_menu_graphics']['final_block_sha256']!=old['pet_menu_graphics']['final_block_sha256']:raise ValueError('prior other payload/graphics drift')
    if not env['passed'] or env['aliases']!=1 or env['native_script']!=0 or env['displayed_entry']!=13 or env['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('chip renderer diagnostic quarantine')
    for file,key in [('capture_roll_pet_license.py','tool_sha256'),('capture_roll_pet_talk.py','observer_sha256'),('capture_roll_pet.py','probe_sha256'),('capture_roll_chipquest.py','wrapper_sha256')]:
        if sha((ROOT/'tools'/file).read_bytes())!=env[key]:raise ValueError('chip observer drift')
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();srcspan=script_spans(source[0x664E28:0x664E28+2158],255)[13]
    if sha(srcspan)!=env['source_script_sha256'] or newspans[13][:21]!=srcspan[:21] or rom[0x765190:0x765190+2437]!=source[0x765190:0x765190+2437]:raise ValueError('chip source insertion/quote/name pool changed')
    for g in env['native_guards']:
        if sha(source[g['start']:g['end']])!=g['sha256'] or rom[g['start']:g['end']]!=source[g['start']:g['end']]:raise ValueError('chip native caller/initializer changed')
    start=pool+struct.unpack_from('<H',payload,26)[0];quote=start+16;e[quote]={'ch':'「','index':146,'record':source[0x608758+146*96:0x608758+147*96],'id':'664E28:13:0-preserved'};selected=streams['664E28:13:1'];text=next(u for u in read(ROOT/'translations/roll_pet_chipquest_ko.json')['units'] if u['id']=='664E28:13:1')['translation'];native=script_spans(source[0x765190:0x765190+2437],256)[104];codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1};pages=[]
    for step in [2,3]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();s=read(path/(cp+'_roll_pet.json'));chip=read(path/(cp+'_chip_draws.json'))['draws'];alias=read(path/(cp+'_license_alias.json'))
        if ram[0x10AC0:0x10AC0+len(native)]!=native or len(chip)!=8 or read(path/(cp+'_talk_ram.json'))['draws']!=chip:raise ValueError('chip104 ROM to native RAM name identity')
        expected=dict(e);name='';width=11
        for i,d in enumerate(chip):
            index=native[i];record=source[0x608758+index*96:0x608758+(index+1)*96];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
            if d['stream']!=0x02010AC0+i or d['glyph_index']!=index or d['offset']!=width*4 or d['context']!=0x0200FA20 or advance!=11 or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record:raise ValueError('chip104 native glyph/geometry')
            expected[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_chip104_RAM'};name+=codes[index];width+=advance
        last={d['stream']:d for d in s['draws'] if d['stream'] in selected or d['stream']==quote}
        if set(last)!=set(selected)|{quote} or last[quote]['offset']!=0 or alias['aliases']!=1 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=0 or s['calls']!=[{'frame':8,'root':pool,'script':0,'lr':0x08037F27}]:raise ValueError('chip native caller/alias/full literal')
        row=0;advance=width;cursor=iter(selected)
        for ch in text:
            if ch=='\n':row+=1;advance=0;continue
            key=next(cursor)
            if last[key]['offset']!=row*10752+advance*4:raise ValueError('chip quote/insertion/suffix line geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[key]['index']*4)[0]
        end=literal_end(rom,selected,e)
        if rom[end-0x08000000:end-0x08000000+5]!=bytes.fromhex('e600f1edff') or struct.unpack_from('<I',ram,0xFA4C)[0]!=end:raise ValueError('chip protected keyWait boundary')
        draws=[last[quote]]+chip+[last[k] for k in selected];counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in s['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('chip CPU font read coverage')
        proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('chip stale text pixels')
        pages.append({'step':step,'unit':'664E28:13:1','native_chip_name':name,'native_chip_width':88,'combined_first_row_width':110,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),'vacant_text_pixels_cleared':len(vacant),**proof})
    for step in [4,5]:
        ram=(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if struct.unpack_from('<I',ram,0xFA50)[0]==pool:raise ValueError('chip quest dismissal did not exit')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'normal_runtime_units':[],'diagnostic_renderer_units':['664E28:13:1'],'prior_other254_PET_script_spans_identical':True,'prior_other15_archive_payloads_identical':True,'pages':pages,'limits':['Native printChip0/104 reaches unchanged Japanese name through RAM; chip-name localization still pending.','PET table alias0 to13; not native chip quest progression or possession evidence.','Prior23 diagnostic routes not recaptured on this ROM; only static script identity and current shared-consumer focused routes.','No full-game/hardware/audio/wording approval.']}
    out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'chipquest_diagnostic_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def main():
    import report_roll_pet_talk as talk
    import report_roll_mail_alert as mail
    from report_roll_intro import main as intro
    from report_roll_pet import main as pet
    from report_attack_caption_runtime import main as caption
    previous=talk.STEM,talk.PREFIX,talk.OUTDIR
    try:talk.STEM=STEM;talk.PREFIX=PREFIX;talk.OUTDIR=OUTDIR;reports=[talk.talk_report()]
    finally:talk.STEM,talk.PREFIX,talk.OUTDIR=previous
    reports.extend([intro(STEM,PREFIX+'roll-',OUTDIR+'/greeting_regression'),pet(STEM,PREFIX,OUTDIR+'/pet_regression'),caption(STEM,PREFIX+'roll-',OUTDIR+'/roll_caption',roll=True)])
    # Mail-arrival source capture is fixed; this ROM crosses its own boundary.
    previous=mail.STEM,mail.PREFIX,mail.OUTDIR
    try:mail.STEM=STEM;mail.PREFIX=PREFIX;mail.OUTDIR=OUTDIR;reports.append(mail.arrival_report())
    finally:mail.STEM,mail.PREFIX,mail.OUTDIR=previous
    from run_roll_pet_weekday import DATE_ACTIONS,INTRO_ACTIONS
    routes=[];names=['date','profile','navi-menu','select-roll','intro']
    for i,name in enumerate(names):
        path=ROOT/'poc/runtime'/(PREFIX+'weekday-'+name);r=verify_route(path,reports[0]['rom_sha256'],set());parent=ROOT/'poc/runtime'/(PREFIX+'weekday-'+names[i-1] if i else PREFIX+'roll-cold-part1')/'result.json'
        if r.get('normal_play_checkpoint_eligible') is False or r['state_origin']!=str(parent) or name=='date' and r['actions']!=DATE_ACTIONS or name=='intro' and r['actions']!=INTRO_ACTIONS:raise ValueError('chipquest weekday normal chain')
        routes.append({'name':name,'result_sha256':sha((path/'result.json').read_bytes())})
    reports.append(chip_report());out=ROOT/'analysis'/OUTDIR;summary={'policy':'development-draft; NON-DISTRIBUTION','passed':all(r['passed'] for r in reports),'release_eligible':False,'rom_sha256':reports[0]['rom_sha256'],'reports_total':6,'normal_reports':5,'diagnostic_reports':1,'new_units':1,'weekday_routes':routes,'limits':reports[-1]['limits']};(out/'focused_runtime.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
