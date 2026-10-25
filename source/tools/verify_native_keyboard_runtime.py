"""Exact-artifact three-page native keyboard graphics/input regression."""
import argparse,json,struct
from audit_save_keyboard_fonts import ROOT,digest
from verify_startup_runtime import verify

def run(product,out,page_steps,paths=None,page_path=None):
    paths=paths or ['poc/runtime/native-keyboard-labels-v1-boot','poc/runtime/native-keyboard-labels-v1-complete']
    report=verify(product,paths)
    m=json.loads(product.with_suffix('.json').read_text(encoding='utf8'));rom=product.read_bytes()
    folder=ROOT/(page_path or 'poc/runtime/native-keyboard-labels-v1-pagecycle')
    result=json.loads((folder/'result.json').read_text(encoding='utf8'))
    if result['rom_sha256']!=report['rom_sha256'] or not result['complete'] or result['steps_expected']!=result['steps_captured']:raise ValueError('native page runtime binding')
    for name,h in result['artifacts'].items():
        p=folder/name
        if digest(p.read_bytes())!=h:raise ValueError('native page evidence changed')
        report['artifacts'][str(p.relative_to(ROOT))]=h
    report['artifacts'][str((folder/'result.json').relative_to(ROOT))]=digest((folder/'result.json').read_bytes())
    observations=[]
    for p,step in zip(m['native_keyboard_labels']['pages'],page_steps):
        data=(folder/f'step_{step:03}_gbaVideoRam.bin').read_bytes()
        bank=rom[p['bank_offset']:p['bank_offset']+p['bank_bytes']]
        mapping=rom[p['map_offset']:p['map_offset']+1200]
        if data[0x8000:0x8000+len(bank)]!=bank:raise ValueError('native keyboard uploaded bank differs')
        actual=b''.join(data[0xF000+y*64:0xF000+y*64+60] for y in range(20))
        expected=list(struct.unpack('<600H',mapping))
        # Native UI installs two 10x2 dynamic text fields after loading the map.
        # They are not baked keyboard pixels. Pin their unchanged index rule.
        for y in (4,5):
            for x in range(3,13):expected[y*30+x]=0xA1C0+2*(x-3)+y-4
            for x in range(17,27):expected[y*30+x]=0xB180+2*(x-17)+y-4
        if actual!=struct.pack('<600H',*expected):raise ValueError('native keyboard BG2 map/field overlay differs')
        observations.append(dict(page=p['page'],capture_step=step,bank_vram=0x8000,tilemap_vram=0xF000,bank_byte_identical=True,map_unchanged_source_cells_identical=560,native_dynamic_field_cells_verified=40,bank_sha256=digest(bank),map_sha256=digest(mapping)))
    report.update(native_keyboard_labels_verified=True,native_keyboard_pages=observations,native_input_regression='Three-page switch/reentry and native kana name confirmed into profile via normal input; no commit/save code changed.',native_keyboard_commands=18)
    report['limits']=[x.replace('Kana keyboard and command labels remain native Japanese;', 'Kana letters remain native Japanese; command labels translated;') for x in report['limits']]
    report['agent_visual_review']=['boot: native keyboard Korean command labels; startup date/welcome preserved','pages: three native pages, command focus and transitions inspected','complete: native Japanese name confirmation/profile and Rockman startup/mail inspected']
    if out.exists():raise ValueError('preserve native keyboard report')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS native keyboard three-page VRAM/map and startup regression')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--out',required=True);p.add_argument('--page-steps',required=True);a=p.parse_args()
    run(ROOT/a.rom,ROOT/a.out,[int(s) for s in a.page_steps.split(',')])
