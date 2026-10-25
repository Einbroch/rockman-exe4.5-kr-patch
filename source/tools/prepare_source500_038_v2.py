"""Source-only500: typed source tables including explicit B0/B1 and hints.

No runtime/product admission is inferred from these references. Preserve v1
failure and its candidate work; never include pointerless reward/tournament.
"""
import prepare_source500_038_v1 as prior
from prepare_source500_036_v1 import *
from normal_store_tail038_v1 import validate as tail_validate
from survey_new_storage_035 import VALIDATORS as KNOWN
from archive_scripts import script_spans

OUT='analysis/pending_insertion_500_038_source_only_v2'
BASE=prior.BASE
BASE_SHA=prior.BASE_SHA

def typed_lookup(source):
    result=defaultdict(list)
    def word(at):return struct.unpack_from('<I',source,at)[0]
    for scene in (0xA0,0xA1,0xA2,0xA3,0xB0,0xB1):
        table=word(0x53700+(scene-0x80)*4)-0x08000000
        need(0<=table<len(source)-16,'038 NPC scene lookup')
        for sub in range(4):
            row=word(table+4*sub)-0x08000000
            need(0<=row<len(source)-32,'038 NPC weekday lookup')
            for day in range(7):
                at=row+4*day;off=word(at)-0x08000000
                need(0<=off<len(source) and source[off]==0x10,'038 NPC compressed reference')
                result[f'{off:X}'].append(dict(source_class='native-NPC',scene=scene,sub=sub,slot=day,pointer=at,root=0x02039800,caller_lr=0x0804F773))
        board=word(0x537CC+(scene-0x80)*4)-0x08000000
        need(0<=board<len(source)-16,'038 board scene lookup')
        for sub in range(4):
            at=board+sub*4;off=word(at)-0x08000000
            need(0<=off<len(source) and source[off]==0x10,'038 board compressed reference')
            result[f'{off:X}'].append(dict(source_class='field-board',scene=scene,sub=sub,pointer=at,root=0x0203C800,caller_lr=0x0806A507))
    for scene in (0xA0,0xA1,0xA2,0xA3,0xA4,0xB0,0xB1):
        table=word(0x53FA0+(scene-0x80)*4)-0x08000000
        need(0<=table<len(source)-92,'038 hint source table')
        for navi in range(23):
            at=table+navi*4;off=word(at)-0x08000000
            if off==-0x08000000:continue
            need(0<=off<len(source) and source[off]==0x10,'038 hint compressed reference')
            result[f'{off:X}'].append(dict(source_class='navi-hint',scene=scene,navi=navi,pointer=at,root=0x0203D800,caller_lr=0x0804F807))
    return result

def baseline():return prior.baseline()

