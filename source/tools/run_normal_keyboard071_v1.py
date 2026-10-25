"""Own coldboot of stage 071 with run_normal_generic_v1, recipe segment 02 adapted to the confirm guard.

The 040 recipe types one cell (formerly あ, now the lone jamo ㄱ) and confirms; 071 refuses that (user decision),
so after recipe action 27 (the A that types ㄱ, cursor still on row 0 col 0) the cursor goes down two rows to ㅏ
and A types it (가). Captures after action 27 shift by 3. Everything else is the unchanged recipe; the newest
wrapper sentinel is typed065's (071 adds no text wrapper).
"""
import sys
import run_normal_generic_v1 as R

INSERT_AFTER, EXTRA = 27, ['down:2:20', 'down:2:20', 'a:2:60']
_guards, _read = R.guards, R.read
history = _read('analysis/pending500_040_v2/normal_recipe_receipts_v1.json')
SEG02 = history['segments'][1]['path']


def read(path):
    data = _read(path)
    if path == SEG02:
        acts = data['actions'].split(',')
        if acts[INSERT_AFTER - 1] != 'a:2:120':raise SystemExit('segment 02 recipe drift')
        data = dict(data, actions=','.join(acts[:INSERT_AFTER] + EXTRA + acts[INSERT_AFTER:]),
                    capture_steps=[s + len(EXTRA) if s > INSERT_AFTER else s for s in data['capture_steps']])
    return data


R.read = read
R.guards = lambda rom, m, key: _guards(rom, m, 'typed065' if key == 'typed071' else key)
sys.argv = [sys.argv[0], 'poc/output/pending500_071_v1.gba', '071']
R.main()
