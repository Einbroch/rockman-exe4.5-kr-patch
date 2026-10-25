"""Next exact500 canonical draft preparation, never a product/ROM writer.

Reuse protected source/wording/geometry contracts, exclude every036 owner.
Additional compressed loader classes remain explicitly unadmitted.
"""
from prepare_source500_036_v1 import *
from field_npc_rom_selector_036_v1 import source_population as population036

BASE='poc/output/pending500_036_v1.gba'
BASE_SHA='0d85748e6c8c9b6abd561972f319b2687d6791778092c5ff1e9b15abb868876a'
OUT='analysis/pending_insertion_500_037_source_only_v1'

def baseline():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);require_hash(ROOT/BASE,BASE_SHA);m=read(BASE.replace('.gba','.json'));audit=read('analysis/pending500_036_v1/integration.json')
    need(m['output_sha256']==BASE_SHA and audit['passed'] and audit['rom_sha256']==BASE_SHA and audit['independent_rebuild_byte_identical'],'Current036 audited product')
    return cfg,sp.read_bytes(),(ROOT/BASE).read_bytes(),m

def native_lookup(source):
    # A0/A1/A2/A3 have four sub-area rows and seven weekday entries.
    # This is a bounded source classification, not native runtime admission.
    out=defaultdict(list)
    for scene in (0xA0,0xA1,0xA2,0xA3):
        top=0x53700+(scene-0x80)*4;table=struct.unpack_from('<I',source,top)[0]-0x08000000
        need(0<=table<=len(source)-16,'037 scene-table range')
        for sub in range(4):
            row=struct.unpack_from('<I',source,table+sub*4)[0]-0x08000000;need(0<=row<=len(source)-28,'037 subtable range')
            for day in range(7):
                off=struct.unpack_from('<I',source,row+day*4)[0]-0x08000000;need(0<=off<len(source) and source[off]==0x10,'037 source compressed lookup')
                payload,_=lz77_decompress(source,off);need(payload[:2]==b'\xfe\x01','037 native255 header')
                out[f'{off:X}'].append(dict(scene=scene,sub=sub,slot=day,pointer=row+day*4,root=0x02039800,native_bytes=len(payload)))
    return out

def select():
    cfg,source,rom,m=baseline();survey=read(SURVEY)
    for p,h in survey['dependencies'].items():require_hash(ROOT/p,h)
    applied={u['id'] for r in layout_records(m) for u in r['layout']};owned={r['archive'] for r in layout_records(m)};old=read('poc/output/pending500_035_v2.json');oldids={u['id'] for r in layout_records(old) for u in r['layout']};manifest=read('analysis/pending_insertion_500_036_npc_inputs_v1/manifest.json');cohort={k for r in manifest['archives'] for k in r['new_ids']}
    need(oldids<=applied and applied-oldids==cohort and len(cohort)==500,'Actual036 exact500 prior delta')
    lookup=native_lookup(source)
    candidates=[deepcopy(g) for g in survey['candidate_groups'] if g['archive'] not in owned and g['storage']=='compressed' and g['profile'] in ('normal-pages','normal-horizontal')]
    candidates.sort(key=lambda g:(g['archive'] not in lookup,g['archive'],g['script']))
    dp={0:[]}
    for i,g in enumerate(candidates):
        for total in sorted(list(dp),reverse=True):
            n=total+g['units']
            if n<=500 and n not in dp:dp[n]=dp[total]+[i]
        if 500 in dp:break
    need(500 in dp,'Exact500 whole-script subset; no split/partial batch')
    groups=[candidates[i] for i in dp[500]];ids=[k for g in groups for k in g['ids']];need(len(ids)==len(set(ids))==500 and not set(ids)&applied,'037 new nonduplicate IDs')
    texts={};drafts={};profiles=Counter();validators=dict(VALIDATORS);native_units=0;other_units=0
    for g in groups:
        need(not g['locked_parent_units'] and not g['already_applied_ids_in_script'],'037 no edited parent source')
        arc=g['archive'];src=g['source_tpl'];require_hash(ROOT/src['path'],src['sha256']);original=texts.setdefault(arc,(ROOT/src['path']).read_text(encoding='utf-8-sig'));raw={u.key:u.text for u in literals(original)};payload=payload_of(source,g['source_row'])
        need(sha(payload)==g['source_archive_sha256'] and payload_of(rom,g['source_row'])==payload,'037 current source binary provenance')
        values={}
        for d in g['drafts']:
            require_hash(ROOT/d['path'],d['sha256']);asset=drafts.setdefault(d['path'],read(d['path']));u=next(u for u in asset['units'] if u['id']==d['id']);v=g['explicit_layouts'].get(u['id'],u['translation'])
            need(asset['source_sha256']==sha(source) and asset['source_tpl']==src and asset['source_archive_sha256']==sha(payload) and u['source']==raw[u['id']] and u['state']=='needs_review','037 canonical wording source/context baseline')
            need(v.replace('\n',' ')==u['translation'].replace('\n',' ') and protected_edges(u['source'],v),'037 no wording/space/control-edge rewrite');values[u['id']]=v
        need(set(values)==set(g['ids']) and validators[g['profile']](original,replace_exact(original,values),[g['script']],set(g['geometry_ids']),99)==g['geometry'],'037 whole-script current geometry replay')
        profiles[g['profile']]+=g['units'];g['source_native_lookup_candidates']=lookup.get(arc,[])
        if arc in lookup:native_units+=g['units']
        else:other_units+=g['units']
    census=read('analysis/pending_insertion_500_035_inventory_v1/census.json');pending={k for g in census['groups'] for k in g['ids']}-applied;need(len(pending)==11424 and set(ids)<=pending,'037 canonical pending denominator')
    deps=[SURVEY,'analysis/pending_insertion_500_035_inventory_v1/census.json','analysis/pending500_036_v1/integration.json','tools/prepare_source500_037_v1.py','tools/prepare_source500_036_v1.py'];deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS]
    frozen_write(ROOT/OUT/'selection.json',dict(schema=1,status='EXACT500_CANONICAL_SOURCE_PREPARATION_NOT_PRODUCT_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),planned_new_units=500,selected_ids=sorted(ids),groups=groups,archives=sorted(texts),profiles=dict(profiles),native_nickname_bound=99,native_A0_A1_A2_A3_lookup_classified_units=native_units,other_compressed_loader_unestablished_units=other_units,canonical_pending_draft_ids_before_selection=len(pending),remaining_unselected_draft_ids=len(pending-set(ids)),wording_changed=False,rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Existing canonical wording revalidated, not500 new authored sentences or ROM-integrated IDs.','A2/static lookup and additional compressed loader classes require boundary/admission evidence before any037 ROM build.','A1/A3 natural acquisition remains unverified;036 qualified native boundary diagnostics do not establish natural progression.','All entries remain needs_review/NON-DISTRIBUTION. Count is canonical draft subset, not whole-game/images.']))
    print('PASS037 source-only exact500',len(groups),'scripts',len(texts),'archives; native lookup',native_units,'other loader unestablished',other_units,'NO ROM')

if __name__=='__main__':select()
