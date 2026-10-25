"""45 real deferred normal units plus455 untouched raw units. No prose edits."""
import argparse,json,re
import prepare_repartition500 as selector
import prepare_pending_batch500_002 as compiler
from build_visibility_poc import ROOT,sha,require_hash
from equipment_labels import validate
from equipment_weapons import merge
from tpl_literals import resolve_units

BASE='poc/output/exe45_ko_development_pending500_002_v1.gba'
SELECTION='analysis/pending_insertion_500_003_selection_v1'
PREFLIGHT='analysis/pending_insertion_500_003_preflight_v1'
SEEDS=[('translations/batch500_001_equipment_guts_draft_ko.json',{60,61,62,70,71,72,73,74,75},13),
       ('translations/batch500_001_equipment_fire_draft_ko.json',{60,61,62,70,71,72,73,74,75},13),
       ('translations/batch500_001_equipment_proto_draft_ko.json',{60,61,62,70,71,72,73,74,75},13),
       ('translations/batch500_045_navi_mail_npcs_6A5578_draft_ko.json',{1,2,20,21,22,23},6)]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-selection',action='store_true');parser.add_argument('--preflight',default=PREFLIGHT);args=parser.parse_args()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    meta=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'));require_hash(ROOT/BASE,meta['output_sha256'])
    validate(source)
    common=merge(json.loads((ROOT/'translations/equipment_labels_ko.json').read_text(encoding='utf8')),
        json.loads((ROOT/'translations/equipment_weapons_ko.json').read_text(encoding='utf8')))
    names={int(u['id'].split(':')[1]):u for u in resolve_units(common)}
    aliases=[];seeds=[]
    for path,scripts,count in SEEDS:
        d=json.loads((ROOT/path).read_text(encoding='utf8'));a=d['archive']
        if a!='6A5578':
            for u in d['units']:
                s=int(u['id'].split(':')[1])
                if 1<=s<=37:
                    if u['source']!=names[s]['source'] or u['translation']!=names[s]['translation']:raise ValueError('Common label/gear wording conflict')
                    aliases.append(dict(source_id=u['id'],existing_consumer_id=names[s]['id'],source=u['source'],translation=u['translation'],counted_as_new=False))
        chosen=[u for u in d['units'] if int(u['id'].split(':')[1]) in scripts]
        if len(chosen)!=count:raise ValueError('Deferred source population')
        seeds.append(dict(path=path,sha256=sha((ROOT/path).read_bytes()),archive=a,scripts=sorted(scripts),units=count,selected_ids=[u['id'] for u in chosen]))
    selector.BASE=BASE;selector.OUT=SELECTION;selector.TARGET=455;selector.EXCLUDE={s['archive'] for s in seeds}
    if not args.reuse_selection:selector.main()
    selection_path=ROOT/SELECTION/'selection.json'
    selection=json.loads(selection_path.read_text(encoding='utf8'))
    selection.update(batch_id='pending-insertion-500-003',seed_archives=seeds,existing_common_display_aliases=aliases,
        remaining_deferred_ids=['6E1554:0:0','6E1CC0:0:0','6E21B0:0:0','6A5578:10:0'],
        deferred_reconciliation='Original160 =111 existing common-name aliases +45 real normal insertions +4 still unresolved; alias display/source/wording verified, no duplicate count.')
    selection_path.write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    plan=[]
    for r in seeds+selection['replacement_archives']:
        d=json.loads((ROOT/r['path']).read_text(encoding='utf8'));tpl=(ROOT/d['source_tpl']['path']).read_text(encoding='utf-8-sig')
        all_scripts={int(m.group(1)) for m in re.finditer(r'^script\s+(\d+)\s',tpl,re.M)}
        plan.append((r['path'],all_scripts-set(r['scripts']),r['units']))
    compiler.BASE=BASE;compiler.BASE_SHA=meta['output_sha256'];compiler.PLAN=plan
    compiler.LAYOUT='translations/pending_insertion_500_003_layout.json';compiler.LAYOUT_COUNT=0
    compiler.prepare(ROOT/args.preflight)
    report=json.loads((ROOT/args.preflight/'preflight.json').read_text(encoding='utf8'))
    if report['layout_candidates']:raise ValueError('Geometry candidates remain')
    report.update(batch_id='pending-insertion-500-003',selection=dict(path=str(selection_path.relative_to(ROOT)),sha256=sha(selection_path.read_bytes())))
    (ROOT/args.preflight/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


if __name__=='__main__':main()
