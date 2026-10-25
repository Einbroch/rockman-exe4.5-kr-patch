"""Own024 native startup/keyboard residency, cards and first-mail regression.

Uses current024 static audit, not the historical startup count/lineage model.
Visual approval is separate from these mechanical runtime observations.
"""
import argparse
import json
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_navi_card_runtime import verify as verify_cards
from verify_first_mail_runtime_024 import verify_mail


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_024_v1.gba')
    p.add_argument('--prefix',default='pending500-024-v1');p.add_argument('--out',default='analysis/pending500_024_v1/normal_runtime.json');a=p.parse_args()
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    proof=read('analysis/pending500_024_v1/integration_pre_repro.json')
    if not proof['passed'] or proof['rom_sha256']!=sha(rom):raise ValueError('024 independent static prerequisite')
    folders={name:ROOT/'poc/runtime'/(a.prefix+'-'+name) for name in ('boot','pagecycle','complete','read','selection')}
    artifacts={};segments=[]
    for name,folder in folders.items():
        receipt=read(folder/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['steps_captured']!=receipt['steps_expected'] or receipt['return_code']!=0:
            raise ValueError('024 own-ROM normal receipt '+name)
        for path,h in receipt['artifacts'].items():
            require_hash(folder/path,h);artifacts[str((folder/path).relative_to(ROOT))]=h
        artifacts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
        segments.append(dict(segment=name,actions=receipt['actions'],captures=receipt['steps_captured'],state_origin=receipt['state_origin']))
    observations=[]
    for page,step in zip(m['native_keyboard_labels']['pages'],(6,7,9)):
        video=(folders['pagecycle']/f'step_{step:03}_gbaVideoRam.bin').read_bytes()
        bank=rom[page['bank_offset']:page['bank_offset']+page['bank_bytes']]
        mapping=rom[page['map_offset']:page['map_offset']+1200]
        expected=list(struct.unpack('<600H',mapping))
        for y in (4,5):
            for x in range(3,13):expected[y*30+x]=0xA1C0+2*(x-3)+y-4
            for x in range(17,27):expected[y*30+x]=0xB180+2*(x-17)+y-4
        actual=b''.join(video[0xF000+y*64:0xF000+y*64+60] for y in range(20))
        if video[0x8000:0x8000+len(bank)]!=bank or actual!=struct.pack('<600H',*expected):
            raise ValueError('024 native keyboard bank/map/field overlay')
        observations.append(dict(page=page['page'],step=step,bank_vram_byte_identical=True,map_560_source_cells_and_40_native_field_cells_verified=True))
    boot=folders['boot'];video=(boot/'step_003_gbaVideoRam.bin').read_bytes();footer=m['startup_footer']
    if video[0x15200:0x15200+footer['bytes']]!=rom[footer['source_offset']:footer['source_offset']+footer['bytes']]:
        raise ValueError('024 startup footer native upload')
    video=(boot/'step_009_gbaVideoRam.bin').read_bytes();ram=(boot/'step_009_gbaExtWorkRam.bin').read_bytes()
    for record,dest,offset in zip(m['startup_welcome']['records'],(video,ram),(0x8000,0x1C800)):
        payload,used=lz77_decompress(rom,record['offset'])
        if used!=record['stored_bytes'] or dest[offset:offset+len(payload)-4]!=payload[4:]:
            raise ValueError('024 startup welcome decompressed residency')
    out=ROOT/a.out
    frozen_write(out,dict(schema=1,passed=True,rom_sha256=sha(rom),artifacts=artifacts,segments=segments,
        native_keyboard_labels_verified=True,native_keyboard_pages=observations,
        native_footer_and_welcome_residency_verified=True,agent_visual_review=[],visual_review_pending=True,
        release_eligible=False,limits=['Native kana entry regression only; automatic Hangul composition/commit/save/redisplay unfinished.']))
    verify_cards(rp,out,str(folders['selection'].relative_to(ROOT)),[(23,0),(25,0),(26,1),(28,1),(29,2),(31,2),(32,8),(34,8),(35,2),(36,1),(37,0)])
    verify_mail(rp,out,str(folders['read'].relative_to(ROOT)))
    # Legacy helpers add visual-review prose; do not promote that prose to an
    # observation before the actual024 contact sheets are inspected separately.
    report=read(out);report['agent_visual_review']=[];report['visual_review_pending']=True
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PASS024 own boot/startup/native keyboard3pages/cards4/first-mail23waits+reentry; visual review separate')


if __name__=='__main__':main()
