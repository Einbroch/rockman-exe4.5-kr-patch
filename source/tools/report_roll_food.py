"""Native food scene: second-row RAM nickname, ROM/font/VRAM/screen proof."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from run_roll_food import STEM,PREFIX

def main(outdir='roll_food_v1'):
    m,rom,expected,streams,checks=static(STEM,'661858')
    ar=next(a for a in m['archives'] if a['archive']=='661858');pool=0x08000000+ar['rom_offset']
    path=ROOT/'poc/runtime'/(PREFIX+'food');receipt=verify_route(path,m['output_sha256'],set())
    project=read(ROOT/'project.json')
    if receipt['emulator_sha256']!=project['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('food emulator identity')
    source=(ROOT/project['source_profile']['filename']).read_bytes()
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    asset=next(x for x in m['translation_assets'] if x.get('archive')=='661858')
    units={u['id']:u for u in read(ROOT/asset['path'])['units']};pages=[];observed=set()
    for step,indices in [(10,[0]),(11,[1,2]),(12,[3]),(13,[3])]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();state=read(path/(cp+'_roll_pet.json'))
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=11:raise ValueError('food native root/script')
        keys=[f'661858:11:{i}' for i in indices];selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
        if set(last)!=set(selected):raise ValueError('food literal draw coverage')
        draws=[last[s] for s in selected];e=dict(expected);nickname=None;nickname_width=0
        if indices==[1,2]:
            nd=read(path/(cp+'_family_ram.json'))['draws'];native={d['stream']:d for d in nd};ordered=[native[s] for s in sorted(native)];offset=10752;nickname=''
            if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xE5:raise ValueError('food nickname RAM span/terminator')
            for d in ordered:
                index=ram[d['stream']-0x02000000]
                if index!=d['glyph_index'] or index not in codes or d['offset']!=offset or d['context']!=0x0200FA20:raise ValueError('food second-row nickname geometry')
                record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset']
                if rom[font+index*96:font+(index+1)*96]!=record:raise ValueError('food native nickname font')
                advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
                native_width=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
                if advance!=struct.unpack_from('<I',source,native_width+index*4)[0]:raise ValueError('food native nickname advance changed')
                e[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*advance
            nickname_width=(offset-10752)//4
            if last[streams['661858:11:2'][0]]['offset']!=offset:raise ValueError('food comma after second-row nickname')
            draws+=ordered
        for key in keys:
            row=0;advance=0;cursor=iter(streams[key])
            if key.endswith(':2'):row=1;advance=nickname_width
            for ch in units[key]['translation']:
                if ch=='\n':row+=1;advance=0;continue
                s=next(cursor);d=last[s]
                if d['offset']!=row*10752+4*advance:raise ValueError('food exact literal row/advance')
                advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+expected[s]['index']*4)[0]
        counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('food CPU font read coverage')
        proof=pixels(path,step,draws,e,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError('food stale text pixels')
        pages.append({'step':step,'units':keys,'nickname':nickname,'nickname_row':1 if nickname is not None else None,'nickname_width':nickname_width,'vacant_text_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});observed.update(keys)
    calls=read(path/'step_013_roll_pet.json')['calls']
    if len(calls)!=1 or calls[0]['script']!=11 or calls[0]['root']!=pool or calls[0]['lr']!=0x08037F27:raise ValueError('food native caller')
    end=max(streams['661858:11:3'])+1;cursor=struct.unpack_from('<I',(path/'step_013_gbaExtWorkRam.bin').read_bytes(),0xFA4C)[0]
    if not end<=cursor<=end+2 or rom[end-0x08000000:end-0x08000000+11]!=bytes.fromhex('e600f1e900150ee900160e'):raise ValueError('food stop before input initialization')
    if observed!={f'661858:11:{i}' for i in range(4)}:raise ValueError('food four-unit coverage')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,step in enumerate([10,11,12]):sheet.paste(Image.open(path/f'step_{step:03}.png'),(i*240,0))
    sheet.save(out/'food_pages.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'normal_runtime_units':sorted(observed),'pages':pages,'native_entry_calls':calls,'food_question_stopped_before_input_init':True,'food_question_cursor':cursor,'limits':['Only script11 favorite-food question, not food input/confirmation/redisplay/save.','Native nickname preserved; only captured nickname verified.','Human wording/visual and whole-game/hardware/audio/release QA pending.']}
    (out/'food_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def cumulative(outdir='roll_food_v1'):
    import report_roll_family_siblings as siblings
    previous=siblings.STEM,siblings.PREFIX
    try:siblings.STEM=STEM;siblings.PREFIX=PREFIX;reports=siblings.main(outdir)
    finally:siblings.STEM,siblings.PREFIX=previous
    reports.append(main(outdir));expected=read(ROOT/f'poc/output/{STEM}.json')['output_sha256']
    if len(reports)!=12 or not all(r['passed'] and not r['release_eligible'] and r['rom_sha256']==expected for r in reports):raise ValueError('food cumulative exact-ROM reports')
    summary={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':expected,'reports_total':len(reports),'reports':[{'normal_runtime_units':r.get('normal_runtime_units',r.get('runtime_observed_units',[])),'passed':r['passed'],'release_eligible':r['release_eligible']} for r in reports]}
    (ROOT/'analysis'/outdir/'cumulative_runtime.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    return reports

if __name__=='__main__':cumulative()
