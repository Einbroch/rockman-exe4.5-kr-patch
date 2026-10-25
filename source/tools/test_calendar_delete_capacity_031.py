"""Finite calendar50 topology/geometry acceptance and refusal fixtures."""
import re
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from calendar_delete_capacity_031 import validate
from survey_pet_quick_reflow_024 import replace_for_analysis

OUT='analysis/pending_insertion_500_031_calendar_models_v1/result.json'


def main():
    path=ROOT/'analysis/full_scope_v1/source_tpl/65F11C.tpl';text=path.read_text(encoding='utf-8-sig');src='@archive 65F11C\n@size 255\n'+re.search(r'^script 50 mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)[0];fixtures=[]
    def case(name,a,b,ok):
        try:validate(a,b,[50],{'65F11C:50:5'},99);actual=True
        except ValueError:actual=False
        if actual!=ok:raise ValueError('031 calendar fixture '+name)
        fixtures.append(dict(name=name,accepted=actual))
    case('bounded-source-calendar50',src,src,True)
    changes=[('unknown-root',src.replace('65F11C','ABCDEF')),('unknown-window',src.replace('\tmsgOpenQuick\n','\tmsgOpen\n')),('shifted-topology',src.replace('\ttextSpeed','\tsoundDisableChoiceSFX\n\ttextSpeed')),('first-page-overflow',src.replace('を さくじょしちゃうよ','가'*20)),('missing-choice-row',src.replace('だいじょうぶ?\\n\\n','だいじょうぶ?\\n')),('oversize-choice-label',src.replace('はい  ','가'*10)),('wrong-choice-width',src.replace('width = 8','width = 9')),('wrong-pad',src.replace('count = 1','count = 2')),('wrong-default',src.replace('default = 0','default = 1')),('wrong-clear',src.replace('clear = true','clear = false')),('wrong-navigation',src.replace('left = 1','left = 0')),('unbounded-frequency',src.replace('callBufferEventFrequency','callBufferEventYear')),('wrong-string-flags',src.replace('printN = false','printN = true')),('missing-close',src.replace('\tmsgCloseQuick\n',''))]
    for name,b in changes:case(name,b,b,False)
    case('protected-source-control-changed',src,src.replace('mugshot = Roll','mugshot = Rockman'),False)
    survey_path='analysis/pending_insertion_500_031_calendar_layout_v2/survey.json';s=read(survey_path);count=groups=0
    for g in s['candidate_groups']:
        if g['profile']!='calendar-delete-quick':continue
        ref=g['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);original=(ROOT/ref['path']).read_text(encoding='utf-8-sig');units=[]
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);u=deepcopy(next(u for u in read(link['path'])['units'] if u['id']==link['id']));u['translation']=g['explicit_layouts'].get(u['id'],u['translation']);units.append(u)
        if validate(original,replace_for_analysis(original,units),[50],set(g['ids']),s['native_nickname_bound'])!=g['geometry']:raise ValueError('031 calendar current geometry not reproduced')
        count+=len(units);groups+=1
    deps=[survey_path,'tools/test_calendar_delete_capacity_031.py','tools/calendar_delete_capacity_031.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,fixtures=fixtures,current_conditional_candidate_units=count,current_conditional_scripts=groups,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},product_admitted=False,rom_written=False,release_eligible=False,limits=['Model topology/geometry and current76 only; native source guards/current title scope/final031 Korean GBA remain separate.']))
    print('031 calendar model PASS',len(fixtures),'fixtures',count,'conditional units',groups,'scripts',flush=True)


if __name__=='__main__':main()
