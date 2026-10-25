"""Validated raw normal-dialogue inputs for the fourth cumulative500 batch."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

PREFLIGHT='analysis/pending_insertion_500_004_preflight_v1/preflight.json'
OUT='analysis/pending_insertion_500_004_rom'

def entries(source,preflight=PREFLIGHT,batch_id='pending-insertion-500-004'):
    pre=json.loads((ROOT/preflight).read_text(encoding='utf8'))
    if pre['batch_id']!=batch_id or pre['source_sha256']!=sha(source) or pre['total_units']!=500 or pre['layout_candidates'] or pre['release_eligible'] is not False:raise ValueError('Raw batch preflight binding')
    for key in ('selection','individual_layout'):require_hash(ROOT/pre[key]['path'],pre[key]['sha256'])
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows=parse_tpi(ROOT/cfg['text_catalog']['path']);result=[]
    for r in pre['archives']:
        path=r['draft_path'];require_hash(ROOT/path,r['draft_sha256']);d=json.loads((ROOT/path).read_text(encoding='utf8'));a=d['archive']
        require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
        units=[{k:u[k] for k in ('id','source','translation','state')} for u in d['units'] if u['id'] in set(r['selected_ids'])]
        if [u['id'] for u in units]!=r['selected_ids']:raise ValueError('Batch004 ordered IDs')
        row=next(x for x in rows if x['offset']==int(a,16));native=payload_of(source,row)
        if sha(native)!=r['source_payload_sha256'] or row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0]:raise ValueError('Batch004 raw source contract')
        asset={k:d[k] for k in ('schema','policy','archive','source_sha256','source_tpl','source_archive_sha256','review')};asset.update(consumer='normal-dialogue',units=units)
        scope=dict(consumer='normal-dialogue',complete_literal_scope=False,literal_scripts=r['scripts'],literal_ids=r['selected_ids'],script_count=r['script_count'],
            max_literal_rows=3,max_line_advance=132,literal_language='mmbn45',preserve_literal_numerals=True,standard_relocation=True,
            source_bytes=row['size'],pointers=row['pointers'],compressed=False)
        result.append((path,row,asset,scope,r,native))
    if sum(len(x[2]['units']) for x in result)!=500:raise ValueError('Batch004 denominator')
    return result

def prepare(preflight=PREFLIGHT,out=OUT,batch_id='pending-insertion-500-004'):
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);paths=[]
    for _,_,asset,_,_,_ in entries(sp.read_bytes(),preflight,batch_id):
        path=ROOT/out/f"{asset['archive']}_selected_asset.json";data=json.dumps(asset,ensure_ascii=False,indent=2)+'\n';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('Preserve prior selected input')
        if not path.exists():path.write_text(data,encoding='utf8')
        paths.append(str(path.relative_to(ROOT)))
    return paths
