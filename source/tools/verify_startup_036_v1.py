"""Own036 startup native bank/field residency and exact checkpoint lineage."""
import struct
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress

def main():
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();audit=read('analysis/pending500_036_v1/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=sha(rom):raise ValueError('036 audited artifact required')
    folders={k:ROOT/('poc/runtime/pending500-036-v1-'+k) for k in ('boot','pagecycle','complete')};refs={};previous=None
    for name,d in folders.items():
        r=read(d/'result.json')
        if not r['complete'] or r['rom_sha256']!=sha(rom) or r['return_code']!=0 or r['steps_captured']!=r['steps_expected']:raise ValueError('036 startup receipt')
        for p,h in r['artifacts'].items():require_hash(d/p,h)
        if previous:
            if r['state_origin']!=str((previous/'result.json').resolve()) or r['state_sha256']!=read(previous/'result.json')['artifacts']['checkpoint.mss']:raise ValueError('036 own-ROM lineage')
        elif r['state_origin'] is not None:raise ValueError('036 coldboot required')
        previous=d;refs[str((d/'result.json').relative_to(ROOT))]=sha((d/'result.json').read_bytes())
    observations=[]
    for page,step in zip(m['native_keyboard_labels']['pages'],(6,7,9)):
        v=(folders['pagecycle']/f'step_{step:03}_gbaVideoRam.bin').read_bytes();bank=rom[page['bank_offset']:page['bank_offset']+page['bank_bytes']];mapping=list(struct.unpack('<600H',rom[page['map_offset']:page['map_offset']+1200]))
        for y in (4,5):
            for x in range(3,13):mapping[y*30+x]=0xA1C0+2*(x-3)+y-4
            for x in range(17,27):mapping[y*30+x]=0xB180+2*(x-17)+y-4
        actual=b''.join(v[0xF000+y*64:0xF000+y*64+60] for y in range(20))
        if v[0x8000:0x8000+len(bank)]!=bank or actual!=struct.pack('<600H',*mapping):raise ValueError('036 native keyboard residency')
        observations.append(dict(page=page['page'],step=step,bank_and_native_field_map_verified=True))
    v=(folders['boot']/'step_003_gbaVideoRam.bin').read_bytes();f=m['startup_footer']
    if v[0x15200:0x15200+f['bytes']]!=rom[f['source_offset']:f['source_offset']+f['bytes']]:raise ValueError('036 footer upload')
    v=(folders['boot']/'step_009_gbaVideoRam.bin').read_bytes();ram=(folders['boot']/'step_009_gbaExtWorkRam.bin').read_bytes()
    for record,dest,offset in zip(m['startup_welcome']['records'],(v,ram),(0x8000,0x1C800)):
        payload,used=lz77_decompress(rom,record['offset'])
        if used!=record['stored_bytes'] or dest[offset:offset+len(payload)-4]!=payload[4:]:raise ValueError('036 welcome residency')
    items=[('boot',s) for s in (2,3,8,9)]+[('pagecycle',s) for s in (6,7,9)]+[('complete',s) for s in (14,15,16,17,18,19,20,21,22,23,24,34)]
    sheet=Image.new('RGB',(960,180*((len(items)+3)//4)),'#20232a');draw=ImageDraw.Draw(sheet)
    for i,(name,step) in enumerate(items):
        im=Image.open(folders[name]/f'step_{step:03}.png').convert('RGB')
        if im.size!=(240,160):raise ValueError('036 native screenshot size')
        x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+3,y+3),name+' '+str(step),fill='white')
    path=ROOT/'analysis/pending500_036_v1/startup_contact_v1.png'
    if path.exists():raise ValueError('preserve previous sheet')
    sheet.save(path)
    frozen_write(ROOT/'analysis/pending500_036_v1/startup_runtime_v1.json',dict(passed=True,rom_sha256=sha(rom),scope='Own036 coldboot, native kana bank switching, startup residency and initial settings/Navi controller route; NOT Hangul composition/save or036 native NPC selection',receipts=refs,native_keyboard_pages=observations,footer_and_welcome_residency_verified=True,contact_sheet=dict(path=str(path.relative_to(ROOT)),sha256=sha(path.read_bytes()),screens=len(items)),visual_review_pending=True,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_startup_036_v1.py','tools/run_startup_036_v1.py','analysis/pending500_036_v1/integration.json']}))
    print('PASS036 own startup lineage, kana banks/field maps, footer/welcome residency; visual review pending')

if __name__=='__main__':main()
