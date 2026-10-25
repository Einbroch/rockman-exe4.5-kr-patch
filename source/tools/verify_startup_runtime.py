"""Bind inspected startup captures and native graphic residency to one ROM."""
import argparse,json
from audit_save_keyboard_fonts import ROOT,digest
from audit_startup_ui import audit
from verify_tpi_index import lz77_decompress

def verify(product,paths=None):
    static=audit(product);rom=product.read_bytes()
    m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    paths=paths or ['poc/runtime/startup-ui-v1-r7-newgame','poc/runtime/startup-ui-v1-r7-mail']
    artifacts={};segments=[]
    for path in paths:
        folder=ROOT/path;result=json.loads((folder/'result.json').read_text(encoding='utf8'))
        if result['rom_sha256']!=static['rom_sha256'] or not result['complete'] or result['steps_captured']!=result['steps_expected'] or result['return_code']!=0:raise ValueError('incomplete/different startup runtime')
        for name,h in result['artifacts'].items():
            f=folder/name
            if digest(f.read_bytes())!=h:raise ValueError('startup evidence changed')
            artifacts[str(f.relative_to(ROOT))]=h
        artifacts[str((folder/'result.json').relative_to(ROOT))]=digest((folder/'result.json').read_bytes())
        segments.append(dict(path=path,actions=result['actions'],rom_sha256=result['rom_sha256'],captures=result['steps_captured'],state_origin=result['state_origin']))
    folder=ROOT/paths[0]
    video=(folder/'step_003_gbaVideoRam.bin').read_bytes();footer=m['startup_footer']
    if video[0x15200:0x15200+footer['bytes']]!=rom[footer['source_offset']:footer['source_offset']+footer['bytes']]:raise ValueError('footer actual native VRAM differs')
    video=(folder/'step_009_gbaVideoRam.bin').read_bytes()
    ram=(folder/'step_009_gbaExtWorkRam.bin').read_bytes()
    residency=[]
    for r,dest,offset in zip(m['startup_welcome']['records'],[video,ram],[0x8000,0x1C800]):
        payload,used=lz77_decompress(rom,r['offset'])
        if used!=r['stored_bytes'] or dest[offset:offset+len(payload)-4]!=payload[4:]:raise ValueError('welcome native decompressed residency differs')
        residency.append(dict(storage_offset=r['offset'],payload_sha256=r['payload_sha256'],observed_ram_offset=offset,bytes=len(payload)-4,byte_identical=True))
    return dict(schema=1,status='LOCAL_DEVELOPMENT_ONLY_NOT_RELEASE',rom_sha256=static['rom_sha256'],rom_bytes=len(rom),title_menu_verified=True,startup_ui_verified=True,fresh_process_reload_verified=False,automatic_hangul_keyboard_installed=False,hangul_persistence_verified=False,full_initial_menu_translation_complete=False,agent_visual_review=['newgame 2: 처음부터 title label','newgame 3: date prompt, Korean weekday, 늘림·줄임/다음/뒤로','newgame 8: date confirmation 예/아니요','newgame 9: PET purchase/name request graphic','newgame 14/15/16/17: gender, age, ten occupations, profile confirmation','newgame 19: 내비 록맨 선택할까요?','mail 1: native nickname plus 메일이야!!'],native_welcome_residency=residency,native_footer_vram_byte_identical=True,segments=segments,static_audit=static,limits=['Kana keyboard and command labels remain native Japanese; automatic Hangul entry/save not installed.','Navi card graphic lettering and NAVI SELECT title remain native.','Only Rockman initial normal route runtime-tested; other selected Navi names static-validated only.','Dynamic native nickname remains unchanged, including Japanese suffix.','No full playthrough or public-release approval.'],artifacts=artifacts)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('preserve runtime report')
    report=verify(ROOT/a.rom);out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS startup route and actual native graphics residency; partial development scope only')
