"""Diagnostic039 component memory fixture, NOT immutable-source primary build."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from communication_rom_product039_v1 import load_inputs,install,verify_final,predecessor_view,finalize,BASE,BASE_SHA,MANIFEST,CPU
from textpet_korean import command
from keyitem_rom_selector import INSTALL
from prepare_repartition500 import layout_records


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'));inputs=load_inputs(source);km=deepcopy(meta['keyitem_rom']);work=ROOT/'analysis/pending_insertion_500_039_component_fixture_v1';plugins=ROOT/'analysis/pending_insertion_500_039_communication_inputs_v1/plugins'
    append,patches,km,records=install(source,base[len(source):],[(INSTALL,base[INSTALL:INSTALL+12],'diagnostic038 stub')],km,inputs,command(plugins),plugins,work/'compile')
    if len(patches)!=1 or patches[0][0]!=INSTALL:raise ValueError('039 diagnostic single writer')
    target=bytearray(base);target[INSTALL:INSTALL+12]=patches[0][1];target.extend(append[len(base)-len(source):]);target=bytes(target)
    verify_final(source,target,km)
    if predecessor_view(source,target,km)!=base:raise ValueError('039 exact038 projection')
    mock=deepcopy(meta);mock['keyitem_rom']=km;before=list(layout_records(mock));finalize(source,target,mock,inputs,records);after=list(layout_records(mock));oldids={u['id'] for r in before for u in r['layout']};newids={u['id'] for r in after for u in r['layout']}
    if len(newids-oldids)!=500 or oldids-newids or len(after)-len(before)!=17 or mock['translated_units']!=meta['translated_units']+500:raise ValueError('039 exact500 diagnostic finalize')
    if sha(target)!=read(CPU)['fixture_only']['fixture_sha256']:raise ValueError('039 component/CPU byte identity')
    deps=['tools/bench_product_component039_v1.py','tools/communication_rom_product039_v1.py',MANIFEST,CPU,'tools/specs/primary039_v1_version.json']
    frozen_write(work/'verification_v1.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),fixture_sha256=sha(target),fixture_bytes=len(target),new_unique_ID_delta=500,prior_consumer_records_preserved=len(before),new_consumers=17,fixture_total_IDs=mock['translated_units'],predecessor_projection_byte_identical=True,matches_selector_PREFIX_CPU_fixture=True,rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Comparison038 image only used in diagnostic memory; actual primary must reconstruct all preceding components from source.','No complete initialization, GBA screen/runtime or release proof.']))
    print('PASS039 component recompile17 /new500 /old644 /parent038 gate /CPU identity; NO ROM')


if __name__=='__main__':main()
