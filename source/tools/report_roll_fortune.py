"""Exact-ROM normal fortune pages, timed dots, font reads and OBJ pixels."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
from tpl_literals import literals
from build_development_patch import translate_literal_scope,selected_scope

STEM='exe45_ko_development_roll_fortune_v1'
PREFIX='roll-fortune-v1-'

def main(stem=STEM,prefix=PREFIX,outdir='roll_fortune_v1',extra_routes=()):
    m,rom,expected,streams,checks=static(stem,'65FF3C')
    ar=next(a for a in m['archives'] if a['archive']=='65FF3C');root=0x08000000+ar['rom_offset']
    original=(ROOT/'analysis/tpl_baseline/65FF3C.tpl').read_text(encoding='utf-8-sig');asset=read(ROOT/next(a['path'] for a in m['translation_assets'] if a['archive']=='65FF3C'));scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FF3C'],asset)
    translated=translate_literal_scope(original,asset['units'],scope)
    dots=[x for x in literals(translated) if x.text=='・']
    if len(dots)!=6 or any(x.text!=next(y.text for y in literals(original) if y.key==x.key) for x in dots):raise ValueError('six timed dots')
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    dot=codes['・'];seen=set();pages=[];observed=set();timing=[]
    for name in ['fortune-select','fortune-intro',*extra_routes]:
        path=ROOT/'poc/runtime'/(prefix+name);receipt=verify_route(path,m['output_sha256'],seen)
        if receipt['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
        for step in receipt['capture_steps']:
            cp=f'step_{step:03}';state=read(path/(cp+'_roll_pet.json'));ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes()
            if struct.unpack_from('<I',ram,0xFA50)[0]!=root:continue
            script=ram[0xFA21];cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
            keys=[u for u in streams if int(u.split(':')[1])==script]
            for unit in keys:
                is_dots=unit in ['65FF3C:0:3','65FF3C:1:2']
                end=min(streams['65FF3C:0:7' if script==0 else '65FF3C:1:6']) if is_dots else max(streams[unit])+5
                if not min(streams[unit])<=cursor<=end:continue
                last={d['stream']:d for d in state['draws'] if d['stream'] in streams[unit]}
                if set(last)!=set(streams[unit]):continue
                draws=[last[s] for s in streams[unit]]
                if is_dots:
                    native=[d for d in state['draws'] if max(streams[unit])<d['stream']<end and d['glyph_index']==dot[0]]
                    native=list({d['stream']:d for d in native}.values())
                    if len(native)!=3:raise ValueError('three dots not fully drawn')
                    for d in native:
                        off=d['stream']-0x08000000
                        if rom[off:off+len(dot)]!=dot:raise ValueError('dot stream encoding')
                        i=dot[0];f=m['extension']['normal_font_offset'];expected[d['stream']]={'ch':'・','index':i,'record':rom[f+i*96:f+(i+1)*96],'id':unit+':timed-dot','script':script}
                    frames=[d['frame'] for d in sorted(native,key=lambda d:d['stream'])]
                    if any(b-a<30 for a,b in zip(frames,frames[1:])):raise ValueError('native waitSkip dot pacing')
                    timing.append({'route':name,'step':step,'frames':frames,'spacing':[b-a for a,b in zip(frames,frames[1:])]});draws+=native
                counts=Counter(expected[d['stream']]['index'] for d in draws);reads={r['index']:r['reads'] for r in state['font_reads']}
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('fortune font CPU reads')
                proof=pixels(path,step,draws,expected,rom,m)
                # Verify the vacated text interior, not the native border or
                # page arrow. Every current glyph rectangle is excluded;
                # stale ink/shadows anywhere else must have been cleared.
                im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
                for d in draws:
                    row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;i=expected[d['stream']]['index'];w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+i*4)[0];rects.append((x,y,x+w,y+12))
                vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not (x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
                if any(im.getpixel(p)!=bg for p in vacant):raise ValueError(f'fortune stale/vacant text pixels:{name}/{step}/{unit}')
                proof.update(vacant_text_pixels_cleared=len(vacant))
                pages.append({'route':name,'step':step,'unit':unit,**proof,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes())});observed.add(unit)
    required={u for u in streams if int(u.split(':')[1]) in ([0,4,20] if len(asset['units']) in (80,88,102,103) else [0,4])}
    if not required<=observed:raise ValueError(f'normal introduction/blue/hint coverage: {sorted(observed)}')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True)
    selected=[next(p for p in pages if p['unit']==u) for u in sorted(observed,key=lambda u:tuple(map(int,u.split(':')[1:])))]
    sheet=Image.new('RGB',(240*3,160*((len(selected)+2)//3)))
    for i,p in enumerate(selected):sheet.paste(Image.open(ROOT/'poc/runtime'/(prefix+p['route'])/f"step_{p['step']:03}.png"),((i%3)*240,(i//3)*160))
    sheet.save(out/'fortune_pages.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'pages':pages,'runtime_observed_units':sorted(observed),'runtime_open_units':sorted(set(streams)-observed),'timed_dot_pacing':timing,'six_timed_dots_source_preserved':True,'page_vacancies_cleared':True,'limits':['Repeat-day script1 remains static only; other outcomes, item-location hints and minigame results untranslated','Blue/depressed wordplay adaptation needs human judgment','Human wording/visual approval, full-game/hardware/audio/release QA pending']}
    if len(asset['units'])==80:result['limits'][0]='All16 heart results and three number-range hints translated as drafts; unobserved units remain static only. Source23 composite-page behavior and minigame result scripts untranslated.'
    if len(asset['units'])==88:result['limits'][0]='Inherited80 fortune units plus eight non-variable minigame result drafts. Normal minigame result gameplay is unverified; diagnostic renderer samples, if any, are reported separately. Source23 and fourteen dynamic reward literals remain Japanese.'
    if len(asset['units'])==102:result['limits'][0]='Inherited88 plus fourteen bonus reward drafts. Minigame normal gameplay, recording and awards unverified; renderer diagnostics separate. Only composite hint23 remains Japanese in this archive apart from six native timed dots.'
    if len(asset['units'])==103:result['limits'][0]='All103 prose literals in this archive translated as drafts; six native timed dots retained. Unobserved units remain static only; hint23 and reward diagnostic evidence separate. Normal minigame completion/awards and real hint23 location selection unverified.'
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json');return result

if __name__=='__main__':main()
