"""038 component recompile/finalize in CPU-memory fixture, NOT primary build.

Uses prior image only as a diagnostic fixture. Actual product builders running
separately must regenerate the parent from immutable source. No ROM is saved.
"""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from field_native_rom_product_038_v1 import load_inputs,install,verify_final,finalize,predecessor_view
from prepare_source500_038_v5 import baseline,BASE_SHA
from textpet_korean import command
from keyitem_rom_selector import INSTALL
from prepare_repartition500 import layout_records

def main():
    cfg,source,base,meta=baseline();inputs=load_inputs(source);keymeta=deepcopy(meta['keyitem_rom']);work=ROOT/'analysis/pending_insertion_500_038_component_fixture_v1';plugins=ROOT/'analysis/pending_insertion_500_038_native_inputs_v1/plugins'
    append,patches,keymeta,records=install(source,base[len(source):],[(INSTALL,base[INSTALL:INSTALL+12],'diagnostic prior composed stub')],keymeta,inputs,command(plugins),plugins,work/'compile')
    if len(patches)!=1 or patches[0][0]!=INSTALL:raise ValueError('038 diagnostic one composed writer')
    target=bytearray(base);target[INSTALL:INSTALL+12]=patches[0][1];target.extend(append[len(base)-len(source):]);target=bytes(target)
    verify_final(source,target,keymeta);parent=predecessor_view(source,target,keymeta)
    if sha(parent)!=BASE_SHA or parent!=base:raise ValueError('038 unchanged037 full-image gate projection')
    mock=deepcopy(meta);mock['keyitem_rom']=keymeta;before=list(layout_records(mock));finalize(source,target,mock,inputs,records);after=list(layout_records(mock));oldids={u['id'] for r in before for u in r['layout']};newids={u['id'] for r in after for u in r['layout']}
    if len(newids-oldids)!=500 or oldids-newids or len(after)-len(before)!=66 or mock['translated_units']!=meta['translated_units']+500:raise ValueError('038 component full500 finalization')
    cpu=read('analysis/pending_insertion_500_038_selector_cpu_v1/cpu.json')
    if sha(target)!=cpu['fixture_only']['fixture_sha256']:raise ValueError('038 source/assets recompile not CPU fixture image')
    deps=['tools/bench_product_component038_v1.py','tools/field_native_rom_product_038_v1.py','tools/specs/primary038_v1_version.json','analysis/pending_insertion_500_038_native_inputs_v1/manifest.json','analysis/pending_insertion_500_038_selector_cpu_v1/cpu.json']
    frozen_write(work/'verification_v1.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),fixture_sha256=sha(target),fixture_bytes=len(target),predecessor_projection_byte_identical=True,complete_authored_asset_primary_component_recompiles=66,new_unique_ID_delta=500,inherited_IDs_preserved=496,prior_consumer_records_preserved=len(before),fixture_total_IDs=mock['translated_units'],matches_actual_caller_CPU_fixture=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits=['Component exercised against diagnostic prior-image fixture, NOT immutable-source parent regeneration or standalone038 primary build success.','Actual primary/repro builds, whole final diff audit and exact-ROM GBA runtime remain separate.']))
    print('PASS038 component recompile66/full carry/finalize500/prefix gate/CPU full-image identity; NO ROM')

if __name__=='__main__':main()
