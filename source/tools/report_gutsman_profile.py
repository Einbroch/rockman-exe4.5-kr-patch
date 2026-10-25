"""Exact cumulative ROM: profile text, native nickname, font/OBJ/pixel evidence."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from run_gutsman_profile import STEM,PREFIX
from capture_gutsman_profile_diagnostic import SCRIPTS

OUT=ROOT/'analysis/gutsman_profile_v1'

def main(selected_scripts=None,outdir=OUT):
    m,rom,e,streams,checks=static(STEM,'667044');ar=next(a for a in m['archives'] if a['archive']=='667044');pool=0x08000000+ar['rom_offset']
    project=read(ROOT/'project.json');source=(ROOT/project['source_profile']['filename']).read_bytes();native_width=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    units={u['id']:u for u in read(ROOT/'translations/gutsman_profile_ko.json')['units'] if selected_scripts is None or int(u['id'].split(':')[1]) in selected_scripts};seen=set();pages=[];routes={}
    for name in ['choices','weak']+[f'diagnostic-{s}' for s in SCRIPTS if selected_scripts is None or s in selected_scripts]:
        path=ROOT/'poc/runtime'/(PREFIX+name);receipt=verify_route(path,m['output_sha256'],seen)
        if receipt['emulator_sha256']!=project['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('profile emulator identity')
        diagnostic=name.startswith('diagnostic-');script=int(name.split('-')[-1]) if diagnostic else 29
        if diagnostic:
            env=read(path/'profile_environment.json')
            if not env['passed'] or env['aliases']!=1 or env['requested_script']!=29 or env['displayed_script']!=script or env['rom_sha256']!=m['output_sha256'] or env['tool_sha256']!=sha((ROOT/'tools/capture_gutsman_profile_diagnostic.py').read_bytes()) or env['observer_sha256']!=sha((ROOT/'tools/capture_roll_family.py').read_bytes()) or env['probe_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()) or receipt.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in receipt['artifacts']:raise ValueError('profile diagnostic quarantine/identity')
        routes[name]=(path,receipt,script,diagnostic)
    for key,unit in units.items():
        script,literal=map(int,key.split(':')[1:]);found=None
        for name,(path,receipt,target,diagnostic) in routes.items():
            if target!=script:continue
            for step in receipt['capture_steps']:
                cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();cursor=struct.unpack_from('<I',ram,0xFA4C)[0];selected=streams[key]
                if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=29 or not min(selected)<=cursor<=max(selected)+5:continue
                state=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in state['draws'] if d['stream'] in selected}
                if set(last)!=set(selected):continue
                draws=[last[s] for s in selected];expected=dict(e);nickname=None;nickname_width=0
                if (script in (27,29) and literal in (0,2)) or (script in (32,33,34) and literal in (0,3)):
                    native={d['stream']:d for d in read(path/(cp+'_family_ram.json'))['draws']};ordered=[native[s] for s in sorted(native)]
                    if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xe5:raise ValueError('profile nickname contiguous span/terminator')
                    nickname='';offset=0
                    for d in ordered:
                        index=ram[d['stream']-0x02000000]
                        if index!=d['glyph_index'] or index not in codes or d['context']!=0x0200FA20 or d['offset']!=offset:raise ValueError('profile native nickname geometry')
                        record=source[0x608758+index*96:0x608758+(index+1)*96];font=m['extension']['normal_font_offset'];advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
                        if rom[font+index*96:font+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,native_width+index*4)[0]:raise ValueError('profile native nickname font/advance')
                        expected[d['stream']]=dict(ch=codes[index],index=index,record=record,id='native_RAM_nickname');nickname+=codes[index];offset+=4*advance
                    nickname_width=offset//4;draws+=ordered
                row=0;advance=nickname_width;stream_iter=iter(selected)
                for ch in unit['translation']:
                    if ch=='\n':row+=1;advance=0;continue
                    stream=next(stream_iter)
                    if last[stream]['offset']!=row*10752+advance*4:raise ValueError('profile exact literal/newline/nickname advance')
                    advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
                counts=Counter(expected[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
                if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('profile CPU font reads')
                proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');occupied=set()
                for d in draws:
                    row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0]
                    occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
                blank={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and (x,y) not in occupied}
                if any(im.getpixel(xy)!=im.getpixel((233,110)) for xy in blank):raise ValueError('profile vacant page text clearing')
                found=dict(unit=key,route=name,step=step,diagnostic=diagnostic,nickname=nickname,nickname_width=nickname_width,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**proof);break
            if found:break
        if not found:raise ValueError('profile complete page unobserved '+key)
        pages.append(found)
    calls=read(routes['choices'][0]/'step_015_roll_pet.json')['calls']
    if len(calls)!=1 or calls[0]['script']!=29 or calls[0]['root']!=pool or calls[0]['lr']!=0x08037F27:raise ValueError('profile native caller')
    weak=routes['weak'][0];before=(weak/'step_002_gbaExtWorkRam.bin').read_bytes();weak_ram=(weak/'step_003_gbaExtWorkRam.bin').read_bytes();end=max(streams['667044:29:2'])+1
    if struct.unpack_from('<I',before,0xFA4C)[0]!=end or struct.unpack_from('<I',weak_ram,0xFA4C)[0]!=end+11 or rom[end-0x08000000:end-0x08000000+13]!=bytes.fromhex('e600f1e900150ee900160eedff') or read(weak/'step_002_roll_pet.json')['draws']!=read(weak/'step_003_roll_pet.json')['draws']:raise ValueError('native question keyWait/flags/waitHold transition')
    baseline=ROOT/'poc/runtime/gutsman-subjects-source-v1-weak';old=read(ROOT/'poc/output/exe45_ko_development_gutsman_plugout_v1.json');verify_route(baseline,old['output_sha256'],set());crop=(8,23,232,154)
    reference=Image.open(baseline/'step_003.png').convert('RGB').crop(crop).tobytes();keyboard_step=None;phase_differences={}
    # Both recorded frames are unchanged-input holds after the same native
    # waitHold. Match the entire crop, including its animated cursor; do not
    # mask a rectangle or bless unmatched pixels as animation.
    for step in (3,4):
        phase=(weak/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if struct.unpack_from('<I',phase,0xFA4C)[0]!=end+11 or struct.unpack_from('<I',phase,0xFA50)[0]!=pool or phase[0xFA21]!=29:raise ValueError('keyboard hold changed dialogue state')
        actual=Image.open(weak/f'step_{step:03}.png').convert('RGB').crop(crop).tobytes()
        phase_differences[step]=sum(actual[i:i+3]!=reference[i:i+3] for i in range(0,len(actual),3))
        if actual==reference and keyboard_step is None:keyboard_step=step
    if keyboard_step is None:raise ValueError('unchanged native Japanese input UI crop: neither recorded hold matches')
    if len(pages)!=len(units) or (selected_scripts is None and len(pages)!=40) or sum(not p['diagnostic'] for p in pages)!=3:raise ValueError('profile finite coverage')
    outdir=ROOT/outdir;outdir.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(240*5,160*((len(pages)+4)//5)))
    for i,p in enumerate(pages):sheet.paste(Image.open(routes[p['route']][0]/f"step_{p['step']:03}.png"),(i%5*240,i//5*160))
    sheet.save(outdir/'profile_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_literal_units=m['translated_units'],added_units=40,static=checks,normal_runtime_units=[p['unit'] for p in pages if not p['diagnostic']],diagnostic_renderer_units=[p['unit'] for p in pages if p['diagnostic']],pages=pages,native_entry_calls=calls,native_question_to_input_ui_observed=True,limits=['Only script29 selected through normal gameplay. Other37 literals are renderer diagnostics, not native age/answer-selection evidence.','Preschool32 renderer entry bypasses unchanged native age dispatch; no age-branch proof.','Input keyboard remains Japanese. Hangul input/commit/redisplay/persistence/old saves not verified.','Whole-game translation, human wording/style and release QA incomplete.'])
    result.update(added_units=0 if selected_scripts is not None else 40,full_selected40_renderer_coverage=selected_scripts is None,renderer_verified_units=len(pages),input_transition=dict(question_cursor=end,waitHold_cursor=end+11,dialogue_root_retained=True,native_flags=[3605,3606],keyboard_crop=list(crop),keyboard_pixels_identical_to_previous_original_question=True,keyboard_matched_hold_step=keyboard_step,keyboard_hold_different_pixels=phase_differences,keyboard_no_pixels_excluded=True,keyboard_screenshot_sha256=sha((weak/f'step_{keyboard_step:03}.png').read_bytes()),keyboard_baseline_screenshot_sha256=sha((baseline/'step_003.png').read_bytes())))
    (outdir/'profile_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'Profile{len(pages)} font/OBJ/pixel QA PASS; normal3 / diagnostic{len(pages)-3}');return result

if __name__=='__main__':main()
