"""Render ten corresponding Rockman story-mail sender/title pairs in isolated sessions."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);a=p.parse_args()
    if not a.prefix.replace('-','').isalnum():raise ValueError('simple prefix')
    rom=ROOT/a.rom;origin=ROOT/f'poc/runtime/{a.prefix}-complete';h=sha(rom.read_bytes())
    result=json.loads((origin/'result.json').read_text(encoding='utf8'))
    if result.get('normal_play_checkpoint_eligible') is False or result['rom_sha256']!=h:raise ValueError('current normal route required')
    actions=['b:2:120']+['down:2:90']*4+['a:2:180','a:2:300','a:2:180','a:2:240']
    for script in [1,2,3,8,9,10,11,12,13,14]:
        folder=ROOT/f'poc/runtime/{a.prefix}-header-pair{script}'
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_official_mail.py'),'--mail-script',str(script),'--corresponding-header',
             '--header-only',
             '--rom',str(rom),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(folder),
             '--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),'--expect-rom-sha256',h,
             '--probe','snapshot','--actions',','.join(actions),'--timeout','120','--capture-steps','9']
        subprocess.run(cmd,check=True,cwd=ROOT);print('Header diagnostic complete',script,flush=True)

if __name__=='__main__':main()
