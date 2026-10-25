"""Analysis-only clear-before-open normal pages; native control effects pending."""
import re
from tpl_literals import skeleton
from normal_timing_capacity_025 import validate as core


def project(text,script):
    h=re.search(r'^@archive \w+',text,re.M)[0]+'\n';m=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
    if not m:raise ValueError('Cleared normal script')
    one=h+m[0];prefix='script '+str(script)+' mmbn45 {\n\tclearMsg\n\tmsgOpen\n'
    if not m[0].startswith(prefix):raise ValueError('Cleared normal exact empty entry boundary')
    return one.replace(prefix,'script '+str(script)+' mmbn45 {\n\tmsgOpen\n',1)


def validate(original,target,scripts,selected_ids):
    if skeleton(original)!=skeleton(target) or len(scripts)!=1:raise ValueError('Cleared normal source controls')
    proof=core(project(original,scripts[0]),project(target,scripts[0]),scripts,selected_ids,99,88)
    for p in proof:p.update(initializer='source clearMsg then msgOpen',entry_clear_preserved=True,entry_clear_native_effects_runtime_pending=True,geometry_projection_only=True,product_admitted=False)
    return proof
