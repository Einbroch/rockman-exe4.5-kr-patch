"""Source-pinned full catalog backlog; never infer translations or exclusions."""
import argparse,json,re
from collections import Counter
from pathlib import Path
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals,resolve_units
from verify_tpi_index import parse_tpi
from build_development_patch import payload_of
from build_visibility_poc import require_hash

def inherited_guts_input(item,manifest):
    """Explicit read-only dependency is not a second selected archive writer."""
    if item.get('scope') in ('authored UI delta authority','authored input UI delta21 authority','authored initialization UI delta authority'):
        from input_remaining import DELTA
        from verify_calendar_date_save_draft import ASSET
        path=Path(item['path']).as_posix()
        if item['scope']=='authored initialization UI delta authority':
            from save_initialize import DELTA as INIT_DELTA
            allowed={DELTA,ASSET,INIT_DELTA}
        else:allowed={DELTA,ASSET} if item['scope']=='authored UI delta authority' else {DELTA}
        if path not in allowed or item.get('archive')!='6368E8':raise ValueError('authored delta identity')
        writers=[a for a in manifest['translation_assets'] if a.get('archive')=='6368E8' and 'scope' not in a]
        if len(writers)!=1:raise ValueError('one common writer required')
        writer=ROOT/writers[0]['path'];require_hash(writer,writers[0]['sha256']);asset=read(writer)
        if item['scope']=='authored initialization UI delta authority':
            from save_initialize import validate
        elif item['scope']=='authored UI delta authority':
            from calendar_date_save import validate
        else:
            from input_remaining import validate
        validate(asset);selected={u['id']:u for u in asset['units']}
        delta=read(ROOT/path)
        if any(selected.get(u['id'])!=u for u in delta['units']):raise ValueError('delta not in selected writer')
        return True
    if item.get('scope') in ('read-only inherited55 preset units','read-only inherited38 preset units','read-only inherited17 preset units'):
        expected={'read-only inherited55 preset units':55,'read-only inherited38 preset units':38,'read-only inherited17 preset units':17}[item['scope']]
        if item.get('carry_units')!=expected:raise ValueError('UI inherited population')
        if item['carry_units']==55:
            from save_initialize import PARENT,GENERATED as CHILD,PARENT_SHA,validate
            accepted=(None,)
        elif item['carry_units']==38:
            from calendar_date_save import PARENT,GENERATED as CHILD,PARENT_SHA,validate
            accepted=(None,'read-only inherited55 preset units')
        else:
            from input_remaining import PARENT,GENERATED as CHILD,PARENT_SHA,validate
            accepted=(None,'read-only inherited38 preset units')
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='6368E8' or item.get('sha256')!=PARENT_SHA:raise ValueError('UI inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='6368E8' and a.get('scope') in accepted]
        if len(children)!=1:raise ValueError('one UI child required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited16 preset units':
        from input_heading import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='6368E8' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=16:raise ValueError('heading inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='6368E8' and a.get('scope') in (None,'read-only inherited17 preset units')]
        if len(children)!=1:raise ValueError('one heading writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited13 preset units':
        from input_confirmation import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='6368E8' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=13:raise ValueError('confirmation inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='6368E8' and a.get('scope') in (None,'read-only inherited16 preset units')]
        if len(children)!=1:raise ValueError('one confirmation writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited12 preset units':
        from possessions_statistics import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='6368E8' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=12:raise ValueError('statistics inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='6368E8' and a.get('scope') in (None,'read-only inherited13 preset units')]
        if len(children)!=1:raise ValueError('one statistics writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited7 preset units':
        from calendar_frequency_names import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='6368E8' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=7:raise ValueError('frequency inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='6368E8' and a.get('scope') in (None,'read-only inherited12 preset units')]
        if len(children)!=1:raise ValueError('one frequency names writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited54 calendar units':
        from gutsman_calendar_inventory import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=54:raise ValueError('inventory inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='665698' and 'scope'not in a]
        if len(children)!=1:raise ValueError('one inventory writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited45 calendar units':
        from gutsman_calendar_schedule_delete import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=45:raise ValueError('schedule deletion inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited54 calendar units')]
        if len(children)!=1:raise ValueError('one schedule deletion writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited22 calendar units':
        from gutsman_calendar_management import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=22:raise ValueError('management inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited45 calendar units')]
        if len(children)!=1:raise ValueError('one calendar management writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited18 calendar units':
        from gutsman_calendar_navigation import PARENT,CHILD,PARENT_SHA,validate
        if Path(item.get('path','')).as_posix()!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=18:raise ValueError('navigation inherited identity')
        children=[a for a in manifest['translation_assets'] if Path(a['path']).as_posix()==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited22 calendar units')]
        if len(children)!=1:raise ValueError('one calendar navigation writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope') in ('read-only inherited15 anniversary units','read-only inherited5 anniversary units'):
        from calendar_anniversary_confirmation import PARENTS,DIALOGUE,LABELS,validate
        arc=item['archive'];parent,digest,count,_=PARENTS[arc];child=DIALOGUE if arc=='665698' else LABELS
        if item['path'].replace('\\','/')!=parent or item.get('sha256')!=digest or item.get('carry_units')!=count:raise ValueError('anniversary confirmation inherited identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==child and a.get('archive')==arc]
        if len(children)!=1:raise ValueError('one anniversary confirmation composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate(read(p));return True
    if item.get('scope')=='read-only inherited4 preset units':
        from calendar_anniversary_labels import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='6368E8' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=4:raise ValueError('anniversary preset parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='6368E8']
        if len(children)!=1:raise ValueError('one anniversary fixed-cell writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited14 calendar units':
        from gutsman_calendar_anniversary import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=14:raise ValueError('anniversary dialogue parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='665698']
        if len(children)!=1:raise ValueError('one anniversary dialogue writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited10 calendar units':
        from gutsman_calendar_register import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=10:raise ValueError('calendar register inherited parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited14 calendar units')]
        if len(children)!=1:raise ValueError('one calendar register composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited7 calendar units':
        from gutsman_calendar_home import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=7:raise ValueError('calendar home inherited parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited10 calendar units')]
        if len(children)!=1:raise ValueError('one calendar home composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited4 calendar units':
        from gutsman_calendar_confirmation import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=4:raise ValueError('confirmation inherited parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited7 calendar units')]
        if len(children)!=1:raise ValueError('one confirmation composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited2 calendar units':
        from gutsman_calendar_content import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='665698' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=2:raise ValueError('calendar inherited parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='665698' and a.get('scope') in (None,'read-only inherited4 calendar units')]
        if len(children)!=1:raise ValueError('one calendar composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited5 alarm units':
        from gutsman_alarm_meal import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='66651C' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=5:raise ValueError('meal inherited parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='66651C']
        if len(children)!=1:raise ValueError('one meal composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')=='read-only inherited3 alarm units':
        from gutsman_alarm_followup import PARENT,CHILD,PARENT_SHA,validate_parent
        if item.get('path','').replace('\\','/')!=PARENT or item.get('archive')!='66651C' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=3:raise ValueError('alarm inherited parent identity')
        children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')==CHILD and a.get('archive')=='66651C']
        if len(children)!=1:raise ValueError('one alarm composite writer required')
        p=ROOT/children[0]['path'];require_hash(p,children[0]['sha256']);validate_parent(read(p));return True
    if item.get('scope')!='read-only inherited31 units':return False
    from gutsman_chipquest_model import PARENT_SHA,validate_parent
    if item.get('path')!='translations\\gutsman_pet_talk_ko.json' and item.get('path')!='translations/gutsman_pet_talk_ko.json':raise ValueError('inherited parent path')
    if item.get('archive')!='66A844' or item.get('sha256')!=PARENT_SHA or item.get('carry_units')!=31:raise ValueError('inherited parent role/identity')
    children=[a for a in manifest['translation_assets'] if a['path'].replace('\\','/')=='translations/gutsman_pet_chipquest_ko.json' and a.get('archive')=='66A844']
    if len(children)!=1:raise ValueError('one selected Guts composite writer required')
    child=children[0];p=ROOT/child['path'];require_hash(p,child['sha256']);validate_parent(read(p));return True

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',default='poc/output/exe45_ko_development_numberman_return_v1.json');ap.add_argument('--source-dir',default='analysis/full_scope_v1/source_tpl');ap.add_argument('--out',default='analysis/full_scope_v1');a=ap.parse_args()
    cfg=read(ROOT/'project.json');source=ROOT/cfg['source_profile']['filename'];require_hash(source,cfg['source_profile']['sha256']);rom=source.read_bytes()
    catalog=ROOT/cfg['text_catalog']['path'];require_hash(catalog,cfg['text_catalog']['sha256']);rows=parse_tpi(catalog)
    manifest_path=ROOT/a.manifest;m=read(manifest_path);require_hash(manifest_path.with_suffix('.gba'),m['output_sha256'])
    directory=ROOT/a.source_dir;files=sorted(directory.glob('*.tpl'));lookup={p.stem.upper():p for p in files}
    if len(rows)!=732 or len(lookup)!=732 or set(lookup)!={f"{r['offset']:X}" for r in rows}:raise ValueError('catalog/extraction population mismatch')
    selected={};asset_hashes={};graphics=[]
    for item in m['translation_assets']:
        path=ROOT/item['path'];require_hash(path,item['sha256']);asset=read(path);asset_hashes[str(path.relative_to(ROOT))]=item['sha256']
        if inherited_guts_input(item,m):continue
        if path.name in ('equipment_attack_caption_ko.json','calendar_frequency_graphics_ko.json'):
            if 'text count unchanged' not in item.get('scope','') and 'text units unchanged' not in item.get('scope',''):raise ValueError('graphics scope mismatch')
            graphics.append(dict(path=item['path'],sha256=item['sha256'],scope=item['scope'],units=asset.get('units',[{k:asset[k] for k in ('id','source','translation')}]) if 'units' not in asset else asset['units']))
            continue
        for u in resolve_units(asset):
            if u['id'] in selected:
                # The registered raw-ROM clone deliberately reuses the one
                # already selected bounded-RAM empty message; count it once.
                if (u['id']=='709408:32:0' and u==selected[u['id']] and 'keyitem_rom' in m and
                    path.name=='keyitem_full_rom_ko.json' and item.get('scope')=='full39 raw-ROM clone; existing empty unit counted once' and
                    m['keyitem_rom']['archive']['translated_units']==len(resolve_units(asset))==39):continue
                raise ValueError('duplicate selected unit')
            selected[u['id']]=u
    records=[];archives=[];errors=[];seen=set();language=Counter();statuses=Counter()
    jp=re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
    registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']
    for row in rows:
        archive=f"{row['offset']:X}";p=lookup[archive];tpl=p.read_text(encoding='utf-8-sig')
        try:items=literals(tpl)
        except ValueError as exc:errors.append(dict(archive=archive,error=str(exc),source_tpl_sha256=sha(p.read_bytes())));continue
        payload=payload_of(rom,row);counts=Counter()
        for x in items:
            if x.key in seen:raise ValueError('global duplicate literal key')
            seen.add(x.key);u=selected.get(x.key);count=len(jp.findall(x.text))
            if u and u['source']!=x.text:raise ValueError('selected source baseline mismatch '+x.key)
            # Non-Japanese literals still belong to the finite inventory;
            # ASCII names/symbols require review, not automatic exclusion.
            status='selected_in_current_rom' if u else 'unselected_japanese' if count else 'unselected_non_japanese_review'
            counts[status]+=1;statuses[status]+=1;language[x.language]+=1
            records.append(dict(id=x.key,archive=archive,language=x.language,source=x.text,source_chars=len(x.text),japanese_chars=count,status=status,translation=u['translation'] if u else None,source_tpl_sha256=sha(p.read_bytes()),source_payload_sha256=sha(payload),catalog_row=row['line'],registered_consumer=registry.get(archive,{}).get('consumer'),context_status='registered_scene_requires_unit_review' if archive in registry else 'consumer_context_unregistered'))
        archives.append(dict(archive=archive,source_tpl_sha256=sha(p.read_bytes()),source_payload_sha256=sha(payload),stored_bytes=row['size'],payload_bytes=len(payload),compressed=row['compressed'],pointers=row['pointers'],script_slots=int(re.search(r'^@size\s+(\d+)',tpl,re.M).group(1)),literal_counts=dict(counts),registered_consumer=registry.get(archive,{}).get('consumer')))
    missing=sorted(set(selected)-seen)
    if missing:raise ValueError('selected unit absent from extraction '+str(missing[:10]))
    summary=dict(policy='development-draft; NON-DISTRIBUTION',release_eligible=False,baseline_rom_sha256=m['output_sha256'],source_sha256=cfg['source_profile']['sha256'],catalog_sha256=cfg['text_catalog']['sha256'],catalog_archives=732,parsed_archives=len(archives),parse_errors=errors,canonical_literals=len(records),counts=dict(statuses),literal_languages=dict(language),source_chars=sum(x['source_chars'] for x in records),japanese_chars=sum(x['japanese_chars'] for x in records),unselected_japanese_chars=sum(x['japanese_chars'] for x in records if x['status']=='unselected_japanese'),unique_unselected_japanese_texts=len({x['source'] for x in records if x['status']=='unselected_japanese'}),selected_catalog_literal_units=len(selected),manifest_selected_text_units=m['translated_units'],asset_hashes=asset_hashes,limits=['Catalog732 is exhaustively enumerated, not proof of all ROM text including inline tables/name input/graphics.','Non-Japanese entries not excluded; source strings are not globally interchangeable across speakers/renderers.','Unknown consumer/context and graphics population remain unresolved. No complete-translation percentage or full ROM completion claim.','Existing review/runtime limitations and Hangul name entry/persistence/old-save condition remain open.'])
    out=ROOT/a.out;out.mkdir(parents=True,exist_ok=True)
    for name,data in [('inventory.json',dict(summary=summary,archives=archives,selected_graphics_assets=graphics)),('literal_backlog.json',dict(source_sha256=cfg['source_profile']['sha256'],baseline_rom_sha256=m['output_sha256'],units=records))]:
        (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('asset_hashes','limits')},ensure_ascii=False,indent=2))
    return 1 if errors else 0

if __name__=='__main__':raise SystemExit(main())
