"""Preserve failed exact500 selection denominator without relaxing its gates."""
import traceback
from collections import Counter
import prepare_source500_038_v1 as prepare
from build_visibility_poc import ROOT
from cumulative_batch500 import frozen_write

try:prepare.select()
except ValueError as error:
    tb=error.__traceback__
    while tb and tb.tb_frame.f_code.co_name!='select':tb=tb.tb_next
    if tb is None:raise
    v=tb.tb_frame.f_locals;good=v.get('good',[]);bad=v.get('bad',[])
    result=dict(passed=False,reason=str(error),candidate_units=sum(g['units'] for g in good),candidate_groups=good,rejections=bad,maximum_reachable=max(v.get('dp',{0:[]})),rom_written=False,new_units_applied=0,release_eligible=False)
    frozen_write(ROOT/prepare.OUT/'selection_attempt_v1.json',result)
    print('PRESERVED038 failed exact500:',result['candidate_units'],'candidate units',len(good),'groups; max',result['maximum_reachable'])
    print('REASONS',Counter(x for g in bad for x in g['reasons']).most_common(18))
