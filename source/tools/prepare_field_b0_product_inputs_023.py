"""Compile source-bound exact500 via the primary archive component; no ROM."""
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from textpet_korean import prepare_plugins,command
from build_development_patch import compile_archive
from korean_codec import EXTRA_CHARACTER_INDICES


def main():
    base='analysis/pending_insertion_500_023_b0_reuse_v1'
    selection=read(base+'/selection.json');inputs=read(base+'/prepared_inputs.json');extraction=read('analysis/field_b0_hints_v1/extraction.json');by={r['archive']:r for r in extraction['archives']}
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,selection['source_sha256']);source=sp.read_bytes();require_hash(ROOT/selection['baseline_rom'],selection['baseline_sha256'])
    out=ROOT/'analysis/pending_insertion_500_023_product_preflight_v2'
    out.mkdir(parents=True,exist_ok=False);plugins=out/'plugins';prepare_plugins(plugins,set(EXTRA_CHARACTER_INDICES));common=command(plugins);records=[]
    for entry in inputs['archives']:
        require_hash(ROOT/entry['path'],entry['sha256']);asset=read(entry['path']);arc=asset['archive'];native=by[arc]
        groups=[g for g in selection['groups'] if g['archive']==arc];layouts={k:v for g in groups for k,v in g['individual_layouts'].items()}
        for u in asset['units']:
            if u['id'] in layouts:u['translation']=layouts[u['id']]
        ids=[u['id'] for u in asset['units']];scripts=sorted({int(key.split(':')[1]) for key in ids})
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=scripts,literal_ids=ids,script_count=255,max_literal_rows=3,max_line_advance=180,max_compiled_bytes=65535,preserve_literal_numerals=True,field_hint_capacity_profile='b0-native-insertions-v1')
        row=dict(offset=int(arc,16),compressed=True,size=native['compressed_bytes_consumed'],size_header=False,pointers=[native['source_pointer']])
        payload,record=compile_archive(source,row,asset,scope,common,plugins,out/arc)
        record.update(input_asset=entry,scope=scope,individual_layouts=layouts,source_catalog_row=row,navi_index=native['navi_index'],script_count=255)
        records.append(record);print('PASS primary archive preflight',arc,len(ids),flush=True)
    if sum(r['translated_units'] for r in records)!=500:raise ValueError('Exact500 source preflight denominator')
    deps=[base+'/selection.json',base+'/prepared_inputs.json','analysis/field_b0_hints_v1/extraction.json','analysis/pending_insertion_500_023_capacity_v2/survey.json','analysis/pending_insertion_500_023_reader_v1/cpu.json','tools/build_development_patch.py','tools/field_hint_capacity.py','tools/prepare_field_b0_product_inputs_023.py']
    # The capacity survey predates the additional source-binding wrapper in the
    # same module. It remains historical analysis, not a current code-hash gate;
    # primary archive compilation above recomputes all source/layout invariants.
    frozen_write(out/'preflight.json',dict(schema=1,batch_id='pending-insertion-500-023-b0',status='PRIMARY_ARCHIVE_COMPONENT_PREFLIGHT_PASS_NO_ROM',source_sha256=sha(source),baseline_rom=selection['baseline_rom'],baseline_sha256=selection['baseline_sha256'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},total_units=500,archives=records,rom_written=False,reader_registered_in_product=False,runtime_tested=False,release_eligible=False,limits='Exact selected500 source-bound compiled/layout/provider/control/byte-roundtrip proof through primary compile_archive. This component preflight is not an integrated product build. Original compressed data/pointers remain untouched; B0 descriptor installation, cumulative final-write verification/independent rebuild and own-ROM GBA runtime still required.'))
    print('PASS exact500 primary archive preflight; NO ROM written')


if __name__=='__main__':main()
