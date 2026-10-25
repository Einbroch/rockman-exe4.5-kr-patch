"""Controlled acceptance/refusal for the finite direct-profile PET model."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from pet_nickname_capacity_025 import PREFIX
from nickname_capacity import ARGS
from pet_profile_capacity_027_v2 import validate,PROVIDER_BOUNDS
from tpl_literals import literals

def main():
    prefix=''.join('\t'+n+'\n'+a for n,a in PREFIX);wait='\tkeyWait\n\t\tany = false\n';cases=[]
    def wrap(body):return '@archive TEST\n@size 1\nscript 0 mmbn45 {\n'+prefix+body+wait+'\tend\n}\n'
    def check(name,t,good,source=None):
        try:result=validate(source or t,t,[0],{i.key for i in literals(t)},99)
        except ValueError as ex:
            if good:raise
            cases.append(dict(name=name,accepted=False,error=str(ex)));return
        if not good:raise ValueError('Invalid direct-profile fixture accepted '+name)
        if not result:raise ValueError('Missing valid geometry')
        cases.append(dict(name=name,accepted=True))
    for name,bound in PROVIDER_BOUNDS.items():
        base=wrap('\t'+name+'\n'+ARGS+'\t",\\n가나다"\n');check(name,base,True)
        check(name+'-aggregate-overflow',wrap('\t'+name+'\n'+ARGS+'\t"'+'가'*12+'"\n'),False)
        check(name+'-wrong-args',base.replace('printN = false','printN = true'),False)
    check('unknown-array-provider',wrap('\tprintFriend\n'+ARGS+'\t"가나다"\n'),False)
    check('no-provider',wrap('\t"가나다"\n'),False)
    check('four-rows',wrap('\tprintSchool\n'+ARGS+'\t"가\\n나\\n다\\n라"\n'),False)
    valid=wrap('\tprintSchool\n'+ARGS+'\t"가나다"\n')
    check('changed-source-command',valid.replace('printSchool','printDream'),False,valid)
    check('dirty-page-flags',wrap('\tprintSchool\n'+ARGS+'\tflagSet\n\t\tflag = 1\n\t"가나다"\n'),False)
    deps=['tools/test_pet_profile_capacity_027.py','tools/pet_profile_capacity_027_v2.py','tools/profile_provider_bounds_027_v2.py','tools/field_hint_capacity.py','tools/nickname_capacity.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_027_models_test_v1/result.json',dict(schema=1,passed=True,tests=len(cases),cases=cases,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,limits='Controlled geometry/protected-command fixtures only. Not new ROM, dynamic native input/save or semantic approval.'))
    print('PASS027 direct-profile model',len(cases),'fixtures')

if __name__=='__main__':main()
