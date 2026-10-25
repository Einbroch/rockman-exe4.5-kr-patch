"""Own pre-profile normal checkpoint; all remaining profile text renderer pages."""
import subprocess,sys,struct
from report_roll_pet import ROOT,read,verify_route
from run_gutsman_profile import STEM,PREFIX
from capture_gutsman_profile_diagnostic import SCRIPTS
ASSET='gutsman_profile_ko.json'
PAGE_COUNTS={}

def main():
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime';pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset']
    normal=rt/(PREFIX+'choices');verify_route(normal,m['output_sha256'],set());calls=read(normal/'step_015_roll_pet.json')['calls']
    if not calls or calls[-1]['root']!=pool or calls[-1]['script']!=29 or calls[-1]['lr']!=0x08037F27:raise ValueError('normal profile29 caller prerequisite')
    actions=read(normal/'result.json')['actions'].split(',');seed=rt/(PREFIX+'profile-seed');origin=rt/(PREFIX+'jackin')
    def run(tool,out,parent,recipe,extra=()):
        if out.exists():raise ValueError('preserve profile evidence '+str(out))
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),
            '--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--probe','snapshot','--actions',recipe,'--timeout','240','--state',str(parent/'checkpoint.mss'),
            '--state-origin',str(parent/'result.json'),*extra],check=True,cwd=ROOT)
    run('capture_gutsman_profile.py',seed,origin,','.join(actions[:12]))
    ram=(seed/'final_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]==pool or read(seed/'step_012_roll_pet.json')['calls']:raise ValueError('seed already crossed profile load')
    units=read(ROOT/'translations'/ASSET)['units']
    for script in SCRIPTS:
        count=PAGE_COUNTS.get(script,sum(int(u['id'].split(':')[1])==script for u in units))
        recipe=','.join([actions[12],'none:1:180']+['a:2:180']*(count-1))
        run('capture_gutsman_profile_diagnostic.py',rt/(PREFIX+f'diagnostic-{script}'),seed,recipe,('--profile-script',str(script)))
    run('capture_roll_plugout.py',rt/(PREFIX+'regression-choices'),origin,','.join(actions))

if __name__=='__main__':main()
