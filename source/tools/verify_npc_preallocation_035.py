"""In-memory append/component composition check; no game ROM output."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from inspect_remaining_035 import BASE,BASE_SHA
from field_npc_rom_product_035 import load_inputs,install,verify_final,finalize
from keyitem_rom_selector import INSTALL
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES

OUT='analysis/pending_insertion_500_035_npc_preallocation_v1'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'));inputs=load_inputs(source)
    out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));km=deepcopy(meta['keyitem_rom'])
    #034 is an explicit comparison/component fixture only, not primary-build input.
    tail,patches,km,records=install(source,rom[len(source):],[(INSTALL,rom[INSTALL:INSTALL+12],'fixture preceding reader')],km,inputs,command(out/'plugins'),out/'plugins',out/'compile')
    target=bytearray(rom+tail[len(rom)-len(source):]);target[INSTALL:INSTALL+12]=patches[0][1]
    verify_final(source,target,km)
    model=deepcopy(meta);model['keyitem_rom']=km;finalize(source,target,model,inputs,records)
    refusals=[]
    for label,at in [('stub',INSTALL),('code',km['npc035']['code_offset']),('descriptor',km['npc035']['descriptor_offset']),('native-identity',km['npc035']['placements'][0]['native_copy_offset']),('target-text',km['npc035']['placements'][0]['rom_offset']),('original-compression',inputs[0][0]['source_row']['offset']),('original-reference',inputs[0][0]['source_row']['pointers'][0])]:
        broken=bytearray(target);broken[at]^=1
        try:verify_final(source,broken,km)
        except ValueError as ex:refusals.append(dict(kind=label,error=str(ex)))
        else:raise ValueError('035 missed placed corruption '+label)
    deps=['tools/verify_npc_preallocation_035.py','tools/field_npc_rom_product_035.py','tools/field_npc_rom_selector_035_v2.py','analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json']
    frozen_write(out/'verification.json',dict(schema=1,status='MEMORY_ONLY_NPC_APPEND_COMPOSITION_PASS_NOT_PRIMARY_ROM',passed=True,baseline_sha256=BASE_SHA,new_units=500,archives=9,refusals=refusals,
        prior034_bytes_unchanged_except_single_reader_stub=True,full_prior_metadata_and_literal_population_preserved=True,source_recompiled_target_bytes=True,
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,product_integrated=False,runtime_tested=False,release_eligible=False,
        limits='034 appended data used only as an in-memory component fixture to exercise composition. No game ROM emitted. The primary build must independently reconstruct all preceding content from immutable original source. Final-placement/repro/runtime remain required.'))
    print('035 memory-only append/one-stub/500delta',len(refusals),'corruption refusals PASS;NO ROM')

if __name__=='__main__':main()
