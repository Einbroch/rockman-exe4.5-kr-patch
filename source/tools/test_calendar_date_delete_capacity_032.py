"""Controlled source-template date geometry acceptance and symmetric refusals."""
import re
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from calendar_date_delete_capacity_032 import validate
from survey_pet_quick_reflow_024 import replace_for_analysis


def main():
    source=(ROOT/'analysis/tpl_baseline/659CB8.tpl').read_text(encoding='utf-8-sig');fixtures={};cases=[]
    for script in (51,52):
        original='@archive 659CB8\n'+re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',source,re.M)[0]
        from tpl_literals import literals
        ja=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
        if len(ja)!=4:raise ValueError('032 fixed source template changed')
        values=['」\n가','나?\n\n','예  ','아니요'];units=[dict(id=x.key,source=x.text,translation=t,state='needs_review') for x,t in zip(ja,values)];target=replace_for_analysis(original,units);ids={u['id'] for u in units};fixtures[script]=(original,target,ids,units)
        proof=validate(original,target,[script],ids)
        if proof[0]['pages'][0]['dynamic_slots']!=(5 if script==51 else 3):raise ValueError('032 controlled date slot count')
        cases.append(dict(fixture='valid-calendar-'+str(script),accepted=True))
    original,target,ids,units=fixtures[51]
    def refuse(name,old,new,script=51,selected=None):
        try:validate(old,new,[script],ids if selected is None else selected)
        except ValueError as ex:cases.append(dict(fixture=name,rejected=True,error=str(ex)));return
        raise ValueError('032 invalid date geometry accepted '+name)
    def both(name,before,after):
        if before not in original or before not in target:raise ValueError('032 fixture anchor '+name)
        refuse(name,original.replace(before,after),target.replace(before,after))
    both('undeclared-calendar','@archive 659CB8','@archive 123456')
    both('unknown-year-provider','callBufferEventYear','callBufferCurrentYear')
    both('year-no-zero-padding','padZeros = true','padZeros = false')
    both('dayname-missing-producer','callBufferEventDayName','callBufferEventAMPM')
    both('unknown-name-provider','callBufferEventName','printPlayerNickname')
    both('unexpected-native-choice-allocation','width = 8','width = 9')
    both('unexpected-choice-space','count = 1','count = 2')
    both('changed-default-option','default = 0','default = 1')
    both('B-input-disabled','disableB = false','disableB = true')
    both('choice-does-not-clear','clear = true','clear = false')
    both('different-native-wait','any = false','any = true')
    both('extra-unmodeled-script-event','\tend\n','\tend\n\tmugshotHide\n')
    refuse('target-protected-token-change',original,target.replace('width = 8','width = 7'))
    refuse('unbound-id',original,target,selected={'659CB8:51:999'})
    over=[dict(u) for u in units];over[0]['translation']='가'*20
    refuse('name-plus-literal-aggregate-overflow',original,replace_for_analysis(original,over))
    over=[dict(u) for u in units];over[1]['translation']='나?\n'
    refuse('choice-row-not-empty-three-row',original,replace_for_analysis(original,over))
    over=[dict(u) for u in units];over[2]['translation']='예'*10
    refuse('choice-label-exceeds-native93',original,replace_for_analysis(original,over))
    out=ROOT/'analysis/pending_insertion_500_032_date_models_v1/result.json';frozen_write(out,dict(schema=1,passed=True,controlled_cases=cases,positive_cases=2,negative_cases=len(cases)-2,fixture_source=dict(path='analysis/tpl_baseline/659CB8.tpl',sha256=sha((ROOT/'analysis/tpl_baseline/659CB8.tpl').read_bytes())),checker=dict(path='tools/test_calendar_date_delete_capacity_032.py',sha256=sha((ROOT/'tools/test_calendar_date_delete_capacity_032.py').read_bytes())),rom_written=False,release_eligible=False,limits='Controlled native51/52 fixture models, not current translation semantic review or runtime proof.'))
    print('032 calendar date models PASS',len(cases),'controlled cases')


if __name__=='__main__':main()
