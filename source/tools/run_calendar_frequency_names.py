"""Own cumulative ROM route and five normal committed frequency samples."""
import json,sys,subprocess
import run_gutsman_calendar_schedule_delete as base
from build_visibility_poc import ROOT,require_hash
STEM='exe45_ko_development_calendar_frequency_names_v1'
PREFIX='calendar-frequency-names-v1-'
OUTDIR='calendar_frequency_names_v1'
KINDS=['once','daily','weekly','monthly','yearly']
def trace(name,parent):
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rt=ROOT/'poc/runtime';out=rt/(PREFIX+name);p=rt/(PREFIX+parent)
    if out.exists():raise ValueError('preserve frequency trace evidence')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_calendar_frequency_copy.py'),'--rom',str(rp),'--expect-rom-sha256',m['output_sha256'],'--mesen',str(rt/'isolated-mesen-chip-matrix/Mesen.exe'),'--out',str(out),'--probe','snapshot','--actions','none:1:7,a:2:90','--timeout','240','--state',str(p/'checkpoint.mss'),'--state-origin',str(p/'result.json')],check=True,cwd=ROOT)
def main():
    base.STEM=STEM;base.PREFIX=PREFIX;base.OUTDIR=OUTDIR;base.main()
    capture=base.base.capture
    trace('frequency-once-first','schedule-delete-list')
    capture('frequency-selector','calendar','none:1:7,up:2:90,none:1:10,up:2:90,a:2:90')
    for i,kind in enumerate(KINDS[1:],1):
        select=','.join(['none:1:7,right:2:90']*i+['a:2:90'])
        capture('frequency-'+kind+'-type','frequency-selector',select)
        capture('frequency-'+kind+'-confirmation','frequency-'+kind+'-type','none:1:7,down:4:90,none:1:10,down:4:90,a:2:90')
        capture('frequency-'+kind+'-commit','frequency-'+kind+'-confirmation','none:1:7,a:2:90')
        capture('frequency-'+kind+'-delete-selector','frequency-'+kind+'-commit','none:1:7,down:2:90,none:1:7,down:2:90,a:2:90')
        capture('frequency-'+kind+'-list','frequency-'+kind+'-delete-selector','none:1:7,a:2:90')
        trace('frequency-'+kind+'-first','frequency-'+kind+'-list')
if __name__=='__main__':main()
