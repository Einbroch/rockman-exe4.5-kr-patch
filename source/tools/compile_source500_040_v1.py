"""040 source500 plus authored039 carry compile, NOT product ROM/integration."""
import re,json
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from prepare_source500_040_v2 import OUT
from tpl_literals import literals,skeleton,resolve_units
from survey_aggregate_pet_033 import replace_exact
from canonical_literals_031 import canonical_literals
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from build_development_patch import validate_literal_numerals,validate_characters
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from battle_bbs_geometry040_v1 import validate as bbs
from profile_quick_geometry039_v1 import validate as communication
from normal_timing_capacity_025 import validate as normal
from survey_batch500_017_layout import protected_edges


def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))


def main():
    s=read(OUT+'/selection.json');cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,s['source_sha256']);source=sp.read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'))
    if s['selected_units']!=500 or s['rom_written'] or s['product_admitted']:raise ValueError('040 exact500 source-only prerequisites')
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    out=ROOT/OUT/'compile_v1';out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins');groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    records=[];seen=set();carryids=set();chars=set()
    for arc,gs in sorted(groups.items()):
        sr=gs[0]['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);original=(ROOT/sr['path']).read_text(encoding='utf-8-sig');native=payload_of(source,gs[0]['source_row']);raw={u.key:u.text for u in literals(original)};new=[];parent=None;old=[]
        link=m['active_communication_owners039'].get(arc)
        if link:
            require_hash(ROOT/link['path'],link['sha256']);a=read(link['path']);old=deepcopy(resolve_units(a));parent=next(r for r in m['keyitem_rom']['communication039']['archives'] if r['archive']==arc)
            if a['source_sha256']!=sha(source) or a['source_archive_sha256']!=sha(native) or a['policy']!='development-draft; NON-DISTRIBUTION' or {u['id'] for u in old}!={x['id'] for x in parent['layout']}:raise ValueError('040 authored039 carry provenance')
        for g in gs:
            subset={}
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(x for x in a['units'] if x['id']==d['id']));value=g['explicit_layouts'][u['id']]
                if u['id'] in seen or u['source']!=raw[u['id']] or u['state']!='needs_review' or a['source_sha256']!=sha(source) or a['source_tpl']!=sr or value.replace('\n',' ')!=u['translation'].replace('\n',' ') or not protected_edges(u['source'],value):raise ValueError('040 canonical word-boundary source binding')
                u['canonical_wording']=u['translation'];u['translation']=value;new.append(u);subset[u['id']]=value;seen.add(u['id'])
            targetone=replace_exact(original,subset);kind=g['source_class']
            geo=communication(original,targetone,[g['script']],set(g['ids'])) if kind=='communication-help' else bbs(original,targetone,[g['script']],set(g['ids'])) if kind=='battle-BBS-trial' else normal(original,targetone,[g['script']],set(g['ids']),99,88)
            if json.loads(json.dumps(geo))!=g['geometry']:raise ValueError('040 selected geometry replay')
        units=old+new;ids={u['id'] for u in units}
        if len(ids)!=len(units) or any(u['source']!=raw[u['id']] for u in units):raise ValueError('040 carry/new identity')
        target=replace_exact(original,{u['id']:u['translation'] for u in units});oldtarget=replace_exact(original,{u['id']:u['translation'] for u in old})
        if skeleton(target)!=skeleton(original):raise ValueError('040 protected control topology')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));f=out/arc;f.mkdir();src=f/'source.tpl';prior=f/'prior.tpl';tp=f/'target.tpl'
        for path,text in [(src,original),(prior,oldtarget),(tp,target)]:path.write_text(canonical_literals(text),encoding='utf8',newline='\n')
        def convert(x,xf,y,yf,log):run_textpet(common+['Read-Text-Archives',str(x),'--format',xf,'Write-Text-Archives',str(y),'--format',yf],f/log)
        np=f/(arc+'_native.msg');pp=f/(arc+'_prior.msg');bp=f/(arc+'.msg');reverse=f/'reverse.tpl';again=f/'rebuilt.msg'
        convert(src,'tpl',np,'bin','native.log');convert(prior,'tpl',pp,'bin','prior.log');convert(tp,'tpl',bp,'bin','compile.log')
        if np.read_bytes()!=native or len(bp.read_bytes())>65535:raise ValueError('040 original roundtrip/u16 capacity')
        if parent:
            before=rom[parent['rom_offset']:parent['rom_offset']+parent['compiled_bytes']]
            if sha(before)!=parent['compiled_sha256'] or pp.read_bytes()!=before:raise ValueError('040 regenerated authored carry not current039 bytes')
        else:
            if pp.read_bytes()!=native:raise ValueError('040 unowned source carry')
            before=native
        payload=bp.read_bytes();convert(bp,'bin',reverse,'tpl','reverse.log');convert(reverse,'tpl',again,'bin','rebuild.log');exported=reverse.read_text(encoding='utf-8-sig')
        if again.read_bytes()!=payload or skeleton(exported)!=skeleton(original) or [(u.key,u.language,u.text) for u in literals(target)]!=[(u.key,u.language,u.text) for u in literals(exported)]:raise ValueError('040 target text/control/binary roundtrip')
        count=gs[0]['script_count'];kept=verify_untouched_scripts(before,payload,count,{g['script'] for g in gs});scope=dict(consumer='normal-dialogue',literal_language='mmbn45',literal_scripts=sorted({int(u['id'].split(':')[1]) for u in units}),literal_ids=sorted(ids),complete_literal_scope=False,max_literal_rows=3,max_line_advance=180)
        metrics=validate_characters(target,out/'plugins/exe45-utf8.tbl',scope,ids)
        if parent and {x['id']:x for x in parent['layout']}!={x['id']:x for x in metrics if x['id'] in {u['id'] for u in old}}:raise ValueError('040 inherited literal metrics changed')
        chars.update(c for u in units for c in u['translation']);carryids.update(u['id'] for u in old);records.append(dict(archive=arc,source_tpl=sr,source_row=gs[0]['source_row'],source_sha256=sha(native),native_bytes=len(native),compiled=ref(bp),compiled_bytes=len(payload),target_tpl=ref(tp),units=units,new_ids=[u['id'] for u in new],inherited_ids=[u['id'] for u in old],parent_asset=link,parent_record_identity=({k:parent[k] for k in ('archive','rom_offset','compiled_sha256','compiled_bytes')} if parent else None),script_count=count,layout=metrics,unselected_current039_scripts=kept,roundtrip=True,controls_unchanged=True,product_admitted=False))
        print('PASS040 source',arc,'new',len(new),'carry',len(old),flush=True)
    if seen!=set(s['selected_ids']) or len(seen)!=500:raise ValueError('040 exact500 denominator')
    wanted={c for c in chars if '\uac00'<=c<='\ud7a3'};extra=chars&EXTRA_CHARACTER_INDICES.keys();fp=ROOT/cfg['development_dependencies']['font']['path'];require_hash(fp,cfg['development_dependencies']['font']['sha256']);glyphs=bdf_glyphs(fp,wanted);glyphs.update(bdf_glyphs(fp,extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    for c,glyph in glyphs.items():
        index=m['extension']['legacy_index_view']+(ord(c)-0xAC00 if c in wanted else EXTRA_CHARACTER_INDICES[c]);at=m['extension']['normal_font_offset']+index*96
        if rom[at:at+96]!=glyph:raise ValueError('040 current039 glyph supply '+c)
    deps=[OUT+'/selection.json','tools/compile_source500_040_v1.py','tools/battle_bbs_geometry040_v1.py','tools/profile_quick_geometry039_v1.py','tools/normal_timing_capacity_025.py','tools/textpet_korean.py','tools/archive_scripts.py']
    frozen_write(ROOT/OUT/'verification_v1.json',dict(passed=True,status='040_EXACT500_PLUS_AUTHORED_CARRY_SOURCE_FONT_ROUNDTRIP_PASS_NOT_ROM',source_sha256=sha(source),baseline_sha256=s['baseline_sha256'],units=500,inherited_units=len(carryids),archives=records,extended_glyphs_checked=len(glyphs),wording_changed=False,Hangul_syllable_breaks=0,rom_written=False,new_units_applied=0,product_admitted=False,runtime_tested=False,release_eligible=False,plugin=plugin,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=s['limits']+['Source compile only: original+authored039 carry recompiled, NOT previous-ROM extracted text. No new product ROM, loader/RAM/caller/CPU or screen verification.','Compressed-normal6E93C8 reader/loader context and BBS168 trial capacity must be established before product adoption.']))
    print('PASS040 exact500/carry',len(carryids),'archives',len(records),'glyphs',len(glyphs),'NOT ROM')


if __name__=='__main__':main()
