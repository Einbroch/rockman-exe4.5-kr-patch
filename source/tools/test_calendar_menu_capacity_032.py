"""Controlled short-caption fixtures for the calendar menu geometry model."""
import re
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from calendar_menu_capacity_032_v2 import validate
from tpl_literals import literals
from survey_pet_quick_reflow_024 import replace_for_analysis


def main():
    fixtures={};cases=[];sources={}
    for arc,script in [('659CB8',0),('659CB8',2),('659CB8',3),('659CB8',4),('659CB8',10),('659CB8',24),('65F11C',25),('6762A8',30),('659CB8',63)]:
        path='analysis/tpl_baseline/'+arc+'.tpl';tpl=(ROOT/path).read_text(encoding='utf-8-sig');sources[path]=sha((ROOT/path).read_bytes());match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)
        if not match:continue
        old='@archive '+arc+'\n'+match[0];units=[dict(id=x.key,source=x.text,translation='가'+'\n'*x.text.count('\n'),state='needs_review') for x in literals(old) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)];new=replace_for_analysis(old,units);ids={u['id'] for u in units};validate(old,new,[script],ids);fixtures[(arc,script)]=(old,new,ids,units);cases.append(dict(fixture=arc+':'+str(script),accepted=True))
    def refuse(label,key,change):
        old,new,ids,units=fixtures[key];old,new,ids=change(old,new,ids,units)
        try:validate(old,new,[key[1]],ids)
        except ValueError as ex:cases.append(dict(fixture=label,rejected=True,error=str(ex)));return
        raise ValueError('032 invalid menu accepted '+label)
    def both(before,after):return lambda a,b,i,u:(a.replace(before,after),b.replace(before,after),i)
    key=('659CB8',2)
    refuse('undeclared-root',key,both('@archive 659CB8','@archive 123456'))
    refuse('different-explicit-box',key,both('\tmsgOpenQuick\n','\tmsgOpen\n'))
    refuse('vertical-width-not-seven',key,both('width = 7','width = 8'))
    refuse('vertical-B-contract',key,both('BSeparate = true','BSeparate = false'))
    refuse('vertical-clear-contract',key,both('clear = false','clear = true'))
    refuse('vertical-navigation-contract',key,both('up = 1','up = 0'))
    refuse('unsupported-space-width',key,both('count = 1','count = 2'))
    refuse('extra-event-after-hold',key,both('\twaitHold\n','\twaitHold\n\tend\n'))
    refuse('unbound-ID',key,lambda a,b,i,u:(a,b,{'659CB8:2:999'}))
    refuse('protected-target-control',key,lambda a,b,i,u:(a,b.replace('width = 7','width = 8'),i))
    refuse('current-date-unmodeled-provider',('659CB8',0),both('callBufferCurrentMonth','callBufferCurrentYear'))
    refuse('current-date-pad-zero',('659CB8',0),both('padZeros = false','padZeros = true'))
    refuse('horizontal-nonclearing',('659CB8',24),both('clear = true','clear = false'))
    refuse('wrong-fire-width',('6762A8',30),both('width = 7','width = 8'))
    def overflow(a,b,ids,u):
        values=[dict(x) for x in u];values[0]['translation']='가'*20+'\n'*values[0]['source'].count('\n');return a,replace_for_analysis(a,values),ids
    refuse('horizontal-prompt-overflow',('659CB8',24),overflow)
    refuse('single-caption-name-aggregate-overflow',('659CB8',10),overflow)
    def bad_vertical_label(a,b,ids,u):
        values=[dict(x) for x in u];values[1]['translation']='가'*8+'\n';return a,replace_for_analysis(a,values),ids
    refuse('vertical-85px-option-overflow',key,bad_vertical_label)
    frozen_write(ROOT/'analysis/pending_insertion_500_032_menu_models_v1/result.json',dict(schema=1,passed=True,positive_cases=sum(c.get('accepted',False) for c in cases),negative_cases=sum(c.get('rejected',False) for c in cases),cases=cases,fixture_sources=sources,model=dict(path='tools/calendar_menu_capacity_032_v2.py',sha256=sha((ROOT/'tools/calendar_menu_capacity_032_v2.py').read_bytes())),checker=dict(path='tools/test_calendar_menu_capacity_032.py',sha256=sha((ROOT/'tools/test_calendar_menu_capacity_032.py').read_bytes())),rom_written=False,release_eligible=False,limits='Synthetic short Korean labels on frozen source templates. Not current500 semantics, caller origin universality or runtime proof.'))
    print('032 menu models PASS',len(cases),'controlled fixtures')


if __name__=='__main__':main()
