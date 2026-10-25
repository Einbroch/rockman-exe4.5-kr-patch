"""Family source/choice padding and exact inherited wording rejection."""
import copy,unittest
from report_roll_pet import ROOT,read
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from tpl_literals import skeleton

class FamilyGuards(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/gutsman_profile_family_checked_ko.json');self.registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['667044'];self.source=(ROOT/'analysis/full_scope_v1/source_tpl/667044.tpl').read_text(encoding='utf-8-sig')
    def test_source_controls_font_parent_and_choice_row_accepted(self):
        scope=selected_scope(self.registry,self.asset);target=translate_literal_scope(self.source,self.asset['units'],scope)
        self.assertEqual(skeleton(target),skeleton(self.source));validate_nickname_suffix(self.asset['units'],'667044',scope)
        measured=validate_characters(target,ROOT/'poc/build/exe45_ko_development_gutsman_questions_v1/plugins/exe45-utf8.tbl',scope,{u['id'] for u in self.asset['units']})
        self.assertTrue(all(r['choice_row_advance_pixels']<=132 for r in measured if 'choice_row_advance_pixels' in r))
    def test_parent_change_rejected(self):
        bad=copy.deepcopy(self.asset);bad['units'][0]['translation']='다른 번역'
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_choice_padding_loss_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:1:4')['translation']='있어'
        with self.assertRaisesRegex(ValueError,'padding'):translate_literal_scope(self.source,bad['units'],selected_scope(self.registry,bad))
    def test_nickname_particle_growth_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:3:2')['translation']='한테는\n남동생이 있거스?'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad['units'],'667044',selected_scope(self.registry,bad))
    def test_choice_overflow_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:1:4')['translation']='있어있어있어있어있어있어  '
        scope=selected_scope(self.registry,bad);target=translate_literal_scope(self.source,bad['units'],scope)
        with self.assertRaises(ValueError):validate_characters(target,ROOT/'poc/build/exe45_ko_development_gutsman_questions_v1/plugins/exe45-utf8.tbl',scope,{u['id'] for u in bad['units']})

if __name__=='__main__':unittest.main()
