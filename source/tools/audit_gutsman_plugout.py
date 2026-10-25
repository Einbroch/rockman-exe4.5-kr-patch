"""Final identity, immutable-source write ledger and exact cumulative carry audit."""
import json,struct
from report_roll_pet import ROOT,read,sha,require_hash,static
from keyitem_rom_data import verify_final

STEM='exe45_ko_development_gutsman_plugout_v1'
OLD='exe45_ko_development_keyitem_full_rom_v1'
OUT=ROOT/'analysis/gutsman_plugout_v1'

def main():
    m,rom,_,streams,checks=static(STEM,'778338')
    old=read(ROOT/f'poc/output/{OLD}.json');prior=(ROOT/f'poc/output/{OLD}.gba').read_bytes()
    if sha(prior)!=old['output_sha256']:raise ValueError('previous product identity')
    source_path=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source_path,m['source_sha256']);source=source_path.read_bytes()
    reconstructed=bytearray(source);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];value=bytes.fromhex(w['final_hex'])
        if len(value)!=n or source[at:at+n]!=bytes.fromhex(w['expected_hex']) or occupied.intersection(range(at,at+n)):raise ValueError('immutable ledger overlap/source')
        occupied.update(range(at,at+n));reconstructed[at:at+n]=value
    if bytes(reconstructed)!=rom[:len(source)] or rom[:192]!=source[:192] or len(rom)!=len(source)+m['append_bytes'] or sha(rom[len(source):])!=m['append_sha256']:raise ValueError('final ledger/header/append')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    before={a['archive']:a for a in old['archives']};after={a['archive']:a for a in m['archives']}
    if set(before)!=set(after):raise ValueError('unexpected archive membership')
    preserved=[]
    for name,a in before.items():
        b=after[name]
        if name=='778338':continue
        x=prior[a['rom_offset']:a['rom_offset']+a['compiled_bytes']];y=rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']]
        if x!=y:raise ValueError('prior archive payload changed '+name)
        preserved.append(name)
    old_assets={a['path'].replace('\\','/'):a['sha256'] for a in old['translation_assets']};new_assets={a['path'].replace('\\','/'):a['sha256'] for a in m['translation_assets']}
    replaced='translations/roll_plugout_ko.json';replacement='translations/roll_gutsman_plugout_ko.json'
    if set(new_assets)!=(set(old_assets)-{replaced}|{replacement}) or any(new_assets[k]!=v for k,v in old_assets.items() if k!=replaced):raise ValueError('unrelated selected input changed')
    units=read(ROOT/replacement)['units'];parent=read(ROOT/replaced)['units'];index={u['id']:u for u in units}
    if any(index.get(u['id'])!=u for u in parent) or m['translated_units']!=old['translated_units']+len(units)-len(parent):raise ValueError('retained Roll / cumulative denominator')
    font=m['extension']['normal_font_offset'];end=m['extension']['advance_offset']
    oldfont=old['extension']['normal_font_offset'];oldend=old['extension']['advance_offset']
    if rom[font:end]!=prior[oldfont:oldend]:raise ValueError('existing font glyph bytes changed')
    count=m['extension']['legacy_index_view']+m['extension']['hangul_syllables']+m['extension']['extra_glyph_count']
    oldcount=old['extension']['legacy_index_view']+old['extension']['hangul_syllables']+old['extension']['extra_glyph_count']
    if count!=oldcount or rom[end:end+count*4]!=prior[oldend:oldend+oldcount*4]:raise ValueError('font advance table drift')
    graphic_scopes=[]
    for key in ('calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics'):
        a,b=old[key],m[key];at=b['source_offset'];n=b.get('stored_bytes',b.get('bytes'))
        if a!=b or prior[at:at+n]!=rom[at:at+n]:raise ValueError('previous graphics changed '+key)
        graphic_scopes.append(key)
    verify_final(source,rom,m['keyitem_rom'])
    a,b=old['keyitem_rom'],m['keyitem_rom']
    if prior[a['rom_offset']:a['rom_offset']+a['rom_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['rom_bytes']]:raise ValueError('full39 clone wording changed')
    cpu=read(OUT/'cpu/report.json');runtime=read(OUT/'plugout_runtime.json')
    if not(cpu['passed'] and cpu['integrated_artifact_final_bytes_checked'] and cpu['baseline_rom_sha256']==m['output_sha256'] and runtime['passed'] and runtime['rom_sha256']==m['output_sha256']):raise ValueError('CPU/runtime identity')
    rt=ROOT/'poc/runtime';prefix='gutsman-plugout-v1-';commit=rt/(prefix+'save-commit');env=read(commit/'save_environment.json');sav=STEM+'.sav';saved=env['files_after'][sav]
    if not env['observer_only'] or env['build_sha256']!=m['output_sha256'] or env['files_before'][sav]!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or saved['bytes']!=65536 or saved['sha256']==sha(bytes([255])*65536) or sha((commit/'persistent_files_after'/sav).read_bytes())!=saved['sha256']:raise ValueError('fresh own native save')
    state=(commit/'step_013_gbaExtWorkRam.bin').read_bytes();savepool=0x08000000+after['6DA21C']['rom_offset']
    if state[0xFA21]!=58 or struct.unpack_from('<I',state,0xFA50)[0]!=savepool:raise ValueError('native save success script58')
    reload=read(rt/(prefix+'normal-reload-menu')/'result.json')
    if reload['state_origin'] is not None or reload['rom_sha256']!=m['output_sha256']:raise ValueError('cold continue must not import checkpoint')
    tools={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted((ROOT/'tools').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,
        rom_sha256=m['output_sha256'],source_sha256=sha(source),repro_sha256=sha((ROOT/f'poc/output/{STEM}_repro.gba').read_bytes()),
        selected_literal_units=m['translated_units'],added_literal_units=len(units)-len(parent),source_header_append_and_write_ledger_verified=True,
        unchanged_prior_archive_payloads=preserved,retained_Roll_units=len(parent),all_other_input_hashes_unchanged=True,font_provider_bytes_unchanged=True,
        keyitem_full39_clone_unchanged=True,keyitem_final_machine_code_verified=True,plugout_static=checks,
        unchanged_graphics=graphic_scopes,native_save_sha256=saved['sha256'],native_save_success_script=58,cold_continue_without_imported_checkpoint=True,
        new_units_normal_runtime_verified=runtime['normal_runtime_units'],tool_pins=tools,
        limits=['Shop other02031000 caller actual execution remains open; Internet normal route now preserved.','Other Navi plugout prose, other remaining Japanese, global Hangul input/persistence/old-save compatibility, human review and release remain incomplete.'])
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'final_identity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:result[k] for k in ('passed','rom_sha256','selected_literal_units','added_literal_units','retained_Roll_units')},indent=2))

if __name__=='__main__':main()
