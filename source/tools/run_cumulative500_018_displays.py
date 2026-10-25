"""Own018 normal state; hold each final keyWait before end/event commands."""
import json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from verify_cumulative500_018_displays import verify
def main():
    rom=ROOT/'poc/output/exe45_ko_development_pending500_018_v1.gba';meta=json.loads(rom.with_suffix('.json').read_text(encoding='utf8'));require_hash(rom,meta['output_sha256']);parent=ROOT/'poc/runtime/pending500-018-v1-complete'
    for case,archive,script,count,steps,origin in verify.CASES:
        actions='b:2:120,r:2:240,none:1:120'+',a:2:240,none:1:60'*(len(steps)-1)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_cumulative500_018_display.py'),'--rom',str(rom),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--expect-rom-sha256',meta['output_sha256'],'--probe','snapshot','--timeout','240','--display-case',case,'--out',str(ROOT/f'poc/runtime/pending500-018-v1-display-{case}'),'--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),'--actions',actions,'--capture-steps',','.join(map(str,steps))],check=True,cwd=ROOT)
    verify.main()
if __name__=='__main__':main()
