"""Wording fits for units that exceed their window/cells: rule-based shortenings plus manual overrides.

Rules touch only literals inside failing pages (dialogue) or failing labels, and only shorten a fixed
connective after a variable print, or apply a manual rewrite from MANUAL. Every change is written to
translations/wording_fit_v1_ko.json with source, before, after and reason; prepare() applies an entry only
when the draft's current translation equals 'before'.
"""
import json,re,sys
from build_visibility_poc import ROOT
from cumulative_batch500 import read
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
import generic_page_gate059_v1 as G

RULES=[  # (prefix, replacement) applied to the START of a literal that follows a variable print
    ('말입니다,','말이죠,'),('말이에요,','말이죠,'),('말이다만,','말인데,'),('말이더군요','말이오'),
    (' 말이야,',' 말야,'),(' 말이야','\n'),('말이야,','말야,'),('말이죠,','말야,'),
]
MANUAL={}   # id -> new text (filled below from manual_fits)
OUT='translations/wording_fit_v1_ko.json'


def load_manual():
    p=ROOT/'translations/wording_fit_v1_manual.json'
    return json.loads(p.read_text(encoding='utf8')) if p.exists() else {}


def main():
    L=read('analysis/wording_fit_v1/overflow_list.json');manual=load_manual();fixes=[];left=[]
    for x in L:
        if x['kind']!='dialogue':continue
        tpl=(ROOT/f"analysis/full_scope_v1/source_tpl/{x['archive']}.tpl").read_text(encoding='utf-8-sig');one,_=G.script_text(tpl,x['script'])
        vals={k:u['translation'] for k,u in x['units'].items()};orig=dict(vals);vals=G.fit(one,vals)
        def errs(v):
            s=G.simulate(one);t=G.simulate(replace_exact(one,v));return G.page_errors(s,t) if len(s)==len(t) else {'struct':1}
        for k in list(vals):
            if k in manual:vals[k]=manual[k]
        e=errs(vals)
        for _ in range(3):
            if not e:break
            t=G.simulate(replace_exact(one,vals))
            for i in e:
                if i=='struct':continue
                for k,row,off in t[i]['keys']:
                    if k not in vals or k in manual or off<40:continue
                    for a,b in RULES:
                        if vals[k].startswith(a):
                            trial=dict(vals,**{k:b+vals[k][len(a):]});te=errs(trial)
                            if len(te)<len(e) or i not in te:vals=trial;e=te;break
            vals=G.fit(one,vals);e=errs(vals)
        if e:
            r=G.split_fit(one,vals)
            if r is not None:
                try:G.check_split(one,*r);e={}
                except ValueError:pass
        changed={k:v for k,v in vals.items() if v.replace('\n',' ')!=orig[k].replace('\n',' ')}
        for k,v in changed.items():fixes.append(dict(id=k,source=x['units'][k]['source'],before=orig[k],after=v,reason='manual' if k in manual else 'connective after variable print shortened'))
        if e:left.append(dict(group=f"{x['archive']}:{x['script']}",errors=list(map(str,e.values())),units={k:dict(source=x['units'][k]['source'],now=vals[k]) for k in vals}))
    keep=[f for f in (json.loads((ROOT/OUT).read_text(encoding='utf8'))['fixes'] if (ROOT/OUT).exists() else []) if f['reason']=='label cells']
    (ROOT/OUT).write_text(json.dumps(dict(schema=1,policy='development-draft wording fits for window width; NON-DISTRIBUTION',fixes=fixes+keep),ensure_ascii=False,indent=1)+'\n',encoding='utf8')
    (ROOT/'analysis/wording_fit_v1/still_failing.json').write_text(json.dumps(left,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
    print('fixes',len(fixes),'groups still failing',len(left))


if __name__=='__main__':main()
