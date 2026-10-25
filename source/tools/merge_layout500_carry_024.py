"""Reconstruct023 carry from pinned source inputs and merge exact024500.

Analysis/preflight only: actual023 bytes are a comparison oracle, never the
source of the merged payload. No existing build gate, ROM or package is edited.
"""
import re
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read,frozen_write,entries,PROFILE022
from build_development_patch import selected_scope,literal_scope,translate_literal_scope,validate_characters,validate_literal_numerals
from tpl_literals import literals,skeleton,resolve_units
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES
from compile_layout_candidates_024 import canonical_literals,ref
from survey_pet_quick_reflow_024 import replace_for_analysis
from prepare_layout500_024 import OUT as SELECTION

OUT='analysis/pending_insertion_500_024_carry_v1'


def registry(source,meta):
    """Replay the adopted scope derivation, not a new registry discovery."""
    path='tools/specs/exe45_dialogue_archives_v1.json'
    require_hash(ROOT/path,meta['archive_registry_sha256'])
    for name in ('cumulative_batch500.py','build_development_patch.py','hint_rom_data.py','textpet_korean.py'):
        require_hash(ROOT/'tools'/name,meta['build_tools_sha256'][name])
    reg=deepcopy(read(path)['archives'])
    from batch500_002_rom import entries as e2
    from batch500_003_rom import entries as e3
    from batch500_004_rom import entries as e4
    from batch500_005_rom import entries as e5
    from batch500_006_rom import entries as e6
    for derive in (e2,e3,e4,e5,e6):
        reg.update({a['archive']:s for _,_,a,s,_,_ in derive(source) if s['standard_relocation']})
    for profile in PROFILE022['prior_cumulative']+(PROFILE022,):
        result=entries(source,profile,_prior_registry=reg)
        reg.update({a['archive']:s for _,_,a,s,_,_ in result})
        print('Reconstructed carry scope',profile['out'],flush=True)
    return reg


