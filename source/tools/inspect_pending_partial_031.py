"""Exact030 mixed-script census. No translation, consumer admission or ROM writes."""
import re
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from field_hint_capacity import events
from tpl_literals import literals

BASE='poc/output/pending500_030_v1.gba'
SURVEY='analysis/pending_insertion_500_031_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_031_partial_v1/census.json'

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256'])
    m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256'])
    proof=read('analysis/pending500_030_v1/integration.json');survey=read(SURVEY)
    if not proof['passed'] or proof['rom_sha256']!=m['output_sha256'] or survey['baseline_sha256']!=m['output_sha256'] or survey['pinned_changed_inputs']:raise ValueError('031 exact baseline')
    applied={u['id'] for r in layout_records(m) for u in r['layout']}
    coverage=read(survey['pinned_coverage']['path']);require_hash(ROOT/survey['pinned_coverage']['path'],survey['pinned_coverage']['sha256'])
    pool=defaultdict(list);sources={}
    for p,h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/p,h);a=read(p);sources[a['archive']]=a['source_tpl']
        for u in a['units']:pool[u['id']].append((p,h,u))
    records=[];classes=Counter();fully=0;cache={}
    for g in survey['unresolved_groups']:
        if 'script_has_applied_ids' not in g['reasons']:continue
        new=set(g['ids'])-applied;old=set(g['ids'])&applied
        if not new:fully+=1;continue
        arc=g['archive'];ref=sources[arc];require_hash(ROOT/ref['path'],ref['sha256'])
        if arc not in cache:cache[arc]=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
        section=re.search(r'^script '+str(g['script'])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',cache[arc],re.M)
        if not section:raise ValueError('031 mixed language or identity')
        tpl='@archive '+arc+'\n'+section[0];commands=[e[2][0] for e in events(tpl) if e[1]=='command'];missing=[];refs=[]
        for key in sorted(new):
            choices=pool[key]
            if not choices or len({(u['source'],u['translation'],u['state']) for _,_,u in choices})!=1:missing.append(key);continue
            p,h,u=choices[0];refs.append(dict(id=key,path=p,sha256=h))
        family='PET' if 'positionBox' in commands else 'menu-quick' if 'msgOpenQuick' in commands else 'normal' if 'msgOpen' in commands else 'inherited-or-other'
        classes[family]+=len(new)
        records.append(dict(archive=arc,script=g['script'],new_ids=sorted(new),old_ids=sorted(old),new_units=len(new),class_hint=family,commands=commands,source_tpl=ref,drafts=refs,missing_or_conflicting=missing,reasons=g['reasons'],product_admitted=False))
    frozen_write(ROOT/OUT,dict(schema=1,status='MIXED_SCRIPT_POPULATION_ONLY_NOT_ADMISSION',baseline_rom=BASE,baseline_sha256=m['output_sha256'],source_sha256=cfg['source_profile']['sha256'],new_units=sum(r['new_units'] for r in records),mixed_scripts=len(records),fully_applied_scripts=fully,classes=dict(classes),groups=records,dependencies={p:sha((ROOT/p).read_bytes()) for p in (SURVEY,'analysis/pending500_030_v1/integration.json','tools/inspect_pending_partial_031.py')},rom_written=False,release_eligible=False,limits='New Japanese literal IDs sharing scripts with applied Japanese literal IDs only. Consumers, aggregate geometry, non-Japanese literal companions and old/new mixed-byte equivalence are not admitted. No scope relaxation or prose change.'))
    print('031 mixed-script new units',sum(r['new_units'] for r in records),'scripts',len(records),'classes',dict(classes),'fullyapplied',fully)

if __name__=='__main__':main()
