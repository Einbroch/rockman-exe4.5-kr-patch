"""Materialize the frozen500 selection verbatim, with per-unit parent links."""
import re
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from tpl_literals import literals
SELECTION='analysis/pending_insertion_500_016_selection_v1/selection.json'
OUT='analysis/pending_insertion_500_016_inputs_v1'
def prepare(selection=SELECTION,out_dir=OUT,allow_carry=False):
    p=read(selection);require_hash(ROOT/p['survey']['path'],p['survey']['sha256']);require_hash(ROOT/p['baseline_rom'],p['baseline_sha256']);cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],p['source_sha256'])
    m=read(p['baseline_rom'].replace('.gba','.json'));applied={r['archive'] for r in layout_records(m)};registry=read('tools/specs/exe45_dialogue_archives_v1.json')['archives'];total=0;seen=set();out=[]
    if p['total_new_units']!=500 or p['release_eligible'] is not False or p['policy']!='development-draft; NON-DISTRIBUTION':raise ValueError('Selection policy/scope')
    for item in p['selected']:
        arc=item['archive']
        if arc in seen or (not allow_carry and (arc in applied or arc in registry)):raise ValueError('Untouched archive contract')
        seen.add(arc);selected={r['id']:r for g in item['groups'] for r in g['drafts']};tpl_ref=item['groups'][0]['source_tpl'];require_hash(ROOT/tpl_ref['path'],tpl_ref['sha256']);tpl=(ROOT/tpl_ref['path']).read_text(encoding='utf-8-sig');native=literals(tpl);units=[];links=[];parent=None
        # Reconstruct source literal order, not lexical sorting of :10 and :2.
        for n in native:
            if n.key not in selected:continue
            ref=selected[n.key];require_hash(ROOT/ref['path'],ref['sha256']);a=read(ref['path'])
            if a['archive']!=arc or a['source_sha256']!=p['source_sha256'] or a['source_tpl']!=tpl_ref or a['review']['release_eligible'] is not False:raise ValueError('Selected draft identity/policy')
            u=next(u for u in a['units'] if u['id']==n.key)
            if u['source']!=n.text or n.language!='mmbn45' or u['state']!='needs_review' or re.search(r'[\u3040-\u30ff\u3400-\u9fff]',u['translation']):raise ValueError('Source/wording/state binding')
            if parent is None:parent=a
            units.append(deepcopy(u));links.append(dict(unit_id=n.key,parent=dict(path=ref['path'],sha256=ref['sha256'],unit_id=n.key)))
        if len(units)!=item['units'] or {u['id'] for u in units}!=set(selected):raise ValueError('Frozen group identity')
        b=deepcopy(parent);b.update(consumer='normal-dialogue',units=units,insertion_state='Explicit frozen500 technical development selection; review and runtime incomplete',source_draft_links=dict(selection=dict(path=selection,sha256=sha((ROOT/selection).read_bytes())),links=links))
        target=out_dir+'/'+arc+'_draft_ko.json';frozen_write(ROOT/target,b);out.append(dict(archive=arc,path=target,sha256=sha((ROOT/target).read_bytes()),units=len(units),scripts=sorted({int(u['id'].split(':')[1]) for u in units}),selected_ids=[u['id'] for u in units]));total+=len(units)
    if total!=500:raise ValueError('Exact500 input denominator')
    return out
if __name__=='__main__':print('Prepared',len(prepare()),'archives; source wording unchanged')
