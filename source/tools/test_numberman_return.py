import copy,unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_literal_numerals,validate_numberman_return_decision

class ReturnTests(unittest.TestCase):
    def test_scope_source_controls_and_lineage(self):
        a=read(ROOT/'translations/numberman_return_ko.json');b=read(ROOT/'translations/numberman_intro_ko.json')
        self.assertEqual(a['units'][:7],b['units']);self.assertEqual(len(a['units']),12)
        s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6872B8'],a)
        t=(ROOT/'analysis/tpl_baseline/6872B8.tpl').read_text(encoding='utf8')
        lookup={x.key:x.text for x in literals(t)}
        self.assertTrue(all(u['source']==lookup[u['id']] for u in a['units']))
        self.assertEqual(skeleton(t),skeleton(translate_literal_scope(t,a['units'],s)))
        validate_literal_numerals(a['units'],s);validate_numberman_return_decision(a)
    def test_numeric_person_count_guard(self):
        a=read(ROOT/'translations/numberman_return_ko.json');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6872B8'],a)
        next(u for u in a['units'] if u['id']=='6872B8:2:3')['translation']='2명뿐이라 외로워서\n계속 수를\n세고 있었어요~'
        with self.assertRaisesRegex(ValueError,'numeral'):validate_literal_numerals(a['units'],s)
    def test_wordplay_approval_required(self):
        a=read(ROOT/'translations/numberman_return_ko.json');a['decisions'][0]['approved']=False
        with self.assertRaisesRegex(ValueError,'decision'):validate_numberman_return_decision(a)

if __name__=='__main__':unittest.main()
