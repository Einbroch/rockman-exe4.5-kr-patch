"""024 cumulative composition before allocation and final source-bound checks.

The versioned primary entry retains the frozen023 implementation. No patched
ROM is an input: baseline023 bytes are only a comparison reference.
"""
import struct
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read
from layout500_inputs_024 import load_inputs, MANIFEST, MANIFEST_SHA
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of
from build_development_patch import validate_characters


def compose(record, payload, prior_payload, prior_record, plugins):
    if sha(prior_payload) != record['parent_compiled_sha256']:
        raise ValueError('024 actual build carry mismatch '+record['archive'])
    if record['old_record'] is not None:
        parent=record['old_record']
        for key in ('archive','compiled_sha256','compiled_bytes','translated_units','layout'):
            if prior_record.get(key)!=parent.get(key):
                raise ValueError('024 build parent metadata '+record['archive']+' '+key)
    target=(ROOT/record['merged_tpl']['path']).read_text(encoding='utf-8-sig')
    asset=read(record['merged_asset']['path']);ids={u['id'] for u in asset['units']}
    layout=validate_characters(target,plugins/'exe45-utf8.tbl',record['scope'],ids)
    measured={r['id']:r['line_advance_pixels'] for r in layout}
    if measured!={r['id']:r['line_advance_pixels'] for r in record['layout']}:
        raise ValueError('024 current plugin metrics mismatch')
    result=deepcopy(prior_record)
    result.update(archive=record['archive'],source_bytes=record['old_record']['source_bytes'] if record['old_record'] else len(prior_payload),
        source_sha256=record['source_payload_sha256'],compiled_bytes=len(payload),
        compiled_sha256=sha(payload),translated_units=len(ids),layout=deepcopy(record['layout']),
        native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,
        protected_controls_unchanged=True,script_count=record['script_count'],
        unselected_script_bytes_preserved=record['unselected_parent_scripts'],
        cumulative024=dict(manifest=MANIFEST,manifest_sha256=MANIFEST_SHA,
            new_ids=record['new_ids'],new_scripts=record['new_scripts'],
            carry_compiled_sha256=record['parent_compiled_sha256'],
            original_native_unselected_proof='source-only compile500 plus source-reconstructed carry',
            parent_scope=record['parent_scope'],scope=record['scope'],
            source_bound_page_gate=True,conditional_effects_runtime_pending=True))
    return payload,result


def compose_primary(archive,payload,record,inputs,plugins):
    match=[(r,p) for r,p in inputs if r['archive']==archive and r['storage']=='raw-carry']
    if not match:return payload,record
    r,p=match[0]
    return compose(r,p,payload,record,plugins)


def append_new_raw(source,archive_blob,products,records,selected,inputs,plugins):
    for r,p in inputs:
        if r['storage']!='new-raw':continue
        arc=r['archive'];row=r['source_row'];asset=read(r['merged_asset']['path'])
        if arc in selected or row['offset'] in products or row['compressed']:
            raise ValueError('024 new raw writer overlaps')
        payload,record=compose(r,p,payload_of(source,row),{},plugins)
        archive_blob.extend(b'\xff'*(-len(archive_blob)%4));at=len(source)+len(archive_blob)
        archive_blob.extend(payload);products[row['offset']]=(at,payload,payload)
        record.update(rom_offset=at,pointers=row['pointers']);records.append(record)
        selected[arc]=(row,asset,r['scope'])


def compose_hints(payloads,inputs,plugins):
    merged={r['archive']:(r,p) for r,p in inputs if r['storage']=='A3-clone-merge'}
    if len(payloads)!=len(merged):raise ValueError('024 A3 population')
    result=[]
    for raw,native,prior,index in payloads:
        r,p=merged[prior['archive']]
        payload,record=compose(r,p,raw,prior,plugins)
        record.update(asset_path=r['merged_asset']['path'],asset_sha256=r['merged_asset']['sha256'])
        result.append((payload,native,record,index))
    return result


