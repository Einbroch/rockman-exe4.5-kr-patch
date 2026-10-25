"""Separate license renderer diagnostics from normal PET/cold-chain evidence."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from run_roll_pet_license import STEM,PREFIX,OUTDIR,SCRIPTS
from korean_codec import encode_character,EXTRA_CHARACTER_INDICES

def literal_end(rom,selected,expected):
    # Stream keys point at the first byte of a glyph, not its final byte.
    last=max(selected);ch=expected[last]['ch']
    data=encode_character(ch) if 0xAC00<=ord(ch)<=0xD7A3 or ch in EXTRA_CHARACTER_INDICES else bytes([expected[last]['index']])
    offset=last-0x08000000
    if rom[offset:offset+len(data)]!=data:raise ValueError('diagnostic final glyph bytes')
    return last+len(data)

def nickname_proof(path,cp,ram,rom,m,expected):
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    nw=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    native={d['stream']:d for d in read(path/(cp+'_talk_ram.json'))['draws']};ordered=[native[k] for k in sorted(native)];offset=0;nickname='';expected=dict(expected)
    if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xE5:raise ValueError('diagnostic nickname span')
    for d in ordered:
        index=ram[d['stream']-0x02000000];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0];record=source[0x608758+index*96:0x608758+(index+1)*96]
        if index!=d['glyph_index'] or d['offset']!=offset or index not in codes or d['context']!=0x0200FA20 or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,nw+index*4)[0]:raise ValueError('diagnostic nickname native font/advance/geometry')
        expected[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*advance
    return ordered,offset//4,nickname,expected

def diagnostic_report(script):
    m,rom,e,streams,checks=static(STEM,'664E28');key=f'664E28:{script}:0';selected=streams[key];path=ROOT/'poc/runtime'/f'{PREFIX}script{script}';r=verify_route(path,m['output_sha256'],set());environment=read(path/'license_environment.json');ar=next(a for a in m['archives'] if a['archive']=='664E28');pool=0x08000000+ar['rom_offset']
    project=read(ROOT/'project.json')
    if r['emulator_sha256']!=project['development_dependencies']['runtime_capture']['mesen_sha256'] or not environment['passed'] or environment['rom_sha256']!=m['output_sha256'] or environment['aliases']!=1 or environment['native_script']!=0 or environment['displayed_entry']!=script or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('license diagnostic identity/quarantine')
    entry_tool=environment.get('entry_tool','capture_roll_pet_license.py')
    if entry_tool not in ['capture_roll_pet_license.py','capture_roll_pet_events.py','capture_roll_pet_mail.py','capture_roll_pet_weekday.py']:raise ValueError('unregistered PET entry observer')
    for module,field in [(entry_tool,'tool_sha256'),('capture_roll_pet_talk.py','observer_sha256'),('capture_roll_pet.py','probe_sha256')]:
        if sha((ROOT/'tools'/module).read_bytes())!=environment[field]:raise ValueError('license observer drift')
    source=(ROOT/project['source_profile']['filename']).read_bytes()
    if entry_tool=='capture_roll_pet_events.py':
        from archive_scripts import script_spans
        flags={16:9424,18:9425,19:9426,20:9427,21:9428,22:9429}
        if script not in flags:raise ValueError('event scope mismatch')
        prefix=b'\xee\x00'+struct.pack('<H',flags[script])+b'\x21\xff'
        original=script_spans(source[0x664E28:0x664E28+2158],255)[script]
        compiled=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],255)[script]
        if not original.startswith(prefix) or not compiled.startswith(prefix) or environment['entry_flag_prefix_hex']!=prefix.hex():raise ValueError('event checkFlag branch altered')
    if entry_tool=='capture_roll_pet_mail.py':
        from archive_scripts import script_spans
        if script not in [32,33]:raise ValueError('mail entry scope')
        prefix=(b'\xee\x00'+struct.pack('<H',9430)+b'\x21\xff') if script==32 else b''
        window=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')+(bytes.fromhex('f90c01') if script==33 else b'')
        original=script_spans(source[0x664E28:0x664E28+2158],255)[script];compiled=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],255)[script]
        if not original.startswith(prefix+window) or not compiled.startswith(prefix+window) or environment['entry_flag_prefix_hex']!=prefix.hex():raise ValueError('mail entry flag/nickname changed')
    if entry_tool=='capture_roll_pet_weekday.py':
        from archive_scripts import script_spans
        if script not in [26,28,29]:raise ValueError('weekday entry scope')
        prefix=bytes.fromhex('ee2d0c00001effee2d0c06061eff' if script==29 else 'ee2d0c000022ffee2d0c060622ff')
        window=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')+(bytes.fromhex('f90c01') if script==28 else b'')
        original=script_spans(source[0x664E28:0x664E28+2158],255)[script];compiled=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],255)[script]
        if not original.startswith(prefix+window) or not compiled.startswith(prefix+window) or environment['entry_flag_prefix_hex']!=prefix.hex():raise ValueError('weekday branch/nickname changed')
    for g in environment['native_guards']:
        if sha(source[g['start']:g['end']])!=g['sha256'] or rom[g['start']:g['end']]!=source[g['start']:g['end']]:raise ValueError('license source native guards')
    if 'wrapper' in environment:
        if environment['wrapper'] not in ['capture_roll_pet_incident.py','capture_roll_pet_keyquest.py','capture_roll_pet_tournament.py','capture_roll_pet_undernet.py'] or sha((ROOT/'tools'/environment['wrapper']).read_bytes())!=environment['wrapper_sha256']:raise ValueError('PET diagnostic wrapper drift')
        if environment['wrapper']=='capture_roll_pet_undernet.py' and script!=27:raise ValueError('undernet diagnostic scope')
    asset=next(a for a in m['translation_assets'] if a.get('archive')=='664E28');units={u['id']:u for u in read(ROOT/asset['path'])['units']};pages=[]
    samples=[(2,0),(4,1),(5,1)] if script in [17,26,27,28,34] else [(2,0),(3,0)]
    for step,literal in samples:
        key=f'664E28:{script}:{literal}';selected=streams[key];text=units[key]['translation']
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();s=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in s['draws'] if d['stream'] in selected};alias=read(path/(cp+'_license_alias.json'))
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=0 or set(last)!=set(selected) or alias['aliases']!=1:raise ValueError('license diagnostic pool/native0/literal coverage')
        if s['calls']!=[{'frame':8,'root':pool,'script':0,'lr':0x08037F27}]:raise ValueError('license diagnostic native caller')
        ordered=[];nickname_width=0;nickname='';expected=e
        if script in [28,33]:
            ordered,nickname_width,nickname,expected=nickname_proof(path,cp,ram,rom,m,e)
            if script==28 and literal==1:
                # Observer logs retain first-page RAM draws. They are not
                # current-page pixels after clearMsg; require their region to
                # clear by excluding them from the occupied rectangles below.
                ordered=[];nickname_width=0;nickname=''
        elif read(path/(cp+'_talk_ram.json'))['draws']:raise ValueError('license unexpected nickname/variable insertion')
        row=0;advance=nickname_width;cursor=iter(selected)
        for ch in text:
            if ch=='\n':row+=1;advance=0;continue
            stream=next(cursor);d=last[stream]
            if d['offset']!=row*10752+4*advance:raise ValueError('license exact line geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
        draws=[last[k] for k in selected];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in s['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('license CPU font read coverage')
        proof=pixels(path,step,draws+ordered,expected,rom,m);end=literal_end(rom,selected,e)
        tail=bytes.fromhex('e600f1') if script in [17,26,27,28,34] and literal==0 else bytes.fromhex('e600f1edff')
        if rom[end-0x08000000:end-0x08000000+len(tail)]!=tail or struct.unpack_from('<I',ram,0xFA4C)[0]!=end:raise ValueError('license protected wait boundary')
        im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws+ordered:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('license stale text pixels')
        pages.append({'step':step,'unit':key,'diagnostic':True,'nickname':nickname,'nickname_width':nickname_width,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),'vacant_text_pixels_cleared':len(vacant),**proof})
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'static':checks,'normal_runtime_units':[],'diagnostic_renderer_units':sorted({p['unit'] for p in pages}),'pages':pages,'limits':['Table read alias, not progress/acquisition/native branch evidence.','No alias stored in product ROM.','Whole-game/hardware/audio/wording approval pending.']}
    out=ROOT/'analysis'/OUTDIR/f'script{script}';out.mkdir(parents=True,exist_ok=True);(out/'diagnostic_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def main(new_units=4):
    import report_roll_pet_talk as talk
    from report_roll_intro import main as intro
    from report_roll_pet import main as pet
    from report_attack_caption_runtime import main as caption
    previous=talk.STEM,talk.PREFIX,talk.OUTDIR
    try:talk.STEM=STEM;talk.PREFIX=PREFIX;talk.OUTDIR=OUTDIR;reports=[talk.talk_report()]
    finally:talk.STEM,talk.PREFIX,talk.OUTDIR=previous
    reports.extend([intro(STEM,PREFIX+'roll-',OUTDIR+'/greeting_regression'),pet(STEM,PREFIX,OUTDIR+'/pet_regression'),caption(STEM,PREFIX+'roll-',OUTDIR+'/roll_caption',roll=True)])
    reports.extend(diagnostic_report(s) for s in SCRIPTS);m=read(ROOT/f'poc/output/{STEM}.json')
    if len(reports)!=4+len(SCRIPTS) or not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==m['output_sha256'] for r in reports):raise ValueError('license focused exact-ROM reports')
    source=read(ROOT/'poc/output/exe45_ko_development_roll_pet_talk_v2.json');ar={a['archive']:a for a in m['archives']}
    if not all(ar[a['archive']]['compiled_sha256']==a['compiled_sha256'] for a in source['archives'] if a['archive']!='664E28') or m['pet_menu_graphics']['final_block_sha256']!=source['pet_menu_graphics']['final_block_sha256']:raise ValueError('license prior payload/graphics drift')
    sheet=Image.new('RGB',(240*len(SCRIPTS),160))
    for i,s in enumerate(SCRIPTS):sheet.paste(Image.open(ROOT/'poc/runtime'/f'{PREFIX}script{s}'/'step_003.png'),(i*240,0))
    out=ROOT/'analysis'/OUTDIR;sheet.save(out/'license_diagnostic_pages.png')
    summary={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'reports_total':len(reports),'normal_reports':4,'diagnostic_reports':len(SCRIPTS),'new_units':new_units,'prior_other_archive_payloads_identical':True,'prior_pet_graphics_identical':True,'limits':['Focused modified-consumer QA, not the full prior15-report matrix on this ROM.','Progress branches have renderer diagnostic proof only.']}
    (out/'cumulative_runtime.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
