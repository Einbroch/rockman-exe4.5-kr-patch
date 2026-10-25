import unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_seasonal_companions import DRAFTS

class Companions(unittest.TestCase):
    def test_complete_drafts_protected_source_and_controls(self):
        for name,ar,count in [('rockman','65E438',28),('roll','6648D0',41)]:
            a=read(ROOT/f'translations/{name}_seasonal_ko.json');tpl=(ROOT/f'analysis/full_scope_v1/source_tpl/{ar}.tpl').read_text(encoding='utf-8-sig')
            self.assertEqual(count,len(a['units']));self.assertEqual({x.key:x.text for x in literals(tpl)},{u['id']:u['source'] for u in a['units']})
            self.assertEqual(skeleton(tpl),skeleton(replace_literals(tpl,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
            for u in a['units']:
                _,s,i=u['id'].split(':');self.assertEqual(DRAFTS[ar][int(s)][int(i)],u['translation'])
    def test_layout_and_dynamic_delimiters(self):
        for name in ['rockman','roll']:
            a=read(ROOT/f'translations/{name}_seasonal_ko.json')
            for u in a['units']:
                self.assertLessEqual(len(u['translation'].split('\n')),3)
                for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
                if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
            self.assertFalse(a['review']['release_eligible'])

if __name__=='__main__':unittest.main()
