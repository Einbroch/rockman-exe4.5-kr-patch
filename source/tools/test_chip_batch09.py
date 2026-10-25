import unittest
from build_visibility_poc import ROOT
from report_chip_library_runtime import read
from tpl_literals import resolve_units,skeleton,replace_literals
from prepare_chip_descriptions_batch09 import prepare
from build_development_patch import selected_scope,validate_literal_numerals

class Batch09(unittest.TestCase):
    def test_source_bound_dark_descriptions_and_scope(self):
        a=read(ROOT/'translations/chip_descriptions_batch09_ko.json')
        self.assertEqual(a,prepare())
        u=resolve_units(a);self.assertEqual(len(u),251)
        self.assertEqual(u[:249],resolve_units(read(ROOT/'translations/chip_descriptions_batch08_ko.json')))
        self.assertEqual(a['wordings'],read(ROOT/'translations/chip_descriptions_batch08_ko.json')['wordings'])
        self.assertEqual([x['id'] for x in u[-2:]],['76937C:195:0','76937C:196:0'])
        self.assertTrue(all(x['state']=='needs_review' for x in u))
        r=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')
        scope=selected_scope(r['archives']['76937C'],a);validate_literal_numerals(u,scope)
        self.assertEqual(set(scope['literal_scripts']),set(range(1,197))|set(range(201,256)))
        original=(ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(skeleton(original),skeleton(replace_literals(original,u)))
