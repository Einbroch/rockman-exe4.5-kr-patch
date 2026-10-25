"""Next500 source-only preparation; deliberately has no ROM writer.

Reuses pinned canonical wording and geometry, excludes every already owned
archive, and leaves035 natural-selection QA open. Not a product-admission gate.
"""
import re,sys,struct
from collections import defaultdict,Counter
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash,run_textpet,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from field_npc_rom_selector_035_v3 import source_population
from compare_archive_payloads import payload_of
from verify_tpi_index import lz77_decompress
from survey_new_storage_035 import VALIDATORS
from survey_aggregate_pet_033 import replace_exact
from tpl_literals import literals,skeleton
from survey_batch500_017_layout import protected_edges
from canonical_literals_031 import canonical_literals
from archive_scripts import verify_untouched_scripts
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from build_development_patch import validate_literal_numerals

BASE='poc/output/pending500_035_v2.gba'
BASE_SHA='41fdee5673329c00f80989e5de2d98db6b3b0980c9a30c5e4b8202fd8dd4d95d'
SURVEY='analysis/pending_insertion_500_035_new_storage_layout_v1/survey.json'
OUT='analysis/pending_insertion_500_036_source_only_v1'


def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))
def need(ok,msg):
    if not ok:raise ValueError(msg)


def baseline():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256'])
    require_hash(ROOT/BASE,BASE_SHA);m=read(BASE.replace('.gba','.json'))
    need(m['output_sha256']==BASE_SHA,'Current035 baseline')
    return cfg,sp.read_bytes(),(ROOT/BASE).read_bytes(),m


def select():
    cfg,source,rom,m=baseline();s=read(SURVEY)
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    applied={u['id'] for r in layout_records(m) for u in r['layout']};owned={r['archive'] for r in layout_records(m)}
    old=read('poc/output/pending500_034_v1.json');oldids={u['id'] for r in layout_records(old) for u in r['layout']}
    need(len(applied-oldids)==500 and oldids<=applied,'Actual035 adds exactly500 unique literal IDs')
    selected035={r['archive'] for r in m['keyitem_rom']['npc035']['archives']}
    population=source_population(source,selected035);a0={r['archive'] for r in population}
    gs=[deepcopy(g) for g in s['candidate_groups'] if g['storage']=='compressed' and g['archive'] in (a0|{'7AAF94','7B469C'}) and g['archive'] not in owned]
    gs.sort(key=lambda g:(g['archive'] not in a0,g['archive'],g['script']))
    ids=[k for g in gs for k in g['ids']]
    need(len(ids)==len(set(ids))==500 and not set(ids)&applied,'Exactly500 disjoint new IDs')
    need(sum(g['units'] for g in gs if g['archive'] in a0)==430,'Retained A0 candidate denominator')
    validators=dict(VALIDATORS);texts={};drafts={};profiles=Counter()
    for g in gs:
        need(not g['locked_parent_units'] and not g['already_applied_ids_in_script'],'No prior script edits')
        a=g['archive'];src=g['source_tpl'];require_hash(ROOT/src['path'],src['sha256'])
        original=texts.setdefault(a,(ROOT/src['path']).read_text(encoding='utf-8-sig'))
        native=payload_of(source,g['source_row']);need(sha(native)==g['source_archive_sha256'],'Immutable source archive identity')
        need(payload_of(rom,g['source_row'])==native,'Current source storage identity')
        values={};raw={u.key:u.text for u in literals(original)}
        for d in g['drafts']:
            require_hash(ROOT/d['path'],d['sha256']);asset=drafts.setdefault(d['path'],read(d['path']))
            u=next(u for u in asset['units'] if u['id']==d['id'])
            need(asset['source_sha256']==sha(source) and asset['source_tpl']==src and asset['source_archive_sha256']==sha(native) and u['source']==raw[u['id']] and u['state']=='needs_review','Canonical draft provenance')
            v=g['explicit_layouts'].get(u['id'],u['translation'])
            need(v.replace('\n',' ')==u['translation'].replace('\n',' ') and protected_edges(u['source'],v),'No prose/spacing/control-edge change')
            values[u['id']]=v
        need(set(values)==set(g['ids']),'Selected whole-script IDs')
        need(validators[g['profile']](original,replace_exact(original,values),[g['script']],set(g['geometry_ids']),99)==g['geometry'],'Independent geometry replay')
        profiles[g['profile']]+=g['units']
    census=read('analysis/pending_insertion_500_035_inventory_v1/census.json')
    remaining=set(k for g in census['groups'] for k in g['ids'])-applied
    need(len(remaining)==11924 and set(ids)<=remaining,'Pinned pending-draft denominator')
    deps=[SURVEY,'analysis/pending_insertion_500_035_inventory_v1/census.json','analysis/pending500_035_v2/native_mode_display_v1.json','tools/prepare_source500_036_v1.py']
    deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS]
    result=dict(schema=1,status='EXACT500_SOURCE_ONLY_GEOMETRY_REPLAY_PASS_NOT_ROM_ADMISSION',baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),planned_new_units=500,native_nickname_bound=99,selected_ids=sorted(ids),groups=gs,profiles=dict(profiles),archives=sorted(texts),canonical_pending_draft_ids_before_selection=len(remaining),remaining_unselected_draft_ids=len(remaining-set(ids)),wording_changed=False,rom_written=False,new_units_applied=0,insertion_ready=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Source-only work may proceed while035 natural cached actor selection remains OPEN; no ROM promotion is authorized by this report.','430 A0 candidates,70 in two additional compressed archives with loader/root/residency NOT yet admitted.','Existing canonical drafts, not500 newly authored translations or500 runtime-tested sentences.','Draft count excludes unextracted text/graphics and is not a whole-game remaining denominator.'])
    frozen_write(ROOT/OUT/'selection.json',result)
    print('PASS next500 source-only selection:',len(gs),'scripts,',len(texts),'archives;11924 pending draft IDs; NO ROM')


