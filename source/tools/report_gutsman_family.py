"""Finite family29 display coverage and native choices AFTER entry read-alias."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_questions import page_end
from run_gutsman_family import STEM,PREFIX

OUT=ROOT/'analysis/gutsman_family_v1'

def main():
    import report_gutsman_profile as normal
    old=normal.STEM,normal.PREFIX
    try:
        normal.STEM=STEM;normal.PREFIX=PREFIX;regression=normal.main([29],outdir=OUT/'normal_subject_regression')
    finally:normal.STEM,normal.PREFIX=old
    m,rom,e,streams,checks=static(STEM,'667044');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset']
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();units={u['id']:u for u in read(ROOT/next(a for a in m['translation_assets'] if a.get('archive')=='667044')['path'])['units']}
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    pages=[];observed=set();seen=set();routes={};branch_proofs=[];environments=[]
    def proof(path,step,script,indices,choice=False,nick=False):
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();actual=ram[0xFA21];keys=[f'667044:{script}:{i}' for i in indices]
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or actual!=(script if script%2==0 else 29):raise ValueError('family display root/context script')
        selected=[s for k in keys for s in streams[k]];obs=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
        if set(last)!=set(selected):raise ValueError('family incomplete page glyphs')
        draws=[last[s] for s in selected];expected=dict(e);nickname=None
        if nick:
            native={d['stream']:d for d in read(path/(cp+'_family_ram.json'))['draws']};ordered=[native[s] for s in sorted(native)];offset=0;nickname=''
            if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xe5:raise ValueError('family nickname span/terminator')
            for d in ordered:
                index=ram[d['stream']-0x02000000];record=source[0x608758+index*96:0x608758+(index+1)*96]
                if index!=d['glyph_index'] or index not in codes or d['context']!=0x0200FA20 or d['offset']!=offset or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record:raise ValueError('family native nickname glyph/geometry')
                expected[d['stream']]=dict(ch=codes[index],index=index,record=record,id='native_RAM_nickname');nickname+=codes[index];offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
            if last[selected[0]]['offset']!=offset or e[selected[0]]['ch']!='、':raise ValueError('family particle-free nickname suffix')
            draws=ordered+draws
        reads={x['index']:x['reads'] for x in obs['font_reads']};counts=Counter(expected[d['stream']]['index'] for d in draws)
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('family CPU font reads')
        result=pixels(path,step,draws,expected,rom,m,cursor_screen_background=choice);rects=[];im=Image.open(path/(cp+'.png')).convert('RGB')
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        cursor=None
        if choice:
            a,b,k=struct.unpack_from('<HHH',(path/(cp+'_gbaSpriteRam.bin')).read_bytes(),0);cursor=b&511
            if a&255!=108 or k&1023!=1020 or k>>12!=14:raise ValueError('family choice cursor sprite')
            rects.append((cursor,108,cursor+16,124));offset=24*4
            for key in keys:
                for stream in streams[key]:
                    if last[stream]['offset']!=offset:raise ValueError('family choice labels native spacing')
                    offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
                offset+=8*4
        else:
            cursor_at=struct.unpack_from('<I',ram,0xFA4C)[0]
            if cursor_at!=page_end(rom,selected):raise ValueError('family full page must stop at keyWait')
        blank={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)}
        if any(im.getpixel(p)!=im.getpixel((233,110)) for p in blank):raise ValueError('family stale page pixels')
        pages.append(dict(route=path.name,step=step,script=script,units=keys,nickname=nickname,choice_cursor_x=cursor,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**result));observed.update(keys)
        return cursor
    for script in (1,3,5,7):
        choice_step=6 if script==1 else 5;choice_indices=[4,5] if script==1 else [3,4];last=6 if script==1 else 5
        for branch in ('no','yes')+(('b',) if script==1 else ()):
            path=ROOT/'poc/runtime'/(PREFIX+f'diagnostic-{script}-{branch}');routes[path.name]=path;r=verify_route(path,m['output_sha256'],seen);env=read(path/'profile_environment.json');environments.append(env)
            if not env['passed'] or env['aliases']!=1 or env['displayed_script']!=script or env['requested_script']!=29 or env['rom_sha256']!=m['output_sha256'] or env['age_dispatch_skipped_bytes']!=0 or env['gender_dispatch_skipped_bytes']!=0 or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('family diagnostic scope/quarantine')
            for field,filename in [('tool_sha256','capture_gutsman_profile_diagnostic.py'),('observer_sha256','capture_roll_family.py'),('probe_sha256','capture_roll_pet.py')]:
                if env[field]!=sha((ROOT/'tools'/filename).read_bytes()):raise ValueError('family observer identity')
            if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('family emulator identity')
            initial=proof(path,choice_step,script,choice_indices,choice=True)
            if branch=='no':
                for step in range(2,choice_step):proof(path,step,script,[step-2],nick=step==choice_step-1)
                moves=[proof(path,choice_step+i,script,choice_indices,choice=True) for i in (1,2,3)]
                if not initial==moves[1]<moves[0]==moves[2]:raise ValueError('family defaultYes/rightNo/leftYes/rightNo')
                proof(path,choice_step+4,script+1,[0]);proof(path,choice_step+5,script+1,[0])
                branch_proofs.append(dict(script=script,branch='No',default_cursor=initial,moves=moves,native_response_script=script+1))
            elif branch=='b':
                proof(path,choice_step+1,script+1,[0]);proof(path,choice_step+2,script+1,[0])
                branch_proofs.append(dict(script=script,branch='B',native_response_script=script+1,observed_BSeparate_false_behavior='No response; third select target is not evidence of B continuation'))
            else:
                proof(path,choice_step+1,script,[last]);proof(path,choice_step+2,script,[last])
                end=page_end(rom,streams[f'667044:{script}:{last}'])
                if rom[end-0x08000000:end-0x08000000+11]!=bytes.fromhex('e600f1e900150ee900160e'):raise ValueError('family input initialization source flags')
                branch_proofs.append(dict(script=script,branch=branch,native_name_prompt=True,stopped_before_input_init=True))
    prior={u['id'] for u in read(ROOT/'translations/gutsman_profile_questions_ko.json')['units']};new=set(units)-prior
    if observed!=new or len(new)!=29:raise ValueError('family new29 finite coverage')
    OUT.mkdir(parents=True,exist_ok=True);unique={}
    for p in pages:unique.setdefault(tuple(p['units']),p)
    sheet=Image.new('RGB',(1200,160*((len(unique)+4)//5)))
    for i,p in enumerate(unique.values()):sheet.paste(Image.open(routes[p['route']]/f"step_{p['step']:03}.png"),(i%5*240,i//5*160))
    sheet.save(OUT/'family_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_literal_units=m['translated_units'],added_units=29,static=checks,new_units_normal_runtime_verified=[],new_units_diagnostic_renderer_verified=sorted(observed),normal_subject_regression_units=regression['normal_runtime_units'],pages=pages,diagnostic_environments=environments,branch_proofs=branch_proofs,all_diagnostics_stopped_before_input_init=True,limits=['Entry to four sibling questions was read-aliased from normal29; native Yes/No and script1 B branches then executed. NOT proof of normal sibling selection or stored family names.','Native Japanese nickname retained; no Hangul typing/edit/commit/redisplay/persistence/old-save compatibility proof.','Other profile text runtime not automatically inherited; previous81 wording/scripts byte identity checked separately. Whole game and human review incomplete.'])
    (OUT/'family_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Family29 font/OBJ/pixels, four Yes/No and script1 B: PASS');return result

if __name__=='__main__':main()
