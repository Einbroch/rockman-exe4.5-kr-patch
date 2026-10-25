"""Controlled accepted/rejected input cases for immutable-source102 component API."""
from copy import deepcopy
from fixture_subchip041_v3 import construct,SOURCE
from subchip_rom_component041_v2 import plan
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write


def main():
    source,base,meta,image,rows,f=construct();kw=dict(source=source,source_sha256=sha(source),start_offset=len(base),previous_entry=f['previous_wrapper_address'],rows=rows);valid=plan(**kw);second=plan(**deepcopy(kw))
    if valid!=second or valid['audit']['selected_units']!=102 or valid['audit']['source_archives']!=21 or valid['audit']['rom_written']:raise ValueError('041 component accepted deterministic input')
    rejected=[]
    def check(name,change,expected):
        args=deepcopy(kw);change(args)
        try:plan(**args)
        except ValueError as error:
            if expected not in str(error):raise ValueError(('041 controlled rejection wrong boundary',name,str(error)))
            rejected.append(dict(case=name,error=str(error)))
        else:raise ValueError('041 invalid component input accepted: '+name)
    check('wrong-source-hash',lambda k:k.update(source_sha256='0'*64),'immutable source')
    check('unaligned-append',lambda k:k.update(start_offset=k['start_offset']+1),'immutable source')
    check('append-inside-original',lambda k:k.update(start_offset=len(source)-4),'immutable source')
    check('predecessor-after-append',lambda k:k.update(previous_entry=0x08000000+k['start_offset']),'immutable source')
    check('odd-predecessor',lambda k:k.update(previous_entry=k['previous_entry']|1),'immutable source')
    check('missing-archive',lambda k:k['rows'].pop(),'archive population')
    check('duplicate-archive',lambda k:k['rows'][-1].update(archive=k['rows'][0]['archive']),'archive population')
    check('wrong-source-family',lambda k:k['rows'][0].update(archive='6DD0B8'),'original subchip table')
    def source_word(k,at,value):
        b=bytearray(k['source']);b[at:at+4]=value.to_bytes(4,'little');k.update(source=bytes(b),source_sha256=sha(b))
    check('populate-original-NULL13',lambda k:source_word(k,0x41F38+13*4,0x086F9B4C),'NULL slots')
    check('populate-original-NULL14',lambda k:source_word(k,0x41F38+14*4,0x086F9B4C),'NULL slots')
    check('wrong-loader-root',lambda k:source_word(k,0x41F94,0x02024000),'original subchip table')
    check('wrong-reader-root',lambda k:source_word(k,0x41D98,0x02024000),'original subchip table')
    check('empty-target',lambda k:k['rows'][0].update(target=b''),'native/count/target')
    check('oversized-target',lambda k:k['rows'][0].update(target=b'\0'*65536),'native/count/target')
    check('corrupt-native-copy',lambda k:k['rows'][0].update(native=b'\0'+k['rows'][0]['native'][1:]),'native/count/target')
    check('invalid-count',lambda k:k['rows'][0].update(scripts=33),'native/count/target')
    check('unselected-small-script',lambda k:k['rows'][0].update(selected_scripts=[0]),'native/count/target')
    check('script-mask-overflow',lambda k:k['rows'][0].update(selected_scripts=[32]),'native/count/target')
    check('duplicate-script',lambda k:k['rows'][0]['selected_scripts'].append(k['rows'][0]['selected_scripts'][0]),'native/count/target')
    check('duplicate-ID',lambda k:k['rows'][0]['selected_ids'].append(k['rows'][0]['selected_ids'][0]),'native/count/target')
    check('ID-script-mismatch',lambda k:k['rows'][0].update(selected_ids=[k['rows'][0]['archive']+':0:0']),'stable selected IDs')
    def mutate_unselected(k):
        r=k['rows'][0];b=bytearray(r['target']);at=int.from_bytes(b[:2],'little');b[at]^=1;r['target']=bytes(b)
    check('unselected-native-script-changed',mutate_unselected,'unselected script bytes changed')
    if len(rejected)!=22:raise ValueError('041 invalid-input fixture denominator')
    deps=['tools/bench_subchip_component041_v1.py','tools/subchip_rom_component041_v2.py','tools/subchip_rom_selector041_v1.py','tools/fixture_subchip041_v3.py',SOURCE+'/subchip_selector_cpu_v3.json']
    frozen_write(ROOT/SOURCE/'subchip_component_inputs_v1.json',dict(passed=True,status='041_COMPONENT_API_VALID_INPUT_AND22_REJECTION_CASES_NOT_ROM',source_sha256=sha(source),baseline_sha256=sha(base),valid_inputs_accepted=True,independent_plan_identical=True,selected_units=102,archives=21,invalid_inputs_rejected=rejected,planned_append_bytes=len(valid['tail']),plan_only_sha256=sha(valid['tail']),full500_orchestrator_still_required=True,rom_written=False,new_units_applied=0,product_integrated=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Controlled API conformance cases, not new041 screen/loader or release proof.','Pure component API assumes primary has verified authored inputs/lineage and registered complete500; it must not be used to emit a partial102-cohort ROM.','No source ROM, user save or distribution package modified.']))
    print('PASS041 component API deterministic valid102/21 and22 invalid-input rejections; no ROM')


if __name__=='__main__':main()
