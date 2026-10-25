"""Source-retained leading clear before normal msgOpen, finite trader labels."""
import re
from tpl_literals import skeleton
from normal_timing_capacity_025 import validate as core


def validate(original,target,scripts,selected_ids,nickname_bound):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1 or scripts[0] not in (21,23):raise ValueError('034 leading-clear protected finite scope')
    arc=re.search(r'^@archive (\w+)',original,re.M)[1]
    if arc!='6FE8D4':raise ValueError('034 leading-clear trader root')
    pattern=r'^script '+str(scripts[0])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)';projected=[]
    for tpl in (original,target):
        found=re.search(pattern,tpl,re.M)
        if found is None:raise ValueError('034 leading-clear script')
        one='@archive '+arc+'\n'+found[0]
        anchor='\tclearMsg\n\tmsgOpen\n'
        if one.count(anchor)!=1 or not one.startswith('@archive '+arc+'\nscript '+str(scripts[0])+' mmbn45 {\n'+anchor):raise ValueError('034 clear must immediately precede explicit open')
        projected.append(one.replace(anchor,'\tmsgOpen\n',1))
    proof=core(*projected,scripts,selected_ids,nickname_bound,88)
    proof[0].update(source_leading_clear_retained=True,geometry_projection_only=True,conditional_native_origin_required=[52,110],source_trader_caller_clear_and_open_runtime_pending=True)
    return proof
