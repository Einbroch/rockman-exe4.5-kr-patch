"""Finite profile scope, source, nickname, controls and geometry rejection fixtures."""
import copy,unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters

class ProfileGuards(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/gutsman_profile_ko.json');self.registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['667044']
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/667044.tpl').read_text(encoding='utf-8-sig');self.scope=selected_scope(self.registry,self.asset)
    def test_complete_selected40_controls_and_font(self):
        units=self.asset['units'];self.assertEqual(len(units),40);validate_nickname_suffix(units,'667044',self.scope)
        translated=translate_literal_scope(self.source,units,self.scope);self.assertEqual(skeleton(self.source),skeleton(translated))
        validate_characters(translated,ROOT/'poc/build/exe45_ko_development_gutsman_profile_v1/plugins/exe45-utf8.tbl',self.scope,{u['id'] for u in units})
        self.assertEqual(static('exe45_ko_development_gutsman_profile_v1','667044')[4]['new_units'],40)
    def test_changed_source_reject(self):
        units=copy.deepcopy(self.asset['units']);units[0]['source']='잘못된 원문'
        with self.assertRaises(ValueError):translate_literal_scope(self.source,units,self.scope)
    def test_duplicate_selected_unit_reject(self):
        with self.assertRaises(ValueError):translate_literal_scope(self.source,self.asset['units']+[self.asset['units'][0]],self.scope)
    def test_unselected_script_reject(self):
        units=copy.deepcopy(self.asset['units']);x=next(x for x in literals(self.source) if int(x.key.split(':')[1])==88)
        units.append(dict(id=x.key,source=x.text,translation='잘못된 추가',state='needs_review'))
        with self.assertRaises(ValueError):translate_literal_scope(self.source,units,self.scope)
    def test_all_nickname_suffixes_reject_growth(self):
        for key in [f'667044:{s}:{i}' for s in (27,29) for i in (0,2)]+[f'667044:{s}:{i}' for s in (32,33,34) for i in (0,3)]:
            units=copy.deepcopy(self.asset['units']);unit=next(u for u in units if u['id']==key);unit['translation']='야'+unit['translation']
            with self.assertRaises(ValueError):validate_nickname_suffix(units,'667044',self.scope)

if __name__=='__main__':unittest.main()
