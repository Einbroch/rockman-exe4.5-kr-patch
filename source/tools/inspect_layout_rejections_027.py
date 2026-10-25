"""Read-only census of same-wording layout failures, not ROM admission."""
from collections import Counter
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from nickname_capacity import advance

def main():
    survey=read('analysis/pending_insertion_500_027_layout_v1/survey.json');coverage=read('analysis/translation_first_v1/coverage.json');pool={}
    for path,h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/path,h)
        for u in read(path)['units']:pool[u['id']]=u
    counts=Counter();examples=[]
    for g in survey['rejections']:
        if g['reason']!='protected_same_wording_placement':continue
        problems=[]
        for key in g['ids']:
            t=pool[key]['translation'];flat=t.replace('\n',' ');rows=t.split('\n')
            reasons=[]
            if t!=t.strip():reasons.append('protected-edges')
            if len(rows)>3:reasons.append('draft-more-than3rows')
            if advance(flat)>396:reasons.append('more-than3x132')
            if advance(flat)>528:reasons.append('more-than180+180+168')
            if max(map(advance,flat.split(' ')))>132:reasons.append('word-wider-than132')
            if reasons:problems.append(dict(id=key,translation=t,reasons=reasons,flat_advance=advance(flat)))
        for r in {r for p in problems for r in p['reasons']}:counts[r]+=1
        examples.append(dict(archive=g['archive'],script=g['script'],units=len(g['ids']),problems=problems))
    print('Rejected groups',len(examples),dict(counts))
    for e in examples[:20]:print(e)

if __name__=='__main__':main()
