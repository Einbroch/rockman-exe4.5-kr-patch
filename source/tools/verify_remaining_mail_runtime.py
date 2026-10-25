"""39 diagnostic pages /43 new literals; no mail receipt/progression claim."""
import argparse,json,struct
from full_mail_body import ROOT,ASSET,SPECS,payload
from build_visibility_poc import sha,require_hash
from verify_tpi_index import lz77_decompress
from korean_codec import encode_character

def verify(product,prefix,out,visual=False):
    if not visual:raise ValueError('inspect all39 screenshots before attesting visual review')
    if out.exists():raise ValueError('preserve remaining-mail report')
    rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'));require_hash(product,m['output_sha256'])
    mail=m['keyitem_rom']['mail_rom_reader']
    if not mail.get('archive') or mail['archive']['translated_units']!=120:raise ValueError('full120 explicit clone')
    units=json.loads((ROOT/ASSET).read_text(encoding='utf8'))['units'];body,root=payload(rom,m)
    table={}
    for line in (ROOT/'poc/build'/product.stem/'plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            k,v=line.split('=',1)
            if len(v)==1:table[v]=bytes.fromhex(k)
    records={r['archive']:r for r in m['archives']}
    ram_payloads={a:lz77_decompress(rom,records[a]['rom_offset'])[0] for a in SPECS}
    if len(ram_payloads['6DD9AC'])!=7005 or ram_payloads['6DD9AC'][:16].hex()!=mail['guard_header_hex']:raise ValueError('bounded77 RAM retained')
    observations=[];artifacts={};joined=0
    for script,pages in [(11,13),(12,9),(13,8),(14,9)]:
        begin,end=struct.unpack_from('<2H',body,script*2);span=body[begin:end]
        selected=[u for u in units if int(u['id'].split(':')[1])==script]
        cursor=0;ends={};pending=[];bookmark=root+begin;name_page=False
        for u in selected:
            encoded=b''.join(b'\xE8' if c=='\n' else encode_character(c) if '\uac00'<=c<='\ud7a3' or c==',' else table[c] for c in u['translation'])
            pos=span.find(encoded,cursor)
            if pos<0:raise ValueError('ordered literal absent '+u['id'])
            # A dynamic insert between literals is the preserved F90C1F command.
            if b'\xf9\x0c\x1f' in span[cursor:pos]:name_page=True
            cursor=pos+len(encoded);pending.append(u['id'])
            if span[cursor:cursor+2]==b'\xe6\x00':
                endpoint=root+begin+cursor
                ends[endpoint]=dict(ids=pending,bookmark=bookmark,name_page=name_page)
                pending=[];name_page=False;bookmark=endpoint+3
        if len(ends)!=pages or pending:raise ValueError('remaining page grouping')
        folder=ROOT/f'poc/runtime/{prefix}-official{script}'
        r=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r.get('normal_play_checkpoint_eligible') is not False or r['official_mail_diagnostic']['aliases']!=1 or r['official_mail_diagnostic']['displayed_script']!=script:raise ValueError('quarantined exact-ROM receipt')
        seen=[];returned=False
        for n in r['capture_steps']:
            ram=(folder/f'step_{n:03}_gbaExtWorkRam.bin').read_bytes()
            ptr,base,bm=struct.unpack_from('<3I',ram,0xFA4C)
            if base!=root:continue
            if ptr==max(ends)+2 and ram[0xFA20]==0:returned=True
            if ptr not in ends:continue
            page=ends[ptr]
            if bm!=page['bookmark']:raise ValueError('remaining native page bookmark')
            for a,p in ram_payloads.items():
                at=SPECS[a]['destination']-0x02000000
                if ram[at:at+len(p)]!=p:raise ValueError('remaining native loader bytes '+a)
            item=dict(script=script,step=n,ids=page['ids'],wait_pointer=ptr,page_bookmark=bm,native_loaded_bytes_identical=True)
            if page['name_page']:
                name=ram[0xE51:0xE5E];i=0;count=0
                while i<len(name) and name[i]!=0xE5:
                    i+=2 if name[i]==0xE4 else 1;count+=1
                if i>=len(name) or count>6:raise ValueError('native player name extent')
                item.update(player_name_hex=name[:i+1].hex(),native_name_glyphs=count);joined+=1
            seen.append(ptr);observations.append(item)
        if seen!=list(ends) or not returned:raise ValueError('remaining ordered pages and return '+str(script))
        for name,h in r['artifacts'].items():
            p=folder/name;require_hash(p,h);artifacts[str(p.relative_to(ROOT))]=h
        artifacts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
    if len(observations)!=39 or joined!=5:raise ValueError('remaining literal/name coverage')
    report=dict(passed=True,rom_sha256=sha(rom),added_literals=43,diagnostic_pages=39,name_insert_pages=5,
        all_pages_agent_visual_reviewed=True,observations=observations,artifacts=artifacts,
        bounded_ram_payload_bytes=7005,raw_rom_payload_bytes=len(body),
        normal_mail_acquisition_verified=False,normal_quest_progression_verified=False,corresponding_header_verified=False,
        limits=['One native script-table read alias per isolated session; original quest/flag commands execute there only.',
                'Human wording/presentation approval pending; no custom Hangul save/input ABI adopted.'])
    out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS remaining43 literals /39 diagnostic pages /5 native name inserts; NOT acquisition QA')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--out',required=True);p.add_argument('--visual-reviewed',action='store_true');a=p.parse_args()
    verify(ROOT/a.rom,a.prefix,ROOT/a.out,a.visual_reviewed)
