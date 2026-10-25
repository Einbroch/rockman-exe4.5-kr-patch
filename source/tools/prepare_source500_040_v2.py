"""040 exact500 source-only proposals; no hooks, product adoption or ROM write."""
import re,json
from copy import deepcopy
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from survey_pending040_v1 import BASE,BASE_SHA,OUT as CENSUS
from tpl_literals import literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from survey_calendar_layout500_031_v2 import place
from survey_batch500_017_layout import protected_edges
from battle_bbs_geometry040_v1 import validate as bbs
from profile_quick_geometry039_v1 import validate as communication
from normal_timing_capacity_025 import validate as normal
from archive_scripts import script_spans
from compare_archive_payloads import payload_of
from prepare_repartition500 import layout_records

OUT='analysis/pending_insertion_500_040_source_v2'
COMMS='analysis/pending_insertion_500_039_communication_words_survey_v1/selection.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();m=read(BASE.replace('.gba','.json'));c=read(CENSUS);applied={u['id'] for r in layout_records(m) for u in r['layout']};templates={};drafts={};good=[];bad=[];oldcomm={ (g['archive'],g['script']):g for g in read(COMMS)['candidate_groups'] };owners={}
    for r in layout_records(m):
        if all(k in r for k in ('rom_offset','compiled_bytes','script_count')):owners.setdefault(r['archive'],[]).append(r)
    for g in c['groups']:
        arc=g['archive'];script=g['script'];ids=set(g['ids'])
        if ids&applied or g['already_applied_ids_in_script'] or not g['all_japanese_literals_unapplied'] or g['literal_language']!='mmbn45':continue
        if (arc,script) in oldcomm:kind='communication-help';caps=(132,132,132)
        elif arc in {'7000AC','7011F0','701ED8','7028FC'} and set(g['significant_commands'])=={'color','positionArrow','positionText','waitHold'}:kind='battle-BBS-trial';caps=(168,168,168)
        elif (g['storage']=='raw-existing' or arc=='6E93C8') and not any(x.startswith(('print','callBuffer')) for x in g['commands']):kind='compressed-normal' if arc=='6E93C8' else 'existing-raw-normal';caps=(180,180,168)
        else:continue
        sr=g['source_tpl']
        if arc not in templates:require_hash(ROOT/sr['path'],sr['sha256']);templates[arc]=(ROOT/sr['path']).read_text(encoding='utf-8-sig')
        text=templates[arc];match=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script|\Z)',text,re.M)
        if match is None:raise ValueError('040 source script')
        one='@archive '+arc+'\n'+match[0];raw={u.key:u.text for u in literals(one)};units=[];values={};error=None
        for d in g['drafts']:
            if d['path'] not in drafts:require_hash(ROOT/d['path'],d['sha256']);drafts[d['path']]=read(d['path'])
            a=drafts[d['path']];u=deepcopy(next(x for x in a['units'] if x['id']==d['id']))
            if a['source_sha256']!=sha(source) or a['source_tpl']!=sr or u['source']!=raw[u['id']] or u['state']!='needs_review':raise ValueError('040 canonical authored provenance')
            value=place(u['translation'],caps)
            if value is None or value.replace('\n',' ')!=u['translation'].replace('\n',' ') or not protected_edges(u['source'],value):error='word-only layout exceeds trial/established profile';break
            values[u['id']]=value;units.append(u)
        if error:bad.append(dict(archive=arc,script=script,units=g['units'],source_class=kind,reason=error));continue
        target=replace_exact(one,values)
        try:
            if kind=='communication-help':geometry=communication(one,target,[script],ids)
            elif kind=='battle-BBS-trial':geometry=bbs(one,target,[script],ids)
            else:geometry=normal(one,target,[script],ids,99,88)
        except ValueError as ex:bad.append(dict(archive=arc,script=script,units=g['units'],source_class=kind,reason=str(ex)));continue
        native=payload_of(source,g['source_row']);count=int(re.search(r'^@size (\d+)$',text,re.M)[1]);span=script_spans(native,count)[script]
        if sha(native)!=g['source_archive_sha256'] or payload_of(rom,g['source_row'])!=native:raise ValueError('040 native source storage')
        for owner in owners.get(arc,[]):
            data=rom[owner['rom_offset']:owner['rom_offset']+owner['compiled_bytes']]
            if sha(data)!=owner['compiled_sha256'] or script_spans(data,count)[script]!=span:raise ValueError('040 current owned script differs from original')
        good.append(dict(deepcopy(g),source_class=kind,geometry=json.loads(json.dumps(geometry)),geometry_ids=sorted(ids),explicit_layouts=values,canonical_units=units,script_count=count,current_unselected_script_identity_verified=True,wording_changed=False,product_admitted=False))
    good.sort(key=lambda g:({'communication-help':0,'battle-BBS-trial':1,'existing-raw-normal':2,'compressed-normal':2}[g['source_class']],g['archive'],g['script']))
    dp={0:[]}
    for i,g in enumerate(good):
        for n in sorted(list(dp),reverse=True):
            total=n+g['units']
            if total<=500 and total not in dp:dp[total]=dp[n]+[i]
    chosen=[good[i] for i in dp.get(500,[])];keys=[k for g in chosen for k in g['ids']]
    if chosen and (len(keys)!=500 or len(set(keys))!=500 or set(keys)&applied):raise ValueError('040 exact500 unique source proposals')
    deps=[CENSUS,COMMS,'tools/prepare_source500_040_v2.py','tools/battle_bbs_geometry040_v1.py','tools/normal_timing_capacity_025.py','tools/profile_quick_geometry039_v1.py','tools/survey_calendar_layout500_031_v2.py']
    frozen_write(ROOT/OUT/'selection.json',dict(status='040_SOURCE_ONLY_LAYOUT_PROPOSALS_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),current_ROM_units=20622,canonical_pending_IDs=9924,candidate_units=sum(g['units'] for g in good),candidate_classes=dict(Counter({k:sum(g['units'] for g in good if g['source_class']==k) for k in {g['source_class'] for g in good}})),selected_units=len(keys),selected_ids=sorted(keys),groups=chosen,candidate_groups=good,rejections=bad,wording_changed=False,Hangul_syllable_breaks=0,rom_written=False,new_units_applied=0,product_admitted=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Battle BBS168px rows are conservative trial layout only, NOT established consumer capacity. Actual compressed loader/reader/RAM/initializer/renderer path must be established before integration.','Existing raw normal candidates still require complete authored carry/current owner and unchanged unselected scripts verification.','Communication candidates need full039 authored carry where already owned; do not replace existing500 translations with native source.','No040 product build or distribution package.']))
    print('040 eligible proposal units',sum(g['units'] for g in good),'selected',len(keys));print('classes',Counter({k:sum(g['units'] for g in good if g['source_class']==k) for k in {g['source_class'] for g in good}}));print('selected',Counter({k:sum(g['units'] for g in chosen if g['source_class']==k) for k in {g['source_class'] for g in chosen}}))


if __name__=='__main__':main()
