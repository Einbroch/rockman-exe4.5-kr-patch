"""Source-only new500 binary/text/font verification, NOT injectable product input.

Existing Korean carries are explicitly NOT replaced or reconstructed here.
Product admission must independently bind authored carry variants and consumers.
"""
import argparse,re
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from canonical_literals_031 import canonical_literals
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from build_development_patch import validate_literal_numerals,validate_characters
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from survey_batch500_017_layout import protected_edges
from prepare_source500_041_v3 import PROFILES
from default_quick_geometry041_v1 import validate as default_quick
from normal_battle_choice_capacity_026 import validate as battle_choice
from pet_choice_capacity_026 import validate as pet_choice
from pet_entry_profile_capacity_030 import validate as pet_entry
from battle_bbs_geometry040_v1 import validate as bbs
from cleared_normal_geometry041_v1 import validate as cleared_normal

PROFILES=dict(PROFILES,**{'default-quick':default_quick,'battle-choice':lambda o,t,ss,ids:battle_choice(o,t,ss,ids,99,88),'pet-choice':lambda o,t,ss,ids:pet_choice(o,t,ss,ids,99),'pet-entry':lambda o,t,ss,ids:pet_entry(o,t,ss,ids,99),'battle-BBS-trial':bbs,'cleared-normal':cleared_normal})


