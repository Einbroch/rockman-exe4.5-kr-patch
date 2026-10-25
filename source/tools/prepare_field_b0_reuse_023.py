"""Context-exact source-to-wording links; 500 development inputs, NOT ROM admission."""
import re,struct
from copy import deepcopy
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from tpl_literals import literals,skeleton,replace_literals
from fullbox_capacity import validate
from fullbox_layout import place
from survey_batch500_017_layout import protected_edges
from verify_tpi_index import lz77_decompress

EXTRACTION='analysis/field_b0_hints_v1/extraction.json'
OUT='analysis/pending_insertion_500_023_b0_reuse_v1'
INPUTS='analysis/pending_insertion_500_023_b0_inputs_v1'

def sections(tpl):
    return {int(m.group(1)):m.group() for m in re.finditer(r'^script\s+(\d+)\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)}

def script_identity(section):
    t='@archive CONTEXT\n'+section
    return skeleton(t),[(u.key.split(':',1)[1],u.language,u.text) for u in literals(t)]

def main():
    e=read(EXTRACTION);rp=ROOT/e['baseline_rom'];require_hash(rp,e['baseline_sha256']);m=read(rp.with_suffix('.json'));applied={u['id'] for r in layout_records(m) for u in r['layout']}
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,e['source_sha256']);source=sp.read_bytes();coverage_path='analysis/translation_first_v1/coverage.json';cov=read(coverage_path)
    if not cov['passed'] or cov['source_sha256']!=sha(source):raise ValueError('Frozen draft coverage source')
    by=defaultdict(list)
    for path,h in cov['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);asset=read(path);by[asset['archive']].append((path,h,asset))
    candidates=[];rejected=[];storage={};jp=re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
    for r in e['archives']:
        arc=r['archive'];navi=r['navi_index'];donor_arc=f"{struct.unpack_from('<I',source,0x54180+navi*4)[0]-0x08000000:X}";donors=by[donor_arc]
        if not donors:raise ValueError('Same-Navi donor absent')
        require_hash(ROOT/r['source_tpl']['path'],r['source_tpl']['sha256']);tpl=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');new_sections=sections(tpl);pool=defaultdict(list);old_sections=None;old_ref=None
        for path,h,a in donors:
            ref=a['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);native,_=lz77_decompress(source,int(donor_arc,16))
            if a['source_sha256']!=sha(source) or a['source_archive_sha256']!=sha(native) or a['review']['release_eligible'] is not False:raise ValueError('Donor source/policy')
            s=sections((ROOT/ref['path']).read_text(encoding='utf-8-sig'))
            if old_sections is not None and s!=old_sections:raise ValueError('Conflicting donor extraction')
            old_sections=s;old_ref=ref
            for u in a['units']:pool[u['id'].split(':',1)[1]].append((path,h,u))
        storage[arc]=r;targets=defaultdict(list)
        for u in r['units']:
            if jp.search(u['source']):targets[int(u['id'].split(':')[1])].append(u)
        for script,items in targets.items():
            section=new_sections[script]
            if script not in old_sections or script_identity(section)!=script_identity(old_sections[script]):
                rejected.append(dict(archive=arc,navi_index=navi,script=script,ids=[u['id'] for u in items],reason='source_script_controls_or_literal_context_differ'));continue
            links=[];units=[]
            for u in items:
                key=u['id'].split(':',1)[1];opts=pool[key]
                if not opts or len({(v['source'],v['translation'],v['state']) for _,_,v in opts})!=1:raise ValueError('Absent/conflicting same-role wording '+u['id'])
                path,h,v=opts[0]
                if v['source']!=u['source'] or v['state']!='needs_review' or u['id'] in applied:raise ValueError('Protected literal/state/new-ID binding')
                links.append(dict(id=u['id'],source=u['source'],parent=dict(path=path,sha256=h,unit_id=v['id'])));units.append(dict(id=u['id'],source=u['source'],translation=v['translation'],state=v['state']))
            commands=re.findall(r'^\t(print\w+)\b',section,re.M);profile=dict(script=script,ids=[u['id'] for u in items]);layouts={};reason=None;geometry=None
            placed=[]
            for u in units:
                v=place(u['translation'])
                if v is None or not protected_edges(u['source'],v):reason='same_wording_fullbox_placement_unresolved';break
                placed.append(dict(u,translation=v))
                if v!=u['translation']:layouts[u['id']]=v
            if reason is None:
                guards=re.findall(r'^\t(\w+)\b',section.split('\tmugshotShow')[0],re.M)
                if guards:profile['entry_guards']=guards
                if len(re.findall(r'^\tmugshotShow\s*$',section,re.M))>1:profile['portrait_changes']=True
                try:geometry=validate(tpl,replace_literals(tpl,placed),[profile],set(profile['ids']))
                except ValueError as ex:reason=str(ex)
            candidates.append(dict(archive=arc,navi_index=navi,script=script,units=len(items),ids=profile['ids'],source_tpl=r['source_tpl'],source_script_sha256=sha(section.encode('utf8')),donor_archive=donor_arc,donor_source_tpl=old_ref,source_script_controls_and_all_literals_identical=True,links=links,print_commands=commands,fullbox_profile=profile,individual_layouts=layouts,fullbox_geometry=geometry,technical_class='fullbox_geometry_verified' if geometry else 'print_insertion_requires_aggregate_model' if commands else 'entry_or_geometry_contract_unresolved',technical_rejection=reason))
    total=sum(g['units'] for g in candidates);states={0:[]}
    # Keep complete per-script Japanese literal groups. Prioritize the visible default hint.
    for g in sorted(candidates,key=lambda g:(g['script']!=10,g['archive'],g['script'])):
        for n,chosen in list(states.items()):
            k=n+g['units']
            if k<=500 and k not in states:states[k]=chosen+[g]
    classes=Counter()
    for g in candidates:classes[g['technical_class']]+=g['units']
    survey=dict(schema=1,status='CONTEXT_EXACT_WORDING_REUSE_NOT_PRODUCT_ADMISSION',baseline_rom=e['baseline_rom'],baseline_sha256=e['baseline_sha256'],source_sha256=sha(source),extraction=dict(path=EXTRACTION,sha256=sha((ROOT/EXTRACTION).read_bytes())),coverage=dict(path=coverage_path,sha256=sha((ROOT/coverage_path).read_bytes())),candidate_units=total,candidate_groups=len(candidates),units_by_technical_class=dict(classes),rejected_groups=rejected,candidates=candidates,rom_written=False,release_eligible=False,limits='Reuse only the same Navi, same script/literal role, exact source text and entire source-script control/literal identity. Authoritative wording remains the frozen donor asset; no prose rewrite or human approval. Capacity, B0 ROM-reader registration, compiled source/cumulative/integrity/runtime checks remain separate. Not a whole-game remaining count.')
    frozen_write(ROOT/OUT/'survey.json',survey)
    if 500 not in states:raise ValueError('No exact500 complete-script subset; preserve survey')
    chosen=states[500];ids=[u for g in chosen for u in g['ids']]
    if len(ids)!=500 or len(set(ids))!=500 or set(ids)&applied:raise ValueError('Actual distinct new500 source identities')
    selection=dict(schema=1,batch_id='pending-insertion-500-023-b0-context-reuse',policy='development-draft; NON-DISTRIBUTION',release_eligible=False,baseline_rom=e['baseline_rom'],baseline_sha256=e['baseline_sha256'],source_sha256=sha(source),survey=dict(path=OUT+'/survey.json',sha256=sha((ROOT/OUT/'survey.json').read_bytes())),total_new_units=500,groups=chosen,rom_written=False,insertion_ready=False)
    frozen_write(ROOT/OUT/'selection.json',selection)
    selected_by=defaultdict(list)
    for g in chosen:selected_by[g['archive']].append(g)
    results=[]
    for arc,groups in sorted(selected_by.items()):
        r=storage[arc];units=[];links=[]
        for g in groups:
            for link in g['links']:
                parent=link['parent'];require_hash(ROOT/parent['path'],parent['sha256']);v=next(u for u in read(parent['path'])['units'] if u['id']==parent['unit_id'])
                units.append(dict(id=link['id'],source=link['source'],translation=v['translation'],state=v['state']));links.append(link)
        order={u['id']:i for i,u in enumerate(r['units'])};units.sort(key=lambda u:order[u['id']]);asset=dict(schema=1,archive=arc,source_sha256=sha(source),source_archive_sha256=r['source_payload_sha256'],source_tpl=r['source_tpl'],consumer='normal-dialogue',policy='development-draft; NON-DISTRIBUTION',review=dict(release_eligible=False,state='needs_review'),units=units,source_draft_links=dict(selection=dict(path=OUT+'/selection.json',sha256=sha((ROOT/OUT/'selection.json').read_bytes())),links=links),ownership='Derived read-only projection; edit authoritative donor wording only. New source fields come from B0 extraction, not donor identity.',insertion_ready=False)
        path=INPUTS+'/'+arc+'_draft_ko.json';frozen_write(ROOT/path,asset);results.append(dict(archive=arc,path=path,sha256=sha((ROOT/path).read_bytes()),units=len(units)))
    frozen_write(ROOT/OUT/'prepared_inputs.json',dict(schema=1,total_units=500,archives=results,rom_written=False,insertion_ready=False,release_eligible=False))
    print('PASS context-exact reuse candidates',total,'selected500',len(results),'archives;',dict(classes),'; no ROM written')

if __name__=='__main__':main()
