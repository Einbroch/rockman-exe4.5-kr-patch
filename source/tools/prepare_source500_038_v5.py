"""Exact500 existing canonical drafts, source-only, no ROM/product writer."""
from prepare_source500_037_v2 import native_lookup,board_lookup
from prepare_source500_036_v1 import *
from normal_store_tail038_v1 import validate as tail_validate
from survey_aggregate_normal_033 import aggregate
from survey_calendar_layout500_031_v2 import place
from normal_timing_capacity_025 import validate as normal
from normal_battle_choice_capacity_026 import validate as horizontal
from archive_scripts import script_spans
from prepare_source500_038_v3 import typed_lookup
from normal_navi_tail038_v1 import validate as navi_tail
from field_hint_capacity import validate as hint_validate

BASE='poc/output/pending500_037_v2.gba'
BASE_SHA='b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd'
OUT='analysis/pending_insertion_500_038_source_only_v5'
CENSUS='analysis/pending_insertion_500_035_inventory_v1/census.json'

def baseline():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);require_hash(ROOT/BASE,BASE_SHA);m=read(BASE.replace('.gba','.json'))
    st=read('analysis/pending500_037_v2/batch_status.json')
    need(st['artifact_audited_ROM_sha256']==BASE_SHA and st['next500_admission_ready'] and st['new037_board_actual_caller_selector_and_Korean_display_verified'],'037 representative link prerequisite')
    for x in st['reports'].values():require_hash(ROOT/x['path'],x['sha256'])
    return cfg,sp.read_bytes(),(ROOT/BASE).read_bytes(),m

