"""Own normal pre-load checkpoint, read-only lookup and quarantined renderer."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

STEM='exe45_ko_development_iceman_seasonal_v1'
PREFIX='iceman-seasonal-v1-'

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    rt=ROOT/'poc/runtime';parent=rt/(PREFIX+'normal-reload-select');lookup=rt/(PREFIX+'lookup');em=rt/'isolated-mesen-chip-matrix/Mesen.exe'
    actions='none:1:60,'+','.join(['a:2:300']*8)+',none:1:120'
    for tool,out,extra in [('capture_seasonal_lookup.py',lookup,[]),('capture_iceman_seasonal_diagnostic.py',rt/(PREFIX+'diagnostic-christmas-eve'),['--lookup-evidence',str(lookup),'--ice-script','8']),('capture_iceman_seasonal_diagnostic.py',rt/(PREFIX+'diagnostic-new-years-eve'),['--lookup-evidence',str(lookup),'--ice-script','10'])]:
        if out.exists():raise ValueError('preserve existing run')
        cmd=[sys.executable,'-X','utf8',str(ROOT/'tools'/tool),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(em),'--out',str(out),'--probe','snapshot','--actions',actions,'--timeout','240','--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),*extra]
        subprocess.run(cmd,check=True,cwd=ROOT)

if __name__=='__main__':main()
