"""Pinned fixed40 redisplay prose; retain buffers and inherited110 exactly."""
import copy,unittest
from report_roll_pet import ROOT,read
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from tpl_literals import skeleton

class AnswerGuards(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/gutsman_profile_answers_ko.json');self.registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['667044'];self.source=(ROOT/'analysis/full_scope_v1/source_tpl/667044.tpl').read_text(encoding='utf-8-sig')
    def test_fixed40_source_controls_buffers_and_font_geometry(self):
        scope=selected_scope(self.registry,self.asset);target=translate_literal_scope(self.source,self.asset['units'],scope)
        self.assertEqual(len(self.asset['units']),150);self.assertEqual(skeleton(target),skeleton(self.source));self.assertEqual(len(scope['literal_scripts']),62)
        for token in ['printStringBuffer1','printStringBuffer2','printStringBuffer3']:
            self.assertEqual(target.count(token),self.source.count(token))
        validate_nickname_suffix(self.asset['units'],'667044',scope)
        measured=validate_characters(target,ROOT/'poc/build/exe45_ko_development_gutsman_answers_v1/plugins/exe45-utf8.tbl',scope,{u['id'] for u in self.asset['units']})
        self.assertTrue(all(r['choice_row_advance_pixels']<=132 for r in measured if 'choice_row_advance_pixels' in r))
    def test_inherited_family_wording_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:1:0')['translation']='다른 문구'
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_parent_denominator_rejected(self):
        bad=copy.deepcopy(self.asset);bad['parent_asset']['carry_units']=109
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_new_source_mismatch_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:40:0')['source']='잘못된 원문'
        with self.assertRaises(ValueError):translate_literal_scope(self.source,bad['units'],selected_scope(self.registry,bad))
    def test_choice_padding_loss_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:41:1')['translation']='있어'
        with self.assertRaisesRegex(ValueError,'padding'):translate_literal_scope(self.source,bad['units'],selected_scope(self.registry,bad))
    def test_suffix_growth_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:40:0')['translation']='한테는\n형이나 오빠는・・・'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad['units'],'667044',selected_scope(self.registry,bad))
    def test_choice_overflow_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:41:1')['translation']='있어있어있어있어있어있어  '
        scope=selected_scope(self.registry,bad);target=translate_literal_scope(self.source,bad['units'],scope)
        with self.assertRaises(ValueError):validate_characters(target,ROOT/'poc/build/exe45_ko_development_gutsman_answers_v1/plugins/exe45-utf8.tbl',scope,{u['id'] for u in bad['units']})

if __name__=='__main__':unittest.main()
