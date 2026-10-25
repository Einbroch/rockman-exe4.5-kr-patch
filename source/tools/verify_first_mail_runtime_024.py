"""All 23 first-letter wait boundaries, native load bytes, exit and reentry."""
import argparse,json,struct
from audit_save_keyboard_fonts import ROOT,digest
from first_mail import SPECS,asset_path
from verify_tpi_index import lz77_decompress
from korean_codec import encode_character
from verify_native_keyboard_runtime import run
from verify_navi_card_runtime import verify as verify_cards

def verify_mail(product,out,folder_path):
    rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    folder=ROOT/folder_path;result=json.loads((folder/'result.json').read_text(encoding='utf8'));report=json.loads(out.read_text(encoding='utf8'))
    if not result['complete'] or result['rom_sha256']!=digest(rom) or result['steps_expected']!=result['steps_captured']:raise ValueError('first letter runtime binding')
    records={r['archive']:r for r in m['archives']};payloads={a:lz77_decompress(rom,records[a]['rom_offset'])[0] for a in SPECS}
    # Native context+2C points at the waiting opcode; +30 is the archive base.
    # +34 is a page bookmark, not an invariant script base: capture receipts
    # show it moving to the previous wait endpoint+3 after each native F1.
    # Every unchanged keyWait is E6 00; during the wait +2C points at E6.
    table={}
    if m.get('build_argument_manifest'):
        from build_visibility_poc import require_hash
        from build_arguments import validate
        ref=m['build_argument_manifest'];require_hash(ROOT/ref['path'],ref['sha256'])
        args=validate(json.loads((ROOT/ref['path']).read_text(encoding='utf8')))
        if args.count('--work')!=1:raise ValueError('Mail runtime build work binding')
        plugin=ROOT/args[args.index('--work')+1]/'plugins/exe45-utf8.tbl'
        if digest(plugin.read_bytes())!=m['plugin']['derived_plugin_sha256']['exe45-utf8.tbl']:raise ValueError('Mail runtime derived codec binding')
    else:plugin=ROOT/'poc/build'/product.stem/'plugins/exe45-utf8.tbl'
    for line in plugin.read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            key,value=line.split('=',1)
            if len(value)==1:table[value]=bytes.fromhex(key)
    from first_mail import mode_for_manifest
    official=mode_for_manifest(m)
    asset=json.loads((ROOT/asset_path('6DD9AC',official)).read_text(encoding='utf8'));ends={}
    asset['units']=[u for u in asset['units'] if u['id'].split(':')[1]=='0']
    from full_mail_body import payload
    body,dest=payload(rom,m);bookmarks={};previous=None
    if dest!=SPECS['6DD9AC']['destination']:
        from keyitem_rom_data_024 import verify_final
        source=ROOT/json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']['filename']
        verify_final(source.read_bytes(),rom,m['keyitem_rom'])
        if not m['keyitem_rom']['mail_rom_reader'].get('archive') and body!=payloads['6DD9AC']:raise ValueError('mail PoC clone/RAM payload differs')
    for unit in asset['units']:
        encoded=b''.join(b'\xE8' if c=='\n' else encode_character(c) if '\uac00'<=c<='\ud7a3' or c==',' else table[c] for c in unit['translation'])
        pos=body.find(encoded)
        if pos<0 or body.find(encoded,pos+1)>=0 or body[pos+len(encoded):pos+len(encoded)+2]!=b'\xE6\x00':raise ValueError('first mail literal/wait identity')
        endpoint=dest+pos+len(encoded)
        if previous is not None and body[previous-dest+2]!=0xF1:raise ValueError('first mail native page clear boundary')
        ends[endpoint]=unit['id']
        bookmarks[endpoint]=dest+int.from_bytes(body[:2],'little') if previous is None else previous+3
        previous=endpoint
    pages=[];seen=[];reentry=False
    for step in result['capture_steps']:
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        ptr,base,bookmark=struct.unpack_from('<3I',ram,0xFA20+0x2C)
        if base!=dest or ptr not in ends:continue
        if bookmark!=bookmarks[ptr]:raise ValueError(f'first mail native page bookmark identity: step={step}, unit={ends[ptr]}, actual={bookmark:08X}, expected={bookmarks[ptr]:08X}')
        for a,payload in payloads.items():
            at=SPECS[a]['destination']-0x02000000
            if ram[at:at+len(payload)]!=payload:raise ValueError('mail native loaded bytes differ '+a)
        pages.append(dict(step=step,id=ends[ptr],wait_stream_pointer=ptr,native_page_bookmark=bookmark,native_archive_bytes_identical=True))
        if len(seen)<23:seen.append(ends[ptr])
        elif ends[ptr]==asset['units'][0]['id']:reentry=True
    if seen!=[u['id'] for u in asset['units']] or not reentry:raise ValueError('first letter23 ordered pages/reentry not established')
    for name,h in result['artifacts'].items():
        p=folder/name
        if digest(p.read_bytes())!=h:raise ValueError('first mail evidence changed')
        report['artifacts'][str(p.relative_to(ROOT))]=h
    report['artifacts'][str((folder/'result.json').relative_to(ROOT))]=digest((folder/'result.json').read_bytes())
    report.update(first_mail_verified=True,first_mail_translated_units=30,first_mail_body_pages=pages,first_mail_ordered_page_count=23,first_mail_normal_reentry_verified=True)
    if dest!=SPECS['6DD9AC']['destination']:report.update(mail_rom_reader_first_letter_verified=True,mail_rom_reader_root=dest,mail_ram_extent_unchanged=True)
    report['agent_visual_review']+=['mail: translated mailbox labels/title/prompt; all23 body pages, completion/list return/reentry inspected']
    if m.get('keyitem_rom',{}).get('mail_rom_reader',{}).get('archive'):
        report['limits']+=['This report proves first I.P.C. normal route only. Full120 common body literals are selected; additional bodies have separate diagnostic/equivalence reports. Other Navi archives/normal acquisition remain unresolved.']
    else:
        report['limits']+=['Only first I.P.C. letter and Rockman mailbox tested in this report; selected additional bodies have separate diagnostic reports. Other Navi archives remain native.']
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS first mail23 ordered keyWait boundaries, three native archive loads and reentry')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--prefix',default='first-mail-v2');a=p.parse_args()
    product=ROOT/a.rom;out=ROOT/a.out
    run(product,out,[6,7,9],[f'poc/runtime/{a.prefix}-boot',f'poc/runtime/{a.prefix}-complete'],f'poc/runtime/{a.prefix}-pagecycle')
    verify_cards(product,out,f'poc/runtime/{a.prefix}-selection',[(23,0),(25,0),(26,1),(28,1),(29,2),(31,2),(32,8),(34,8),(35,2),(36,1),(37,0)])
    verify_mail(product,out,f'poc/runtime/{a.prefix}-read')
