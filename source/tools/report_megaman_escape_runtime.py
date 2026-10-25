"""Exact750-unit build: bounded native/diagnostic escape and folder evidence."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from report_chip_library_runtime import read,require,bdf_cells
from report_fixedcell_runtime import verify_route
from report_chip_folder_pixels import visible_folder
from report_chip_mono_cannon_runtime import mono_sentence
from archive_scripts import script_spans,verify_untouched_scripts
from tpl_literals import resolve_units
from korean_codec import encode_character
from prepare_megaman_escape import prepare as prepare_asset

STEM='exe45_ko_development_megaman_escape_v1'
PREFIX='poc/runtime/megaman-escape-v1-'

def choice_cursor(p,step,shot):
    """Bind observed native cursor region, not an unproved tile scanout model."""
    oam=(p/f'step_{step:03d}_gbaSpriteRam.bin').read_bytes();video=(p/f'step_{step:03d}_gbaVideoRam.bin').read_bytes()
    palette=(p/f'step_{step:03d}_gbaPaletteRam.bin').read_bytes();io=(p/f'step_{step:03d}_display_io.bin').read_bytes()
    a0,a1,a2=struct.unpack_from('<HHH',oam);x=a1&511;y=a0&255
    require(a0==122 and a1==0x4000+(121 if step in (4,6) else 85) and a2==0xE3FC,'native choice cursor focus/format')
    require(struct.unpack_from('<H',io)[0]&64,'choice OBJ 1D tile mapping')
    pixels={};colors={};background=(248,236,212)
    for yy in range(16):
        for xx in range(16):
            tile=1020+(yy//8)*2+xx//8;byte=video[0x10000+tile*32+(yy%8)*4+(xx%8)//2];role=(byte>>(4*(xx%2)))&15
            color=shot.getpixel((x+xx,y+yy))
            if color==background:continue
            colors[str(color)]=colors.get(str(color),0)+1;pixels[x+xx,y+yy]=color
    require(pixels and len(colors)>=2,'empty/native cursor region')
    return pixels,{'oam_index':0,'x':x,'y':y,'tile':1020,'palette':14,'width':16,'height':16,'observed_nonbackground_pixels':len(pixels),
        'observed_rgb_counts':colors,'tile_snapshot_sha256':sha(video[0x17F80:0x18000]),'palette_snapshot_sha256':sha(palette[0x3C0:0x3E0]),
        'pixel_roles_verified':False,'limit':'Exact OAM focus/geometry and inspected screenshot only; snapshot cursor tile role masks disagree with scanout and are not credited. Space-padding overlay pixels excluded from text masks; all text ink/shadow still checked.'}

def prepare():
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));build=m['output_sha256'];require_hash(rp,build)
    require_hash(ROOT/f'poc/output/{STEM}_repro.gba',build);rom=rp.read_bytes()
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    require(m['translated_units']==750 and m['unchanged_archives']==725 and m['final_diff_audited'] and m['header_unchanged'],'cumulative750 scope')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    asset=read(ROOT/'translations/megaman_tactics_escape_ko.json');require(asset==prepare_asset(),'draft/protected provenance drift')
    units=resolve_units(asset);ar=next(a for a in m['archives'] if a['archive']=='76C944');base=0x08000000+ar['rom_offset']
    payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    require(ar['translated_units']==8 and len(verify_untouched_scripts(native[0x76C944:0x76C944+4473],payload,144,set(range(6))))==138,'other Navi scripts preserved')
    require(struct.unpack_from('<I',rom,0x212E8)[0]==base,'native Navi root relocation')
    require(all(ar[k] for k in ('native_roundtrip','semantic_roundtrip','binary_roundtrip','protected_controls_unchanged')),'mixed archive roundtrip')
    spans=script_spans(payload,144);codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    ef=m['extension'];font=ef['normal_font_offset'];bias=ef['legacy_index_view']
    wanted={c for u in units[2:] for c in u['translation'] if '\uac00'<=c<='\ud7a3'}
    glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted)
    expected={};by_script={}
    for u in units[2:]:
        script=int(u['id'].split(':')[1]);text=u['translation'];encoded=b''.join(b'\xe8' if c=='\n' else encode_character(c) if c in wanted else codes[c] for c in text)
        require(spans[script].count(encoded)==1,'literal encoding/source identity')
        start=base+struct.unpack_from('<H',payload,script*2)[0]+spans[script].index(encoded)
        cursor=start;records=[]
        for c in text:
            if c=='\n':cursor+=1;continue
            data=encode_character(c) if c in wanted else codes[c]
            require(c in wanted or len(data)==1,'unsupported native normal glyph code')
            index=ord(c)-0xAC00+bias if c in wanted else data[0]
            record=rom[font+index*96:font+(index+1)*96]
            if c in wanted:require(record==glyphs[c],'ROM/BDF normal glyph mismatch')
            else:require(record==native[0x608758+index*96:0x608758+(index+1)*96],'native glyph changed')
            expected[cursor]={'id':u['id'],'character':c,'index':index,'record':record};records.append(cursor);cursor+=len(data)
        by_script.setdefault(script,[]).extend(records)
    seen=set();routes={};pages={}
    # These coordinates/role colors apply only to inspected battle dialogue pages.
    # Roles1/3 cross-check with native punctuation, shadow2 is observed per page.
    colors={1:(248,236,212),2:(208,207,174),3:(20,16,17)}
    for name,script,steps,diagnostic in [('l-target',5,[2,3],False),('confirm-sample',2,[2,3,4,5,6],True),
            ('success-sample',3,[2,3],True),('failure-sample',4,[2,3],True)]:
        p=ROOT/(PREFIX+name);r=verify_route(p,build,seen);routes[name]={'receipt_sha256':sha((p/'result.json').read_bytes()),'diagnostic':diagnostic}
        env=read(p/'escape_environment.json');require(env['passed'] and env['rom_sha256']==build,'escape observer')
        require_hash(ROOT/'tools/capture_megaman_escape.py',env['tool_sha256'])
        require(5 in env['selected_scripts'],'native escape forbidden selector not reached')
        if diagnostic:
            a=read(p/'escape_alias_environment.json');require(a['passed'] and a['displayed_script']==script and a['native_script']==5 and a['reads']==1 and r['normal_play_checkpoint_eligible'] is False,'diagnostic selector/quarantine')
            require_hash(ROOT/'tools/capture_megaman_escape_samples.py',a['tool_sha256']);require_hash(ROOT/'tools/capture_megaman_escape.py',a['observer_sha256'])
        else:require(r.get('normal_play_checkpoint_eligible',True),'normal route mislabeled')
        for step in steps:
            require(step in r['capture_steps'],'missing escape screenshot')
            state=read(p/f'step_{step:03d}_escape.json');draws=[d for d in state['draws'] if d['stream'] in by_script[script]]
            require([d['stream'] for d in draws]==by_script[script],'normal dialogue stream order/coverage')
            reads={d['index']:d['reads'] for d in state['font_reads']};counts=Counter(expected[d['stream']]['index'] for d in draws)
            require(all(reads.get(i,0)>=24*n for i,n in counts.items()),'normal font supply/read coverage')
            shot=Image.open(p/f'step_{step:03d}.png').convert('RGB');cells=[];native_roles=set()
            overlay,cursor=choice_cursor(p,step,shot) if script==2 else ({},None)
            for d in draws:
                g=expected[d['stream']];require(d['glyph_index']==g['index'] and d['offset']%4==0,'normal renderer glyph/cursor')
                row,off=divmod(d['offset'],10752);x=52+off//4;y=110+row*14
                width=12 if g['character'] in wanted else struct.unpack_from('<I',rom,ef['advance_offset']+g['index']*4)[0]
                require(0<=row<=1 and x+width<=236 and y+12<=140,'battle dialogue bounds')
                overlay_count=0
                for yy in range(12):
                    for xx in range(width):
                        role=(g['record'][yy*8+xx//2]>>(4*(xx%2)))&15
                        at=(x+xx,y+yy);target=colors.get(role)
                        if at in overlay and g['character']==' ':
                            require(role==1,'cursor covers text ink/shadow')
                            target=overlay[at];overlay_count+=1
                        require(target is not None and shot.getpixel(at)==target,f'normal glyph pixel mismatch {name}:{step} {g["character"]!r} {at} role{role} actual{shot.getpixel(at)}')
                        if g['character'] not in wanted:native_roles.add(role)
                cells.append({'character':g['character'],'stream':d['stream'],'index':g['index'],'x':x,'y':y,'width':width,'glyph_sha256':sha(g['record']),'pixel_masks_match':True,'native_choice_cursor_overlay_pixels':overlay_count})
            require({1,3}<=native_roles,'native punctuation role cross-check')
            pages[f'{name}:{step}']={'script':script,'normal_draws':cells,'pixel_masks_match':True,'choice_cursor':cursor,'role_colors':colors,'palette_scope':'observed exact battle pages; native punctuation roles1/3 checked, shadow2 observed; native cursor overlay on source space padding excluded; all text ink/shadow checked; not independent color pipeline or human approval'}
    folder=ROOT/(PREFIX+'folder-regression');fr=verify_route(folder,build,seen);require(read(folder/'folder_qa_environment.json')['passed'],'folder copy/cache/ABI')
    table={int(k,16):v for v,kb in codes.items() if len(kb)==1 for k in [kb.hex()]}
    f=m['fixedcell_extension'];cells=bdf_cells(ROOT/f['font']['path'],set('캐논에어슛발칸'),f['raster']);rows={0:'캐논',1:'캐논',2:'캐논',3:'에어슛',4:'에어슛',5:'에어슛',6:'발칸1'}
    texts={int(u['id'].split(':')[1]):u['translation'] for u in resolve_units(read(ROOT/'translations/chip_descriptions_batch09_ko.json'))}
    folder_pixels={str(step):{'names':visible_folder(folder,step,rows,cells,native,table),'description':mono_sentence(folder,step,m,native,table,texts[i],i,rp)} for step,i in [(9,1),(12,4),(15,15),(16,15)]}
    tactics={};p=ROOT/(PREFIX+'tactics-regression-r2');verify_route(p,build,seen)
    for name,script in [('target',0),('distance',1)]:
        path=ROOT/f'analysis/exe45_escape_tactics_{name}_v1.json';r=read(path)
        require(r['rom_sha256']==build and r['status'].startswith('PASS') and len(r['screens'])==2 and all(s['script']==script and s['pixels_verified'] for s in r['screens']),'tactics regression binding')
        require(r['result_sha256']==sha((p/'result.json').read_bytes()),'tactics receipt binding')
        tactics[name]={'path':str(path.relative_to(ROOT)),'sha256':sha(path.read_bytes()),'screens':r['screens']}
    clear={};before=ROOT/(PREFIX+'battle-tutorial-complete');verify_route(before,build,seen)
    baseline=Image.open(before/'step_104.png').convert('RGB')
    background_mask={(x,y) for x in range(52,236) for y in range(110,138) if baseline.getpixel((x,y))==colors[1]}
    target_ref=ROOT/(PREFIX+'tactics-regression-r2');target_video=(target_ref/'step_006_gbaVideoRam.bin').read_bytes()
    target_shot=Image.open(target_ref/'step_006.png').convert('RGB')
    for name,steps in [('confirm-sample',[7,8]),('success-sample',[4,5]),('failure-sample',[4,5]),('forbidden-clear',[2,3])]:
        p=ROOT/(PREFIX+name);r=verify_route(p,build,seen)
        for step in steps:
            shot=Image.open(p/f'step_{step:03d}.png').convert('RGB')
            mask={(x,y) for x in range(52,236) for y in range(110,138) if shot.getpixel((x,y))==colors[1]}
            require(mask==background_mask,'closed dialogue background mask differs from pre-dialogue scene')
            ew=(p/f'step_{step:03d}_gbaExtWorkRam.bin').read_bytes()
            require(ew[0xFA20]==0,'normal dialogue context remains active after close')
            calls=[c for c in read(p/f'step_{step:03d}_fixedcells.json')['calls'] if c['font']==0x08619EF8]
            stream=base+struct.unpack_from('<H',payload,0)[0]
            if calls:require(calls[-1]['stream']==stream and calls[-1]['complete'] and (calls[-1]['width'],calls[-1]['height'],calls[-1]['bytes'])==(5,2,640),'close returned wrong target parser')
            selections=read(p/f'step_{step:03d}_escape.json')['selections']
            require(selections and selections[-1]['script']==0 and selections[-1]['pool']==base,'close did not select native target prompt')
            video=(p/f'step_{step:03d}_gbaVideoRam.bin').read_bytes()
            require(video[0x8A20:0x8A20+640]==target_video[0x8A20:0x8A20+640],'cached target glyph residency')
            require(all(shot.getpixel((x,y))==target_shot.getpixel((x,y)) for x in range(56,96) for y in range(32,64)),'cached target visible pixels')
            clear[f'{name}:{step}']={'screenshot_sha256':sha((p/f'step_{step:03d}.png').read_bytes()),'normal_dialogue_active':False,
                'background_mask_matches_pre_dialogue_scene':True,'pre_dialogue_scene_same_color_pixels':len(background_mask),
                'baseline_screenshot_sha256':sha((before/'step_104.png').read_bytes()),'returned_target_stream':stream,'normal_play':name=='forbidden-clear',
                'render_event_seen':bool(calls),'resident_target_matches_pixel_verified_regression':True,
                'limit':'Background color mask/context/target return plus inspected screenshot, not full animated battlefield pixel equality.'}
    saves={}
    for p in seen:
        env=read(p/'probe_environment.json')
        require(all(env['files_after'].get(k)==v for k,v in env['files_before'].items() if k not in (STEM+'.sav',STEM+'.rtc')),'foreign save changed')
        saves[str(p.relative_to(ROOT))]={'other_save_files_preserved':True,'own_save':env['files_after'].get(STEM+'.sav'),'own_rtc':env['files_after'].get(STEM+'.rtc')}
    return {'status':'PASS bounded750-unit development escape display and folder regression','policy':'development-draft; NON-DISTRIBUTION','rom_sha256':build,
        'translated_units':750,'new_escape_literals':6,'preserved_other_navi_scripts':138,'reproducible':True,'routes':routes,'escape_pixels':pages,'clear_and_return':clear,'tactics_regression':tactics,'folder_regression':folder_pixels,'saves':saves,
        'limits':['Only forbidden escape script5 is normal-play route evidence; scripts2/3/4 use quarantined native lookup read aliases, not successful/failed real escape outcomes.',
            'Confirmation cursor left/right and No close inspected; real escape Yes/result probabilities and B cancel still pending.',
            'Cursor OAM focus/geometry inspected, but animated cursor tile snapshot masks did not match screenshot scanout; no exact cursor bitmap-pixel claim.',
            'Other Navi prompts/escape dialogue and most dialogue/UI/graphics remain untranslated.',
            'New-ROM secondary-name, library, battle-name and save-commit/reboot/lifetime/timing regressions not inherited from prior ROM.',
            'Wording/presentation human approval, complete playthrough, audio, hardware and release QA remain pending.']}

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
