"""Verify diagnostic scope only, never mailbox acquisition or title identity."""
import argparse,json,struct
from first_mail import ROOT,asset_path,SPECS,mode_for_manifest
from build_visibility_poc import sha
from verify_tpi_index import lz77_decompress
from korean_codec import encode_character

def verify(product,out,prefix,news=False):
    rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    report=json.loads(out.read_text(encoding='utf8'))
    if report['rom_sha256']!=sha(rom) or not report.get('first_mail_verified'):raise ValueError('current normal-route evidence required')
    units=json.loads((ROOT/asset_path('6DD9AC',mode_for_manifest(m))).read_text(encoding='utf8'))['units']
    records={r['archive']:r for r in m['archives']};payloads={a:lz77_decompress(rom,records[a]['rom_offset'])[0] for a in SPECS}
    from full_mail_body import payload
    body,dest=payload(rom,m);table={}
    for line in (ROOT/'poc/build'/product.stem/'plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            key,value=line.split('=',1)
            if len(value)==1:table[value]=bytes.fromhex(key)
    dest=m.get('keyitem_rom',{}).get('mail_rom_reader',{}).get('clone_address',dest)
    observations=[]
    for script in ((8,9,10) if news else (1,2,3)):
        selected=[u for u in units if int(u['id'].split(':')[1])==script]
        begin,end=struct.unpack_from('<2H',body,script*2);span=body[begin:end];ends={};bookmarks={};previous=None
        for u in selected:
            encoded=b''.join(b'\xE8' if c=='\n' else encode_character(c) if '\uac00'<=c<='\ud7a3' or c==',' else table[c] for c in u['translation'])
            pos=span.find(encoded)
            if pos<0 or span.find(encoded,pos+1)>=0 or span[pos+len(encoded):pos+len(encoded)+2]!=bytes.fromhex('e600'):raise ValueError('Official literal/wait boundary '+u['id'])
            endpoint=dest+begin+pos+len(encoded)
            if previous is not None and body[previous-dest+2]!=0xF1:raise ValueError('Official native page clear')
            ends[endpoint]=u['id'];bookmarks[endpoint]=dest+begin if previous is None else previous+3;previous=endpoint
        folder=ROOT/f'poc/runtime/{prefix}-official{script}';r=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r.get('normal_play_checkpoint_eligible') is not False or r['official_mail_diagnostic']['aliases']!=1 or r['official_mail_diagnostic']['displayed_script']!=script:raise ValueError('Official diagnostic binding')
        seen=[];returned=False
        for n in r['capture_steps']:
            ram=(folder/f'step_{n:03}_gbaExtWorkRam.bin').read_bytes();ptr,base,bookmark=struct.unpack_from('<3I',ram,0xFA4C)
            if base!=dest:continue
            if ptr==previous+2 and ram[0xFA20]==0:returned=True
            if ptr not in ends:continue
            if bookmark!=bookmarks[ptr]:raise ValueError('Official page bookmark')
            for a,p in payloads.items():
                at=SPECS[a]['destination']-0x02000000
                if ram[at:at+len(p)]!=p:raise ValueError('Official native decompressed bytes '+a)
            seen.append(ends[ptr]);observations.append(dict(script=script,step=n,id=ends[ptr],wait_pointer=ptr,page_bookmark=bookmark,native_loaded_bytes_identical=True))
        if seen!=[u['id'] for u in selected] or not returned:raise ValueError(f'Official pages/order/exit incomplete: {script}, {seen}, returned={returned}')
        for name,h in r['artifacts'].items():
            path=folder/name
            if sha(path.read_bytes())!=h:raise ValueError('Official evidence changed')
            report['artifacts'][str(path.relative_to(ROOT))]=h
        report['artifacts'][str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
    if news:
        report.update(news_mail_display_diagnostic_verified=True,news_mail_added_units=22,news_mail_observations=observations,news_mail_acquisition_verified=False,news_mail_quest_progression_verified=False)
        report['limits']+=['News1..3 body display tested by isolated table alias. Acquisition, corresponding header and normal quest progression NOT tested. Original callBeginStoryQuest executes in isolated sessions.']
        report['agent_visual_review']+=['News1..3: all22 body pages, text/arrow placement and native exit inspected; diagnostic header intentionally not corresponding.']
    else:
        report.update(official_mail_display_diagnostic_verified=True,official_mail_added_units=32,official_mail_observations=observations,official_mail_acquisition_verified=False,official_mail_header_correspondence_verified=False)
        report['limits']+=['Official bodies1..3 inspected through one quarantined native table alias after real decompression. Acquisition conditions and corresponding sender/title NOT tested; first-letter header stays in diagnostic. Original flagClear executes only in isolated runtime.']
        report['agent_visual_review']+=['Official diagnostic bodies1..3: all32 literal pages, text/arrow placement, native exit inspected; header intentionally not corresponding.']
    if dest!=SPECS['6DD9AC']['destination']:
        report['mail_rom_reader_diagnostic_verified']=bool(report.get('official_mail_display_diagnostic_verified') and report.get('news_mail_display_diagnostic_verified'))
        report['mail_rom_reader_root']=dest
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS '+('News22' if news else 'Official32')+' diagnostic page boundaries/native residency/exit; NOT acquisition proof')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--prefix',required=True);p.add_argument('--news',action='store_true');a=p.parse_args();verify(ROOT/a.rom,ROOT/a.out,a.prefix,a.news)
