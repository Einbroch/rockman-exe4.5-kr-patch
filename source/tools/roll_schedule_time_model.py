"""Require unchanged clock insertion and non-growing same-row schedule suffix."""
from tpl_literals import literals,skeleton
def validate(units,scope,original,translated,layout):
    if scope.get('schedule_variable_profile')!='non-growing-clock-suffix-v1':raise ValueError('unknown schedule profile')
    suffix_key=scope.get('schedule_suffix_literal_id','661754:11:2');archive=suffix_key.split(':')[0]
    if suffix_key not in ('661754:11:2','666F38:11:2'):raise ValueError('unregistered clock suffix consumer')
    u=next(u for u in units if u['id']==suffix_key)
    if u['source']!=' から\n' or u['translation'].count('\n')!=1 or not u['translation'].endswith('\n'):raise ValueError('schedule line boundary altered')
    original_width=sum(8 if c==' ' else 11 for c in u['source'].split('\n')[0]);p=next(p for p in layout if p['id']==u['id'])
    if p['line_advance_pixels'][0]>original_width:raise ValueError('dynamic clock suffix grows')
    if skeleton(original)!=skeleton(translated):raise ValueError('clock insertion controls changed')
    before={x.key:x.text for x in literals(original)};after={x.key:x.text for x in literals(translated)}
    for i in [0,1,3,4]:
        k=f'{archive}:11:{i}'
        if before[k]!=after[k]:raise ValueError('protected clock punctuation/event quote changed')
    p.update(source_suffix_width=original_width,non_growing_dynamic_suffix=True,dynamic_clock_population_runtime_complete=False)
