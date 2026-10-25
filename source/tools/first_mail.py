"""Explicit first-mail scope from source-pinned existing drafts; no prose rewrite."""
import json,re,struct
from build_visibility_poc import ROOT,sha,require_hash
from tpl_literals import literals

SPECS={
 '6DD9AC':dict(draft='translations/story_mail_draft_ko.json',draft_sha='842f558f575cb1ffe0afe2f98e98ed59bd974d85d7964b24c961cb8c7e96000f',scripts=[0],count=23,size=2331,pointers=list(range(0x405F8,0x40658,4)),script_count=32,destination=0x0202B2F4,cap=8192,next=0x0202D2F4,consumer='normal-dialogue',rows=3,width=152),
 '6DD0B8':dict(draft='translations/batch500_016_mailbox_6DD0B8_draft_ko.json',draft_sha='379c2ba307848818f9e8476adf41e56b61337a19e82f7744dd7b99d98d03672f',scripts=[0,1,9,10,11],count=5,size=1412,pointers=list(range(0x41140,0x4119C,4)),script_count=130,destination=0x02024000,cap=8192,next=0x020262F4,consumer='normal-dialogue',rows=2,width=132),
 '6DD63C':dict(draft='translations/batch500_045_navi_mail_npcs_6DD63C_draft_ko.json',draft_sha='11ae8e6996c2da69b86d229ae36d509839a2adeb797a6dbc0ad56b225b22514a',scripts=[1,41],count=2,size=217,pointers=list(range(0x4057C,0x405DC,4)),script_count=42,destination=0x020262F4,cap=4096,next=0x020272F4,consumer='fixed-cell-big',rows=1,width=88),
}
FULL_HEADER_SCRIPTS=[1,2,3,4,5,6,7,16,17,18,19,20,21,22,23,24,25,26,27,28,29,41]
FULL_HEADER_LAYOUT='translations/full_mail_header_layout_v2.json'

def specifications(official=False,full_header=False):
    result={a:dict(s) for a,s in SPECS.items()}
    if official:result['6DD9AC'].update(scripts=[0,1,2,3],count=55)
    if official=='news':result['6DD9AC'].update(scripts=[0,1,2,3,8,9,10],count=77)
    if full_header:result['6DD63C'].update(scripts=FULL_HEADER_SCRIPTS,count=22)
    return result
def asset_path(archive,official=False,full_header=False):
    if archive=='6DD63C' and full_header:return 'analysis/full_mail_header_v1_r2/6DD63C_selected_asset.json'
    return f"analysis/{'news_mail_v1' if official=='news' else 'official_mail_v1' if official else 'first_mail_v2'}/{archive}_selected_asset.json"
def mode_for_manifest(m):
    paths={a['path'].replace('\\','/') for a in m['translation_assets']}
    return 'news' if asset_path('6DD9AC','news') in paths else asset_path('6DD9AC',True) in paths
