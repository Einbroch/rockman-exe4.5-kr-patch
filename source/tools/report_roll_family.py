"""Exact-ROM post-internet younger-sister dialogue, choices and nickname QA."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,static,pixels,sha,verify_route
STEM='exe45_ko_development_roll_family_sister_v1'
PREFIX='roll-family-sister-v1-'

def main(outdir='roll_family_sister_v1',question_script=7,response_script=8,entry_steps=(15,16,17,18,19,20)):
    m,rom,e,streams,checks=static(STEM,'661858');ar=next(a for a in m['archives'] if a['archive']=='661858');pool=0x08000000+ar['rom_offset'];seen=set();pages=[];observed=set();cursors={};routes={}
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    samples={'entry':list(zip(entry_steps,[[0],[1],[2],[3],[4,5],[4,5]])),'yes':[(2,[6]),(3,[6])],'no':[(5,[0]),(6,[0])]}
    for name,wanted in samples.items():
        path=ROOT/'poc/runtime'/(PREFIX+name);r=verify_route(path,m['output_sha256'],seen);routes[name]=r
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('family emulator identity')
        for step,indices in wanted:
            cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();script=response_script if name=='no' else question_script;keys=[f'661858:{script}:{i}' for i in indices];state=read(path/(cp+'_roll_pet.json'))
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script:raise ValueError(f'family root/script {name}/{step}')
            selected=[s for k in keys for s in streams[k]];last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
            if set(last)!=set(selected):raise ValueError('family incomplete draw coverage')
            draws=[last[s] for s in selected];expected=dict(e);nickname=None
            if keys==[f'661858:{question_script}:3']:
                nd=read(path/(cp+'_family_ram.json'))['draws'];lastn={d['stream']:d for d in nd};ordered=[lastn[s] for s in sorted(lastn)];offset=0;nickname=''
                if not ordered or sorted(lastn)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xE5:raise ValueError('family nickname RAM stream/terminator')
                for d in ordered:
                    index=ram[d['stream']-0x02000000]
                    if index!=d['glyph_index'] or index not in codes or d['offset']!=offset or d['context']!=0x0200FA20:raise ValueError('family nickname index/geometry')
                    record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset']
                    if rom[font+index*96:font+(index+1)*96]!=record:raise ValueError('family native nickname font')
                    expected[d['stream']]={'ch':codes[index],'index':index,'record':record,'id':'native_RAM_nickname'};nickname+=codes[index];offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
                if draws[0]['offset']!=offset or expected[draws[0]['stream']]['ch']!='、':raise ValueError('family particle-free comma geometry')
                draws=ordered+draws
            counts=Counter(expected[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('family CPU font read coverage')
            proof=pixels(path,step,draws,expected,rom,m,cursor_screen_background=indices==[4,5]);im=Image.open(path/(cp+'.png')).convert('RGB');bg=im.getpixel((233,110));rects=[]
            for d in draws:
                row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
            if indices==[4,5]:
                a,b,k=struct.unpack_from('<HHH',(path/(cp+'_gbaSpriteRam.bin')).read_bytes(),0)
                if a&255!=108 or k&1023!=1020 or k>>12!=14:raise ValueError('family separate-page choice cursor')
                cursors[f'{name}/{step}']=b&511;rects.append((b&511,108,(b&511)+16,124))
            vacant=[(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)]
            if any(im.getpixel(p)!=bg for p in vacant):raise ValueError(f'family stale text/{name}/{step}')
            pages.append({'route':name,'step':step,'script':script,'units':keys,'nickname':nickname,'vacant_text_pixels_cleared':len(vacant),'screenshot_sha256':sha((path/(cp+'.png')).read_bytes()),**proof});observed.update(keys)
    wanted_streams={k for k in streams if int(k.split(':')[1]) in [question_script,response_script]}
    if len(wanted_streams)!=8 or observed!=wanted_streams:raise ValueError('family eight-unit normal coverage')
    no=ROOT/'poc/runtime'/(PREFIX+'no');moves=[]
    for step in range(1,5):
        ram=(no/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',(no/f'step_{step:03}_gbaSpriteRam.bin').read_bytes(),0)
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=question_script or a&255!=108 or k&1023!=1020:raise ValueError('family choice navigation state')
        moves.append(b&511)
    if not(moves[0]==moves[2]==cursors[f'entry/{entry_steps[-1]}']<moves[1]==moves[3]):raise ValueError('family defaultYes/rightNo/leftYes')
    entry=ROOT/'poc/runtime'/(PREFIX+'entry');calls=read(entry/f'step_{entry_steps[-1]:03}_roll_pet.json')['calls']
    if len(calls)!=1 or calls[0]['script']!=question_script or calls[0]['root']!=pool or calls[0]['lr']!=0x08037F27:raise ValueError('family native entry caller')
    end=max(streams[f'661858:{question_script}:6'])+1;yes=ROOT/'poc/runtime'/(PREFIX+'yes');cursor=struct.unpack_from('<I',(yes/'step_003_gbaExtWorkRam.bin').read_bytes(),0xFA4C)[0]
    if not end<=cursor<=end+2 or rom[end-0x08000000:end-0x08000000+11]!=bytes.fromhex('e600f1e900150ee900160e'):raise ValueError('name question stop before input-init flags')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,480));shots=[('entry',s) for s in entry_steps[:5]]+[('no',4),('no',5),('yes',2)]
    for i,(name,step) in enumerate(shots):sheet.paste(Image.open(ROOT/'poc/runtime'/(PREFIX+name)/f'step_{step:03}.png'),(i%3*240,i//3*160))
    sheet.save(out/'family_pages.png');result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':checks,'normal_runtime_units':sorted(observed),'pages':pages,'choice_cursor_x':moves,'defaultYes_rightNo_leftYes':True,'native_entry_calls':calls,'nickname_topic_suffix_pixels':{'source':22,'translated':11},'name_question_stopped_before_input_init':True,'name_question_cursor':cursor,'limits':['Only younger-sister7/8 selected; other95 scripts preserved including unselected leading-newline29.','Other sibling entry conditions unresolved; survey-v1 selected5, exact survey-v2 recipe selected7. No random-condition claim.','No typed family-name entry/confirmation/persistence or actual personal-name data changed.','Human wording/visual, whole-game/hardware/audio/release approval pending.']}
    result['limits']=[f'Only family scripts {question_script}/{response_script} normal coverage in this report; see static protected-script count for cumulative scope.','Sibling entry conditions unresolved; distinct normal input recipes select5 and7. No player-gender/random-condition claim.','No typed family-name entry/confirmation/persistence or actual personal-name data changed.','Human wording/visual, whole-game/hardware/audio/release approval pending.']
    (out/'family_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'family_runtime.json');return result

if __name__=='__main__':main()
