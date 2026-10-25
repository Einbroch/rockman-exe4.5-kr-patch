"""Single-writer merge of source-bound new scripts into retained consumer scopes.

Analysis freezes a cumulative preflight. Product builds rederive every asset and
scope and bind them to that preflight; no source-only payload is injectable.
"""
import json
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash

BASE='poc/output/exe45_ko_development_middle_dot_v1.gba'
BASE_SHA='bd16c794be18178e84e0d473c0faff43c78eb1d492f8c7b9137265ff5aef3f0c'
SOURCE_PREFLIGHT='analysis/pending_insertion_500_007_partial_preflight_v1/preflight.json'
OUT='analysis/pending_insertion_500_007_cumulative_v2'
PREFLIGHT=OUT+'/preflight.json'
BATCH_ID='pending-insertion-500-007-cumulative'
PROFILE007=dict(base=BASE,base_sha=BASE_SHA,source_preflight=SOURCE_PREFLIGHT,out=OUT,batch_id=BATCH_ID,source_batch_id='pending-insertion-500-007-partial-source-only',archive_count=13,prior_cumulative=())
PROFILE008=dict(base='poc/output/exe45_ko_development_pending500_007_v1.gba',base_sha='c5078d66ffe11d4cc80960edb5484bf9bf3f8b4d533c28d178581345a4367656',source_preflight='analysis/pending_insertion_500_008_partial_preflight_v1/preflight.json',out='analysis/pending_insertion_500_008_cumulative_v1',batch_id='pending-insertion-500-008-cumulative',source_batch_id='pending-insertion-500-008-partial-source-only',archive_count=23,prior_cumulative=(PROFILE007,))
PROFILE009=dict(base='poc/output/exe45_ko_development_pending500_008_v1.gba',base_sha='be95c71b2cabc2ca2bb7587b34bc38aa1d528868704d7f97a73efd3c63986e76',source_preflight='analysis/pending_insertion_500_009_partial_preflight_v1/preflight.json',out='analysis/pending_insertion_500_009_cumulative_v1',batch_id='pending-insertion-500-009-cumulative',source_batch_id='pending-insertion-500-009-partial-source-only',archive_count=64,prior_cumulative=(PROFILE007,PROFILE008))
PROFILE010=dict(base='poc/output/exe45_ko_development_pending500_009_v1.gba',base_sha='0b623c19d8cbc944b555b26c2571c52d110e076af5fdb5aa0bedf52c0ac54096',source_preflight='analysis/pending_insertion_500_010_partial_preflight_v1/preflight.json',out='analysis/pending_insertion_500_010_cumulative_v1',batch_id='pending-insertion-500-010-cumulative',source_batch_id='pending-insertion-500-010-partial-source-only',archive_count=69,new_archives=['693778','693AA4','6989B0','698CB0','699194','69E5A8','69E61C','69E6BC','69EA0C','6A504C','6AA1A0','6AA730','6AAB08','6AAEB0','6AB600','6AE758','6B6050','6B60F0','6B6474','6B69A0'],prior_cumulative=(PROFILE007,PROFILE008,PROFILE009))

PROFILE011=dict(base='poc/output/exe45_ko_development_pending500_010_v1.gba',base_sha='8f05118a2dd8a7e452e81f81413b1c580fe9883493aae1e0d85c3d496075663a',source_preflight='analysis/pending_insertion_500_011_partial_preflight_v2/preflight.json',out='analysis/pending_insertion_500_011_cumulative_v1',batch_id='pending-insertion-500-011-cumulative',source_batch_id='pending-insertion-500-011-partial-source-only',archive_count=61,new_archives=['6BC2F8','6BC74C','6BCCD0','6C1B84','6C231C','6C2660','6C5F28','6C7608','6C79E8','6C7D04','6CB6C0','6CD068','6CD48C','6D1068','6D26A0','6D2700','6D27A0','6D2B34','6D3050','6D5EB0','704368'],prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010))

PROFILE012=dict(base='poc/output/exe45_ko_development_pending500_011_v1.gba',base_sha='c9a23d3cf303921cfaf33b8f053621c6a16cbe180e3723076a87a5721d084f86',source_preflight='analysis/pending_insertion_500_012_partial_preflight_v1/preflight.json',out='analysis/pending_insertion_500_012_cumulative_v1',batch_id='pending-insertion-268-012-cumulative',source_batch_id='pending-insertion-268-012-partial-source-only',units=268,archive_count=48,new_archives=['768800','768BD0','7B67C8','7C0970','7C0F8C','7C5CE0','7C714C','7CC6A0'],prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011))

