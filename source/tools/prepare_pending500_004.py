"""Select500 untouched raw, complete-script existing drafts; no prose changes."""
import argparse,json,re
import prepare_repartition500 as selector
import prepare_pending_batch500_002 as compiler
from build_visibility_poc import ROOT,sha,require_hash

BASE='poc/output/exe45_ko_development_pending500_003_v2.gba'
SELECTION='analysis/pending_insertion_500_004_selection_v1'
PREFLIGHT='analysis/pending_insertion_500_004_preflight_v1'
LAYOUT='translations/pending_insertion_500_004_layout.json'
BATCH_ID='pending-insertion-500-004'
EXTRA_EXCLUDE=set()
TARGET=500

def main():
    p=argparse.ArgumentParser();p.add_argument('--reuse-selection',action='store_true');a=p.parse_args()
    meta=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'));require_hash(ROOT/BASE,meta['output_sha256'])
    selector.BASE=BASE;selector.OUT=SELECTION;selector.TARGET=TARGET;selector.TOTAL_UNITS=TARGET
    selector.EXCLUDE={'6E1554','6E1CC0','6E21B0','6A5578'}|EXTRA_EXCLUDE
    if not a.reuse_selection:selector.main()
    sp=ROOT/SELECTION/'selection.json';selection=json.loads(sp.read_text(encoding='utf8'))
    selection.update(batch_id=BATCH_ID,reason=f'{TARGET} previously unapplied raw normal-dialogue units, no prose changes; existing partial archives require cumulative merge.' if selector.ALLOW_PARTIAL else f'{TARGET} previously unapplied raw normal-dialogue units, no prose changes, all compiled consumers excluded.')
    sp.write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    plan=[]
    for r in selection['replacement_archives']:
        d=json.loads((ROOT/r['path']).read_text(encoding='utf8'));tpl=(ROOT/d['source_tpl']['path']).read_text(encoding='utf-8-sig')
        scripts={int(x) for x in re.findall(r'^script\s+(\d+)\s',tpl,re.M)}
        plan.append((r['path'],scripts-set(r['scripts']),r['units']))
    compiler.BASE=BASE;compiler.BASE_SHA=meta['output_sha256'];compiler.PLAN=plan
    compiler.LAYOUT=LAYOUT;compiler.LAYOUT_COUNT=0
    compiler.EXPECTED_UNITS=TARGET
    compiler.prepare(ROOT/PREFLIGHT)
    report=json.loads((ROOT/PREFLIGHT/'preflight.json').read_text(encoding='utf8'))
    if report['layout_candidates']:raise ValueError('Unresolved geometry candidates')
    report.update(batch_id=BATCH_ID,selection=dict(path=str(sp.relative_to(ROOT)),sha256=sha(sp.read_bytes())))
    (ROOT/PREFLIGHT/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':main()
