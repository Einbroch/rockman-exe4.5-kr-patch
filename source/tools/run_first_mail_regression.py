"""Cold-boot cumulative first-mail regression, normal buttons and own states."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--expanded-startup-captures',action='store_true');a=p.parse_args()
    if not a.prefix.replace('-','').isalnum():raise ValueError('simple runtime prefix')
    rom=ROOT/a.rom;h=sha(rom.read_bytes())
    old=ROOT/'poc/runtime/native-keyboard-labels-v1-complete/result.json'
    complete=json.loads(old.read_text(encoding='utf8'))['actions']
    page=json.loads((ROOT/'poc/runtime/native-keyboard-labels-v1-pagecycle/result.json').read_text(encoding='utf8'))['actions']
    boot='none:1:900,start:2:90,'+','.join(['a:2:180']*8)
    cards=','.join(complete.split(',')[:23])+',a:2:120,b:2:120,right:2:120,a:2:120,b:2:120,right:2:120,a:2:120,b:2:120,right:2:120,a:2:120,b:2:120,left:2:120,left:2:120,left:2:120'
    read=json.loads((ROOT/'poc/runtime/first-mail-v1-read/result.json').read_text(encoding='utf8'))['actions']
    def run(suffix,actions,parent=None,captures=None):
        folder=ROOT/'poc/runtime'/f'{a.prefix}-{suffix}'
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/run_mesen_segment.py'),'--rom',str(rom),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(folder),'--expect-rom-sha256',h,'--probe','snapshot','--actions',actions,'--timeout','240']
        if parent:
            origin=ROOT/'poc/runtime'/f'{a.prefix}-{parent}'
            cmd+=['--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json')]
        if captures:cmd+=['--capture-steps',captures]
        subprocess.run(cmd,check=True,cwd=ROOT)
        print('Verified segment receipt:',suffix,flush=True)
    run('boot',boot)
    run('pagecycle',page,'boot')
    run('complete',complete,'pagecycle','14,15,16,17,18,19,20,21,22,23,24,34' if a.expanded_startup_captures else '19,20,21,22,23,24,34')
    run('read',read,'complete')
    run('selection',cards,'pagecycle',','.join(str(i) for i in range(23,38)))
if __name__=='__main__':main()
