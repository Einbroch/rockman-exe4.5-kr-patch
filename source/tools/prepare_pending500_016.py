"""Source-only compiler gate for the adopted500 scope; no ROM mutation."""
import re
import prepare_pending_batch500_002 as compiler
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from prepare_batch500_016_inputs import prepare,SELECTION
OUT='analysis/pending_insertion_500_016_preflight_v1'
def main():
    p=read(SELECTION);items=prepare();plan=[]
    for r in items:
        a=read(r['path']);tpl=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');scripts={int(s) for s in re.findall(r'^script\s+(\d+)\s',tpl,re.M)}
        plan.append((r['path'],scripts-set(r['scripts']),r['units']))
    compiler.BASE=p['baseline_rom'];compiler.BASE_SHA=p['baseline_sha256'];compiler.PLAN=plan;compiler.LAYOUT='translations/pending_insertion_500_016_layout.json';compiler.LAYOUT_COUNT=0;compiler.EXPECTED_UNITS=500
    compiler.prepare(ROOT/OUT);report=read(OUT+'/preflight.json')
    if report['layout_candidates'] or report['total_units']!=500 or report['applied_id_intersection']:raise ValueError('Source-only gate')
    report.update(batch_id=p['batch_id'],selection=dict(path=SELECTION,sha256=sha((ROOT/SELECTION).read_bytes())))
    # compiler creates this report; finalize its explicit source-only batch link.
    (ROOT/OUT/'preflight.json').write_text(__import__('json').dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS exact500 source-only; ROM not written')
if __name__=='__main__':main()