def selected_units(archive,official=False,full_header=False):
    s=SPECS[archive];require_hash(ROOT/s['draft'],s['draft_sha']);draft=json.loads((ROOT/s['draft']).read_text(encoding='utf8'))
    units=[dict(id=u['id'],source=u['source'],translation=u['translation'],state='needs_review') for u in draft['units'] if int(u['id'].split(':')[1]) in specifications(official,full_header)[archive]['scripts']]
    if archive=='6DD63C' and full_header:
        proposed=json.loads((ROOT/FULL_HEADER_LAYOUT).read_text(encoding='utf8'))
        expected={'6DD63C:7:0':'또 1체 다크로이드','6DD63C:21:0':'의문의 오퍼레이터!',
                  '6DD63C:23:0':'오퍼레이터 정체!','6DD63C:25:0':'길거리 습격 발생'}
        if (proposed.get('release_eligible') is not False or proposed.get('consumer')!='fixed-cell-big'
                or proposed.get('max_line_advance')!=88 or proposed.get('layouts')!=expected):
            raise ValueError('full mail header layout authority changed')
        for u in units:
            if u['id'] in expected:u['translation']=expected[u['id']]
    if archive=='6DD9AC':
        layout=json.loads((ROOT/'translations/first_mail_layout_v2.json').read_text(encoding='utf8'))
        u=next(u for u in units if u['id']=='6DD9AC:0:22')
        if layout['id']!=u['id'] or layout['translation']!='부디 주의하시며,\n쾌적한 넷 배틀러 생활을\n즐기시길 바랍니다' or layout['translation'].replace('\n',' ')!=u['translation'].replace('\n',' ') or layout['release_eligible'] is not False:raise ValueError('first mail layout changes wording/authority')
        u['translation']=layout['translation']
        if official:
            proposed=json.loads((ROOT/'translations/official_mail_layout_v1.json').read_text(encoding='utf8'))
            if proposed['release_eligible'] is not False or set(proposed['layouts'])!={'6DD9AC:2:1','6DD9AC:2:3'}:raise ValueError('official mail proposal scope')
            for key,value in proposed['layouts'].items():
                u=next(u for u in units if u['id']==key)
                if key.endswith(':1') and value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('official layout changes words')
                if key.endswith(':3') and value!='자세한 건 조사 중이나,\n다크로이드의 정보가\n외부에 새지 않도록':raise ValueError('official individual wording candidate differs')
                u['translation']=value
        if official=='news':
            proposed=json.loads((ROOT/'translations/news_mail_layout_v1.json').read_text(encoding='utf8'))
            if proposed['release_eligible'] is not False or set(proposed['layouts'])!={'6DD9AC:9:2','6DD9AC:9:7','6DD9AC:10:0'}:raise ValueError('news layout scope')
            for key,value in proposed['layouts'].items():
                u=next(u for u in units if u['id']==key)
                if key=='6DD9AC:10:0':
                    if value!='메일 뉴스3호\n「의문의 오퍼레이터!」':raise ValueError('news individual title candidate differs')
                elif value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('news layout changes words')
                u['translation']=value
    return units
def validate_selected(asset):
    archive=asset['archive']
    full_header=asset.get('scope_variant')=='full-mail-header-v1'
    mode='news' if asset.get('scope_variant')=='news-mail-v1' else asset.get('scope_variant')=='official-mail-v1'
    if asset['units']!=selected_units(archive,mode,full_header):raise ValueError('first mail selected wording/layout mismatch')
    if full_header:
        if archive!='6DD63C' or len(asset['units'])!=22:raise ValueError('full mail header scope')
        if any('\n' in u['translation'] or len(u['translation'])*8>88 for u in asset['units']):raise ValueError('full mail header one-line extent')
    if archive=='6DD9AC':
        for u in asset['units']:
            rows=u['translation'].split('\n')
            if len(rows)==3:
                width=sum(12 if '\uac00'<=c<='\ud7a3' or c==',' else 8 if c==' ' else 11 for c in rows[2])
                if width>132:raise ValueError('first mail row3 overlaps native advance arrow')
def prepare(official=False,full_header=False):
    results=[]
    for archive,s in specifications(official,full_header).items():
        require_hash(ROOT/s['draft'],s['draft_sha']);draft=json.loads((ROOT/s['draft']).read_text(encoding='utf8'))
        require_hash(ROOT/draft['source_tpl']['path'],draft['source_tpl']['sha256'])
        units=selected_units(archive,official,full_header)
        tpl=(ROOT/draft['source_tpl']['path']).read_text(encoding='utf-8-sig')
        expected={x.key for x in literals(tpl) if int(x.key.split(':')[1]) in s['scripts']}
        if len(units)!=s['count'] or expected!={u['id'] for u in units}:raise ValueError('first mail literal population')
        asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=draft['source_sha256'],source_tpl=draft['source_tpl'],source_archive_sha256=draft['source_archive_sha256'],consumer=s['consumer'],context='First I.P.C. customer letter and Rockman normal mailbox; same source controls, page order, normal nickname and quest flags. Other mail bodies and Navi branches preserved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units)
        if official:asset['scope_variant']='official-mail-v1';asset['context']+=' Official bodies1/2/3 added under draft policy; acquisition route not established by display bench.'
        if official=='news':asset['scope_variant']='news-mail-v1';asset['context']+=' News bodies8/9/10 added; native quest commands kept; acquisition route not established by diagnostic.'
        if archive=='6DD63C' and full_header:
            asset['scope_variant']='full-mail-header-v1'
            asset['context']='All22 translated story-mail sender/title labels. Native 11-cell one-line extent retained; four individual title candidates shortened. Header/body lookup mapping and acquisition routes require runtime proof.'
        path=ROOT/asset_path(archive,official,full_header);path.parent.mkdir(exist_ok=True)
        data=json.dumps(asset,ensure_ascii=False,indent=2)+'\n'
        if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('preserve first mail selected input')
        if not path.exists():path.write_text(data,encoding='utf8')
        results.append(asset_path(archive,official,full_header))
    return results
