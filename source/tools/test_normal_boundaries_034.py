"""Controlled grammar/geometry refusal coverage for two034 adapters."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from normal_jump_tail_034 import validate as jump
from normal_leading_clear_034 import validate as clear


def main():
    a='@archive 71A66C\nscript 19 mmbn45 {\n\tmsgOpen\n\t"가"\n\tkeyWait\n\t\tany = false\n\tclearMsg\n\tjump\n\t\ttarget = 1\n\tend\n}\n'
    b='@archive 6FE8D4\nscript 21 mmbn45 {\n\tclearMsg\n\tmsgOpen\n\t"가"\n\tkeyWait\n\t\tany = false\n\tend\n}\n'
    jump(a,a,[19],{'71A66C:19:0'},99);clear(b,b,[21],{'6FE8D4:21:0'},99);refused=[]
    changes=[('target255',jump,a.replace('target = 1','target = 255'),[19],{'71A66C:19:0'}),('target-continue',jump,a.replace('target = 1','target = continue'),[19],{'71A66C:19:0'}),('two-ends',jump,a.replace('\tend\n','\tend\n\tend\n'),[19],{'71A66C:19:0'}),('no-cleared-page',jump,a.replace('\tclearMsg\n',''),[19],{'71A66C:19:0'}),('wrong-root',jump,a.replace('71A66C','ABCDEF'),[19],{'ABCDEF:19:0'}),('jump-overflow',jump,a.replace('"가"','"'+'가'*20+'"'),[19],{'71A66C:19:0'}),('missing-open',clear,b.replace('\tmsgOpen\n',''),[21],{'6FE8D4:21:0'}),('clear-after-open',clear,b.replace('\tclearMsg\n\tmsgOpen\n','\tmsgOpen\n\tclearMsg\n'),[21],{'6FE8D4:21:0'}),('duplicate-clear',clear,b.replace('\tclearMsg\n','\tclearMsg\n\tclearMsg\n'),[21],{'6FE8D4:21:0'}),('trader-wrong-root',clear,b.replace('6FE8D4','ABCDEF'),[21],{'ABCDEF:21:0'}),('wrong-script',clear,b.replace('script 21','script 20'),[20],{'6FE8D4:20:0'}),('no-wait',clear,b.replace('\tkeyWait\n\t\tany = false\n',''),[21],{'6FE8D4:21:0'}),('clear-overflow',clear,b.replace('"가"','"'+'가'*20+'"'),[21],{'6FE8D4:21:0'})]
    for name,fn,bad,scripts,ids in changes:
        try:fn(bad,bad,scripts,ids,99)
        except ValueError as ex:refused.append(dict(kind=name,error=str(ex)))
        else:raise ValueError('034 invalid normal adapter accepted '+name)
    for name,fn,tpl,scripts,ids in [('jump-control-mutation',jump,a,[19],{'71A66C:19:0'}),('clear-control-mutation',clear,b,[21],{'6FE8D4:21:0'})]:
        changed=tpl.replace('any = false','any = true')
        try:fn(tpl,changed,scripts,ids,99)
        except ValueError as ex:refused.append(dict(kind=name,error=str(ex)))
        else:raise ValueError('034 source command mutation accepted')
    deps=['tools/test_normal_boundaries_034.py','tools/normal_jump_tail_034.py','tools/normal_leading_clear_034.py','tools/normal_timing_capacity_025.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_034_normal_models_v1/result.json',dict(schema=1,passed=True,positive_count=2,refusal_count=len(refused),refusals=refused,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,release_eligible=False))
    print('034 normal boundary models 2 positive',len(refused),'refusal PASS')


if __name__=='__main__':main()
