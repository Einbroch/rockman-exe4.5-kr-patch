"""Source-bound ten-unit input with five explicitly authored wording proposals.

No rule-based prose shortening: each proposed expression is an authored input.
Original drafts, source/control structure and review state remain unchanged.
"""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
PROPOSALS='translations/pending_insertion_014_wording_proposals.json'
PLAN=[('7B3C30','translations/batch500_046_remaining_7B3C30_draft_ko.json','d9aa0f45b0e91b9f4a12fd97adfaef123ab8f15a511522e2ef087d68f3f64f21',[0]),('7B4184','translations/batch500_046_remaining_7B4184_draft_ko.json','623f3758619bf9915b18f68be4fe5ab3c70a8ac344169e07e19e38e23e919db5',[1,2,3]),('7BDC90','translations/stereo_program_draft_ko.json','a852477bebddb1561183e2fad9fa9a34265a90e7b1b9ae7640c131765e14ae97',[0])]
def prepare():
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=read(PROPOSALS)
    if set(p)!={'schema','policy','review','approved','proposals'} or p['schema']!=1 or p['policy']!='development-draft; NON-DISTRIBUTION' or p['review']!='needs_review' or p['approved'] is not False:raise ValueError('Development proposal policy')
    proposals={r['unit_id']:r for r in p['proposals']}
    if len(proposals)!=5 or len({r['id'] for r in p['proposals']})!=5:raise ValueError('Explicit five wording identities')
    for r in p['proposals']:
        if set(r)!={'id','unit_id','translation','rationale'} or not all(isinstance(v,str) and v for v in r.values()):raise ValueError('Proposal schema')
    found=set();out=[];total=0
    for archive,path,digest,scripts in PLAN:
        require_hash(ROOT/path,digest);a=read(path)
        if a['archive']!=archive or a['source_sha256']!=cfg['source_profile']['sha256'] or a['review']['release_eligible'] is not False:raise ValueError('Draft revision/policy')
        require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256'])
        b=deepcopy(a);b['units']=[deepcopy(u) for u in a['units'] if int(u['id'].split(':')[1]) in scripts]
        links=[]
        for u in b['units']:
            if u['state']!='needs_review':raise ValueError('Proposal input review state')
            if u['id'] in proposals:
                r=proposals[u['id']];found.add(u['id'])
                if r['translation'].count('\n')!=u['source'].count('\n'):raise ValueError('Protected line topology')
                links.append(dict(unit_id=u['id'],selected_wording_id=r['id'],parent=dict(path=path,sha256=digest,unit_id=u['id']),approved=False))
                u['translation']=r['translation']
        b.update(consumer='normal-dialogue',insertion_state='Explicit technical development selection; wording and presentation need independent/human review',manual_wording_proposals=dict(path=PROPOSALS,sha256=sha((ROOT/PROPOSALS).read_bytes()),links=links))
        target=f'translations/batch500_000_insertion014_{archive}_draft_ko.json'
        frozen_write(ROOT/target,b);out.append(target);total+=len(b['units'])
    if found!=set(proposals) or total!=10:raise ValueError('Proposal/ten-unit scope binding')
    return out
if __name__=='__main__':print(prepare())
