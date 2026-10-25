"""Own coldboot of the keyboard stage 069 with run_normal_generic_v1 unchanged.

069 adds no text wrapper, so the newest wrapper sentinel is typed065's (still carried in the 069 metadata);
the graphic regions themselves are pinned by the ROM SHA (--expect-rom-sha256).
Usage: run_normal_graphics066_v1.py
"""
import sys
import run_normal_generic_v1 as R

_guards = R.guards
R.guards = lambda rom, m, key: _guards(rom, m, 'typed065' if key == 'typed069' else key)
sys.argv = [sys.argv[0], 'poc/output/pending500_069_v1.gba', '069']
R.main()
