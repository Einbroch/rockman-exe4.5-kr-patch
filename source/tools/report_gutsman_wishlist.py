"""Last3 fixed literals, not natural wishlist selection or input storage."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_questions import page_end
from tpl_literals import literals
from run_gutsman_wishlist import STEM,PREFIX

OUT=ROOT/'analysis/gutsman_wishlist_v1'

def main():
    import report_gutsman_profile as normal
    old=normal.STEM,normal.PREFIX
    try:
        normal.STEM=STEM;normal.PREFIX=PREFIX;regression=normal.main([29],outdir=OUT/'normal_subject_regression')
    finally:normal.STEM,normal.PREFIX=old
    m,rom,e,streams,checks=static(STEM,'667044');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset']
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    child=read(ROOT/'translations/gutsman_profile_wishlist_ko.json');all_units={u['id'] for u in child['units']}
    tpl=(ROOT/'analysis/full_scope_v1/source_tpl/667044.tpl').read_text(encoding='utf-8-sig')
    if all_units!={u.key for u in literals(tpl)} or len(all_units)!=153:raise ValueError('entire fixed-literal archive denominator')
    path=ROOT/'poc/runtime'/(PREFIX+'diagnostic-31');r=verify_route(path,m['output_sha256'],set());env=read(path/'profile_environment.json')
    if not env['passed'] or env['aliases']!=1 or env['displayed_script']!=31 or env['requested_script']!=29 or env['rom_sha256']!=m['output_sha256'] or env['age_dispatch_skipped_bytes'] or env['gender_dispatch_skipped_bytes'] or r.get('normal_play_checkpoint_eligible') is not False or (path/'checkpoint.mss').exists() or 'diagnostic_checkpoint.mss' not in r['artifacts']:raise ValueError('wishlist diagnostic quarantine')
    for field,filename in [('tool_sha256','capture_gutsman_profile_diagnostic.py'),('observer_sha256','capture_roll_family.py'),('probe_sha256','capture_roll_pet.py')]:
        if env[field]!=sha((ROOT/'tools'/filename).read_bytes()):raise ValueError('wishlist observer identity')
    if r['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('wishlist emulator identity')
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    pages=[]
    for literal,step in enumerate((2,3,4)):
        key=f'667044:31:{literal}';selected=streams[key];cp=f'step_{step:03}';ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(path/(cp+'_roll_pet.json'));last={d['stream']:d for d in obs['draws'] if d['stream'] in selected}
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=29 or set(last)!=set(selected):raise ValueError('wishlist root/context/page glyphs')
        expected=dict(e);draws=[last[s] for s in selected];nickname=None
        if literal==2:
            native={d['stream']:d for d in read(path/(cp+'_family_ram.json'))['draws']};ordered=[native[s] for s in sorted(native)];offset=0;nickname=''
            if not ordered or sorted(native)!=list(range(ordered[0]['stream'],ordered[0]['stream']+len(ordered))) or ram[ordered[0]['stream']-0x02000000+len(ordered)]!=0xe5:raise ValueError('wishlist nickname span/terminator')
            for d in ordered:
                index=ram[d['stream']-0x02000000];record=source[0x608758+index*96:0x608758+(index+1)*96]
                if index!=d['glyph_index'] or index not in codes or d['context']!=0x0200FA20 or d['offset']!=offset or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record:raise ValueError('wishlist nickname geometry/font')
                expected[d['stream']]=dict(ch=codes[index],index=index,record=record,id='native_RAM_nickname');nickname+=codes[index];offset+=4*struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
            if last[selected[0]]['offset']!=offset or e[selected[0]]['ch']!='、':raise ValueError('wishlist nickname suffix')
            draws=ordered+draws
        reads={x['index']:x['reads'] for x in obs['font_reads']};counts=Counter(expected[d['stream']]['index'] for d in draws)
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('wishlist CPU font reads')
        proof=pixels(path,step,draws,expected,rom,m);im=Image.open(path/(cp+'.png')).convert('RGB');rects=[]
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];rects.append((x,y,x+w,y+12))
        blank={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138) and not any(a<=x<c and b<=y<d for a,b,c,d in rects)}
        if any(im.getpixel(p)!=im.getpixel((233,110)) for p in blank):raise ValueError('wishlist stale page pixels')
        end=page_end(rom,selected)
        if struct.unpack_from('<I',ram,0xFA4C)[0]!=end:raise ValueError('wishlist keyWait boundary')
        if literal==2 and rom[end-0x08000000:end-0x08000000+13]!=bytes.fromhex('e600f1e900150ee900160eedff'):raise ValueError('wishlist source input-init flags/waitHold')
        pages.append(dict(unit=key,step=step,nickname=nickname,keyWait_cursor=end,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((path/(cp+'.png')).read_bytes()),**proof))
    OUT.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,p in enumerate(pages):sheet.paste(Image.open(path/f"step_{p['step']:03}.png"),(i*240,0))
    sheet.save(OUT/'wishlist_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_literal_units=m['translated_units'],added_units=3,static=checks,entire_fixed_archive_selected=True,fixed_archive_literal_units=153,new_units_normal_runtime_verified=[],new_units_diagnostic_renderer_verified=[p['unit'] for p in pages],normal_subject_regression_units=regression['normal_runtime_units'],pages=pages,diagnostic_environment=env,all_diagnostics_stopped_before_input_init=True,limits=['Wishlist31 entry is a quarantined read-alias from normal29. Fixed3 display and unchanged controls only, NOT natural wishlist selection/input/commit/persistence.','All153 fixed literals selected does not cover dynamic buffers, Japanese keyboard, all native branches or Hangul user strings. Whole-game/human/release review incomplete.'])
    (OUT/'wishlist_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Wishlist3 exact renderer/nickname/input-boundary PASS; all153 fixed archive literals selected');return result

if __name__=='__main__':main()
