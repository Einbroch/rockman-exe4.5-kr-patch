"""Explicit additional common weapon scope; carry original UI drafts unchanged."""
from copy import deepcopy
from equipment_labels import SCOPE as LABEL_SCOPE
from tpl_literals import resolve_units

SCRIPTS=list(range(5,38))
SCOPE=deepcopy(LABEL_SCOPE)
SCOPE['literal_scripts']=list(range(1,38))
SCOPE['literal_profiles'].append({'scripts':SCRIPTS,'consumer':'fixed-cell-big','literal_language':'mmbn45s','max_literal_rows':1,'max_line_advance':72})

def merge(base,additional):
    for key in ['schema','policy','source_sha256','archive','source_archive_sha256','consumer']:
        if base[key]!=additional[key]:raise ValueError('weapon translation source contract')
    if additional['review']['release_eligible'] is not False:raise ValueError('weapon drafts cannot be release eligible')
    units=resolve_units(additional)
    if {u['id'] for u in units}!={f'6E2B9C:{s}:0' for s in SCRIPTS} or len(units)!=33:raise ValueError('exact additional weapon population')
    if any(u['state']!='needs_review' or '\n' in u['translation'] for u in units):raise ValueError('weapon draft state/rows')
    for s,letters in [(27,'C'),(28,'WB'),(35,'B'),(36,'D')]:
        text=next(u['translation'] for u in units if u['id']==f'6E2B9C:{s}:0')
        if ''.join(c for c in text if c.isascii() and c.isalpha())!=letters:raise ValueError('source weapon abbreviation changed')
    out=deepcopy(base);out['wordings']+=deepcopy(additional['wordings']);out['units']+=deepcopy(additional['units'])
    resolve_units(out)
    return out
