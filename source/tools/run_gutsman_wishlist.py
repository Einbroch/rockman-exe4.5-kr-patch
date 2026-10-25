"""Fresh own-ROM normal route and quarantined wishlist31 renderer pages."""
import subprocess,sys,struct
import run_gutsman_profile as normal
from report_roll_pet import ROOT,read,verify_route

STEM='exe45_ko_development_gutsman_wishlist_v1'
PREFIX='gutsman-wishlist-v1-'

def main():
    normal.STEM=STEM;normal.PREFIX=PREFIX;normal.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime'
    choices=rt/(PREFIX+'choices');verify_route(choices,m['output_sha256'],set())
    actions=read(choices/'result.json')['actions'].split(',');origin=rt/(PREFIX+'jackin');seed=rt/(PREFIX+'profile-seed')
    def run(tool,out,parent,recipe,extra=()):
        if out.exists():raise ValueError('preserve wishlist evidence '+str(out))
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),
            '--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--probe','snapshot','--actions',','.join(recipe),'--timeout','240',
            '--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),*extra],check=True,cwd=ROOT)
    run('capture_gutsman_profile.py',seed,origin,actions[:12])
    pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset']
    if struct.unpack_from('<I',(seed/'final_gbaExtWorkRam.bin').read_bytes(),0xFA50)[0]==pool or read(seed/'step_012_roll_pet.json')['calls']:raise ValueError('seed crossed profile load')
    run('capture_gutsman_profile_diagnostic.py',rt/(PREFIX+'diagnostic-31'),seed,[actions[12],'none:1:180','a:2:180','a:2:180'],('--profile-script','31'))
    run('capture_roll_plugout.py',rt/(PREFIX+'regression-choices'),origin,actions)

if __name__=='__main__':main()
