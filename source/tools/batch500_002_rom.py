"""Revised500 insertion input binding, including immutable26-unit destruction carry."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

PREFLIGHT='analysis/pending_insertion_500_002_repartition_preflight_v1/preflight.json'


def entries(source):
    pre=json.loads((ROOT/PREFLIGHT).read_text(encoding='utf8'))
    if pre['source_sha256']!=sha(source) or pre['total_units']!=500 or pre['layout_candidates'] or pre['release_eligible'] is not False:
        raise ValueError('Revised500 preflight identity')
    require_hash(ROOT/pre['repartition']['path'],pre['repartition']['sha256'])
    require_hash(ROOT/pre['individual_layout']['path'],pre['individual_layout']['sha256'])
    layouts=json.loads((ROOT/pre['individual_layout']['path']).read_text(encoding='utf8'))['layouts']
    from pending500_002_pages import specification
    _,page_sha=specification()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows=parse_tpi(ROOT/cfg['text_catalog']['path'])
    result=[]
    for r in pre['archives']:
        path=r['draft_path'];require_hash(ROOT/path,r['draft_sha256'])
        d=json.loads((ROOT/path).read_text(encoding='utf8'));a=d['archive']
        require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
        wanted=set(r['selected_ids'])
        if a=='6E01AC':wanted.update(u['id'] for u in d['units'] if int(u['id'].split(':')[1]) in (38,39,40))
        units=[{k:u[k] for k in ('id','source','translation','state')} for u in d['units'] if u['id'] in wanted]
        for u in units:
            if u['id'] in layouts:
                text=layouts[u['id']]
                if text.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('Words changed in individual layout')
                u['translation']=text
        if {u['id'] for u in units}!=wanted:raise ValueError('Revised population')
        row=next(x for x in rows if x['offset']==int(a,16));native=payload_of(source,row)
        if sha(native)!=r['source_payload_sha256']:raise ValueError('Raw source archive identity')
        raw_clone=a in ('6E01AC','6DED88','6DE2C8')
        asset={k:d[k] for k in ('schema','policy','archive','source_sha256','source_tpl','source_archive_sha256','review')}
        asset.update(consumer='normal-dialogue',units=units)
        scope=dict(consumer='normal-dialogue',complete_literal_scope=False,literal_scripts=sorted({int(u['id'].split(':')[1]) for u in units}),
            literal_ids=[u['id'] for u in units],script_count=r['script_count'],max_literal_rows=3,max_line_advance=152 if raw_clone else 132,
            preserve_literal_numerals=True,literal_language='mmbn45',standard_relocation=not raw_clone)
        if not raw_clone:
            if row['compressed'] or row['size_header'] or row['pointers']==[0]:raise ValueError('Unsupported raw relocation')
            scope.update(source_bytes=row['size'],pointers=row['pointers'],compressed=False)
        else:scope['mail_arrow_row3_limit']=132
        if a=='6DED88':
            if r['explicit_page_proof']['sha256']!=page_sha:raise ValueError('Page identity')
            scope['pending500_002_pages']=True
        bound=dict(r)
        if a=='6E01AC':
            audit=json.loads((ROOT/'analysis/pending_insertion_500_002_capacity_v2/report.json').read_text(encoding='utf8'))
            carry=audit['cumulative_destruction']
            if carry['carried_units']!=26 or carry['prior_selected_script_bytes_exact']!=[38,39,40]:raise ValueError('Destruction carry identity')
            bound.update(compiled_sha256=carry['compiled_sha256'],compiled_bytes=carry['compiled_bytes'])
        result.append((path,row,asset,scope,bound,native))
    if sum(len(x[2]['units']) for x in result)!=526:raise ValueError('500new plus26carry')
    return result


def prepare():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source=ROOT/cfg['source_profile']['filename'];require_hash(source,cfg['source_profile']['sha256'])
    paths=[]
    for _,_,asset,scope,_,_ in entries(source.read_bytes()):
        if not scope['standard_relocation']:continue
        path=ROOT/f"analysis/pending_insertion_500_002_repartition_rom/{asset['archive']}_selected_asset.json"
        text=json.dumps(asset,ensure_ascii=False,indent=2)+'\n'
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() and path.read_text(encoding='utf8')!=text:raise ValueError('Existing selected asset differs')
        if not path.exists():path.write_text(text,encoding='utf8')
        paths.append(str(path.relative_to(ROOT)))
    return paths
