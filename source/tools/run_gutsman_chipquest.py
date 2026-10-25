"""Fresh exact-ROM Guts/NumberMan regressions and both guarded chip-name callers."""
import subprocess,sys,struct
from report_roll_pet import ROOT,read,verify_route
import run_gutsman_pet
STEM='exe45_ko_development_gutsman_chipquest_v1'
PREFIX='gutsman-chipquest-v1-'
OUTDIR='gutsman_chipquest_v1'

def main():
    resume='--resume-roll-selection' in sys.argv
    if len(sys.argv)>1 and sys.argv[1:]!=['--resume-roll-selection']:raise ValueError('unknown runtime resume argument')
    if not resume:
        run_gutsman_pet.STEM=STEM;run_gutsman_pet.PREFIX=PREFIX;run_gutsman_pet.main()
    m=read(ROOT/f'poc/output/{STEM}.json');rt=ROOT/'poc/runtime';rom=ROOT/f'poc/output/{STEM}.gba'
    def capture(name,tool,parent,actions,extra=()):
        out=rt/(PREFIX+name);p=rt/(PREFIX+parent)
        if out.exists():raise ValueError('preserve runtime evidence')
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools'/tool),*extra,'--rom',str(rom),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(p/'checkpoint.mss'),'--state-origin',str(p/'result.json')],check=True,cwd=ROOT)
        return out
    if not resume:
        capture('normal-talk','capture_gutsman_pet_talk.py','select-gutsman','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180')
        capture('chip13','capture_gutsman_chipquest.py','select-gutsman','none:1:7,r:2:180,none:1:180,a:2:180,none:1:180,r:2:180,none:1:180',['--talk-script','13'])
        p=capture('roll-select','capture_roll_pet.py','normal-reload-select','none:1:60,left:2:60,left:2:60,a:2:300');parent='roll-select';chain=[parent];start=0
    else:
        chain=['roll-select']+[f'roll-advance{i}' for i in range(1,14)];parent='normal-reload-select'
        for route in chain:
            q=rt/(PREFIX+route);receipt=verify_route(q,m['output_sha256'],set())
            if receipt['state_origin']!=str(rt/(PREFIX+parent)/'result.json') or receipt.get('normal_play_checkpoint_eligible') is False:raise ValueError('resume only own normal exact-ROM chain')
            parent=route
        p=rt/(PREFIX+parent);start=13
    petpool=0x08000000+next(a for a in m['archives'] if a['archive']=='65FA58')['rom_offset']
    for i in range(start,25):
        ram=(p/'final_gbaExtWorkRam.bin').read_bytes()
        if struct.unpack_from('<I',ram,0xFA50)[0]==petpool and ram[0xFA21]==1:break
        name=f'roll-advance{i+1}';p=capture(name,'capture_roll_pet.py',parent,'a:2:300,none:1:60');parent=name;chain.append(parent)
    else:raise ValueError('Roll native idle not reached; preserve captures')
    (rt/(PREFIX+'roll-select')/'roll_selection_chain.json').write_text(__import__('json').dumps(dict(rom_sha256=m['output_sha256'],routes=chain,final_parent=parent),indent=2),encoding='utf8')
    capture('roll-chip13','capture_dialogue_chip_name.py',parent,'none:1:7,r:2:180,none:1:180,a:2:180,none:1:180',['--talk-script','13'])

if __name__=='__main__':main()
