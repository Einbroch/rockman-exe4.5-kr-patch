"""Bound guide selector ABI, exact source/font, OBJ residency and screen pixels."""
import json,struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from archive_scripts import script_spans,verify_untouched_scripts
from verify_tpi_index import lz77_decompress
from tpl_literals import resolve_units
from korean_codec import encode_character
from report_equipment_labels_runtime import main as labels_report
from equipment_guides import validate,construct,INSTALL
from bench_equipment_guides import main as bench

def read(p):return json.loads(p.read_text(encoding='utf-8'))

def verify_pet_exit(source,rom,metadata,ram,previous,current):
    # Native initializer 0804FB70 stores root at context+30, script at +1,
    # current stream at +2C and starting stream at +34. PET starts its own
    # idle speech on exit, so the generic activation byte must NOT be zero.
    at=0x4FB70;native=bytes.fromhex('286369704900415a4018e8626863')
    if source[at:at+len(native)]!=native or rom[at:at+len(native)]!=native:raise ValueError('native text context field contract')
    ar=next(a for a in metadata['archives'] if a['archive']=='65A608');root=0x08000000+ar['rom_offset']
    payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];start=root+struct.unpack_from('<H',payload,2)[0]
    end=start+len(script_spans(payload,22)[1])
    actual_root=struct.unpack_from('<I',ram,0xFA50)[0];cursor=struct.unpack_from('<I',ram,0xFA4C)[0];initial=struct.unpack_from('<I',ram,0xFA54)[0]
    if actual_root!=root or ram[0xFA21]!=1 or initial!=start or not start<=cursor<end:raise ValueError('exit did not replace guide with PET script1')
    if any(current[k]!=previous[k] for k in ['entries','calls','returns','draws']):raise ValueError('guide observed after PET exit')
    return {'step':12,'guide_replaced':True,'pet_archive':'65A608','pet_script':1,'pet_root':root,'initial_stream':initial,'current_stream':cursor,'normal_context_active':bool(ram[0xFA20]),'native_field_contract_verified':True,'no_new_guide_calls_or_draws':True}

