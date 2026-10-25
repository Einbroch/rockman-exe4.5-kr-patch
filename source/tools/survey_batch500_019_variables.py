"""Read-only nickname/template investigation on the exact018 baseline.

Not consumer admission: dynamic native values, compilation, cumulative writer
registration and runtime aggregate checks remain separate unresolved gates.
"""
import argparse,re
from dataclasses import replace
from collections import defaultdict,Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals
from survey_batch500_017_layout import advance,protected_edges
SURVEY='analysis/pending_insertion_500_019_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_019_variable_survey_v1/survey.json'
ARGS='\t\tcapitalizeFirst = false\n\t\tcapitalizeAll = false\n\t\tprintN = false\n'
INVARIANT_SUFFIXES=frozenset(('의','도','님의','님은','님이','님께',' 님의',' 님은',' 님이',' 님께'))

def inspect_template(section,items,units,native_bound=None,invariant_suffixes=False):
    commands=re.findall(r'^\t(print\w+)\b',section,re.M)
    if commands!=['printPlayerNickname']:return None,'other_or_multiple_variables'
    call=re.search(r'^\tprintPlayerNickname\n((?:\t\t[^\n]+\n)*)',section,re.M)
    if not call or call.group(1)!=ARGS:return None,'nickname_arguments'
    resets=list(re.finditer(r'^\t(?:msgOpen(?:Quick)?|clearMsg)\s*$',section[:call.start()],re.M))
    if not resets:return None,'page_initialization'
    prefixes=[i for i in items if resets[-1].end()<i.start<call.start()]
    if len(prefixes)>1:return None,'composite_prefix'
    after=[i for i in items if i.start>=call.end()]
    if not after:return None,'missing_suffix'
    suffix=after[0]
    if section[call.end():suffix.start].strip():return None,'intervening_commands'
    if suffix.key not in units:return None,'unselected_suffix'
    target=units[suffix.key]['translation'];first=target.split('\n')[0];source_first=suffix.text.split('\n')[0]
    punctuation=bool(re.fullmatch(r'[、,!！?？ .…~]*',first))
    invariant=invariant_suffixes and native_bound is not None and first in INVARIANT_SUFFIXES
    if not punctuation and not invariant:return None,'particle_or_word_suffix_requires_context'
    if '\n' not in target:return None,'suffix_row_or_static_growth'
    if native_bound is None:
        if advance(first)>advance(source_first):return None,'suffix_row_or_static_growth'
    elif native_bound+advance(first)>132:return None,'nickname_aggregate_width'
    prefix=prefixes[0] if prefixes else None
    prefix_text=units[prefix.key]['translation'] if prefix and prefix.key in units else prefix.text if prefix else ''
    if prefix and not (prefix.text.endswith('\n') and prefix_text.endswith('\n')):return None,'same_row_prefix_requires_full_model'
    rows=prefix_text.count('\n')+target.count('\n')+1
    if rows>3:return None,'aggregate_rows'
    for item in items:
        if item.key in units and not protected_edges(item.text,units[item.key]['translation']):return None,'protected_edge_or_padding'
    return dict(suffix_id=suffix.key,source_first_line=source_first,first_line=first,source_static_advance=advance(source_first),target_static_advance=advance(first),prefix_id=prefix.key if prefix else None,aggregate_rows=rows,nickname_column_zero=True,native_variable_unchanged=True,**(dict(invariant_suffix=True,semantic_approval=False) if invariant else {}),**(dict(conditional_native_advance=native_bound,conditional_first_row_advance=native_bound+advance(first)) if native_bound is not None else {})),None

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--bounded-native-cpu');parser.add_argument('--native-runtime');parser.add_argument('--out');parser.add_argument('--invariant-suffixes',action='store_true');args=parser.parse_args()
    if bool(args.bounded_native_cpu)!=bool(args.native_runtime) or bool(args.out)!=bool(args.bounded_native_cpu):raise ValueError('Separate evidence and output required for conditional survey')
    if args.invariant_suffixes and not args.bounded_native_cpu:raise ValueError('Invariant suffix survey requires bounded native evidence')
    s=read(SURVEY);require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256'])
    bound=None;dependencies={}
    if args.bounded_native_cpu:
        cpu=read(args.bounded_native_cpu);runtime=read(args.native_runtime)
        if cpu['status']!='BOUNDED_CPU_ANALYSIS_NOT_INSERTION_APPROVAL' or runtime['status']!='NORMAL_NATIVE_NAME_BOUNDARY_RUNTIME_VERIFIED_NOT_HANGUL_INPUT' or any(r['rom_sha256']!=s['baseline_sha256'] for r in (cpu,runtime)):raise ValueError('Native evidence baseline/scope')
        require_hash(ROOT/'tools/analyze_nickname_native_019.py',cpu['tool_sha256'])
        for name,digest in runtime['tools'].items():require_hash(ROOT/'tools'/name,digest)
        if runtime['native_E406_renderer_index']!=234 or not all(runtime[k] for k in ('sixth_accepted','seventh_rejected','delete_reinsert_verified')):raise ValueError('Native boundary evidence')
        bound=cpu['conditional_native_bound']['owner_six_glyphs_plus_suffix']
        if bound!=6*cpu['conditional_native_bound']['max_glyph_advance']+cpu['conditional_native_bound']['max_suffix_advance']:raise ValueError('Native width derivation')
        dependencies={path:sha((ROOT/path).read_bytes()) for path in (args.bounded_native_cpu,args.native_runtime)}
    proof=read('analysis/pending500_018_v1/integration.json')
    if not proof['passed'] or proof['rom_sha256']!=s['baseline_sha256'] or s['pinned_changed_inputs']:raise ValueError('Verified baseline/pinned corpus')
    require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256']);coverage=read(s['pinned_coverage']['path']);pool=defaultdict(list)
    for path,digest in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/path,digest)
        for u in read(path)['units']:pool[u['id']].append((path,digest,u))
    candidates=[];rejected=[];types=Counter();tpls={}
    for g in s['unresolved_groups']:
        if g['reasons']!=['variable_insertion']:continue
        arc=g['archive'];ref=read(pool[g['ids'][0]][0][0])['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256'])
        tpl=tpls.setdefault(arc,(ROOT/ref['path']).read_text(encoding='utf-8-sig'))
        section=re.search(r'^script '+str(g['script'])+r'\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M).group()
        types.update([tuple(re.findall(r'^\t(print\w+)\b',section,re.M))]);us={};refs=[]
        for key in g['ids']:
            options=pool[key]
            if len({(u['source'],u['translation'],u['state']) for _,_,u in options})!=1:raise ValueError('Conflicting pinned wording '+key)
            path,digest,u=options[0];us[key]=u;refs.append(dict(id=key,path=path,sha256=digest))
        items=literals('@archive '+arc+'\n'+section)
        if any(us[i.key]['source']!=i.text for i in items if i.key in us):raise ValueError('Protected source identity')
        header=len('@archive '+arc+'\n')
        model,reason=inspect_template(section,[replace(i,start=i.start-header,end=i.end-header) for i in items],us,bound,args.invariant_suffixes)
        if reason:rejected.append(dict(archive=arc,script=g['script'],ids=g['ids'],reason=reason));continue
        candidates.append(dict(archive=arc,script=g['script'],units=len(g['ids']),ids=g['ids'],drafts=refs,source_tpl=ref,template=model))
    result=dict(schema=1,baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=s['source_sha256'],survey=dict(path=SURVEY,sha256=sha((ROOT/SURVEY).read_bytes())),variable_only_groups=sum(types.values()),variable_only_units=sum(len(g['ids']) for g in s['unresolved_groups'] if g['reasons']==['variable_insertion']),command_populations=[dict(commands=list(k),groups=v) for k,v in types.most_common()],nickname_template_candidates=candidates,candidate_units=sum(g['units'] for g in candidates),rejections=rejected,rejection_group_counts=dict(Counter(g['reason'] for g in rejected)),rom_written=False,prose_changed=False,release_eligible=False,limits='Structural non-growing punctuation/column-zero nickname investigation only. Not full remaining population, native value capacity proof, consumer admission, build readiness, semantic approval, or runtime evidence. All other survey rejection reasons remain unresolved.')
    if bound is not None:
        result.update(native_evidence=dependencies,conditional_native_advance=bound,limits='Conditional native-six-glyph plus suffix0..41 width survey; punctuation/column-zero template only. Not consumer admission, source-only compilation, cumulative build readiness, all-name/save proof, comma-page runtime, semantic approval, or new ROM. Other rejection reasons remain unresolved.')
        if args.invariant_suffixes:
            result.update(invariant_suffix_forms=sorted(INVARIANT_SUFFIXES),limits='Conditional native-six-glyph/column-zero/punctuation or explicit invariant suffix structure survey. No prose edit or semantic/human approval; needs_review development input only. Not consumer admission, compilation, cumulative build readiness, all-name/save proof, new-page runtime, or new ROM. Other rejection reasons remain unresolved.')
    frozen_write(ROOT/(args.out or OUT),result);print('Variable-only',result['variable_only_groups'],result['variable_only_units'],'nickname template candidates',len(candidates),result['candidate_units']);print(result['rejection_group_counts'])
if __name__=='__main__':main()
