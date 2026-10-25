"""Controlled conformance/refusal fixtures for finite026 geometry contracts."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from tpl_literals import literals
from normal_battle_choice_capacity_026 import validate as horizontal
from normal_vertical_choice_capacity_026 import validate as vertical
from pet_choice_capacity_026 import validate as pet
from pet_nickname_capacity_025 import PREFIX

OUT='analysis/pending_insertion_500_026_models_test_v1/result.json'

def main():
    nav0='\toption\n\t\tbrackets = false\n\t\tleft = 1\n\t\tright = 1\n\t\tup = 0\n\t\tdown = 1\n\tspace\n\t\tcount = 1\n'
    nav1=nav0.replace('left = 1','left = 0').replace('right = 1','right = 0')
    select=('\tselect\n\t\tdefault = 0\n\t\tlastCancelSFX = false\n\t\tnoDelay = false\n\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = true\n\t\ttargets = [\n\t\t\tjump = continue,\n\t\t\tjump = 3,\n\t\t\tjump = continue\n\t\t]\n')
    prefix=''.join('\t'+name+'\n'+args for name,args in PREFIX)
    def wrap(body):return '@archive TEST\n@size 4\nscript 0 mmbn45 {\n'+body+'\tend\n}\n'
    h=wrap('\tmsgOpen\n\tpositionOptionHorizontal\n\t\twidth = 8\n'+nav0+'\t"A"\n'+nav1+'\t"B"\n'+select+'\tclearMsg\n\tstoreGlobal8\n\t\tglobal = 8\n\t\tvalue = 255\n\tstoreGlobal16\n\t\tglobal = 10\n\t\tvalue = 6082\n\t"C"\n\tkeyWait\n\t\tany = false\n')
    v=wrap('\tmsgOpen\n\tpositionOptionVertical\n\t\twidth = 6\n'+nav0+'\t"A\\n"\n\tpositionOptionVertical\n\t\twidth = 6\n'+nav1+'\t"B"\n'+select)
    p=wrap(prefix+'\tspacePx\n\t\tcount = 16\n'+nav0+'\t"A"\n'+nav1+'\t"B"\n'+select)
    cases=[]
    def check(name,fn,text,accept,source=None):
        ids={i.key for i in literals(text)}
        try:
            args=[source or text,text,[0],ids,99]
            if fn is not pet:args.append(88)
            result=fn(*args)
        except ValueError as ex:
            if accept:raise
            cases.append(dict(name=name,accepted=False,reason=str(ex)));return
        if not accept:raise ValueError('Accepted invalid controlled fixture '+name)
        if not result:raise ValueError('No geometry for valid fixture')
        cases.append(dict(name=name,accepted=True))
    for name,fn,t in [('horizontal',horizontal,h),('vertical',vertical,v),('pet',pet,p)]:
        check(name,fn,t,True)
        for suffix,old,new in [('unknown-provider','\tend\n','\tprintFriend\n\tend\n'),
                               ('unbounded-nav','left = 1','left = 2'),('no-pad','count = 1\n','count = 2\n'),
                               ('clear-false','clear = true','clear = false'),('brackets','brackets = false','brackets = true'),
                               ('multiline-last','\t"B"','\t"B\\nC"'),('overwide','\t"B"','\t"'+'가'*20+'"')]:
            if old not in t:raise ValueError('Fixture mutation missing')
            check(name+'-'+suffix,fn,t.replace(old,new,1),False)
        check(name+'-protected-command',fn,t.replace('default = 0','default = 1'),False,source=t)
    check('vertical-disableB',vertical,v.replace('disableB = false','disableB = true'),True)
    check('vertical-width11',vertical,v.replace('width = 6','width = 11'),False)
    check('vertical-missing-first-LF',vertical,v.replace('A\\n','A'),False)
    check('vertical-width-mismatch',vertical,v.replace('width = 6','width = 7',1),False)
    check('vertical-inline-prompt',vertical,v.replace('\tmsgOpen\n','\tmsgOpen\n\t"C\\n"\n'),False)
    check('pet-offset15',pet,p.replace('count = 16','count = 15'),False)
    check('pet-dirty-page',pet,p.replace('\tspacePx\n','\t"C"\n\tspacePx\n'),False)
    check('horizontal-global-slot7',horizontal,h.replace('global = 8','global = 7'),False)
    check('horizontal-global8-overflow',horizontal,h.replace('value = 255','value = 256'),False)
    check('horizontal-global16-overflow',horizontal,h.replace('value = 6082','value = 65536'),False)
    check('horizontal-global-dirty',horizontal,h.replace('\tstoreGlobal8\n','\t"D"\n\tstoreGlobal8\n'),False)
    deps=['tools/test_layout500_026.py','tools/normal_battle_choice_capacity_026.py','tools/normal_vertical_choice_capacity_026.py','tools/pet_choice_capacity_026.py','tools/pet_nickname_capacity_025.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,tests=len(cases),cases=cases,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,limits='Controlled geometry acceptance/refusal only, not current product integration or runtime evidence.'))
    print('PASS026 controlled model fixtures',len(cases))

if __name__=='__main__':main()