def main(stem='exe45_ko_development_equipment_guides_v1',prefix='equipment-guides-v1-',outdir='equipment_guides_v1',roll=False):
    rp=ROOT/f'poc/output/{stem}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();validate(source)
    ar=m['equipment_guides']['roll_archive' if roll else 'archive'];h=m['equipment_guides']['selector'];pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    if sha(payload)!=ar['compiled_sha256']:raise ValueError('guide clone identity')
    appended,patches,rebuilt=construct(source,rom[len(source):h['hook_offset']],m['equipment_guides']['archive']['rom_offset'],m['equipment_guides'].get('roll_archive',{}).get('rom_offset'))
    if 'dialogue_chip_name' in m:
        # The guide is no longer the final appended component. Rebuild the
        # declared successor as well, keeping full-tail equality fail-closed.
        from dialogue_chip_name import construct as name_construct
        nh=m['dialogue_chip_name'];name_asset=ROOT/nh['wording_asset_path'];require_hash(name_asset,nh['wording_asset_sha256']);nar=next(a for a in m['archives'] if a['archive']=='664E28');np=rom[nar['rom_offset']:nar['rom_offset']+nar['compiled_bytes']];ns=script_spans(np,255)[13]
        name_ar={'rom_offset':nar['rom_offset'],'script13_offset':int.from_bytes(np[26:28],'little'),'script13_prefix_hex':ns[:21].hex()}
        appended,name_patches,name_record=name_construct(source,appended,name_ar,read(name_asset));name_record.update(wording_asset_path=nh['wording_asset_path'],wording_asset_sha256=nh['wording_asset_sha256'])
        if name_record!=nh or rom[name_patches[0][0]:name_patches[0][0]+len(name_patches[0][1])]!=name_patches[0][1]:raise ValueError('declared dialogue name successor exact placement')
    if 'calendar_presets_poc' in m:
        # A declared successor is rebuilt, not accepted as an arbitrary tail.
        from calendar_presets import construct as preset_construct,validate as preset_validate
        pa=ROOT/'translations/calendar_presets_ko.json';pmanifest=next(a for a in m['translation_assets'] if a.get('archive')=='6368E8')
        if (ROOT/pmanifest['path']).resolve()!=pa.resolve():raise ValueError('preset successor asset')
        require_hash(pa,pmanifest['sha256']);preset_validate(read(pa)['units'])
        appended,preset_patches,preset_record=preset_construct(source,appended)
        if preset_record!=m['calendar_presets_poc'] or any(rom[at:at+len(blob)]!=blob for at,blob,_ in preset_patches):raise ValueError('declared preset successor exact placement')
    if rom[len(source):]!=appended or rom[INSTALL:INSTALL+12]!=patches[0][1] or rebuilt!=h:raise ValueError('hook exact final placement')
    source_offset=0x6E12DC if roll else 0x6E1068
    preserved=verify_untouched_scripts(lz77_decompress(source,source_offset)[0],payload,76,{60,61,62})
    if roll and rom[source_offset:source_offset+631]!=source[source_offset:source_offset+631]:raise ValueError('Roll original compressed pool altered')
    if rom[0x6E1068:0x6E1068+625]!=source[0x6E1068:0x6E1068+625] or rom[0x3C5BC:0x3C61C]!=source[0x3C5BC:0x3C61C]:raise ValueError('original Navi pool/loader changed')
    bench(stem,outdir);bench_result=read(ROOT/'analysis'/outdir/'bench.json')
    if not bench_result['passed'] or bench_result['vectors']!=72 or bench_result['rom_sha256']!=m['output_sha256']:raise ValueError('selector CPU fixtures')
    regression=labels_report(stem,prefix,outdir+'/labels_regression') if not roll else {'passed':False}
    if roll:
        from report_fixedcell_runtime import verify_route
        verify_route(ROOT/('poc/runtime/'+prefix+'equipment'),m['output_sha256'],set())
    ef=m['extension'];font=ef['normal_font_offset'];bias=ef['legacy_index_view'];asset=read(ROOT/('translations/roll_equipment_guides_ko.json' if roll else 'translations/rockman_equipment_guides_ko.json'));units=resolve_units(asset)
    if sha((ROOT/('translations/roll_equipment_guides_ko.json' if roll else 'translations/rockman_equipment_guides_ko.json')).read_bytes())!=ar['asset_sha256']:raise ValueError('guide input asset identity')
    wanted={c for u in units for c in u['translation'] if '\uac00'<=c<='\ud7a3'};glyphs=bdf_glyphs(ROOT/read(ROOT/'project.json')['development_dependencies']['font']['path'],wanted)
    codes={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(v)==1}
    spans=script_spans(payload,76);expected={};streams={}
    for u in units:
        script=int(u['id'].split(':')[1]);text=u['translation'];encoded=b''.join(b'\xe8' if c=='\n' else encode_character(c) if c in wanted else codes[c] for c in text)
        if spans[script].count(encoded)!=1:raise ValueError('literal encoding identity')
        cursor=pool+struct.unpack_from('<H',payload,script*2)[0]+spans[script].index(encoded);ordered=[]
        for ch in text:
            if ch=='\n':cursor+=1;continue
            data=encode_character(ch) if ch in wanted else codes[ch];index=ord(ch)-0xAC00+bias if ch in wanted else data[0];record=rom[font+index*96:font+(index+1)*96]
            if ch in wanted and record!=glyphs[ch]:raise ValueError('normal Korean BDF supply')
            if ch not in wanted and record!=source[0x608758+index*96:0x608758+(index+1)*96]:raise ValueError('native Latin/space/punctuation supply')
            expected[cursor]={'ch':ch,'index':index,'record':record};ordered.append(cursor);cursor+=len(data)
        streams[script]=ordered
    p=ROOT/('poc/runtime/'+prefix+'equipment');states={step:read(p/f'step_{step:03}_guides.json') for step in [7,9,11,12,15]};final=states[15]
    if len(final['entries'])!=4 or len(final['calls'])!=4 or len(final['returns'])!=4:raise ValueError('guide ABI observation count')
    abi=[]
    for e,c,r in zip(final['entries'],final['calls'],final['returns']):
        before=e['regs'];call=c['regs'];returned=r['regs'];navi=e['navi']
        if navi not in ([1] if roll else [0,13,14]) or call[0]!=pool or call[1]!=before[0]+60 or call[2:12]!=before[2:12] or call[13]!=before[13]-4 or c['saved_lr']!=before[14] or call[14]!=0x0803C485:raise ValueError('native guide call live-ins/stack')
        if returned[4:12]!=before[4:12] or returned[13]!=before[13]-4 or r['saved_lr']!=before[14]:raise ValueError('native normal callee return ABI')
        abi.append({'frame':e['frame'],'navi':navi,'script':call[1],'root':call[0],'caller_saved_lr':c['saved_lr'],'call_r2_r11_preserved':True,'return_r4_r11_and_stack_preserved':True})
    if [c['script'] for c in abi]!=[60,61,62,60]:raise ValueError('normal selection/exit/reentry sequence')
    pages=[]
    for step,script in [(7,60),(9,61),(11,62),(15,60)]:
        state=states[step];frame=state['entries'][-1]['frame'];draws=[d for d in state['draws'] if d['frame']>=frame and d['stream'] in streams[script]]
        if [d['stream'] for d in draws]!=streams[script]:raise ValueError('guide source stream coverage/order')
        counts=Counter(expected[d['stream']]['index'] for d in draws);reads={d['index']:d['reads'] for d in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('normal font CPU consumption')
        im=Image.open(p/f'step_{step:03}.png').convert('RGB');v=(p/f'step_{step:03}_gbaVideoRam.bin').read_bytes();o=(p/f'step_{step:03}_gbaSpriteRam.bin').read_bytes();objects=[]
        for i in range(128):
            a,b,k=struct.unpack_from('<HHH',o,i*8)
            if not a&0x2300 and a>>14==1 and b>>14==2 and k>>12==14 and a&255 in [110,126]:objects.append((i,b&511,a&255,k&1023))
        colors={1:set(),2:set(),3:set()};cells=[]
        for d in draws:
            g=expected[d['stream']]
            if d['glyph_index']!=g['index'] or d['color']!=0 or d['offset']%4:raise ValueError('guide normal glyph selection/color')
            row,off=divmod(d['offset'],10752);x0=92+off//4;y0=110+row*14;width=12 if g['ch'] in wanted else struct.unpack_from('<I',rom,ef['advance_offset']+g['index']*4)[0]
            if row not in [0,1] or x0+width>236 or y0+12>138:raise ValueError('guide bounds')
            for yy in range(12):
                for xx in range(width):
                    role=(g['record'][yy*8+xx//2]>>(4*(xx%2)))&15;x=x0+xx;y=y0+yy
                    matches=[obj for obj in objects if obj[1]<=x<obj[1]+32 and obj[2]<=y<obj[2]+16]
                    if len(matches)!=1:raise ValueError('guide OBJ residency/geometry')
                    idx,ox,oy,tile=matches[0];lx=x-ox;ly=y-oy;at=0x10000+tile*32+(ly//8*4+lx//8)*32+(ly%8)*4+lx%8//2
                    vr=(v[at]>>(4*(lx%2)))&15
                    if vr!=role:raise ValueError('guide ROM glyph -> OBJ VRAM role')
                    colors[role].add(im.getpixel((x,y)))
            cells.append({'character':g['ch'],'stream':d['stream'],'index':g['index'],'xy':[x0,y0],'width':width,'glyph_sha256':sha(g['record']),'font_vram_pixels_match':True})
        if any(len(values)!=1 for values in colors.values()) or len({next(iter(values)) for values in colors.values()})!=3:raise ValueError('guide screenshot role masks')
        pages.append({'step':step,'script':script,'cells':cells,'role_colors':{k:list(next(iter(v))) for k,v in colors.items()},'font_cpu_reads_verified':True,'all_glyph_pixels_match':True})
    ram=(p/'step_012_gbaExtWorkRam.bin').read_bytes()
    if roll:
        root=struct.unpack_from('<I',ram,0xFA50)[0];cursor=struct.unpack_from('<I',ram,0xFA4C)[0]
        pet_ar=next((a for a in m['archives'] if a['archive']=='65FA58'),None)
        native_root=0x08000000+pet_ar['rom_offset'] if pet_ar else 0x0865FA58
        native_payload=rom[pet_ar['rom_offset']:pet_ar['rom_offset']+pet_ar['compiled_bytes']] if pet_ar else source[0x65FA58:0x65FA58+1126]
        start=native_root+struct.unpack_from('<H',native_payload,2)[0];end=start+len(script_spans(native_payload,22)[1])
        if (root!=native_root or ram[0xFA21]!=1 or struct.unpack_from('<I',ram,0xFA54)[0]!=start or not start<=cursor<end
                or rom[0x65FA58:0x65FA58+1126]!=source[0x65FA58:0x65FA58+1126]
                or any(states[11][k]!=states[12][k] for k in ['entries','calls','returns','draws'])):raise ValueError('Roll guide persists or PET native script1 not consumed')
        exit_check={'step':12,'guide_replaced':True,'pet_root':root,'current_stream':cursor,'no_new_guide_calls_or_draws':True,'limit':'Relocated Roll PET script1 consumed' if pet_ar else 'Native Roll PET dialogue preserved, not yet translated'}
    else:exit_check=verify_pet_exit(source,rom,m,ram,states[11],states[12])
    out=ROOT/'analysis'/outdir;sheet=Image.new('RGB',(720,160))
    for i,step in enumerate([7,9,11]):sheet.paste(Image.open(p/f'step_{step:03}.png'),(i*240,0))
    sheet.save(out/'three_guides.png')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'rom_sha256':m['output_sha256'],'translated_units':m['translated_units'],'new_guide_units':3,'protected_clone_scripts':len(preserved),'selector_cpu_fixture_vectors':bench_result['vectors'],'selector_cpu_fixture_limit':bench_result['policy'],'native_abi':abi,'guide_pages':pages,'exit_check':exit_check,'equipment_folder_pet_regression_passed':regression['passed'],'guide_wordings':[{k:u[k] for k in ['id','source','translation','state']} for u in units],'contact_sheet_sha256':sha((out/'three_guides.png').read_bytes()),'limits':['Normal-play runtime uses Navi0 only; Navi13/14 and other Navi fallback covered by static source pool equality and synthetic CPU selection/ABI, not gameplay','Attack-power OBJ caption and other weapon names remain Japanese','Full playthrough, hardware, audio and human wording/presentation/release approval pending']}
    if 'weapons' in m['folder_labels']:result['limits'][1]='Common weapon drafts statically verified and representative cycling evaluated separately; no all-Navi gameplay claim'
    if 'equipment_attack_caption' in m:result['limits'].append('Caption has its own native decompression/residency/pixel report; guide report alone does not verify it')
    if roll:result['limits'][0]='Normal-play runtime Navi1 Roll only; synthetic selector fixtures cover 23 Navi plus invalid255; no all-Navi gameplay claim'
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(out/'runtime.json');return result

if __name__=='__main__':main()
