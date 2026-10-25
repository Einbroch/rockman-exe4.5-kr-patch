"""Native unregistered tournament/name consumer and exact-ROM regression."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,static,pixels,verify_route
from report_gutsman_pet import main as pet_regression
from report_roll_pet_license import literal_end
from run_gutsman_competition import STEM,PREFIX

def main():
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2229,53,679),oldstem='exe45_ko_development_gutsman_operations_v1',outdir='gutsman_competition_v1/pet_regression',inventory_outdir='full_scope_gutsman_competition_v1',added_literal_units=0)
    m,rom,e,streams,checks=static(STEM,'666D5C');ar=next(a for a in m['archives'] if a['archive']=='666D5C');pool=0x8000000+ar['rom_offset'];petpool=0x8000000+next(a for a in m['archives'] if a['archive']=='665F3C')['rom_offset'];source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();rt=ROOT/'poc/runtime';seen=set()
    for name,parent in [('tournament-prompt','select-gutsman'),('unregistered','tournament-prompt')]:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],seen)
        if r['state_origin']!=str(rt/(PREFIX+parent)/'result.json') or r.get('normal_play_checkpoint_eligible') is False or any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('normal ancestry/intervention')
    prompt=rt/(PREFIX+'tournament-prompt');rr=(prompt/'step_003_gbaExtWorkRam.bin').read_bytes()
    if rr[0xFA21]!=2 or struct.unpack_from('<I',rr,0xFA50)[0]!=petpool:raise ValueError('native PET2 question')
    p=rt/(PREFIX+'unregistered');key='666D5C:10:0';unit=next(u for u in read(ROOT/'translations/gutsman_competition_ko.json')['units'] if u['id']==key);pages=[]
    codes={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    native_advance=read(ROOT/'tools/specs/exe45_dialogue_extension_v1.json')['advance_literal']['expected_address']&0x1ffffff
    for step in [2,3]:
        cp=f'step_{step:03}';r=(p/(cp+'_gbaExtWorkRam.bin')).read_bytes();obs=read(p/(cp+'_roll_pet.json'));calls=obs['calls']
        if r[0xFA21]!=10 or struct.unpack_from('<I',r,0xFA50)[0]!=pool or len(calls)!=1 or calls[0]['root']!=pool or calls[0]['script']!=10:raise ValueError('native unregistered entry')
        last={d['stream']:d for d in obs['draws'] if d['stream'] in streams[key]}
        if set(last)!=set(streams[key]):raise ValueError('complete literal')
        native=read(p/(cp+'_return_ram.json'))['draws'];native=list({d['stream']:d for d in native}.values());native.sort(key=lambda d:d['stream']);expected=dict(e)
        # Capture the nickname actually supplied by this own normal profile.
        # A prior ROM's ああくん fixture is not this run's input contract.
        if len(native)!=4 or r[native[0]['stream']-0x2000000+len(native)]!=0xE5:raise ValueError('own native nickname span/terminator')
        nickname='';nickname_width=0
        for i,d in enumerate(native):
            index=r[d['stream']-0x2000000];record=source[0x608758+index*96:0x608758+(index+1)*96]
            advance=struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]
            if d['stream']!=native[0]['stream']+i or d['glyph_index']!=index or d['offset']!=nickname_width*4 or d['context']!=0x0200FA20 or index not in codes or rom[m['extension']['normal_font_offset']+index*96:m['extension']['normal_font_offset']+(index+1)*96]!=record or advance!=struct.unpack_from('<I',source,native_advance+index*4)[0]:raise ValueError('native nickname font/geometry')
            expected[d['stream']]=dict(ch='native nickname',index=index,record=record,id='native_RAM_nickname')
            nickname+=codes[index];nickname_width+=advance
        if nickname_width!=44:raise ValueError('tested native nickname width')
        row=0;advance=nickname_width;it=iter(streams[key])
        for ch in unit['translation']:
            if ch=='\n':row+=1;advance=0;continue
            stream=next(it)
            if last[stream]['offset']!=row*10752+advance*4:raise ValueError('combined nickname/literal geometry')
            advance+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[stream]['index']*4)[0]
        end=literal_end(rom,streams[key],e)
        if struct.unpack_from('<I',r,0xFA4C)[0]!=end or rom[end-0x8000000:end-0x8000000+3]!=bytes.fromhex('e600f1'):raise ValueError('native keyWait boundary')
        draws=[last[s] for s in streams[key]]+native;counts=Counter(d['glyph_index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('CPU glyph reads')
        proof=pixels(p,step,draws,expected,rom,m);occupied=set();im=Image.open(p/(cp+'.png')).convert('RGB')
        for d in draws:
            row,off=divmod(d['offset'],10752);x=92+off//4;y=110+row*14;w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+d['glyph_index']*4)[0];occupied.update((xx,yy) for yy in range(y,y+12) for xx in range(x,x+w))
        blank={(x,y) for y in range(110,150) for x in range(92,234) if (x,y) not in occupied and not(x>=224 and y>=138)}
        if {im.getpixel(xy) for xy in blank}!={im.getpixel((233,110))}:raise ValueError('native vacant text clearing')
        pages.append(dict(step=step,unit=key,native_nickname=nickname,nickname_width=nickname_width,native_nickname_bytes=r[native[0]['stream']-0x2000000:native[0]['stream']-0x2000000+5].hex(),native_entry=calls,wait_cursor=end,vacant_pixels_cleared=len(blank),screenshot_sha256=sha((p/(cp+'.png')).read_bytes()),**proof))
    for step in [4,5]:
        r=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if r[0xFA21]!=1 or struct.unpack_from('<I',r,0xFA50)[0]!=petpool:raise ValueError('native cancel menu return')
    final=read(p/'step_005_roll_pet.json')
    if final['calls']!=read(p/'step_003_roll_pet.json')['calls'] or final['draws']!=read(p/'step_003_roll_pet.json')['draws']:raise ValueError('unregistered draw lifetime')
    out=ROOT/'analysis/gutsman_competition_v1';out.mkdir(parents=True,exist_ok=True);Image.open(p/'step_003.png').save(out/'normal_unregistered.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=10,selected_text_units=2229,static=checks,native_competition_binding=dict(root_offset=0x3812C,rom_pointer=pool),pet_regression=baseline,normal_pages=pages,normal_runtime_units=[key],static_only_units=sorted(set(streams)-{key}),native_menu_return_steps=[4,5],draws_stopped_after_page=True,remaining_catalog=baseline['remaining_catalog'],limits=['Only native GutsMan unregistered10 with captured own source-native nickname. Defeat/victory/encouragement other9 literals and arbitrary nickname population static-only.','Own NumberMan save/cold continue/3pages,Guts intro2/PET8scenes22units regression. No actual tournament participation/win/loss/live communication/Guts save proof.','Prior52 payloads/graphics identical; this ROM does not rerun previous Jack-In/mail/return/seasonal paths.','Whole text/graphics/inline/fixed populations and Hangul name input/committed records/all redisplays/persistence/old-save compatibility unresolved; prior wait-arrow53pixel difference open; human wording review pending; no release.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts competition10 static / native unregistered+nickname / PET return PASS');return result
if __name__=='__main__':main()
