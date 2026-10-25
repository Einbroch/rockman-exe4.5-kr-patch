"""Read-only5x2 mono TACTICS observation; no RAM injection."""
from pathlib import Path
import capture_chip_battle_names as previous


def main():
    code = Path(previous.__file__).read_text(encoding='utf-8')
    old = "s['cpu.r6']~=0x08612E38"
    if code.count(old) != 2:
        raise ValueError('prompt filter binding drift')
    code = code.replace(old, "(s['cpu.r6']~=0x08619EF8 or s['cpu.r4']~=5 or s['cpu.r5']~=2)")
    code = code.replace('battle_name', 'tactics_prompt').replace('battle-name', 'TACTICS prompt')
    ns = {'__name__':'tactics_prompt_observer_bound', '__file__':__file__}
    exec(compile(code, previous.__file__+' [5x2 mono binding]', 'exec'), ns)
    return ns['main']()


if __name__ == '__main__':
    raise SystemExit(main())
