"""Finite PET text/controls/font coverage and normal-play stream/OBJ pixel QA."""
import json,struct
from collections import Counter
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from tpl_literals import resolve_units,literals,skeleton
from korean_codec import encode_character,EXTRA_CHARACTER_INDICES
from archive_scripts import script_spans,verify_untouched_scripts
from report_fixedcell_runtime import verify_route

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def static(stem,archive='65FA58'):
    rp=ROOT/f'poc/output/{stem}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);require_hash(ROOT/f'poc/output/{stem}_repro.gba',m['output_sha256']);rom=rp.read_bytes()
    profiles={'65FA58':(1126,22,0x380D8,'roll_pet_menu_ko.json',44,6),'65F9AC':(170,4,0x380D4,'roll_intro_ko.json',5,2),'65FF3C':(3434,65,0x380E0,'roll_fortune_intro_blue_ko.json',13,62)}
    profiles['660CA8']=(231,5,0x380E4,'roll_jackin_ko.json',5,2)
    profiles['65F11C']=(2190,255,0x322E0,'roll_calendar_dialogue_ko.json',9,250)
    if archive=='65F11C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==11:
        profiles['65F11C']=(2190,255,0x322E0,'roll_calendar_content_ko.json',11,248)
    if archive=='65F11C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==14:
        profiles['65F11C']=(2190,255,0x322E0,'roll_calendar_date_ko.json',14,247)
    profiles['660D90']=(717,28,0x380E8,'roll_schedule_alarm_ko.json',3,25)
    profiles['6DA21C']=(9008,120,244860,'rockman_roll_save_ko.json',32,110)
    profiles['6872B8']=(313,4,0x38278,'numberman_intro_ko.json',7,3)
    profiles['665EB8']=(129,4,0x38110,'gutsman_intro_ko.json',4,2)
    profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_prompts_ko.json',2,253)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==4:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_content_ko.json',4,251)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==7:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_confirmation_ko.json',7,250)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==10:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_home_ko.json',10,249)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==14:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_register_ko.json',14,247)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==15:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_anniversary_ko.json',15,246)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==18:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_anniversary_confirmation_ko.json',18,245)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==22:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_navigation_ko.json',22,243)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==45:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_management_ko.json',45,230)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==54:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_schedule_delete_ko.json',54,227)
    if archive=='665698' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==57:
        profiles['665698']=(2077,255,0x322E4,'gutsman_calendar_inventory_ko.json',57,226)
    profiles['665F3C']=(1147,22,0x38114,'gutsman_pet_menu_ko.json',44,6)
    profiles['6663B8']=(120,4,0x38118,'gutsman_return_ko.json',2,2)
    profiles['6664D0']=(75,3,0x38120,'gutsman_jackin_ko.json',1,2)
    profiles['666820']=(1337,255,0x38128,'gutsman_mail_alert_ko.json',28,241)
    profiles['666D5C']=(473,25,0x3812C,'gutsman_competition_ko.json',10,18)
    profiles['666F38']=(265,14,0x38134,'gutsman_schedule_ko.json',12,8)
    profiles['66651C']=(771,28,0x38124,'gutsman_schedule_alarm_ko.json',3,26)
    if archive=='66651C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==5:
        profiles['66651C']=(771,28,0x38124,'gutsman_alarm_followup_ko.json',5,24)
    if archive=='66651C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==6:
        profiles['66651C']=(771,28,0x38124,'gutsman_alarm_meal_ko.json',6,23)
    profiles['66A7A8']=(155,5,0x38130,'gutsman_battle_results_ko.json',3,2)
    profiles['66A844']=(2191,255,0x38148,'gutsman_pet_talk_ko.json',31,231)
    if archive=='66A844' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==33:
        profiles['66A844']=(2191,255,0x38148,'gutsman_pet_chipquest_ko.json',33,230)
    profiles['68BBB4']=(1813,21,230060,'numberman_seasonal_ko.json',60,6)
    profiles['66A234']=(1395,21,229700,'gutsman_seasonal_ko.json',49,6)
    profiles['66F78C']=(1292,21,229760,'windman_seasonal_ko.json',46,7)
    profiles['675440']=(1273,21,229820,'searchman_seasonal_ko.json',40,6)
    profiles['67AE2C']=(1444,21,229880,'fireman_seasonal_ko.json',47,6)
    profiles['680454']=(1134,21,229940,'thunderman_seasonal_ko.json',34,6)
    profiles['685C68']=(1201,21,230000,'blues_seasonal_ko.json',33,6)
    profiles['691A64']=(1307,21,230120,'metalman_seasonal_ko.json',39,6)
    profiles['696DD8']=(1168,21,230180,'junkman_seasonal_ko.json',37,6)
    profiles['69C9F4']=(1358,21,230240,'aquaman_seasonal_ko.json',43,6)
    profiles['6A2184']=(1348,21,230300,'woodman_seasonal_ko.json',41,6)
    profiles['6A8ADC']=(1439,21,230360,'starman_seasonal_ko.json',48,6)
    profiles['6AE834']=(1367,21,230420,'shadowman_seasonal_ko.json',41,7)
    profiles['6BA3AC']=(1378,21,230480,'knightman_seasonal_ko.json',42,6)
    profiles['6C004C']=(1199,21,230540,'napalmman_seasonal_ko.json',38,6)
    profiles['6C5A88']=(1182,21,230600,'iceman_seasonal_ko.json',34,6)
    profiles['6CB184']=(1340,21,230660,'elecman_seasonal_ko.json',40,6)
    profiles['6D0ADC']=(1420,21,230720,'plantman_seasonal_ko.json',43,6)
    profiles['6D5A9C']=(1042,21,230780,'forte_seasonal_ko.json',33,6)
    profiles['65E438']=(1007,21,229580,'rockman_seasonal_ko.json',28,6)
    profiles['6648D0']=(1202,21,229640,'roll_seasonal_ko.json',41,6)
    if archive=='6872B8' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==12:
        profiles['6872B8']=(313,4,0x38278,'numberman_return_ko.json',12,2)
    profiles['6873F4']=(1160,22,0x3827C,'numberman_pet_menu_ko.json',44,6)
    profiles['687910']=(1323,65,0x38284,'numberman_training_intro_ko.json',16,61)
    if archive=='687910' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==33:
        profiles['687910']=(1323,65,0x38284,'numberman_training_results_ko.json',33,53)
    profiles['687E3C']=(76,3,0x38288,'numberman_jackin_ko.json',1,2)
    if archive=='687910' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==39:
        profiles['687910']=(1323,65,0x38284,'numberman_training_rewards_ko.json',39,51)
    profiles['715064']=(1207,16,0xDD394,'numberman_drill_intro_ko.json',20,14)
    if archive=='715064' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==32:
        profiles['715064']=(1207,16,0xDD394,'numberman_drill_bubbles_ko.json',32,2)
    profiles['661060']=(1351,255,0x380EC,'roll_mail_alert_ko.json',14,241)
    if archive=='715064' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==42:
        chosen=next(a for a in m['translation_assets'] if a['archive']==archive)['path'].replace('\\','/').rsplit('/',1)[-1]
        if chosen not in ('numberman_drill_options_ko.json','numberman_drill_options_padded_ko.json','numberman_drill_options_spaced_ko.json'):raise ValueError('unknown42-unit options asset')
        profiles['715064']=(1207,16,0xDD394,chosen,42,0)
    profiles['6615A8']=(426,25,0x380F0,'roll_competition_ko.json',14,18)
    profiles['661754']=(260,14,0x380F8,'roll_schedule_ko.json',5,10)
    if archive=='661754' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==6:
        profiles['661754']=(260,14,0x380F8,'roll_schedule_time_ko.json',6,9)
    profiles['664E28']=(2158,255,0x3810C,'roll_pet_talk_ko.json',1,254)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==30:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_chipquest_ko.json',30,230)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==29:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_weekday_ko.json',29,231)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==24:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_undernet_ko.json',24,234)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==5:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_license_ko.json',5,250)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==8:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_incident_ko.json',8,248)
    profiles['65FEC0']=(123,4,0x380DC,'roll_return_ko.json',4,2)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==22:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_mail_ko.json',22,235)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==20:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_events_ko.json',20,237)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==14:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_tournament_ko.json',14,243)
    if archive=='664E28' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==11:
        profiles['664E28']=(2158,255,0x3810C,'roll_pet_keyquest_ko.json',11,245)
    profiles['778338']=(1810,46,0x6A544,'roll_plugout_ko.json',4,44)
    if archive=='778338' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==8:
        profiles['778338']=(1810,46,0x6A544,'roll_gutsman_plugout_ko.json',8,42)
    profiles['661858']=(5121,97,0x380FC,'roll_family_sister_ko.json',8,95)
    if archive=='661858' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==16:
        profiles['661858']=(5121,97,0x380FC,'roll_family_sisters_ko.json',16,93)
    if archive=='661858' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==32:
        profiles['661858']=(5121,97,0x380FC,'roll_family_siblings_ko.json',32,89)
    profiles['667044']=(5225,97,0x38138,'gutsman_profile_ko.json',40,77)
    if archive=='667044' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==81:
        profiles['667044']=(5225,97,0x38138,'gutsman_profile_questions_ko.json',81,67)
    if archive=='667044' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==110:
        profiles['667044']=(5225,97,0x38138,Path(next(a for a in m['translation_assets'] if a.get('archive')=='667044')['path']).name,110,59)
    if archive=='667044' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==150:
        profiles['667044']=(5225,97,0x38138,Path(next(a for a in m['translation_assets'] if a.get('archive')=='667044')['path']).name,150,35)
    if archive=='667044' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==153:
        profiles['667044']=(5225,97,0x38138,Path(next(a for a in m['translation_assets'] if a.get('archive')=='667044')['path']).name,153,34)
    size,count,pointer,asset_name,unit_count,protected_count=profiles[archive];offset=int(archive,16)
    if archive=='6DA21C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==69:
        asset_name,unit_count,protected_count='four_navi_save_ko.json',69,95
    if archive=='6DA21C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==53:
        asset_name,unit_count,protected_count='rockman_roll_gutsman_save_ko.json',53,100
    if archive=='661858' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==36:
        asset_name,unit_count,protected_count='roll_food_ko.json',36,88
    if archive=='661858' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==41:
        asset_name,unit_count,protected_count='roll_subjects_ko.json',41,86
    if archive=='65FF3C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==80:
        asset_name,unit_count,protected_count='roll_fortune_results_ko.json',80,44
    if archive=='65FF3C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==88:
        asset_name,unit_count,protected_count='roll_minigame_results_ko.json',88,40
    if archive=='65FF3C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==102:
        asset_name,unit_count,protected_count='roll_minigame_rewards_ko.json',102,36
    if archive=='65FF3C' and next(a for a in m['archives'] if a['archive']==archive)['translated_units']==103:
        asset_name,unit_count,protected_count='roll_fortune_complete_ko.json',103,35
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();ar=next(a for a in m['archives'] if a['archive']==archive);pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    asset_path=ROOT/'translations'/asset_name;asset=read(asset_path)
    manifest=next(a for a in m['translation_assets'] if a['archive']==archive);require_hash(asset_path,manifest['sha256'])
    if sha(payload)!=ar['compiled_sha256'] or sha(source[offset:offset+size])!=asset['source_archive_sha256'] or rom[offset:offset+size]!=source[offset:offset+size] or struct.unpack_from('<I',rom,pointer)[0]!=pool:raise ValueError('Roll relocation/source identity')
    units=resolve_units(asset);changed={int(u['id'].split(':')[1]) for u in units};preserved=verify_untouched_scripts(source[offset:offset+size],payload,count,changed)
    if len(units)!=unit_count or len(preserved)!=protected_count or not ar['protected_controls_unchanged'] or not ar['binary_roundtrip'] or not ar['semantic_roundtrip']:raise ValueError('Roll denominator/roundtrip')
    if archive=='65FA58':
        idle=next(u for u in units if u['id']=='65FA58:1:0')
        if idle['translation'].split('\n')[0]!=idle['source'].split('\n')[0]:raise ValueError('dynamic nickname suffix growth')
    if archive=='661060':
        for script in [1,2,3]:
            suffix=next(u for u in units if u['id']==f'661060:{script}:1')
            if suffix['translation'].split('\n')[0]!=suffix['source'].split('\n')[0]:raise ValueError('mail nickname suffix growth')
    if archive=='65FEC0':
        suffix=next(u for u in units if u['id']=='65FEC0:1:1')
        if suffix['translation'].split('\n')[0]!=suffix['source'].split('\n')[0]:raise ValueError('dynamic nickname suffix growth')
    if archive=='778338':
        suffix=next(u for u in units if u['id']=='778338:6:0')
        if suffix['translation'].split('\n')[0]!=suffix['source'].split('\n')[0]:raise ValueError('dynamic nickname suffix growth')
    if archive=='661858':
        for script in ([1,3,5,7] if unit_count in (32,36,41) else [5,7] if unit_count==16 else [7]):
            suffix=next(u for u in units if u['id']==f'661858:{script}:3')
            if suffix['source'].split('\n')[0]!='は、' or suffix['translation'].split('\n')[0]!='、':raise ValueError('dynamic nickname topic suffix translation')
        if unit_count in (36,41):
            suffix=next(u for u in units if u['id']=='661858:11:2')
            if suffix['source']!='は' or suffix['translation']!='、':raise ValueError('food nickname topic suffix translation')
        if unit_count==41:
            for script,literal in [(27,1),(29,2)]:
                suffix=next(u for u in units if u['id']==f'661858:{script}:{literal}')
                if suffix['source'].split('\n')[0]!='の' or suffix['translation'].split('\n')[0]!='、':raise ValueError('subject nickname topic suffix translation')
    ef=m['extension'];font=ef['normal_font_offset'];bias=ef['legacy_index_view'];wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'}
    glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted)
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    spans=script_spans(payload,count);expected={};unit_streams={}
    for u in units:
        script=int(u['id'].split(':')[1]);text=u['translation']
        def encoded(c):return b'\xe8' if c=='\n' else encode_character(c) if c in wanted or c in EXTRA_CHARACTER_INDICES else codes[c]
        body=b''.join(encoded(c) for c in text)
        if u['id'] in ('6A2184:1:1','6A2184:1:3'):
            # Two identical shrine claps in one source script. Each is tied
            # to its exact next consumer boundary, never the first match.
            before=script_spans(source[offset:offset+size],count)[script]
            native_body=b''.join(codes[c] for c in u['source'])
            boundary=bytes.fromhex('e600f1')
            if u['source']!='パンパン!' or text!='짝짝!' or before.count(native_body)!=2 or spans[script].count(body)!=2:raise ValueError('WoodMan paired claps identity')
            if u['id']=='6A2184:1:1':
                following=next(v for v in units if v['id']=='6A2184:1:2')
                native_after=b''.join(b'\xe8' if c=='\n' else codes[c] for c in following['source'])+boundary
                after=b''.join(encoded(c) for c in following['translation'])+boundary
            else:
                native_after=after=bytes.fromhex('f90c01')+codes['、']+b'\xe8'
            native_anchor=native_body+boundary+native_after;anchor=body+boundary+after
            if before.count(native_anchor)!=1 or spans[script].count(anchor)!=1:raise ValueError('WoodMan clap consumer boundary')
            body_at=spans[script].index(anchor)
        elif u['id'] in ('666F38:11:0','666F38:11:1'):
            before=script_spans(source[offset:offset+size],count)[script]
            prefix=bytes.fromhex('f9038201' if u['id'].endswith(':0') else 'f903c201')
            suffix=bytes.fromhex('fc032900' if u['id'].endswith(':0') else 'fc032b00')
            anchor=prefix+body+suffix
            if text!=u['source'] or text!=(':' if u['id'].endswith(':0') else ' ') or before.count(anchor)!=1 or spans[script].count(anchor)!=1:raise ValueError('Guts schedule clock scalar consumer anchor')
            body_at=spans[script].index(anchor)+len(prefix)
        elif archive=='666820' and u['id'].endswith(':0'):
            # The first !! is separate from the mail sentence ending in !!.
            # Bind it to the original arrow/sound/wait consumer boundaries.
            before=script_spans(source[offset:offset+size],count)[script]
            prefix=bytes.fromhex('f604e18d')
            suffix=bytes.fromhex('fd009b00ed006000fd009b00ed006000f1')
            anchor=prefix+body+suffix
            if u['source']!='!!' or text!='!!' or before.count(body)!=2 or spans[script].count(body)!=2 or before.count(anchor)!=1 or spans[script].count(anchor)!=1:raise ValueError('GutsMan initial mail exclamations command anchor')
            body_at=spans[script].index(anchor)+len(prefix)
        elif u['id']=='6BA3AC:1:2':
            before=script_spans(source[offset:offset+size],count)[script]
            anchor=bytes.fromhex('f90c01')+body+bytes.fromhex('e600f1')
            if u['source']!='、' or text!='、' or before.count(anchor)!=1 or spans[script].count(anchor)!=1:raise ValueError('KnightMan nickname scalar command anchor')
            body_at=spans[script].index(anchor)+3
        elif u['id']=='67AE2C:11:5':
            # The source-identical final ! follows the second nickname print.
            # Other exclamation marks belong to earlier birthday literals.
            before=script_spans(source[offset:offset+size],count)[script]
            native_anchor=bytes.fromhex('f90c01')+codes['!']+bytes.fromhex('e600f1')
            anchor=bytes.fromhex('f90c01')+body+bytes.fromhex('e600f1')
            if u['source']!='!' or u['translation']!='!' or before.count(native_anchor)!=1 or spans[script].count(anchor)!=1:raise ValueError('FireMan final nickname scalar anchor')
            body_at=spans[script].index(anchor)+3
        elif u['id']=='661858:11:2':
            # A single comma also occurs inside earlier literals. Bind this
            # scalar to the source-pinned newline/nickname/keyWait boundary,
            # not an arbitrary first matching punctuation byte.
            before=script_spans(source[offset:offset+size],count)[script]
            native_anchor=b'\xe8\xf9\x0c\x01'+codes['は']+bytes.fromhex('e600f1')
            anchor=b'\xe8\xf9\x0c\x01'+body+bytes.fromhex('e600f1')
            if before.count(native_anchor)!=1 or spans[script].count(anchor)!=1:raise ValueError('food nickname scalar command anchor')
            body_at=spans[script].index(anchor)+4
        else:
            if spans[script].count(body)!=1:raise ValueError('PET literal encoding uniqueness')
            body_at=spans[script].index(body)
        cursor=pool+struct.unpack_from('<H',payload,script*2)[0]+body_at;streams=[]
        for ch in text:
            data=encoded(ch)
            if ch=='\n':cursor+=1;continue
            index=ord(ch)-0xAC00+bias if ch in wanted else EXTRA_CHARACTER_INDICES[ch]+bias if ch in EXTRA_CHARACTER_INDICES else data[0]
            record=rom[font+index*96:font+(index+1)*96]
            if ch in wanted and record!=glyphs[ch]:raise ValueError('PET Hangul font supply')
            if ch not in wanted and ch not in EXTRA_CHARACTER_INDICES and record!=source[0x608758+index*96:0x608758+(index+1)*96]:raise ValueError('native punctuation/space font altered')
            expected[cursor]={'ch':ch,'index':index,'record':record,'id':u['id'],'script':script};streams.append(cursor);cursor+=len(data)
        unit_streams[u['id']]=streams
    result={'new_units':unit_count,'protected_unselected_scripts' if archive=='65FF3C' else 'protected_nonliteral_scripts':preserved,'all_fonts_verified':True,'max_literal_width':max(max(x['line_advance_pixels']) for x in ar['layout'])}
    if archive=='65FA58':result.update(nickname_first_line_bytes_unchanged=True,all14_choice_rows_validated_by_build=True)
    return m,rom,expected,unit_streams,result

