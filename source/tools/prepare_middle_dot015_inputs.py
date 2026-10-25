"""Two explicitly authored proposals; immutable source and draft provenance."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
PROPOSALS='translations/pending_insertion_015_wording_proposals.json'
PARENT='translations/final_047_remaining_7C9C44_draft_ko.json'
PARENT_SHA='e72f1c1740ce7722137cf02e2eacae294185c62bbf0223e9dc48af70d23b9e75'
OUT='translations/batch500_000_insertion015_7C9C44_draft_ko.json'
def prepare():
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    require_hash(ROOT/PARENT,PARENT_SHA);a=read(PARENT);p=read(PROPOSALS)
    if set(p)!={'schema','policy','review','approved','proposals'} or p['schema']!=1 or p['policy']!='development-draft; NON-DISTRIBUTION' or p['review']!='needs_review' or p['approved'] is not False:raise ValueError('Proposal policy')
    expected=['7C9C44:0:0','7C9C44:0:1']
    if [r['unit_id'] for r in p['proposals']]!=expected or len({r['id'] for r in p['proposals']})!=2:raise ValueError('Two proposal identities')
    for r in p['proposals']:
        if set(r)!={'id','unit_id','translation','rationale'} or not all(isinstance(v,str) and v for v in r.values()):raise ValueError('Proposal schema')
    if a['archive']!='7C9C44' or a['source_sha256']!=cfg['source_profile']['sha256'] or a['review']['release_eligible'] is not False:raise ValueError('Draft identity/policy')
    require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256'])
    b=deepcopy(a);b['units']=[deepcopy(u) for u in a['units'] if u['id'] in expected]
    if [u['id'] for u in b['units']]!=expected:raise ValueError('Source identity')
    links=[]
    for u,r in zip(b['units'],p['proposals']):
        if u['state']!='needs_review' or r['translation'].count('\n')!=u['source'].count('\n'):raise ValueError('Review/line topology')
        links.append(dict(unit_id=u['id'],selected_wording_id=r['id'],parent=dict(path=PARENT,sha256=PARENT_SHA,unit_id=u['id']),approved=False))
        u['translation']=r['translation']
    b.update(consumer='normal-dialogue',insertion_state='Source-only development input; NO ROM integration or runtime proof',manual_wording_proposals=dict(path=PROPOSALS,sha256=sha((ROOT/PROPOSALS).read_bytes()),links=links))
    frozen_write(ROOT/OUT,b);return [OUT]
if __name__=='__main__':print(prepare())
