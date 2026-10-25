"""Current038 pending inventory and exact500 profile-layout investigation.

No primary-build input, ROM, source text or canonical translation is modified.
The new profile loader/reader is NOT the field NPC/board/hint selector.
"""
import re,struct
from collections import Counter,defaultdict
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from prepare_source500_038_v3 import typed_lookup
from verify_tpi_index import parse_tpi,lz77_decompress
from tpl_literals import literals
from field_hint_capacity import events
from pet_quick_capacity import PREFIX
from profile_quick_geometry039_v1 import validate
from survey_aggregate_pet_033 import replace_exact
from survey_batch500_017_layout import protected_edges
from profile_layout039_v1 import propose
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

BASE='poc/output/pending500_038_v2.gba'
BASE_SHA='97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b'
CENSUS='analysis/pending_insertion_500_035_inventory_v1/census.json'
OUT='analysis/pending_insertion_500_039_profile_source_v2'

def ref(path):return dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()))

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();m=read(BASE.replace('.gba','.json'));status=read('analysis/pending500_038_v2/batch_status.json')
    if not status['next500_development_preparation_eligible'] or not status['new038_three_classes_Korean_display_verified'] or status['artifact_audited_ROM_sha256']!=BASE_SHA:raise ValueError('038 representative-link prerequisite')
    census=read(CENSUS)
    for p,h in census['dependencies'].items():require_hash(ROOT/p,h)
    applied={u['id'] for r in layout_records(m) for u in r['layout']};pending={k for g in census['groups'] for k in g['ids']}-applied
    if len(pending)!=10424:raise ValueError('039 canonical pending identity')
    out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False)
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);code=[]
    for lo,hi in [(0x448BC,0x448DC),(0xCEC,0xCF4)]:
        if source[lo:hi]!=rom[lo:hi]:raise ValueError('Original profile code drift')
        ins=list(decoder.disasm(source[lo:hi],0x08000000+lo))
        if sum(i.size for i in ins)!=hi-lo:raise ValueError('Bounded Thumb instruction extent')
        code.extend(dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in ins)
    word=lambda at:struct.unpack_from('<I',source,at)[0]
    if word(0x448DC)!=0x080448E0 or word(0x4493C)!=0x02024000 or source[0x448DC:0x44940]!=rom[0x448DC:0x44940]:raise ValueError('Original profile table and shared load/root literal')
    if next(i for i in code if i['address']==0x080448C2)['operands']!='#0x804f7b6' or next(i for i in code if i['address']==0x080448D6)['operands']!='#0x80ec158':raise ValueError('Original profile reader/LZ call')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={r['offset']:r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};lookups=defaultdict(list)
    for navi in range(23):
        ptr=0x448E0+4*navi;offset=word(ptr)-0x08000000
        row=catalog[offset]
        if not row['compressed'] or source[offset]!=0x10:raise ValueError('Profile original compressed source')
        lookups[f'{offset:X}'].append(dict(Navi=navi,pointer=ptr))
    if len(lookups)!=21:raise ValueError('Profile23 ->21 source owner population')
    owners=defaultdict(list)
    for r in layout_records(m):owners[r['archive']].append(r)
    profile_records=[]
    for arc,refs in sorted(lookups.items()):
        row=catalog[int(arc,16)];native,used=lz77_decompress(source,int(arc,16))
        if set(row['pointers'])!={r['pointer'] for r in refs} or rom[int(arc,16):int(arc,16)+used]!=source[int(arc,16):int(arc,16)+used] or any(rom[r['pointer']:r['pointer']+4]!=source[r['pointer']:r['pointer']+4] for r in refs):raise ValueError('Profile native full source/reference identity')
        profile_records.append(dict(archive=arc,source_row=row,references=refs,native_bytes=len(native),native_sha256=sha(native),current_compiled_owners=len(owners.get(arc,[]))))
    typed=typed_lookup(source);groups=[g for g in census['groups'] if not set(g['ids'])&applied];good=[];bad=[];templates={};drafts={}
    for g in groups:
        arc=g['archive']
        if arc not in lookups:continue
        if owners.get(arc):raise ValueError('Profile carry unexpectedly required')
        sr=g['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);tpl=templates.setdefault(arc,(ROOT/sr['path']).read_text(encoding='utf-8-sig'))
        section=re.search(r'^script '+str(g['script'])+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)
        if section is None:continue
        one='@archive '+arc+'\n'+section[0];seq=events(one)
        if len(seq)<4 or any(e[1]!='command' for e in seq[:4]) or [e[2] for e in seq[:4]]!=PREFIX:continue
        raw={u.key:u.text for u in literals(one)};proposals=[];values={}
        try:
            for link in g['drafts']:
                p=link['path']
                if p not in drafts:require_hash(ROOT/p,link['sha256']);drafts[p]=read(p)
                a=drafts[p];u=next(u for u in a['units'] if u['id']==link['id'])
                if a['source_sha256']!=sha(source) or a['source_tpl']!=sr or u['source']!=raw[u['id']] or u['state']!='needs_review':raise ValueError('Profile canonical identity')
                proposal=propose(u['translation'])
                if not protected_edges(u['source'],proposal['target']):raise ValueError('Profile source padding')
                values[u['id']]=proposal['target'];proposals.append(dict(id=u['id'],draft=link,layout=proposal))
            target=replace_exact(one,values);geometry=validate(one,target,[g['script']],set(g['ids']))
        except ValueError as ex:bad.append(dict(archive=arc,script=g['script'],units=g['units'],reason=str(ex)));continue
        item=deepcopy(g);item.update(source_class='PET-profile',source_lookup_candidates=lookups[arc],profile='profile-quick-zero-speed-visible-hold132',layout_proposals=proposals,geometry=geometry,source_row=next(x['source_row'] for x in profile_records if x['archive']==arc),new_geometry_policy_approval=False,product_admitted=False);good.append(item)
    good.sort(key=lambda g:(g['archive'],g['script']));dp={0:[]}
    for i,g in enumerate(good):
        for total in sorted(list(dp),reverse=True):
            n=total+g['units']
            if n<=500 and n not in dp:dp[n]=dp[total]+[i]
        if 500 in dp:break
    selected=[good[i] for i in dp.get(500,[])];ids=[k for g in selected for k in g['ids']]
    if selected and (len(ids)!=len(set(ids)) or len(ids)!=500 or not set(ids)<=pending):raise ValueError('039 exact500 proposal ownership')
    previous=read('analysis/pending_insertion_500_038_source_only_v5/selection.json')
    deps=[CENSUS,'tools/prepare_profile_source039_v2.py','tools/profile_layout039_v1.py','tools/profile_quick_geometry039_v1.py','tools/pet_quick_capacity.py','tools/prepare_source500_038_v3.py','analysis/pending500_038_v2/integration.json','analysis/pending500_038_v2/qualified_npc_hint_v1.json','analysis/pending500_038_v2/board_qualified_v1.json']
    result=dict(schema=1,status='PROFILE_SOURCE_AND_LAYOUT_PROPOSALS_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),current_ROM_units=m['translated_units'],canonical_pending_ids=len(pending),pending_storage_units=dict(Counter({k:sum(g['units'] for g in groups if g['storage']==k) for k in {g['storage'] for g in groups}})),pending_typed_source_units=sum(g['units'] for g in groups if g['archive'] in typed),previous038_eligible_unapplied_units=previous['candidate_units']-500,profile_source_owners=profile_records,source_code=code,profile_loader_entry=0x080448C8,source_LZ_BL=0x080448D6,native_destination=0x02024000,source_reader_entry=0x080448BC,source_reader_BL=0x080448C2,source_reader_target=0x0804F7B6,source_reader_return_LR=0x080448C7,field_selector_4FB4C_applicable=False,candidate_units=sum(g['units'] for g in good),candidate_scripts=len(good),selected_proposed_units=len(ids),selected_ids=sorted(ids),groups=selected,rejections=bad,wording_changed=False,layout_proposal_only=True,source_native_RAM_capacity_for_growth_established=False,product_admitted=False,rom_written=False,new_units_applied=0,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['New profile load root02024000 and direct4F7B6 reader are NOT038 field selector/root contract. Do not admit these through that selector.','Explicit132px window geometry comes from unchanged original prefix; proposed Hangul-syllable breaks preserve all normalized wording through per-break schema, but presentation is unapproved.','Visible-page EDFF hold and zero text speed are distinct source controls, not ordinary quick dialogue; external option/input overlap is unresolved. No translated archive compiled/reinserted yet; source roundtrip, font supply, new consumer CPU/loader/residency/display, cumulative immutable-source build and exact-ROM runtime remain.','CurrentROM stays038/20122, canonical pending10424. No partial500 or distribution output.'])
    frozen_write(out/'selection.json',result)
    print('039 profile source23Navis/21owners; layout candidates',result['candidate_units'],'selected proposals',len(ids),'NO ROM',flush=True)

if __name__=='__main__':main()
