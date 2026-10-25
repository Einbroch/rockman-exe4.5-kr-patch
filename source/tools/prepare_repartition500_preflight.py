"""Source-bound compile preflight for revised340+160 batch; preserve original batch plan."""
import json,re
import prepare_pending_batch500_002 as preflight
from build_visibility_poc import ROOT,require_hash,sha

SELECTION='analysis/pending_insertion_500_002_repartition_v1/selection.json'
OUT='analysis/pending_insertion_500_002_repartition_preflight_v1'


def main():
    selection=json.loads((ROOT/SELECTION).read_text(encoding='utf8'))
    if selection['total_new_units']!=500 or selection['replacement_units']!=160 or selection['release_eligible'] is not False:
        raise ValueError('Repartition count/policy')
    plan=list(preflight.PLAN[:3])
    for r in selection['replacement_archives']:
        require_hash(ROOT/r['path'],r['sha256'])
        d=json.loads((ROOT/r['path']).read_text(encoding='utf8'))
        tpl=(ROOT/d['source_tpl']['path']).read_text(encoding='utf-8-sig')
        all_scripts={int(m.group(1)) for m in re.finditer(r'^script\s+(\d+)\s',tpl,re.M)}
        plan.append((r['path'],all_scripts-set(r['scripts']),r['units']))
    preflight.PLAN=plan
    preflight.prepare(ROOT/OUT)
    report=json.loads((ROOT/OUT/'preflight.json').read_text(encoding='utf8'))
    if report['layout_candidates']:raise ValueError('Repartition still has geometry candidates')
    report['repartition']=dict(path=SELECTION,sha256=sha((ROOT/SELECTION).read_bytes()),deferred_units=160)
    (ROOT/OUT/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


if __name__=='__main__':main()
