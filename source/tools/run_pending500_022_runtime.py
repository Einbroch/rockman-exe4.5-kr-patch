"""Same-ROM cold boot, ordinary hint fallback and quarantined hint display samples."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);a=p.parse_args()
    if not a.prefix.replace('-','').isalnum():raise ValueError('Simple runtime prefix')
    rom=ROOT/a.rom;h=sha(rom.read_bytes())
    subprocess.run([sys.executable,'-X','utf8','tools/run_first_mail_regression.py','--rom',a.rom,'--prefix',a.prefix,'--expanded-startup-captures'],check=True,cwd=ROOT)
    page=read('poc/runtime/native-keyboard-labels-v1-pagecycle/result.json')['actions']
    complete=read('poc/runtime/native-keyboard-labels-v1-complete/result.json')['actions']
    field=read('poc/runtime/pending500-022-weekday-field-v1/result.json')['actions']
    route=','.join(['a:2:180']*6+['l:2:180'])
    def run(suffix,actions,parent=None,tool='run_mesen_segment.py',extra=None):
        folder=ROOT/'poc/runtime'/f'{a.prefix}-{suffix}'
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rom),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(folder),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240']
        if parent:
            origin=ROOT/'poc/runtime'/f'{a.prefix}-{parent}';cmd+=['--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        if extra:cmd+=extra
        subprocess.run(cmd,check=True,cwd=ROOT)
        print('Verified 022 runtime segment:',suffix,flush=True)
    run('weekday-boot','none:1:900,start:2:90,a:2:180,a:2:120,a:2:120,up:2:120,up:2:120,a:2:120,a:2:120,a:2:120,a:2:120,a:2:180')
    run('weekday-pagecycle',page,'weekday-boot')
    run('weekday-complete',complete,'weekday-pagecycle')
    run('weekday-field',field,'weekday-complete')
    run('weekday-native-hint',route+',none:1:120,a:2:180,none:1:120,l:2:180,none:1:120,a:2:180','weekday-field',extra=['--capture-steps','7,9,11,13'])
    combined=complete+','+field+','+route
    at=len(combined.split(','))
    combined+=',none:1:120,a:2:180,none:1:120,l:2:180,none:1:120,a:2:180,none:1:120'
    for script in (11,15):
        run('hint-display-'+str(script),combined,'weekday-pagecycle','capture_hint_rom_display.py',['--hint-script',str(script),'--capture-steps',','.join(map(str,(at,at+2,at+4,at+6)))])
    for case in ('bass','carry'):
        actions='b:2:120,r:2:240,none:1:120,a:2:240,none:1:120'
        if case=='bass':actions+=',a:2:240,none:1:120'
        actions+=',a:2:240,none:1:120'
        run('raw-display-'+case,actions,'complete','capture_cumulative500_022_display.py',['--display-case',case])

if __name__=='__main__':main()
