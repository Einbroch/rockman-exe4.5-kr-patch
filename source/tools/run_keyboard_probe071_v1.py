"""Type a Korean name on the 071 ROM's jamo page with normal pad input from its own segment-01 checkpoint.

Replays the first 11 actions of the 040 normal recipe segment 02 (reaches the name keyboard), moves to row 0
col 0, types 오여 using the formerly skipped cells ㅗ (row2 col8) and ㅕ (row2 col6), then confirms.
Captures after each jamo and after confirmation. No RAM/state injection; isolated Mesen test runner.
Usage: run_keyboard_probe071_v1.py OUT_FOLDER [PROBE WATCH_START WATCH_END]
"""
import json,subprocess,sys
from build_visibility_poc import ROOT
from cumulative_batch500 import read

ROM = 'poc/output/pending500_071_v1.gba'
SEG01 = 'poc/runtime/pending500-071-normal-v1-01'
SEG02 = 'poc/runtime/pending500-071-normal-v1-02'
MOVE = lambda key, n: [f'{key}:2:20'] * n
TYPE = 'a:2:60'


def main():
    out = sys.argv[1];m = read(ROM.replace('.gba', '.json'))
    lead = read(SEG02 + '/result.json')['actions'].split(',')[:11]
    acts = list(lead) + MOVE('left', 15)
    caps = []
    def add(seq, capture):
        acts.extend(seq)
        if capture:caps.append(len(acts))
    add([], True)                                                  # keyboard, cursor at row 0 col 0
    add(MOVE('right', 11) + [TYPE], True)                           # ㅇ (row0 col11)
    add(MOVE('down', 2) + MOVE('left', 3) + [TYPE], True)           # ㅗ (row2 col8) -> 오
    add(MOVE('up', 2) + MOVE('right', 3) + [TYPE], True)            # ㅇ
    add(MOVE('down', 2) + MOVE('left', 5) + [TYPE], True)           # ㅕ (row2 col6) -> 오여
    add(['start:2:60'], True)
    add(['start:2:120'], True)
    for _ in range(3):add(['a:2:180'], True)
    cmd = [sys.executable, '-X', 'utf8', 'tools/run_mesen_segment.py', '--rom', ROM, '--expect-rom-sha256', m['output_sha256'],
           '--mesen', 'poc/runtime/isolated-mesen-chip-matrix/Mesen.exe', '--out', out, '--probe', sys.argv[2] if len(sys.argv) > 2 else 'snapshot',
           '--actions', ','.join(acts), '--capture-steps', ','.join(map(str, caps)), '--timeout', '300',
           '--watch-start', sys.argv[3] if len(sys.argv) > 4 else '0', '--watch-end', sys.argv[4] if len(sys.argv) > 4 else '0',
           '--state', SEG01 + '/checkpoint.mss', '--state-origin', SEG01 + '/result.json']
    subprocess.run(cmd, cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    r = read(out + '/result.json');print('complete', r['complete'], 'captures', r['steps_captured'], caps)


if __name__ == '__main__':main()
