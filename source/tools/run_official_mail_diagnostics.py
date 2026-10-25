"""Sequential diagnostic bodies1..3, cold-route state bound to current ROM."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,sha

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--prefix',required=True);p.add_argument('--include-news',action='store_true');p.add_argument('--remaining-only',action='store_true');a=p.parse_args()
    if not a.prefix.replace('-','').isalnum():raise ValueError('simple prefix')
    rom=ROOT/a.rom;origin=ROOT/f'poc/runtime/{a.prefix}-complete'
    result=json.loads((origin/'result.json').read_text(encoding='utf8'))
    if result.get('normal_play_checkpoint_eligible') is False or result['rom_sha256']!=sha(rom.read_bytes()):raise ValueError('diagnostic origin is not current normal route')
    routing=['b:2:120']+['down:2:90']*4+['a:2:180','a:2:300','a:2:180','a:2:240']
    choices=[(11,13),(12,9),(13,8),(14,9)] if a.remaining_only else [(1,7),(2,13),(3,12)]+([(8,7),(9,8),(10,7)] if a.include_news else [])
    for script,pages in choices:
        # Capture native list->load entry, every page, and return to list.
        actions=routing+['a:2:180']*(pages+1)
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/capture_official_mail.py'),'--mail-script',str(script),'--rom',str(rom),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(ROOT/f'poc/runtime/{a.prefix}-official{script}'),'--state',str(origin/'checkpoint.mss'),'--state-origin',str(origin/'result.json'),'--expect-rom-sha256',sha(rom.read_bytes()),'--probe','snapshot','--actions',','.join(actions),'--timeout','240','--capture-steps',','.join(str(n) for n in range(9,len(actions)+1))]
        subprocess.run(cmd,check=True,cwd=ROOT)
        print('Official native-renderer diagnostic complete',script,flush=True)

if __name__=='__main__':main()
