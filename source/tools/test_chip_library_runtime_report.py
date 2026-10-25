"""Read-only positive and negative checks of the frozen pixel-evidence verifier."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_chip_library_runtime import ROOT, read, directory, visible_names
from fixedcell_font import bdf_cells


class RuntimeReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = read(ROOT / "project.json")
        cls.source = (ROOT / config["source_profile"]["filename"]).read_bytes()
        manifest = read(ROOT / "poc/output/exe45_ko_development_chip_library_v1.json")
        fixed = manifest["fixedcell_extension"]
        cls.cells = bdf_cells(ROOT / fixed["font"]["path"], set("캐논에어슛발칸"), fixed["raster"])
        cls.table = {}
        for line in (ROOT / "external/textpet-plugins/exe45-utf8.tbl").read_text(encoding="utf-8-sig").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                if len(value) == 1:
                    cls.table[value] = bytes.fromhex(key)

    def test_frozen_names_and_unknown_row_clear(self):
        evidence = visible_names(directory("tabs"), 7, {0: "캐논", 3: "에어슛", 4: "발칸1"}, self.cells, self.source, self.table)
        self.assertEqual(len(evidence), 8)
        self.assertEqual(visible_names(directory("scroll-reentry"), 18, {}, self.cells, self.source, self.table), [])

    def test_wrong_row_plan_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing parser-return row evidence"):
            visible_names(directory("tabs"), 7, {0: "에어슛", 3: "캐논", 4: "발칸1"}, self.cells, self.source, self.table)

    def test_wrong_font_supply_rejected(self):
        altered = dict(self.cells)
        altered["캐"] = bytes(64)
        with self.assertRaisesRegex(ValueError, "chip glyph supply mismatch"):
            visible_names(directory("tabs"), 7, {0: "캐논", 3: "에어슛", 4: "발칸1"}, altered, self.source, self.table)


if __name__ == "__main__":
    unittest.main()
