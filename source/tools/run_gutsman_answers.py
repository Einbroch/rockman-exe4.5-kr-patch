"""Fresh own ROM; fixed redisplay prose diagnostics, no injected answer buffers."""
import subprocess,sys,struct
import run_gutsman_profile as normal
from report_roll_pet import ROOT,read,verify_route

STEM='exe45_ko_development_gutsman_answers_v1'
PREFIX='gutsman-answers-v1-'

def main():
    normal.STEM=STEM;normal.PREFIX=PREFIX;normal.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime'
    choices=rt/(PREFIX+'choices');verify_route(choices,m['output_sha256'],set())
    actions=read(choices/'result.json')['actions'].split(',');origin=rt/(PREFIX+'jackin');seed=rt/(PREFIX+'profile-seed')
    def run(tool,out,parent,recipe,extra=()):
        if out.exists():raise ValueError('preserve answers evidence '+str(out))
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(ROOT/f'poc/output/{STEM}.gba'),
            '--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--probe','snapshot','--actions',','.join(recipe),'--timeout','240',
            '--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),*extra],check=True,cwd=ROOT)
    run('capture_gutsman_profile.py',seed,origin,actions[:12])
    pool=0x08000000+next(a for a in m['archives'] if a['archive']=='667044')['rom_offset']
    if struct.unpack_from('<I',(seed/'final_gbaExtWorkRam.bin').read_bytes(),0xFA50)[0]==pool or read(seed/'step_012_roll_pet.json')['calls']:raise ValueError('seed crossed profile load')
    for script in (40,43,46,49,52,55,58,61):
        entry=[actions[12],'none:1:180']
        # Stop before printStringBuffer: no fabricated stored answer fixture.
        run('capture_gutsman_profile_diagnostic.py',rt/(PREFIX+f'diagnostic-{script}-prefix'),seed,entry,('--profile-script',str(script)))
        choice=script+1
        for branch in ('no','b') if choice==41 else ('no',):
            tail=['right:2:30','left:2:30','right:2:30','a:2:180','none:1:180'] if branch=='no' else ['b:2:180','none:1:180']
            run('capture_gutsman_profile_diagnostic.py',rt/(PREFIX+f'diagnostic-{choice}-{branch}'),seed,entry+tail,('--profile-script',str(choice)))
    run('capture_roll_plugout.py',rt/(PREFIX+'regression-choices'),origin,actions)

if __name__=='__main__':main()
