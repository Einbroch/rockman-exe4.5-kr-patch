"""Exact-artifact card selection evidence plus inherited startup regression."""
import argparse,json,struct
from audit_save_keyboard_fonts import ROOT,digest
from verify_tpi_index import lz77_decompress
from verify_native_keyboard_runtime import run

def verify(product,out,card_path,observations):
    folder=ROOT/card_path
    result=json.loads((folder/'result.json').read_text(encoding='utf8'))
    rom=product.read_bytes();m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    if not result['complete'] or result['rom_sha256']!=digest(rom) or result['steps_expected']!=result['steps_captured']:raise ValueError('Navi runtime binding')
    payload,_=lz77_decompress(rom,m['navi_card_graphics']['source_offset'])
    records=[]
    native_palette=(ROOT/'poc/runtime/native-keyboard-labels-v1-complete/step_023_gbaPaletteRam.bin').read_bytes()[928:960]
    for step,index in observations:
        prefix=folder/f'step_{step:03}'
        video=prefix.with_name(prefix.name+'_gbaVideoRam.bin').read_bytes()
        oam=prefix.with_name(prefix.name+'_gbaSpriteRam.bin').read_bytes()
        palette=prefix.with_name(prefix.name+'_gbaPaletteRam.bin').read_bytes()
        if video[0x15000:0x15000+len(payload)-4]!=payload[4:]:raise ValueError('Navi full bank residency differs')
        if palette[928:960]!=native_palette:raise ValueError('Navi native palette differs')
        attr0,attr1,attr2=struct.unpack_from('<3H',oam,0)
        if (attr0>>14,attr1>>14,attr2>>12,attr2&1023)!=(1,1,13,640+index*4):raise ValueError('Navi selected OAM index/shape/palette differs')
        records.append(dict(step=step,index=index,name=m['navi_card_graphics']['records'][index]['translation'],tile_base=attr2&1023,x=attr1&511,y=attr0&255,full_bank_resident=True,native_palette_identical=True))
    if {index for _,index in observations}!={0,1,2,8}:raise ValueError('Navi four selectable identities incomplete')
    report=json.loads(out.read_text(encoding='utf8'))
    for name,h in result['artifacts'].items():
        p=folder/name
        if digest(p.read_bytes())!=h:raise ValueError('Navi runtime evidence changed')
        report['artifacts'][str(p.relative_to(ROOT))]=h
    report['artifacts'][str((folder/'result.json').relative_to(ROOT))]=digest((folder/'result.json').read_bytes())
    report.update(navi_card_graphics_verified=True,navi_card_graphics_count=21,navi_selection_observations=records)
    report['limits']=[s for s in report['limits'] if not s.startswith('Navi card graphic') and not s.startswith('Only Rockman initial')]
    report['limits']+=['NAVI SELECT title remains English.','Four native unlocked card names tested by normal selection; remaining 17 names static-validated and full-bank upload proven, not unlocked/playtested.']
    report['agent_visual_review']+=['cards: four normal selectable portraits/names and confirmation/cancel inspected; no portrait/character substitution']
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS 21-name native bank residency and four selectable OAM identities')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--cards',required=True);p.add_argument('--observations',required=True);a=p.parse_args()
    product=ROOT/a.rom;out=ROOT/a.out
    run(product,out,[6,7,9],['poc/runtime/navi-card-names-v1-boot','poc/runtime/navi-card-names-v1-complete'],'poc/runtime/navi-card-names-v1-pagecycle')
    verify(product,out,a.cards,[tuple(map(int,v.split(':'))) for v in a.observations.split(',')])
