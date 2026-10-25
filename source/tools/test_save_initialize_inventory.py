"""Initialization writer and inherited authorities must not be double-counted."""
import copy,json,unittest
from build_visibility_poc import ROOT
from inventory_full_scope import inherited_guts_input

class InitializationInventoryTests(unittest.TestCase):
    def setUp(self):
        self.m=json.loads((ROOT/'poc/output/exe45_ko_development_save_initialize_v1.json').read_text(encoding='utf8'))
    def test_lineage(self):
        items=[a for a in self.m['translation_assets'] if a.get('scope') in ('authored initialization UI delta authority','read-only inherited55 preset units','read-only inherited38 preset units','read-only inherited17 preset units','read-only inherited16 preset units')]
        self.assertEqual(len(items),7)
        for item in items:self.assertTrue(inherited_guts_input(item,self.m))
    def test_wrong_population(self):
        item=copy.deepcopy(next(a for a in self.m['translation_assets'] if a.get('scope')=='read-only inherited55 preset units'));item['carry_units']=38
        with self.assertRaises(ValueError):inherited_guts_input(item,self.m)
    def test_unknown_authority(self):
        item=copy.deepcopy(next(a for a in self.m['translation_assets'] if a.get('scope')=='authored initialization UI delta authority'));item['path']='translations/input_heading_ko.json'
        with self.assertRaises(ValueError):inherited_guts_input(item,self.m)

if __name__=='__main__':unittest.main()
