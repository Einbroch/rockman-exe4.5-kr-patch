"""Last3 literals retain exact150 parent, nickname and input controls."""
import copy,unittest
from report_roll_pet import ROOT,read
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from tpl_literals import skeleton,literals

class WishlistGuards(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/gutsman_profile_wishlist_ko.json');self.registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['667044'];self.source=(ROOT/'analysis/full_scope_v1/source_tpl/667044.tpl').read_text(encoding='utf-8-sig')
    def test_complete_fixed_literal_population_and_controls(self):
        scope=selected_scope(self.registry,self.asset);target=translate_literal_scope(self.source,self.asset['units'],scope)
        self.assertEqual({u['id'] for u in self.asset['units']},{u.key for u in literals(self.source)});self.assertEqual(skeleton(target),skeleton(self.source));validate_nickname_suffix(self.asset['units'],'667044',scope)
        validate_characters(target,ROOT/'poc/build/exe45_ko_development_gutsman_wishlist_v1/plugins/exe45-utf8.tbl',scope,{u['id'] for u in self.asset['units']})
    def test_parent_wording_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:40:0')['translation']='다른 문구'
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_source_mismatch_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:31:0')['source']='잘못된 원문'
        with self.assertRaises(ValueError):translate_literal_scope(self.source,bad['units'],selected_scope(self.registry,bad))
    def test_suffix_growth_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:31:2')['translation']='너는\n지금 갖고 싶은 게\n있거스?'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad['units'],'667044',selected_scope(self.registry,bad))
    def test_extra_line_rejected(self):
        bad=copy.deepcopy(self.asset);next(u for u in bad['units'] if u['id']=='667044:31:0')['translation']+='\n가'
        with self.assertRaises(ValueError):translate_literal_scope(self.source,bad['units'],selected_scope(self.registry,bad))

if __name__=='__main__':unittest.main()
