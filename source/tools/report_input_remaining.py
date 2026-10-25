"""Exact ROM write/selection/unmodified-payload audit; NOT runtime QA."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans
from input_remaining import GENERATED,validate,SCRIPTS
from keyitem_rom_data import verify_final

STEM='exe45_ko_development_input_remaining_v1'

def read(p):return json.loads(p.read_text(encoding='utf8'))

def main(stem=STEM,previous='exe45_ko_development_input_heading_v1_r2',generated=GENERATED,validator=validate,scripts=SCRIPTS,added=21,outdir='analysis/input_remaining_v1',extra_tools=(),limits=None):
    path=ROOT/f'poc/output/{stem}.gba';m=read(path.with_suffix('.json'));require_hash(path,m['output_sha256']);rom=path.read_bytes()
    profile=read(ROOT/'project.json')['source_profile'];srcpath=ROOT/profile['filename'];require_hash(srcpath,profile['sha256']);src=srcpath.read_bytes()
    rebuilt=bytearray(src);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];value=bytes.fromhex(w['final_hex']);span=set(range(at,at+n))
        if len(value)!=n or src[at:at+n]!=bytes.fromhex(w['expected_hex']) or occupied&span:raise ValueError('expected writes')
        occupied|=span;rebuilt[at:at+n]=value
    if rebuilt!=rom[:len(src)] or rom[:192]!=src[:192] or len(rom)!=len(src)+m['append_bytes'] or sha(rom[len(src):])!=m['append_sha256']:raise ValueError('ledger/header/append')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    validator(read(ROOT/generated))
    oldpath=ROOT/f'poc/output/{previous}.gba';oldm=read(oldpath.with_suffix('.json'));require_hash(oldpath,oldm['output_sha256']);old=oldpath.read_bytes()
    prior={a['archive']:a for a in oldm['archives']};current={a['archive']:a for a in m['archives']}
    if set(prior)!=set(current) or m['translated_units']!=oldm['translated_units']+added:raise ValueError('selected population')
    for name,a in prior.items():
        b=current[name];op=old[a['rom_offset']:a['rom_offset']+a['compiled_bytes']];np=rom[b['rom_offset']:b['rom_offset']+b['compiled_bytes']]
        if name!='6368E8':
            if op!=np:raise ValueError('prior archive '+name)
        else:
            before=script_spans(op,255);after=script_spans(np,255)
            if any(before[i]!=after[i] for i in range(255) if i not in scripts):raise ValueError('unselected common script')
            if any(before[i]==after[i] for i in scripts):raise ValueError('new text missing')
            if not all(b[k] for k in ('binary_roundtrip','semantic_roundtrip','protected_controls_unchanged')):raise ValueError('roundtrip')
            root=0x08000000+b['rom_offset']
            if any(struct.unpack_from('<I',rom,p)[0]!=root for p in b['pointers']):raise ValueError('common roots')
    for key in ('normal_font_offset','advance_offset'):
        n=(m['extension']['legacy_index_view']+11172+m['extension']['extra_glyph_count'])*(96 if key=='normal_font_offset' else 4)
        a=oldm['extension'][key];b=m['extension'][key]
        if old[a:a+n]!=rom[b:b+n]:raise ValueError('normal font/advance')
    for a,b in ((oldm['fixedcell_extension']['font_offset'],m['fixedcell_extension']['font_offset']),(oldm['fixedcell_extension']['mono_provider']['font_offset'],m['fixedcell_extension']['mono_provider']['font_offset'])):
        if old[a:a+11172*64]!=rom[b:b+11172*64]:raise ValueError('big/mono font')
    for key in ('calendar_frequency_graphics','pet_menu_graphics','equipment_attack_caption','save_title_graphics'):
        a=oldm[key];b=m[key];at=b['source_offset'];n=b.get('stored_bytes',b.get('bytes'))
        if a!=b or old[at:at+n]!=rom[at:at+n]:raise ValueError('graphics')
    verify_final(src,rom,m['keyitem_rom'])
    a=oldm['keyitem_rom'];b=m['keyitem_rom']
    if old[a['rom_offset']:a['rom_offset']+a['rom_bytes']]!=rom[b['rom_offset']:b['rom_offset']+b['rom_bytes']]:raise ValueError('keyitem39')
    out=ROOT/outdir;out.mkdir(exist_ok=True)
    result=dict(passed=True,runtime_verified=False,release_eligible=False,rom_sha256=m['output_sha256'],rom_bytes=len(rom),translated_units=m['translated_units'],added_units=21,unchanged_archives=len(prior)-1,unchanged_common_scripts=255-len(SCRIPTS),source_sha256=profile['sha256'],manifest_sha256=sha(path.with_suffix('.json').read_bytes()),tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('input_remaining.py','report_input_remaining.py','build_development_patch.py','build_roll_pet.py','build_keyitem_full_rom.py')},limits=['Static ROM ledger/header/append/roots/roundtrip audit, original source unchanged. Other59 archive payloads and parent common scripts retained.', 'Normal/big/mono font banks, graphics and keyitem39 retained. No Hangul keyboard/storage candidate installed.', 'New20 headings and notice21 are development drafts. Actual caller/render/VRAM/screen, boot/save/freshload regression and independent rebuild remain pending. Previous ROM runtime evidence is not inherited.'])
    result.update(added_units=added,unchanged_common_scripts=255-len(scripts),previous_rom_sha256=oldm['output_sha256'])
    result['tools'].update({n:sha((ROOT/'tools'/n).read_bytes()) for n in extra_tools})
    if limits is not None:result['limits']=limits
    (out/'artifact_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(f'PASS{added} ROM static audit; NOT runtime',m['output_sha256'],flush=True)
    return result

if __name__=='__main__':main()
