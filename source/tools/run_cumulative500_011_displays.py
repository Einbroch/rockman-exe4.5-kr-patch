"""Own-ROM normal NumberMan setup, then quarantined native text diagnostics."""
import json,subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash

def main():
    rom=ROOT/'poc/output/exe45_ko_development_pending500_011_v1.gba'
    meta=json.loads(rom.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(rom,meta['output_sha256'])
    prefix='pending500-011-v1'
    parent=ROOT/f'poc/runtime/{prefix}-pagecycle'
    origin=json.loads((parent/'result.json').read_text(encoding='utf8'))
    if not origin['complete'] or origin['rom_sha256']!=sha(rom.read_bytes()):raise ValueError('Own normal pagecycle prerequisite')
    # Reuse verified buttons, not a foreign saved state or RAM/caller mutation.
    actions=json.loads((ROOT/'poc/runtime/pending500-010-v1-number-complete/result.json').read_text(encoding='utf8'))['actions']
    normal=ROOT/f'poc/runtime/{prefix}-number-complete'
    common=['--rom',str(rom),'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),'--expect-rom-sha256',meta['output_sha256'],'--probe','snapshot','--timeout','240']
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/run_mesen_segment.py'),*common,'--out',str(normal),'--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),'--actions',actions,'--capture-steps','49'],check=True,cwd=ROOT)
    for case,script in [('ice',1),('plant',3),('carry',22)]:
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/capture_cumulative500_011_display.py'),*common,'--display-kind',case,'--alert-script',str(script),'--out',str(ROOT/f'poc/runtime/{prefix}-display-{case}'),'--state',str(normal/'checkpoint.mss'),'--state-origin',str(normal/'result.json'),'--actions','none:1:7,r:2:180,none:1:180','--capture-steps','2'],check=True,cwd=ROOT)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'tools/verify_cumulative500_011_displays.py')],check=True,cwd=ROOT)
if __name__=='__main__':main()
