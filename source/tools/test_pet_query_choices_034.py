"""Synthetic source-preserved PET query geometry/refusal fixtures, not runtime."""
import re
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from pet_query_choices_034 import validate


def main():
    path='analysis/full_scope_v1/source_tpl/65B9E8.tpl';full=(ROOT/path).read_text(encoding='utf-8-sig')
    source='@archive 65B9E8\n'+re.search(r'^script 41 mmbn45 \{[\s\S]*?(?=^script\s|\Z)',full,re.M)[0]
    values={u.key:'가'+'\n'*u.text.count('\n')+' '*(len(u.text)-len(u.text.rstrip(' '))) for u in literals(source)}
    target=replace_exact(source,values);ids=set(values);cases=[]
    for pad in (8,16,24):
        old=source.replace('count = 24','count = '+str(pad));new=target.replace('count = 24','count = '+str(pad))
        validate(old,new,[41],ids,99);cases.append(dict(label='two-choice-row2-pad'+str(pad),accepted=True))
    after='\tclearMsg\n\t"가"\n\tkeyWait\n\t\tany = false\n\tclearMsg\n'
    for label,extra in [('post-select-caption',after),('post-select-caption-held',after.rsplit('\tclearMsg\n',1)[0])]:
        old=source.replace('\tflagSet\n',extra+'\tflagSet\n',1);new=target.replace('\tflagSet\n',extra+'\tflagSet\n',1)
        validate(old,new,[41],ids,99);cases.append(dict(label=label,accepted=True))
    def reject(label,change):
        a,b,i=change(source,target,set(ids))
        try:validate(a,b,[41],i,99)
        except ValueError as ex:cases.append(dict(label=label,rejected=True,error=str(ex)));return
        raise ValueError('034 invalid query fixture accepted '+label)
    def both(a,b):return lambda old,new,ids:(old.replace(a,b),new.replace(a,b),ids)
    reject('unsupported-pad',both('count = 24','count = 32'))
    reject('different-window-origin',both('left = 92','left = 52'))
    reject('unknown-provider',both('\tspacePx\n','\tprintStringBuffer1\n\tspacePx\n'))
    reject('unsupported-SFX-command',both('\tspacePx\n','\tsoundDisableChoiceSFX\n\tspacePx\n'))
    reject('different-label-pad',both('count = 1','count = 2'))
    reject('nonclearing-select',both('clear = true','clear = false'))
    reject('different-B-contract',both('BSeparate = false','BSeparate = true'))
    reject('bad-default',both('default = 0','default = 2'))
    reject('bad-flag-range',both('flag = 3605','flag = 65536'))
    reject('broken-navigation',both('left = 1','left = 0'))
    reject('target-control-only',lambda a,b,i:(a,b.replace('count = 24','count = 16'),i))
    reject('outside-selected-ID',lambda a,b,i:(a,b,i|{'65B9E8:99:0'}))
    reject('no-selected-ID',lambda a,b,i:(a,b,set()))
    reject('label-overflow',lambda a,b,i:(a,replace_exact(b,{'65B9E8:41:1':'가'*20}),i))
    reject('multiline-label',lambda a,b,i:(a,replace_exact(b,{'65B9E8:41:1':'가\n가'}),i))
    reject('prompt-overflow',lambda a,b,i:(a,replace_exact(b,{'65B9E8:41:0':'가'*12+'\n\n'}),i))
    reject('fourth-option-row',lambda a,b,i:(a,replace_exact(b,{'65B9E8:41:0':'가\n\n\n'}),i))
    reject('post-terminal-text',both('\twaitHold\n','\twaitHold\n\t"가"\n'))
    reject('source-name-before-option-row',both('\tspacePx\n','\tprintPlayerNickname\n\t\tcapitalizeFirst = false\n\t\tcapitalizeAll = false\n\t\tprintN = false\n\tspacePx\n'))
    positive=sum(x.get('accepted',False) for x in cases)
    deps=[path,'tools/test_pet_query_choices_034.py','tools/pet_query_choices_034.py','tools/pet_choice_capacity_026.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_query_models_v1/result.json',dict(schema=1,passed=True,positive_cases=positive,negative_cases=len(cases)-positive,cases=cases,
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,release_eligible=False,
        limits='Synthetic short literal geometry on source-derived templates; source/control mutations applied equally only to rejection fixtures. Not native EB/EA/EC, external editor/caller, flags, actual canonical wording fit, compilation or ROM approval.'))
    print('034 query model',positive,'positive',len(cases)-positive,'refusals;NO ROM')


if __name__=='__main__':main()
