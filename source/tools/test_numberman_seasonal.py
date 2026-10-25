import unittest,re
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_numberman_seasonal import DRAFT

class Seasonal(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/numberman_seasonal_ko.json')
        self.tpl=(ROOT/'analysis/full_scope_v1/source_tpl/68BBB4.tpl').read_text(encoding='utf-8-sig')
        self.scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['68BBB4']
    def test_complete_source_and_manual_draft(self):
        source={x.key:x.text for x in literals(self.tpl)}
        self.assertEqual(60,len(source));self.assertEqual(source,{x['id']:x['source'] for x in self.asset['units']})
        for u in self.asset['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation']);self.assertEqual('needs_review',u['state'])
    def test_controls_geometry_numerals(self):
        output=replace_literals(self.tpl,self.asset['units']);self.assertEqual(skeleton(output),skeleton(self.tpl))
        validate_literal_numerals(self.asset['units'],self.scope)
        for u in self.asset['units']:
            lines=u['translation'].split('\n');self.assertLessEqual(len(lines),3)
            for line in lines:self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
    def test_dynamic_quotes_not_rewritten(self):
        for u in self.asset['units']:
            if u['id'].startswith('68BBB4:18:'):self.assertEqual(u['source'],u['translation'])
        self.assertFalse(self.asset['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',self.asset['policy'])

if __name__=='__main__':unittest.main()