def select():
    cfg,source,rom,m=baseline();lookup=typed_lookup(source);old=read(prior.OUT+'/selection_attempt_v1.json');survey=read(SURVEY)
    for p,h in survey['dependencies'].items():require_hash(ROOT/p,h)
    census=read(prior.CENSUS);applied={u['id'] for r in layout_records(m) for u in r['layout']};owners=defaultdict(list)
    for r in layout_records(m):owners[r['archive']].append(r)
    good={};validators=dict(KNOWN);validators['normal-store-tail-geometry']=lambda a,b,c,d,e:tail_validate(a,b,c,d,e,88)
    templates={};drafts={}
    for g in old['candidate_groups']+survey['candidate_groups']:
        arc=g['archive'];key=(arc,g['script'])
        if arc not in lookup or key in good or set(g['ids'])&applied or g.get('already_applied_ids_in_script') or g.get('locked_parent_units'):continue
        refs=lookup[arc];need(len({x['source_class'] for x in refs})==1,'038 unique lookup class')
        src=g['source_tpl'];require_hash(ROOT/src['path'],src['sha256']);original=templates.setdefault(arc,(ROOT/src['path']).read_text(encoding='utf-8-sig'));raw={u.key:u.text for u in literals(original)};native=payload_of(source,g['source_row']);count=int(re.search(r'^@size (\d+)$',original,re.M)[1])
        need(sha(native)==g['source_archive_sha256'] and payload_of(rom,g['source_row'])==native,'038 source payload retained')
        need(set(g['source_row']['pointers'])=={x['pointer'] for x in refs},'038 complete explicit table references')
        original_script=script_spans(native,count)[g['script']]
        for r in owners.get(arc,[]):
            live=rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']];need(sha(live)==r['compiled_sha256'] and script_spans(live,count)[g['script']]==original_script,'038 source script matches all existing clones')
        values={}
        for d in g['drafts']:
            require_hash(ROOT/d['path'],d['sha256']);a=drafts.setdefault(d['path'],read(d['path']));u=next(u for u in a['units'] if u['id']==d['id']);v=g['explicit_layouts'].get(u['id'],u['translation'])
            need(a['source_sha256']==sha(source) and a['source_tpl']==src and a['source_archive_sha256']==sha(native) and u['source']==raw[u['id']] and u['state']=='needs_review' and protected_edges(u['source'],v) and v.replace('\n',' ')==u['translation'].replace('\n',' '),'038 canonical wording/source/policy')
            values[u['id']]=v
        proof=validators[g['profile']](original,replace_exact(original,values),[g['script']],set(g['geometry_ids']),99)
        need(proof==g['geometry'],'038 independent geometry replay')
        item=deepcopy(g);item.update(source_lookup_candidates=refs,source_class=refs[0]['source_class'],current_owned_archive=arc in owners,current_untouched_script_bytes_verified=True,current_parent_records=[dict(archive=r['archive'],rom_offset=r['rom_offset'],compiled_bytes=r['compiled_bytes'],compiled_sha256=r['compiled_sha256']) for r in owners.get(arc,[])],product_admitted=False);good[key]=item
    candidates=sorted(good.values(),key=lambda g:(g['current_owned_archive'],g['source_class']=='navi-hint',g['profile']=='normal-store-tail-geometry',g['archive'],g['script']))
    dp={0:[]}
    for i,g in enumerate(candidates):
        for total in sorted(list(dp),reverse=True):
            n=total+g['units']
            if n<=500 and n not in dp:dp[n]=dp[total]+[i]
        if 500 in dp:break
    need(500 in dp,'038 whole-script exact500 only')
    groups=[candidates[i] for i in dp[500]];ids=[k for g in groups for k in g['ids']];pending={k for g in census['groups'] for k in g['ids']}-applied
    need(len(pending)==10924 and len(ids)==len(set(ids))==500 and set(ids)<=pending,'038 exact500 disjoint pending subset')
    deps=[prior.OUT+'/selection_attempt_v1.json',SURVEY,prior.CENSUS,'tools/prepare_source500_038_v2.py','tools/prepare_source500_038_v1.py','tools/normal_store_tail038_v1.py','analysis/pending500_037_v2/board_qualified_v1.json']+['tools/'+fn.__module__+'.py' for _,fn in KNOWN]
    result=dict(schema=1,status='EXACT500_TYPED_SOURCE_PREPARATION_NOT_PRODUCT_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),planned_new_units=500,selected_ids=sorted(ids),groups=groups,archives=sorted({g['archive'] for g in groups}),native_nickname_bound=99,profiles={p:sum(g['units'] for g in groups if g['profile']==p) for p in {g['profile'] for g in groups}},source_classes={p:sum(g['units'] for g in groups if g['source_class']==p) for p in {g['source_class'] for g in groups}},canonical_pending_draft_ids_before_selection=len(pending),remaining_unselected_draft_ids=len(pending)-500,candidate_units=sum(g['units'] for g in candidates),candidate_scripts=len(candidates),wording_changed=False,rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in set(deps)},limits=['Existing canonical wording selected, not500 newly authored translations or actual ROM-applied IDs.','Geometry projection of protected final store tail is NOT native store CPU or battle-outcome admission.','B0/B1 source lookups and A4 hint root/caller are static classifications. Natural A4 field acquisition is NOT inferred from its hint table; NPC table is null.','Previously owned clones require complete carry merge/supersession and all old translated scripts preserved before product admission.','Compile roundtrips/font/metrics, typed registry/CPU/applicability, cumulative immutable-source build/rebuild and exact-ROM runtime still required.','Current037 ROM/19622 remains; canonical pending10924 includes selected500. Whole-game/images/Hangul commit-save-redisplay not complete.','needs_review/NON-DISTRIBUTION; no distribution packages.'])
    frozen_write(ROOT/OUT/'selection.json',result)
    print('PASS038 exact500 SOURCE ONLY',len(groups),'scripts',len(result['archives']),'archives',result['source_classes'],result['profiles'],'candidates',result['candidate_units'],flush=True)

if __name__=='__main__':select()