PROFILE013=dict(base='poc/output/exe45_ko_development_pending500_012_v1.gba',base_sha='c64f3f8d00079a6f77c87b0fd97035ab018959fcc7412c785dcc563e5e97dc90',source_preflight='analysis/pending_insertion_500_013_partial_preflight_v1/preflight.json',out='analysis/pending_insertion_500_013_cumulative_v1',batch_id='pending-insertion-1-013-cumulative',source_batch_id='pending-insertion-1-013-partial-source-only',units=1,archive_count=1,new_archives=[],startup_carry=True,prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011,PROFILE012))

PROFILE014=dict(base='poc/output/exe45_ko_development_pending500_013_v1.gba',base_sha='00093bd660f08930abf2db43cd98f5ce93f64c563c9313496051f4472d86b20c',source_preflight='analysis/pending_insertion_500_014_partial_preflight_v1/preflight.json',out='analysis/pending_insertion_500_014_cumulative_v1',batch_id='pending-insertion-10-014-cumulative',source_batch_id='pending-insertion-10-014-partial-source-only',units=10,archive_count=3,new_archives=['7BDC90','7B4184','7B3C30'],manual_dot_proposals=True,prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011,PROFILE012,PROFILE013))

PROFILE015=dict(base='poc/output/exe45_ko_development_pending500_014_v1.gba',base_sha='6cdcae37d8682c03a909b08d3ddefea02ad825c6a272899c38bcc5f316be9245',source_preflight='analysis/pending_insertion_500_015_partial_preflight_v2/preflight.json',out='analysis/pending_insertion_500_015_cumulative_v1',batch_id='pending-insertion-6-015-cumulative',source_batch_id='pending-insertion-6-015-partial-source-only',units=6,archive_count=2,new_archives=['7C9C44'],manual_015_proposals=True,prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011,PROFILE012,PROFILE013,PROFILE014))

PROFILE016=dict(base='poc/output/exe45_ko_development_pending500_015_v1.gba',base_sha='a6d3b0330566374937857cb49b2f07475a6c590e73ac6873486556585a4f4d81',source_preflight='analysis/pending_insertion_500_016_preflight_v1/preflight.json',out='analysis/pending_insertion_500_016_cumulative_v1',batch_id='pending-insertion-500-016-cumulative',source_batch_id='pending-insertion-500-016-source-only',archive_count=24,new_archives=['659CB8','65AAE0','65AFA0','65B8E4','65B9E8','65E384','65E8B8','66B0D4','66CA84','66FD14','670568','671958','671F24','672238','67593C','675A20','6762A8','677774','677F64','67B47C','67BCF4','67CB70','67CED8','67D708'],prepared_016=True,prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011,PROFILE012,PROFILE013,PROFILE014,PROFILE015))

PROFILE017=dict(base='poc/output/exe45_ko_development_pending500_016_v1.gba',base_sha='d58330fba33d9656e90405309afc39496483aacce2df73908e62b53a4f64bd08',source_preflight='analysis/pending_insertion_500_017_preflight_v1/preflight.json',out='analysis/pending_insertion_500_017_cumulative_v1',batch_id='pending-insertion-500-017-cumulative',source_batch_id='pending-insertion-500-017-source-only',archive_count=6,new_archives=[],prepared_017=True,prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011,PROFILE012,PROFILE013,PROFILE014,PROFILE015,PROFILE016))

PROFILE018=dict(base='poc/output/exe45_ko_development_pending500_017_v1.gba',base_sha='73cb5ec4b297faaeb95f8ccb531096c753f8a5455adfb2c2d8a5cbe9f30f9106',source_preflight='analysis/pending_insertion_500_018_preflight_v2/preflight.json',out='analysis/pending_insertion_500_018_cumulative_v1',batch_id='pending-insertion-500-018-cumulative',source_batch_id='pending-insertion-500-018-source-only',archive_count=78,new_archives=['65E828', '664804', '664D84', '66A160', '66B8B0', '66BDE0', '66BF44', '66C978', '66FC98', '670DF4', '67133C', '671684', '672124', '675338', '676AE4', '677028', '6770B8', '677364', '677C94', '677E58', '67AD3C', '67B3D0', '67C4CC', '67D44C', '67D5F8', '682D68', '698424', '6A907C', '7BAEF8', '7BB31C'],prepared_018=True,startup_mail_carry=True,prior_cumulative=(PROFILE007,PROFILE008,PROFILE009,PROFILE010,PROFILE011,PROFILE012,PROFILE013,PROFILE014,PROFILE015,PROFILE016,PROFILE017))

