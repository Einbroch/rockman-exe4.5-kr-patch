"""Reconcile the finite historic encoding backlog, not total game coverage."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
def main():
    history='analysis/pending_insertion_500_006_selection_v2/selection.json'
    old=read(history)['deferred_unmapped_literals']
    paths=['poc/output/exe45_ko_development_pending500_013.gba','poc/output/exe45_ko_development_pending500_014.gba']
    paths=[p.replace('.gba','_v1.gba') for p in paths]
    populations=[]
    for path in paths:
        m=read(path.replace('.gba','.json'));require_hash(ROOT/path,m['output_sha256'])
        ids={u['id'] for r in layout_records(m) for u in r['layout']}
        populations.append((m,ids))
    before,after=[ids for _,ids in populations]
    keys={r['id'] for r in old}
    if len(old)!=19 or len(keys)!=19 or len(keys&before)!=3 or len(keys&after)!=10:raise ValueError('Finite backlog identity')
    records=[dict(r,applied_before=r['id'] in before,applied_after=r['id'] in after,new_this_batch=r['id'] in after-before) for r in old]
    frozen_write(ROOT/'analysis/pending500_014_v1/middle_dot_reconciliation.json',dict(schema=1,history=dict(path=history,sha256=sha((ROOT/history).read_bytes())),baseline_sha256=populations[0][0]['output_sha256'],rom_sha256=populations[1][0]['output_sha256'],historic_ids=19,prior_applied=3,newly_applied=7,current_applied=10,current_pending=9,records=records,scope='Finite historic encoding deferrals, NOT total game untranslated population; source-ID integration does not approve wording',release_eligible=False))
    print('Historic19: prior3 + new7 = applied10; pending9. Not whole-game coverage.')
if __name__=='__main__':main()
