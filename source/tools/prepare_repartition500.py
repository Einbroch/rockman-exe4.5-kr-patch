"""Repartition prepared340 plus160 complete raw dialogue drafts; no prose/ROM writes."""
import json,re
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import parse_tpi
from tpl_literals import literals
from korean_codec import EXTRA_CHARACTER_INDICES

BASE='poc/output/exe45_ko_development_pending500_arrow_v2.gba'
OUT='analysis/pending_insertion_500_002_repartition_v1'
TARGET=160
TOTAL_UNITS=500
EXCLUDE=set()
ALLOW_PARTIAL=False

def layout_records(tree):
    """All declared compiled consumers, including supplemental ROM clones."""
    if isinstance(tree,dict):
        if {'archive','compiled_sha256','layout','translated_units'}<=tree.keys():yield tree
        for value in tree.values():yield from layout_records(value)
    elif isinstance(tree,list):
        for value in tree:yield from layout_records(value)


def main():
    out=ROOT/OUT
    if out.exists():raise ValueError('Preserve previous selection')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source_path=ROOT/cfg['source_profile']['filename'];require_hash(source_path,cfg['source_profile']['sha256'])
    source=source_path.read_bytes()
    meta=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'));require_hash(ROOT/BASE,meta['output_sha256'])
    applied={r['archive'] for r in layout_records(meta)}
    applied_ids={x['id'] for r in layout_records(meta) for x in r['layout']}
    rows={r['offset']:r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    eligible=[]
    unmapped=[]
    # This is the existing encoding repertoire, not a substitution rule.
    native_chars={v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for _,v in [line.split('=',1)] if len(v)==1}
    seen=set()
    for path in sorted((ROOT/'translations').glob('*draft*json')):
        d=json.loads(path.read_text(encoding='utf8'))
        if 'archive' not in d or not d.get('units'):continue
        a=d['archive'];row=rows[int(a,16)]
        if a in applied and not ALLOW_PARTIAL or a in EXCLUDE or a in seen or row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0] or not 0x680000<=int(a,16)<0x800000:continue
        seen.add(a)
        require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
        tpl=(ROOT/d['source_tpl']['path']).read_text(encoding='utf-8-sig')
        scripts={int(x['id'].split(':')[1]) for x in d['units']}
        sections={int(m.group(1)):m.group() for m in re.finditer(r'^script\s+(\d+)\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)}
        originals={x.key:x for x in literals(tpl)}
        if d['source_sha256']!=sha(source) or d['review']['release_eligible'] is not False:raise ValueError('Draft source/policy')
        for s in sorted(scripts):
            if re.search(r'^\s*print\w+',sections[s],re.M):continue
            group=[u for u in d['units'] if int(u['id'].split(':')[1])==s]
            if any(u['id'] in applied_ids for u in group):continue
            valid=True
            for u in group:
                missing=sorted({ch for ch in u['translation'] if ch!='\n' and not '\uac00'<=ch<='\ud7a3' and ch not in native_chars and ch not in EXTRA_CHARACTER_INDICES})
                if missing:
                    unmapped.append(dict(id=u['id'],characters=missing,draft_path=str(path.relative_to(ROOT)),reason='Encoding extension required; source/draft preserved, no substitution'))
                    valid=False
                before=originals[u['id']]
                widths=[sum(12 if '\uac00'<=ch<='\ud7a3' or ch in EXTRA_CHARACTER_INDICES else 8 if ch==' ' else 11 for ch in line) for line in u['translation'].split('\n')]
                if before.language!='mmbn45' or before.text!=u['source'] or len(widths)>3 or max(widths)>132 or u['source'].count('\n')!=u['translation'].count('\n'):valid=False
            expected={x.key for x in originals.values() if int(x.key.split(':')[1])==s and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)}
            if not valid or expected!={x['id'] for x in group}:continue
            eligible.append(dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()),archive=a,units=len(group),scripts=[s],selected_ids=[u['id'] for u in group]))
    # Whole selected draft populations only. Prefer fewer archives, stable lexical tie-break.
    states={0:[]}
    for item in sorted(eligible,key=lambda x:(-x['units'],x['archive'])):
        for total,chosen in list(states.items()):
            n=total+item['units']
            if n<=TARGET and (n not in states or len(chosen)+1<len(states[n])):states[n]=chosen+[item]
    if TARGET not in states:
        out.mkdir(parents=True)
        failure=dict(source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=meta['output_sha256'],requested_units=TARGET,
            eligible_script_groups=len(eligible),eligible_units=sum(r['units'] for r in eligible),max_reachable_requested_subset=max(states),
            eligible_archives=eligible,deferred_unmapped_literals=unmapped,rom_written=False,release_eligible=False,
            reason='No complete requested population under untouched-archive/raw/no-variable/geometry comparison; existing partial archives need explicit merge.')
        (out/'selection_failure.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        raise ValueError('No complete requested population under raw/no-variable comparison')
    selected=[]
    for item in states[TARGET]:
        old=next((x for x in selected if x['archive']==item['archive']),None)
        if old is None:selected.append(dict(item))
        else:
            old['units']+=item['units'];old['scripts']+=item['scripts'];old['selected_ids']+=item['selected_ids']
    out.mkdir(parents=True)
    report=dict(schema=1,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=meta['output_sha256'],
        preserved_prepared_units=TOTAL_UNITS-TARGET,replacement_units=TARGET,total_new_units=TOTAL_UNITS,
        replacement_archives=selected,eligible_archives=eligible,
        prior_partial_archives_included=ALLOW_PARTIAL,
        requires_cumulative_merge=[r['archive'] for r in selected if r['archive'] in applied],
        deferred_unmapped_literals=unmapped,
        deferred_draft_paths=['translations/batch500_001_equipment_guts_draft_ko.json',
        'translations/batch500_001_equipment_fire_draft_ko.json','translations/batch500_001_equipment_proto_draft_ko.json',
        'translations/batch500_045_navi_mail_npcs_6A5578_draft_ko.json'],
        reason='Prioritize requested actual500 ROM insertion; retain gear153 and Navi7 for next batch with consumer integration. No wording/source change.',
        rom_written=False,release_eligible=False)
    (out/'selection.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Selected'+str(TARGET),[(x['archive'],x['units']) for x in selected])


if __name__=='__main__':main()
