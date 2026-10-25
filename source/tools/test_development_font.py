import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_visibility_poc import ROOT, bdf_glyphs
from korean_codec import EXTRA_CHARACTER_METRICS


class PunctuationSupplyTests(unittest.TestCase):
    def test_comma_ink_and_shadow_not_clipped(self):
        glyph = bdf_glyphs(ROOT / "external/fonts/Galmuri11.bdf", {","},
                           {",": EXTRA_CHARACTER_METRICS[","]["vertical_shift"]})[","]
        self.assertEqual(len(glyph), 96)
        pixels = [n for b in glyph for n in (b & 15, b >> 4)]
        ink = {(i % 16, i // 16) for i, n in enumerate(pixels) if n == 3}
        shadow = {(i % 16, i // 16) for i, n in enumerate(pixels) if n == 2}
        self.assertEqual(ink, {(1, 9), (0, 10)})
        self.assertEqual(shadow, {(2, 10), (1, 11)})

    def test_default_hangul_packer_rejects_comma_descender(self):
        with self.assertRaises(ValueError):
            bdf_glyphs(ROOT / "external/fonts/Galmuri11.bdf", {","})


if __name__ == "__main__":
    unittest.main()
