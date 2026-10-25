"""Independent partial500 parent/carry/scope audit; never applies a ROM."""
from copy import deepcopy
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from archive_scripts import script_spans,verify_untouched_scripts
from build_development_patch import literal_scope
from tpl_literals import literals,skeleton
from prepare_exact500_034 import OUT as SELECTION
from inspect_remaining_034 import BASE,BASE_SHA


def main():
    boundary_path='analysis/pending_insertion_500_034_list_formatter_cpu_v2/cpu.json'
    boundary=read(boundary_path)
    if not boundary['passed'] or boundary['baseline_sha256']!=BASE_SHA or boundary['case_count']!=10512:raise ValueError('034 full-two-byte native list boundary')
    require_hash(ROOT/'tools/bench_profile_list_formatter_034_v2.py',boundary['tool_sha256'])
    if any(max(r['max_initialized_page_bytes'])>128 for r in boundary['results']):raise ValueError('034 list initialized page exceeds native slot')
    cp='analysis/pending_insertion_500_034_compile500_v1/verification.json';mp='analysis/pending_insertion_500_034_carry500_v1/preflight.json'
    selection=read(SELECTION);compiled=read(cp);carry=read(mp);require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();meta=read(BASE.replace('.gba','.json'))
    for report in (selection,compiled,carry):
        if report['baseline_sha256']!=BASE_SHA or report['rom_written']:raise ValueError('034 current baseline/source-only claim')
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    if not compiled['passed'] or not carry['passed'] or compiled['units']!=500 or carry['new_units']!=500:raise ValueError('034 current partial population')
    if set(selection['selected_ids'])!={k for r in carry['archives'] for k in r['new_ids']}:raise ValueError('034 exact selected carry IDs')
    old={r['archive']:r for r in meta['archives']};source_records={r['archive']:r for r in compiled['archives']};parent_proofs=[];refusals=[];old_total=0;mixed_scripts=[];punctuation=[]
    def equal_parent(actual,expected):
        if actual!=expected:raise ValueError('034 locked parent script identity')
    for rec in carry['archives']:
        arc=rec['archive'];prior=old[arc];count=rec['script_count'];sr=source_records[arc];groups=[g for g in selection['groups'] if g['archive']==arc]
        actual=rom[prior['rom_offset']:prior['rom_offset']+prior['compiled_bytes']]
        for key in ('carry_compiled','compiled','merged_asset','merged_tpl'):require_hash(ROOT/rec[key]['path'],rec[key]['sha256'])
        parent=(ROOT/rec['carry_compiled']['path']).read_bytes();target=(ROOT/rec['compiled']['path']).read_bytes()
        if parent!=actual or sha(parent)!=prior['compiled_sha256']:raise ValueError('034 complete carry reconstructed equality')
        if verify_untouched_scripts(parent,target,count,set(rec['new_scripts']))!=rec['unselected_parent_scripts']:raise ValueError('034 unselected script identity')
        asset=read(rec['merged_asset']['path']);oldasset=read(rec['parent']['path']);before={u['id']:u for u in oldasset['units']};after={u['id']:u for u in asset['units']}
        oldmetrics={u['id']:u for u in prior['layout']};newmetrics={u['id']:u for u in rec['layout']}
        for key,u in before.items():
            if after[key]!=u or newmetrics[key]!=oldmetrics[key]:raise ValueError('034 old rich literal/metrics changed')
            for field in ('consumer','literal_language','max_literal_rows','max_line_advance'):
                if literal_scope(rec['parent_scope'],key).get(field)!=literal_scope(rec['scope'],key).get(field):raise ValueError('034 old effective scope changed')
        old_total+=len(before)
        original=(ROOT/sr['source_tpl']['path']).read_text(encoding='utf-8-sig');tpl=(ROOT/rec['merged_tpl']['path']).read_text(encoding='utf-8-sig')
        if skeleton(original)!=skeleton(tpl):raise ValueError('034 cumulative source controls')
        final_literals={u.key:u.text for u in literals(tpl)}
        if any(final_literals[k]!=u['translation'] for k,u in after.items()):raise ValueError('034 actual cumulative literal selection')
        parent_path=(ROOT/sr['compiled']['path']).parent/(arc+'_parent.msg');reconstructed=script_spans(parent_path.read_bytes(),count);live=script_spans(actual,count)
        for g in groups:
            script=g['script'];equal_parent(reconstructed[script],live[script])
            parent_proofs.append(dict(archive=arc,script=script,bytes=len(live[script]),sha256=sha(live[script]),reconstructed_parent_binary=dict(path=str(parent_path.relative_to(ROOT)),sha256=sha(parent_path.read_bytes()))))
            if g['locked_parent_units']:mixed_scripts.append(dict(archive=arc,script=script,locked_ids=[u['id'] for u in g['locked_parent_units']],new_ids=g['ids']))
            for where in (0,len(live[script])//2,len(live[script])-1):
                bad=bytearray(reconstructed[script]);bad[where]^=1
                try:equal_parent(bytes(bad),live[script])
                except ValueError:refusals.append(dict(kind='changed-parent-script-byte',archive=arc,script=script,offset=where))
                else:raise ValueError('034 changed parent accepted')
        test=deepcopy(rec['scope']);script=groups[0]['script'];key=groups[0]['ids'][0]
        profile={k:v for k,v in literal_scope(rec['scope'],key).items() if k in {'consumer','literal_language','max_literal_rows','max_line_advance'}};profile['scripts']=[script]
        test['literal_profiles']=test.get('literal_profiles',[])+[deepcopy(profile),deepcopy(profile)]
        try:literal_scope(test,key)
        except ValueError:refusals.append(dict(kind='overlapping-script-profiles',archive=arc,script=script))
        else:raise ValueError('034 duplicate script profiles accepted')
        punctuation.extend(k for k in rec['new_ids'] if not any(c.isalnum() for c in after[k]['source']))
    if old_total!=carry['carry_units_in_changed_archives'] or len(parent_proofs)!=243 or len(mixed_scripts)!=7 or len(punctuation)!=18:raise ValueError('034 audit finite population')
    deps=[SELECTION,cp,mp,'tools/verify_exact500_preflight_034.py','analysis/pending_insertion_500_034_query_models_v1/result.json','analysis/pending_insertion_500_034_query_controls_cpu_v1/cpu.json',boundary_path]
    frozen_write(ROOT/'analysis/pending_insertion_500_034_preflight500_v1/verification.json',dict(schema=1,passed=True,status='EXACT500_PARENT_AND_CUMULATIVE_SOURCE_PREFLIGHT_NOT500_NOT_ROM_ADMISSION',
        baseline_rom=BASE,baseline_sha256=BASE_SHA,current_rom_units=meta['translated_units'],prepared_new_literal_units=500,prose_or_label_units=482,punctuation_only_units=18,punctuation_ids=punctuation,
        requested_rom_cohort=500,additional_literal_units_needed=0,archives=len(carry['archives']),carry_units_retained=old_total,parent_script_proofs=parent_proofs,mixed_scripts=mixed_scripts,
        locked_prior_literal_count=sum(len(g['locked_ids']) for g in mixed_scripts),controlled_refusals=len(refusals),refusal_fixtures=refusals,
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,insertion_ready=False,runtime_tested=False,release_eligible=False,
        limits='500 canonical literal IDs, including18 separately timed punctuation literals, not500 independent prose translations or a500 cohort. Native source/current033 script bytes and all affected prior units/scopes/metrics retained. Exact500 product input gates, primary preallocation, wholewrite/repro and own-ROM runtime remain required; no new ROM or package.'))
    print('PASS034 partial500 source/carry',old_total,'retained;',len(parent_proofs),'parent scripts;',len(mixed_scripts),'mixed/',sum(len(g['locked_ids']) for g in mixed_scripts),'locked units;',len(refusals),'refusals;NO ROM')


if __name__=='__main__':main()




