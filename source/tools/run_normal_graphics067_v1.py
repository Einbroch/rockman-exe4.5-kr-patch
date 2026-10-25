"""Own coldboot of the graphics-only stage 067 with run_normal_generic_v1 unchanged.

067 adds no text wrapper, so the newest wrapper sentinel is typed065's (still carried in the 067 metadata);
the graphic regions themselves are pinned by the ROM SHA (--expect-rom-sha256).
Usage: run_normal_graphics066_v1.py
"""
import sys
import run_normal_generic_v1 as R

_guards = R.guards
R.guards = lambda rom, m, key: _guards(rom, m, 'typed065' if key == 'typed067' else key)
sys.argv = [sys.argv[0], 'poc/output/pending500_067_v1.gba', '067']
R.main()
