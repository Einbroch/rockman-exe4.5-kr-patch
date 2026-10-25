import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_literal_numerals

class BubbleTests(unittest.TestCase):
    def test_retained_scope_and_small_geometry(self):
        a=read(ROOT/'translations/numberman_drill_bubbles_ko.json');old=read(ROOT/'translations/numberman_drill_intro_ko.json')
        self.assertEqual(a['units'][:20],old['units']);self.assertEqual(a['wordings'][:20],old['wordings'])
        self.assertFalse(a['review']['release_eligible']);u=resolve_units(a);self.assertEqual(len(u),32)
        s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064'],a)
        self.assertEqual(s['literal_profiles'][0]['max_line_advance'],60);self.assertEqual(s['literal_scripts'],[0,1,2,3,4,5,6,7,8,9,10,11,12,14])
        t=(ROOT/'analysis/tpl_baseline/715064.tpl').read_text(encoding='utf-8');v=translate_literal_scope(t,u,s)
        self.assertEqual(skeleton(t),skeleton(v));chosen={x['id'] for x in u}
        self.assertEqual({x.key:x.text for x in literals(t) if x.key not in chosen},{x.key:x.text for x in literals(v) if x.key not in chosen})
        validate_literal_numerals(u,s)
        for x in u:self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))
        self.assertEqual({x['id'] for x in u[20:]},{f'715064:{i}:0' for i in list(range(2,13))+[14]})

if __name__=='__main__':unittest.main()
