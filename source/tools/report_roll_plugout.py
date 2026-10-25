"""Shared archive relocation, Roll nickname/choices/response exact-ROM pixel QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
STEM='exe45_ko_development_roll_plugout_v1'
PREFIX='roll-plugout-v1-'

def main(outdir='roll_plugout_v1',stem=STEM,prefix=PREFIX,navi='Roll'):
    if navi not in ('Roll','GutsMan'):raise ValueError('unregistered plugout runtime Navi')
    prompt,response,return_archive=(6,26,'65FEC0') if navi=='Roll' else (7,27,'6663B8')
    m,rom,e,streams,checks=static(stem,'778338');streams={k:v for k,v in streams.items() if int(k.split(':')[1]) in (prompt,response)}
    pool=0x08000000+next(a for a in m['archives'] if a['archive']=='778338')['rom_offset'];path=ROOT/'poc/runtime'/(prefix+'choices');r=verify_route(path,m['output_sha256'],set());pages=[];observed=set();cursors={}
    if any(token in (path/'segment.lua').read_text() for token in ('emu.write','emu.setState','matrixCases')):raise ValueError('normal route contains intervention')
    if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('plugout emulator identity')
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    for step in [2,4,6,7,8,9,10]:
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();state=read(path/(cp+'_roll_pet.json'));script=response if step==10 else prompt;keys=[k for k in streams if int(k.split(':')[1])==script]
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script:raise ValueError('plugout native root/script')
        selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
        if set(last)!=set(selected):raise ValueError('plugout incomplete literal draw')
        draws=[last[s] for s in selected];expected=dict(e);nickname=None
        if script==prompt:
            nd=read(path/(cp+'_plugout_ram.json'))['draws'];lastn={d['stream']:d for d in nd};ordered=[lastn[s] for s in sorted(lastn)]
            if not ordered:raise ValueError('missing plugout native nickname')
            first=ordered[0]['stream'];nickname='';offset=0
            if sorted(lastn)!=list(range(first,first+len(ordered))) or ram[first-0x02000000+len(ordered)]!=0xE5:raise ValueError('plugout nickname stream/terminator')
            for d in ordered:
                index=ram[d['stream']-0x02000000]
                if index!=d['glyph_index'] or index not in codes or d['offset']!=offset or d['context']!=0x0200FA20:raise ValueError('plugout nickname index/geometry')
                record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset']
                if rom[font+index*96:font+(index+1)*96]!=record:raise ValueError('plugout native font changed')
                expected[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
            if draws[0]['offset']!=offset:raise ValueError('plugout nickname comma position')
            draws=ordered+draws
            a,b,k=struct.unpack_from('<HHH',(path/(cp+'_gbaSpriteRam.bin')).read_bytes(),0)
            if a&255!=136 or k&1023!=1020 or k>>12!=14:raise ValueError('plugout choice cursor OBJ')
            cursors[step]=b&511
        counts=Counter(expected[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('plugout font CPU read coverage')
        proof=pixels(path,step,draws,expected,rom,m,origin=(52,110),cursor_screen_background=True);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=52+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        # Choice cursor is native UI, not stale text. Its unchanged16x16 OBJ
        # may paint beyond the font cell; exclude only this native UI rectangle.
        if script==prompt:rects.append((cursors[step],136,cursors[step]+16,152))
        vacant=[(x,y) for y in range(110,150) for x in range(52,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
        if any(im.getpixel(p)!=bg for p in vacant):raise ValueError(f'plugout stale text pixels/{step}')
        pages.append({'step':step,'script':script,'units':keys,'nickname':nickname,'vacant_text_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});observed.update(keys)
    if observed!=set(streams) or not(cursors[2]==cursors[4]==cursors[6]==cursors[8] and cursors[7]==cursors[9]<cursors[2]):raise ValueError('plugout defaultNo/left/right selection')
    for before,after in [(2,3),(4,5)]:
        a=read(path/f'step_{before:03}_roll_pet.json');b=read(path/f'step_{after:03}_roll_pet.json')
        if a['draws']!=b['draws']:raise ValueError('No/cancel must not draw Yes response')
    return_pool=0x08000000+next(a for a in m['archives'] if a['archive']==return_archive)['rom_offset']
    after=(path/'step_011_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',after,0xFA50)[0]!=return_pool or after[0xFA21]!=1:raise ValueError('Yes response to normal return')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,320))
    for i,step in enumerate([2,7,8,10,11,13]):sheet.paste(Image.open(path/f'step_{step:03}.png'),(i%3*240,i//3*160))
    sheet.save(out/'plugout_pages.png');result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'normal_runtime_units':sorted(observed),'pages':pages,'choice_cursor_x':cursors,'defaultNo_leftYes_rightNo':True,'No_and_B_no_response_draw':True,'Yes_response_to_normal_return':True,'limits':['Other44 scripts retained in Japanese; relocated source bytes/pointers verified, other Navi runtime branches not claimed.','Observed native nickname ああくん only; first-line comma unchanged.','Human wording/visual, whole-game/hardware/audio/release approval pending.']}
    result['normal_msgOpen_origin']=[52,110]
    result['navi']=navi
    result['limits']=[f'Only {navi} script{prompt}/{response} runtime verified in this report; other Navi execution not claimed.',f'Native nickname observed: {pages[0]["nickname"]}; not general Hangul input/persistence proof.','Human wording/visual, whole-game/hardware/audio/release approval pending.']
    result['native_cursor_screen_rectangle_background_only_exclusion']=True
    (out/'plugout_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'plugout_runtime.json');return result

if __name__=='__main__':main()
