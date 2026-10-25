"""Retain typed lookup attempt failure and its exact candidate population."""
from collections import Counter
import prepare_source500_038_v3 as prepare
from build_visibility_poc import ROOT
from cumulative_batch500 import frozen_write

try:prepare.select()
except ValueError as error:
    tb=error.__traceback__
    while tb and tb.tb_frame.f_code.co_name!='select':tb=tb.tb_next
    if tb is None:raise
    v=tb.tb_frame.f_locals;candidates=v.get('candidates',[])
    result=dict(passed=False,reason=str(error),candidate_units=sum(g['units'] for g in candidates),candidate_groups=candidates,maximum_reachable=max(v.get('dp',{0:[]})),rom_written=False,new_units_applied=0,release_eligible=False)
    frozen_write(ROOT/prepare.OUT/'selection_attempt_v3.json',result)
    print('PRESERVED038 typed attempt',result['candidate_units'],len(candidates),'max',result['maximum_reachable'])
    print('CLASSES',Counter({k:sum(g['units'] for g in candidates if g['source_class']==k) for k in {g['source_class'] for g in candidates}}))