def verify_hints(source,target,meta):
    """Versioned A3 final check: identical native guards, cumulative521 units."""
    from hint_rom_data import input_entries
    inputs,_=load_inputs(source)
    merged={r['archive']:(r,p) for r,p in inputs if r['storage']=='A3-clone-merge'}
    native_inputs=input_entries(source);records=meta.get('hint_archives',[]);guard=meta.get('hint_guard')
    if len(records)!=19 or not guard or set(guard)!={'descriptor_address'}:
        raise ValueError('024 A3 final population')
    table=[(0,0,0,0)]*23;selected=set()
    for final,entry in zip(records,native_inputs):
        _,row,asset,_,_,native,index=entry;r,payload=merged[asset['archive']]
        cp=final['rom_offset'];np=final['native_copy_offset'];n=final['compiled_bytes']
        if (final['archive']!=asset['archive'] or final['navi_index']!=index
                or final['asset_path']!=r['merged_asset']['path'] or final['asset_sha256']!=r['merged_asset']['sha256']
                or target[cp:cp+n]!=payload or n!=len(payload) or final['compiled_sha256']!=sha(payload)
                or final['rom_sha256']!=sha(payload) or final['layout']!=r['layout']
                or final['translated_units']!=r['carry_units']+r['new_units']):
            raise ValueError('024 A3 final cumulative clone identity')
        if (cp&3 or np&3 or not len(source)<=np<np+len(native)<=cp<cp+n<=guard['descriptor_address']-0x08000000
                or final['native_ram_archive_retained'] is not True or final['source_pointers']!=row['pointers']):
            raise ValueError('024 A3 placement/storage contract')
        if (target[np:np+len(native)]!=native or final['native_copy_bytes']!=len(native)
                or final['native_payload_sha256']!=sha(native)):
            raise ValueError('024 A3 native comparison copy')
        at=row['offset']
        if target[at:at+row['size']]!=source[at:at+row['size']] or any(target[p:p+4]!=source[p:p+4] for p in row['pointers']):
            raise ValueError('024 A3 native compressed storage/reference changed')
        table[index]=(0x08000000+cp,0x08000000+np,len(native),0)
        selected.update(u['id'] for u in read(r['merged_asset']['path'])['units'])
    at=guard['descriptor_address']-0x08000000
    expected=b''.join(struct.pack('<4I',*v) for v in table)
    if target[at:at+len(expected)]!=expected or len(selected)!=521:
        raise ValueError('024 A3 descriptor/521-ID binding')
    return selected


def finalize(source,target,result,inputs,summary):
    baseline_path=ROOT/'poc/output/pending500_023_v1.gba'
    old=read(baseline_path.with_suffix('.json'));baseline=baseline_path.read_bytes()
    before=list(layout_records(old));after=list(layout_records(result))
    old_ids={u['id'] for r in before for u in r['layout']}
    new_ids={u['id'] for r in after for u in r['layout']}
    selected={key for r,_ in inputs for key in r['new_ids']}
    if old_ids-new_ids or new_ids-old_ids!=selected or len(selected)!=500 or result['translated_units']!=old['translated_units']+len(selected):
        raise ValueError('024 final actual500/all-carry/translated-unit delta')
    # Archive identity alone is insufficient: the header/full-body consumers
    # of some source archives are distinct, so use their exact selected IDs.
    matched=set()
    changed={r['archive']:(r,p) for r,p in inputs}
    for current in after:
        ids={u['id'] for u in current['layout']}
        parents=[r for r in before if r['archive']==current['archive'] and {u['id'] for u in r['layout']}<=ids]
        if not parents:
            if current['archive'] not in changed or changed[current['archive']][0]['storage']!='new-raw':
                raise ValueError('024 unaccounted compiled consumer')
            continue
        parent=max(parents,key=lambda r:len(r['layout']))
        matched.add((parent['archive'],parent['compiled_sha256']))
        cp=current.get('rom_offset');pp=parent.get('rom_offset')
        if current['archive'] in changed and current.get('cumulative024'):
            r,payload=changed[current['archive']]
            if target[cp:cp+current['compiled_bytes']]!=payload:raise ValueError('024 final merged payload')
        elif cp is not None and pp is not None:
            if target[cp:cp+current['compiled_bytes']]!=baseline[pp:pp+parent['compiled_bytes']] or current['layout']!=parent['layout']:
                raise ValueError('024 unrelated compiled consumer changed '+current['archive'])
    if any((r['archive'],r['compiled_sha256']) not in matched for r in before):
        raise ValueError('024 prior compiled consumer missing')
    for r,payload in inputs:
        candidates=[x for x in after if x['archive']==r['archive'] and x.get('cumulative024')]
        if len(candidates)!=1 or candidates[0]['compiled_sha256']!=sha(payload):
            raise ValueError('024 unique final merged writer')
        # Reclassify old asset as inherited, register the single effective owner.
        for asset in result['translation_assets']:
            if asset.get('archive')==r['archive'] and not asset.get('scope','').startswith('read-only inherited'):
                asset['scope']='read-only inherited023; composed by024 cumulative input'
        result['translation_assets'].append(dict(r['merged_asset'],archive=r['archive'],scope='024 effective cumulative translation owner'))
    result['pending_batch500_024']=dict(**summary,manifest=MANIFEST,manifest_sha256=MANIFEST_SHA,
        rom_integrated=True,exact_new500_delta=True,prior_compiled_consumers_preserved=True,
        runtime='pending',release_eligible=False)
    result['primary_entry']='tools/build_development_patch_024.py'
    result['limits'].append('024 exact500 cumulative insertion; runtime and semantic review pending; NON-DISTRIBUTION')
