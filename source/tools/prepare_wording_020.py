"""Materialize individual020 proposals with pinned source and whole-script guards."""
import re
from copy import deepcopy
from collections import defaultdict
from dataclasses import replace
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from tpl_literals import literals,replace_literals,skeleton
from nickname_capacity import validate_templates,CPU
from survey_batch500_020_variables import applicability
from survey_batch500_019_variables import inspect_template
from survey_batch500_017_layout import advance,protected_edges

DECISIONS='translations/pending_insertion_500_020_wording_v1.json'
OUT='analysis/pending_insertion_500_020_wording_v1'

def main():
    d=read(DECISIONS);s=read('analysis/pending_insertion_500_020_survey_v1/survey.json');v=read('analysis/pending_insertion_500_020_variable_survey_v1/survey.json');cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,s['source_sha256']);source=sp.read_bytes();rp=ROOT/s['baseline_rom'];require_hash(rp,s['baseline_sha256']);meta=read(rp.with_suffix('.json'));bound=applicability(source,rp.read_bytes(),read(CPU))
    if d['human_approved'] or d['rom_applied'] or v['baseline_sha256']!=s['baseline_sha256']:raise ValueError('Development wording scope')
    changes={x['id']:x for x in d['decisions']}
    if len(changes)!=len(d['decisions']) or len(changes)!=20:raise ValueError('Explicit20 decision denominator')
    applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    if set(changes)&applied:raise ValueError('Already applied wording')
    coverage=read(s['pinned_coverage']['path']);require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256']);pool=defaultdict(list)
    for p,h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/p,h)
        for u in read(p)['units']:pool[u['id']].append((p,h,u))
    groups=[g for g in s['unresolved_groups'] if set(g['ids'])&set(changes)]
    if len(groups)!=20 or {k for g in groups for k in g['ids'] if k in changes}!=set(changes):raise ValueError('Whole-script source scope')
    archive_units=defaultdict(list);parents={};profiles=defaultdict(list);reports=[]
    for g in groups:
        refs=[];units=[]
        for key in g['ids']:
            options=pool[key]
            if len({(x['source'],x['translation'],x['state']) for _,_,x in options})!=1:raise ValueError('Conflicting draft '+key)
            path,h,old=options[0];u=deepcopy(old);parent=read(path);refs.append(dict(id=key,path=path,sha256=h))
            if key in changes:
                change=changes[key]
                if u['translation']!=change['before'] or not change['reason']:raise ValueError('Wording decision parent '+key)
                u['translation']=change['translation'];u['state']='needs_review'
            if not protected_edges(u['source'],u['translation']) or any(advance(line)>132 for line in u['translation'].split('\n')) or u['translation'].count('\n')>2:raise ValueError('Protected source/geometry '+key)
            units.append(u)
        ref=parent['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);tpl=(ROOT/ref['path']).read_text(encoding='utf-8-sig');native={i.key:i.text for i in literals(tpl)}
        if any(native[u['id']]!=u['source'] for u in units):raise ValueError('Native source identity')
        section=re.search(r'^script '+str(g['script'])+r'\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M).group();items=literals('@archive '+g['archive']+'\n'+section);header=len('@archive '+g['archive']+'\n')
        model,reason=inspect_template(section,[replace(i,start=i.start-header,end=i.end-header) for i in items],{u['id']:u for u in units},bound,True)
        if reason:raise ValueError('Template '+str(g['script'])+' '+reason)
        profile=dict(script=g['script'],suffix_id=model['suffix_id'],source_first_line=model['source_first_line'],first_line=model['first_line']);target=replace_literals(tpl,units)
        if skeleton(target)!=skeleton(tpl):raise ValueError('Control skeleton changed')
        proof=validate_templates(tpl,target,[profile],bound,{u['id'] for u in units})
        reports.append(dict(archive=g['archive'],script=g['script'],selected_ids=g['ids'],drafts=refs,capacity=proof,wording_changes=[k for k in g['ids'] if k in changes]))
        archive_units[g['archive']]+=units;parents[g['archive']]=parent;profiles[g['archive']].append(profile)
    out=ROOT/OUT
    if out.exists():raise ValueError('Preserve wording attempt')
    records=[]
    for arc,units in archive_units.items():
        asset=deepcopy(parents[arc]);asset['units']=units;asset['batch_id']='pending020-individual-wording-proposals';asset['review']=dict(state='needs_review',release_eligible=False,policy='development-draft; NON-DISTRIBUTION');asset['wording_decisions']=dict(path=DECISIONS,sha256=sha((ROOT/DECISIONS).read_bytes()));path=out/(arc+'_selected_asset.json');frozen_write(path,asset)
        records.append(dict(archive=arc,path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()),selected_ids=[u['id'] for u in units],scripts=[p['script'] for p in profiles[arc]],nickname_capacity_profiles=profiles[arc]))
    frozen_write(out/'report.json',dict(schema=1,baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],decisions=dict(path=DECISIONS,sha256=sha((ROOT/DECISIONS).read_bytes())),individual_wording_changes=len(changes),selected_script_units=sum(len(x) for x in archive_units.values()),scripts=reports,assets=records,protected_controls_unchanged=True,conditional_native_bound=bound,consumer_admission=False,compiler_preflight=False,rom_written=False,release_eligible=False,limits='Individual development proposals, not a500 batch. Pinned source/whole-script geometry/explicit native capacity templates only. Binary compile/carry/product/runtime/independent human review pending.'))
    print('PASS individual20 corrections;',len(groups),'scripts;',sum(len(x) for x in archive_units.values()),'whole-script units; no ROM write')

if __name__=='__main__':main()
