"""Strict source500 communication-help compile, full roundtrips/font; NOT ROM."""
import re
from collections import defaultdict
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash,run_textpet,bdf_glyphs
from cumulative_batch500 import read,frozen_write
from prepare_communication039_v1 import OUT
from profile_layout039_v1 import reconstruct
from profile_quick_geometry039_v1 import validate
from compare_archive_payloads import payload_of
from tpl_literals import literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from canonical_literals_031 import canonical_literals
from archive_scripts import verify_untouched_scripts
from build_development_patch import validate_literal_numerals
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES,EXTRA_CHARACTER_METRICS
from survey_batch500_017_layout import protected_edges

def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))

def main():
    s=read(OUT+'/selection.json');cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,s['source_sha256']);source=sp.read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'))
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if s['selected_proposed_units']!=500 or s['rom_written'] or s['product_admitted']:raise ValueError('039 source-only500 selection')
    out=ROOT/OUT/'compile_v1';out.mkdir(parents=True,exist_ok=False);plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins');grouped=defaultdict(list)
    for g in s['groups']:grouped[g['archive']].append(g)
    records=[];seen=set();chars=set();soft=0
    for arc,groups in sorted(grouped.items()):
        sr=groups[0]['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);original=(ROOT/sr['path']).read_text(encoding='utf-8-sig');row=groups[0]['source_row'];native=payload_of(source,row)
        if payload_of(rom,row)!=native or any(rom[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('039 unchanged native source/lookup')
        units=[];values={};raw={u.key:u.text for u in literals(original)}
        for g in groups:
            byid={x['id']:x for x in g['layout_proposals']};subset={}
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']));p=byid[u['id']]['layout'];value=g['explicit_layouts'][u['id']]
                if u['id'] in seen or u['source']!=raw[u['id']] or u['state']!='needs_review' or p['canonical']!=u['translation'] or p['flat_wording']!=u['translation'].replace('\n',' ') or '\n'.join(p['lines'])!=value or reconstruct(p['lines'],p['break_kinds'])!=p['flat_wording'] or not protected_edges(u['source'],value):raise ValueError('039 canonical wording/break schema/source binding')
                u['canonical_wording']=u['translation'];u['translation']=value;u['explicit_layout_proposal']=p
                units.append(u);values[u['id']]=value;subset[u['id']]=value;seen.add(u['id']);chars.update(value);soft+=int(bool(p['soft_breaks']))
            if validate(original,replace_exact(original,subset),[g['script']],set(g['ids']))!=g['geometry']:raise ValueError('039 independent window geometry replay')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True));target=replace_exact(original,values)
        if skeleton(original)!=skeleton(target):raise ValueError('039 original control topology')
        f=out/arc;f.mkdir();a=f/'source.tpl';b=f/'target.tpl';a.write_text(canonical_literals(original),encoding='utf8',newline='\n');b.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        def convert(x,xf,y,yf,log):run_textpet(common+['Read-Text-Archives',str(x),'--format',xf,'Write-Text-Archives',str(y),'--format',yf],f/log)
        n=f/(arc+'_native.msg');p=f/(arc+'.msg');reverse=f/'reverse.tpl';again=f/(arc+'_rebuilt.msg')
        convert(a,'tpl',n,'bin','native.log')
        if n.read_bytes()!=native:raise ValueError('039 complete original archive byte roundtrip')
        convert(b,'tpl',p,'bin','compile.log');payload=p.read_bytes()
        if len(payload)>65535:raise ValueError('039 script offset capacity')
        convert(p,'bin',reverse,'tpl','reverse.log');convert(reverse,'tpl',again,'bin','rebuild.log');exported=reverse.read_text(encoding='utf-8-sig')
        if again.read_bytes()!=payload or skeleton(exported)!=skeleton(original) or [(u.key,u.language,u.text) for u in literals(target)]!=[(u.key,u.language,u.text) for u in literals(exported)]:raise ValueError('039 target semantic/control/binary roundtrip')
        count=int(re.search(r'^@size (\d+)$',original,re.M)[1]);kept=verify_untouched_scripts(native,payload,count,{g['script'] for g in groups})
        records.append(dict(archive=arc,source_tpl=sr,source_row=row,source_sha256=sha(native),native_bytes=len(native),compiled=ref(p),compiled_bytes=len(payload),target_tpl=ref(b),units=units,script_count=count,unselected_source_scripts=kept,controls_unchanged=True,roundtrip=True,product_admitted=False))
        print('PASS039 source',arc,len(units),'units',flush=True)
    if seen!=set(s['selected_ids']) or len(seen)!=500:raise ValueError('039 complete exact500 compile population')
    wanted={c for c in chars if '\uac00'<=c<='\ud7a3'};extra=chars&EXTRA_CHARACTER_INDICES.keys();fp=ROOT/cfg['development_dependencies']['font']['path'];require_hash(fp,cfg['development_dependencies']['font']['sha256']);glyphs=bdf_glyphs(fp,wanted);glyphs.update(bdf_glyphs(fp,extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    for c,glyph in glyphs.items():
        i=m['extension']['legacy_index_view']+(ord(c)-0xAC00 if c in wanted else EXTRA_CHARACTER_INDICES[c]);at=m['extension']['normal_font_offset']+i*96
        if rom[at:at+96]!=glyph:raise ValueError('039 current038 glyph supply '+c)
    deps=[OUT+'/selection.json','tools/compile_communication039_v1.py','tools/profile_layout039_v1.py','tools/profile_quick_geometry039_v1.py','tools/archive_scripts.py','tools/tpl_literals.py','tools/canonical_literals_031.py','tools/textpet_korean.py']
    frozen_write(ROOT/OUT/'verification_v1.json',dict(passed=True,status='EXACT500_COMMUNICATION_SOURCE_COMPILE_FONT_LAYOUT_PROPOSALS_PASS_NOT_ROM',baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=sha(source),units=500,archives=records,extended_glyphs_checked=len(glyphs),units_with_Hangul_syllable_break_proposal=soft,wording_changed=False,rom_written=False,new_units_applied=0,product_admitted=False,product_integrated=False,runtime_tested=False,release_eligible=False,plugin=plugin,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=s['limits']+['Static source compile only; no040/039 product ROM. External communication-menu options/hold lifetime/native reader and font-to-screen link remain. No network connection attempted.']))
    print('PASS039 exact500 source/font/roundtrip;',len(records),'archives,',len(glyphs),'glyphs; NO ROM')

if __name__=='__main__':main()
