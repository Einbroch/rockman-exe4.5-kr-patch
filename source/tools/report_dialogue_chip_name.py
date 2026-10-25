"""Exact-ROM guarded source -> native128 copy -> RAM -> normal glyph pixels."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_roll_pet_license import literal_end
from build_visibility_poc import bdf_glyphs,require_hash
from run_dialogue_chip_name import STEM,PREFIX,OUTDIR

def name_report():
    m,rom,e,streams,checks=static(STEM,'664E28');h=m['dialogue_chip_name'];pool=0x08000000+next(a for a in m['archives'] if a['archive']=='664E28')['rom_offset'];name=0x08000000+h['name_offset'];path=ROOT/'poc/runtime'/(PREFIX+'name-script13');r=verify_route(path,m['output_sha256'],set());env=read(path/'name_selector_environment.json');aliasenv=read(path/'license_environment.json')
    if env['rom_sha256']!=m['output_sha256'] or not env['observer_only'] or env['name_source']!=name or aliasenv['aliases']!=1 or not aliasenv['passed'] or aliasenv['displayed_entry']!=13 or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts'] or r['state_origin']!=str(ROOT/'poc/runtime'/(PREFIX+'roll-intro')/'result.json'):raise ValueError('Korean name observer/alias/quarantine identity')
    for file,key,record in [('capture_dialogue_chip_name.py','tool_sha256',env),('capture_roll_chipquest.py','base_wrapper_sha256',env),('capture_roll_pet_license.py','tool_sha256',aliasenv),('capture_roll_pet_talk.py','observer_sha256',aliasenv),('capture_roll_pet.py','probe_sha256',aliasenv)]:
        if sha((ROOT/'tools'/file).read_bytes())!=record[key]:raise ValueError('name observer drift')
    require_hash(ROOT/h['wording_asset_path'],h['wording_asset_sha256']);source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();old=(ROOT/'poc/output/exe45_ko_development_roll_chipquest_v1.gba').read_bytes()
    if any(a!=b and not h['install_offset']<=i<h['install_offset']+12 for i,(a,b) in enumerate(zip(old,rom))) or rom[0x765190:0x765190+2437]!=source[0x765190:0x765190+2437]:raise ValueError('prior ROM/source name pool drift')
    for at in [0x1F7F0,0x22AF8,0x3866C,0x3CB98,0x42F98,0x4CAA8,0x4E6A4,0x4E79C,0x51664]:
        if rom[at:at+8]!=source[at:at+8]:raise ValueError('shared name root pair changed')
    block=rom[h['name_offset']:h['name_offset']+128]
    if len(block)!=128 or sha(block)!=h['name_block_sha256'] or block[:h['name_bytes']].hex()!=h['name_hex'] or block[h['name_bytes']:]!=b'\xe5'*(128-h['name_bytes']):raise ValueError('bounded name source block')
    quote=h['command_stream']-1;e[quote]={'ch':'「','index':146,'record':source[0x608758+146*96:0x608758+147*96],'id':'664E28:13:0-preserved'};selected=streams['664E28:13:1'];glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],set(h['name'][:-1]));pages=[]
    for step in [2,3]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();s=read(path/(cp+'_roll_pet.json'));proof=read(path/(cp+'_name_selector.json'));chip=read(path/(cp+'_chip_draws.json'))['draws']
        if len(proof['abi'])!=2 or [x['label'] for x in proof['abi']]!=['entry','continuation']:raise ValueError('name hook native ABI crossings')
        before,after=[x['regs'] for x in proof['abi']];expectedregs=list(before);expectedregs[0]=name;expectedregs[1]=0x02010AC0;expectedregs[2]=0;expectedregs[7]=before[5]+100
        if before[0]+before[1]!=h['native_name_stream'] or before[4]!=h['command_stream'] or before[5]!=h['context'] or after!=expectedregs:raise ValueError('native selector all-register/SP/LR ABI')
        copies=proof['copy_reads']
        if len(copies)!=128 or any(c['address']!=name+127-i or c['remaining']!=127-i or c['value']!=block[127-i] or c['source']!=name or c['destination']!=0x02010AC0 for i,c in enumerate(copies)) or ram[0x10AC0:0x10B40]!=block:raise ValueError('native128 copy read -> RAM residency')
        expected=dict(e);cursor=0x02010AC0;width=11
        if len(chip)!=4:raise ValueError('name four-glyph population')
        for ch,d in zip(h['name'],chip):
            index=ord(ch)-0xAC00+m['extension']['legacy_index_view'] if ch!='1' else 2;record=rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96];advance=12 if ch!='1' else 11
            if d['stream']!=cursor or d['glyph_index']!=index or d['offset']!=width*4 or d['context']!=0x0200FA20 or struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]!=advance or record!=(glyphs[ch] if ch!='1' else source[0x608758+2*96:0x608758+3*96]):raise ValueError('name codec/font/advance/geometry')
            expected[cursor]={'ch':ch,'index':index,'record':record,'id':'765190:104:0-normal-RAM'};cursor+=4 if ch!='1' else 1;width+=advance
        if ram[cursor-0x02000000]!=0xE5 or width!=58:raise ValueError('name terminator/first-row insertion width')
        last={d['stream']:d for d in s['draws'] if d['stream'] in selected or d['stream']==quote}
        if set(last)!=set(selected)|{quote} or last[quote]['offset']!=0 or s['calls']!=[{'frame':8,'root':pool,'script':0,'lr':0x08037F27}]:raise ValueError('name original PET consumer/glyph coverage')
        text=next(u for u in read(ROOT/'translations/roll_pet_chipquest_ko.json')['units'] if u['id']=='664E28:13:1')['translation'];row=0;advance=width;cursor_iter=iter(selected)
        for ch in text:
            if ch=='\n':row+=1;advance=0;continue
            key=next(cursor_iter)
            if last[key]['offset']!=row*10752+advance*4:raise ValueError('Korean name/suffix combined layout')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[key]['index']*4)[0]
        end=literal_end(rom,selected,e)
        if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+5]!=bytes.fromhex('e600f1edff'):raise ValueError('name protected keyWait')
        draws=[last[quote]]+chip+[last[k] for k in selected];counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in s['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('name CPU font read coverage')
        pixelproof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('name stale pixels')
        pages.append({'step':step,'name':'빅해머1','name_width':47,'combined_first_row_width':69,'native_copy_bytes':128,'all_registers_SP_LR_match_source_contract':True,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),'vacant_text_pixels_cleared':len(vacant),**pixelproof})
    for step in [4,5]:
        if struct.unpack_from('<I',(path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes(),0xFA50)[0]==pool:raise ValueError('name dialogue exit')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'normal_runtime_units':[],'diagnostic_renderer_units':['664E28:13:1','765190:104:0-normal-dialogue-reuse'],'new_wording_count':0,'prior_common_ROM_identical_except_install12':True,'shared_nine_root_pairs_and_native_name_pool_identical':True,'pages':pages,'limits':['PET alias13 only, not normal chip acquisition or quest progression.','Only exact Roll13 command/normal context/native104 stream selected; other dialogue names remain native.','Guard fallback/CPSR boundary fixtures are synthetic CPU evidence, not all normal game callers.','No audio/hardware/save/RTC/full-game/wording approval.']};out=ROOT/'analysis'/OUTDIR;out.mkdir(parents=True,exist_ok=True);(out/'name_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def main():
    import report_roll_pet_talk as talk
    import report_roll_mail_alert as mail
    from report_roll_intro import main as intro
    from report_roll_pet import main as pet
    from report_attack_caption_runtime import main as caption
    from bench_dialogue_chip_name import main as bench
    previous=talk.STEM,talk.PREFIX,talk.OUTDIR
    try:talk.STEM=STEM;talk.PREFIX=PREFIX;talk.OUTDIR=OUTDIR;reports=[talk.talk_report()]
    finally:talk.STEM,talk.PREFIX,talk.OUTDIR=previous
    reports.extend([intro(STEM,PREFIX+'roll-',OUTDIR+'/greeting_regression'),pet(STEM,PREFIX,OUTDIR+'/pet_regression'),caption(STEM,PREFIX+'roll-',OUTDIR+'/roll_caption',roll=True)])
    previous=mail.STEM,mail.PREFIX,mail.OUTDIR
    try:mail.STEM=STEM;mail.PREFIX=PREFIX;mail.OUTDIR=OUTDIR;reports.append(mail.arrival_report())
    finally:mail.STEM,mail.PREFIX,mail.OUTDIR=previous
    reports.append(name_report());b=bench(STEM,OUTDIR);summary={'policy':'development-draft; NON-DISTRIBUTION','passed':all(r['passed'] for r in reports) and b['passed'],'release_eligible':False,'rom_sha256':reports[0]['rom_sha256'],'reports_total':6,'normal_reports':5,'diagnostic_reports':1,'new_wording_count':0,'cpu_bench_vectors':b['vectors'],'limits':reports[-1]['limits']};(ROOT/'analysis'/OUTDIR/'focused_runtime.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
