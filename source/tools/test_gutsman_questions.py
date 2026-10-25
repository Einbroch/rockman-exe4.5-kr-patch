"""Frozen source/parent fixtures and joined-page/nickname rejection contracts."""
import copy,unittest
from report_roll_pet import ROOT,read
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from tpl_literals import skeleton
from report_gutsman_questions import page_end

class QuestionCursorGuards(unittest.TestCase):
    def test_native_one_byte_end(self):
        self.assertEqual(page_end(bytes.fromhex('7ee600f1'),[0x08000000]),0x08000001)
    def test_extension_four_byte_end(self):
        self.assertEqual(page_end(bytes.fromhex('f9fca42be600f1'),[0x08000000]),0x08000004)
    def test_unfinished_page_rejected(self):
        with self.assertRaisesRegex(ValueError,'keyWait'):
            page_end(bytes.fromhex('f9fca42bf1e600'),[0x08000000])

class QuestionGuards(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/gutsman_profile_questions_ko.json');self.registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['667044'];self.source=(ROOT/'analysis/full_scope_v1/source_tpl/667044.tpl').read_text(encoding='utf-8-sig')
    def test_source_controls_font_and_parent_accepted(self):
        scope=selected_scope(self.registry,self.asset);target=translate_literal_scope(self.source,self.asset['units'],scope);self.assertEqual(skeleton(target),skeleton(self.source));validate_nickname_suffix(self.asset['units'],'667044',scope)
        validate_characters(target,ROOT/'poc/build/exe45_ko_development_gutsman_profile_v1/plugins/exe45-utf8.tbl',scope,{u['id'] for u in self.asset['units']})
    def test_retained_wording_change_rejected(self):
        bad=copy.deepcopy(self.asset);bad['units'][0]['translation']='다른 번역'
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_retained_identity_change_rejected(self):
        bad=copy.deepcopy(self.asset);bad['parent_asset']['carry_units']=39
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_joined_page_growth_and_lost_newline_rejected(self):
        for key in ['667044:11:3','667044:88:0']:
            for value in ['가\n나\n','가']:
                bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']==key)['translation']=value
                with self.assertRaisesRegex(ValueError,'joined nickname'):selected_scope(self.registry,bad)
    def test_joined_suffix_growth_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:88:1')['translation']='、\n가\n나'
        with self.assertRaisesRegex(ValueError,'joined nickname'):selected_scope(self.registry,bad)
    def test_new_nickname_suffix_growth_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:15:3')['translation']='야、\n장래의 꿈은\n뭐거스?'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad['units'],'667044',selected_scope(self.registry,bad))
    def test_new_source_mismatch_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:25:0')['source']='잘못된 원문'
        with self.assertRaises(ValueError):translate_literal_scope(self.source,bad['units'],selected_scope(self.registry,bad))

if __name__=='__main__':unittest.main()
