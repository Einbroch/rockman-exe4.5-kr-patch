"""Catalog counts the selected writer once, not its immutable authorities."""
import copy,json,unittest
from build_visibility_poc import ROOT
from inventory_full_scope import inherited_guts_input

class CalendarInventoryLineageTests(unittest.TestCase):
    def setUp(self):
        self.m=json.loads((ROOT/'poc/output/exe45_ko_development_calendar_date_save_v1_r2.json').read_text(encoding='utf8'))
    def test_authorities_and_parents(self):
        matches=[a for a in self.m['translation_assets'] if a.get('scope') in ('authored UI delta authority','read-only inherited38 preset units','read-only inherited17 preset units','read-only inherited16 preset units')]
        self.assertEqual(len(matches),5)
        for item in matches:self.assertTrue(inherited_guts_input(item,self.m))
    def test_parent_count_rejected(self):
        item=copy.deepcopy(next(a for a in self.m['translation_assets'] if a.get('scope')=='read-only inherited38 preset units'));item['carry_units']=17
        with self.assertRaises(ValueError):inherited_guts_input(item,self.m)
    def test_unknown_authority_rejected(self):
        item=copy.deepcopy(next(a for a in self.m['translation_assets'] if a.get('scope')=='authored UI delta authority'));item['path']='translations/input_heading_ko.json'
        with self.assertRaises(ValueError):inherited_guts_input(item,self.m)

if __name__=='__main__':unittest.main()
