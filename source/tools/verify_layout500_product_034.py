"""Independent026 product audit: all carry consumers, references and diff."""
import argparse
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from layout500_inputs_034 import load_inputs
from verify_pending500_002_rom import clones,read_payload
from archive_scripts import verify_untouched_scripts
from keyitem_rom_data_024 import verify_final
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_034_v1.gba')
    p.add_argument('--repro');p.add_argument('--out',default='analysis/pending500_034_v1/integration.json');a=p.parse_args()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    inputs,summary=load_inputs(source);changed={r['archive']:(r,raw) for r,raw in inputs}
    rp=ROOT/a.rom;meta=read(rp.with_suffix('.json'));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    bp=ROOT/'poc/output/pending500_033_v1.gba';old=read(bp.with_suffix('.json'));require_hash(bp,old['output_sha256']);base=bp.read_bytes()
    for name,h in meta['build_tools_sha256'].items():require_hash(ROOT/'tools'/name,h)
    before=list(clones(old));after=list(clones(meta));selected={k for r,_ in inputs for k in r['new_ids']}
    before_ids={u['id'] for _,r in before for u in r['layout']};after_ids={u['id'] for _,r in after for u in r['layout']}
    if before_ids-after_ids or after_ids-before_ids!=selected or len(selected)!=500 or meta['translated_units']!=old['translated_units']+500:
        raise ValueError('025 actual500 delta or old IDs lost')
    preserved=[];merged=[]
    for path,prior in before:
        ids={u['id'] for u in prior['layout']}
        candidates=[r for _,r in after if r['archive']==prior['archive'] and ids<={u['id'] for u in r['layout']}]
        # Bounded mail and its full-body ROM clone share a source archive.
        # Select the narrowest matching declared consumer, not the source alone.
        candidates.sort(key=lambda r:len(r['layout']))
        if not candidates or len(candidates)>1 and len(candidates[0]['layout'])==len(candidates[1]['layout']):
            raise ValueError('025 prior consumer identity ambiguous/missing '+str(path))
        current=candidates[0];raw=read_payload(rom,current);prior_raw=read_payload(base,prior)
        if current.get('cumulative034'):
            r,expected=changed[prior['archive']]
            if raw!=expected:raise ValueError('025 changed payload/source compile binding')
            verify_untouched_scripts(prior_raw,raw,r['script_count'],set(r['new_scripts']))
            old_metrics={u['id']:u for u in prior['layout']}
            if any(u!=old_metrics[u['id']] for u in current['layout'] if u['id'] in old_metrics):
                raise ValueError('025 rich carry metrics changed')
            merged.append(prior['archive'])
        else:
            if raw!=prior_raw or any(current.get(k)!=prior.get(k) for k in ('compiled_sha256','layout','translated_units','source_sha256','protected_controls_unchanged')):
                raise ValueError('025 unrelated consumer changed '+str(path))
            preserved.append('/'.join(map(str,path)))
    verify_final(source,rom,meta['keyitem_rom'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows=parse_tpi(ROOT/cfg['text_catalog']['path']);primary={int(r['archive'],16):r for r in meta['archives']};untouched=0
    for row in rows:
        if row['offset'] in primary:
            record=primary[row['offset']]
            if row['pointers']!=record['pointers']:raise ValueError('025 pointer inventory')
            for at in row['pointers']:
                if struct.unpack_from('<I',rom,at)[0]!=0x08000000+record['rom_offset']:raise ValueError('025 pointer target')
            if sha(read_payload(rom,record))!=record['compiled_sha256']:raise ValueError('025 final primary payload')
        else:
            if payload_of(source,row)!=payload_of(rom,row) or any(source[p:p+4]!=rom[p:p+4] for p in row['pointers']):
                raise ValueError('025 protected catalog payload/reference')
            untouched+=1
    for record,payload in inputs:
        row=record['source_row'];at=row['offset'];final=primary[at]
        if rom[at:at+row['size']]!=source[at:at+row['size']] or read_payload(rom,final)!=payload:
            raise ValueError('027 newRAW original storage/final compiled payload')
        parent_payload=checked_ref_payload= (ROOT/record['carry_compiled']['path']).read_bytes()
        require_hash(ROOT/record['carry_compiled']['path'],record['carry_compiled']['sha256'])
        if verify_untouched_scripts(parent_payload,payload,record['script_count'],set(record['new_scripts']))!=record['unselected_parent_scripts']:
            raise ValueError('027 final newRAW untouched scripts')
        if final['layout']!=record['layout'] or final['translated_units']!=record['new_units']+record['carry_units']:
            raise ValueError('027 final newRAW metrics/unit population')
    coverage=bytearray(len(source))
    for w in meta['expected_writes']:
        at,n=w['offset'],w['bytes']
        if not 0<=at<=len(source)-n or any(coverage[at:at+n]) or source[at:at+n].hex()!=w['expected_hex'] or rom[at:at+n].hex()!=w['final_hex']:
            raise ValueError('025 immutable source/final/overlap write contract')
        coverage[at:at+n]=b'\x01'*n
    if (any(x!=y and not coverage[i] for i,(x,y) in enumerate(zip(source,rom)))
            or rom[:0xC0]!=source[:0xC0] or len(rom)!=meta['output_bytes']
            or len(rom)-len(source)!=meta['append_bytes'] or sha(rom[len(source):])!=meta['append_sha256']):
        raise ValueError('025 complete final diff/header/tail')
    new_raw={r['archive'] for r,_ in inputs if r['storage']=='new-raw'}
    if len(primary)!=len(old['archives'])+len(new_raw) or untouched!=old['unchanged_archives']-len(new_raw) or untouched!=meta['unchanged_archives'] or len(after)!=len(before)+len(new_raw):
        raise ValueError('025 primary/source population')
    for r,_ in inputs:
        owners=[x for x in meta['translation_assets'] if x.get('archive')==r['archive'] and not x.get('scope','').startswith('read-only inherited')]
        if len(owners)!=1 or {k:owners[0][k] for k in ('path','sha256')}!=r['merged_asset']:
            raise ValueError('025 effective input ownership')
    repro=False
    if a.repro:
        if (ROOT/a.repro).read_bytes()!=rom:raise ValueError('025 independent rebuild bytes differ')
        repro=True
    frozen_write(ROOT/a.out,dict(schema=1,passed=True,rom_sha256=sha(rom),rom_bytes=len(rom),
        source_sha256=sha(source),baseline_sha256=sha(base),new_units=500,total_units=meta['translated_units'],
        primary_archives=len(primary),unchanged_source_archives=untouched,new_raw_archives=sorted(new_raw),
        preserved_consumer_count=len(preserved),preserved_consumer_paths=preserved,
        merged_consumer_archives=sorted(merged),selected_ids=sorted(selected),
        final_selector_and_native_storage_verified=True,all_effective_input_owners_verified=True,
        expected_writes_and_complete_diff_verified=True,independent_rebuild_byte_identical=repro,
        runtime_tested=False,release_eligible=False,
        limits='Static exact product only. New normal/PET/flag pages and A3 hints require actual026 '
               'consumer execution. Automatic Hangul commit/save/redisplay and full semantic review remain open.'))
    print('PASS025 actual500/total',meta['translated_units'],'carry consumers',len(preserved),'+ merged',len(merged),'repro',repro)


if __name__=='__main__':main()