PROFILE019=dict(base='poc/output/exe45_ko_development_pending500_018_v1.gba',base_sha='a8d39423bbd4792d948af4bea991dd8c56bb6d34dac8c1a7c570f0c3938f3241',source_preflight='analysis/pending_insertion_500_019_preflight_v3/preflight.json',out='analysis/pending_insertion_500_019_cumulative_v1',batch_id='pending-insertion-500-019-cumulative',source_batch_id='pending-insertion-500-019-conditional-plan',archive_count=133,new_archives=['65AA80','65AF54','65B74C','666430','66B950','66BE58','66BEF8','66C7D8','66F6A0','670E9C','6713B8','671638','676BA8','677318','67C578','67C9FC','67CA84','67CB24','6996DC','6B5FB0','6C7594'],prepared_019=True,prior_cumulative=PROFILE018['prior_cumulative']+(PROFILE018,))

PROFILE020=dict(base='poc/output/pending500_019_v1.gba',base_sha='38118847f8deeec0586b7c5b400a9dd15ec32a1875c174657fad3ee8029b8042',source_preflight='analysis/pending_insertion_500_020_preflight_v1/preflight.json',out='analysis/pending_insertion_500_020_cumulative_v1',batch_id='pending-insertion-500-020-cumulative',source_batch_id='pending-insertion-500-020-source-only',archive_count=52,new_archives=['7B7AF0','7B7EF8','7B9104','7BA26C','7BBE54','7C0668'],prepared_020=True,prior_cumulative=PROFILE019['prior_cumulative']+(PROFILE019,))

PROFILE021=dict(base='poc/output/pending500_020_v1.gba',base_sha='1e595b2113e446fa74be2c2e0c7737a0bf13bcbd7984114eb1c1df79b4580788',source_preflight='analysis/pending_insertion_500_021_preflight_v1/preflight.json',out='analysis/pending_insertion_500_021_cumulative_v1',batch_id='pending-insertion-500-021-cumulative',source_batch_id='pending-insertion-500-021-source-only',archive_count=20,new_archives=[],prepared_021=True,prior_cumulative=PROFILE020['prior_cumulative']+(PROFILE020,))

PROFILE022=dict(base='poc/output/pending500_021_v1.gba',base_sha='76d9cf6626436f4c683a49f9389f72c3c85b01b6d6b43461a466e32976ec7ac4',source_preflight='analysis/pending_insertion_500_022_raw_preflight_v1/preflight.json',out='analysis/pending_insertion_500_022_cumulative_v1',batch_id='pending-insertion-136-022-cumulative',source_batch_id='pending-insertion-136-022-raw-source-only',units=136,archive_count=4,new_archives=['7CB850'],prepared_022=True,supplemental_hint=True,prior_cumulative=PROFILE021['prior_cumulative']+(PROFILE021,))

def unit_count(profile):
    n=profile.get('units',500)
    if type(n) is not int or not 1<=n<=500:raise ValueError('Explicit batch unit denominator')
    return n

def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def frozen_write(path,value):
    data=json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('Frozen merge input changed: '+str(path))
    if not path.exists():path.write_text(data,encoding='utf8')

