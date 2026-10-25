"""Source/descriptor applicability refusals; no ROM emitted or modified."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from prepare_source500_037_v2 import baseline
from prepare_native_inputs037_v2 import OUT,selected_from
from field_native_rom_selector_037_v2 import source_population,contracts,wrap


def main():
    cfg,source,base,m=baseline();manifest=read(OUT+'/manifest.json');selected=selected_from(manifest['archives']);pool=source_population(source,selected);rows=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError) as e:rows.append(dict(name=name,rejected=True,error=str(e)));return
        raise ValueError('Unexpected acceptance: '+name)
    for kind,at in [('npc_BL',0x4F76E),('board_BL',0x6A502),('npc_root',0x4F78C),('board_root',0x6A50C),('npc_argument',0x4F76A),('board_argument',0x6A500)]:
        altered=bytearray(source);altered[at]^=1;reject(kind,lambda b=bytes(altered):contracts(b))
    for counter in (0,256,-1,True):reject('descriptor_counter_'+str(counter),lambda c=counter:wrap(source,0x08C20000,0x08C00000,0x08C10000,c))
    for args in [(0x08C20002,0x08C00000,0x08C10000,70),(0x08C20000,0x08C00000,0x08C20000,70),(0x08C20000,0x07000000,0x08C10000,70)]:reject('placement_'+str(args),lambda a=args:wrap(source,*a))
    for kind in ('missing-equivalent-owner','different-target-bytes','different-script-count','different-scene','different-class'):
        bad=deepcopy(selected)
        if kind=='missing-equivalent-owner':del bad['7B450C']
        elif kind=='different-target-bytes':bad['7B450C']['target_sha256']='0'*64
        elif kind=='different-script-count':bad['7B450C']['script_count']=254
        elif kind=='different-scene':bad['7B450C']['scene']=0xA2
        else:bad['7B450C']['source_class']='field-board'
        reject(kind,lambda b=bad:source_population(source,b))
    equivalents={}
    for arc in ('7B3120','7B3E60','7B450C'):
        r=next(p for p in pool if p['archive']==arc);equivalents[arc]=dict(native_sha256=sha(r['payload']),target_sha256=selected[arc]['target_sha256'],script_count=selected[arc]['script_count'])
    frozen_write(ROOT/'analysis/pending_insertion_500_037_selector_cpu_v2/guards_v1.json',dict(passed=True,scope='Finite037 source applicability/alias rejection fixtures, not all malformed-input or runtime evidence',baseline_sha256=sha(base),accepted_equivalent_aliases=equivalents,rejected_fixtures=rows,count=len(rows),rom_written=False,new_units_applied=0,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_native037_guards_v1.py','tools/field_native_rom_selector_037_v2.py',OUT+'/manifest.json']}))
    print('PASS037',len(rows),'source/alias applicability refusals; no ROM written')


if __name__=='__main__':main()
