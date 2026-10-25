"""Fresh exact-ROM native save/continue seasonal path; no imported save/state."""
import argparse,json,subprocess,sys
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha

STEM='exe45_ko_development_numberman_seasonal_v1'
PREFIX='numberman-seasonal-v1-'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stem',default=STEM);ap.add_argument('--prefix',default=PREFIX);a=ap.parse_args()
    rp=ROOT/f'poc/output/{a.stem}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    rt=ROOT/'poc/runtime';em=rt/'isolated-mesen-chip-matrix/Mesen.exe';config=json.loads((em.parent/'settings.json').read_text(encoding='utf-8-sig'))
    save=Path(config['Preferences']['SaveDataFolder']).resolve()
    if not config['Preferences']['OverrideSaveDataFolder'] or not save.is_relative_to(rt.resolve()):raise ValueError('isolated saves required')
    if any((save/(a.stem+e)).exists() for e in ['.sav','.rtc']):raise ValueError('fresh own candidate save required')
    chain=['cold-part1','date','profile','navi-menu','select-numberman','intro','save-enter','save-commit','normal-reload-menu','normal-reload-navi','normal-reload-select','normal-return']
    parent=None
    for name in chain:
        old=json.loads((rt/('numberman-return-v1-'+name)/'result.json').read_text())
        out=rt/(a.prefix+name)
        if out.exists():raise ValueError('preserve existing run '+str(out))
        tool='capture_roll_save.py' if name.startswith('save-') else 'capture_numberman_seasonal.py'
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(em),'--out',str(out),'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,range(1,len(old['actions'].split(','))+1))),'--timeout','240']
        # Cold native continue intentionally has no loaded savestate.
        if name=='normal-reload-menu':parent=None
        if parent is not None:cmd+=['--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json')]
        print('normal seasonal path',name,flush=True);subprocess.run(cmd,check=True,cwd=ROOT);parent=out
    return 0

if __name__=='__main__':raise SystemExit(main())
