"""Finite new41 profile units on39 native renderer pages; normal29 regression."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from run_gutsman_questions import STEM,PREFIX

OUT=ROOT/'analysis/gutsman_questions_v1'
PAGE_UNITS={9:[[0],[1],[2]],11:[[0],[1],[2],[3,4],[5]],13:[[0],[1],[2]],15:[[0],[1],[2],[3]],17:[[0],[1],[2],[3],[4],[5]],19:[[0],[1],[2],[3],[4],[5]],21:[[0],[1],[2],[3]],23:[[0],[1],[2],[3]],25:[[0],[1],[2]],88:[[0,1]]}
NICKNAME_LITERAL={9:[1],11:[4],13:[2],15:[1,3],17:[3],19:[3],21:[3],23:[3],25:[2],88:[1]}

def page_end(rom,streams):
    last=max(streams);at=last-0x08000000
    end=last+(4 if rom[at:at+2]==bytes.fromhex('f9fc') else 1)
    if rom[end-0x08000000:end-0x08000000+2]!=bytes.fromhex('e600'):
        raise ValueError('question page must terminate at native keyWait')
    return end

def main():
    import report_gutsman_profile as normal
    old=normal.STEM,normal.PREFIX
    try:
        normal.STEM=STEM;normal.PREFIX=PREFIX;normal_report=normal.main([29],outdir=OUT/'normal_subject_regression')
    finally:normal.STEM,normal.PREFIX=old
    m,rom,e,streams,checks=static(STEM,'667044');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset'];project=read(ROOT/'project.json');source=(ROOT/project['source_profile']['filename']).read_bytes()
    native_width=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    units={u['id']:u for u in read(ROOT/'translations/gutsman_profile_questions_ko.json')['units']};pages=[];seen=set();observed=set();routes={};environments=[]
    for script,groups in PAGE_UNITS.items():
        path=ROOT/'poc/runtime'/(PREFIX+f'diagnostic-{script}');routes[script]=path;r=verify_route(path,m['output_sha256'],seen);env=read(path/'profile_environment.json');environments.append(env)
        if r['emulator_sha256']!=project['development_dependencies']['runtime_capture']['mesen_sha256'] or not env['passed'] or env['aliases']!=1 or env['displayed_script']!=script or env['requested_script']!=29 or env['rom_sha256']!=m['output_sha256'] or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('question diagnostic quarantine/identity')
        for field,filename in [('tool_sha256','capture_gutsman_profile_diagnostic.py'),('observer_sha256','capture_roll_family.py'),('probe_sha256','capture_roll_pet.py')]:
            if env[field]!=sha((ROOT/'tools'/filename).read_bytes()):raise ValueError('question observer identity')
        if env['gender_dispatch_skipped_bytes']!=(6 if script==17 else 0) or env['age_dispatch_skipped_bytes']!=0:raise ValueError('question dispatch intervention scope')
        found_steps=[]
        for indices in groups:
            keys=[f'667044:{script}:{i}' for i in indices];selected=[s for k in keys for s in streams[k]];found=None
            for step in r['capture_steps']:
                cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
                if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=29 or cursor!=page_end(rom,selected):continue
                obs=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
                if set(last)!=set(selected):continue
                draws=[last[s] for s in selected];expected=dict(e);nickname=None;nickname_width=0;nickname_row=None;suffix=next((i for i in indices if i in NICKNAME_LITERAL[script]),None)
                if suffix is not None:
                    nickname_row=1 if script in (11,88) else 0;offset=nickname_row*10752;native={d['stream']:d for d in read(path/(cp+'_family_ram.json'))['draws']};ordered=[native[s] for s in sorted(native)]
                    if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xe5:raise ValueError('question nickname span/terminator')
                    nickname=''
                    for d in ordered:
                        index=ram[d['stream']-0x02000000]
                        if index!=d['glyph_index'] or index not in codes or d['context']!=0x0200FA20 or d['offset']!=offset:raise ValueError('question native nickname row/advance')
                        record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset'];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
                        if rom[font+index*96:font+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,native_width+index*4)[0]:raise ValueError('question nickname glyph/advance identity')
                        expected[d['stream']]=dict(ch=codes[index],index=index,record=record,id='native_RAM_nickname');nickname+=codes[index];offset+=advance*4
                    nickname_width=(offset-nickname_row*10752)//4;draws+=ordered
                row=0;advance=0
                for key in keys:
                    if suffix is not None and int(key.split(':')[2])==suffix:
                        if row!=nickname_row:raise ValueError('question nickname insertion row')
                        advance+=nickname_width
                    iterator=iter(streams[key])
                    for ch in units[key]['translation']:
                        if ch=='\n':row+=1;advance=0;continue
                        stream=next(iterator)
                        if last[stream]['offset']!=row*10752+advance*4:raise ValueError('question joined literal geometry')
                        advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
                reads={x['index']:x['reads'] for x in obs['font_reads']};counts=Counter(expected[d['stream']]['index'] for d in draws)
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('question font CPU reads')
                proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');occupied=set()
                for d in draws:
                    rr,off=divmod(d['offset'],10752);x=92+off//4;y=110+rr*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
                blank={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and (x,y) not in occupied}
                if any(im.getpixel(p)!=im.getpixel((233,110)) for p in blank):raise ValueError('question page stale pixels')
                found=dict(units=keys,script=script,step=step,nickname=nickname,nickname_row=nickname_row,nickname_width=nickname_width,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**proof);break
            if found is None:raise ValueError('question full page unobserved '+str(keys))
            pages.append(found);observed.update(keys);found_steps.append(found['step'])
        if any(b<=a for a,b in zip(found_steps,found_steps[1:])):raise ValueError('question page order')
        lastkey=f'667044:{script}:{groups[-1][-1]}';end=page_end(rom,streams[lastkey]);ram=(path/f"step_{r['capture_steps'][-1]:03}_gbaExtWorkRam.bin").read_bytes()
        if struct.unpack_from('<I',ram,0xFA4C)[0]!=end or rom[end-0x08000000:end-0x08000000+3]!=bytes.fromhex('e600f1'):raise ValueError('question diagnostic must stop at last keyWait before input/clear')
    prior=read(ROOT/'translations/gutsman_profile_ko.json')['units'];new_keys=set(units)-{u['id'] for u in prior}
    if observed!=new_keys or len(observed)!=41 or len(pages)!=39:raise ValueError('new question41 finite population')
    OUT.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(240*5,160*8))
    for i,p in enumerate(pages):sheet.paste(Image.open(routes[p['script']]/f"step_{p['step']:03}.png"),(i%5*240,i//5*160))
    sheet.save(OUT/'question_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_literal_units=m['translated_units'],added_units=41,static=checks,new_units_normal_runtime_verified=[],new_units_diagnostic_renderer_verified=sorted(observed),normal_subject_regression_units=normal_report['normal_runtime_units'],pages=pages,diagnostic_environments=environments,all_diagnostics_stopped_before_input_init=True,limits=['New41 units renderer-only via guarded table read alias, not normal question/response choice or input/persistence evidence.','Script17 gender dispatch bypassed only in diagnostic; source6bytes unchanged.','Original Japanese nickname retained; Japanese keyboard and Hangul input/commit/redisplay/persistence/old saves unresolved.','Whole game translation, human wording/style/release review incomplete.'])
    (OUT/'question_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('New41 literals /39 pages font-OBJ-pixel PASS; normal29 three-page regression PASS');return result

if __name__=='__main__':main()