def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--selection',default='analysis/pending_insertion_500_041_source_v7/selection.json');args=parser.parse_args();sp=ROOT/args.selection;s=read(sp);cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'))
    if s['selected_units']!=500 or s['rom_written'] or s['product_admitted']:raise ValueError('041 exact500 source-only prerequisite')
    for path,h in s['dependencies'].items():require_hash(ROOT/path,h)
    out=sp.parent/'compile_v1';out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins');groups=defaultdict(list);chars=set();seen=set();records=[]
    for g in s['groups']:groups[g['archive']].append(g)
    owners=read('analysis/pending_insertion_500_041_inventory_v1/authored_owners.json')
    for arc,gs in sorted(groups.items()):
        sr=gs[0]['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);original=(ROOT/sr['path']).read_text(encoding='utf-8-sig');native=payload_of(source,gs[0]['source_row']);raw={u.key:u.text for u in literals(original)};units=[]
        if sha(native)!=gs[0]['source_archive_sha256']:raise ValueError('041 immutable original payload')
        for g in gs:
            subset={}
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']));text=g['explicit_layouts'][u['id']]
                if u['id'] in seen or u['source']!=raw[u['id']] or a['source_sha256']!=sha(source) or a['source_tpl']!=sr or u['state']!='needs_review' or text.replace('\n',' ')!=u['translation'].replace('\n',' ') or not protected_edges(u['source'],text):raise ValueError('041 exact canonical source/words/edges')
                u['canonical_wording']=u['translation'];u['translation']=text;units.append(u);subset[u['id']]=text;seen.add(u['id']);chars.update(text)
            profile=g['source_class'].removeprefix('unbound-');geo=PROFILES[profile](original,replace_exact(original,subset),[g['script']],set(g['ids']))
            import json
            if json.loads(json.dumps(geo))!=g['geometry']:raise ValueError('041 geometry replay')
        target=replace_exact(original,{u['id']:u['translation'] for u in units});validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        if skeleton(target)!=skeleton(original):raise ValueError('041 protected controls')
        f=out/arc;f.mkdir();src=f/'source.tpl';tp=f/'target_new_only.tpl';np=f/(arc+'_native.msg');bp=f/(arc+'_new_only.msg');reverse=f/'reverse.tpl';again=f/'rebuilt.msg'
        for path,text in [(src,original),(tp,target)]:path.write_text(canonical_literals(text),encoding='utf8',newline='\n')
        def convert(x,xf,y,yf,log):run_textpet(common+['Read-Text-Archives',str(x),'--format',xf,'Write-Text-Archives',str(y),'--format',yf],f/log)
        convert(src,'tpl',np,'bin','native.log');convert(tp,'tpl',bp,'bin','compile.log');payload=bp.read_bytes()
        if np.read_bytes()!=native or len(payload)>65535:raise ValueError('041 original byte roundtrip/u16 table')
        convert(bp,'bin',reverse,'tpl','reverse.log');convert(reverse,'tpl',again,'bin','rebuild.log');exported=reverse.read_text(encoding='utf-8-sig')
        if again.read_bytes()!=payload or skeleton(exported)!=skeleton(original) or [(u.key,u.language,u.text) for u in literals(target)]!=[(u.key,u.language,u.text) for u in literals(exported)]:raise ValueError('041 exact target literal/control/binary roundtrip')
        ids={u['id'] for u in units};scope=dict(consumer='normal-dialogue',literal_language='mmbn45',literal_scripts=sorted({g['script'] for g in gs}),literal_ids=sorted(ids),complete_literal_scope=False,max_literal_rows=3,max_line_advance=180)
        metrics=validate_characters(target,out/'plugins/exe45-utf8.tbl',scope,ids);kept=verify_untouched_scripts(native,payload,gs[0]['script_count'],{g['script'] for g in gs});prior=[r for r in owners['records'] if r['archive']==arc]
        records.append(dict(archive=arc,units=units,new_ids=sorted(ids),source_tpl=sr,native_sha256=sha(native),native_bytes=len(native),source_row=gs[0]['source_row'],target_tpl=ref(tp),new_only_compiled=ref(bp),compiled_bytes=len(payload),script_count=gs[0]['script_count'],layout=metrics,unselected_SOURCE_scripts=kept,current_consumer_carry_requirements=prior,source_roundtrip=True,target_binary_roundtrip=True,protected_controls_unchanged=True,existing_Korean_carry_merged=False,product_admitted=False))
        print('PASS041 source-only',arc,len(units),'old consumer carry pending',len(prior),flush=True)
    if seen!=set(s['selected_ids']) or len(seen)!=500:raise ValueError('041 exact500 denominator')
    wanted={c for c in chars if '\uac00'<=c<='\ud7a3'};extra=chars&EXTRA_CHARACTER_INDICES.keys();fp=ROOT/cfg['development_dependencies']['font']['path'];require_hash(fp,cfg['development_dependencies']['font']['sha256']);glyphs=bdf_glyphs(fp,wanted);glyphs.update(bdf_glyphs(fp,extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    for c,glyph in glyphs.items():
        i=m['extension']['legacy_index_view']+(ord(c)-0xAC00 if c in wanted else EXTRA_CHARACTER_INDICES[c]);at=m['extension']['normal_font_offset']+i*96
        if rom[at:at+96]!=glyph:raise ValueError('041 current font supply '+c)
    deps=[args.selection,'tools/compile_source500_041_v1.py','tools/prepare_source500_041_v3.py','tools/default_quick_geometry041_v1.py','tools/cleared_normal_geometry041_v1.py','tools/normal_battle_choice_capacity_026.py','tools/pet_choice_capacity_026.py','tools/pet_entry_profile_capacity_030.py','analysis/pending_insertion_500_041_inventory_v1/authored_owners.json']
    frozen_write(sp.parent/'verification_v1.json',dict(passed=True,status='041_NEW500_SOURCE_ONLY_ROUNDTRIP_FONT_PASS_NOT_CARRY_OR_ROM',baseline_sha256=s['baseline_sha256'],source_sha256=sha(source),units=500,archives=records,extended_glyphs_checked=len(glyphs),wording_changed=False,rom_written=False,new_units_applied=0,existing_Korean_carry_merged=False,product_admitted=False,runtime_tested=False,release_eligible=False,plugin=plugin,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['New-only binary diagnostic is NOT an injectable target: existing Korean carries are absent. Regenerate all active carry variants from authored inputs and preserve every unchanged current script before admission.','Conditional geometry is not real caller/default origin/lifetime/selector/initializer/renderer proof.','No041 ROM or distribution package.']))
    print('PASS041 source-only exact500 glyphs',len(glyphs),'NOT carry/ROM')


if __name__=='__main__':main()
