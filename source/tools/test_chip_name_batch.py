"""Protected batch source/grammar checks independent of runtime drafting."""
import copy
import json
import unittest
from pathlib import Path
from chip_library_extension import compile_clone, encode_name
from build_visibility_poc import ROOT


class ChipNameBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
        cls.spec = json.loads((ROOT / 'tools/specs/exe45_chip_library_v1.json').read_text())
        cls.asset = json.loads((ROOT / 'translations/library_chip_names_batch01_ko.json').read_text())
        cls.table = {int(k,16):v for line in (ROOT / 'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines()
                     if '=' in line for k,v in [line.split('=',1)] if len(k)==2}

    def test_roundtrip_and_unselected_population(self):
        _, r = compile_clone(self.source,self.spec,self.asset,self.table)
        self.assertEqual({u['script'] for u in r['units']},set(range(1,31)))
        self.assertEqual(len(r['unselected_scripts']),226)
        self.assertTrue(all(u['cells']<=8 for u in r['units']))

    def test_source_text_mismatch_rejected(self):
        a = copy.deepcopy(self.asset)
        a['units'][3]['source'] += '1'
        with self.assertRaises(ValueError):
            compile_clone(self.source,self.spec,a,self.table)

    def test_numeric_suffix_change_rejected(self):
        a = copy.deepcopy(self.asset)
        a['wordings'][8]['translation'] = '와이드샷2'
        with self.assertRaises(ValueError):
            compile_clone(self.source,self.spec,a,self.table)

    def test_raw_source_mismatch_rejected(self):
        a = copy.deepcopy(self.asset)
        a['source_script_hex']['30'] = 'e5'
        with self.assertRaises(ValueError):
            compile_clone(self.source,self.spec,a,self.table)

    def test_nine_cells_rejected_not_shortened(self):
        with self.assertRaises(ValueError):
            encode_name('가'*9,self.table)


if __name__ == '__main__':
    unittest.main()
