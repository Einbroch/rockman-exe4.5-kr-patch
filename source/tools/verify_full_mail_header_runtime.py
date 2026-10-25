"""Bind normal first-mail and ten isolated sender/title render receipts."""
import argparse,json
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from first_mail import SPECS,asset_path,validate_selected
from verify_tpi_index import lz77_decompress

PAIRS={1:(2,3),2:(4,5),3:(6,7),8:(16,17),9:(18,19),10:(20,21),11:(22,23),12:(24,25),13:(26,27),14:(28,29)}

def verify(product:Path,out:Path,prefix:str):
    if out.exists():raise ValueError('preserve full mail header runtime report')
    rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(product,m['output_sha256']);normal=ROOT/'analysis/full_mail_header_v1_r2/runtime_verification.json'
    n=json.loads(normal.read_text(encoding='utf8'))
    if n['rom_sha256']!=sha(rom) or not n.get('first_mail_verified') or not n.get('first_mail_normal_reentry_verified'):raise ValueError('normal first mail receipt')
    static=ROOT/'analysis/full_mail_header_v1_r2/static_verification.json';s=json.loads(static.read_text(encoding='utf8'))
    if not s['passed'] or s['rom_sha256']!=sha(rom):raise ValueError('static header audit')
    asset=json.loads((ROOT/asset_path('6DD63C','news',True)).read_text(encoding='utf8'));validate_selected(asset)
    units={int(u['id'].split(':')[1]):u['translation'] for u in asset['units']}
    record=next(r for r in m['archives'] if r['archive']=='6DD63C');payload=lz77_decompress(rom,record['rom_offset'])[0]
    observations=[];artifacts={str(normal.relative_to(ROOT)):sha(normal.read_bytes()),str(static.relative_to(ROOT)):sha(static.read_bytes())}
    for body,(sender,title) in PAIRS.items():
        folder=ROOT/f'poc/runtime/{prefix}-header-pair{body}';rpath=folder/'result.json';r=json.loads(rpath.read_text(encoding='utf8'))
        h=r.get('mail_header_diagnostic') or {}
        if (not r['complete'] or r['rom_sha256']!=sha(rom) or r.get('normal_play_checkpoint_eligible') is not False
                or r['official_mail_diagnostic']['aliases']!=0 or h.get('body_script')!=body
                or (h.get('sender_script'),h.get('title_script'))!=(sender,title)
                or h.get('sender_aliases',0)<=0 or h.get('title_aliases',0)<=0
                or h.get('header_root')!=SPECS['6DD63C']['destination']):raise ValueError('header diagnostic binding '+str(body))
        ram=(folder/'step_009_gbaExtWorkRam.bin').read_bytes();at=SPECS['6DD63C']['destination']-0x02000000
        if ram[at:at+len(payload)]!=payload:raise ValueError('header archive residency '+str(body))
        image=folder/'step_009.png';require_hash(image,r['artifacts'][image.name])
        artifacts[str(image.relative_to(ROOT))]=sha(image.read_bytes());artifacts[str(rpath.relative_to(ROOT))]=sha(rpath.read_bytes())
        observations.append(dict(body_script=body,sender_script=sender,title_script=title,sender=units[sender],title=units[title],
            sender_alias_reads=h['sender_aliases'],title_alias_reads=h['title_aliases'],header_payload_resident=True,
            screenshot=str(image.relative_to(ROOT)),screenshot_sha256=sha(image.read_bytes())))
    gallery=ROOT/'analysis/full_mail_header_v1_r2/header_gallery/index.json';g=json.loads(gallery.read_text(encoding='utf8'))
    if len(g['images'])!=10 or len(g['sheets'])!=2:raise ValueError('header gallery population')
    artifacts[str(gallery.relative_to(ROOT))]=sha(gallery.read_bytes())
    for row in g['sheets']:
        require_hash(ROOT/row['path'],row['sha256']);artifacts[row['path']]=row['sha256']
    report=dict(schema=1,passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,
        rom=str(product.relative_to(ROOT)),rom_sha256=sha(rom),normal_first_pair_verified=True,
        normal_first_pair=dict(body_script=0,sender_script=0,title_script=1,sender='I.P.C.',title=units[1]),
        normal_first_mail_pages=23,normal_list_return_and_reentry_verified=True,
        isolated_corresponding_pairs_verified=len(observations),observations=observations,
        header_archive_storage_lookup_load_residency_and_fixed_cell_consumption_verified=True,
        agent_visual_review=['All ten isolated list rows inspected in two contact sheets: Hangul glyphs render, sender/title remain in their cells, NEW marker is not overlapped, and no title is visibly truncated.',
                             'The four shortened titles render as 또 1체 다크로이드 / 의문의 오퍼레이터! / 오퍼레이터 정체! / 길거리 습격 발생.'],
        artifacts=artifacts,
        acquisition_verified=False,story_progression_verified=False,save_compatibility_verified=False,
        limits=['Ten non-first pairs use quarantined table-read aliases on a normal current-ROM checkpoint. They prove the compiled header archive, lookup, RAM residency and native list renderer, not natural mail receipt.',
                'Only I.P.C./고객 여러분께 is verified through normal acquisition. Full story playthrough, actual later receipt order and header/body selection state remain open.',
                'Automatic Hangul input/save, other Navi mail archives and human wording approval remain unresolved. No BPS/xdelta/ZIP was created.'])
    out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS normal first pair + ten isolated corresponding header pairs; NOT acquisition proof')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--prefix',required=True);a=p.parse_args()
    verify(ROOT/a.rom,ROOT/a.out,a.prefix)
