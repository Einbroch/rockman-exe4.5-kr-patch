"""Fail-closed static audit for the full Rockman story-mail header selection."""
import argparse,json,struct
from pathlib import Path
from archive_scripts import verify_untouched_scripts
from build_visibility_poc import ROOT,sha,require_hash
from first_mail import FULL_HEADER_SCRIPTS,SPECS,asset_path,validate_selected
from verify_tpi_index import lz77_decompress

PRIOR='poc/output/exe45_ko_development_full_mail_body_v1_r2.gba'
PRIOR_SHA='7eee4265c0c0177d65255ecf7c2af31c1cfc0e2301191551e2ec45f67986617d'
PACKAGE='patches/exe45_ko_development_news_mail_20261013.zip'
PACKAGE_SHA='2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6'
MAPPING=[(0,0,1),(1,2,3),(2,4,5),(3,6,7),(8,16,17),(9,18,19),(10,20,21),
         (11,22,23),(12,24,25),(13,26,27),(14,28,29)]

def verify(product:Path,out:Path):
    if out.exists():raise ValueError('preserve full mail header audit')
    rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    if sha(rom)!=m['output_sha256'] or len(rom)!=m['output_bytes']:raise ValueError('product identity')
    source=ROOT/json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']['filename']
    require_hash(source,m['source_sha256']);native=source.read_bytes()
    prior=ROOT/PRIOR;require_hash(prior,PRIOR_SHA);oldrom=prior.read_bytes();old=json.loads(prior.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(ROOT/PACKAGE,PACKAGE_SHA)
    if m['translated_units']!=old['translated_units']+20 or len(m['archives'])!=len(old['archives']):raise ValueError('selection count')
    records={r['archive']:r for r in m['archives']};oldrecords={r['archive']:r for r in old['archives']}
    for archive,row in oldrecords.items():
        if archive=='6DD63C':continue
        current=records[archive]
        for key in ['source_sha256','compiled_sha256','compiled_bytes','translated_units','layout','protected_controls_unchanged']:
            if current[key]!=row[key]:raise ValueError('non-header archive changed '+archive)
    header=records['6DD63C'];oldheader=oldrecords['6DD63C']
    selected=json.loads((ROOT/asset_path('6DD63C','news',True)).read_text(encoding='utf8'));validate_selected(selected)
    if header['translated_units']!=22 or [r['id'] for r in header['layout']]!=[u['id'] for u in selected['units']]:raise ValueError('header denominator')
    if max(x['line_advance_pixels'][0] for x in header['layout'])>88:raise ValueError('header layout')
    payload=lz77_decompress(rom,header['rom_offset'])[0];oldpayload=lz77_decompress(oldrom,oldheader['rom_offset'])[0]
    untouched=verify_untouched_scripts(oldpayload,payload,42,set(FULL_HEADER_SCRIPTS))
    if len(untouched)!=20:raise ValueError('unselected header script count')
    pointers=SPECS['6DD63C']['pointers'];root=0x08000000+header['rom_offset']
    if len(pointers)!=24 or any(struct.unpack_from('<I',rom,p)[0]!=root for p in pointers):raise ValueError('header lookup pointers')
    allowed={i for w in m['expected_writes'] for i in range(w['offset'],w['offset']+w['bytes'])}
    changed=[i for i,(a,b) in enumerate(zip(oldrom[:len(native)],rom[:len(native)])) if a!=b]
    if not m.get('final_diff_audited') or any(i not in allowed for i in changed):raise ValueError('original image changed outside declared writes')
    for key in ['rom_sha256','payload_bytes']:
        if m['keyitem_rom']['mail_rom_reader'][key]!=old['keyitem_rom']['mail_rom_reader'][key]:raise ValueError('full body clone changed')
    clone_shift=m['keyitem_rom']['mail_rom_reader']['clone_address']-old['keyitem_rom']['mail_rom_reader']['clone_address']
    stored_growth=header['compression']['stored_bytes']-oldheader['compression']['stored_bytes']
    if clone_shift!=stored_growth:raise ValueError('full body clone relocation is not exact header growth')
    pairs=[]
    for body,sender,title in MAPPING:
        pairs.append(dict(body_script=body,sender_script=sender,title_script=title,
            sender='I.P.C.' if sender==0 else next(u['translation'] for u in selected['units'] if u['id']==f'6DD63C:{sender}:0'),
            title=next(u['translation'] for u in selected['units'] if u['id']==f'6DD63C:{title}:0')))
    report=dict(schema=1,passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,
        rom=str(product.relative_to(ROOT)),rom_sha256=sha(rom),rom_bytes=len(rom),translated_units=m['translated_units'],
        prior_rom=PRIOR,prior_rom_sha256=PRIOR_SHA,new_header_units=20,total_header_units=22,
        header_payload_bytes=len(payload),header_payload_sha256=sha(payload),header_rom_offset=header['rom_offset'],
        header_destination=SPECS['6DD63C']['destination'],header_capacity=SPECS['6DD63C']['cap'],
        header_pointer_count=len(pointers),header_lookup_root=root,max_line_advance=max(x['line_advance_pixels'][0] for x in header['layout']),
        unselected_header_scripts_preserved=len(untouched),non_header_archives_byte_equivalent=True,
        original_image_changes_limited_to_declared_writes=True,original_image_changed_bytes_vs_prior=len(changed),full_mail_body_clone_unchanged=True,
        full_mail_body_clone_relocation_bytes=clone_shift,
        body_header_static_correspondence=pairs,prior_distribution_package_unchanged=True,
        limits=['Static sender/title pairing follows the native sequential body/header inventories and matching subjects; it is not normal receipt/acquisition proof.',
                'Only the first I.P.C. pair has an existing normal-route runtime receipt. Remaining pairs require isolated header rendering and later normal story acquisition QA.',
                'Wording remains needs_review; automatic Hangul input/save and other Navi mail archives remain unresolved. No patch package was created.'])
    out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS full story-mail header22 / +20 / non-header archives equivalent / package untouched')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    verify(ROOT/a.rom,ROOT/a.out)