def scopes(source,official=False,full_header=False):
    if source[0xEC158:0xEC15C]!=bytes.fromhex('11df7047'):raise ValueError('mail BIOS LZ decoder')
    if source[0x405F0:0x405F4]!=struct.pack('<I',0x020262F4) or source[0x4066C:0x40670]!=struct.pack('<I',0x0202B2F4) or source[0x4119C:0x411A0]!=struct.pack('<I',0x02024000):raise ValueError('mail fixed loader destinations')
    if source[0x411C4:0x411C8]!=struct.pack('<I',0x0202D2F4):raise ValueError('mail following title assets')
    result={}
    for a,s in specifications(official,full_header).items():
        refs=[m.start() for m in re.finditer(re.escape(struct.pack('<I',0x08000000+int(a,16))),source)]
        if refs!=s['pointers']:raise ValueError('mail pointer population')
        scope=dict(source_bytes=s['size'],pointers=s['pointers'],compressed=True,compression='BIOS type-10 literal-only, 4-byte aligned, zero-padded',decompression_destination=s['destination'],max_payload_bytes=s['cap'],next_scene_asset=s['next'],consumer=s['consumer'],max_literal_rows=s['rows'],max_line_advance=s['width'],literal_scripts=s['scripts'],complete_literal_scope=False,script_count=s['script_count'],preserve_literal_numerals=True,context='Source-pinned first mail native decompression and separate body/header consumers')
        if a=='6DD0B8':scope['literal_profiles']=[dict(scripts=[0,1],consumer='fixed-cell-big',literal_language='mmbn45s',max_literal_rows=1,max_line_advance=88),dict(scripts=[9,10,11],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=2,max_line_advance=132)]
        if a=='6DD63C':scope['literal_language']='mmbn45s'
        result[a]=scope
    return result

