"""Protected TPL/wording/layout audit; deliberately not compiler preflight."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals,skeleton,replace_literals
from survey_batch500_017_layout import advance,protected_edges
from prepare_repartition500 import layout_records

def main():
    folder='analysis/pending_insertion_500_019_inputs_v1'
    inputs=read(folder+'/inputs.json');sel=read(inputs['selection']['path']);require_hash(ROOT/inputs['selection']['path'],inputs['selection']['sha256'])
    require_hash(ROOT/sel['baseline_rom'],sel['baseline_sha256']);meta=read(sel['baseline_rom'].replace('.gba','.json'))
    applied={u['id'] for r in layout_records(meta) for u in r['layout']}
    require_hash(ROOT/sel['individual_layout']['path'],sel['individual_layout']['sha256']);layouts=read(sel['individual_layout']['path'])['layouts']
    all_ids=set();reports=[]
    for item in inputs['inputs']:
        require_hash(ROOT/item['path'],item['sha256']);asset=read(item['path']);ref=asset['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256'])
        source=(ROOT/ref['path']).read_text(encoding='utf-8-sig');units=deepcopy(asset['units']);original={i.key:i for i in literals(source)}
        for u in units:
            key=u['id']
            if key in all_ids or key in applied or u['source']!=original[key].text or u['state']!='needs_review':raise ValueError('Selected ID/source/state')
            all_ids.add(key)
            if key in layouts:
                target=layouts[key]
                if u['translation'].replace('\n',' ')!=target.replace('\n',' ') or u['translation'].count('\n')!=target.count('\n'):raise ValueError('Layout changes wording/topology')
                u['translation']=target
            if not protected_edges(u['source'],u['translation']) or u['source'].count('\n')!=u['translation'].count('\n') or max(map(advance,u['translation'].split('\n')))>132 or len(u['translation'].split('\n'))>3:raise ValueError('Protected edges/static geometry')
        target=replace_literals(source,units,language='mmbn45');after={i.key:i for i in literals(target)}
        if set(after)!=set(original) or skeleton(target)!=skeleton(source):raise ValueError('Protected command/argument/topology')
        selected={u['id']:u['translation'] for u in units}
        if any(after[k].language!=i.language or after[k].text!=(selected[k] if k in selected else i.text) for k,i in original.items()):raise ValueError('Unselected/source literal preservation')
        reports.append(dict(archive=item['archive'],units=len(units),source_tpl_sha256=ref['sha256'],protected_skeleton_sha256=sha(skeleton(source).encode('utf8')),source_literal_population=len(original),selected_ids=list(selected),unselected_literals_unchanged=True,commands_arguments_order_unchanged=True))
    if len(all_ids)!=500 or all_ids!={key for a in sel['selected'] for g in a['groups'] for key in g['ids']}:raise ValueError('Exact frozen500')
    frozen_write(ROOT/(folder+'/protected_input_audit.json'),dict(schema=1,status='PROTECTED_INPUTS_PASS_COMPILATION_AND_ROM_PENDING',selection=inputs['selection'],total_new_units=len(all_ids),explicit_layout_units=len(layouts),archives=reports,tool_sha256=sha((ROOT/'tools/audit_batch500_019_inputs.py').read_bytes()),rom_written=False,compiler_preflight=False,release_eligible=False,limits='TPL substitution audit only: exact500 ID/source/wording/layout/protected controls and unselected literal preservation. No TextPet binary roundtrip, native aggregate product gate, cumulative carry proof or runtime admission.'))
    print('PASS protected500 inputs,',len(reports),'archives,',len(layouts),'word-preserving layouts; compiler/ROM still pending')

if __name__=='__main__':main()
