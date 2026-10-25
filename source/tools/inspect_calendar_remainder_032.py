"""Actual031 calendar table remainder, including mixed scripts; not admission."""
import re
from collections import Counter,defaultdict
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from tpl_literals import literals
from field_hint_capacity import events
from compare_archive_payloads import payload_of
from verify_tpi_index import parse_tpi
from calendar_delete_capacity_031 import CALENDARS

BASE='poc/output/pending500_031_v1.gba'
OUT='analysis/pending_insertion_500_032_calendar_inventory_v1/census.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256']);proof=read('analysis/pending500_031_v1/integration.json')
    if not proof['passed'] or not proof['independent_rebuild_byte_identical'] or proof['rom_sha256']!=m['output_sha256']:raise ValueError('032 completed actual031 baseline')
    coverage=read('analysis/translation_first_v1/coverage.json');pool=defaultdict(list)
    deps={'analysis/translation_first_v1/coverage.json':sha((ROOT/'analysis/translation_first_v1/coverage.json').read_bytes()),'analysis/pending500_031_v1/integration.json':sha((ROOT/'analysis/pending500_031_v1/integration.json').read_bytes()),'tools/inspect_calendar_remainder_032.py':sha((ROOT/'tools/inspect_calendar_remainder_032.py').read_bytes())}
    for path,h in coverage['draft_asset_hashes'].items():
        # Coverage is an immutable translator-authored wording catalog.
        require_hash(ROOT/path,h);a=read(path)
        if a['archive'] not in CALENDARS:continue
        deps[path]=h
        for u in a['units']:pool[u['id']].append((path,h,u,a))
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};applied={u['id'] for r in layout_records(m) for u in r['layout']};groups=[];by_script=Counter();by_kind=Counter()
    for arc in sorted(CALENDARS):
        row=catalog[arc];native=sha(payload_of(source,row));path='analysis/tpl_baseline/'+arc+'.tpl';text=(ROOT/path).read_text(encoding='utf-8-sig');deps[path]=sha((ROOT/path).read_bytes());old={u.key:u for u in literals(text)}
        remaining=[u for u in old.values() if u.language=='mmbn45' and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',u.text) and u.key not in applied]
        for script in sorted({int(u.key.split(':')[1]) for u in remaining}):
            chosen=[u for u in remaining if int(u.key.split(':')[1])==script];refs=[];issues=[]
            for original in chosen:
                options=pool[original.key]
                if not options or len({(u['source'],u['translation'],u['state']) for _,_,u,_ in options})!=1:issues.append(original.key);continue
                p,h,u,a=options[0]
                if u['source']!=original.text or a['source_sha256']!=sha(source) or a['source_archive_sha256']!=native:raise ValueError('032 original source/wording provenance')
                refs.append(dict(id=u['id'],path=p,sha256=h,source=u['source'],translation=u['translation'],state=u['state']))
            section=re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',text,re.M)[0];commands=[d[0] for _,kind,d in events('@archive '+arc+'\n'+section) if kind=='command'];already=sorted(k for k in applied if k.startswith(arc+':'+str(script)+':'));kind='mixed-script' if already else 'whole-script';by_kind[kind]+=len(chosen);by_script[str(script)]+=len(chosen)
            groups.append(dict(archive=arc,script=script,ids=[u.key for u in chosen],units=len(chosen),already_applied_ids=already,kind=kind,commands=commands,drafts=refs,missing_or_conflicting=issues,source_payload_sha256=native,source_tpl=dict(path=path,sha256=deps[path]),source_row=row,product_admitted=False))
    ids=[k for g in groups for k in g['ids']]
    if len(ids)!=len(set(ids)) or set(ids)&applied:raise ValueError('032 remainder duplicate or already applied')
    frozen_write(ROOT/OUT,dict(schema=1,status='ACTUAL031_CALENDAR_REMAINDER_INVENTORY_NOT_ADMISSION',baseline_rom=BASE,baseline_sha256=m['output_sha256'],source_sha256=sha(source),literal_units=len(ids),script_groups=len(groups),calendar_roots=len(CALENDARS),by_script=dict(by_script),by_kind=dict(by_kind),groups=groups,dependencies=deps,rom_written=False,new_units_applied=0,release_eligible=False,limits=['Only original Japanese text literals in21 declared calendar-table roots, not full-game or graphics remainder.','Mixed-script ownership, date/current-date/weekday producers, annotation titles and menu choice/control consumers still require individual evidence before selecting next500.','Canonical needs_review wording retained, not semantic/human approval.']))
    print('032 remaining calendar literals',len(ids),'groups',len(groups),'by kind',dict(by_kind),'by script',dict(by_script))


if __name__=='__main__':main()
