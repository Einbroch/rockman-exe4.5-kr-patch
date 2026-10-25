"""Resume only A3 samples from own024 pre-field checkpoint; no flag edits."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read


def main():
    rom=ROOT/'poc/output/pending500_024_v1.gba';m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256']);h=sha(rom.read_bytes())
    complete=read('poc/runtime/native-keyboard-labels-v1-complete/result.json')['actions']
    field=read('poc/runtime/pending500-022-weekday-field-v1/result.json')['actions']
    combined=complete+','+field+','+','.join(['a:2:180']*6+['l:2:180']);at=len(combined.split(','))
    combined+=',none:1:120,a:2:180,none:1:120,l:2:180,none:1:120,a:2:180,none:1:120'
    parent=ROOT/'poc/runtime/pending500-024-v1-weekday-pagecycle'
    for script in (10,26):
        out=ROOT/f'poc/runtime/pending500-024-v1-hint-display-{script}'
        subprocess.run([sys.executable,'-X','utf8','tools/capture_hint_rom_display_024_v2.py',
            '--rom',str(rom),'--expect-rom-sha256',h,'--mesen',str(ROOT/'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'),
            '--out',str(out),'--probe','snapshot','--actions',combined,'--timeout','240',
            '--state',str(parent/'checkpoint.mss'),'--state-origin',str(parent/'result.json'),
            '--hint-script',str(script),'--capture-steps',','.join(map(str,(at,at+2,at+4,at+6)))],cwd=ROOT,check=True)


if __name__=='__main__':main()
