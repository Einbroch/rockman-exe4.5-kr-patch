"""Analysis-only complete038 payloads with current037 script carry preserved.

These derivatives are NOT primary-build inputs: that build must regenerate
the parent from immutable source/adopted assets and verify the same boundary.
"""
import re
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read,frozen_write
from prepare_source500_038_v5 import BASE,BASE_SHA,OUT as SOURCE,baseline
from prepare_repartition500 import layout_records
from canonical_literals_031 import canonical_literals
from survey_aggregate_pet_033 import replace_exact
from tpl_literals import literals,skeleton
from archive_scripts import verify_untouched_scripts,script_spans
from textpet_korean import command

OUT='analysis/pending_insertion_500_038_carry_v2'

def ref(path):return dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()))

def main():
    cfg,source,rom,m=baseline();s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v1.json')
    require_hash(ROOT/v['selection']['path'],v['selection']['sha256'])
    if not v['passed'] or v['units']!=500 or v['rom_written']:raise ValueError('038 strict source compile prerequisite')
    out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);common=command(ROOT/SOURCE/'compile_v1/plugins')
    owners=defaultdict(list)
    for r in layout_records(m):owners[r['archive']].append(r)
    groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    records=[];seen=set();inherited=set()
    for r in v['archives']:
        arc=r['archive'];count=r['script_count'];gs=groups[arc];new_scripts={g['script'] for g in gs};new_ids={u['id'] for u in r['units']};current=owners.get(arc,[])
        for k in ('source_tpl','compiled','target_tpl'):require_hash(ROOT/r[k]['path'],r[k]['sha256'])
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');f=out/arc;f.mkdir();candidate=f/(arc+'.msg')
        if not current:
            # New owner: the already verified complete source target is enough.
            candidate.write_bytes((ROOT/r['compiled']['path']).read_bytes());kept=r['unselected_scripts'];carry=[];parent=None
        else:
            if len(current)!=1:raise ValueError('038 multiple current consumers need separate carry ownership '+arc)
            parent=current[0];before=rom[parent['rom_offset']:parent['rom_offset']+parent['compiled_bytes']]
            if sha(before)!=parent['compiled_sha256']:raise ValueError('037 complete parent identity')
            native=(ROOT/SOURCE/'compile_v1'/arc/(arc+'_native.msg')).read_bytes()
            if any(script_spans(before,count)[k]!=script_spans(native,count)[k] for k in new_scripts):raise ValueError('Selected new scripts were not untouched in current037')
            parent_dir=f/'parent';parent_dir.mkdir();bp=parent_dir/(arc+'.msg');bp.write_bytes(before);pt=f/'current037.tpl';rebuilt=f/(arc+'_current037_rebuilt.msg')
            def convert(a,af,b,bf,log):run_textpet(common+['Read-Text-Archives',str(a),'--format',af,'Write-Text-Archives',str(b),'--format',bf],f/log)
            convert(bp,'bin',pt,'tpl','parent-read.log');convert(pt,'tpl',rebuilt,'bin','parent-rebuild.log')
            parent_text=pt.read_text(encoding='utf-8-sig')
            if rebuilt.read_bytes()!=before or skeleton(parent_text)!=skeleton(original):raise ValueError('037 parent exact binary/control roundtrip '+arc)
            raw={u.key:u.text for u in literals(original)};old={u.key:u.text for u in literals(parent_text)}
            if old.keys()!=raw.keys() or any(old[k]!=raw[k] for k in new_ids):raise ValueError('038 literal identity/source for new entries')
            carried_ids={u['id'] for u in parent['layout']};carry=[dict(id=k,translation=old[k],authority='Read-only derivative of exact037 compiled owner; not independent wording authority') for k in sorted(carried_ids)]
            target=replace_exact(parent_text,{u['id']:u['translation'] for u in r['units']});tp=f/'target.tpl';tp.write_text(canonical_literals(target),encoding='utf8',newline='\n')
            convert(tp,'tpl',candidate,'bin','compile.log');reverse=f/'reverse.tpl';again=f/(arc+'_rebuilt.msg');convert(candidate,'bin',reverse,'tpl','reverse.log');convert(reverse,'tpl',again,'bin','rebuild.log')
            exported=reverse.read_text(encoding='utf-8-sig')
            if again.read_bytes()!=candidate.read_bytes() or skeleton(exported)!=skeleton(original) or [(u.key,u.language,u.text) for u in literals(exported)]!=[(u.key,u.language,u.text) for u in literals(target)]:raise ValueError('038 carry semantic/control/binary roundtrip')
            kept=verify_untouched_scripts(before,candidate.read_bytes(),count,new_scripts)
            current_spans=script_spans(candidate.read_bytes(),count);new_spans=script_spans((ROOT/r['compiled']['path']).read_bytes(),count)
            if any(current_spans[k]!=new_spans[k] for k in new_scripts):raise ValueError('038 selected script differs from strict source compilation')
            inherited|=carried_ids
        payload=candidate.read_bytes()
        if len(payload)>65535 or new_ids&seen:raise ValueError('038 carry capacity/disjoint IDs')
        seen|=new_ids
        records.append(dict(archive=arc,compiled=ref(candidate),compiled_bytes=len(payload),script_count=count,new_ids=sorted(new_ids),new_scripts=sorted(new_scripts),inherited_IDs=[x['id'] for x in carry],inherited_translation_derivative=carry,parent_record=parent,parent_unselected_script_bytes_preserved=kept,product_admitted=False,source_class=gs[0]['source_class'],source_lookup_candidates=gs[0]['source_lookup_candidates']))
        print('PASS038 carry',arc,'new',len(new_ids),'inherited',len(carry),flush=True)
    if len(seen)!=500 or seen!=set(s['selected_ids']) or inherited&seen:raise ValueError('038 complete500 carry denominator')
    frozen_write(out/'verification_v1.json',dict(passed=True,scope=__doc__,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),new_units=500,inherited_IDs_unchanged=len(inherited),archives=records,source_selection=ref(ROOT/SOURCE/'selection.json'),source_compile=ref(ROOT/SOURCE/'verification_v1.json'),dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/compile_carry038_v2.py','tools/archive_scripts.py','tools/tpl_literals.py','tools/survey_aggregate_pet_033.py','tools/canonical_literals_031.py']},rom_written=False,new_units_applied=0,product_admitted=False,release_eligible=False,limits=['Analysis derivatives only. Primary immutable-source build must regenerate037 parent and reconstruct these same complete payloads, never patch a previous ROM as build source.','New navi-hint root/source scene applicability and native store/Navi-tail continuations, selector alias guard/CPU/product integration/runtime remain unresolved.','No ROM or distribution package produced.']))
    print('PASS038 complete500 carry analysis, inherited',len(inherited),'IDs unchanged; NO ROM')

if __name__=='__main__':main()
