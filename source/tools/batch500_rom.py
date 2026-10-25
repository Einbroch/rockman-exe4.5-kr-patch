"""Explicit source-bound pending 500 selection; no automatic prose translation."""
import json
from build_visibility_poc import ROOT,require_hash,sha
from prepare_pending_batch500 import PLAN
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

PREFLIGHT='analysis/pending_insertion_500_001_r4/preflight.json'

def entries(source):
    pre=json.loads((ROOT/PREFLIGHT).read_text(encoding='utf8'))
    if pre['source_sha256']!=sha(source) or pre['total_units']!=500 or pre['layout_candidates'] or pre['release_eligible'] is not False:
        raise ValueError('pending 500 preflight binding')
    layout=json.loads((ROOT/pre['individual_layout']['path']).read_text(encoding='utf8'))
    require_hash(ROOT/pre['individual_layout']['path'],pre['individual_layout']['sha256'])
    require_hash(ROOT/pre['arrow_layout']['path'],pre['arrow_layout']['sha256'])
    from prepare_pending_batch500 import arrow_layouts,same_layout_words
    combined_layout=dict(layout['layouts'],**arrow_layouts())
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    rows=parse_tpi(ROOT/cfg['text_catalog']['path'])
    result=[]
    for (path,scripts,count),r in zip(PLAN,pre['archives']):
        require_hash(ROOT/path,r['draft_sha256'])
        d=json.loads((ROOT/path).read_text(encoding='utf8'))
        require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
        units=[{k:u[k] for k in ('id','source','translation','state')} for u in d['units'] if scripts is None or int(u['id'].split(':')[1]) in scripts]
        for u in units:
            if u['id'] in combined_layout:
                value=combined_layout[u['id']]
                if not same_layout_words(u['id'],value,u['translation']):raise ValueError('individual layout wording changed')
                u['translation']=value
        if len(units)!=count or [u['id'] for u in units]!=r['selected_ids']:raise ValueError('500 population')
        a=d['archive'];row=next(x for x in rows if x['offset']==int(a,16));native=payload_of(source,row)
        if sha(native)!=r['source_payload_sha256']:raise ValueError('native 500 binding')
        header=a.startswith('6DD')
        asset={k:d[k] for k in ('schema','policy','archive','source_sha256','source_tpl','source_archive_sha256','review')}
        asset.update(consumer='fixed-cell-big' if header else 'normal-dialogue',units=units)
        scope=dict(consumer=asset['consumer'],complete_literal_scope=False,literal_scripts=r['scripts'],literal_ids=r['selected_ids'],script_count=r['script_count'],max_literal_rows=1 if header else 3,max_line_advance=88 if header else 152,preserve_literal_numerals=True,literal_language='mmbn45s' if header else 'mmbn45')
        if header:scope.update(source_bytes=row['size'],pointers=row['pointers'],compressed=True,compression='BIOS type-10 literal-only, 4-byte aligned, zero-padded',decompression_destination=0x020262F4,max_payload_bytes=4096,next_scene_asset=0x020272F4)
        if a=='6DE3E0':scope['mission_reward_profile']='protoman-mission-reward-v1'
        if not header:scope['mail_arrow_row3_limit']=132
        result.append((path,row,asset,scope,r,native))
    if sum(len(x[2]['units']) for x in result)!=500:raise ValueError('500 denominator')
    return result

def prepare():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));p=ROOT/cfg['source_profile']['filename'];require_hash(p,cfg['source_profile']['sha256'])
    paths=[]
    for _,_,asset,_,_,_ in entries(p.read_bytes()):
        if asset['consumer']!='fixed-cell-big':continue
        path=ROOT/f"analysis/pending_insertion_500_rom/{asset['archive']}_selected_asset.json"
        data=json.dumps(asset,ensure_ascii=False,indent=2)+'\n'
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('preserve selected 500 input')
        if not path.exists():path.write_text(data,encoding='utf8')
        paths.append(str(path.relative_to(ROOT)))
    return paths
