"""025 cumulative composition before allocation and final source-bound checks.

The versioned primary entry retains the frozen023 implementation. No patched
ROM is an input: baseline024 bytes are only a comparison reference.
"""
import struct
from copy import deepcopy
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read
from layout500_inputs_026 import load_inputs, MANIFEST, MANIFEST_SHA
from prepare_repartition500 import layout_records
from compare_archive_payloads import payload_of
from build_development_patch import validate_characters


def compose(record, payload, prior_payload, prior_record, plugins):
    if sha(prior_payload) != record['parent_compiled_sha256']:
        raise ValueError('025 actual build carry mismatch '+record['archive'])
    if record['old_record'] is not None:
        parent=record['old_record']
        for key in ('archive','compiled_sha256','compiled_bytes','translated_units','layout'):
            if prior_record.get(key)!=parent.get(key):
                raise ValueError('025 build parent metadata '+record['archive']+' '+key)
    target=(ROOT/record['merged_tpl']['path']).read_text(encoding='utf-8-sig')
    asset=read(record['merged_asset']['path']);ids={u['id'] for u in asset['units']}
    layout=validate_characters(target,plugins/'exe45-utf8.tbl',record['scope'],ids)
    measured={r['id']:r['line_advance_pixels'] for r in layout}
    if measured!={r['id']:r['line_advance_pixels'] for r in record['layout']}:
        raise ValueError('025 current plugin metrics mismatch')
    result=deepcopy(prior_record)
    result.update(archive=record['archive'],source_bytes=record['old_record']['source_bytes'] if record['old_record'] else len(prior_payload),
        source_sha256=record['source_payload_sha256'],compiled_bytes=len(payload),
        compiled_sha256=sha(payload),translated_units=len(ids),layout=deepcopy(record['layout']),
        native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,
        protected_controls_unchanged=True,script_count=record['script_count'],
        unselected_script_bytes_preserved=record['unselected_parent_scripts'],
        cumulative026=dict(manifest=MANIFEST,manifest_sha256=MANIFEST_SHA,
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


def finalize(source,target,result,inputs,summary,inputs024,summary024,inputs025,summary025):
    baseline_path=ROOT/'poc/output/pending500_025_v2.gba'
    old=read(baseline_path.with_suffix('.json'));baseline=baseline_path.read_bytes()
    before=list(layout_records(old));after=list(layout_records(result))
    old_ids={u['id'] for r in before for u in r['layout']}
    new_ids={u['id'] for r in after for u in r['layout']}
    selected={key for r,_ in inputs for key in r['new_ids']}
    if old_ids-new_ids or new_ids-old_ids!=selected or len(selected)!=500 or result['translated_units']!=old['translated_units']+len(selected):
        raise ValueError('025 final actual500/all-carry/translated-unit delta')
    # Archive identity alone is insufficient: the header/full-body consumers
    # of some source archives are distinct, so use their exact selected IDs.
    matched=set()
    changed={r['archive']:(r,p) for r,p in inputs}
    for current in after:
        ids={u['id'] for u in current['layout']}
        parents=[r for r in before if r['archive']==current['archive'] and {u['id'] for u in r['layout']}<=ids]
        if not parents:
            if current['archive'] not in changed or changed[current['archive']][0]['storage']!='new-raw':
                raise ValueError('025 unaccounted compiled consumer')
            continue
        parents.sort(key=lambda r:len(r['layout']),reverse=True)
        if len(parents)>1 and len(parents[0]['layout'])==len(parents[1]['layout']):
            raise ValueError('025 ambiguous compiled consumer')
        parent=parents[0]
        matched.add((parent['archive'],parent['compiled_sha256']))
        cp=current.get('rom_offset');pp=parent.get('rom_offset')
        if current['archive'] in changed and current.get('cumulative026'):
            r,payload=changed[current['archive']]
            if target[cp:cp+current['compiled_bytes']]!=payload:raise ValueError('025 final merged payload')
        elif cp is not None and pp is not None:
            if target[cp:cp+current['compiled_bytes']]!=baseline[pp:pp+parent['compiled_bytes']] or current['layout']!=parent['layout']:
                raise ValueError('025 unrelated compiled consumer changed '+current['archive'])
    if any((r['archive'],r['compiled_sha256']) not in matched for r in before):
        raise ValueError('025 prior compiled consumer missing')
    # Reconstruct prior effective input owners in adopted024->025 order.
    for version,prior_inputs,prior_summary in (('024',inputs024,summary024),('025',inputs025,summary025)):
        for prior,_ in prior_inputs:
            for asset in result['translation_assets']:
                if asset.get('archive')==prior['archive'] and not asset.get('scope','').startswith('read-only inherited'):
                    asset['scope']='read-only inherited; composed by'+version+' cumulative input'
            result['translation_assets'].append(dict(prior['merged_asset'],archive=prior['archive'],scope=version+' effective cumulative translation owner'))
        result['pending_batch500_'+version]=deepcopy(old['pending_batch500_'+version])
        if prior_summary['new_units']!=500:raise ValueError('026 retained prior population')
    for r,payload in inputs:
        candidates=[x for x in after if x['archive']==r['archive'] and x.get('cumulative026')]
        if len(candidates)!=1 or candidates[0]['compiled_sha256']!=sha(payload):
            raise ValueError('025 unique final merged writer')
        # Reclassify old asset as inherited, register the single effective owner.
        for asset in result['translation_assets']:
            if asset.get('archive')==r['archive'] and not asset.get('scope','').startswith('read-only inherited'):
                asset['scope']='read-only inherited025; composed by026 cumulative input'
        result['translation_assets'].append(dict(r['merged_asset'],archive=r['archive'],scope='026 effective cumulative translation owner'))
    result['pending_batch500_026']=dict(**summary,manifest=MANIFEST,manifest_sha256=MANIFEST_SHA,
        rom_integrated=True,exact_new500_delta=True,prior_compiled_consumers_preserved=True,
        runtime='pending',release_eligible=False)
    result['primary_entry']='tools/build_development_patch_026.py'
    result['limits'].append('026 exact500 cumulative insertion; runtime and semantic review pending; NON-DISTRIBUTION')