def audit_layer(product,source,rom,m):
    from verify_tpi_index import lz77_decompress
    prior=ROOT/'poc/output/exe45_ko_development_navi_card_names_v1.gba'
    old=json.loads(prior.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(prior,'0fb840efacfb3d90bdb0a752f459e3ea2065e1911233d46f9b7a9cb6cc77a00c')
    official=mode_for_manifest(m);full_header=any(a['path'].replace('\\','/')==asset_path('6DD63C',official,True) for a in m['translation_assets'])
    specs=specifications(official,full_header);scopes(source,official,full_header)
    extra=set(asset_path(a,official,full_header) for a in specs)
    from mission_mail_header import ASSET as mission_asset
    mission=any(a['path'].replace('\\','/')==mission_asset for a in m['translation_assets'])
    if mission:extra.add(mission_asset)
    batch=[]
    if m.get('pending_batch500'):
        from batch500_rom import entries
        batch=entries(source)
        for path,_,asset,_,_,_ in batch:
            extra.add(f"analysis/pending_insertion_500_rom/{asset['archive']}_selected_asset.json" if asset['consumer']=='fixed-cell-big' else path)
    second=[]
    if m.get('pending_batch500_002'):
        from batch500_002_rom import entries as entries002
        second=entries002(source)
        for path,_,asset,scope,_,_ in second:
            extra.add(f"analysis/pending_insertion_500_002_repartition_rom/{asset['archive']}_selected_asset.json" if scope['standard_relocation'] else path)
    third=[]
    if m.get('pending_batch500_003'):
        from batch500_003_rom import entries as entries003
        third=entries003(source)
        for path,_,asset,scope,_,_ in third:
            extra.add(f"analysis/pending_insertion_500_003_rom/{asset['archive']}_selected_asset.json" if scope['standard_relocation'] else path)
    fourth=[]
    if m.get('pending_batch500_004'):
        from batch500_004_rom import entries as entries004
        fourth=entries004(source)
        for _,_,asset,_,_,_ in fourth:
            extra.add(f"analysis/pending_insertion_500_004_rom/{asset['archive']}_selected_asset.json")
    fifth=[]
    if m.get('pending_batch500_005'):
        from batch500_005_rom import entries as entries005
        fifth=entries005(source)
        for _,_,asset,_,_,_ in fifth:
            extra.add(f"analysis/pending_insertion_500_005_rom/{asset['archive']}_selected_asset.json")
    sixth=[]
    if m.get('pending_batch500_006'):
        from batch500_006_rom import entries as entries006
        sixth=entries006(source)
        for _,_,asset,_,_,_ in sixth:
            extra.add(f"analysis/pending_insertion_500_006_rom/{asset['archive']}_selected_asset.json")
    if m.get('keyitem_rom',{}).get('mail_rom_reader',{}).get('archive'):
        from full_mail_body import ASSET
        extra.add(ASSET)
    lineage=None;lineage_assets=m['translation_assets']
    if m.get('pending_batch500_007'):
        from cumulative_batch500 import manifest_lineage
        lineage=manifest_lineage(source,rom,m);lineage_assets=lineage['parent_assets']
    if [a for a in lineage_assets if a['path'].replace('\\','/') not in extra]!=old['translation_assets']:raise ValueError('first mail previous selected assets changed')
    records={r['archive']:r for r in m['archives']}
    if official:
        from archive_scripts import verify_untouched_scripts
        previous_mail=ROOT/'poc/output/exe45_ko_development_first_mail_v2.gba'
        require_hash(previous_mail,'40d99164e2f0651f8e190afa7f7c1f73758117fe17bf111dbc86924840204635')
        pm=json.loads(previous_mail.with_suffix('.json').read_text(encoding='utf8'))
        previous_bytes=previous_mail.read_bytes();pr={r['archive']:r for r in pm['archives']}
        for a in specs:
            before=lz77_decompress(previous_bytes,pr[a]['rom_offset'])[0]
            after=lz77_decompress(rom,records[a]['rom_offset'])[0]
            if a=='6DD9AC':verify_untouched_scripts(before,after,32,{1,2,3,8,9,10} if official=='news' else {1,2,3})
            elif a=='6DD63C' and full_header:verify_untouched_scripts(before,after,42,set(FULL_HEADER_SCRIPTS))
            elif before!=after:raise ValueError('Official previous mailbox/header payload changed')
        if official=='news':
            previous_news=ROOT/'poc/output/exe45_ko_development_official_mail_v1_r2.gba'
            require_hash(previous_news,'e4c56544b754c84f464797d20657f88f7562f017c874c74d7f3ca0af2f024fbd')
            pn=json.loads(previous_news.with_suffix('.json').read_text(encoding='utf8'))
            r=next(r for r in pn['archives'] if r['archive']=='6DD9AC')
            verify_untouched_scripts(lz77_decompress(previous_news.read_bytes(),r['rom_offset'])[0],lz77_decompress(rom,records['6DD9AC']['rom_offset'])[0],32,{8,9,10})
    for r in old['archives']:
        if lineage and r['archive'] in lineage['merged_archives']:continue # explicit source-ID/script proof above
        n=records[r['archive']]
        for k in ['source_sha256','compiled_sha256','compiled_bytes','translated_units','layout','protected_controls_unchanged']:
            if r[k]!=n[k]:raise ValueError('first mail previous archive changed')
    def keys(writes):return {(w['offset'],w['bytes'],w['writer'],w['expected_hex']) for w in writes}
    expected=keys(old['expected_writes'])
    if m.get('pending_batch500_010'):
        from cumulative_batch500_010 import entries as entries010
        for _,row,asset,_,bound,_ in entries010(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_011'):
        from cumulative_batch500_011 import entries as entries011
        for _,row,asset,_,bound,_ in entries011(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_012'):
        from cumulative_batch500_012 import entries as entries012
        for _,row,asset,_,bound,_ in entries012(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_014'):
        from cumulative_batch500_014 import entries as entries014
        for _,row,asset,_,bound,_ in entries014(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_015'):
        from cumulative_batch500_015 import entries as entries015
        for _,row,asset,_,bound,_ in entries015(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_016'):
        from cumulative_batch500_016 import entries as entries016
        for _,row,asset,_,bound,_ in entries016(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_018'):
        from cumulative_batch500_018 import entries as entries018
        for _,row,asset,_,bound,_ in entries018(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_019'):
        from cumulative_batch500_019 import entries as entries019
        for _,row,asset,_,bound,_ in entries019(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_020'):
        from cumulative_batch500_020 import entries as entries020
        for _,row,asset,_,bound,_ in entries020(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if m.get('pending_batch500_021'):
        from cumulative_batch500_021 import entries as entries021
        for _,row,asset,_,bound,_ in entries021(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    if mission:expected.add((0x405E8,4,'archive 6DD864 relocation',source[0x405E8:0x405EC].hex()))
    if m.get('pending_batch500_022'):
        from cumulative_batch500_022 import entries as entries022
        for _,row,asset,_,bound,_ in entries022(source):
            if bound['parent'] is None:
                for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    for _,row,asset,_,_,_ in batch:
        if asset['consumer']=='fixed-cell-big':
            for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    for _,row,asset,scope,_,_ in second+third+fourth+fifth+sixth:
        if scope['standard_relocation']:
            for p in row['pointers']:expected.add((p,4,f"archive {asset['archive']} relocation",source[p:p+4].hex()))
    for a,s in specs.items():
        for p in s['pointers']:expected.add((p,4,f'archive {a} relocation',source[p:p+4].hex()))
    if keys(m['expected_writes'])!=expected:raise ValueError('first mail write population changed beyond three new archive references')
    for key in ['extension','fixedcell_extension']:
        for old_row,new_row in zip(old[key]['layout'][:2],m[key]['layout'][:2]):
            n=old_row.get('size',old_row.get('bytes'))
            if '·' in m.get('extra_glyph_metrics',{}) and '·' not in old.get('extra_glyph_metrics',{}):
                from font_extension_lineage import verify_middle_dot_lineage
                verify_middle_dot_lineage(old,m,prior.read_bytes(),rom)
                break
            if new_row.get('size',new_row.get('bytes'))!=n or sha(rom[new_row['offset']:new_row['offset']+n])!=old_row['sha256']:raise ValueError('first mail previous font/advance supply changed')
    observations=[]
    for a,s in specs.items():
        validate_selected(json.loads((ROOT/asset_path(a,official,full_header)).read_text(encoding='utf8')))
        r=records[a];c=r['compression'];packed=rom[r['rom_offset']:r['rom_offset']+c['stored_bytes']];payload,used=lz77_decompress(packed,0)
        if len(payload)>s['cap'] or used!=c['consumed_bytes'] or len(payload)!=r['compiled_bytes'] or sha(payload)!=r['compiled_sha256'] or sha(packed)!=c['stored_sha256']:raise ValueError('first mail final compressed placement')
        if r['translated_units']!=s['count'] or r['pointers']!=s['pointers']:raise ValueError('first mail scope population')
        if any(int.from_bytes(rom[p:p+4],'little')!=0x08000000+r['rom_offset'] for p in s['pointers']):raise ValueError('first mail relocated lookup')
        if rom[int(a,16):int(a,16)+s['size']]!=source[int(a,16):int(a,16)+s['size']]:raise ValueError('first mail old source bank overwritten')
        observations.append(dict(archive=a,units=s['count'],payload_bytes=len(payload),destination=s['destination'],cap=s['cap']))
    return observations
