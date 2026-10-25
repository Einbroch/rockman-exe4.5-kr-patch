"""Fixed40 prose evidence; dynamic stored buffers explicitly NOT covered."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_questions import page_end
from run_gutsman_answers import STEM,PREFIX

OUT=ROOT/'analysis/gutsman_answers_v1'

def main():
    import report_gutsman_profile as normal
    old=normal.STEM,normal.PREFIX
    try:
        normal.STEM=STEM;normal.PREFIX=PREFIX;regression=normal.main([29],outdir=OUT/'normal_subject_regression')
    finally:normal.STEM,normal.PREFIX=old
    m,rom,e,streams,checks=static(STEM,'667044');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset']
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    pages=[];observed=set();seen=set();routes={};environments=[];branches=[]
    def route(script,branch):
        path=ROOT/'poc/runtime'/(PREFIX+f'diagnostic-{script}-{branch}');r=verify_route(path,m['output_sha256'],seen);env=read(path/'profile_environment.json')
        if not env['passed'] or env['aliases']!=1 or env['displayed_script']!=script or env['requested_script']!=29 or env['rom_sha256']!=m['output_sha256'] or env['age_dispatch_skipped_bytes'] or env['gender_dispatch_skipped_bytes'] or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('answers diagnostic scope/quarantine')
        for field,filename in [('tool_sha256','capture_gutsman_profile_diagnostic.py'),('observer_sha256','capture_roll_family.py'),('probe_sha256','capture_roll_pet.py')]:
            if env[field]!=sha((ROOT/'tools'/filename).read_bytes()):raise ValueError('answers observer identity')
        if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('answers emulator identity')
        routes[path.name]=path;environments.append(env);return path
    def proof(path,step,script,indices,choice=False,nick=False):
        cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();keys=[f'667044:{script}:{i}' for i in indices]
        actual=script if script in (42,45,48,51,54,57,60,63) else 29
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=actual:raise ValueError('answers root/context')
        selected=[s for k in keys for s in streams[k]];obs=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
        if set(last)!=set(selected):raise ValueError('answers incomplete glyph page')
        draws=[last[s] for s in selected];expected=dict(e);nickname=None
        if nick:
            native={d['stream']:d for d in read(path/(cp+'_family_ram.json'))['draws']};ordered=[native[s] for s in sorted(native)];offset=0;nickname=''
            if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xe5:raise ValueError('answers nickname span')
            for d in ordered:
                index=ram[d['stream']-0x02000000];record=source[0x608758+index*96:0x608758+(index+1)*96]
                if index!=d['glyph_index'] or index not in codes or d['context']!=0x0200FA20 or d['offset']!=offset or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record:raise ValueError('answers native nickname geometry')
                expected[d['stream']]=dict(ch=codes[index],index=index,record=record,id='native_RAM_nickname');nickname+=codes[index];offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
            if last[selected[0]]['offset']!=offset or e[selected[0]]['ch']!='、':raise ValueError('answers nickname suffix')
            draws=ordered+draws
        counts=Counter(expected[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('answers CPU font reads')
        result=pixels(path,step,draws,expected,rom,m,cursor_screen_background=choice);rects=[];im=Image.open(path/(cp+'.png')).convert('RGB')
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        cursor=None
        if choice:
            a,b,k=struct.unpack_from('<HHH',(path/(cp+'_gbaSpriteRam.bin')).read_bytes(),0);cursor=b&511
            if a&255!=136 or k&1023!=1020 or k>>12!=14:raise ValueError('answers row2 cursor')
            rects.append((cursor,136,cursor+16,152))
            offset=0
            for stream in streams[keys[0]]:
                if last[stream]['offset']!=offset:raise ValueError('answers prompt geometry')
                offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
            offset=2*10752+32*4
            for key in keys[1:]:
                for stream in streams[key]:
                    if last[stream]['offset']!=offset:raise ValueError('answers option geometry')
                    offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
                offset+=8*4
        else:
            end=page_end(rom,selected)
            if struct.unpack_from('<I',ram,0xFA4C)[0]!=end:raise ValueError('answers keyWait boundary')
            if nick and rom[end-0x08000000:end-0x08000000+5]!=bytes.fromhex('e600f1f90c'):raise ValueError('prefix must stop before native buffer producer/consumer')
        blank={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)}
        if any(im.getpixel(p)!=im.getpixel((233,110)) for p in blank):raise ValueError('answers stale page pixels')
        pages.append(dict(route=path.name,step=step,script=script,units=keys,nickname=nickname,choice_cursor_x=cursor,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**result));observed.update(keys);return cursor
    for prefix in (40,43,46,49,52,55,58,61):
        p=route(prefix,'prefix');proof(p,2,prefix,[0],nick=True)
        choice=prefix+1;p=route(choice,'no');initial=proof(p,2,choice,[0,1,2],choice=True)
        moves=[proof(p,i,choice,[0,1,2],choice=True) for i in (3,4,5)]
        if not initial==moves[1]<moves[0]==moves[2]:raise ValueError('answers Yes/No cursor movement')
        proof(p,6,choice+1,[0]);proof(p,7,choice+1,[0]);branches.append(dict(script=choice,branch='No',native_response_script=choice+1,default_cursor=initial,moves=moves))
        if choice==41:
            p=route(choice,'b');proof(p,2,choice,[0,1,2],choice=True);proof(p,3,42,[0]);proof(p,4,42,[0]);branches.append(dict(script=41,branch='B',native_response_script=42))
    child=read(ROOT/'translations/gutsman_profile_answers_ko.json');prior={u['id'] for u in read(ROOT/'translations/gutsman_profile_family_checked_ko.json')['units']};new={u['id'] for u in child['units']}-prior
    if len(new)!=40 or new!=observed:raise ValueError('answers fixed40 finite coverage')
    OUT.mkdir(parents=True,exist_ok=True);unique={}
    for p in pages:unique.setdefault(tuple(p['units']),p)
    sheet=Image.new('RGB',(1200,160*((len(unique)+4)//5)))
    for i,p in enumerate(unique.values()):sheet.paste(Image.open(routes[p['route']]/f"step_{p['step']:03}.png"),(i%5*240,i//5*160))
    sheet.save(OUT/'answer_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_literal_units=m['translated_units'],added_units=40,static=checks,new_units_normal_runtime_verified=[],new_units_diagnostic_renderer_verified=sorted(observed),normal_subject_regression_units=regression['normal_runtime_units'],pages=pages,diagnostic_environments=environments,branch_proofs=branches,all_diagnostics_stopped_before_input_init=True,dynamic_stored_answer_buffer_pages_verified=[],limits=['Fixed40 prose only. Entry read-aliased from normal29, then eight native No responses and script41 B. No normal family/friend/hobby/TV/wishlist redisplay selection proof.','Prefix pages stop before printStringBuffer1/2/3. No fabricated answer RAM. Dynamic input/write/commit/read provenance and Hangul input/edit/save/reload/old-save compatibility remain unresolved.','Native Japanese keyboard retained. Previous110 preserved statically, not all re-executed. Whole game/human/release review incomplete.'])
    (OUT/'answer_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Fixed answer40 renderer, eight No and one B: PASS');return result

if __name__=='__main__':main()
