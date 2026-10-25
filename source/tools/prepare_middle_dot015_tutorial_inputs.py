"""Complete four-page legacy script; two manual alternatives, no game mutation."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
PROPOSALS='translations/pending_insertion_015_tutorial_wording_proposals.json'
PARENT='translations/batch500_046_remaining_768800_draft_ko.json'
PARENT_SHA='c790b97eb2b1f68b512a5ac3e5867eea2a066d0ed1ff28ba98502a2fb1e412f3'
OUT='translations/batch500_000_insertion015_768800_draft_ko.json'
def prepare():
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256']);require_hash(ROOT/PARENT,PARENT_SHA)
    a=read(PARENT);p=read(PROPOSALS)
    if set(p)!={'schema','policy','review','approved','proposals'} or p['schema']!=1 or p['policy']!='development-draft; NON-DISTRIBUTION' or p['review']!='needs_review' or p['approved'] is not False:raise ValueError('Proposal policy')
    ids=['768800:2:0','768800:2:2']
    if [r['unit_id'] for r in p['proposals']]!=ids or len({r['id'] for r in p['proposals']})!=2:raise ValueError('Proposal identities')
    proposals={r['unit_id']:r for r in p['proposals']}
    for r in p['proposals']:
        if set(r)!={'id','unit_id','translation','rationale'} or not all(isinstance(v,str) and v for v in r.values()):raise ValueError('Proposal schema')
    if a['archive']!='768800' or a['source_sha256']!=cfg['source_profile']['sha256'] or a['review']['release_eligible'] is not False:raise ValueError('Draft identity/policy')
    require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256'])
    b=deepcopy(a);b['units']=[deepcopy(u) for u in a['units'] if u['id'].startswith('768800:2:')]
    if [u['id'] for u in b['units']]!=['768800:2:'+str(i) for i in range(4)]:raise ValueError('Whole-script identities')
    links=[]
    for u in b['units']:
        if u['state']!='needs_review':raise ValueError('Review state')
        if u['id'] in proposals:
            r=proposals[u['id']]
            if r['translation'].count('\n')!=u['source'].count('\n'):raise ValueError('Protected line topology')
            links.append(dict(unit_id=u['id'],selected_wording_id=r['id'],parent=dict(path=PARENT,sha256=PARENT_SHA,unit_id=u['id']),approved=False))
            u['translation']=r['translation']
    b.update(consumer='normal-dialogue',insertion_state='Source-only legacy tutorial development input; NO ROM integration or gameplay support proof',manual_wording_proposals=dict(path=PROPOSALS,sha256=sha((ROOT/PROPOSALS).read_bytes()),links=links))
    frozen_write(ROOT/OUT,b);return [OUT]
if __name__=='__main__':print(prepare())
