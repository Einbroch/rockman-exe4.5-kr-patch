"""Survey a next500 scope from pinned draft-first inputs; never edits ROM/prose.

This expands analysis beyond the old680000 address filter, not beyond confirmed
raw storage/known pointer and normal-dialogue contracts. Candidates still need
source-only and cumulative preflight and exact-artifact runtime verification.
"""
import re
import argparse
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from tpl_literals import literals
from korean_codec import EXTRA_CHARACTER_INDICES
BASE='poc/output/exe45_ko_development_pending500_015_v1.gba'
OUT='analysis/pending_insertion_500_016_survey_v1/survey.json'
def main(base=BASE,out=OUT,proof_path='analysis/pending500_015_v1/integration.json'):
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    meta=read(base.replace('.gba','.json'));require_hash(ROOT/base,meta['output_sha256']);proof=read(proof_path)
    if not proof['passed'] or proof['rom_sha256']!=meta['output_sha256']:raise ValueError('Verified baseline required')
    coverage_path='analysis/translation_first_v1/coverage.json';coverage=read(coverage_path)
    if not coverage['passed'] or coverage['source_sha256']!=sha(source):raise ValueError('Draft-first source population')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={format(r['offset'],'X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    applied={u['id'] for r in layout_records(meta) for u in r['layout']};pool=defaultdict(list);assets={};changed=[]
    for path,digest in coverage['draft_asset_hashes'].items():
        if not (ROOT/path).exists() or sha((ROOT/path).read_bytes())!=digest:changed.append(dict(path=path,expected_sha256=digest));continue
        a=read(path)
        if 'archive' not in a or not a.get('units'):raise ValueError('Unexpected pinned draft boundary '+path)
        if a['source_sha256']!=sha(source) or a['review']['release_eligible'] is not False:raise ValueError('Draft policy/source')
        require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256']);native=payload_of(source,rows[a['archive']])
        if sha(native)!=a['source_archive_sha256']:raise ValueError('Actual native payload '+a['archive'])
        assets[path]=a
        for u in a['units']:pool[u['id']].append((path,digest,u))
    native_chars={v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for _,v in [line.split('=',1)] if len(v)==1}
    reasons=Counter();groups=[];details=[];seen=set();jp=re.compile(r'[\u3040-\u30ff\u3400-\u9fff]')
    for path,a in assets.items():
        tpl=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');native={u.key:u for u in literals(tpl)}
        sections={int(m.group(1)):m.group() for m in re.finditer(r'^script\s+(\d+)\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)}
        for s in sorted({int(u['id'].split(':')[1]) for u in a['units']}):
            identity=(a['archive'],s)
            if identity in seen:continue
            seen.add(identity);keys=sorted(k for k,u in native.items() if int(k.split(':')[1])==s and jp.search(u.text));why=[];row=rows[a['archive']];section=sections[s]
            if not keys:why.append('no_japanese_target')
            if any(k in applied for k in keys):why.append('script_has_applied_ids')
            if row['compressed'] or row['size_header']:why.append('different_storage_adapter')
            if not row['pointers'] or row['pointers']==[0]:why.append('unresolved_references')
            if any(native[k].language!='mmbn45' for k in keys):why.append('different_renderer')
            if re.search(r'^\s*print\w+',section,re.M):why.append('variable_insertion')
            if re.search(r'^\s*(option|select|positionOption\w*)\b',section,re.M):why.append('choice_layout')
            if not re.search(r'^\s*msgOpen(?:Quick)?\s*$',section,re.M):why.append('caller_window_context')
            refs=[];widths={}
            for key in keys:
                candidates=pool.get(key,[])
                if not candidates:why.append('missing_pinned_draft');continue
                signatures={(u['source'],u['translation'],u['state']) for _,_,u in candidates}
                if len(signatures)!=1:why.append('conflicting_wording');continue
                p,d,u=candidates[0]
                if u['source']!=native[key].text:raise ValueError('Extraction source identity '+key)
                if u['state']!='needs_review':why.append('unsupported_review_state')
                if u['source'].count('\n')!=u['translation'].count('\n'):why.append('line_topology')
                if any(c!='\n' and not '\uac00'<=c<='\ud7a3' and c not in native_chars and c not in EXTRA_CHARACTER_INDICES for c in u['translation']):why.append('glyph_encoding')
                w=[sum(12 if '\uac00'<=c<='\ud7a3' or c in EXTRA_CHARACTER_INDICES else 8 if c==' ' else 11 for c in line) for line in u['translation'].split('\n')];widths[key]=w
                if len(w)>3 or max(w)>132:why.append('adopted_normal_geometry')
                refs.append(dict(id=key,path=p,sha256=d))
            why=sorted(set(why))
            if why:
                reasons.update(why);details.append(dict(archive=a['archive'],script=s,ids=keys,reasons=why));continue
            groups.append(dict(archive=a['archive'],script=s,units=len(keys),ids=keys,drafts=refs,source_tpl=a['source_tpl'],source_archive_sha256=a['source_archive_sha256'],source_pointers=row['pointers'],source_bytes=row['size'],below_legacy_filter=int(a['archive'],16)<0x680000,adopted_normal_advances=widths))
    states={0:[]}
    for g in sorted(groups,key=lambda g:(g['archive'],g['script'])):
        for total,selected in list(states.items()):
            n=total+g['units']
            if n<=500 and n not in states:states[n]=selected+[g]
    result=dict(schema=1,source_sha256=sha(source),baseline_rom=base,baseline_sha256=meta['output_sha256'],pinned_coverage=dict(path=coverage_path,sha256=sha((ROOT/coverage_path).read_bytes())),requested_units=500,pinned_changed_inputs=changed,candidate_groups=len(groups),candidate_units=sum(g['units'] for g in groups),candidate_units_below_legacy_filter=sum(g['units'] for g in groups if g['below_legacy_filter']),rejection_group_counts=dict(reasons),selected500=states.get(500),max_reachable_requested_subset=max(states),candidates=groups,unresolved_groups=details,rom_written=False,prose_changed=False,release_eligible=False,limits='Finite pinned-draft survey, not full-game untranslated count or insertion readiness. No conflicting wording selected. Source-only/cumulative preflight, known consumer/registry admission and runtime checks remain required.')
    frozen_write(ROOT/out,result);print('Candidate groups',len(groups),'units',result['candidate_units'],'below legacy filter',result['candidate_units_below_legacy_filter'],'exact500',500 in states,'changed pinned inputs',len(changed));print('Rejected groups by overlapping reason',dict(reasons))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',default=BASE)
    parser.add_argument('--out',default=OUT)
    parser.add_argument('--proof',default='analysis/pending500_015_v1/integration.json')
    args=parser.parse_args();main(args.base,args.out,args.proof)
