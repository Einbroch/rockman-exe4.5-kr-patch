"""List remaining canonical dialogue/label units that fail only on width, with the budget they must meet.

Writes analysis/wording_fit_v1/overflow_list.json: per unit id, source, current translation, kind, and for
dialogue the failing page caps/offsets; for labels the per-line cell budget. No ROM or draft changes.
"""
import json,re,sys
from collections import defaultdict
from build_visibility_poc import ROOT
from cumulative_batch500 import read
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from prepare_repartition500 import layout_records
import generic_page_gate059_v1 as G

BASE='poc/output/pending500_062_v1.gba'


def main():
    c=read('analysis/pending_insertion_500_041_inventory_v1/census.json');m=read(BASE.replace('.gba','.json'))
    applied={u['id'] for r in layout_records(m) for u in r['layout']};t={};d={};out=[]
    from label_cells_v1 import scan
    src=(ROOT/read('project.json')['source_profile']['filename']).read_bytes();cells=scan(src)[0]
    from verify_tpi_index import parse_tpi
    cat={f"{r['offset']:X}":r for r in parse_tpi(ROOT/read('project.json')['text_catalog']['path'])}
    for g in c['groups']:
        if set(g['ids'])&applied or g['storage'] not in ('raw-existing','compressed','raw-new'):continue
        arc=g['archive']
        if arc not in t:t[arc]=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        one,lang=G.script_text(t[arc],g['script']);raw={u.key:u.text for u in literals(one)};vals={}
        for dd in g['drafts']:
            if dd['path'] not in d:d[dd['path']]=read(dd['path'])
            vals[dd['id']]=next(x for x in d[dd['path']]['units'] if x['id']==dd['id'])['translation']
        if lang=='mmbn45':
            v2=G.fit(one,vals);s=G.simulate(one);tt=G.simulate(replace_exact(one,v2));e=G.page_errors(s,tt)
            if not e:continue
            pages=[]
            for i,msg in e.items():
                keys=[(k,r,o) for k,r,o in tt[i]['keys'] if k in vals]
                pages.append(dict(error=msg,caps=s[i]['caps'],standard=s[i]['standard'],inherited=s[i]['inherited'],source_rows=s[i]['rows'],target_rows=tt[i]['rows'],literals=[dict(id=k,row=r,offset=o) for k,r,o in keys]))
            out.append(dict(kind='dialogue',archive=arc,script=g['script'],ids=g['ids'],units={k:dict(source=raw[k],translation=vals[k]) for k in vals},pages=pages,script_text=re.sub(r'\n\t\t[^\n]+','',one)[:1200]))
        else:
            row=cat[arc];roots=[0x08000000+row['offset']] if not row['compressed'] else []
            calls=[x for r in roots for x in cells.get(r,[])]
            budget=min([x[1] for x in calls if x[3]==g['script']] or [x[1] for x in calls] or [0])
            bad={k:v for k,v in vals.items() if len(v.split('\n'))!=len(raw[k].split('\n')) or any(len(a)>max(len(b),budget) for a,b in zip(v.split('\n'),raw[k].split('\n')))}
            if bad:out.append(dict(kind='label',archive=arc,script=g['script'],ids=g['ids'],cell_budget=budget,units={k:dict(source=raw[k],translation=v,line_cells=[max(len(b),budget) for b in raw[k].split('\n')]) for k,v in bad.items()}))
    p=ROOT/'analysis/wording_fit_v1';p.mkdir(parents=True,exist_ok=True);(p/'overflow_list.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
    from collections import Counter
    print(Counter(x['kind'] for x in out),sum(len(x['units']) for x in out),Counter(x['archive'] for x in out).most_common(12))


if __name__=='__main__':main()
