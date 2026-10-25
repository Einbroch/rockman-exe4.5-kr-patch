"""Historic encoding backlog reconciled only after exact ROM integration passes."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
def main():
    history='analysis/pending_insertion_500_006_selection_v2/selection.json';old=read(history)['deferred_unmapped_literals'];keys={r['id'] for r in old}
    paths=['poc/output/exe45_ko_development_pending500_014_v1.gba','poc/output/exe45_ko_development_pending500_015_v1.gba'];populations=[]
    for path in paths:
        m=read(path.replace('.gba','.json'));require_hash(ROOT/path,m['output_sha256'])
        populations.append((m,{u['id'] for r in layout_records(m) for u in r['layout']}))
    proof=read('analysis/pending500_015_v1/integration.json')
    if not proof['passed'] or proof['new_units']!=6 or proof['rom_sha256']!=populations[1][0]['output_sha256']:raise ValueError('Actual integration authority')
    before,after=[ids for _,ids in populations]
    if len(old)!=19 or len(keys)!=19 or len(keys&before)!=10 or len(keys&after)!=14 or len(after-before)!=6 or before-after:raise ValueError('Historic/new-ID identity')
    records=[dict(r,applied_before=r['id'] in before,applied_after=r['id'] in after,new_this_batch=r['id'] in after-before) for r in old]
    frozen_write(ROOT/'analysis/pending500_015_v1/middle_dot_reconciliation.json',dict(schema=1,history=dict(path=history,sha256=sha((ROOT/history).read_bytes())),integration=dict(path='analysis/pending500_015_v1/integration.json',sha256=sha((ROOT/'analysis/pending500_015_v1/integration.json').read_bytes())),baseline_sha256=populations[0][0]['output_sha256'],rom_sha256=populations[1][0]['output_sha256'],historic_ids=19,prior_applied=10,newly_applied=4,current_applied=14,current_pending=5,records=records,scope='Finite historical encoding deferrals, not whole-game untranslated population or wording approval',release_eligible=False))
    print('Historic19: prior10 + new4 = applied14; pending5. Six actual new IDs total.')
if __name__=='__main__':main()
