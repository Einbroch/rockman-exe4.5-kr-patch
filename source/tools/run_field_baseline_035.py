"""Own034 weekday startup, old actions only; no old saved state reuse."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from inspect_remaining_035 import BASE,BASE_SHA

def main():
    require_hash(ROOT/BASE,BASE_SHA)
    for suffix,parent in [('boot',None),('pagecycle','boot'),('complete','pagecycle')]:
        old='poc/runtime/pending500-022-weekday-'+('complete-trace' if suffix=='complete' else suffix)+'/result.json'
        actions=read(old)['actions'];folder='poc/runtime/pending500-035-baseline034-weekday-'+suffix
        tool='capture_field_loader_035.py' if suffix=='complete' else 'run_mesen_segment.py'
        cmd=[sys.executable,'-X','utf8','tools/'+tool,'--rom',BASE,'--expect-rom-sha256',BASE_SHA,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--actions',actions,'--probe','snapshot','--timeout','240','--capture-steps','10,12' if suffix=='boot' else '11' if suffix=='pagecycle' else '24,34']
        if parent:
            pf='poc/runtime/pending500-035-baseline034-weekday-'+parent
            cmd+=['--state',pf+'/checkpoint.mss','--state-origin',pf+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True)
        print('035 own034 weekday '+suffix+' receipt complete',flush=True)

if __name__=='__main__':main()
