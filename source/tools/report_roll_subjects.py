"""Strong/weak subject native nickname pages and cumulative exact-ROM QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from run_roll_subjects import STEM,PREFIX,SCENES

def scene_report(scene,outdir='roll_subjects_v1'):
    name,script,_,_,confirmations=scene;m,rom,expected,streams,checks=static(STEM,'661858')
    ar=next(a for a in m['archives'] if a['archive']=='661858');pool=0x08000000+ar['rom_offset'];path=ROOT/'poc/runtime'/(PREFIX+name);receipt=verify_route(path,m['output_sha256'],set())
    project=read(ROOT/'project.json')
    if receipt['emulator_sha256']!=project['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('subject emulator identity')
    source=(ROOT/project['source_profile']['filename']).read_bytes();native_width=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    asset=next(a for a in m['translation_assets'] if a.get('archive')=='661858');units={u['id']:u for u in read(ROOT/asset['path'])['units']};pages=[];observed=set();final=11+confirmations
    samples=[(10,0)]+[(10+i,i) for i in range(1,confirmations+1)]+[(final,confirmations)]
    for step,literal in samples:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();state=read(path/(cp+'_roll_pet.json'));key=f'661858:{script}:{literal}';selected=streams[key];last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or set(last)!=set(selected):raise ValueError('subject native root/script/literal coverage')
        draws=[last[s] for s in selected];e=dict(expected);nickname=None;nickname_width=0
        if literal:
            nd=read(path/(cp+'_family_ram.json'))['draws'];native={d['stream']:d for d in nd};ordered=[native[s] for s in sorted(native)];offset=0;nickname=''
            if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xE5:raise ValueError('subject nickname RAM span/terminator')
            for d in ordered:
                index=ram[d['stream']-0x02000000]
                if index!=d['glyph_index'] or index not in codes or d['offset']!=offset or d['context']!=0x0200FA20:raise ValueError('subject nickname first-row geometry')
                record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset'];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
                if rom[font+index*96:font+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,native_width+index*4)[0]:raise ValueError('subject native nickname font/advance')
                e[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*advance
            nickname_width=offset//4;draws+=ordered
        row=0;advance=nickname_width;cursor=iter(selected)
        for ch in units[key]['translation']:
            if ch=='\n':row+=1;advance=0;continue
            stream=next(cursor);d=last[stream]
            if d['offset']!=row*10752+4*advance:raise ValueError('subject exact newline/nickname/literal geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[stream]['index']*4)[0]
        counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('subject CPU font read coverage')
        proof=pixels(path,step,draws,e,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('subject stale text pixels')
        pages.append({'step':step,'units':[key],'nickname':nickname,'nickname_row':0 if nickname is not None else None,'nickname_width':nickname_width,'source_leading_newline_preserved':script==29 and literal==1,'vacant_text_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});observed.add(key)
    calls=read(path/f'step_{final:03}_roll_pet.json')['calls']
    if len(calls)!=1 or calls[0]['script']!=script or calls[0]['root']!=pool or calls[0]['lr']!=0x08037F27:raise ValueError('subject native caller')
    end=max(streams[f'661858:{script}:{confirmations}'])+1;cursor=struct.unpack_from('<I',(path/f'step_{final:03}_gbaExtWorkRam.bin').read_bytes(),0xFA4C)[0]
    if not end<=cursor<=end+2 or rom[end-0x08000000:end-0x08000000+11]!=bytes.fromhex('e600f1e900150ee900160e'):raise ValueError('subject stop before input initialization')
    if observed!={f'661858:{script}:{i}' for i in range(confirmations+1)}:raise ValueError('subject full selected scene coverage')
    out=ROOT/'analysis'/outdir/name;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(240*(confirmations+1),160))
    for i in range(confirmations+1):sheet.paste(Image.open(path/f'step_{10+i:03}.png'),(i*240,0))
    sheet.save(out/'subject_pages.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'normal_runtime_units':sorted(observed),'pages':pages,'native_entry_calls':calls,'subject_question_stopped_before_input_init':True,'subject_question_cursor':cursor,'limits':['Only subject question pages, not typed subject input/confirmation/redisplay/save.','Original captured player nickname retained; no other nickname claim.','Human wording/visual, whole-game/hardware/audio/release QA pending.']}
    (out/'subject_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');return result

def main(outdir='roll_subjects_v1'):
    import report_roll_food as food
    previous=food.STEM,food.PREFIX
    try:food.STEM=STEM;food.PREFIX=PREFIX;reports=food.cumulative(outdir)
    finally:food.STEM,food.PREFIX=previous
    reports.extend(scene_report(s,outdir) for s in SCENES);expected=read(ROOT/f'poc/output/{STEM}.json')['output_sha256']
    if len(reports)!=14 or not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==expected for r in reports):raise ValueError('subject cumulative exact-ROM reports')
    summary={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':expected,'reports_total':len(reports),'school_subject_units':sorted(set().union(*(set(r['normal_runtime_units']) for r in reports[-2:])))}
    (ROOT/'analysis'/outdir/'cumulative_runtime.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8');return reports

if __name__=='__main__':main()