def pixels(path,step,draws,expected,rom,m,origin=(92,110),cursor_screen_background=False,cursor_indices=(0,)):
    cp=f'step_{step:03}';v=(path/(cp+'_gbaVideoRam.bin')).read_bytes();o=(path/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(path/(cp+'.png')).convert('RGB');objects=[];cursors=[]
    dimensions=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]]
    for i in range(128):
        a,b,k=struct.unpack_from('<HHH',o,i*8)
        if not a&0x2300 and a>>14<3 and k>>12==14:
            w,h=dimensions[a>>14][b>>14];ob=(b&511,a&255,k&1023,w,h)
            if k&1023==1020:
                if i not in cursor_indices or (w,h)!=(16,16):raise ValueError('registered option cursor OBJ contract')
                cursors.append(ob)
            else:objects.append(ob)
    checked=0;colors={};cursor_overlap=0
    for d in draws:
        g=expected[d['stream']]
        if d['glyph_index']!=g['index'] or d['offset']%4:raise ValueError('PET glyph index/geometry')
        row,off=divmod(d['offset'],10752);x0=origin[0]+off//4;y0=origin[1]+row*14
        width=struct.unpack_from('<I',rom,m['extension']['advance_offset']+g['index']*4)[0]
        if row>2 or x0+width>236 or y0+12>154:raise ValueError('PET glyph out of adopted screen range')
        for yy in range(12):
            for xx in range(width):
                role=(g['record'][yy*8+xx//2]>>(4*(xx%2)))&15;x=x0+xx;y=y0+yy
                matches=[ob for ob in objects if ob[0]<=x<ob[0]+ob[3] and ob[1]<=y<ob[1]+ob[4]]
                if len(matches)!=1:raise ValueError(f'PET unique OBJ residency:{path.name}/{step}/{g["id"]}/{g["ch"]}/{x},{y}/{len(matches)}')
                ox,oy,tile,w,h=matches[0];lx=x-ox;ly=y-oy;at=0x10000+tile*32+(ly//8*(w//8)+lx//8)*32+(ly%8)*4+lx%8//2
                vr=(v[at]>>(4*(lx%2)))&15
                if vr!=role:raise ValueError('PET ROM glyph -> OBJ VRAM pixel')
                covered=False
                for cx,cy,ct,cw,ch in cursors:
                    if cx<=x<cx+cw and cy<=y<cy+ch:
                        # The animated native cursor owns the screen background
                        # inside its OBJ rectangle. Font ink/shadow are never
                        # exempted, and ROM->VRAM checks above remain strict.
                        if cursor_screen_background and role==1:
                            covered=True;cursor_overlap+=1
                        px=x-cx;py=y-cy;ca=0x10000+ct*32+(py//8*(cw//8)+px//8)*32+py%8*4+px%8//2
                        if (v[ca]>>(4*(px%2)))&15:
                            if role!=1:raise ValueError(f'PET choice cursor covers translated ink or shadow:{path.name}/{step}/{g["id"]}/{g["ch"]}/{x},{y}/role={role}/cursor={cx},{cy}')
                            if not covered:cursor_overlap+=1
                            covered=True
                if role and not covered:colors.setdefault((d['color'],role),set()).add(im.getpixel((x,y)))
                checked+=1
    if any(len(c)!=1 for c in colors.values()):raise ValueError('PET visible role colors disagree')
    return {'glyphs':len(draws),'pixels':checked,'font_vram_screen_pixels_match':True,'native_cursor_overlap_background_pixels':cursor_overlap,'no_translated_ink_occluded':True,'role_colors':{str(k):list(next(iter(c))) for k,c in colors.items()}}

def main(stem='exe45_ko_development_roll_pet_v2',prefix='roll-pet-v2-',outdir='roll_pet_v2'):
    m,rom,expected,streams,static_result=static(stem);runtime=ROOT/'poc/runtime';routes=[runtime/(prefix+'roll-intro'),runtime/(prefix+'prompts')];seen=set();pages=[];observed=set()
    for path in routes:
        receipt=verify_route(path,m['output_sha256'],seen)
        if receipt['emulator_sha256']!=read(ROOT/'project.json')['development_dependencies']['runtime_capture']['mesen_sha256']:raise ValueError('emulator identity')
        for step in receipt['capture_steps']:
            cp=f'step_{step:03}';state=read(path/(cp+'_roll_pet.json'));ram=(path/(cp+'_gbaExtWorkRam.bin')).read_bytes();ar=next(a for a in m['archives'] if a['archive']=='65FA58');pool=0x08000000+ar['rom_offset']
            if struct.unpack_from('<I',ram,0xFA50)[0]!=pool:continue
            script=ram[0xFA21];keys=[k for k in streams if int(k.split(':')[1])==script]
            if not keys:continue
            # Latest draw per source character from this active script. Earlier
            # executions of the same unit must not mask a missing current draw.
            all_streams={s for k in keys for s in streams[k]};draws=[d for d in state['draws'] if d['stream'] in all_streams]
            if not draws:continue
            last={d['stream']:d for d in draws};first_frame=max(d['frame'] for d in draws)-1000
            selected=[last[s] for k in keys for s in streams[k] if s in last and last[s]['frame']>=first_frame]
            if set(d['stream'] for d in selected)!=all_streams:continue # text still typing, not a complete-page claim
            counts=Counter(expected[d['stream']]['index'] for d in selected);reads={x['index']:x['reads'] for x in state['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('PET full font CPU read coverage')
            proof=pixels(path,step,selected,expected,rom,m);observed.update(keys);pages.append({'route':path.name,'step':step,'script':script,'units':keys,**proof,'screenshot_sha256':sha((path/(cp+'.png')).read_bytes())})
    behavior=[];prompt_path=runtime/(prefix+'prompts');pool=0x08000000+next(a for a in m['archives'] if a['archive']=='65FA58')['rom_offset']
    expectation={1:(2,108),2:(2,144),3:(1,220),4:(2,108),5:(1,220)}
    for script,base in zip(range(3,9),range(6,30,4)):
        expectation.update({base:(1,220),base+1:(script,108),base+2:(script,144),base+3:(1,220)})
    for step,(script,cursor_x) in expectation.items():
        ram=(prompt_path/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();o=(prompt_path/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();a,b,k=struct.unpack_from('<HHH',o,0)
        if struct.unpack_from('<I',ram,0xFA50)[0]!=pool or ram[0xFA21]!=script or b&511!=cursor_x:raise ValueError('PET Yes/No/cancel/return transition')
        if script!=1 and (a&255!=136 or k&1023!=1020 or k>>12!=14):raise ValueError('PET normal option cursor position')
        behavior.append({'step':step,'script':script,'cursor_x':cursor_x,'same_relocated_root':True})
    for script in [1,2,3,4,5,6,7,8]:
        if not any(p['script']==script for p in pages):raise ValueError(f'missing complete PET normal page {script}')
    out=ROOT/'analysis'/outdir;out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(960,320))
    for i,script in enumerate([1,2,3,4,5,6,7,8]):
        page=next(p for p in pages if p['script']==script);sheet.paste(Image.open(runtime/page['route']/f"step_{page['step']:03}.png"),(i%4*240,i//4*160))
    sheet.save(out/'pet_prompts.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'static':static_result,'runtime_observed_units':sorted(observed),'runtime_open_units':sorted(set(streams)-observed),'pages':pages,'limits':['Only observed complete pages have runtime pixel evidence; duplicate reentry/save-now/interruption branches remain open unless listed','No live communication or actual save executed','First meeting and daily/yearly Roll introduction remain Japanese; human wording/visual review, full-game/hardware/audio/release QA pending']}
    result['choice_behavior']=behavior
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json');return result

if __name__=='__main__':main()
