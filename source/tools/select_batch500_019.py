"""Freeze a conditional500 plan, not build admission, from two pinned surveys."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
import select_batch500_017 as selector

INPUTS=['analysis/pending_insertion_500_019_layout_survey_v1/survey.json','analysis/pending_insertion_500_019_variable_survey_v1/invariant_width_survey.json']
COMBINED='analysis/pending_insertion_500_019_selection_v1/combined_survey.json'
SELECTION='analysis/pending_insertion_500_019_selection_v1/selection.json'
LAYOUT='translations/pending_insertion_500_019_layout_v1.json'

def main():
    static,variable=[read(p) for p in INPUTS]
    for report in (static,variable):
        require_hash(ROOT/report['baseline_rom'],report['baseline_sha256'])
        if report['rom_written'] or report['prose_changed'] or report['release_eligible']:raise ValueError('Read-only NON-DISTRIBUTION survey')
    if any(static[k]!=variable[k] for k in ('baseline_rom','baseline_sha256','source_sha256')):raise ValueError('Inconsistent survey baseline')
    for path,digest in variable['native_evidence'].items():require_hash(ROOT/path,digest)
    candidates=deepcopy(static['candidates'])+deepcopy(variable['nickname_template_candidates'])
    ids=[key for group in candidates for key in group['ids']]
    if len(ids)!=len(set(ids)) or len({(g['archive'],g['script']) for g in candidates})!=len(candidates):raise ValueError('Candidate overlap')
    for group in candidates:
        if group['units']!=len(group['ids']) or {r['id'] for r in group['drafts']}!=set(group['ids']):raise ValueError('Whole-script source ID denominator')
        for ref in group['drafts']:require_hash(ROOT/ref['path'],ref['sha256'])
        require_hash(ROOT/group['source_tpl']['path'],group['source_tpl']['sha256'])
    combined=dict(schema=1,baseline_rom=static['baseline_rom'],baseline_sha256=static['baseline_sha256'],source_sha256=static['source_sha256'],parents=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in INPUTS],candidates=candidates,candidate_units=len(ids),rom_written=False,prose_changed=False,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',limits='Conditional planning only. Native aggregate contract not yet adopted by product compiler. Source-only/cumulative preflight, individual source preservation, new suffix runtime and build registration remain required. Not500 inserted units.')
    frozen_write(ROOT/COMBINED,combined)
    selector.SURVEY=COMBINED;selector.OUT=SELECTION;selector.LAYOUT=LAYOUT
    selector.main('pending-insertion-500-019-conditional-plan')
    chosen=read(SELECTION)
    names=[g for item in chosen['selected'] for g in item['groups'] if 'template' in g]
    print('Conditional plan nickname units',sum(g['units'] for g in names),'scripts',len(names),'static units',500-sum(g['units'] for g in names))

if __name__=='__main__':main()
