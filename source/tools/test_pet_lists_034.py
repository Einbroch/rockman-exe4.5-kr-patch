"""Controlled list grammar/geometry acceptance and refusal fixtures."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from pet_list_capacity_034_v2 import validate
from nickname_capacity import ARGS


def fixture(count,cap,before=False):
    script=52;field=dict(row=5,count=count,cap=cap,list_selector=[script,10])
    def cmd(name,args=''):return '\t'+name+'\n'+args
    text='@archive ABCDEF\nscript 52 mmbn45 {\n'
    for name,args in [('positionBox','\t\tleft = 10\n\t\ttop = 12\n\t\ttype = 1\n'),('msgOpenQuick',''),('positionText','\t\tleft = 92\n\t\ttop = 110\n\t\tarrowDistance = 3\n'),('positionArrow','\t\tleft = 225\n\t\ttop = 141\n'),('flagSet','\t\tflag = 3585\n')]:text+=cmd(name,args)
    if before:text+='\t"가\\n"\n'
    text+=cmd('printPlayerNickname',ARGS)+'\t"의\\n친구는?"\n'+cmd('keyWait','\t\tany = false\n')+cmd('clearMsg')
    for page in range((count+2)//3):
        if page:
            for value in range((page-1)*3+1,page*3+1):text+=cmd('checkGlobal',f'\t\tvariable = 5\n\t\tvalue = {value}\n\t\tjumpIfEqual = 53\n\t\tjumpIfNotEqual = continue\n')
        text+=cmd('printStringBuffer'+str(page+1),ARGS)+cmd('keyWait','\t\tany = false\n')+cmd('clearMsg')
    text+=cmd('jump','\t\ttarget = 53\n')+'}\n'
    return text,field,{'ABCDEF:52:'+str(i) for i in range(2 if before else 1)}


def main():
    positives=[];refusals=[]
    for count,cap in [(3,8),(4,6),(8,6)]:
        for before in (False,True):
            tpl,field,ids=fixture(count,cap,before)
            validate(tpl,tpl,[52],ids,99,field);positives.append(dict(count=count,cap=cap,literal_before_nickname=before))
    tpl,field,ids=fixture(8,6)
    edits=[('initializer',tpl.replace('left = 92','left = 91',1)),('global-index',tpl.replace('variable = 5','variable = 4',1)),('guard-value',tpl.replace('value = 1','value = 0',1)),('guard-target',tpl.replace('jumpIfEqual = 53','jumpIfEqual = 54',1)),('fallthrough',tpl.replace('jumpIfNotEqual = continue','jumpIfNotEqual = 53',1)),('missing-guard',tpl.replace('\tcheckGlobal\n\t\tvariable = 5\n\t\tvalue = 1\n\t\tjumpIfEqual = 53\n\t\tjumpIfNotEqual = continue\n','',1)),('wrong-buffer',tpl.replace('printStringBuffer2','printStringBuffer3',1)),('missing-clear',tpl.replace('\tclearMsg\n','',1)),('wrong-wait',tpl.replace('any = false','any = true',1)),('wrong-terminal',tpl.replace('target = 53','target = 54',1)),('extra-event',tpl.replace('\n}\n','\n\tend\n}\n')),('overflow',tpl.replace('친구는?','가'*20)),('four-rows',tpl.replace('친구는?','가\\n나\\n다')),('nickname-args',tpl.replace('printN = false','printN = true',1)),('duplicate-nickname',tpl.replace('\t"의', '\tprintPlayerNickname\n'+ARGS+'\t"의',1))]
    for name,bad in edits:
        try:validate(bad,bad,[52],ids,99,field)
        except ValueError as ex:refusals.append(dict(kind=name,error=str(ex)))
        else:raise ValueError('List invalid fixture accepted '+name)
    for name,changed,scripts,bound in [('count',dict(field,count=9),[52],99),('cap',dict(field,cap=10),[52],99),('selector',dict(field,list_selector=[52,11]),[52],99),('script',field,[40],99),('nickname-bound',field,[52],100)]:
        try:validate(tpl,tpl,scripts,ids,bound,changed)
        except ValueError as ex:refusals.append(dict(kind=name,error=str(ex)))
        else:raise ValueError('List invalid field accepted '+name)
    try:validate(tpl,tpl.replace('variable = 5','variable = 4',1),[52],ids,99,field)
    except ValueError as ex:refusals.append(dict(kind='source-control-mutation',error=str(ex)))
    else:raise ValueError('List protected control mutation accepted')
    deps=['tools/test_pet_lists_034.py','tools/pet_list_capacity_034_v2.py','tools/nickname_capacity.py','tools/field_hint_capacity.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_list_models_v1/result.json',dict(schema=1,passed=True,positive_count=len(positives),refusal_count=len(refusals),positives=positives,refusals=refusals,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,release_eligible=False))
    print('034 list models',len(positives),'positive',len(refusals),'refusal PASS')


if __name__=='__main__':main()
