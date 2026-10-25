"""Freeze130 canonical candidate units for source-only compilation, NOT ROM."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records

SURVEY='analysis/pending_insertion_500_031_layout_v1/survey.json'
OUT='analysis/pending_insertion_500_031_opponent_chip_selection_v1/selection.json'

def main():
    s=read(SURVEY);m=read('poc/output/pending500_030_v1.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if s['baseline_sha256']!=m['output_sha256']:raise ValueError('031 exact baseline')
    cpu=read('analysis/pending_insertion_500_031_opponent_chip_cpu_v1/cpu.json');rt=read('analysis/pending_insertion_500_031_opponent_chip_runtime_v1/verification.json')
    if not cpu['passed'] or cpu['case_count']!=1580 or not rt['passed'] or rt['baseline_sha256']!=s['baseline_sha256']:raise ValueError('031 conditional evidence')
    for p,h in rt['dependencies'].items():require_hash(ROOT/p,h)
    applied={u['id'] for r in layout_records(m) for u in r['layout']};groups=deepcopy([g for g in s['candidate_groups'] if g['profile']=='pet-extended-native']);seen=set()
    for g in groups:
        if set(g['ids'])&(seen|applied) or g['storage']!='raw-known-pointer' or g['product_admitted']:raise ValueError('031 distinct raw candidate population')
        new_kinds={p.get('kind') for geo in g['geometry'] for page in geo['pages'] for p in page['parts']} & {'printMostLostToOpponentsChip','printMostDefeatedOpponentsChip','printPlayerName'}
        if not new_kinds or 'printPlayerName' in new_kinds:raise ValueError('031 only bounded opponent-chip additions')
        seen.update(g['ids'])
        for p in g['drafts']:require_hash(ROOT/p['path'],p['sha256'])
    if len(seen)!=130:raise ValueError('031 source-only candidate denominator')
    paths=[SURVEY,'tools/prepare_opponent_chip_candidates_031.py','tools/pet_extended_native_capacity_031.py','tools/bench_opponent_chips_031.py','analysis/pending_insertion_500_031_opponent_chip_cpu_v1/cpu.json','analysis/pending_insertion_500_031_opponent_chip_runtime_v1/verification.json']
    frozen_write(ROOT/OUT,dict(schema=1,status='130_CANDIDATE_SOURCE_COMPILE_ONLY_NOT_500_OR_ROM_ADMISSION',source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],planned_new_units=130,native_nickname_bound=s['native_nickname_bound'],selected_ids=sorted(seen),groups=groups,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},rom_written=False,insertion_ready=False,release_eligible=False,limits='Canonical existing needs_review prose and explicit same-word LF layouts only. Not500cohort, carry/product integration, all histories/natural multiplayer or131Korean display proof. No player-name model admitted.'))
    print('031 source-only frozen130',len(groups),'scripts',len({g['archive'] for g in groups}),'archives; no ROM written')

if __name__=='__main__':main()
