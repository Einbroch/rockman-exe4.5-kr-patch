import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from build_visibility_poc import ROOT
from build_development_patch import selected_scope,validate_characters,validate_literal_numerals
from textpet_korean import prepare_plugins
from tpl_literals import replace_literals,resolve_units,skeleton


class DescriptionBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=TemporaryDirectory(prefix='exe45-desc-batch-unit-');cls.plugins=Path(cls.temp.name)/'plugins';prepare_plugins(cls.plugins)

    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def setUp(self):
        self.asset=json.loads((ROOT/'translations/chip_descriptions_batch01_ko.json').read_text(encoding='utf-8'))
        self.units=resolve_units(self.asset)
        self.tpl=(ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig')
        self.base=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text())['archives']['76937C']

    def test_complete_selected_source_and_controls(self):
        t=replace_literals(self.tpl,self.units);self.assertEqual(skeleton(t),skeleton(self.tpl))
        self.assertEqual({u['id'] for u in self.units},{f'76937C:{i}:0' for i in range(1,31)})
        for u in self.units:
            self.assertEqual(re.findall(r'\d+',u['source']),re.findall(r'\d+',u['translation']))
            self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
            self.assertEqual(u['state'],'needs_review')

    def test_source_specific_vulcan_counts(self):
        units={u['id']:u for u in self.units}
        self.assertEqual([re.findall(r'\d+',units[f'76937C:{i}:0']['translation']) for i in (15,16,17)], [['3','1'],['5','1'],['7','1']])

    def test_product_rejects_changed_numeral(self):
        scope=selected_scope(self.base,self.asset);validate_literal_numerals(self.units,scope)
        wrong=[dict(u,translation=u['translation'].replace('5연발','4연발')) for u in self.units]
        with self.assertRaises(ValueError): validate_literal_numerals(wrong,scope)

    def test_scope_variant_and_nine_visible_cells(self):
        scope=selected_scope(self.base,self.asset)
        self.assertEqual(scope['literal_scripts'],list(range(1,31)))
        layout=validate_characters(replace_literals(self.tpl,self.units),self.plugins/'exe45-utf8.tbl',scope,{u['id'] for u in self.units})
        self.assertEqual(len(layout),30)
        self.assertTrue(all(max(l['line_advance_pixels'])<=72 for l in layout))
        self.assertEqual(len(next(l for l in layout if l['id']=='76937C:29:0')['line_advance_pixels']),2)

    def test_old_three_script_scope_still_default(self):
        self.assertEqual(selected_scope(self.base,{})['literal_scripts'],[1,2,3])

    def test_unknown_or_structural_variant_rejected(self):
        with self.assertRaises(ValueError): selected_scope(self.base,{'scope_variant':'unknown'})
        with self.assertRaises(ValueError): selected_scope({'variants':{'bad':{'literal_scripts':[1],'pointers':[0]}}},{'scope_variant':'bad'})


if __name__=='__main__': unittest.main()
