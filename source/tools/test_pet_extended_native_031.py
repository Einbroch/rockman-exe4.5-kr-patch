"""Finite031 geometry acceptance/refusal tests. Not product admission."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from pet_extended_native_capacity_031 import PREFIX,validate
from nickname_capacity import ARGS
from survey_pet_quick_reflow_024 import replace_for_analysis

OUT='analysis/pending_insertion_500_031_models_test_v1/result.json'

def main():
    prefix=''.join('\t'+n+'\n'+a for n,a in PREFIX);records=[]
    def wrap(provider,text='가나'):
        return '@archive ABCDEF\n@size 1\nscript 0 mmbn45 {\n'+prefix+'\t'+provider+'\n'+ARGS+'\t"'+text+'"\n\tkeyWait\n\t\tany = false\n\tend\n}\n'
    def case(name,src,dst,accept):
        try:validate(src,dst,[0],{'ABCDEF:0:0'},99);actual=True
        except ValueError:actual=False
        if actual!=accept:raise ValueError('031 model fixture '+name)
        records.append(dict(fixture=name,accepted=actual))
    for provider in ('printMostLostToOpponentsChip','printMostDefeatedOpponentsChip'):
        s=wrap(provider);case(provider+'-positive',s,s,True)
        for name,dst in [
            ('overflow',wrap(provider,'가나다라바')),
            ('fourrows',wrap(provider,'가\\n나\\n다\\n라')),
            ('unknown-opponent',s.replace(provider,'printMostFrequentOpponent')),
            ('bad-args',s.replace('printN = false','printN = true')),
            ('bad-origin',s.replace('left = 92','left = 91')),
            ('any-wait',s.replace('any = false','any = true')),
            ('unknown-space',s.replace('\tkeyWait','\tspacePx\n\t\tcount = 1\n\tkeyWait')),
            ('missing-end',s.replace('\tend\n','')),
        ]:case(provider+'-'+name,s,dst,False)
        overflow=wrap(provider,'가나다라바');case(provider+'-symmetric-overflow',overflow,overflow,False)
    # The complete fixed candidate set must independently reproduce geometry.
    sel_path='analysis/pending_insertion_500_031_opponent_chip_selection_v1/selection.json';sel=read(sel_path);cache={};actual_count=0
    for g in sel['groups']:
        ref=g['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256'])
        if ref['path'] not in cache:cache[ref['path']]=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
        original=cache[ref['path']];units=[]
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);u=deepcopy(next(u for u in read(link['path'])['units'] if u['id']==link['id']));u['translation']=g['explicit_layouts'].get(u['id'],u['translation']);units.append(u)
        if validate(original,replace_for_analysis(original,units),[g['script']],set(g['ids']),99)!=g['geometry']:raise ValueError('031 candidate geometry not reproduced')
        actual_count+=len(units)
    if actual_count!=130:raise ValueError('031 positive population')
    paths=[sel_path,'tools/test_pet_extended_native_031.py','tools/pet_extended_native_capacity_031.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,tests=len(records),fixtures=records,actual_candidate_units=actual_count,actual_candidate_scripts=len(sel['groups']),dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},product_admitted=False,rom_written=False,release_eligible=False,limits='Geometry and source-control tests only, not native caller/record eligibility, carry or ROM application. PlayerName remains outside this130candidate selection.'))
    print('PASS031 geometry',len(records),'fixtures and actual130/46scripts; no ROM written')

if __name__=='__main__':main()
