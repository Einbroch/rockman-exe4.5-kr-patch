"""040 memory-only component check; previous039 comparison is NOT primary input."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from typed_rom_product040_v2 import load_inputs,install,verify_final,predecessor_view,finalize,BASE,BASE_SHA,MANIFEST,CPU
from textpet_korean import command
from keyitem_rom_selector import INSTALL
from prepare_repartition500 import layout_records


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);base=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'));inputs=load_inputs(source);km=deepcopy(meta['keyitem_rom']);work=ROOT/'analysis/pending_insertion_500_040_component_fixture_v2';plugins=ROOT/'analysis/pending_insertion_500_040_source_v2/compile_v1/plugins'
    append,patches,km,records=install(source,base[len(source):],[(INSTALL,base[INSTALL:INSTALL+12],'diagnostic039 stub')],km,inputs,command(plugins),plugins,work/'compile')
    if len(patches)!=1 or patches[0][0]!=INSTALL:raise ValueError('040 diagnostic single writer')
    target=bytearray(base);target[INSTALL:INSTALL+12]=patches[0][1];target.extend(append[len(base)-len(source):]);target=bytes(target);verify_final(source,target,km)
    if predecessor_view(source,target,km)!=base:raise ValueError('040 exact039 projection')
    mock=deepcopy(meta);mock['keyitem_rom']=km;before=list(layout_records(mock));finalize(source,target,mock,inputs,records);after=list(layout_records(mock));oldids={u['id'] for r in before for u in r['layout']};newids={u['id'] for r in after for u in r['layout']}
    if len(newids-oldids)!=500 or oldids-newids or len(after)-len(before)!=10 or mock['translated_units']!=meta['translated_units']+500:raise ValueError('040 exact500 diagnostic finalize')
    if sha(target)!=read(CPU)['fixture_only']['fixture_sha256']:raise ValueError('040 component/CPU complete byte identity')
    serialized=__import__('json').loads(__import__('json').dumps(km));verify_final(source,target,serialized)
    deps=['tools/bench_product_component040_v2.py','tools/typed_rom_product040_v2.py',MANIFEST,CPU,'tools/specs/primary040_v2_version.json']
    frozen_write(work/'verification_v1.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),fixture_sha256=sha(target),fixture_bytes=len(target),new_unique_ID_delta=500,inherited_IDs_preserved=8,prior_consumer_records_preserved=len(list(__import__('verify_pending500_002_rom').clones(meta))),prior_metadata_records_preserved=len(before),new_consumers=10,fixture_total_IDs=mock['translated_units'],predecessor_projection_byte_identical=True,matches_selector_PREFIX_CPU_fixture=True,metadata_JSON_roundtrip_verified=True,rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Memory comparison039 fixture only, NOT cumulative primary or new040 GBA file.','Korean040 runtime, BBS168px/cache/terminal/exit and tournament exact artifact consumption still required.']))
    print('PASS040 component10/new500/carry8/old661/039 gate/CPU wholeimage identity; NO ROM')


if __name__=='__main__':main()
