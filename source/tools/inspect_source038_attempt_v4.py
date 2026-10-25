"""Keep the expanded NPC/board source-only selection failure auditable."""
from collections import Counter
import prepare_source500_038_v4 as prepare
from build_visibility_poc import ROOT
from cumulative_batch500 import frozen_write

try:prepare.select()
except ValueError as error:
    tb=error.__traceback__
    while tb and tb.tb_frame.f_code.co_name!='select':tb=tb.tb_next
    if tb is None:raise
    v=tb.tb_frame.f_locals;good=v.get('good',[])
    r=dict(passed=False,reason=str(error),candidate_units=sum(g['units'] for g in good),candidate_groups=good,rejections=v.get('bad',[]),maximum_reachable=max(v.get('dp',{0:[]})),rom_written=False,new_units_applied=0,release_eligible=False)
    frozen_write(ROOT/prepare.OUT/'selection_attempt_v4.json',r)
    print('PRESERVED038 expanded attempt',r['candidate_units'],len(good),'max',r['maximum_reachable'])
    print(Counter(x for g in r['rejections'] for x in g['reasons']).most_common(12))