def select():
    cfg,source,rom,m=baseline();census=read(CENSUS)
    for p,h in census['dependencies'].items():require_hash(ROOT/p,h)
    applied={u['id'] for r in layout_records(m) for u in r['layout']};owners=defaultdict(list)
    for r in layout_records(m):owners[r['archive']].append(r)
    pending={k for g in census['groups'] for k in g['ids']}-applied;need(len(pending)==10924,'038 canonical remainder')
    typed=typed_lookup(source);lookup={a:r for a,r in typed.items() if {x['source_class'] for x in r} in ({'native-NPC'},{'navi-hint'})};boards={a:r for a,r in typed.items() if {x['source_class'] for x in r}=={'field-board'}};templates={};drafts={};good=[];bad=[]
    validators=[('normal-navi-tail-geometry',lambda a,b,c,d,e:navi_tail(a,b,c,d,e,88)),('fullbox',lambda a,b,c,d,e:hint_validate(a,b,c,d,e,88)),('normal-pages',lambda a,b,c,d,e:normal(a,b,c,d,e,88)),('normal-horizontal',lambda a,b,c,d,e:horizontal(a,b,c,d,e,88)),('normal-store-tail-geometry',lambda a,b,c,d,e:tail_validate(a,b,c,d,e,88))]
    for g in census['groups']:
        arc=g['archive']
        if arc not in lookup and arc not in boards or set(g['ids'])&applied or not g['all_japanese_literals_unapplied'] or g['already_applied_ids_in_script']:continue
        src=g['source_tpl'];require_hash(ROOT/src['path'],src['sha256']);text=templates.setdefault(arc,(ROOT/src['path']).read_text(encoding='utf-8-sig'));native=payload_of(source,g['source_row'])
        need(sha(native)==g['source_archive_sha256'] and payload_of(rom,g['source_row'])==native,'038 immutable native source')
        count=int(re.search(r'^@size (\d+)$',text,re.M)[1]);original_span=script_spans(native,count)[g['script']]
        for r in owners.get(arc,[]):
            live=rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']];need(sha(live)==r['compiled_sha256'] and script_spans(live,count)[g['script']]==original_span,'038 selected untouched script matches every current clone')
        section=re.search(r'^script '+str(g['script'])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)
        if section is None:continue
        one='@archive '+arc+'\n'+section[0];raw={u.key:u.text for u in literals(one)};units=[]
        for d in g['drafts']:
            require_hash(ROOT/d['path'],d['sha256']);a=drafts.setdefault(d['path'],read(d['path']));u=next(u for u in a['units'] if u['id']==d['id'])
            need(a['source_sha256']==sha(source) and a['source_tpl']==src and a['source_archive_sha256']==sha(native) and u['source']==raw[u['id']] and u['state']=='needs_review','038 canonical source/context binding');units.append(u)
        variants=[('canonical',{u['id']:u['translation'] for u in units})]
        try:variants.append(('normal-aggregate',aggregate(one,units,99)))
        except ValueError:pass
        v={u['id']:place(u['translation'],(180,180,168)) for u in units}
        if all(x is not None for x in v.values()):variants.append(('individual180',v))
        accepted=None;errors=[]
        for label,values in variants:
            if any(v.replace('\n',' ')!=next(u['translation'] for u in units if u['id']==k).replace('\n',' ') or not protected_edges(raw[k],v) for k,v in values.items()):continue
            target=replace_exact(one,values)
            for profile,validate in validators:
                try:geometry=validate(one,target,[g['script']],set(g['ids']),99)
                except ValueError as ex:errors.append(str(ex));continue
                accepted=dict(deepcopy(g),profile=profile,geometry=geometry,geometry_ids=g['ids'],explicit_layouts={u['id']:values[u['id']] for u in units if values[u['id']]!=u['translation']},layout_method=label,source_lookup_candidates=typed[arc],source_class=typed[arc][0]['source_class'],current_owned_archive=arc in owners,current_untouched_script_bytes_verified=True,current_parent_records=[dict(archive=r['archive'],rom_offset=r['rom_offset'],compiled_bytes=r['compiled_bytes'],compiled_sha256=r['compiled_sha256']) for r in owners.get(arc,[])],product_admitted=False)
                break
            if accepted:break
        if accepted:good.append(accepted)
        else:bad.append(dict(archive=arc,script=g['script'],units=g['units'],reasons=sorted(set(errors))))
    good.sort(key=lambda g:(g['archive'] in owners,g['profile']=='normal-store-tail-geometry',g['archive'],g['script']))
    dp={0:[]}
    for i,g in enumerate(good):
        for total in sorted(list(dp),reverse=True):
            n=total+g['units']
            if n<=500 and n not in dp:dp[n]=dp[total]+[i]
        if 500 in dp:break
    need(500 in dp,'038 exact500 whole-script source subset; no partial apply')
    groups=[good[i] for i in dp[500]];ids=[k for g in groups for k in g['ids']];need(len(ids)==len(set(ids))==500 and set(ids)<=pending,'038 exact500 disjoint')
    deps=['tools/normal_navi_tail038_v1.py','tools/field_hint_capacity.py','tools/specs/source038_v5_version.json','tools/prepare_source500_038_v3.py','tools/specs/source038_v4_version.json',CENSUS,'tools/prepare_source500_038_v5.py','tools/normal_store_tail038_v1.py','tools/normal_timing_capacity_025.py','tools/normal_battle_choice_capacity_026.py','tools/survey_aggregate_normal_033.py','tools/survey_calendar_layout500_031_v2.py','tools/prepare_source500_037_v2.py','analysis/pending500_037_v2/board_qualified_v1.json']
    frozen_write(ROOT/OUT/'selection.json',dict(schema=1,status='EXACT500_SOURCE_PREPARATION_NOT_PRODUCT_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),planned_new_units=500,selected_ids=sorted(ids),groups=groups,archives=sorted({g['archive'] for g in groups}),profiles=dict(Counter({p:sum(g['units'] for g in groups if g['profile']==p) for p in {g['profile'] for g in groups}})),native_nickname_bound=99,canonical_pending_draft_ids_before_selection=len(pending),remaining_unselected_draft_ids=len(pending)-500,candidate_units=sum(g['units'] for g in good),candidate_scripts=len(good),rejections=bad,wording_changed=False,rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Existing canonical wording, not500 new authored sentences or ROM-applied IDs.','Geometry-only projection of final native store tail; source commands retained. Store native code/CPU effects, cleared-page Navi branch continuations and battle outcomes unverified for new scope.','A4/B0/B1 NPC/board and navi-hint lookups are finite static source paths, not natural acquisition. A4 NPC table is NOT null:53790=08053B18. Earlier prose was incorrect; old classification JSON records false. Already owned archives require full carry and supersession integration; source-only target must never replace current translated archive.','Current ROM stays037/19622; canonical pending10924 includes selected500; not whole-game/image remainder.','All entries remain needs_review/NON-DISTRIBUTION; no patch packages.']))
    print('PASS038 source-only exact500',len(groups),'scripts',len({g['archive'] for g in groups}),'archives; candidates',sum(g['units'] for g in good),flush=True)

if __name__=='__main__':select()
