"""Exact full120 clone versus bounded77 and prior ROM; never release QA."""
import argparse,json
from full_mail_body import ROOT,ASSET,payload
from build_visibility_poc import sha,require_hash
from audit_startup_ui import audit
from keyitem_rom_data import verify_final
from archive_scripts import verify_untouched_scripts,script_spans
from verify_tpi_index import lz77_decompress

def verify(product,out):
    if out.exists():raise ValueError('preserve full mail audit')
    report=audit(product);rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    source=ROOT/json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']['filename']
    require_hash(source,'588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    verify_final(source.read_bytes(),rom,m['keyitem_rom'])
    prior=ROOT/'poc/output/exe45_ko_development_mail_rom_reader_v1.gba'
    require_hash(prior,'0e25d98bd1ff7c5cda5516a475f49b2936c55ed9bfa1aa8c9640f010a1cae683')
    old=json.loads(prior.with_suffix('.json').read_text(encoding='utf8'));prev=prior.read_bytes()
    records={r['archive']:r for r in m['archives']}
    for r in old['archives']:
        n=records[r['archive']]
        if any(r[k]!=n[k] for k in ['compiled_sha256','compiled_bytes','translated_units','source_sha256']):raise ValueError('bounded archive changed '+r['archive'])
    body,root=payload(rom,m);bounded=lz77_decompress(rom,records['6DD9AC']['rom_offset'])[0]
    preserved=verify_untouched_scripts(bounded,body,32,{11,12,13,14})
    old_body,old_root=payload(prev,old)
    prior_preserved=verify_untouched_scripts(old_body,body,32,{11,12,13,14})
    prior_runtime=ROOT/'analysis/mail_rom_reader_v1/runtime_verification.json'
    prior_receipt=json.loads(prior_runtime.read_text(encoding='utf8'))
    if prior_receipt['rom_sha256']!=sha(prev) or not prior_receipt['mail_rom_reader_diagnostic_verified']:raise ValueError('prior54-page evidence identity')
    equivalent=[]
    for script in [1,2,3,8,9,10]:
        before=int.from_bytes(old_body[2*script:2*script+2],'little');after=int.from_bytes(body[2*script:2*script+2],'little')
        if old_root!=root or before!=after:raise ValueError('prior diagnostic stream address changed')
        equivalent.append(dict(script=script,root=root,relative_offset=after,byte_identical=True,
            stream_sha256=sha(script_spans(body,32)[script])))
    if len(bounded)!=7005 or len(body)!=8531 or m['translated_units']!=old['translated_units']+43:raise ValueError('full mail counts/capacity')
    if m['keyitem_rom']['rom_sha256']!=old['keyitem_rom']['rom_sha256']:raise ValueError('keyitem raw clone changed')
    # Only veneer12 bytes may change inside the already-patched8MiB image.
    if any(a!=b and not 0x4FB4C<=i<0x4FB58 for i,(a,b) in enumerate(zip(prev[:len(source.read_bytes())],rom))):raise ValueError('full mail original image escaped shared selector')
    package=ROOT/'patches/exe45_ko_development_news_mail_20261013.zip'
    require_hash(package,'2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6')
    report.update(full_mail_clone_verified=True,new_literals=43,full_mail_literal_count=120,
        bounded_ram_payload_bytes=len(bounded),raw_rom_payload_bytes=len(body),raw_rom_root=root,
        native_guard_retained=True,previous_bounded_archives_byte_identical=True,
        preserved_raw_script_count=len(preserved),keyitem_clone_unchanged=True,
        original_image_changes_limited_to_shared_selector_veneer=True,prior_distribution_package_unchanged=True,
        player_name_layout_proof=m['keyitem_rom']['mail_rom_reader']['archive']['mail_player_name_proof'])
    report['prior54_page_consumption_equivalence']=dict(prior_rom_sha256=sha(prev),
        prior_report=str(prior_runtime.relative_to(ROOT)),prior_report_sha256=sha(prior_runtime.read_bytes()),
        scripts=equivalent,raw_root_and_stream_addresses_identical=True,bounded_loader_payloads_identical=True,
        limits='Prior54 diagnostic pages were NOT rerun on this ROM; byte/address-equivalent consumed content only. Shared initializer has fresh CPU867/first23/new39 tests in separate reports.')
    out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS full120 raw clone /43 new /bounded7005 unchanged /reproducible /no package')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args();verify(ROOT/a.rom,ROOT/a.out)
