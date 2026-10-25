"""Audit the explicit cumulative startup scope, not a full-localization claim."""
import json
from pathlib import Path
from audit_save_keyboard_fonts import ROOT,digest
from verify_tpi_index import lz77_decompress

BASE_SHA='4b9ed3427001e08931fce46f76fed7d1e220553b15e8297f81e53ac51f0a50b7'
EXTRA={'analysis/startup_ui_v1/selected_asset.json':41,
       'analysis/startup_ui_v1/778A4C_selected_asset.json':4,
       'analysis/startup_ui_v1/65B220_selected_asset.json':7,
       'translations/startup_welcome_graphics_ko.json':0,
       'translations/startup_footer_graphics_ko.json':0}

def audit(product,baseline=None):
    baseline=ROOT/'poc/output/exe45_ko_development_weekend_menu_v1.gba'
    old=json.loads(baseline.with_suffix('.json').read_text(encoding='utf8'))
    if digest(baseline.read_bytes())!=BASE_SHA or old['output_sha256']!=BASE_SHA:raise ValueError('startup baseline identity')
    m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'));rom=product.read_bytes()
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=(ROOT/profile['filename']).read_bytes()
    if digest(rom)!=m['output_sha256'] or len(rom)!=m['output_bytes']:raise ValueError('startup target identity')
    if digest(source)!=profile['sha256'] or m['source_sha256']!=old['source_sha256'] or m['source_sha256']!=digest(source):raise ValueError('startup immutable source')
    expected_extras=dict(EXTRA)
    from mission_mail_header import ASSET as mission_asset
    mission=any(a['archive']=='6DD864' for a in m['archives'])
    if mission:expected_extras[mission_asset]=42
    batch_headers=0
    batch_raw=0
    if m.get('pending_batch500'):
        from batch500_rom import entries
        for path,_,asset,_,_,_ in entries(source):
            header=asset['consumer']=='fixed-cell-big';batch_headers+=int(header)
            expected_extras[f"analysis/pending_insertion_500_rom/{asset['archive']}_selected_asset.json" if header else path]=len(asset['units'])
    if m.get('pending_batch500_002'):
        from batch500_002_rom import entries as entries002
        for path,_,asset,scope,_,_ in entries002(source):
            standard=scope['standard_relocation'];batch_raw+=int(standard)
            expected_extras[f"analysis/pending_insertion_500_002_repartition_rom/{asset['archive']}_selected_asset.json" if standard else path]=len(asset['units'])
    if m.get('pending_batch500_003'):
        from batch500_003_rom import entries as entries003
        for path,_,asset,scope,_,_ in entries003(source):
            standard=scope['standard_relocation'];batch_raw+=int(standard)
            expected_extras[f"analysis/pending_insertion_500_003_rom/{asset['archive']}_selected_asset.json" if standard else path]=len(asset['units'])
    first_mail=any(a['archive']=='6DD9AC' for a in m['archives'])
    if m.get('pending_batch500_004'):
        from batch500_004_rom import entries as entries004
        for _,_,asset,_,_,_ in entries004(source):
            batch_raw+=1
            expected_extras[f"analysis/pending_insertion_500_004_rom/{asset['archive']}_selected_asset.json"]=len(asset['units'])
    if first_mail:
        if m.get('pending_batch500_005'):
            from batch500_005_rom import entries as entries005
            for _,_,asset,_,_,_ in entries005(source):
                batch_raw+=1
                expected_extras[f"analysis/pending_insertion_500_005_rom/{asset['archive']}_selected_asset.json"]=len(asset['units'])
        if m.get('pending_batch500_006'):
            from batch500_006_rom import entries as entries006
            for _,_,asset,_,_,_ in entries006(source):
                batch_raw+=1
                expected_extras[f"analysis/pending_insertion_500_006_rom/{asset['archive']}_selected_asset.json"]=len(asset['units'])
        from first_mail import specifications,asset_path,mode_for_manifest
        official=mode_for_manifest(m)
        full_header=any(a['path'].replace('\\','/')==asset_path('6DD63C',official,True) for a in m['translation_assets'])
        expected_extras.update({asset_path(a,official,full_header):s['count'] for a,s in specifications(official,full_header).items()})
    if m.get('native_keyboard_labels'):expected_extras['translations/native_keyboard_labels_ko.json']=0
    if m.get('navi_card_graphics'):expected_extras['translations/navi_card_graphics_ko.json']=0
    if m.get('keyitem_rom',{}).get('mail_rom_reader',{}).get('archive'):
        from full_mail_body import ASSET
        expected_extras[ASSET]=43
    lineage=None;lineage_assets=m['translation_assets']
    if m.get('pending_batch500_007'):
        from cumulative_batch500 import manifest_lineage
        lineage=manifest_lineage(source,rom,m);lineage_assets=lineage['parent_assets']
    extras=[a for a in lineage_assets if a not in old['translation_assets']]
    if [a for a in lineage_assets if a not in extras]!=old['translation_assets']:raise ValueError('startup prior wording lineage changed')
    if {a['path'].replace('\\','/') for a in extras}!=set(expected_extras) or len(extras)!=len(expected_extras):raise ValueError('startup extra assets population')
    for a in m['translation_assets']:
        path=ROOT/a['path']
        if digest(path.read_bytes())!=a['sha256']:raise ValueError('startup asset changed '+a['path'])
    added_archives=len(lineage['added_archives']) if lineage else 0
    if m['translated_units']!=2596+sum(expected_extras.values())+(lineage['new_units'] if lineage else 0) or m['unchanged_archives']!=669-3*first_mail-mission-batch_headers-batch_raw-added_archives or len(m['archives'])!=63+3*first_mail+mission+batch_headers+batch_raw+added_archives:raise ValueError('startup unit/archive denominator')
    added={'70904C':41,'778A4C':4,'65B220':7}
    if m.get('pending_batch500_018'):
        from cumulative_batch500_018 import entries as entries018
        added['65B220']=len(next(a['units'] for _,_,a,_,_,_ in entries018(source) if a['archive']=='65B220'))
    if m.get('pending_batch500_013'):
        from cumulative_batch500_013 import entries as entries013
        added['70904C']=len(next(a['units'] for _,_,a,_,_,_ in entries013(source) if a['archive']=='70904C'))
    records={a['archive']:a for a in m['archives']}
    for a in old['archives']:
        if lineage and a['archive'] in lineage['merged_archives']:continue # all non-new scripts checked above
        b=records[a['archive']]
        for k in ['compiled_sha256','translated_units','source_sha256']:
            if a[k]!=b[k]:raise ValueError('prior archive semantic scope changed')
    for archive,count in added.items():
        a=records[archive]
        if a['translated_units']!=count or not all(a[k] for k in ['native_roundtrip','semantic_roundtrip','binary_roundtrip','protected_controls_unchanged']):raise ValueError('startup archive roundtrip')
        payload=rom[a['rom_offset']:a['rom_offset']+a['compiled_bytes']]
        if digest(payload)!=a['compiled_sha256']:raise ValueError('startup compiled placement')
        for p in a['pointers']:
            if int.from_bytes(rom[p:p+4],'little')!=0x08000000+a['rom_offset']:raise ValueError('startup archive reference')
    permitted=bytearray(len(source))
    for w in m['expected_writes']:
        at,n=w['offset'],w['bytes'];end=at+n
        if at<0 or end>len(source) or any(permitted[at:end]):raise ValueError('startup planned-write overlap/bounds')
        if source[at:end].hex()!=w['expected_hex'] or rom[at:end].hex()!=w['final_hex']:raise ValueError('startup final-write identity')
        permitted[at:end]=b'\1'*n
    if any(a!=b and not permitted[i] for i,(a,b) in enumerate(zip(source,rom))):raise ValueError('startup unexplained final difference')
    if not m['final_diff_audited'] or not m['header_unchanged'] or rom[:0xC0]!=source[:0xC0] or digest(rom[len(source):])!=m['append_sha256']:raise ValueError('startup final image audit')
    native=[]
    for start,end in [(0x34FA0,0x35050),(0x32AC6,0x32AD8),(0x37366,0x3739A),(0x33334,0x33398)]:
        if source[start:end]!=rom[start:end]:raise ValueError('native name/calendar commit modified')
        native.append(dict(start=start,end=end,sha256=digest(rom[start:end])))
    ui=m['startup_renderer']
    for r in ui['layout']:
        if digest(rom[r['offset']:r['offset']+r['bytes']])!=r['sha256']:raise ValueError('startup renderer placement')
    for at,value in [(0x556A0,0x08000001+ui['layout'][1]['offset']),(0x557D4,0x08000000+m['extension']['advance_offset']),(0x557D8,0x08000000+ui['layout'][0]['offset'])]:
        if int.from_bytes(rom[at:at+4],'little')!=value:raise ValueError('startup renderer reference')
    if ui['normal_font_offset']!=m['extension']['normal_font_offset'] or not ui['native_font_restored_after_each_glyph']:raise ValueError('startup renderer font contract')
    for r in m['startup_welcome']['records']:
        if source[r['source_offset']:r['source_offset']+r['source_stored_bytes']]!=rom[r['source_offset']:r['source_offset']+r['source_stored_bytes']]:raise ValueError('native welcome source overwritten')
        packed=rom[r['offset']:r['offset']+r['stored_bytes']]
        payload,used=lz77_decompress(packed,0)
        if digest(packed)!=r['target_sha256'] or digest(payload)!=r['payload_sha256'] or used!=r['stored_bytes'] or len(payload)!=r['payload_bytes']:raise ValueError('startup welcome payload')
        if int.from_bytes(rom[r['reference']:r['reference']+4],'little')!=0x08000000+r['offset']:raise ValueError('startup welcome reference')
    from startup_footer_graphics import construct
    footer,meta=construct(source,json.loads((ROOT/'translations/startup_footer_graphics_ko.json').read_text(encoding='utf8')))
    if json.loads(json.dumps(meta))!=m['startup_footer'] or rom[meta['source_offset']:meta['source_offset']+meta['bytes']]!=footer:raise ValueError('startup footer construction')
    g=m['hangul_keyboard_glyphs']
    if not g['final_placement_verified'] or digest(rom[g['normal_jamo_offset']:g['normal_jamo_offset']+40*96])!=g['normal_bank_sha256']:raise ValueError('startup jamo placement')
    card_ranges=[]
    if m.get('navi_card_graphics'):
        from navi_card_graphics import construct
        packed,meta=construct(source,json.loads((ROOT/'translations/navi_card_graphics_ko.json').read_text(encoding='utf8')))
        at=meta['source_offset']
        if meta!=m['navi_card_graphics'] or rom[at:at+len(packed)]!=packed:raise ValueError('Navi card construction/placement')
        if rom[0x39760:0x39764]!=source[0x39760:0x39764]:raise ValueError('Navi card loader reference changed')
        prior_card=(ROOT/'poc/output/exe45_ko_development_native_keyboard_labels_v1.gba').read_bytes()
        if digest(prior_card)!='ec6fe6a156c0ec379866267fa2094b85773eb2f471723cc915c02e5ed8bbe40c' or not first_mail and len(prior_card)!=len(rom):raise ValueError('Navi card prior identity')
        card_ranges=[(at,at+len(packed))]
        if not first_mail and any(a!=b and not at<=i<at+len(packed) for i,(a,b) in enumerate(zip(prior_card,rom))):raise ValueError('Navi card change escaped bank')
    if m.get('native_keyboard_labels'):
        from native_keyboard_labels import construct
        patches,meta=construct(source,json.loads((ROOT/'translations/native_keyboard_labels_ko.json').read_text(encoding='utf8')))
        if json.loads(json.dumps(meta))!=m['native_keyboard_labels']:raise ValueError('native label manifest differs')
        for at,payload,_ in patches:
            if rom[at:at+len(payload)]!=payload:raise ValueError('native keyboard label final placement')
        for p in meta['pages']:
            at=p['descriptor_offset']
            if rom[at:at+16]!=source[at:at+16] or rom[p['map_reference']:p['map_reference']+4]!=source[p['map_reference']:p['map_reference']+4]:raise ValueError('native keyboard load metadata changed')
        prior=(ROOT/'poc/output/exe45_ko_development_startup_ui_v1_r7.gba').read_bytes()
        if digest(prior)!='1c0b9e9ba71d7a53d81e20b09f5fb95a74a903835de083059678f7bbef5e32de' or not first_mail and len(prior)!=len(rom):raise ValueError('native label prior cumulative identity')
        changed=[(at,at+len(payload)) for at,payload,_ in patches]+card_ranges
        if not first_mail and any(a!=b and not any(start<=i<end for start,end in changed) for i,(a,b) in enumerate(zip(prior,rom))):raise ValueError('native label change escaped page graphics')
    if first_mail:
        from first_mail import audit_layer
        audit_layer(product,source,rom,m)
    repro=product.with_name(product.stem+'_repro.gba')
    if not repro.exists() or repro.read_bytes()!=rom:raise ValueError('startup reproducible ROM absent/different')
    return dict(schema=1,product=str(product.relative_to(ROOT)),rom_sha256=digest(rom),rom_bytes=len(rom),source_sha256=digest(source),baseline_sha256=BASE_SHA,translated_units=m['translated_units'],added_units=sum(expected_extras.values())+(lineage['new_units'] if lineage else 0),selected_prior_assets_identical=not bool(lineage),cumulative_carry_scripts_identical=bool(lineage),merged_archives=sorted(lineage['merged_archives']) if lineage else [],explicit_added_assets=extras,primary_final_diff_audited=True,reproducible_byte_identical=True,unchanged_native_boundaries=native,automatic_keyboard_installed=False,hangul_save_abi_installed=False,runtime_tested=False,complete_integrated_request=False)