def main():
    selection=read(SELECTION);mechanical_path='analysis/pending_insertion_500_024_compile500_v1/verification.json';compiled=read(mechanical_path)
    for p,h in selection['dependencies'].items():require_hash(ROOT/p,h)
    for p,h in compiled['dependencies'].items():require_hash(ROOT/p,h)
    if not compiled['passed'] or compiled['rom_written'] or compiled['units']!=500 or compiled['selection']['sha256']!=sha((ROOT/SELECTION).read_bytes()):raise ValueError('Source-only500 binding')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,selection['source_sha256']);source=sp.read_bytes()
    rp=ROOT/selection['baseline_rom'];require_hash(rp,selection['baseline_sha256']);base=rp.read_bytes();meta=read(rp.with_suffix('.json'))
    reg=registry(source,meta)
    from hint_rom_data import input_entries
    hint_inputs={a['archive']:(path,row,a,scope) for path,row,a,scope,_,_,_ in input_entries(source)}
    hints={r['archive']:r for r in meta['keyitem_rom']['hint_archives']};primary={r['archive']:r for r in meta['archives']}
    out=ROOT/OUT;out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins')
    new_by={r['archive']:r for r in compiled['archives']};groups=defaultdict(list)
    for g in selection['groups']:groups[g['archive']].append(g)
    records=[];all_new=set();old_total=0
    for arc,gs in sorted(groups.items()):
        new=new_by[arc];src_ref=new['source_tpl'];require_hash(ROOT/src_ref['path'],src_ref['sha256']);original=(ROOT/src_ref['path']).read_text(encoding='utf-8-sig');row=gs[0]['source_row'];native=payload_of(source,row);count=new['script_count']
        if sha(native)!=new['source_sha256']:raise ValueError('Immutable source payload')
        old=primary.get(arc) or hints.get(arc);parent=None;carry=[]
        if arc in hints:
            path,oldrow,a,scope=hint_inputs[arc];parent=dict(path=path,sha256=old['asset_sha256']);require_hash(ROOT/path,parent['sha256']);carry=resolve_units(a)
            if oldrow!=row or old['asset_path']!=path:raise ValueError('A3 carry input identity')
        elif arc in primary:
            owners=[r for r in meta['translation_assets'] if r.get('archive')==arc and not r.get('scope','').startswith('read-only inherited')]
            if len(owners)!=1:raise ValueError('Primary carry owner '+arc)
            parent=owners[0];require_hash(ROOT/parent['path'],parent['sha256']);a=read(parent['path']);scope=selected_scope(reg[arc],a);carry=resolve_units(a)
        else:
            if arc not in ('693590','778CC0'):raise ValueError('Undeclared new raw archive')
            scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=[],literal_ids=[],script_count=count,max_literal_rows=3,max_line_advance=132,preserve_literal_numerals=True,source_bytes=row['size'],pointers=row['pointers'],compressed=False,standard_relocation=True)
        old_ids={u['id'] for u in carry};new_units=new['units'];new_ids={u['id'] for u in new_units};scripts={int(k.split(':')[1]) for k in new_ids};old_scripts={int(k.split(':')[1]) for k in old_ids}
        if old_ids&new_ids or old_scripts&scripts or all_new&new_ids or old is not None and old_ids!={r['id'] for r in old['layout']}:raise ValueError('Distinct carry/new script populations')
        all_new|=new_ids;old_total+=len(carry)
        target_old=translate_literal_scope(original,carry,scope) if carry else original
        if skeleton(original)!=skeleton(target_old):raise ValueError('Carry changes source controls')
        folder=out/arc;folder.mkdir();old_tpl=folder/'carry.tpl';old_bin=folder/(arc+'_carry.msg');old_tpl.write_text(canonical_literals(target_old),encoding='utf-8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(old_tpl),'--format','tpl','Write-Text-Archives',str(old_bin),'--format','bin'],folder/'carry-compile.log');old_payload=old_bin.read_bytes()
        expected=base[old['rom_offset']:old['rom_offset']+old['compiled_bytes']] if old else native
        if old_payload!=expected or old is not None and sha(old_payload)!=old['compiled_sha256']:raise ValueError('Reconstructed carry differs from actual023 '+arc)
        merged_scope=deepcopy(scope);merged_scope['literal_scripts']=sorted(old_scripts|scripts);merged_scope['literal_ids']=[u['id'] for u in carry+new_units];merged_scope['complete_literal_scope']=False
        additions=[]
        for g in gs:
            additions.append(dict(scripts=[g['script']],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=132 if g['profile'] in ('quick-within-page-lf-proposal','pet-flags-within-page-lf-proposal') else 180))
        merged_scope['literal_profiles']=deepcopy(scope.get('literal_profiles',[]))+additions
        for key in old_ids:
            before,after=literal_scope(scope,key),literal_scope(merged_scope,key)
            if any(before.get(k)!=after.get(k) for k in ('consumer','literal_language','max_literal_rows','max_line_advance')):raise ValueError('Carry consumer contract changed')
        validate_literal_numerals(new_units,dict(preserve_literal_numerals=True))
        target=replace_for_analysis(target_old,new_units);merged_tpl=folder/'merged.tpl';binary=folder/(arc+'.msg');reverse=folder/'reverse.tpl';rebuilt=folder/(arc+'_rebuilt.msg');merged_tpl.write_text(canonical_literals(target),encoding='utf-8',newline='\n')
        layout=validate_characters(target,out/'plugins'/'exe45-utf8.tbl',merged_scope,old_ids|new_ids)
        old_layout={r['id']:r for r in old.get('layout',[])} if old else {}
        for r in layout:
            if r['id'] in old_ids and r['line_advance_pixels']!=old_layout[r['id']]['line_advance_pixels']:raise ValueError('Carry display metrics changed')
        run_textpet(common+['Read-Text-Archives',str(merged_tpl),'--format','tpl','Write-Text-Archives',str(binary),'--format','bin'],folder/'merge-compile.log');payload=binary.read_bytes()
        if len(payload)>65535:raise ValueError('Merged16bit offsets')
        kept=verify_untouched_scripts(old_payload,payload,count,scripts)
        run_textpet(common+['Read-Text-Archives',str(binary),'--format','bin','Write-Text-Archives',str(reverse),'--format','tpl'],folder/'reverse.log')
        run_textpet(common+['Read-Text-Archives',str(reverse),'--format','tpl','Write-Text-Archives',str(rebuilt),'--format','bin'],folder/'rebuild.log');exported=reverse.read_text(encoding='utf-8-sig')
        if skeleton(original)!=skeleton(exported) or [(i.key,i.language,i.text) for i in literals(target)]!=[(i.key,i.language,i.text) for i in literals(exported)] or rebuilt.read_bytes()!=payload:raise ValueError('Merged controls/literal/binary roundtrip')
        projected=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=arc,source_sha256=sha(source),source_tpl=src_ref,source_archive_sha256=sha(native),consumer='normal-dialogue',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=carry+new_units,cumulative_merge=dict(parent=parent,selection=ref(ROOT/SELECTION),new_ids=sorted(new_ids)),insertion_ready=False)
        asset=folder/(arc+'_merged_asset.json');frozen_write(asset,projected)
        # Preserve prior richer aggregate metadata, not just the measured width.
        merged_layout=[deepcopy(old_layout[r['id']]) if r['id'] in old_layout else r for r in layout]
        records.append(dict(archive=arc,source_row=row,source_payload_sha256=sha(native),script_count=count,storage='A3-clone-merge' if arc in hints else 'new-raw' if old is None else 'raw-carry',parent=parent,parent_scope=scope,scope=merged_scope,parent_compiled_sha256=sha(old_payload),carry_compiled=ref(old_bin),carry_units=len(carry),new_units=len(new_units),new_ids=sorted(new_ids),new_scripts=sorted(scripts),merged_asset=ref(asset),compiled=ref(binary),merged_tpl=ref(merged_tpl),compiled_bytes=len(payload),layout=merged_layout,unselected_parent_scripts=kept,carry_reconstructed_from_source_and_assets=True,carry_consumer_contracts_preserved=True,old_record=old,product_admitted=False))
        print('PASS carry merge',arc,'kept',len(carry),'new',len(new_units),flush=True)
    if len(all_new)!=500 or all_new!=set(selection['selected_ids']):raise ValueError('Actual500 carry delta')
    deps=[SELECTION,mechanical_path,'tools/merge_layout500_carry_024.py','tools/cumulative_batch500.py','tools/build_development_patch.py','tools/hint_rom_data.py','tools/tpl_literals.py']
    frozen_write(out/'preflight.json',dict(schema=1,status='EXACT500_CUMULATIVE_CARRY_COMPILE_NOT_ROM_ADMISSION',passed=True,source_sha256=sha(source),baseline_rom=selection['baseline_rom'],baseline_sha256=sha(base),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},new_units=500,carry_units_in_changed_archives=old_total,archives=records,plugin=plugin,all_carry_payloads_reconstructed_from_immutable_source_and_pinned_assets=True,all_nonnew_parent_scripts_byte_identical=True,all_carry_consumer_contracts_preserved=True,rom_written=False,insertion_ready=False,runtime_tested=False,release_eligible=False,limits='Merged message payloads only, reconstructed from immutable source and pinned wording/scope.023 ROM was only a byte comparison reference. Primary source-bound024/LF/normal/conditional gates and raw/A3 allocation/ExpectedWrites, all other clones, independent product/repro and actual024 GBA verification remain required. Existing old preflights and build code were not modified.'))
    print('PASS cumulative source carry',old_total,'retained +500 new;',len(records),'archives;NO ROM written')


if __name__=='__main__':main()