def derive(source,profile=PROFILE007,_prior_registry=None):
    if profile.get('prepared_022'):
        from prepare_pending500_022_raw import prepare as materialize022
        materialize022()
    if profile.get('prepared_021'):
        from prepare_pending500_021 import materialize as materialize021
        materialize021()
    if profile.get('prepared_020'):
        from prepare_pending500_020 import materialize as materialize020
        materialize020()
    if profile.get('prepared_019'):
        from prepare_batch500_016_inputs import prepare as materialize
        materialize('analysis/pending_insertion_500_019_selection_v1/selection.json','analysis/pending_insertion_500_019_inputs_v1',allow_carry=True)
    if profile.get('prepared_018'):
        from prepare_batch500_018_inputs import prepare as prepare_inputs018
        prepare_inputs018()
    if profile.get('prepared_017'):
        from prepare_batch500_017_inputs import prepare as prepare_inputs017
        prepare_inputs017()
    if profile.get('prepared_016'):
        from prepare_batch500_016_inputs import prepare as prepare_inputs
        prepare_inputs()
    if profile.get('manual_015_proposals'):
        from prepare_middle_dot015_inputs import prepare as prepare_world
        from prepare_middle_dot015_tutorial_inputs import prepare as prepare_tutorial
        prepare_world();prepare_tutorial()
    if profile.get('manual_dot_proposals'):
        from prepare_middle_dot014_inputs import prepare as prepare_wordings
        prepare_wordings()
    BASE,BASE_SHA,SOURCE_PREFLIGHT,OUT=(profile[k] for k in ('base','base_sha','source_preflight','out'))
    from build_development_patch import selected_scope,literal_scope
    from batch500_002_rom import entries as e2
    from batch500_003_rom import entries as e3
    from verify_tpi_index import parse_tpi
    from compare_archive_payloads import payload_of
    from prepare_repartition500 import layout_records
    from tpl_literals import resolve_units
    require_hash(ROOT/BASE,BASE_SHA)
    old=read(str((ROOT/BASE).with_suffix('.json').relative_to(ROOT)))
    if old['output_sha256']!=BASE_SHA or old['source_sha256']!=sha(source):raise ValueError('Merge baseline/source binding')
    pre=read(SOURCE_PREFLIGHT)
    if pre['batch_id']!=profile['source_batch_id'] or pre['source_sha256']!=sha(source) or pre['total_units']!=unit_count(profile) or pre['applied_id_intersection'] or pre['layout_candidates']:raise ValueError('Source-only batch contract')
    for k in ('selection','individual_layout'):require_hash(ROOT/pre[k]['path'],pre[k]['sha256'])
    old_ids={x['id'] for r in layout_records(old) for x in r['layout']}
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows={f"{r['offset']:06X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    # A top-level derivation verifies the declared ancestry in order. Pass the
    # already verified registry to the next link instead of recursively deriving
    # the same earlier links again. This is not a persistent result/hash cache.
    reg=deepcopy(_prior_registry) if _prior_registry is not None else read('tools/specs/exe45_dialogue_archives_v1.json')['archives']
    if _prior_registry is None:
        reg.update({a['archive']:s for entry in (e2,e3) for _,_,a,s,_,_ in entry(source) if s['standard_relocation']})
    if profile['prior_cumulative'] and _prior_registry is None:
        from batch500_004_rom import entries as e4
        from batch500_005_rom import entries as e5
        from batch500_006_rom import entries as e6
        reg.update({a['archive']:s for entry in (e4,e5,e6) for _,_,a,s,_,_ in entry(source) if s['standard_relocation']})
        for prior in profile['prior_cumulative']:
            reg.update({a['archive']:s for _,_,a,s,_,_ in entries(source,prior,_prior_registry=reg)})
    if profile.get('startup_carry'):
        if unit_count(profile)!=1 or profile['archive_count']!=1 or [r['archive'] for r in pre['archives']]!=['70904C'] or pre['archives'][0]['selected_ids']!=['70904C:10:0']:raise ValueError('Explicit startup normal-notification scope')
        from startup_ui import scope as startup_scope
        if '70904C' in reg:raise ValueError('Startup carry scope already registered')
        reg['70904C']=startup_scope()
    if profile.get('startup_mail_carry'):
        from startup_ui import followup_scopes
        if '65B220' in reg:raise ValueError('Startup mail scope already registered')
        reg['65B220']=followup_scopes()['65B220']
    paths={r['archive']:r for r in old['translation_assets'] if 'archive' in r}
    records={r['archive']:r for r in old['archives']}
    if profile.get('prepared_018') or profile.get('prepared_019') or profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022'):
        # Inherited provenance entries are explicitly read-only, not writers.
        # Admit one actual primary owner; never resolve it by asset-list order.
        for row in pre['archives']:
            arc=row['archive']
            if arc not in records:continue
            owners=[r for r in old['translation_assets'] if r.get('archive')==arc and not r.get('scope','').startswith('read-only inherited')]
            if len(owners)!=1:raise ValueError('Ambiguous primary carry writer '+arc)
            paths[arc]=owners[0]
    new_ids=set();result=[]
    for r in pre['archives']:
        a=r['archive'];parent=paths.get(a)
        require_hash(ROOT/r['draft_path'],r['draft_sha256']);draft=read(r['draft_path'])
        require_hash(ROOT/draft['source_tpl']['path'],draft['source_tpl']['sha256'])
        row=rows[a]
        if parent is None:
            if a not in profile.get('new_archives',[]) or a in reg or a in records or any(key.startswith(a+':') for key in old_ids):raise ValueError('Unregistered new archive contract')
            carry={k:deepcopy(draft[k]) for k in ('schema','policy','archive','source_sha256','source_tpl','source_archive_sha256','review')}
            carry.update(consumer='normal-dialogue',units=[])
            scope=dict(consumer='normal-dialogue',complete_literal_scope=False,literal_scripts=[],literal_ids=[],script_count=r['script_count'],max_literal_rows=3,max_line_advance=132,literal_language='mmbn45',preserve_literal_numerals=True,standard_relocation=True,source_bytes=row['size'],pointers=row['pointers'],compressed=False)
        else:
            require_hash(ROOT/parent['path'],parent['sha256']);carry=read(parent['path']);scope=selected_scope(reg[a],carry)
        ids=set(r['selected_ids']);units=[deepcopy(u) for u in draft['units'] if u['id'] in ids]
        if [u['id'] for u in units]!=r['selected_ids'] or ids&old_ids or ids&new_ids:raise ValueError('New ordered ID binding')
        if profile.get('prepared_017') or profile.get('prepared_018') or profile.get('prepared_019') or profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022'):
            layouts=read(pre['individual_layout']['path'])['layouts']
            for u in units:
                if u['id'] not in layouts:continue
                value=layouts[u['id']]
                if value.replace('\n',' ')!=u['translation'].replace('\n',' ') or value.count('\n')!=u['translation'].count('\n'):raise ValueError('017 protected wording/topology')
                u['translation']=value
        carry_ids={u['id'] for u in carry['units']}
        if carry_ids!={x['id'] for x in records.get(a,{}).get('layout',[])}:raise ValueError('Carry source-ID population')
        scripts={int(u['id'].split(':')[1]) for u in units}
        if scripts&set(scope['literal_scripts']):raise ValueError('New scripts overlap carry')
        row=rows[a];native=payload_of(source,row)
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0] or sha(native)!=draft['source_archive_sha256'] or carry['source_archive_sha256']!=sha(native):raise ValueError('Raw source merge contract')
        asset=deepcopy(carry);asset.pop('scope_variant',None)
        if profile.get('prepared_016') or profile.get('prepared_017') or profile.get('prepared_018') or profile.get('prepared_019') or profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022'):
            asset['source_draft_links']=deepcopy(draft['source_draft_links'])
        if profile.get('prepared_017') or profile.get('prepared_018') or profile.get('prepared_019') or profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022'):
            asset['explicit_line_layout']=deepcopy(pre['individual_layout'])
        if profile.get('manual_dot_proposals') or profile.get('manual_015_proposals'):
            asset['manual_wording_proposals']=deepcopy(draft['manual_wording_proposals'])
        # Explicit schema2 wording-link resolution; pinned parent retains links.
        asset['schema']=1;asset.pop('wordings',None)
        asset['units']=deepcopy(resolve_units(carry))+units
        asset['cumulative_merge']=dict(parent=parent,new_draft=dict(path=r['draft_path'],sha256=r['draft_sha256']),new_ids=r['selected_ids'])
        merged=deepcopy(scope);merged.pop('variants',None)
        merged['literal_scripts']=sorted(set(scope['literal_scripts'])|scripts)
        merged['literal_ids']=[u['id'] for u in asset['units']]
        merged['complete_literal_scope']=False;merged['standard_relocation']=True
        merged['literal_profiles']=deepcopy(scope.get('literal_profiles',[]))+[dict(scripts=sorted(scripts),consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=132)]
        if (profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022')) and r.get('fullbox_capacity_profiles'):
            merged['literal_profiles'][-1]['max_line_advance']=180
            merged['fullbox_capacity_profiles']=deepcopy(scope.get('fullbox_capacity_profiles',[]))+deepcopy(r['fullbox_capacity_profiles'])
        merged['protected_numeral_ids']=scope.get('protected_numeral_ids',[])+r['selected_ids']
        if (profile.get('prepared_019') or profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022')) and r.get('nickname_capacity_profiles'):
            merged['nickname_capacity_profiles']=deepcopy(scope.get('nickname_capacity_profiles',[]))+deepcopy(r['nickname_capacity_profiles'])
        # Prove retained per-literal consumer contracts, not just wording.
        for key in carry_ids:
            before=literal_scope(scope,key);after=literal_scope(merged,key)
            for field in ('consumer','literal_language','max_literal_rows','max_line_advance'):
                if before.get(field)!=after.get(field):raise ValueError('Carry consumer changed '+key)
        path=OUT+f'/{a}_selected_asset.json'
        result.append((path,row,asset,merged,r,native,parent,records.get(a)))
        new_ids|=ids
    if len(new_ids)!=unit_count(profile) or len(result)!=profile['archive_count']:raise ValueError('Merge denominator')
    if {x[2]['archive'] for x in result if x[6] is None}!=set(profile.get('new_archives',[])):raise ValueError('New archive denominator')
    return result

def prepare(profile=PROFILE007):
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256'])
    paths=[]
    for path,_,asset,_,_,_,_,_ in derive(sp.read_bytes(),profile):
        frozen_write(ROOT/path,asset);paths.append(path)
    return paths

def entries(source,profile=PROFILE007,_prior_registry=None):
    PREFLIGHT=profile['out']+'/preflight.json';BATCH_ID=profile['batch_id'];BASE_SHA=profile['base_sha'];SOURCE_PREFLIGHT=profile['source_preflight']
    pre=read(PREFLIGHT)
    if pre['batch_id']!=BATCH_ID or pre['new_units']!=unit_count(profile) or pre['source_sha256']!=sha(source) or pre['baseline_sha256']!=BASE_SHA:raise ValueError('Cumulative preflight binding')
    require_hash(ROOT/SOURCE_PREFLIGHT,pre['source_preflight_sha256'])
    bounds={r['archive']:r for r in pre['archives']};result=[]
    for path,row,asset,scope,_,native,parent,_ in derive(source,profile,_prior_registry=_prior_registry):
        bound=bounds.pop(asset['archive']);require_hash(ROOT/path,bound['asset_sha256'])
        if read(path)!=asset or scope!=bound['scope'] or parent!=bound['parent'] or bound['new_ids']!=asset['cumulative_merge']['new_ids']:raise ValueError('Merged product input differs')
        result.append((path,row,asset,scope,bound,native))
    if bounds:raise ValueError('Unknown merged preflight archive')
    return result

def replace_paths(paths,profile=PROFILE007):
    PREFLIGHT=profile['out']+'/preflight.json'
    pre=read(PREFLIGHT);replacements={r['parent']['path'].replace('\\','/'):r['asset_path'] for r in pre['archives'] if r['parent'] is not None};found=set();out=[]
    for path in paths:
        key=path.replace('\\','/')
        if key in replacements:found.add(key);out.append(replacements[key])
        else:out.append(path)
    if found!=set(replacements):raise ValueError('Missing carry writer in cumulative recipe')
    out.extend(r['asset_path'] for r in pre['archives'] if r['parent'] is None)
    return out

def verify_product_lineage(source,rom,meta,profile=PROFILE007):
    """Exact-ID delta plus every previous clone/script, not an archive exemption."""
    from verify_pending500_002_rom import clones,at_path,read_payload
    from archive_scripts import verify_untouched_scripts
    BASE=profile['base'];BASE_SHA=profile['base_sha']
    old=read(str((ROOT/BASE).with_suffix('.json').relative_to(ROOT)))
    require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes()
    merged={a['archive']:(path,a,s,p) for path,_,a,s,p,_ in entries(source,profile)}
    before={x['id'] for _,r in clones(old) for x in r['layout']};after={x['id'] for _,r in clones(meta) for x in r['layout']}
    selected={key for _,_,_,p in merged.values() for key in p['new_ids']}
    extra_manifest=None;delta=unit_count(profile)
    if profile.get('supplemental_hint'):
        from hint_rom_data import verify_final as verify_hints,MANIFEST
        hint_ids=verify_hints(source,rom,meta['keyitem_rom'])
        if selected&hint_ids or len(hint_ids)!=364:raise ValueError('022 separate raw/hint IDs')
        selected|=hint_ids;delta+=len(hint_ids);extra_manifest=MANIFEST
    if before-after or after-before!=selected or len(selected)!=delta or meta['translated_units']!=old['translated_units']+delta or len(meta['archives'])!=len(old['archives'])+len(profile.get('new_archives',[])):raise ValueError('Actual cumulative batch population')
    current={r['archive']:r for r in meta['archives']};preserved=[];changed=[]
    for path,r in clones(old):
        now=current[r['archive']] if path[0]=='archives' else at_path(meta,path)
        old_raw=read_payload(base,r);raw=read_payload(rom,now)
        if path[0]=='archives' and r['archive'] in merged:
            _,asset,scope,p=merged[r['archive']]
            scripts={int(k.split(':')[1]) for k in p['new_ids']}
            kept=verify_untouched_scripts(old_raw,raw,scope['script_count'],scripts)
            if sha(raw)!=p['compiled_sha256'] or now['translated_units']!=len(asset['units']) or now['pointers']!=r['pointers'] or {x['id'] for x in now['layout']}!={u['id'] for u in asset['units']}:raise ValueError('Final merged payload binding')
            if any(int.from_bytes(rom[ptr:ptr+4],'little')!=0x08000000+now['rom_offset'] for ptr in now['pointers']):raise ValueError('Final merged archive pointer bytes')
            old_layout={x['id']:x for x in r['layout']};new_layout={x['id']:x for x in now['layout']}
            if any(new_layout[k]!=v for k,v in old_layout.items()):raise ValueError('Carry display metrics changed')
            changed.append(dict(archive=r['archive'],new_units=len(p['new_ids']),preserved_scripts=kept))
        else:
            if old_raw!=raw or r['compiled_sha256']!=now['compiled_sha256']:raise ValueError('Previous payload changed '+str(path))
            if any(r.get(key)!=now.get(key) for key in ('layout','translated_units','source_sha256','protected_controls_unchanged')):raise ValueError('Previous unchanged consumer metadata changed '+str(path))
            preserved.append('/'.join(map(str,path)))
    added=[]
    for name in profile.get('new_archives',[]):
        _,asset,scope,p=merged[name];now=current[name];raw=read_payload(rom,now)
        if name in {r['archive'] for r in old['archives']} or sha(raw)!=p['compiled_sha256'] or now['translated_units']!=len(asset['units']) or {x['id'] for x in now['layout']}!={u['id'] for u in asset['units']} or now['pointers']!=scope['pointers']:raise ValueError('Final new archive binding')
        if any(int.from_bytes(rom[ptr:ptr+4],'little')!=0x08000000+now['rom_offset'] for ptr in scope['pointers']):raise ValueError('Final new archive pointer bytes')
        offset=int(name,16);native=source[offset:offset+scope['source_bytes']]
        if rom[offset:offset+len(native)]!=native:raise ValueError('New archive source storage overwritten')
        kept=verify_untouched_scripts(native,raw,scope['script_count'],{int(k.split(':')[1]) for k in p['new_ids']})
        added.append(dict(archive=name,new_units=len(p['new_ids']),unselected_source_scripts=kept))
    original_assets=[];found=set()
    by_path={path.replace('\\','/'):(a,p) for path,a,_,p in merged.values()}
    for entry in meta['translation_assets']:
        key=entry['path'].replace('\\','/')
        if key==extra_manifest:
            require_hash(ROOT/key,entry['sha256'])
            if entry.get('scope')!='022 guarded hint ROM clone inputs':raise ValueError('022 supplemental manifest scope')
            continue
        if key in by_path:
            asset,p=by_path[key];require_hash(ROOT/entry['path'],entry['sha256'])
            if entry['sha256']!=p['asset_sha256'] or entry['archive']!=asset['archive']:raise ValueError('Final merged asset hash')
            if p['parent'] is not None:original_assets.append(p['parent'])
            found.add(key)
        else:original_assets.append(entry)
    if profile.get('prepared_018') or profile.get('prepared_019') or profile.get('prepared_020') or profile.get('prepared_021') or profile.get('prepared_022'):
        # A merged writer removes scope_variant; its immutable parent asset
        # retains the inherited provenance chain formerly projected as extra
        # read-only metadata rows. Normalize only independently verified links.
        inherited=[]
        for entry in old['translation_assets']:
            if entry.get('archive') not in merged or not entry.get('scope','').startswith('read-only inherited') or entry in original_assets:continue
            parent=merged[entry['archive']][3]['parent'];links=set();seen=set()
            while parent is not None:
                pair=(parent['path'].replace('\\','/'),parent['sha256'])
                if pair in seen:raise ValueError('Inherited provenance cycle')
                seen.add(pair);require_hash(ROOT/parent['path'],parent['sha256']);links.add(pair)
                parent=read(parent['path']).get('parent_asset')
            if (entry['path'].replace('\\','/'),entry['sha256']) not in links:raise ValueError('Unrepresented inherited carry provenance')
            inherited.append(entry)
        if original_assets!=[entry for entry in old['translation_assets'] if entry not in inherited]:raise ValueError('018 primary/inherited input lineage')
        original_assets=deepcopy(old['translation_assets'])
    if found!=set(by_path) or original_assets!=old['translation_assets']:raise ValueError('Cumulative selected asset lineage')
    if extra_manifest and sum(e['path'].replace('\\','/')==extra_manifest for e in meta['translation_assets'])!=1:raise ValueError('022 supplemental manifest population')
    return dict(merged_archives=set(merged),parent_assets=original_assets,new_units=delta,preserved_payloads=preserved,merged=changed,added_archives=added)

def manifest_lineage(source,rom,meta):
    """Verify each carry link on its exact artifact before ancestry normalization."""
    if meta.get('field_b0_hints_023'):
        from field_b0_rom_data import verify_final as verify_b0,MANIFEST as B0_MANIFEST
        from verify_pending500_002_rom import clones
        selected=verify_b0(source,rom,meta['keyitem_rom'])
        projected=deepcopy(meta)
        del projected['field_b0_hints_023']
        del projected['keyitem_rom']['b0_hint_archives']
        projected['translated_units']-=len(selected)
        if {u['id'] for _,r in clones(projected) for u in r['layout']}&selected:raise ValueError('B0/source old identity overlap')
        assets=[e for e in projected['translation_assets'] if e['path'].replace('\\','/')==B0_MANIFEST]
        if len(assets)!=1 or assets[0]['sha256']!=sha((ROOT/B0_MANIFEST).read_bytes()):raise ValueError('B0 lineage manifest')
        projected['translation_assets']=[e for e in projected['translation_assets'] if e not in assets]
        result=manifest_lineage(source,rom,projected)
        result['new_units']+=len(selected)
        result['supplemental_b0_verified_units']=len(selected)
        return result
    profile=next((p for flag,p in [('pending_batch500_022',PROFILE022),('pending_batch500_021',PROFILE021),('pending_batch500_020',PROFILE020),('pending_batch500_019',PROFILE019),('pending_batch500_018',PROFILE018),('pending_batch500_017',PROFILE017),('pending_batch500_016',PROFILE016),('pending_batch500_015',PROFILE015),('pending_batch500_014',PROFILE014),('pending_batch500_013',PROFILE013),('pending_batch500_012',PROFILE012),('pending_batch500_011',PROFILE011),('pending_batch500_010',PROFILE010),('pending_batch500_009',PROFILE009),('pending_batch500_008',PROFILE008)] if meta.get(flag)),PROFILE007)
    current=verify_product_lineage(source,rom,meta,profile)
    if not profile['prior_cumulative']:return current
    prior=read(profile['base'].replace('.gba','.json'));require_hash(ROOT/profile['base'],profile['base_sha'])
    ancestry=manifest_lineage(source,(ROOT/profile['base']).read_bytes(),prior)
    if current['parent_assets']!=prior['translation_assets']:raise ValueError('Carry chain asset identity')
    current['parent_assets']=ancestry['parent_assets'];current['merged_archives']|=ancestry['merged_archives'];current['new_units']+=ancestry['new_units']
    current['added_archives']+=ancestry['added_archives']
    return current
