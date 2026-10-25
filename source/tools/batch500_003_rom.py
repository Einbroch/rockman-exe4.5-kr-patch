"""Explicit500 existing draft units: three guarded normal gear pools plus raw relocation."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

PREFLIGHT='analysis/pending_insertion_500_003_preflight_v3/preflight.json'
GEAR={'6E1554':2,'6E1CC0':5,'6E21B0':7}


def entries(source):
    pre=json.loads((ROOT/PREFLIGHT).read_text(encoding='utf8'))
    if pre['source_sha256']!=sha(source) or pre['total_units']!=500 or pre['layout_candidates'] or pre['release_eligible'] is not False:raise ValueError('Batch003 preflight binding')
    require_hash(ROOT/pre['selection']['path'],pre['selection']['sha256'])
    require_hash(ROOT/pre['individual_layout']['path'],pre['individual_layout']['sha256'])
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows=parse_tpi(ROOT/cfg['text_catalog']['path']);result=[]
    for r in pre['archives']:
        path=r['draft_path'];require_hash(ROOT/path,r['draft_sha256'])
        d=json.loads((ROOT/path).read_text(encoding='utf8'));a=d['archive']
        require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
        units=[{k:u[k] for k in ('id','source','translation','state')} for u in d['units'] if u['id'] in set(r['selected_ids'])]
        if [u['id'] for u in units]!=r['selected_ids']:raise ValueError('Batch003 ordered IDs')
        row=next(x for x in rows if x['offset']==int(a,16));native=payload_of(source,row)
        if sha(native)!=r['source_payload_sha256']:raise ValueError('Batch003 native identity')
        gear=a in GEAR
        asset={k:d[k] for k in ('schema','policy','archive','source_sha256','source_tpl','source_archive_sha256','review')}
        asset.update(consumer='normal-dialogue',units=units)
        scope=dict(consumer='normal-dialogue',complete_literal_scope=False,literal_scripts=r['scripts'],literal_ids=r['selected_ids'],
            script_count=r['script_count'],max_literal_rows=3,max_line_advance=132 if not gear else 152,
            literal_language='mmbn45',preserve_literal_numerals=True,standard_relocation=not gear)
        if gear:
            if len(units)!=13 or scope['script_count']!=76 or scope['literal_scripts']!=[60,61,62,70,71,72,73,74,75]:raise ValueError('Gear normal population')
            scope['equipment_navi_index']=GEAR[a]
            scope['literal_profiles']=[dict(scripts=[60,61,62],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=2,max_line_advance=132)]
            scope['equipment_aggregate_profile']=True
            scope['pending500_003_equipment_layout']=True
            require_hash(ROOT/r['explicit_page_proof']['path'],r['explicit_page_proof']['sha256'])
        else:
            if row['compressed'] or row['size_header'] or row['pointers']==[0]:raise ValueError('Unsupported raw body scope')
            scope.update(source_bytes=row['size'],pointers=row['pointers'],compressed=False)
        result.append((path,row,asset,scope,r,native))
    if sum(len(x[2]['units']) for x in result)!=500:raise ValueError('Batch003 denominator')
    return result


def validate_aggregate(source,asset,layout):
    a=asset['archive'];indexed={r['id']:r['line_advance_pixels'] for r in layout}
    # Source0803EFAA zero-extends the halfword at folderState+1C;0803EFAC
    # stores that value in normalContext+4C (printBuffer1). Do not substitute
    # an inventory/folder design limit for this actual producer's bit width.
    if source[0x3EFAA:0x3EFAE]!=bytes.fromhex('ab8bf364'):raise ValueError('Gear buffer1 producer changed')
    suffix=indexed[a+':70:1'];first=indexed[a+':70:0']
    if len(first)!=2 or first[-1]!=0 or len(suffix)!=2 or 55+suffix[0]>152 or suffix[1]>132:
        raise ValueError('Gear joined numeric warning page')
    for r in layout:
        if len(r['line_advance_pixels'])==3 and r['line_advance_pixels'][2]>132:raise ValueError('Gear third-row extent')
    return dict(unsigned_decimal_bits=16,max_digits=5,source_producer=0x0803EFAA,source_producer_hex='ab8bf364',second_row_max_advance=55+suffix[0],third_row_max_advance=suffix[1],
        conditional_name_input_not_claimed=True,required_count_not_assumed=True)


def prepare():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256'])
    paths=[]
    for _,_,asset,scope,_,_ in entries(sp.read_bytes()):
        if not scope['standard_relocation']:continue
        path=ROOT/f"analysis/pending_insertion_500_003_rom/{asset['archive']}_selected_asset.json"
        data=json.dumps(asset,ensure_ascii=False,indent=2)+'\n';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('Preserve prior selected input')
        if not path.exists():path.write_text(data,encoding='utf8')
        paths.append(str(path.relative_to(ROOT)))
    return paths
