"""Exact common-confirmation artifact, normal UI/font/pixels and record transitions."""
import json,struct
from collections import Counter
from PIL import Image
from report_roll_pet import ROOT,read,sha,require_hash,pixels,bdf_glyphs
from archive_scripts import script_spans
from korean_codec import encode_character
from input_confirmation import validate,CHILD,IDS
from keyitem_rom_data import verify_final
from run_input_confirmation import STEM,PREFIX
OUT=ROOT/'analysis/input_confirmation_v1'
OLD='exe45_ko_development_gutsman_wishlist_v1_r2'

def static():
    m=read(ROOT/f'poc/output/{STEM}.json');rp=ROOT/f'poc/output/{STEM}.gba';require_hash(rp,m['output_sha256']);rom=rp.read_bytes();require_hash(ROOT/f'poc/output/{STEM}_repro.gba',m['output_sha256'])
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);src=source.read_bytes();rebuilt=bytearray(src);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];value=bytes.fromhex(w['final_hex'])
        if len(value)!=n or src[at:at+n]!=bytes.fromhex(w['expected_hex']) or occupied.intersection(range(at,at+n)):raise ValueError('immutable write ledger')
        occupied.update(range(at,at+n));rebuilt[at:at+n]=value
    if rebuilt!=rom[:len(src)] or rom[:192]!=src[:192] or len(rom)!=len(src)+m['append_bytes'] or sha(rom[len(src):])!=m['append_sha256']:raise ValueError('header/ledger/append')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    asset=read(ROOT/CHILD);validate(asset);om=read(ROOT/f'poc/output/{OLD}.json');prior=(ROOT/f'poc/output/{OLD}.gba').read_bytes();require_hash(ROOT/f'poc/output/{OLD}.gba',om['output_sha256'])
    before={a['archive']:a for a in om['archives']};after={a['archive']:a for a in m['archives']}
    if set(before)!=set(after) or m['translated_units']!=om['translated_units']+3:raise ValueError('selected population')
    ar=after['6368E8'];oa=before['6368E8'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];sp=script_spans(payload,255);osp=script_spans(prior[oa['rom_offset']:oa['rom_offset']+oa['compiled_bytes']],255)
    if ar['translated_units']!=16 or any(sp[i]!=osp[i] for i in range(255) if i!=10) or not all(ar[k] for k in ['protected_controls_unchanged','binary_roundtrip','semantic_roundtrip']):raise ValueError('only script10 / protected controls')
    if rom[0x6368e8:0x6368e8+2337]!=src[0x6368e8:0x6368e8+2337] or sha(src[0x6368e8:0x6368e8+2337])!=asset['source_archive_sha256']:raise ValueError('retained original common archive')
    root=0x08000000+ar['rom_offset']
    if len(ar['pointers'])!=15 or any(struct.unpack_from('<I',rom,p)[0]!=root for p in ar['pointers']):raise ValueError('all15 common roots')
    for name,a in before.items():
        b=after[name]
        if name!='6368E8' and prior[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']]:raise ValueError('prior payload drift '+name)
    for a in om['translation_assets']:
        if not any(a['path'].replace('\\','/')==b['path'].replace('\\','/') and a['sha256']==b['sha256'] for b in m['translation_assets']):raise ValueError('prior input lost')
    font=m['extension']['normal_font_offset'];advance=m['extension']['advance_offset'];of=om['extension']['normal_font_offset'];ov=om['extension']['advance_offset'];count=m['extension']['legacy_index_view']+m['extension']['hangul_syllables']+m['extension']['extra_glyph_count']
    if rom[font:advance]!=prior[of:ov] or rom[advance:advance+count*4]!=prior[ov:ov+count*4]:raise ValueError('normal font/advance drift')
    for key in ['calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics']:
        a,b=om[key],m[key];at=b['source_offset'];n=b.get('stored_bytes',b.get('bytes'))
        if a!=b or prior[at:at+n]!=rom[at:at+n]:raise ValueError('graphics drift')
    a,b=om['folder_labels']['title'],m['folder_labels']['title'];at=b['source_offset'];n=b.get('stored_bytes',b.get('bytes'))
    if a!=b or prior[at:at+n]!=rom[at:at+n]:raise ValueError('folder title graphics drift')
    verify_final(src,rom,m['keyitem_rom']);a,b=om['keyitem_rom'],m['keyitem_rom']
    if prior[a['rom_offset']:a['rom_offset']+a['rom_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['rom_bytes']]:raise ValueError('keyitem39 drift')
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    units=asset['units'][13:];wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'};glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted);expected={};streams={}
    for u in units:
        def encoded(c):return b'\xe8' if c=='\n' else encode_character(c) if c in wanted else codes[c]
        body=b''.join(encoded(c) for c in u['translation'])
        if sp[10].count(body)!=1:raise ValueError('confirmation literal uniqueness')
        cursor=root+struct.unpack_from('<H',payload,20)[0]+sp[10].index(body);ss=[]
        for c in u['translation']:
            if c=='\n':cursor+=1;continue
            data=encoded(c);index=ord(c)-0xac00+m['extension']['legacy_index_view'] if c in wanted else data[0];record=rom[font+index*96:font+(index+1)*96]
            if record!=(glyphs[c] if c in wanted else src[0x608758+index*96:0x608758+(index+1)*96]):raise ValueError('confirmation font supply')
            expected[cursor]=dict(ch=c,index=index,record=record,id=u['id']);ss.append(cursor);cursor+=len(data)
        streams[u['id']]=ss
    return m,rom,root,expected,streams

def main():
    from report_fixedcell_runtime import verify_route
    m,rom,root,e,streams=static();rt=ROOT/'poc/runtime';routes={};snapshots=[]
    for name in ['typed','confirmation','yes','no-settled','cancel','reconfirm-after-no-settled']:
        p=rt/(PREFIX+name);r=verify_route(p,m['output_sha256'],set());routes[name]=r
        if r.get('normal_play_checkpoint_eligible') is False or any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('native route intervention')
        env=read(p/'input_observer_environment.json')
        if env['rom_sha256']!=m['output_sha256'] or not all(env[k] for k in ['observer_only','no_aliases','no_external_RAM_writes']):raise ValueError('observer identity')
        for step in r['capture_steps']:
            ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();snapshots.append(dict(route=name,step=step,record_hex=ram[0x10a6:0x10ad].hex(),editing_hex=ram[0xfc80:0xfc90].hex(),record_destination=struct.unpack_from('<I',ram,0xfc5c)[0],script=ram[0xfa21],root=struct.unpack_from('<I',ram,0xfa50)[0],writes=read(p/f'step_{step:03}_input_writes.json')['writes'],screenshot_sha256=sha((p/f'step_{step:03}.png').read_bytes())))
    pages=[];wanted={s for ss in streams.values() for s in ss}
    for name,step in [('confirmation',1),('no-settled',2),('reconfirm-after-no-settled',2)]:
        p=rt/(PREFIX+name);ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();obs=read(p/f'step_{step:03}_roll_pet.json');last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
        reused=name=='no-settled'
        if reused:
            if routes[name]['state_origin']!=str(rt/(PREFIX+'confirmation')/'result.json') or last:raise ValueError('No focus must reuse native parent glyph state, not fabricate fresh draws')
            obs=read(rt/(PREFIX+'confirmation')/'step_001_roll_pet.json');last={d['stream']:d for d in obs['draws'] if d['stream'] in wanted}
        if set(last)!=wanted or ram[0xfa21]!=10 or struct.unpack_from('<I',ram,0xfa50)[0]!=root:raise ValueError('complete normal confirmation')
        draws=[last[s] for ss in streams.values() for s in ss];counts=Counter(e[d['stream']]['index'] for d in draws);reads={x['index']:x['reads'] for x in obs['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('font CPU reads')
        proof=pixels(p,step,draws,e,rom,m,origin=(52,110),cursor_screen_background=True)
        cursor=struct.unpack_from('<HHH',(p/f'step_{step:03}_gbaSpriteRam.bin').read_bytes(),0)
        if cursor[1]&511!=(101 if reused else 65) or cursor[0]&255!=122:raise ValueError('confirmation Yes/No cursor position')
        pages.append(dict(route=name,step=step,units=sorted(IDS),parent_font_draw_evidence_reused=reused,**proof))
    for s in snapshots:
        if s['route'] in ['typed','confirmation','no-settled','cancel','reconfirm-after-no-settled'] and (s['record_hex']!='007e7e7ee50000' or s['writes']):raise ValueError('cancel/No must not commit record')
    yes=next(s for s in snapshots if s['route']=='yes' and s['step']==1)
    if yes['record_hex']!='019be57ee50000' or yes['script']!=93 or not all(any(w['address']==a and w['value']==v and w['pc']==pc for w in yes['writes']) for a,v,pc in [(0x020010a6,1,0x0803500c),(0x020010a7,155,0x0803501e),(0x020010a8,229,0x08035026)]):raise ValueError('native Yes record writes/reaction93')
    keyboard_returns=[];crop=(8,54,232,130)
    reference=Image.open(rt/(PREFIX+'typed')/'step_005.png').convert('RGB').crop(crop).tobytes()
    for name,step in [('no-settled',3),('cancel',1)]:
        p=rt/(PREFIX+name);ram=(p/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0xfc80:0xfc90]!=bytes.fromhex('9b989898e50000000000000000000000') or Image.open(p/f'step_{step:03}.png').convert('RGB').crop(crop).tobytes()!=reference:raise ValueError('native keyboard restored; edit field retained; confirmation pixels cleared')
        keyboard_returns.append(dict(route=name,step=step,keyboard_body_crop=list(crop),identical_pixels=224*76,editing_buffer_retained=True,scope='Keyboard body begins below entry-box bottom53, includes former dialog text region; top blinking field caret and lower keyboard cursor are separate consumers.'))
    OUT.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(720,160))
    for i,p in enumerate(pages):sheet.paste(Image.open(rt/(PREFIX+p['route'])/f"step_{p['step']:03}.png"),(i*240,0))
    sheet.save(OUT/'confirmation_pages.png')
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],selected_literal_units=m['translated_units'],added_literal_units=3,all15_common_roots_verified=True,parent13_and254_other_common_scripts_preserved=True,prior59_archive_payloads_identical=True,source_ledger_append_and_header_verified=True,font_graphics_keyitem39_preserved=True,normal_runtime_units=sorted(IDS),pages=pages,snapshots=snapshots,limits=['Only normal question29 single Japanese character input; Hangul keyboard/edit/commit/all redisplays/persistence/old-save compatibility remain unresolved.','Seven-byte watch window is not a proven complete field ABI or full writer population. Native save regression predates answer entry.','Shared confirmation other callers, whole-game translation and human wording/presentation/release review remain open.'])
    result['keyboard_returns']=keyboard_returns
    result['rejected_attempt']=dict(route=PREFIX+'no',observation='Without neutral7 after checkpoint load, initial Right was not accepted; cursor remained at Yes and A committed. This is not No evidence. Old edit-after-no/reconfirm-after-no continue that committed branch, not keyboard editing.',replacement=PREFIX+'no-settled',limits='Checkpoint-load/input readiness cause not fully traced; source controls preserved, current validated recipe uses neutral7 and checks actual cursor before No acceptance.')
    (OUT/'confirmation_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Common confirmation3 normal font/OBJ/pixels/Yes-No-B native records PASS');return result
if __name__=='__main__':main()
