"""Freeze one exact500 conditional source-only cohort; not ROM admission."""
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records

SURVEY='analysis/pending_insertion_500_031_calendar_layout_v2/survey.json'
OUT='analysis/pending_insertion_500_031_selected500_v1/selection.json'


def main():
    s=read(SURVEY);m=read('poc/output/pending500_030_v1.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if s['baseline_sha256']!=m['output_sha256'] or s['selected500'] is None:raise ValueError('031 exact500 baseline/selection')
    applied={u['id'] for r in layout_records(m) for u in r['layout']};seen=set();groups=deepcopy(s['selected500']);allowed={'event-pages','calendar-delete-quick','pet-extended-native','pet-direct-profile','pet-array-conditional','pet-native-chip-profile'}
    for g in groups:
        if set(g['ids'])&(seen|applied) or g['storage']!='raw-known-pointer' or g['product_admitted'] or g['profile'] not in allowed:raise ValueError('031 exact500 distinct raw conditional scope')
        seen.update(g['ids'])
        for p in g['drafts']:require_hash(ROOT/p['path'],p['sha256'])
    if len(seen)!=500 or sum(g['units'] for g in groups)!=500:raise ValueError('031 exact500 literal denominator')
    evidence=['analysis/pending_insertion_500_031_calendar_models_v1/result.json','analysis/pending_insertion_500_031_calendar_delete_runtime_v1/verification.json','analysis/pending_insertion_500_031_frequency_cpu_v1/cpu.json','analysis/pending_insertion_500_031_event_models_v1/result.json','analysis/pending_insertion_500_031_event_title_bounds_v1/cpu.json','analysis/pending_insertion_500_031_event_time_format_v1/cpu.json','analysis/pending_insertion_500_031_event_native_boundary_v1/verification.json','analysis/pending_insertion_500_031_opponent_chip_runtime_v1/verification.json']
    for p in evidence:
        r=read(p)
        if not r['passed'] or r.get('baseline_sha256',m['output_sha256'])!=m['output_sha256']:raise ValueError('031 exact500 conditional evidence')
        for q,h in r['dependencies'].items():require_hash(ROOT/q,h)
    deps=[SURVEY,'tools/prepare_selected500_031.py','tools/calendar_delete_capacity_031.py','tools/event_dialogue_capacity_031.py']+evidence
    counts=Counter()
    for g in groups:counts[g['profile']]+=g['units']
    frozen_write(ROOT/OUT,dict(schema=1,status='EXACT500_CONDITIONAL_SOURCE_COMPILE_SELECTION_NOT_ROM_ADMISSION',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],planned_new_units=500,native_nickname_bound=s['native_nickname_bound'],selected_ids=sorted(seen),groups=groups,profiles=dict(counts),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,insertion_ready=False,release_eligible=False,limits='Exact500source-only. Existing needs_review wording and explicit same-word layouts, not release/human approval. Cumulative030carry, selected-provider/guard product applicability, primary build gates, whole-ROM/repro and final031 Korean GBA still required.'))
    print('031 frozen EXACT500',len(groups),'scripts',len({g['archive'] for g in groups}),'archives; no ROM',flush=True)


if __name__=='__main__':main()