def compile_all():
    cfg,source,rom,m=baseline();s=read(OUT+'/selection.json')
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    out=ROOT/OUT/'compile';out.mkdir(parents=True,exist_ok=False)
    plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins')
    grouped=defaultdict(list)
    for g in s['groups']:grouped[g['archive']].append(g)
    records=[];seen=set();chars=set();validators=dict(VALIDATORS)
    for arc,groups in sorted(grouped.items()):
        sr=groups[0]['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);original=(ROOT/sr['path']).read_text(encoding='utf-8-sig');row=groups[0]['source_row']
        native=payload_of(source,row);need(payload_of(rom,row)==native,'Current native source retained')
        need(all(rom[p:p+4]==source[p:p+4] for p in row['pointers'] if p),'Current source pointers retained')
        units=[];values={};source_lits={u.key:u.text for u in literals(original)}
        for g in groups:
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']))
                v=g['explicit_layouts'].get(u['id'],u['translation'])
                need(u['id'] not in seen and u['source']==source_lits[u['id']] and u['state']=='needs_review' and v.replace('\n',' ')==u['translation'].replace('\n',' ') and protected_edges(u['source'],v),'Compile source/wording ownership')
                u['translation']=v;units.append(u);values[u['id']]=v;seen.add(u['id']);chars.update(v)
            need(validators[g['profile']](original,replace_exact(original,values),[g['script']],set(g['geometry_ids']),99)==g['geometry'],'Compile geometry replay')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        target=replace_exact(original,values);need(skeleton(original)==skeleton(target),'Protected original topology')
        f=out/arc;f.mkdir();a=f/'source.tpl';b=f/'target.tpl'
        a.write_text(canonical_literals(original),encoding='utf8',newline='\n');b.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        def convert(x,xf,y,yf,log):run_textpet(common+['Read-Text-Archives',str(x),'--format',xf,'Write-Text-Archives',str(y),'--format',yf],f/log)
        n=f/'native.msg';p=f/'target.msg';r=f/'reverse.tpl';again=f/'rebuilt.msg'
        convert(a,'tpl',n,'bin','native.log');need(n.read_bytes()==native,'Complete source byte roundtrip')
        convert(b,'tpl',p,'bin','compile.log');payload=p.read_bytes();need(len(payload)<=65535,'16-bit script offset capacity')
        convert(p,'bin',r,'tpl','reverse.log');convert(r,'tpl',again,'bin','rebuild.log')
        exported=r.read_text(encoding='utf-8-sig')
        need(skeleton(original)==skeleton(exported) and [(u.key,u.language,u.text) for u in literals(target)]==[(u.key,u.language,u.text) for u in literals(exported)] and again.read_bytes()==payload,'Target semantic/control/binary roundtrip')
        count=int(re.search(r'^@size (\d+)$',original,re.M)[1]);kept=verify_untouched_scripts(native,payload,count,{g['script'] for g in groups})
        records.append(dict(archive=arc,source_tpl=sr,source_payload_sha256=sha(native),native_bytes=len(native),compiled_bytes=len(payload),script_count=count,target_tpl=ref(b),compiled=ref(p),units=units,unselected_scripts=kept,controls_unchanged=True,roundtrip=True,product_admitted=False))
        print('PASS source036',arc,len(units),'units',flush=True)
    need(seen==set(s['selected_ids']) and len(seen)==500,'Exact500 compile population')
    wanted={c for c in chars if '\uac00'<=c<='\ud7a3'};extra=chars&EXTRA_CHARACTER_INDICES.keys();fp=ROOT/cfg['development_dependencies']['font']['path'];require_hash(fp,cfg['development_dependencies']['font']['sha256'])
    glyphs=bdf_glyphs(fp,wanted);glyphs.update(bdf_glyphs(fp,extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    for c,glyph in glyphs.items():
        i=m['extension']['legacy_index_view']+(ord(c)-0xAC00 if c in wanted else EXTRA_CHARACTER_INDICES[c]);at=m['extension']['normal_font_offset']+i*96
        need(rom[at:at+96]==glyph,'Actual035 glyph supply '+c)
    require_hash(ROOT/BASE,BASE_SHA)
    frozen_write(ROOT/OUT/'verification.json',dict(schema=1,status='EXACT500_SOURCE_COMPILE_FONT_GEOMETRY_PASS_NOT_ROM_ADMISSION',passed=True,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),selection=ref(ROOT/OUT/'selection.json'),units=500,archive_count=len(records),extended_glyphs_checked=len(glyphs),archives=records,plugin=plugin,tool=ref(ROOT/'tools/prepare_source500_036_v1.py'),wording_changed=False,rom_written=False,new_units_applied=0,insertion_ready=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits=s['limits']+['Native loader/root lifetime for additional storage classes, cumulative writer/ownership/independent product build and runtime verification still required.']))
    print('PASS source036 exact500,',len(records),'archives,',len(glyphs),'current-ROM glyphs; NO ROM')


if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--compile':compile_all()
    else:select()
