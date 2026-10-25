"""Positive/negative evidence checks; uses retained local diagnostic captures."""
import sys
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_chip_library_stress import ROOT, read, stats, pixel_masks
from build_visibility_poc import require_hash


class StressReportTests(unittest.TestCase):
    def test_timing_values_fail_closed(self):
        self.assertEqual(stats([{"cycles": 2}, {"cycles": 6}]), {"count": 2, "min": 2, "median": 4.0, "max": 6})
        for rows in ([], [{"cycles": 0}], [{"cycles": -1}]):
            with self.assertRaises(ValueError):
                stats(rows)

    def test_visible_pixels_and_wrong_glyph(self):
        path = ROOT / "poc/output/exe45_ko_development_chip_library_v1.gba"
        font = read(path.with_suffix(".json"))["chip_library_extension"]["font_offset"]
        rom = path.read_bytes()
        shot = Image.open(ROOT / "poc/runtime/chip-ko-v1-stress56-icons-v2/step_004.png").convert("RGB")
        pixel_masks(shot, rom[font:font + 64], 136, 32)
        with self.assertRaises(ValueError):
            pixel_masks(shot, bytes(64), 136, 32)

    def test_isolated_save_restoration(self):
        receipt = read(ROOT / "analysis/chip_timing_save_restoration_v1.json")
        for key, digest in (("target", "after_sha256"), ("recovery_source", "after_sha256"), ("before_preserved_as", "before_sha256")):
            require_hash(ROOT / receipt[key], receipt[digest])


if __name__ == "__main__":
    unittest.main()
