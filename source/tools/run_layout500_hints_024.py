"""Own-ROM cold boot, retained first mail and natural B0 default hint twice."""
import subprocess,sys
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read


def main():
    rom=ROOT/'poc/output/pending500_024_v1.gba';h=sha(rom.read_bytes());prefix='pending500-024-v1'
    def run(suffix,actions,parent=None,tool='run_mesen_segment.py',extra=()):
        out=ROOT/'poc/runtime'/(prefix+'-'+suffix)
        cmd=[sys.executable,'-X','utf8','tools/'+tool,'--rom',str(rom),'--expect-rom-sha256',h,'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240']
        if parent:
            previous=ROOT/'poc/runtime'/(prefix+'-'+parent);cmd+=['--state',str(previous/'checkpoint.mss'),'--state-origin',str(previous/'result.json')]
        subprocess.run(cmd+list(extra),cwd=ROOT,check=True)
    run('weekday-boot','none:1:900,start:2:90,a:2:180,a:2:120,a:2:120,up:2:120,up:2:120,a:2:120,a:2:120,a:2:120,a:2:120,a:2:180')
    run('weekday-pagecycle',read('poc/runtime/native-keyboard-labels-v1-pagecycle/result.json')['actions'],'weekday-boot')
    run('weekday-complete',read('poc/runtime/native-keyboard-labels-v1-complete/result.json')['actions'],'weekday-pagecycle')
    run('weekday-field',read('poc/runtime/pending500-022-weekday-field-v1/result.json')['actions'],'weekday-complete')
    route=','.join(['a:2:180']*6+['l:2:180','none:1:120','a:2:180','none:1:120','l:2:180','none:1:120','a:2:180'])
    run('natural-b0-hint',route,'weekday-field','capture_field_b0_display_023.py',('--capture-steps','7,9,11,13'))
    complete=read('poc/runtime/native-keyboard-labels-v1-complete/result.json')['actions']
    field=read('poc/runtime/pending500-022-weekday-field-v1/result.json')['actions']
    first_route=','.join(['a:2:180']*6+['l:2:180'])
    combined=complete+','+field+','+first_route
    at=len(combined.split(','))
    combined+=',none:1:120,a:2:180,none:1:120,l:2:180,none:1:120,a:2:180,none:1:120'
    for script in (10,26):
        run('hint-display-'+str(script),combined,'weekday-pagecycle','capture_hint_rom_display_024.py',('--hint-script',str(script),'--capture-steps',','.join(map(str,(at,at+2,at+4,at+6)))))


if __name__=='__main__':main()
