"""Freeze205 conditional event candidates for source-only roundtrip checks."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records

SURVEY='analysis/pending_insertion_500_031_event_layout_v1/survey.json'
OUT='analysis/pending_insertion_500_031_event_selection_v1/selection.json'


def main():
    s=read(SURVEY);m=read('poc/output/pending500_030_v1.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if s['baseline_sha256']!=m['output_sha256']:raise ValueError('031 exact event baseline')
    applied={u['id'] for r in layout_records(m) for u in r['layout']};seen=set();groups=deepcopy([g for g in s['candidate_groups'] if g['profile']=='event-pages'])
    for g in groups:
        if set(g['ids'])&(seen|applied) or g['storage']!='raw-known-pointer' or g['product_admitted']:raise ValueError('031 source-only distinct event population')
        seen.update(g['ids'])
        for p in g['drafts']:require_hash(ROOT/p['path'],p['sha256'])
    if len(seen)!=205:raise ValueError('031 event candidate denominator')
    deps=[SURVEY,'tools/prepare_event_candidates_031.py','tools/event_dialogue_capacity_031.py','analysis/pending_insertion_500_031_event_models_v1/result.json','analysis/pending_insertion_500_031_event_title_bounds_v1/cpu.json','analysis/pending_insertion_500_031_event_runtime_v1/verification.json']
    for p in deps[3:]:
        evidence=read(p)
        if not evidence['passed']:raise ValueError('031 event prerequisite')
        for q,h in evidence['dependencies'].items():require_hash(ROOT/q,h)
    frozen_write(ROOT/OUT,dict(schema=1,status='205_CONDITIONAL_EVENT_CANDIDATES_NOT_500_OR_ROM_ADMISSION',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],planned_new_units=205,native_nickname_bound=s['native_nickname_bound'],selected_ids=sorted(seen),groups=groups,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,insertion_ready=False,release_eligible=False,limits='Existing needs_review wording only. Conditional legacy title applicability, time formatter, source guards and maximum GBA route remain separate; no cumulative product construction/admission.'))
    print('031 frozen205 conditional event units',len(groups),'whole scripts; no ROM',flush=True)


if __name__=='__main__':main()
