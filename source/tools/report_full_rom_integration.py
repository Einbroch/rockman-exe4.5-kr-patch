"""Current full-translation/Hangul-input integration preflight, never a ROM.

Registered scope is not inferred from a draft's claimed consumer. Unknown
consumers remain unresolved. CPU fixtures are not installation specifications.
"""
import json,re
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,require_hash,sha
from prepare_translation_first import check_draft
from verify_tpi_index import parse_tpi
from build_development_patch import selected_scope,literal_scope
from korean_codec import EXTRA_CHARACTER_INDICES


def read(path):return json.loads(path.read_text(encoding='utf8'))


def covered(scope,key):
    if scope is None:return False
    if scope.get('literal_ids') is not None:return key in scope['literal_ids']
    return int(key.split(':')[1]) in scope.get('literal_scripts',[])


def main():
    plan_path=ROOT/'translations/full_translation_first_plan.json';plan=read(plan_path)
    cfg=read(ROOT/'project.json');src=ROOT/cfg['source_profile']['filename']
    require_hash(src,cfg['source_profile']['sha256']);rom=src.read_bytes()
    baseline=ROOT/plan['baseline_rom']['path'];require_hash(baseline,plan['baseline_rom']['sha256'])
    manifest_path=baseline.with_suffix('.json');manifest=read(manifest_path)
    if manifest['source_sha256']!=sha(rom) or manifest['output_sha256']!=sha(baseline.read_bytes()):raise ValueError('baseline identity')
    inventory=ROOT/plan['source_inventory']['path'];require_hash(inventory,plan['source_inventory']['sha256'])
    population=read(inventory);base={u['id']:u for u in population['units']}
    if len(base)!=len(population['units']):raise ValueError('duplicate source ID')
    regpath=ROOT/'tools/specs/exe45_dialogue_archives_v1.json';registry=read(regpath)
    require_hash(regpath,manifest['archive_registry_sha256'])
    if registry['source_sha256']!=sha(rom):raise ValueError('registry source')
    cat=ROOT/cfg['text_catalog']['path'];require_hash(cat,cfg['text_catalog']['sha256'])
    rows={f"{r['offset']:X}":r for r in parse_tpi(cat)}
    font=cfg['development_dependencies']['font'];require_hash(ROOT/font['path'],font['sha256'])
    available={int(line.split()[1]) for line in (ROOT/font['path']).read_text(encoding='utf8').splitlines() if line.startswith('ENCODING ')}
    scopes={};inputs={str(plan_path.relative_to(ROOT)):sha(plan_path.read_bytes()),
        str(regpath.relative_to(ROOT)):sha(regpath.read_bytes()),str(manifest_path.relative_to(ROOT)):sha(manifest_path.read_bytes())}
    for item in manifest['translation_assets']:
        path=ROOT/item['path'];require_hash(path,item['sha256']);inputs[item['path']]=item['sha256']
        # The manifest also lists inherited authorities and private clones.
        # Those do not override the active source archive's scope.
        if 'scope' in item or 'carry_units' in item:continue
        a=read(path)
        if a['archive'] in scopes:raise ValueError('duplicate baseline archive')
        scopes[a['archive']]=selected_scope(registry['archives'][a['archive']],a)
    unresolved=[];measured=[];drafts={};geometry=[];archives=set();count=Counter();by_archive=defaultdict(Counter)
    for name in plan['draft_assets']:
        path=ROOT/name;a=read(path);inputs[name]=sha(path.read_bytes());archive=a['archive'];archives.add(archive)
        geometry+=check_draft(a,base,available,rom,rows)
        for u in a['units']:
            key=u['id']
            if key in drafts:raise ValueError('duplicate selected draft ID')
            drafts[key]=name;scope=scopes.get(archive,registry['archives'].get(archive))
            if archive not in registry['archives']:reason='archive_not_registered'
            elif not covered(scope,key):reason='literal_outside_registered_scope'
            else:reason=None
            if reason:
                unresolved.append(dict(id=key,asset=name,reason=reason));count[reason]+=1;by_archive[archive][reason]+=1
                continue
            p=literal_scope(scope,key)
            # Same scalar advance model as the primary builder. This does not
            # validate concatenated variables/choices, decode bytes, or prove
            # runtime wrapping/clearing or reference completeness.
            widths=[sum(8 if p['consumer'].startswith('fixed-cell') or ch==' ' else 12 if '\uac00'<=ch<='\ud7a3' or ch in EXTRA_CHARACTER_INDICES else 11 for ch in line) for line in u['translation'].split('\n')]
            tokens=re.findall(r'\[[^\]]+\]',u['translation'])
            state='token_consumer_needs_validation' if tokens else 'scalar_layout_exceeds_registered_limit' if len(widths)>p['max_literal_rows'] or max(widths,default=0)>p['max_line_advance'] else 'scalar_layout_within_registered_limit'
            measured.append(dict(id=key,asset=name,consumer=p['consumer'],widths=widths,
                max_rows=p['max_literal_rows'],max_advance=p['max_line_advance'],state=state))
            count[state]+=1;by_archive[archive][state]+=1
    pending=[u['id'] for u in population['units'] if u['status']=='unselected_japanese' and u['id'] not in drafts]
    keyboard={}
    for name in ('cpu_latin_input','cpu_calendar_versioned_record','cpu_calendar_versioned_native',
                 'cpu_calendar_versioned_prefill','cpu_calendar_prefill_guard','cpu_calendar_prefill_reentry'):
        path=ROOT/'analysis/hangul_keyboard_v1'/name/'report.json';d=read(path)
        if not d['passed']:raise ValueError('keyboard evidence failed')
        for n,h in d['tools'].items():require_hash(ROOT/'tools'/n,h)
        for n,h in d['artifacts'].items():require_hash(path.parent/n,h)
        for n,h in d.get('dependencies',{}).items():require_hash(path.parent.parent/n,h)
        keyboard[name]=dict(sha256=sha(path.read_bytes()),CPU_passed=True,rom_integrated=d['rom_integrated'],
            format_adopted=d.get('format_adopted'),limits=d['limits'])
    risks_path=ROOT/'analysis/hangul_keyboard_v1/native_storage_risks.json';risks=read(risks_path)
    require_hash(ROOT/'tools/bench_native_keyboard_storage.py',risks['tool_sha256'])
    if sha(rom[0x35000:0x35034])!=risks['writer_range_sha256']:raise ValueError('native writer source changed')
    report=dict(schema=1,audit_completed=True,build_ready=False,rom_created=False,runtime_tested=False,
        source_sha256=sha(rom),baseline_sha256=sha(baseline.read_bytes()),drafts=len(drafts),draft_archives=len(archives),
        registered_archives=len(registry['archives']),structural_without_draft=pending,counts=dict(count),
        per_archive={k:dict(v) for k,v in sorted(by_archive.items())},unresolved_consumers=unresolved,
        registered_scalar_measurements=measured,heuristic_132px_review_flags=geometry,
        heuristic_132px_warning_count=sum(x['needs_geometry_reassessment'] for x in geometry),
        keyboard=keyboard,naive_F9FC_storage_counterexample=dict(report_sha256=sha(risks_path.read_bytes()),
            truncated_syllables=risks['truncated_syllables'],overflow=risks['overflow'],
            meaning='Reject direct F9FC native storage, NOT evidence that the conditional versioned-record candidate fails.'),
        blockers=['Full draft selection has no coordinated registered consumer/reference/layout/build contract.',
            'Keyboard CPU selector and conditional versioned calendar records are separate fixtures; initialization, all writers/readers/prefill/list, save format discrimination and game RAM/IRQ lifetime are not adopted together.',
            'No exact cumulative installed ROM exists to run through input/confirm/redisplay/save/reset/fresh-load.'],
        inputs=inputs,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('report_full_rom_integration.py','prepare_translation_first.py','build_development_patch.py')},
        limits=['Draft source/control/Hangul glyph checks rerun for every selected draft asset. Human review is not the technical integration blocker.',
            '132px flags for unregistered consumers are review candidates, not confirmed clipping failures. Registered scalar checks are not aggregate/variable/choice QA.',
            'No prose shortening, token mutation, source/ROM/save write, test launch, or readiness inference from CPU test counts.'])
    out=ROOT/'analysis/full_rom_integration_v1';out.mkdir(exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(src,cfg['source_profile']['sha256']);require_hash(baseline,plan['baseline_rom']['sha256'])
    print(json.dumps({k:report[k] for k in ('audit_completed','build_ready','drafts','draft_archives','registered_archives','counts','structural_without_draft','heuristic_132px_warning_count')},ensure_ascii=False))
    return 2


if __name__=='__main__':raise SystemExit(main())
