"""Own normal pre-load state, native lookup observation and quarantined pages."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

STEM='exe45_ko_development_searchman_seasonal_v1'
PREFIX='searchman-seasonal-v1-'

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'normal-reload-select');lookup=rt/(PREFIX+'lookup');em=rt/'isolated-mesen-chip-matrix/Mesen.exe'
    actions='none:1:60,'+','.join(['a:2:180']*8)+',none:1:120'
    jobs=[('capture_seasonal_lookup.py',lookup,[])]+[('capture_searchman_seasonal_diagnostic.py',rt/(PREFIX+name),['--lookup-evidence',str(lookup),'--search-script',str(s)]) for s,name in [(1,'diagnostic-new-year'),(7,'diagnostic-weather'),(8,'diagnostic-christmas-eve')]]
    for tool,out,extra in jobs:
        if out.exists():raise ValueError('preserve existing run')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(em),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),*extra]
        subprocess.run(cmd,check=True,cwd=ROOT)

if __name__=='__main__':main()
